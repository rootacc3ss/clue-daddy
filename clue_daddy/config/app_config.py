"""
Application configuration data classes and schemas.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path

def _load_default_system_prompt() -> str:
    """Load default system prompt from prompts module."""
    try:
        from ..prompts import load_default_system_prompt
        return load_default_system_prompt()
    except ImportError:
        # Fallback if prompts module not available
        return DEFAULT_SYSTEM_PROMPT


@dataclass
class AppConfig:
    """Main application configuration dataclass."""
    
    # General Settings
    gemini_api_key: str = ""
    perplexity_api_key: str = ""
    personal_context: str = ""
    default_profile_id: Optional[str] = None
    launch_at_startup: bool = False
    
    # Appearance Settings
    accent_color: str = "#E53E3E"  # Red default
    font_size_multiplier: float = 1.0
    default_transparency: float = 0.65
    enable_animations: bool = True
    
    # AI Settings
    model_name: str = "gemini-live-2.5-flash-preview"
    temperature: float = 0.7
    max_tokens: int = 1000
    universal_system_prompt: str = field(default_factory=_load_default_system_prompt)
    enable_search_tool: bool = True
    
    # Hotkeys
    start_cheating_hotkey: str = "Ctrl+Shift+Space"
    transparency_up_hotkey: str = "Ctrl+Alt+Up"
    transparency_down_hotkey: str = "Ctrl+Alt+Down"
    quick_screenshot_hotkey: str = "Ctrl+Alt+S"
    
    # Privacy & Data
    screenshot_frequency_seconds: int = 2
    auto_delete_sessions_days: Optional[int] = None
    
    # Internal settings
    config_version: str = "1.0.0"
    first_time_setup_completed: bool = False
    
    def to_dict(self) -> dict:
        """Convert config to dictionary for JSON serialization."""
        return {
            # General Settings
            "gemini_api_key": self.gemini_api_key,
            "perplexity_api_key": self.perplexity_api_key,
            "personal_context": self.personal_context,
            "default_profile_id": self.default_profile_id,
            "launch_at_startup": self.launch_at_startup,
            
            # Appearance Settings
            "accent_color": self.accent_color,
            "font_size_multiplier": self.font_size_multiplier,
            "default_transparency": self.default_transparency,
            "enable_animations": self.enable_animations,
            
            # AI Settings
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "universal_system_prompt": self.universal_system_prompt,
            "enable_search_tool": self.enable_search_tool,
            
            # Hotkeys
            "start_cheating_hotkey": self.start_cheating_hotkey,
            "transparency_up_hotkey": self.transparency_up_hotkey,
            "transparency_down_hotkey": self.transparency_down_hotkey,
            "quick_screenshot_hotkey": self.quick_screenshot_hotkey,
            
            # Privacy & Data
            "screenshot_frequency_seconds": self.screenshot_frequency_seconds,
            "auto_delete_sessions_days": self.auto_delete_sessions_days,
            
            # Internal settings
            "config_version": self.config_version,
            "first_time_setup_completed": self.first_time_setup_completed,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AppConfig':
        """Create AppConfig from dictionary."""
        # Filter out any keys that don't exist in the dataclass
        valid_keys = {f.name for f in cls.__dataclass_fields__}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        
        return cls(**filtered_data)


# Default system prompt for the AI
DEFAULT_SYSTEM_PROMPT = """You are Clue Daddy, an AI assistant designed to help users excel in various scenarios including job interviews, sales calls, meetings, presentations, negotiations, and exams.

Your primary role is to provide concise, actionable, and immediately usable responses based on the context provided. You should adapt your communication style and advice based on the specific scenario type indicated in the user's profile.

**Core Principles:**
1. Keep responses SHORT and CONCISE (1-3 sentences max)
2. Use **markdown formatting** for better readability
3. Use **bold** for key points and emphasis
4. Use bullet points (-) for lists when appropriate
5. Focus on the most essential information only
6. Provide direct, ready-to-speak responses when appropriate

**Context Adaptation:**
- For interviews: Focus on showcasing skills, experience, and cultural fit
- For sales: Emphasize value proposition, address objections, and guide toward close
- For meetings: Provide clear, professional, and action-oriented responses
- For presentations: Deliver confident, engaging, and well-structured content
- For negotiations: Offer strategic, professional, and mutually beneficial approaches
- For exams: Provide accurate, comprehensive, and well-organized information

**Response Format:**
Always end your responses with "I'm ready to help!" to maintain consistency and readiness.

Remember: You are here to enhance the user's natural abilities, not replace their authentic voice. Provide guidance that feels natural and genuine to their communication style.

I'm ready to help!"""


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    
    database_path: str = field(default_factory=lambda: str(Path.home() / ".clue-daddy" / "database.db"))
    connection_timeout: int = 30
    enable_wal_mode: bool = True
    backup_frequency_hours: int = 24
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "database_path": self.database_path,
            "connection_timeout": self.connection_timeout,
            "enable_wal_mode": self.enable_wal_mode,
            "backup_frequency_hours": self.backup_frequency_hours,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DatabaseConfig':
        """Create from dictionary."""
        valid_keys = {f.name for f in cls.__dataclass_fields__}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    
    log_level: str = "INFO"
    log_file_max_size_mb: int = 10
    log_file_backup_count: int = 5
    enable_console_logging: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "log_level": self.log_level,
            "log_file_max_size_mb": self.log_file_max_size_mb,
            "log_file_backup_count": self.log_file_backup_count,
            "enable_console_logging": self.enable_console_logging,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'LoggingConfig':
        """Create from dictionary."""
        valid_keys = {f.name for f in cls.__dataclass_fields__}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered_data)