"""
Primary interface with four main buttons and past sessions chat.
"""

from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    """Main application window with central navigation."""
    
    def __init__(self):
        super().__init__()
        # TODO: Setup UI layout
        # TODO: Initialize past sessions chat
        pass
    
    def start_cheating_clicked(self):
        """Navigate to profile selection."""
        # TODO: Implement start cheating handler
        pass
    
    def past_sessions_clicked(self):
        """Open sessions management."""
        # TODO: Implement past sessions handler
        pass
    
    def context_base_clicked(self):
        """Open profile management."""
        # TODO: Implement context base handler
        pass
    
    def settings_clicked(self):
        """Open settings panel."""
        # TODO: Implement settings handler
        pass