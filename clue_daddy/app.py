"""
Main application entry point and lifecycle management.
"""

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer, QObject, Signal
from PySide6.QtGui import QIcon
import sys
import logging
import traceback
import os
from pathlib import Path

# Import configuration and theme management
try:
    import pyqtdarktheme
    DARK_THEME_AVAILABLE = True
except ImportError:
    DARK_THEME_AVAILABLE = False

# Import qtawesome for icons
try:
    import qtawesome as qta
    ICONS_AVAILABLE = True
except ImportError:
    ICONS_AVAILABLE = False


class GlobalExceptionHandler(QObject):
    """Global exception handler for unhandled exceptions."""
    
    exception_occurred = Signal(str, str)
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle unhandled exceptions."""
        if issubclass(exc_type, KeyboardInterrupt):
            # Allow KeyboardInterrupt to pass through
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        # Log the exception
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.error(f"Unhandled exception: {error_msg}")
        
        # Emit signal for UI handling
        self.exception_occurred.emit(str(exc_value), error_msg)


class ClueDaddyApp(QApplication):
    """Main application class extending QApplication."""
    
    def __init__(self):
        super().__init__(sys.argv)
        
        # Setup application metadata
        self.setApplicationName("Clue Daddy")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("Clue Daddy")
        self.setOrganizationDomain("cluedaddy.app")
        
        # Initialize logging
        self._setup_logging()
        
        # Initialize global exception handling
        self._setup_exception_handling()
        
        # Initialize configuration
        from .config import SettingsManager
        self.settings_manager = SettingsManager()
        self.config = self._load_configuration()
        
        # Setup theme and styling
        self._setup_theme()
        
        # Initialize window management
        self.current_window = None
        self.onboarding_window = None
        self.main_window = None
        
        # Setup global services
        self._setup_global_services()
        
        self.logger.info("Clue Daddy application initialized")
        
    def _setup_logging(self):
        """Setup application-wide logging."""
        # Create logs directory
        log_dir = Path.home() / ".clue-daddy" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging configuration
        log_file = log_dir / "app.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging system initialized")
        
    def _setup_exception_handling(self):
        """Setup global exception handling."""
        self.exception_handler = GlobalExceptionHandler()
        self.exception_handler.exception_occurred.connect(self._handle_global_exception)
        
        # Set the global exception hook
        sys.excepthook = self.exception_handler.handle_exception
        
    def _handle_global_exception(self, error_message: str, full_traceback: str):
        """Handle global exceptions with user-friendly dialog."""
        self.logger.error(f"Global exception handled: {error_message}")
        
        # Show user-friendly error dialog
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Unexpected Error")
        msg_box.setText("An unexpected error occurred in Clue Daddy.")
        msg_box.setInformativeText(f"Error: {error_message}")
        msg_box.setDetailedText(full_traceback)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
        
    def _load_configuration(self):
        """Load application configuration."""
        try:
            config = self.settings_manager.load_config()
            self.logger.info("Configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            # Return default config on error
            from .config import AppConfig
            return AppConfig()
        
    def _setup_theme(self):
        """Setup application theme and styling."""
        try:
            if DARK_THEME_AVAILABLE:
                # Apply dark theme
                pyqtdarktheme.setup_theme("dark")
                self.logger.info("Dark theme applied successfully using pyqtdarktheme")
            else:
                self.logger.warning("pyqtdarktheme not available, using default theme")
                
            # Setup application icon if available
            if ICONS_AVAILABLE:
                try:
                    icon = qta.icon('fa5s.user-secret', color='#00BCD4')
                    self.setWindowIcon(icon)
                    self.logger.info("Application icon set successfully")
                except Exception as e:
                    self.logger.warning(f"Could not set application icon: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error setting up theme: {e}")
            
    def _setup_global_services(self):
        """Setup global application services."""
        # Initialize services that need to run throughout the application lifecycle
        self.logger.info("Global services initialized")
        
        # Setup cleanup timer for periodic maintenance
        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self._periodic_cleanup)
        self.cleanup_timer.start(300000)  # 5 minutes
        
    def _periodic_cleanup(self):
        """Perform periodic cleanup tasks."""
        # This can be used for memory cleanup, temporary file removal, etc.
        self.logger.debug("Performing periodic cleanup")
        
    def show_onboarding(self):
        """Display first-time setup."""
        self.logger.info("Showing onboarding interface")
        
        # Close current window if any
        if self.current_window:
            self.current_window.close()
            
        # This will be implemented in task 3.1
        # For now, create a placeholder
        from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
        
        self.onboarding_window = QWidget()
        self.onboarding_window.setWindowTitle("Welcome to Clue Daddy!")
        self.onboarding_window.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        title_label = QLabel("Welcome to Clue Daddy!")
        subtitle_label = QLabel("Let's get to cheating.")
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        self.onboarding_window.setLayout(layout)
        self.onboarding_window.show()
        
        # Center the window
        self._center_window(self.onboarding_window)
        
        self.current_window = self.onboarding_window
        
    def show_main_gui(self):
        """Display main interface."""
        self.logger.info("Showing main GUI interface")
        
        # Close current window if any
        if self.current_window:
            self.current_window.close()
            
        # This will be implemented in task 4.1
        # For now, create a placeholder
        from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
        
        self.main_window = QWidget()
        self.main_window.setWindowTitle("Clue Daddy - Main Interface")
        self.main_window.setFixedSize(600, 500)
        
        layout = QVBoxLayout()
        label = QLabel("Main GUI - Coming Soon!")
        layout.addWidget(label)
        
        self.main_window.setLayout(layout)
        self.main_window.show()
        
        # Center the window
        self._center_window(self.main_window)
        
        self.current_window = self.main_window
        
    def _center_window(self, window):
        """Center a window on the screen."""
        screen = self.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = window.frameGeometry()
        
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        window.move(window_geometry.topLeft())
        
    def register_global_hotkeys(self):
        """Setup system-wide shortcuts."""
        # This will be implemented in task 13.1
        self.logger.info("Global hotkey registration placeholder - will be implemented in task 13.1")
        
    def is_first_time_launch(self):
        """Check if this is the first time the application is launched."""
        return not self.config.first_time_setup_completed
        
    def cleanup_and_exit(self):
        """Perform cleanup before application exit."""
        self.logger.info("Performing application cleanup")
        
        # Stop cleanup timer
        if hasattr(self, 'cleanup_timer'):
            self.cleanup_timer.stop()
            
        # Close all windows
        if self.current_window:
            self.current_window.close()
            
        self.logger.info("Application cleanup completed")
        
    def save_configuration(self):
        """Save current configuration to file."""
        try:
            success = self.settings_manager.save_config(self.config)
            if success:
                self.logger.info("Configuration saved successfully")
            else:
                self.logger.error("Failed to save configuration")
            return success
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False


def main():
    """Application entry point."""
    try:
        app = ClueDaddyApp()
        
        # Check if first time launch and show appropriate interface
        if app.is_first_time_launch():
            app.show_onboarding()
        else:
            app.show_main_gui()
        
        # Setup cleanup on exit
        app.aboutToQuit.connect(app.cleanup_and_exit)
        
        return app.exec()
        
    except Exception as e:
        print(f"Failed to start Clue Daddy: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())