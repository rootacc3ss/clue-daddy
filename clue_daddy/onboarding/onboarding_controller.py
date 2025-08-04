"""
Onboarding controller to manage the setup flow.
"""

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QApplication, QMessageBox
import logging
from typing import Optional, Dict, Any

# Import dialogs locally to prevent premature instantiation


class OnboardingController(QObject):
    """Controller to manage the onboarding flow and navigation between steps."""
    
    # Signals
    onboarding_completed = Signal(dict)  # Emitted with collected data
    onboarding_cancelled = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        
        # Current dialog reference
        self.current_dialog = None
        
        # Collected onboarding data
        self.onboarding_data = {
            'gemini_api_key': '',
            'personal_context': '',
            'first_time_setup_completed': True
        }
        
        # Dialog instances
        self.welcome_dialog = None
        self.api_key_dialog = None
        self.context_dialog = None
        
        self.logger.info("Onboarding controller initialized")
        
    def start_onboarding(self):
        """Begin the onboarding setup flow."""
        self.logger.info("Starting onboarding flow")
        
        # Reset data
        self.onboarding_data = {
            'gemini_api_key': '',
            'personal_context': '',
            'first_time_setup_completed': True
        }
        
        # Show welcome dialog
        self._show_welcome_dialog()
        
    def _show_welcome_dialog(self):
        """Show the welcome dialog."""
        self.logger.info("Showing welcome dialog")
        
        # Close current dialog if any
        self._close_current_dialog()
        
        # Create and show welcome dialog
        from .welcome_dialog import WelcomeDialog
        self.welcome_dialog = WelcomeDialog()
        self.welcome_dialog.continue_clicked.connect(self._on_welcome_continue)
        self.welcome_dialog.finished.connect(self._on_dialog_finished)
        
        self.current_dialog = self.welcome_dialog
        self.welcome_dialog.show()
        
    def _show_api_key_dialog(self):
        """Show the API key input dialog."""
        self.logger.info("Showing API key input dialog")
        
        # Close current dialog
        self._close_current_dialog()
        
        # Create and show API key dialog
        from .api_key_input import ApiKeyInputDialog
        self.api_key_dialog = ApiKeyInputDialog()
        self.api_key_dialog.api_key_validated.connect(self._on_api_key_validated)
        self.api_key_dialog.back_clicked.connect(self._on_api_key_back)
        self.api_key_dialog.finished.connect(self._on_dialog_finished)
        
        self.current_dialog = self.api_key_dialog
        self.api_key_dialog.show()
        
    def _show_personal_context_dialog(self):
        """Show the personal context input dialog."""
        self.logger.info("Showing personal context input dialog")
        
        # Close current dialog
        self._close_current_dialog()
        
        # Create and show context dialog
        from .personal_context_input import PersonalContextInputDialog
        self.context_dialog = PersonalContextInputDialog()
        self.context_dialog.context_saved.connect(self._on_context_saved)
        self.context_dialog.back_clicked.connect(self._on_context_back)
        self.context_dialog.finished.connect(self._on_dialog_finished)
        
        self.current_dialog = self.context_dialog
        self.context_dialog.show()
        
    def _close_current_dialog(self):
        """Close the current dialog if any."""
        if self.current_dialog:
            try:
                # Disconnect all signals first to prevent issues
                try:
                    self.current_dialog.disconnect()
                except:
                    pass  # Ignore disconnect errors
                # Hide and close the dialog
                self.current_dialog.hide()
                self.current_dialog.close()
                # Schedule for deletion
                self.current_dialog.deleteLater()
            except Exception as e:
                self.logger.warning(f"Error closing current dialog: {e}")
            finally:
                self.current_dialog = None
                
        # Also clean up individual dialog references
        if hasattr(self, 'welcome_dialog') and self.welcome_dialog:
            try:
                self.welcome_dialog.disconnect()
                self.welcome_dialog.hide()
                self.welcome_dialog.close()
                self.welcome_dialog.deleteLater()
            except:
                pass
            self.welcome_dialog = None
            
        if hasattr(self, 'api_key_dialog') and self.api_key_dialog:
            try:
                self.api_key_dialog.disconnect()
                self.api_key_dialog.hide()
                self.api_key_dialog.close()
                self.api_key_dialog.deleteLater()
            except:
                pass
            self.api_key_dialog = None
            
        if hasattr(self, 'context_dialog') and self.context_dialog:
            try:
                self.context_dialog.disconnect()
                self.context_dialog.hide()
                self.context_dialog.close()
                self.context_dialog.deleteLater()
            except:
                pass
            self.context_dialog = None
                
    def _on_welcome_continue(self):
        """Handle welcome dialog continue."""
        self.logger.info("Welcome dialog continue clicked")
        self._show_api_key_dialog()
        
    def _on_api_key_validated(self, api_key: str):
        """Handle validated API key."""
        self.logger.info("API key validated successfully")
        self.onboarding_data['gemini_api_key'] = api_key
        self._show_personal_context_dialog()
        
    def _on_api_key_back(self):
        """Handle API key dialog back button."""
        self.logger.info("API key dialog back clicked")
        self._show_welcome_dialog()
        
    def _on_context_saved(self, context: str):
        """Handle personal context saved."""
        self.logger.info("Personal context saved successfully")
        self.onboarding_data['personal_context'] = context
        self._complete_onboarding()
        
    def _on_context_back(self):
        """Handle context dialog back button."""
        self.logger.info("Context dialog back clicked")
        self._show_api_key_dialog()
        
    def _on_dialog_finished(self, result):
        """Handle dialog finished event."""
        if result == 0:  # Rejected/cancelled
            self.logger.info("Dialog was cancelled")
            # Don't emit cancelled signal during normal flow
            
    def _complete_onboarding(self):
        """Complete the onboarding process."""
        self.logger.info("Completing onboarding process")
        
        # Close current dialog
        self._close_current_dialog()
        
        # Show completion message
        self._show_completion_message()
        
        # Emit completion signal with collected data
        self.onboarding_completed.emit(self.onboarding_data)
        
    def _show_completion_message(self):
        """Show onboarding completion message."""
        try:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Setup Complete!")
            msg_box.setText("Welcome to Clue Daddy!")
            msg_box.setInformativeText(
                "Your setup is complete. You're now ready to start using "
                "Clue Daddy for your meetings, interviews, and more!"
            )
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            
            # Apply dark theme styling
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QMessageBox QPushButton {
                    background-color: #E53E3E;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QMessageBox QPushButton:hover {
                    background-color: #C53030;
                }
            """)
            
            msg_box.exec()
            
        except Exception as e:
            self.logger.error(f"Error showing completion message: {e}")
            
    def cancel_onboarding(self):
        """Cancel the onboarding process."""
        self.logger.info("Onboarding cancelled")
        
        # Close current dialog
        self._close_current_dialog()
        
        # Emit cancelled signal
        self.onboarding_cancelled.emit()
        
    def get_collected_data(self) -> Dict[str, Any]:
        """Get the collected onboarding data."""
        return self.onboarding_data.copy()
        
    def cleanup(self):
        """Cleanup resources."""
        self.logger.info("Cleaning up onboarding controller")
        self._close_current_dialog()