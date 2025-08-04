#!/usr/bin/env python3
"""
Test script to verify all dependencies are properly installed and importable.
"""

def test_imports():
    """Test that all required dependencies can be imported."""
    try:
        # UI Framework and Theming
        import PySide6
        from PySide6.QtWidgets import QApplication
        import qdarktheme
        import qtawesome
        print("✓ UI Framework dependencies imported successfully")
        
        # Audio Processing
        import sounddevice
        import speech_recognition
        print("✓ Audio processing dependencies imported successfully")
        
        # AI Integration
        import google.generativeai
        print("✓ AI integration dependencies imported successfully")
        
        # Utility Libraries
        import mss
        import reportlab
        import pytesseract
        import pdf2image
        from PIL import Image
        print("✓ Utility libraries imported successfully")
        
        # Additional Dependencies
        import requests
        import dotenv
        import cryptography
        import keyring
        print("✓ Additional dependencies imported successfully")
        
        # Test our application structure
        from clue_daddy import __version__
        from clue_daddy.app import ClueDaddyApp
        from clue_daddy.config.settings_manager import SettingsManager
        print("✓ Application modules imported successfully")
        
        print(f"\n🎉 All dependencies and modules imported successfully!")
        print(f"Clue Daddy version: {__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)