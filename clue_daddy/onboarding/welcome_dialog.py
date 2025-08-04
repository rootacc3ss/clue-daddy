"""
Welcome dialog for the onboarding process.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QWidget, QFrame, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QPixmap, QPainter, QColor
import logging

try:
    import qtawesome as qta
    ICONS_AVAILABLE = True
except ImportError:
    ICONS_AVAILABLE = False


class WelcomeDialog(QDialog):
    """Welcome dialog with modern styling and animations."""
    
    # Signals
    continue_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Setup dialog properties
        self.setWindowTitle("Welcome to Clue Daddy!")
        self.setFixedSize(550, 450)
        self.setWindowFlags(Qt.WindowType.Dialog)
        # Remove frameless and translucent background for proper window controls
        
        # Setup UI
        self._setup_ui()
        self._setup_styling()
        self._setup_animations()
        
        self.logger.info("Welcome dialog initialized")
        
    def _setup_ui(self):
        """Setup the user interface."""
        # Main layout with proper margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Create main container with rounded corners
        self.container = QFrame()
        self.container.setObjectName("welcomeContainer")
        container_layout = QVBoxLayout(self.container)
        container_layout.setSpacing(15)
        container_layout.setContentsMargins(25, 25, 25, 25)
        
        # Icon section
        icon_layout = QHBoxLayout()
        icon_layout.addStretch()
        
        if ICONS_AVAILABLE:
            try:
                # Create icon label
                self.icon_label = QLabel()
                icon = qta.icon('fa5s.user-secret', color='#E53E3E', scale_factor=1.5)
                pixmap = icon.pixmap(64, 64)
                self.icon_label.setPixmap(pixmap)
                self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                icon_layout.addWidget(self.icon_label)
            except Exception as e:
                self.logger.warning(f"Could not create icon: {e}")
                
        icon_layout.addStretch()
        container_layout.addLayout(icon_layout)
        
        # Title section
        self.title_label = QLabel("Welcome to Clue Daddy!")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.title_label)
        
        # Subtitle section
        self.subtitle_label = QLabel("Let's get to cheating.")
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.subtitle_label)
        
        # Description section
        description_text = (
            "Welcome to your AI-powered assistant for meetings, interviews, "
            "presentations, and more. Let's set up your account to get started."
        )
        self.description_label = QLabel(description_text)
        self.description_label.setObjectName("descriptionLabel")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setWordWrap(True)
        container_layout.addWidget(self.description_label)
        
        # Add some stretch space
        container_layout.addStretch()
        
        # Button section
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.continue_button = QPushButton("Get Started")
        self.continue_button.setObjectName("continueButton")
        self.continue_button.setMinimumSize(120, 40)
        self.continue_button.clicked.connect(self._on_continue_clicked)
        
        if ICONS_AVAILABLE:
            try:
                button_icon = qta.icon('fa5s.arrow-right', color='white')
                self.continue_button.setIcon(button_icon)
            except Exception as e:
                self.logger.warning(f"Could not set button icon: {e}")
                
        button_layout.addWidget(self.continue_button)
        button_layout.addStretch()
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
        
        #welcomeContainer {
            background-color: #2b2b2b;
            border: 1px solid #404040;
            border-radius: 15px;
        }
        
        #titleLabel {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 5px;
        }
        
        #subtitleLabel {
            font-size: 16px;
            color: #E53E3E;
            font-style: italic;
            margin-bottom: 10px;
        }
        
        #descriptionLabel {
            font-size: 14px;
            color: #cccccc;
            line-height: 1.4;
            margin-bottom: 10px;
        }
        
        #continueButton {
            background-color: #E53E3E;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            padding: 10px 20px;
        }
        
        #continueButton:hover {
            background-color: #C53030;
            transform: translateY(-1px);
        }
        
        #continueButton:pressed {
            background-color: #9C1A1A;
            transform: translateY(0px);
        }
        """
        
        self.setStyleSheet(style)
        
    def _setup_animations(self):
        """Setup entrance animations."""
        # Fade in animation
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Scale animation for container
        self.scale_animation = QPropertyAnimation(self.container, b"geometry")
        self.scale_animation.setDuration(400)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutBack)
        
    def showEvent(self, event):
        """Override show event to trigger animations."""
        super().showEvent(event)
        
        # Center the dialog
        self._center_on_screen()
        
        # Start animations
        self.fade_animation.start()
        
        # Setup scale animation
        final_geometry = self.container.geometry()
        start_geometry = QRect(
            final_geometry.x() + final_geometry.width() // 4,
            final_geometry.y() + final_geometry.height() // 4,
            final_geometry.width() // 2,
            final_geometry.height() // 2
        )
        
        self.scale_animation.setStartValue(start_geometry)
        self.scale_animation.setEndValue(final_geometry)
        self.scale_animation.start()
        
    def _center_on_screen(self):
        """Center the dialog on the screen."""
        if self.parent():
            # Center relative to parent
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)
        else:
            # Center on screen
            from PySide6.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
            
    def _on_continue_clicked(self):
        """Handle continue button click."""
        self.logger.info("Continue button clicked in welcome dialog")
        self.continue_clicked.emit()
        
    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self._on_continue_clicked()
        elif event.key() == Qt.Key.Key_Escape:
            # Don't allow escape to close during onboarding
            pass
        else:
            super().keyPressEvent(event)