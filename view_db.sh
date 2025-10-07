#!/bin/bash
# HeyChat Database Viewer - Quick access to conversation viewing tools

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🗣️  HeyChat Database Viewer${NC}"
echo "=" * 40
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is required but not installed.${NC}"
    exit 1
fi

# Show available options
echo -e "${GREEN}Available viewing options:${NC}"
echo "1. Interactive Browser (recommended)"
echo "2. Command Line Viewer"
echo "3. Quick Stats"
echo "4. List Recent Conversations"
echo ""

read -p "Choose an option (1-4) or press Enter for interactive browser: " choice

case "${choice:-1}" in
    1|"")
        echo -e "${BLUE}Starting interactive browser...${NC}"
        python3 "$SCRIPT_DIR/browse_conversations.py"
        ;;
    2)
        echo -e "${BLUE}Command line viewer help:${NC}"
        echo ""
        python3 "$SCRIPT_DIR/view_conversations.py" --help
        echo ""
        echo -e "${YELLOW}Example commands:${NC}"
        echo "  python3 view_conversations.py list --limit 5"
        echo "  python3 view_conversations.py show --session-id session_20251007120000_abc123"
        echo "  python3 view_conversations.py search --search 'python'"
        echo "  python3 view_conversations.py stats"
        ;;
    3)
        echo -e "${BLUE}Quick Statistics:${NC}"
        echo ""
        python3 "$SCRIPT_DIR/view_conversations.py" stats
        ;;
    4)
        echo -e "${BLUE}Recent Conversations:${NC}"
        echo ""
        python3 "$SCRIPT_DIR/view_conversations.py" list --limit 5
        ;;
    *)
        echo -e "${RED}Invalid option. Starting interactive browser...${NC}"
        python3 "$SCRIPT_DIR/browse_conversations.py"
        ;;
esac
