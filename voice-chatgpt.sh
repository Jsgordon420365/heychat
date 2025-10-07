#!/bin/bash
# voice-chatgpt.sh - Interactive voice conversation with ChatGPT

# Load environment variables
ENV_FILE="$HOME/.config/voice-chatgpt/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    echo "Create it with: OPENAI_API_KEY=\"your-openai-api-key-here\""
    exit 1
fi

source "$ENV_FILE"

# Configuration
AUDIO_FILE="$LOG_DIR/voice_input.wav"
TRANSCRIPT_FILE="$LOG_DIR/transcripts.log"
CONVERSATION_FILE="$LOG_DIR/conversation.json"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Create log directory
mkdir -p "$LOG_DIR"

# Initialize conversation history if it doesn't exist
if [ ! -f "$CONVERSATION_FILE" ]; then
    echo '[]' > "$CONVERSATION_FILE"
fi

# Function to add message to conversation history
add_to_conversation() {
    local role="$1"
    local content="$2"
    local temp_file=$(mktemp)
    
    jq --arg role "$role" --arg content "$content" \
       '. + [{"role": $role, "content": $content}]' \
       "$CONVERSATION_FILE" > "$temp_file" && mv "$temp_file" "$CONVERSATION_FILE"
}

# Function to get conversation history for API
get_conversation_history() {
    cat "$CONVERSATION_FILE"
}

# Function to clear conversation history
clear_conversation() {
    echo '[]' > "$CONVERSATION_FILE"
    echo -e "${YELLOW}Conversation history cleared.${NC}"
}

# Function to show help
show_help() {
    echo -e "${BLUE}HeyChat Voice Interface${NC}"
    echo -e "${GREEN}Commands:${NC}"
    echo "  - Press Ctrl+C to stop recording"
    echo "  - Type 'quit' or 'exit' to end conversation"
    echo "  - Type 'clear' to clear conversation history"
    echo "  - Type 'help' to show this help"
    echo "  - Type 'tts on/off' to toggle text-to-speech"
    echo ""
}

# Check for command line arguments
TTS_ENABLED=true
if [ "$1" = "--no-tts" ] || [ "$1" = "-n" ]; then
    TTS_ENABLED=false
    echo -e "${YELLOW}Text-to-speech disabled. Use 'tts on' to enable.${NC}"
fi

echo -e "${BLUE}🎤 HeyChat Voice Interface Started${NC}"
echo -e "${GREEN}Type 'help' for commands or start speaking...${NC}"
echo ""

# Main conversation loop
while true; do
    TIMESTAMP=$(date +%Y%m%d%H%M%S)
    
    echo -e "${BLUE}[${TIMESTAMP}] Recording... Press Ctrl+C when done${NC}"
    
    # Record audio using sox
    rec "$AUDIO_FILE" 2>/dev/null
    
    echo -e "${GREEN}Processing...${NC}"
    
    # Transcribe with Whisper
    TRANSCRIPT=$(curl -s https://api.openai.com/v1/audio/transcriptions \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -H "Content-Type: multipart/form-data" \
      -F file="@$AUDIO_FILE" \
      -F model="whisper-1" | jq -r '.text')
    
    # Check for special commands
    case "$TRANSCRIPT" in
        "quit"|"exit"|"goodbye")
            echo -e "${GREEN}Goodbye! 👋${NC}"
            rm -f "$AUDIO_FILE"
            exit 0
            ;;
        "clear")
            clear_conversation
            rm -f "$AUDIO_FILE"
            continue
            ;;
        "help")
            show_help
            rm -f "$AUDIO_FILE"
            continue
            ;;
        "tts on")
            TTS_ENABLED=true
            echo -e "${GREEN}Text-to-speech enabled.${NC}"
            rm -f "$AUDIO_FILE"
            continue
            ;;
        "tts off")
            TTS_ENABLED=false
            echo -e "${YELLOW}Text-to-speech disabled.${NC}"
            rm -f "$AUDIO_FILE"
            continue
            ;;
    esac
    
    echo -e "${GREEN}You said: ${NC}$TRANSCRIPT"
    echo "[$TIMESTAMP] User: $TRANSCRIPT" >> "$TRANSCRIPT_FILE"
    
    # Add user message to conversation history
    add_to_conversation "user" "$TRANSCRIPT"
    
    # Get ChatGPT response with conversation history
    echo -e "${BLUE}ChatGPT is thinking...${NC}"
    
    RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -d "{
        \"model\": \"$CHATGPT_MODEL\",
        \"messages\": $(get_conversation_history)
      }" | jq -r '.choices[0].message.content')
    
    echo -e "${GREEN}ChatGPT:${NC}"
    echo "$RESPONSE"
    echo "[$TIMESTAMP] ChatGPT: $RESPONSE" >> "$TRANSCRIPT_FILE"
    
    # Add assistant response to conversation history
    add_to_conversation "assistant" "$RESPONSE"
    
    # Speak response if TTS is enabled
    if [ "$TTS_ENABLED" = true ]; then
        echo -e "${BLUE}Speaking response...${NC}"
        say "$RESPONSE"
    else
        echo -e "${YELLOW}(Text-to-speech disabled - use 'tts on' to enable)${NC}"
    fi
    
    # Clean up audio file
    rm -f "$AUDIO_FILE"
    
    echo -e "${GREEN}Ready for next input...${NC}"
    echo ""
done