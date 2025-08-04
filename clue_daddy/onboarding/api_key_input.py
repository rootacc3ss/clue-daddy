"""
API key input dialog for the onboarding process.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QWidget, QFrame, QGraphicsDropShadowEffect,
    QProgressBar, QTextEdit
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor
import logging
import re

try:
    import qtawesome as qta
    ICONS_AVAILABLE = True
except ImportError:
    ICONS_AVAILABLE = False


class ApiKeyValidator(QThread):
    """Thread for validating API key without blocking UI."""
    
    # Signals
    validation_completed = Signal(bool, str)  # success, message
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
        
    def run(self):
        """Run API key validation in background thread."""
        try:
            self.logger.info("Starting API key validation")
            
            # Basic format validation first
            if not self._validate_api_key_format(self.api_key):
                self.validation_completed.emit(False, "Invalid API key format. Please check your key and try again.")
                return
                
            # Test API key with actual API call
            success, message = self._test_api_key(self.api_key)
            self.validation_completed.emit(success, message)
            
        except Exception as e:
            self.logger.error(f"Error during API key validation: {e}")
            self.validation_completed.emit(False, f"Validation error: {str(e)}")
            
    def _validate_api_key_format(self, api_key: str) -> bool:
        """Validate API key format."""
        if not api_key or len(api_key.strip()) == 0:
            return False
            
        # Basic format check for Google API keys
        # Google API keys typically start with "AIza" and are 39 characters long
        api_key = api_key.strip()
        if len(api_key) < 20:  # Minimum reasonable length
            return False
            
        # Check for common patterns
        if api_key.startswith('AIza') and len(api_key) == 39:
            return True
            
        # Allow other formats but with minimum length
        if len(api_key) >= 20:
            return True
            
        return False
        
    def _test_api_key(self, api_key: str) -> tuple[bool, str]:
        """Test API key with actual API call to Google Gemini."""
        try:
            # Import Google GenAI SDK
            try:
                import google.generativeai as genai
            except ImportError:
                self.logger.error("Google GenAI SDK not available")
                return False, "Google GenAI SDK not installed. Please install google-generativeai package."
                
            # Strip whitespace from API key
            api_key = api_key.strip()
            self.logger.info(f"Testing API key of length: {len(api_key)}")
            
            # Configure the API key
            genai.configure(api_key=api_key)
            
            # First, let's check what models are available
            try:
                available_models = list(genai.list_models())
                model_names = [model.name for model in available_models if 'generateContent' in model.supported_generation_methods]
                self.logger.info(f"Available models: {model_names}")
                
                # Try to find the live model or a suitable alternative
                target_model = "gemini-live-2.5-flash-preview"
                if any(target_model in name for name in model_names):
                    # Found exact match
                    model = genai.GenerativeModel(target_model)
                elif any("live" in name.lower() for name in model_names):
                    # Find any live model
                    live_models = [name for name in model_names if "live" in name.lower()]
                    target_model = live_models[0]
                    self.logger.info(f"Using available live model: {target_model}")
                    model = genai.GenerativeModel(target_model)
                elif any("2.5" in name for name in model_names):
                    # Find any 2.5 model
                    v25_models = [name for name in model_names if "2.5" in name]
                    target_model = v25_models[0]
                    self.logger.info(f"Using available 2.5 model: {target_model}")
                    model = genai.GenerativeModel(target_model)
                else:
                    # Fallback to the first available model
                    target_model = model_names[0] if model_names else "gemini-1.5-flash"
                    self.logger.info(f"Using fallback model: {target_model}")
                    model = genai.GenerativeModel(target_model)
                    
            except Exception as list_error:
                self.logger.warning(f"Could not list models: {list_error}")
                # Try with the original model name anyway
                model = genai.GenerativeModel("gemini-live-2.5-flash-preview")
            
            # Test with a simple content generation request
            response = model.generate_content("Hello, please respond with 'API key is working' to validate this connection.")
            
            if response and response.text:
                self.logger.info("API key validation successful")
                return True, "API key validated successfully!"
            else:
                self.logger.warning("API key test returned empty response")
                return False, "API key test failed. Please verify your key is correct."
                
        except Exception as e:
            error_msg = str(e).lower()
            self.logger.error(f"API key test error: {e}")
            
            # Handle specific error types
            if "api_key_invalid" in error_msg or "api key not valid" in error_msg:
                return False, "Invalid API key. Please check your key and try again."
            elif "api_key" in error_msg or "authentication" in error_msg or "unauthorized" in error_msg or "403" in error_msg:
                return False, "Invalid API key. Please check your key and try again."
            elif "quota" in error_msg or "limit" in error_msg or "429" in error_msg:
                return False, "API quota exceeded. Please check your Google Cloud billing."
            elif "network" in error_msg or "connection" in error_msg or "timeout" in error_msg:
                return False, "Network error. Please check your internet connection and try again."
            elif "404" in error_msg or "not found" in error_msg:
                return False, "Model not found. Your API key may not have access to Gemini models."
            elif "illegal header" in error_msg or "metadata" in error_msg:
                return False, "Invalid API key format. Please ensure you copied the key correctly from Google AI Studio."
            else:
                return False, f"API validation failed: {str(e)}"


class ApiKeyInputDialog(QDialog):
    """Dialog for collecting and validating Google Gemini API key."""
    
    # Signals
    api_key_validated = Signal(str)  # Emitted with validated API key
    back_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Setup dialog properties
        self.setWindowTitle("API Key Setup")
        self.setFixedSize(600, 550)
        self.setWindowFlags(Qt.WindowType.Dialog)
        # Remove frameless and translucent background for proper window controls
        
        # Validation thread
        self.validator_thread = None
        
        # Setup UI
        self._setup_ui()
        self._setup_styling()
        self._setup_animations()
        
        self.logger.info("API key input dialog initialized")
        
    def _setup_ui(self):
        """Setup the user interface."""
        # Main layout with proper margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Create main container
        self.container = QFrame()
        self.container.setObjectName("apiKeyContainer")
        container_layout = QVBoxLayout(self.container)
        container_layout.setSpacing(15)
        container_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        header_layout = QHBoxLayout()
        
        if ICONS_AVAILABLE:
            try:
                self.icon_label = QLabel()
                icon = qta.icon('fa5s.key', color='#E53E3E', scale_factor=1.2)
                pixmap = icon.pixmap(48, 48)
                self.icon_label.setPixmap(pixmap)
                header_layout.addWidget(self.icon_label)
            except Exception as e:
                self.logger.warning(f"Could not create icon: {e}")
                
        title_layout = QVBoxLayout()
        self.title_label = QLabel("Google Gemini API Key")
        self.title_label.setObjectName("titleLabel")
        title_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("Step 1 of 2")
        self.subtitle_label.setObjectName("subtitleLabel")
        title_layout.addWidget(self.subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        container_layout.addLayout(header_layout)
        
        # Instructions section
        instructions_text = (
            "Please enter your Google Gemini API key. You can get one from "
            "Google AI Studio (https://makersuite.google.com/app/apikey).\n\n"
            "Your API key will be stored securely on your device and used only "
            "for communicating with Google's AI services."
        )
        self.instructions_label = QLabel(instructions_text)
        self.instructions_label.setObjectName("instructionsLabel")
        self.instructions_label.setWordWrap(True)
        container_layout.addWidget(self.instructions_label)
        
        # API key input section
        input_layout = QVBoxLayout()
        
        self.api_key_label = QLabel("API Key:")
        self.api_key_label.setObjectName("inputLabel")
        input_layout.addWidget(self.api_key_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setObjectName("apiKeyInput")
        self.api_key_input.setPlaceholderText("Enter your Google Gemini API key...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.textChanged.connect(self._on_api_key_changed)
        input_layout.addWidget(self.api_key_input)
        
        # Show/hide API key toggle
        toggle_layout = QHBoxLayout()
        self.show_key_button = QPushButton("Show")
        self.show_key_button.setObjectName("toggleButton")
        self.show_key_button.setMaximumWidth(60)
        self.show_key_button.clicked.connect(self._toggle_api_key_visibility)
        toggle_layout.addStretch()
        toggle_layout.addWidget(self.show_key_button)
        input_layout.addLayout(toggle_layout)
        
        container_layout.addLayout(input_layout)
        
        # Progress bar (hidden initially) - use fixed height to prevent layout shifts
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.setFixedHeight(20)  # Fixed height to prevent layout changes
        container_layout.addWidget(self.progress_bar)
        
        # Status message - use fixed height to prevent layout shifts
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.setVisible(False)
        self.status_label.setMinimumHeight(40)  # Fixed minimum height
        container_layout.addWidget(self.status_label)
        
        # Button section
        button_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("backButton")
        self.back_button.setMinimumSize(100, 40)
        self.back_button.clicked.connect(self._on_back_clicked)
        
        if ICONS_AVAILABLE:
            try:
                back_icon = qta.icon('fa5s.arrow-left', color='#cccccc')
                self.back_button.setIcon(back_icon)
            except Exception as e:
                self.logger.warning(f"Could not set back button icon: {e}")
                
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        
        self.validate_button = QPushButton("Validate & Continue")
        self.validate_button.setObjectName("validateButton")
        self.validate_button.setMinimumSize(150, 40)
        self.validate_button.setEnabled(False)
        self.validate_button.clicked.connect(self._on_validate_clicked)
        
        if ICONS_AVAILABLE:
            try:
                validate_icon = qta.icon('fa5s.check', color='white')
                self.validate_button.setIcon(validate_icon)
            except Exception as e:
                self.logger.warning(f"Could not set validate button icon: {e}")
                
        button_layout.addWidget(self.validate_button)
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(self.container)
        
        # Remove drop shadow for better compatibility
        
    def _setup_styling(self):
        """Apply modern dark theme styling."""
        style = """
        QDialog {
            background-color: #2b2b2b;
        }
        
        #apiKeyContainer {
            background-color: #2b2b2b;
            border: 1px solid #404040;
            border-radius: 15px;
        }
        
        #titleLabel {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
        }
        
        #subtitleLabel {
            font-size: 14px;
            color: #E53E3E;
            margin-top: 5px;
        }
        
        #instructionsLabel {
            font-size: 13px;
            color: #cccccc;
            line-height: 1.4;
            background-color: #363636;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #E53E3E;
        }
        
        #inputLabel {
            font-size: 14px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 5px;
        }
        
        #apiKeyInput {
            background-color: #363636;
            border: 2px solid #404040;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            color: #ffffff;
            font-family: 'Courier New', monospace;
        }
        
        #apiKeyInput:focus {
            border-color: #E53E3E;
            background-color: #404040;
        }
        
        #toggleButton {
            background-color: #404040;
            color: #cccccc;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px 10px;
            font-size: 12px;
        }
        
        #toggleButton:hover {
            background-color: #4a4a4a;
        }
        
        #progressBar {
            background-color: #363636;
            border: 1px solid #404040;
            border-radius: 4px;
            text-align: center;
        }
        
        #progressBar::chunk {
            background-color: #E53E3E;
            border-radius: 3px;
        }
        
        #statusLabel {
            font-size: 13px;
            padding: 10px;
            border-radius: 6px;
        }
        
        #statusLabel[status="success"] {
            color: #4CAF50;
            background-color: rgba(76, 175, 80, 0.1);
            border: 1px solid #4CAF50;
        }
        
        #statusLabel[status="error"] {
            color: #F44336;
            background-color: rgba(244, 67, 54, 0.1);
            border: 1px solid #F44336;
        }
        
        #backButton {
            background-color: #404040;
            color: #cccccc;
            border: 1px solid #555555;
            border-radius: 8px;
            font-size: 14px;
            padding: 10px 20px;
        }
        
        #backButton:hover {
            background-color: #4a4a4a;
            color: #ffffff;
        }
        
        #validateButton {
            background-color: #E53E3E;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            padding: 10px 20px;
        }
        
        #validateButton:hover:enabled {
            background-color: #C53030;
        }
        
        #validateButton:disabled {
            background-color: #555555;
            color: #888888;
        }
        """
        
        self.setStyleSheet(style)
        
    def _setup_animations(self):
        """Setup UI animations."""
        # Fade in animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(400)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def showEvent(self, event):
        """Override show event to trigger animations."""
        super().showEvent(event)
        self._center_on_screen()
        self.fade_animation.start()
        
        # Focus on API key input
        QTimer.singleShot(500, self.api_key_input.setFocus)
        
    def _center_on_screen(self):
        """Center the dialog on the screen."""
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
        else:
            from PySide6.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
            
    def _on_api_key_changed(self, text: str):
        """Handle API key input changes."""
        # Enable validate button if there's text
        self.validate_button.setEnabled(len(text.strip()) > 0)
        
        # Hide status message when user types
        if self.status_label.isVisible():
            self.status_label.setVisible(False)
            
    def _toggle_api_key_visibility(self):
        """Toggle API key visibility."""
        if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_key_button.setText("Hide")
        else:
            self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_key_button.setText("Show")
            
    def _on_back_clicked(self):
        """Handle back button click."""
        self.logger.info("Back button clicked in API key dialog")
        self.back_clicked.emit()
        
    def _on_validate_clicked(self):
        """Handle validate button click."""
        api_key = self.api_key_input.text().strip()
        
        if not api_key:
            self._show_status("Please enter an API key.", "error")
            return
            
        self.logger.info("Starting API key validation")
        
        # Disable UI during validation
        self._set_validation_state(True)
        
        # Start validation in background thread
        self.validator_thread = ApiKeyValidator(api_key)
        self.validator_thread.validation_completed.connect(self._on_validation_completed)
        self.validator_thread.start()
        
    def _on_validation_completed(self, success: bool, message: str):
        """Handle validation completion."""
        self.logger.info(f"API key validation completed: success={success}")
        
        # Re-enable UI
        self._set_validation_state(False)
        
        # Show status message
        status_type = "success" if success else "error"
        self._show_status(message, status_type)
        
        if success:
            # Emit validated API key after a short delay
            QTimer.singleShot(1500, lambda: self.api_key_validated.emit(self.api_key_input.text().strip()))
            
        # Clean up thread
        if self.validator_thread:
            self.validator_thread.deleteLater()
            self.validator_thread = None
            
    def _set_validation_state(self, validating: bool):
        """Set UI state during validation."""
        self.validate_button.setEnabled(not validating)
        self.back_button.setEnabled(not validating)
        self.api_key_input.setEnabled(not validating)
        self.show_key_button.setEnabled(not validating)
        
        self.progress_bar.setVisible(validating)
        
        if validating:
            self.validate_button.setText("Validating...")
            self.status_label.setVisible(False)
        else:
            self.validate_button.setText("Validate & Continue")
            
    def _show_status(self, message: str, status_type: str):
        """Show status message."""
        self.status_label.setText(message)
        self.status_label.setProperty("status", status_type)
        self.status_label.setStyleSheet(self.status_label.styleSheet())  # Refresh style
        self.status_label.setVisible(True)
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            if self.validate_button.isEnabled():
                self._on_validate_clicked()
        elif event.key() == Qt.Key.Key_Escape:
            self._on_back_clicked()
        else:
            super().keyPressEvent(event)
            
    def closeEvent(self, event):
        """Handle close event."""
        # Clean up validation thread if running
        if self.validator_thread and self.validator_thread.isRunning():
            self.validator_thread.terminate()
            self.validator_thread.wait(3000)  # Wait up to 3 seconds
            
        super().closeEvent(event)