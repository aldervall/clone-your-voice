#!/usr/bin/env python3
"""
Clone Your Voice - Main Entry Point
Run the voice cloning web application
"""
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.api.app import run_app

if __name__ == '__main__':
    run_app()
