"""
Main application entry point and lifecycle management.
"""

from PySide6.QtWidgets import QApplication
import sys


class ClueDaddyApp(QApplication):
    """Main application class extending QApplication."""
    
    def __init__(self):
        super().__init__(sys.argv)
        # TODO: Initialize configuration loading
        # TODO: Setup global services
        # TODO: Setup theme and styling
        
    def show_onboarding(self):
        """Display first-time setup."""
        # TODO: Implement onboarding flow
        pass
        
    def show_main_gui(self):
        """Display main interface."""
        # TODO: Implement main GUI
        pass
        
    def register_global_hotkeys(self):
        """Setup system-wide shortcuts."""
        # TODO: Implement global hotkey registration
        pass


def main():
    """Application entry point."""
    app = ClueDaddyApp()
    
    # TODO: Check if first time launch
    # TODO: Show appropriate interface
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())