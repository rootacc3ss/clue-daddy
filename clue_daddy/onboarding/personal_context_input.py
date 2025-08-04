"""
Personal context input dialog for the onboarding process.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTextEdit, QWidget, QFrame, QGraphicsDropShadowEffect,
    QScrollArea
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QTextCursor
import logging

try:
    import qtawesome as qta
    ICONS_AVAILABLE = True
except ImportError:
    ICONS_AVAILABLE = False


class PersonalContextInputDialog(QDialog):
    """Dialog for collecting personal context and resume information."""
    
    # Signals
    context_saved = Signal(str)  # Emitted with saved context
    back_clicked = Signal()
    
    # Constants
    MIN_CONTEXT_LENGTH = 50
    MAX_CONTEXT_LENGTH = 10000
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Setup dialog properties
        self.setWindowTitle("Personal Context Setup")
        self.setFixedSize(750, 700)
        self.setWindowFlags(Qt.WindowType.Dialog)
        # Remove frameless and translucent background for proper window controls
        
        # Setup UI
        self._setup_ui()
        self._setup_styling()
        self._setup_animations()
        
        self.logger.info("Personal context input dialog initialized")
        
    def _setup_ui(self):
        """Setup the user interface."""
        # Main layout with proper margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # Create main container
        self.container = QFrame()
        self.container.setObjectName("contextContainer")
        container_layout = QVBoxLayout(self.container)
        container_layout.setSpacing(12)
        container_layout.setContentsMargins(25, 25, 25, 25)
        
        # Header section
        header_layout = QHBoxLayout()
        
        if ICONS_AVAILABLE:
            try:
                self.icon_label = QLabel()
                icon = qta.icon('fa5s.user-edit', color='#E53E3E', scale_factor=1.2)
                pixmap = icon.pixmap(48, 48)
                self.icon_label.setPixmap(pixmap)
                header_layout.addWidget(self.icon_label)
            except Exception as e:
                self.logger.warning(f"Could not create icon: {e}")
                
        title_layout = QVBoxLayout()
        self.title_label = QLabel("Personal Context")
        self.title_label.setObjectName("titleLabel")
        title_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel("Step 2 of 2")
        self.subtitle_label.setObjectName("subtitleLabel")
        title_layout.addWidget(self.subtitle_label)
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        container_layout.addLayout(header_layout)
        
        # Instructions section
        instructions_text = (
            "Here, write a description of yourself, copy and paste your resume "
            "and add any other important context. This will be important for "
            "acing interviews and tailoring answers to you. You can change this "
            "later in the settings."
        )
        self.instructions_label = QLabel(instructions_text)
        self.instructions_label.setObjectName("instructionsLabel")
        self.instructions_label.setWordWrap(True)
        container_layout.addWidget(self.instructions_label)
        
        # Label with character count
        label_layout = QHBoxLayout()
        self.context_label = QLabel("Personal Context & Resume:")
        self.context_label.setObjectName("inputLabel")
        label_layout.addWidget(self.context_label)
        
        label_layout.addStretch()
        
        self.char_count_label = QLabel("0 characters")
        self.char_count_label.setObjectName("charCountLabel")
        label_layout.addWidget(self.char_count_label)
        
        container_layout.addLayout(label_layout)
        
        # Text area with proper sizing
        self.context_input = QTextEdit()
        self.context_input.setObjectName("contextInput")
        self.context_input.setMinimumHeight(200)
        self.context_input.setMaximumHeight(200)
        # Enable word wrap and proper scrolling
        self.context_input.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        # Set placeholder text with examples
        placeholder_text = (
            "Example:\n\n"
            "I am a software engineer with 5 years of experience in full-stack development. "
            "I specialize in Python, JavaScript, and React.\n\n"
            "EXPERIENCE:\n"
            "• Senior Software Engineer at TechCorp (2021-2024)\n"
            "• Full-Stack Developer at StartupXYZ (2019-2021)\n\n"
            "SKILLS:\n"
            "• Programming: Python, JavaScript, TypeScript, SQL\n"
            "• Frameworks: React, Django, FastAPI, Node.js\n\n"
            "Paste your resume and add any other relevant context here..."
        )
        self.context_input.setPlaceholderText(placeholder_text)
        self.context_input.textChanged.connect(self._on_context_changed)
        
        container_layout.addWidget(self.context_input)
        
        # Tips section - add directly to container layout
        tips_text = (
            "💡 Tips:\n"
            "• Include your work experience, skills, and achievements\n"
            "• Add specific examples and metrics when possible\n"
            "• Mention your career goals and interests\n"
            "• Include any relevant certifications or education"
        )
        self.tips_label = QLabel(tips_text)
        self.tips_label.setObjectName("tipsLabel")
        self.tips_label.setWordWrap(True)
        container_layout.addWidget(self.tips_label)
        
        # Status message
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setWordWrap(True)
        self.status_label.setVisible(False)
        container_layout.addWidget(self.status_label)
        
        # Add stretch space to ensure proper spacing
        container_layout.addStretch()
        
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
        
        self.save_button = QPushButton("Save & Complete Setup")
        self.save_button.setObjectName("saveButton")
        self.save_button.setMinimumSize(180, 40)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self._on_save_clicked)
        
        if ICONS_AVAILABLE:
            try:
                save_icon = qta.icon('fa5s.check-circle', color='white')
                self.save_button.setIcon(save_icon)
            except Exception as e:
                self.logger.warning(f"Could not set save button icon: {e}")
                
        button_layout.addWidget(self.save_button)
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
        
        #contextContainer {
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
        }
        
        #charCountLabel {
            font-size: 12px;
            color: #888888;
        }
        
        #charCountLabel[status="valid"] {
            color: #4CAF50;
        }
        
        #charCountLabel[status="invalid"] {
            color: #F44336;
        }
        
        #contextInput {
            background-color: #363636;
            border: 2px solid #404040;
            border-radius: 8px;
            padding: 15px;
            font-size: 14px;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.4;
        }
        
        #contextInput:focus {
            border-color: #E53E3E;
            background-color: #404040;
        }
        
        #tipsLabel {
            font-size: 12px;
            color: #aaaaaa;
            background-color: rgba(229, 62, 62, 0.1);
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid #E53E3E;
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
        
        #statusLabel[status="warning"] {
            color: #FF9800;
            background-color: rgba(255, 152, 0, 0.1);
            border: 1px solid #FF9800;
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
        
        #saveButton {
            background-color: #E53E3E;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            padding: 10px 20px;
        }
        
        #saveButton:hover:enabled {
            background-color: #C53030;
        }
        
        #saveButton:disabled {
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
        
        # Focus on context input
        QTimer.singleShot(500, self.context_input.setFocus)
        
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
            
    def _on_context_changed(self):
        """Handle context input changes."""
        text = self.context_input.toPlainText()
        char_count = len(text)
        
        # Update character count
        self.char_count_label.setText(f"{char_count:,} characters")
        
        # Update character count styling
        if char_count >= self.MIN_CONTEXT_LENGTH and char_count <= self.MAX_CONTEXT_LENGTH:
            self.char_count_label.setProperty("status", "valid")
            self.save_button.setEnabled(True)
            status = "valid"
        elif char_count > self.MAX_CONTEXT_LENGTH:
            self.char_count_label.setProperty("status", "invalid")
            self.save_button.setEnabled(False)
            status = "invalid"
        else:
            self.char_count_label.setProperty("status", "")
            self.save_button.setEnabled(False)
            status = "insufficient"
            
        # Refresh styling
        self.char_count_label.setStyleSheet(self.char_count_label.styleSheet())
        
        # Show/hide status messages
        if char_count > self.MAX_CONTEXT_LENGTH:
            self._show_status(
                f"Context is too long. Please reduce to {self.MAX_CONTEXT_LENGTH:,} characters or less.",
                "error"
            )
        elif char_count > 0 and char_count < self.MIN_CONTEXT_LENGTH:
            remaining = self.MIN_CONTEXT_LENGTH - char_count
            self._show_status(
                f"Please add at least {remaining} more characters to provide sufficient context.",
                "warning"
            )
        else:
            self.status_label.setVisible(False)
            
    def _on_back_clicked(self):
        """Handle back button click."""
        self.logger.info("Back button clicked in personal context dialog")
        self.back_clicked.emit()
        
    def _on_save_clicked(self):
        """Handle save button click."""
        context = self.context_input.toPlainText().strip()
        
        if not self._validate_context(context):
            return
            
        self.logger.info("Personal context saved successfully")
        
        # Show success message briefly
        self._show_status("Context saved successfully!", "success")
        
        # Emit saved context after a short delay
        QTimer.singleShot(1000, lambda: self.context_saved.emit(context))
        
    def _validate_context(self, context: str) -> bool:
        """Validate the personal context."""
        if len(context) < self.MIN_CONTEXT_LENGTH:
            self._show_status(
                f"Please provide at least {self.MIN_CONTEXT_LENGTH} characters of context.",
                "error"
            )
            return False
            
        if len(context) > self.MAX_CONTEXT_LENGTH:
            self._show_status(
                f"Context is too long. Please reduce to {self.MAX_CONTEXT_LENGTH:,} characters or less.",
                "error"
            )
            return False
            
        # Check for meaningful content (not just whitespace or repeated characters)
        if len(set(context.lower().replace(' ', ''))) < 10:
            self._show_status(
                "Please provide more meaningful and varied content in your context.",
                "error"
            )
            return False
            
        return True
        
    def _show_status(self, message: str, status_type: str):
        """Show status message."""
        self.status_label.setText(message)
        self.status_label.setProperty("status", status_type)
        self.status_label.setStyleSheet(self.status_label.styleSheet())  # Refresh style
        self.status_label.setVisible(True)
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Escape:
            self._on_back_clicked()
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Return:
            # Ctrl+Enter to save
            if self.save_button.isEnabled():
                self._on_save_clicked()
        else:
            super().keyPressEvent(event)
            
    def get_context_text(self) -> str:
        """Get the current context text."""
        return self.context_input.toPlainText().strip()
        
    def set_context_text(self, text: str):
        """Set the context text."""
        self.context_input.setPlainText(text)
        
    def clear_context(self):
        """Clear the context input."""
        self.context_input.clear()