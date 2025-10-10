#!/bin/bash
# HeyChat Web Server Launcher
# Starts the Flask web server for HeyChat

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   HeyChat Web Server Launcher              ║${NC}"
echo -e "${BLUE}║   Voice AI Assistant - HTTP Interface      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    echo "Please install Python 3 and try again."
    exit 1
fi

echo -e "${GREEN}✓${NC} Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠${NC}  Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
fi

# Activate virtual environment
echo -e "${BLUE}→${NC} Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo -e "${BLUE}→${NC} Checking dependencies..."
if [ -f "requirements_gui.txt" ]; then
    pip install -q --upgrade pip
    pip install -q -r requirements_gui.txt
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${YELLOW}⚠${NC}  requirements_gui.txt not found"
    echo "Installing Flask manually..."
    pip install -q flask flask-cors flask-socketio python-socketio python-engineio werkzeug
fi

# Check if environment file exists
ENV_FILE="$HOME/.config/voice-chatgpt/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠${NC}  Environment file not found: $ENV_FILE"
    echo "Some features may not work without proper configuration."
fi

# Make scripts executable
chmod +x voice-chatgpt.sh 2>/dev/null || true
chmod +x quick-ask.sh 2>/dev/null || true

# Check if port 5000 is available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${RED}✗${NC} Port 5000 is already in use!"
    echo "Please stop the service using port 5000 or modify the port in heychat_web_server.py"
    exit 1
fi

echo -e "${GREEN}✓${NC} Port 5000 is available"
echo ""

# Start the web server
echo -e "${GREEN}Starting HeyChat Web Server...${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🌐 Web UI:${NC}      http://localhost:5000"
echo -e "${GREEN}📡 API:${NC}         http://localhost:5000/api"
echo -e "${GREEN}🔌 WebSocket:${NC}   ws://localhost:5000/socket.io"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start server
python3 heychat_web_server.py
