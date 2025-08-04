# Clue Daddy

AI-powered stealthy assistant for meetings, interviews, speeches, homework, tests and more.

## Overview

Clue Daddy is a sophisticated desktop application built with Python and PySide6 that provides real-time AI assistance during various scenarios. The application features a modern dark theme, real-time audio processing, screenshot analysis, and comprehensive session management using Google's Gemini Live API.

## Features

- **Real-time AI Assistance**: Voice recognition and screenshot analysis
- **Profile Management**: Context profiles for different use cases (interviews, sales, meetings, etc.)
- **Session Recording**: Complete interaction history with export capabilities
- **Modern UI**: Dark theme with smooth animations
- **Privacy-focused**: All data stored locally

## Project Structure

```
clue_daddy/
├── __init__.py                 # Package initialization
├── app.py                      # Main application entry point
├── onboarding/                 # First-time setup system
│   ├── __init__.py
│   ├── welcome_dialog.py       # Welcome screen
│   ├── api_key_input.py        # API key collection
│   ├── personal_context_input.py # User context input
│   └── onboarding_controller.py # Flow management
├── main_gui/                   # Central interface
│   ├── __init__.py
│   └── main_window.py          # Main application window
├── assistant/                  # AI interaction system
│   ├── __init__.py
│   ├── profile_selector.py     # Profile selection
│   └── chat_window.py          # Floating chat interface
├── sessions/                   # Session management
│   └── __init__.py
├── profiles/                   # Profile management
│   └── __init__.py
└── config/                     # Configuration system
    ├── __init__.py
    └── settings_manager.py     # Settings persistence
```

## Dependencies

### Core Dependencies
- **PySide6**: Cross-platform GUI framework
- **qdarktheme**: Modern dark theme
- **qtawesome**: Icon library
- **sounddevice**: Audio capture
- **speech_recognition**: Speech-to-text
- **google-generativeai**: Gemini AI integration
- **mss**: Screenshot capture
- **reportlab**: PDF generation
- **pytesseract**: OCR processing
- **pdf2image**: PDF to image conversion

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python -m clue_daddy.app
   ```

## Development Setup

1. Install in development mode:
   ```bash
   pip install -e .
   ```
2. Run tests:
   ```bash
   python test_imports.py
   python test_app_basic.py
   ```

## Configuration

The application stores configuration in `~/.clue-daddy/config.json` with the following structure:
- API keys and personal context
- UI preferences (theme, transparency, animations)
- AI settings (model, temperature, system prompts)
- Hotkey configurations
- Privacy and data management settings

## License

MIT License - see LICENSE file for details.

## Version

Current version: 1.0.0