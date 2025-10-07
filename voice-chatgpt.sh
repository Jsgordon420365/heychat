#!/bin/bash
# voice-chatgpt.sh

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
TIMESTAMP=$(date +%Y%m%d%H%M%S)

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Create log directory
mkdir -p "$LOG_DIR"

echo -e "${BLUE}[${TIMESTAMP}] Recording... Press Ctrl+C when done${NC}"

# Record audio using sox (install via: brew install sox)
rec "$AUDIO_FILE" 2>/dev/null

echo -e "${GREEN}Processing...${NC}"

# Transcribe with Whisper
TRANSCRIPT=$(curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file="@$AUDIO_FILE" \
  -F model="whisper-1" | jq -r '.text')

echo -e "${GREEN}You said: ${NC}$TRANSCRIPT"
echo "[$TIMESTAMP] $TRANSCRIPT" >> "$TRANSCRIPT_FILE"

# Get ChatGPT response
echo -e "${BLUE}ChatGPT is thinking...${NC}"

RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{
    \"model\": \"$CHATGPT_MODEL\",
    \"messages\": [{\"role\": \"user\", \"content\": \"$TRANSCRIPT\"}]
  }" | jq -r '.choices[0].message.content')

echo -e "${GREEN}ChatGPT:${NC}"
echo "$RESPONSE"
echo "[$TIMESTAMP] Response: $RESPONSE" >> "$TRANSCRIPT_FILE"

# Speak response using macOS text-to-speech
say "$RESPONSE"

rm "$AUDIO_FILE"