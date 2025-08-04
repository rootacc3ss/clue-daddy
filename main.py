#!/usr/bin/env python3
"""
Main entry point for Clue Daddy application.
"""

import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from clue_daddy.app import main

if __name__ == "__main__":
    sys.exit(main())