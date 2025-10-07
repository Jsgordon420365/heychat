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
    echo -e "${GREEN}Voice Commands (say any of these):${NC}"
    echo "  🚪 Exit: 'quit', 'exit', 'goodbye', 'bye'"
    echo "  🧹 Clear: 'clear', 'clear conversation', 'reset'"
    echo "  📢 TTS: 'tts on', 'enable tts', 'turn on speech'"
    echo "  🔇 TTS: 'tts off', 'disable tts', 'turn off speech'"
    echo "  ❓ Help: 'help', 'commands', 'what can i say'"
    echo ""
    echo -e "${GREEN}Controls:${NC}"
    echo "  - 4 seconds of silence automatically sends your message"
    echo "  - Press Ctrl+C to manually stop recording"
    echo "  - Your words appear on screen as they're transcribed"
    echo "  - Commands are case-insensitive"
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
    
    echo -e "${BLUE}[${TIMESTAMP}] 🎤 Recording... (4s silence = send, or Ctrl+C to stop)${NC}"
    echo -e "${YELLOW}Listening...${NC}"
    
    # Record audio using sox with silence detection
    # silence 1 0.1 1%: detect silence (1 second of 0.1% volume)
    # -1: end recording after first silence detection  
    # 4: wait 4 seconds of silence before stopping
    rec -t wav "$AUDIO_FILE" trim 0 30 silence 1 0.1 1% -1 4 1% 2>/dev/null
    
    # Check if we got any audio (file size > 0)
    if [ ! -s "$AUDIO_FILE" ]; then
        echo -e "${YELLOW}No audio detected. Try speaking louder or check your microphone.${NC}"
        continue
    fi
    
    echo -e "${GREEN}Processing...${NC}"
    
    # Transcribe with Whisper
    echo -e "${BLUE}Transcribing...${NC}"
    TRANSCRIPT=$(curl -s https://api.openai.com/v1/audio/transcriptions \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -H "Content-Type: multipart/form-data" \
      -F file="@$AUDIO_FILE" \
      -F model="whisper-1" | jq -r '.text')
    
    # Clean up the transcript (remove extra whitespace and normalize)
    TRANSCRIPT=$(echo "$TRANSCRIPT" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr '[:upper:]' '[:lower:]')
    
    # Show the transcript immediately
    echo -e "${GREEN}You said: ${NC}$TRANSCRIPT"
    
    # Check for special commands (case-insensitive)
    case "$TRANSCRIPT" in
        "quit"|"exit"|"goodbye"|"bye")
            echo -e "${GREEN}Goodbye! 👋${NC}"
            rm -f "$AUDIO_FILE"
            exit 0
            ;;
        "clear"|"clear conversation"|"reset")
            clear_conversation
            rm -f "$AUDIO_FILE"
            continue
            ;;
        "help"|"commands"|"what can i say")
            show_help
            rm -f "$AUDIO_FILE"
            continue
            ;;
        "tts on"|"enable tts"|"turn on speech"|"speak responses")
            TTS_ENABLED=true
            echo -e "${GREEN}Text-to-speech enabled.${NC}"
            rm -f "$AUDIO_FILE"
            continue
            ;;
        "tts off"|"disable tts"|"turn off speech"|"stop speaking")
            TTS_ENABLED=false
            echo -e "${YELLOW}Text-to-speech disabled.${NC}"
            rm -f "$AUDIO_FILE"
            continue
            ;;
    esac
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