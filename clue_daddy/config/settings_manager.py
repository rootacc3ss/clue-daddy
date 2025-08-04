"""
Configuration CRUD operations and persistence.
"""

import json
import os
from pathlib import Path


class SettingsManager:
    """Manager for application configuration and settings."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".clue-daddy"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self) -> dict:
        """Load from ~/.clue-daddy/config.json."""
        if not self.config_file.exists():
            return self.get_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.get_default_config()
    
    def save_config(self, config: dict):
        """Persist configuration changes."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            raise Exception(f"Failed to save configuration: {e}")
    
    def get_default_config(self) -> dict:
        """Return default settings."""
        return {
            "gemini_api_key": "",
            "personal_context": "",
            "default_profile_id": None,
            "launch_at_startup": False,
            "accent_color": "#00BCD4",
            "font_size_multiplier": 1.0,
            "default_transparency": 0.65,
            "enable_animations": True,
            "model_name": "gemini-live-2.5-flash-preview",
            "temperature": 0.7,
            "max_tokens": 1000,
            "universal_system_prompt": "",
            "enable_search_tool": True,
            "start_cheating_hotkey": "Ctrl+Shift+Space",
            "transparency_up_hotkey": "Ctrl+Alt+Up",
            "transparency_down_hotkey": "Ctrl+Alt+Down",
            "quick_screenshot_hotkey": "Ctrl+Alt+S",
            "screenshot_frequency_seconds": 2,
            "auto_delete_sessions_days": None
        }
    
    def validate_config(self, config: dict) -> bool:
        """Validate configuration integrity."""
        # TODO: Implement configuration validation
        return True