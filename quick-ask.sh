#!/bin/bash
# quick-ask.sh

# Load environment variables
ENV_FILE="$HOME/.config/voice-chatgpt/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    echo "Create it with: OPENAI_API_KEY=\"your-openai-api-key-here\""
    exit 1
fi

source "$ENV_FILE"

TIMESTAMP=$(date +%Y%m%d%H%M%S)
AUDIO="$LOG_DIR/q_${TIMESTAMP}.wav"

mkdir -p "$LOG_DIR"

# Record 5 seconds
rec "$AUDIO" trim 0 5 2>/dev/null

TRANSCRIPT=$(curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@$AUDIO" \
  -F model="whisper-1" | jq -r '.text')

echo "You: $TRANSCRIPT"

RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$CHATGPT_MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"$TRANSCRIPT\"}]}" | \
  jq -r '.choices[0].message.content')

echo "$RESPONSE"
say "$RESPONSE"

rm "$AUDIO"