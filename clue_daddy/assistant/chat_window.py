"""
Floating assistant chat interface.
"""

from PySide6.QtWidgets import QWidget
from typing import Optional


class AssistantChatWindow(QWidget):
    """Floating chat window for AI assistant interaction."""
    
    def __init__(self, profile=None):
        super().__init__()
        # TODO: Setup floating window
        # TODO: Initialize AI client with profile context
        pass
    
    def start_audio_monitoring(self):
        """Begin voice detection."""
        # TODO: Implement audio monitoring
        pass
    
    def start_screenshot_capture(self):
        """Begin periodic screen capture."""
        # TODO: Implement screenshot capture
        pass
    
    def send_user_message(self, message: str, screenshot: Optional[bytes] = None):
        """Send manual user input with optional screenshot."""
        # TODO: Implement user message sending
        pass
    
    def process_voice_input(self, audio_data: bytes):
        """Handle detected speech."""
        # TODO: Implement voice input processing
        pass