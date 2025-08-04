#!/usr/bin/env python3
"""
Basic test to verify the application can initialize without errors.
"""

import sys
from clue_daddy.app import ClueDaddyApp

def test_app_initialization():
    """Test that the application can be created and initialized."""
    try:
        # Create application instance
        app = ClueDaddyApp()
        print("✓ ClueDaddyApp created successfully")
        
        # Test that methods exist
        assert hasattr(app, 'show_onboarding'), "show_onboarding method missing"
        assert hasattr(app, 'show_main_gui'), "show_main_gui method missing"
        assert hasattr(app, 'register_global_hotkeys'), "register_global_hotkeys method missing"
        print("✓ Required methods exist")
        
        # Test settings manager
        from clue_daddy.config.settings_manager import SettingsManager
        settings = SettingsManager()
        config = settings.load_config()
        print("✓ Settings manager works")
        print(f"✓ Default config loaded with {len(config)} settings")
        
        # Clean up
        app.quit()
        print("✓ Application cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during app initialization: {e}")
        return False

if __name__ == "__main__":
    success = test_app_initialization()
    exit(0 if success else 1)