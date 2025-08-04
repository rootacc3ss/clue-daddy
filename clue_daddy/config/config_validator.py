"""
Configuration validation and default value management.
"""

import re
from typing import Any, Dict, List, Optional, Tuple
import logging


class ConfigValidator:
    """Validates configuration values and provides defaults."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def validate_config(self, config_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate entire configuration dictionary.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate API keys
        if not self._validate_api_key(config_dict.get("gemini_api_key", "")):
            errors.append("Invalid or missing Gemini API key")
            
        # Perplexity API key is optional, but validate if provided
        perplexity_key = config_dict.get("perplexity_api_key", "")
        if perplexity_key and not self._validate_api_key(perplexity_key):
            errors.append("Invalid Perplexity API key format")
            
        # Validate appearance settings
        if not self._validate_color(config_dict.get("accent_color", "")):
            errors.append("Invalid accent color format")
            
        if not self._validate_range(config_dict.get("font_size_multiplier", 1.0), 0.5, 2.0):
            errors.append("Font size multiplier must be between 0.5 and 2.0")
            
        if not self._validate_range(config_dict.get("default_transparency", 0.65), 0.1, 1.0):
            errors.append("Default transparency must be between 0.1 and 1.0")
            
        # Validate AI settings
        if not self._validate_range(config_dict.get("temperature", 0.7), 0.0, 1.0):
            errors.append("Temperature must be between 0.0 and 1.0")
            
        if not self._validate_range(config_dict.get("max_tokens", 1000), 1, 10000):
            errors.append("Max tokens must be between 1 and 10000")
            
        # Validate hotkeys
        hotkeys = [
            "start_cheating_hotkey",
            "transparency_up_hotkey", 
            "transparency_down_hotkey",
            "quick_screenshot_hotkey"
        ]
        
        for hotkey_name in hotkeys:
            if not self._validate_hotkey(config_dict.get(hotkey_name, "")):
                errors.append(f"Invalid hotkey format for {hotkey_name}")
                
        # Validate privacy settings
        screenshot_freq = config_dict.get("screenshot_frequency_seconds", 2)
        if not self._validate_range(screenshot_freq, 1, 60):
            errors.append("Screenshot frequency must be between 1 and 60 seconds")
            
        auto_delete_days = config_dict.get("auto_delete_sessions_days")
        if auto_delete_days is not None and not self._validate_range(auto_delete_days, 1, 365):
            errors.append("Auto delete sessions days must be between 1 and 365")
            
        is_valid = len(errors) == 0
        return is_valid, errors
        
    def _validate_api_key(self, api_key: str) -> bool:
        """Validate Gemini API key format."""
        if not api_key or not isinstance(api_key, str):
            return False
            
        # Basic validation - Gemini API keys typically start with certain patterns
        # This is a basic check, actual validation would require API call
        return len(api_key.strip()) > 10
        
    def _validate_color(self, color: str) -> bool:
        """Validate hex color format."""
        if not color or not isinstance(color, str):
            return False
            
        # Check hex color format (#RRGGBB or #RGB)
        hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return bool(re.match(hex_pattern, color))
        
    def _validate_range(self, value: Any, min_val: float, max_val: float) -> bool:
        """Validate that a numeric value is within range."""
        try:
            num_value = float(value)
            return min_val <= num_value <= max_val
        except (ValueError, TypeError):
            return False
            
    def _validate_hotkey(self, hotkey: str) -> bool:
        """Validate hotkey format."""
        if not hotkey or not isinstance(hotkey, str):
            return False
            
        # Basic hotkey validation - should contain modifier + key
        valid_modifiers = ['Ctrl', 'Alt', 'Shift', 'Meta', 'Win']
        parts = hotkey.split('+')
        
        if len(parts) < 2:
            return False
            
        # Check if at least one modifier is present
        has_modifier = any(part.strip() in valid_modifiers for part in parts[:-1])
        
        # Check if last part is a valid key (basic check)
        key = parts[-1].strip()
        valid_key = len(key) >= 1 and (key.isalnum() or key in ['Space', 'Enter', 'Tab', 'Escape'])
        
        return has_modifier and valid_key
        
    def apply_defaults(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values to missing configuration keys."""
        from .app_config import AppConfig
        
        # Create default config
        default_config = AppConfig()
        default_dict = default_config.to_dict()
        
        # Merge with provided config, keeping existing values
        result = default_dict.copy()
        result.update(config_dict)
        
        return result
        
    def sanitize_config(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize configuration values."""
        sanitized = config_dict.copy()
        
        # Sanitize string values
        string_keys = [
            "gemini_api_key", "perplexity_api_key", "personal_context", "accent_color",
            "model_name", "universal_system_prompt", "start_cheating_hotkey",
            "transparency_up_hotkey", "transparency_down_hotkey", "quick_screenshot_hotkey"
        ]
        
        for key in string_keys:
            if key in sanitized and isinstance(sanitized[key], str):
                sanitized[key] = sanitized[key].strip()
                
        # Sanitize numeric values
        numeric_keys = {
            "font_size_multiplier": (0.5, 2.0, 1.0),
            "default_transparency": (0.1, 1.0, 0.65),
            "temperature": (0.0, 1.0, 0.7),
            "max_tokens": (1, 10000, 1000),
            "screenshot_frequency_seconds": (1, 60, 2),
        }
        
        for key, (min_val, max_val, default_val) in numeric_keys.items():
            if key in sanitized:
                try:
                    value = float(sanitized[key])
                    sanitized[key] = max(min_val, min(max_val, value))
                except (ValueError, TypeError):
                    sanitized[key] = default_val
                    
        return sanitized