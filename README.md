# Clue Daddy

AI-powered stealthy assistant for meetings, interviews, speeches, homework, tests and more. Inspired by Cluely and Cheating Daddy. Huge thanks to Soham (@szham) and a not so huge thanks to that asian guy on Xitter that made Cluely. Please stop invading my feed. I will singlehandedly make a better product than you and offer it to the public for free.

Nothing against him, I just think he's a bit up his own ass for building a beautified GPT wrapper. Good on him or whatever but I'm sick of people selling GPT wrappers. If you aren't at least bringing a fine tuned, trained or novel model to the table, your project is LITERALLY just ChatGPT with a little spice.

Whatever. Anyways...

## Overview

Clue Daddy is a sophisticated desktop application built with Python and PySide6 that provides real-time AI assistance during various scenarios. The application features a modern dark theme, real-time audio processing, screenshot analysis, and comprehensive session management using Google's Gemini Live API.

This tool is on the brink of being better than Cluely, honestly. Just not as pretty.

**Who's this for?**

This tool is for *anybody*, but really, I am refining this for the following:
- **Sales Associates**: Optimizing context

## Features

- **Real-time AI Assistance**: Voice recognition and screenshot analysis
- **Profile Management**: Context profiles for different use cases (interviews, sales, meetings, etc.)
- **Session Recording**: Complete interaction history with export capabilities
- **Modern UI**: Dark theme with smooth animations
- **Privacy-focused**: All data stored locally
- **Awesome Context System**: Allows for much better co
- **Fully Customizable**: Our profile system allows you to tailor how your AI will respond for your situation.

## To Do

**I'm just building this as I go, and it'll probably take a while, but here are some features I plan on adding in the coming weeks:**

- **Add "Two Way TTS"**: Have FAR better context when chatting with the AI on the homepage; chatting about your previous sessions will level up, and context inside of your session will be held better, bringing much better responses. Will be able to recognize who is speaking.
- **Implement Stealth Features**: Fully replicate not only Cheating Daddy's awesome security features but Cluely's evasion features as well. Additions to the stealthing will be added, including evasion of proctoring tools using task manipulation.
- **On The Fly Profile Creation**: Use AI to prepare for a last minute meeting by chatting with AI (or sending a single prompt) to create a profile -- uses Perplexity Deep Research via API to scrape the web for the context you need. *Already partially added; Perplexity API is included for gathering context*.
- **Smart Model Selection**: Integrate Gemini 2.5 Pro Reasoning for certain functions.
- **Master Prompt System Enhancements**: Fix up the master prompt and prompting system for further gains
- **Context Hacking**: Enhance context window by integrating a vector database for LARGE "Profiles" inside of the "Context Base"; sales teams and customer support will be able to store and parse gigabytes of files, easily. Includes responses in the current chat, so if the other party circles back, you can respond with confidence.
- **Improved Latency**: Get responses MUCH faster with our system that is soon to be implemented.
- **New Object Detection**: No more need to send a prompt or click the photo button every time something new to do analysis on pops up on your screen. Without spending your API credits, Clue Daddy intelligently knows when to respond to video.

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

None ATM, but you can do whatever you want. If you bundle it and sell it I'll ruin your life but otherwise I really DGAF what you do with this. You should make a fork and make it even better or try and make the DB work in the cloud. IDK man, I just want you to have fun and be good.

## Version

Current version: 1.0.0

## DISCLAIMER

Do NOT use this program for academic dishonesty. This program is primarily intended for sales calls, meetings, interviews where notes are allowed, et cetera. Please do the right thing. I mean, I'm not looking but you **def** shouldn't be dumb. 

I am not liable for anything done with this tool; dishonesty is bad, but innovation is good.