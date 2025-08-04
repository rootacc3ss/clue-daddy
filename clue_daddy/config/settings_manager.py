"""
Settings manager for configuration persistence and management.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import os
import shutil
from datetime import datetime

from .app_config import AppConfig, DatabaseConfig, LoggingConfig
from .config_validator import ConfigValidator


class SettingsManager:
    """Manages application settings persistence and validation."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validator = ConfigValidator()
        
        # Setup directory structure
        self.config_dir = Path.home() / ".clue-daddy"
        self.config_file = self.config_dir / "config.json"
        self.backup_dir = self.config_dir / "backups"
        
        self._ensure_directory_structure()
        
    def _ensure_directory_structure(self):
        """Create necessary directory structure."""
        directories = [
            self.config_dir,
            self.config_dir / "sessions",
            self.config_dir / "profiles", 
            self.config_dir / "logs",
            self.backup_dir,
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                self.logger.debug(f"Ensured directory exists: {directory}")
            except Exception as e:
                self.logger.error(f"Failed to create directory {directory}: {e}")
                raise
                
    def load_config(self) -> AppConfig:
        """
        Load configuration from file.
        
        Returns:
            AppConfig instance with loaded or default values
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    
                self.logger.info(f"Loaded configuration from {self.config_file}")
                
                # Validate and sanitize
                config_data = self.validator.apply_defaults(config_data)
                config_data = self.validator.sanitize_config(config_data)
                
                is_valid, errors = self.validator.validate_config(config_data)
                if not is_valid:
                    self.logger.warning(f"Configuration validation errors: {errors}")
                    # Continue with sanitized config even if there are validation errors
                    
                return AppConfig.from_dict(config_data)
                
            else:
                self.logger.info("No configuration file found, using defaults")
                return AppConfig()
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            self.logger.info("Using default configuration")
            return AppConfig()
            
    def save_config(self, config: AppConfig) -> bool:
        """
        Save configuration to file.
        
        Args:
            config: AppConfig instance to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup if config file exists
            if self.config_file.exists():
                self._create_backup()
                
            # Convert to dict and validate
            config_dict = config.to_dict()
            config_dict = self.validator.sanitize_config(config_dict)
            
            is_valid, errors = self.validator.validate_config(config_dict)
            if not is_valid:
                self.logger.warning(f"Saving configuration with validation errors: {errors}")
                
            # Write to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
                
            self.logger.info(f"Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving configuration: {e}")
            return False
            
    def _create_backup(self):
        """Create a backup of the current configuration."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"config_backup_{timestamp}.json"
            
            shutil.copy2(self.config_file, backup_file)
            self.logger.debug(f"Created configuration backup: {backup_file}")
            
            # Clean up old backups (keep last 10)
            self._cleanup_old_backups()
            
        except Exception as e:
            self.logger.warning(f"Failed to create configuration backup: {e}")
            
    def _cleanup_old_backups(self):
        """Remove old backup files, keeping only the most recent ones."""
        try:
            backup_files = list(self.backup_dir.glob("config_backup_*.json"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Keep only the 10 most recent backups
            for old_backup in backup_files[10:]:
                old_backup.unlink()
                self.logger.debug(f"Removed old backup: {old_backup}")
                
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")
            
    def get_default_config(self) -> AppConfig:
        """Get default configuration."""
        return AppConfig()
        
    def validate_config(self, config: AppConfig) -> tuple[bool, list[str]]:
        """
        Validate configuration.
        
        Args:
            config: AppConfig instance to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        config_dict = config.to_dict()
        return self.validator.validate_config(config_dict)
        
    def reset_to_defaults(self) -> bool:
        """
        Reset configuration to defaults.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            default_config = AppConfig()
            return self.save_config(default_config)
        except Exception as e:
            self.logger.error(f"Error resetting configuration to defaults: {e}")
            return False
            
    def export_config(self, export_path: Path) -> bool:
        """
        Export configuration to specified path.
        
        Args:
            export_path: Path to export configuration to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.config_file.exists():
                shutil.copy2(self.config_file, export_path)
                self.logger.info(f"Configuration exported to {export_path}")
                return True
            else:
                self.logger.warning("No configuration file to export")
                return False
                
        except Exception as e:
            self.logger.error(f"Error exporting configuration: {e}")
            return False
            
    def import_config(self, import_path: Path) -> bool:
        """
        Import configuration from specified path.
        
        Args:
            import_path: Path to import configuration from
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not import_path.exists():
                self.logger.error(f"Import file does not exist: {import_path}")
                return False
                
            # Load and validate imported config
            with open(import_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            # Validate imported data
            config_data = self.validator.apply_defaults(config_data)
            config_data = self.validator.sanitize_config(config_data)
            
            is_valid, errors = self.validator.validate_config(config_data)
            if not is_valid:
                self.logger.warning(f"Imported configuration has validation errors: {errors}")
                
            # Create config object and save
            config = AppConfig.from_dict(config_data)
            success = self.save_config(config)
            
            if success:
                self.logger.info(f"Configuration imported from {import_path}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error importing configuration: {e}")
            return False
            
    def get_config_info(self) -> Dict[str, Any]:
        """
        Get information about the current configuration.
        
        Returns:
            Dictionary with configuration metadata
        """
        info = {
            "config_file_exists": self.config_file.exists(),
            "config_file_path": str(self.config_file),
            "config_dir_path": str(self.config_dir),
            "backup_count": len(list(self.backup_dir.glob("config_backup_*.json"))),
        }
        
        if self.config_file.exists():
            stat = self.config_file.stat()
            info.update({
                "config_file_size": stat.st_size,
                "config_last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
            
        return info