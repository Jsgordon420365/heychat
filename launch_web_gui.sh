#!/bin/bash
# launch_web_gui.sh - Launch the HeyChat Web GUI application

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🎤 HeyChat Web GUI Launcher${NC}"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3: brew install python3"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "heychat_web_gui.py" ]; then
    echo -e "${RED}Error: heychat_web_gui.py not found${NC}"
    echo "Please run this script from the HeyChat project directory"
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}Flask not found. Installing Flask...${NC}"
    pip3 install flask
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to install Flask${NC}"
        echo "Please install Flask manually: pip3 install flask"
        exit 1
    fi
    echo -e "${GREEN}✅ Flask installed successfully${NC}"
else
    echo -e "${GREEN}✅ Flask is available${NC}"
fi

echo -e "${GREEN}✅ Python 3 and Flask are available${NC}"
echo -e "${BLUE}🚀 Launching HeyChat Web GUI...${NC}"
echo ""
echo -e "${YELLOW}The web interface will open automatically in your browser${NC}"
echo -e "${YELLOW}If it doesn't open, go to: http://localhost:5000${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Launch the web GUI
python3 heychat_web_gui.py

echo -e "${YELLOW}HeyChat Web GUI stopped. Goodbye! 👋${NC}"


