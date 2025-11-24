#!/bin/bash
# Build and Run Script for Clone Your Voice - Refactored Edition
# This script helps you build and run the application

set -e  # Exit on error

echo "======================================================================"
echo "🎙️  Clone Your Voice - Build and Run Script"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_success "Found project root"

# Parse command line arguments
MODE=${1:-"local"}

if [ "$MODE" == "docker" ]; then
    echo ""
    echo "🐳 Building and running with Docker..."
    echo "======================================================================"

    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    print_success "Docker found"

    # Build with docker-compose
    echo ""
    echo "Building Docker image..."
    docker-compose build

    print_success "Docker image built"

    # Run with docker-compose
    echo ""
    echo "Starting container..."
    docker-compose up -d

    print_success "Container started"

    echo ""
    echo "======================================================================"
    echo "🎉 Application is running!"
    echo "======================================================================"
    echo ""
    echo "📍 Access the app at: http://localhost:5000"
    echo ""
    echo "Useful commands:"
    echo "  • View logs:        docker-compose logs -f"
    echo "  • Stop container:   docker-compose down"
    echo "  • Restart:          docker-compose restart"
    echo ""

elif [ "$MODE" == "local" ]; then
    echo ""
    echo "💻 Building and running locally..."
    echo "======================================================================"

    # Check if python3 is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.11+"
        exit 1
    fi

    print_success "Python 3 found: $(python3 --version)"

    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo ""
        print_warning "Virtual environment not found. Creating..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi

    # Activate virtual environment
    echo ""
    echo "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"

    # Install dependencies
    echo ""
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"

    # Create .env if it doesn't exist
    if [ ! -f ".env" ]; then
        echo ""
        print_warning ".env file not found. Creating from template..."
        cp .env.example .env
        print_success ".env file created (please review and customize)"
    fi

    # Run the application
    echo ""
    echo "Starting application..."
    echo "======================================================================"
    python3 main.py

else
    print_error "Unknown mode: $MODE"
    echo ""
    echo "Usage: $0 [local|docker]"
    echo ""
    echo "Modes:"
    echo "  local   - Run locally with Python virtual environment (default)"
    echo "  docker  - Build and run with Docker"
    echo ""
    exit 1
fi
