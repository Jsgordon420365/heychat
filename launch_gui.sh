#!/bin/bash
# launch_gui.sh - Launch the HeyChat GUI application

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🎤 HeyChat GUI Launcher${NC}"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3: brew install python3"
    exit 1
fi

# Check if tkinter is available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${RED}Error: tkinter is not available${NC}"
    echo "Please install tkinter: brew install python-tk"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "heychat_gui.py" ]; then
    echo -e "${RED}Error: heychat_gui.py not found${NC}"
    echo "Please run this script from the HeyChat project directory"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 and tkinter are available${NC}"
echo -e "${BLUE}🚀 Launching HeyChat GUI...${NC}"
echo ""

# Launch the GUI
python3 heychat_gui.py

echo -e "${YELLOW}HeyChat GUI closed. Goodbye! 👋${NC}"
