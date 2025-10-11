#!/bin/bash

# NeuTTS-Air Web Interface Startup Script

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  NeuTTS-Air Web Interface${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if virtual environment exists
if [ ! -d "$PROJECT_DIR/.venv" ]; then
    echo -e "${RED}Error: Virtual environment not found at $PROJECT_DIR/.venv${NC}"
    echo "Please create a virtual environment first:"
    echo "  cd $PROJECT_DIR"
    echo "  python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source "$PROJECT_DIR/.venv/bin/activate"

# Check if Flask is installed
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${RED}Error: Flask is not installed${NC}"
    echo "Installing Flask..."
    pip install flask
fi

# Change to web interface directory
cd "$SCRIPT_DIR"

# Start the Flask app
echo -e "${GREEN}Starting web server...${NC}"
echo ""
echo -e "${BLUE}Open your browser and navigate to:${NC}"
echo -e "${GREEN}  http://localhost:5000${NC}"
echo ""
echo -e "${BLUE}Press Ctrl+C to stop the server${NC}"
echo ""

python app.py
