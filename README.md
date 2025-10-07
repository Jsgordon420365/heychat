# HeyChat

A simple voice-based ChatGPT interface that allows you to have conversations with ChatGPT using your voice. The project consists of two bash scripts that provide different interaction modes for voice-based AI communication.

## Features

- **Voice Recording**: Record audio using your microphone
- **Speech-to-Text**: Automatic transcription using OpenAI's Whisper API
- **AI Responses**: Get responses from ChatGPT
- **Text-to-Speech**: Hear responses using macOS built-in speech synthesis
- **Conversation Logging**: Keep track of your voice conversations
- **Two Interaction Modes**: Quick questions or extended conversations

## Project Structure

```
heychat/
├── quick-ask.sh      # Quick 5-second voice queries
├── voice-chatgpt.sh  # Interactive voice conversations
└── README.md         # This file
```

## Scripts

### 1. `voice-chatgpt.sh` - Interactive Voice Chat

**Purpose**: Full interactive voice conversation with ChatGPT

**Features**:
- Records audio until you press Ctrl+C
- Transcribes audio using OpenAI Whisper API
- Sends transcript to ChatGPT API
- Speaks the response using macOS `say` command
- Logs conversations to `$LOG_DIR/transcripts.log`
- Color-coded terminal output for better UX
- Timestamped recordings and logs

**Usage**:
```bash
./voice-chatgpt.sh
```

### 2. `quick-ask.sh` - Quick Voice Queries

**Purpose**: Fast 5-second voice recording for quick questions

**Features**:
- Records exactly 5 seconds of audio
- Same transcription and ChatGPT integration as main script
- Speaks response and automatically cleans up audio file
- Streamlined workflow for quick interactions

**Usage**:
```bash
./quick-ask.sh
```

## Prerequisites

### System Dependencies

Install the required system tools:

```bash
# Install sox for audio recording
brew install sox

# Install jq for JSON parsing
brew install jq

# curl should already be available on macOS
```

### API Requirements

- **OpenAI API Key**: Required for both Whisper transcription and ChatGPT responses
- **Internet Connection**: For API calls to OpenAI services

## Configuration

### Environment Setup

Create a configuration file at `$HOME/.config/voice-chatgpt/.env` with the following variables:

```bash
# OpenAI API Configuration
OPENAI_API_KEY="your-openai-api-key-here"
CHATGPT_MODEL="gpt-3.5-turbo"  # or gpt-4, gpt-4-turbo, etc.

# Logging Configuration
LOG_DIR="$HOME/.config/voice-chatgpt/logs"
```

### Creating the Configuration

```bash
# Create the config directory
mkdir -p "$HOME/.config/voice-chatgpt"

# Create the .env file
cat > "$HOME/.config/voice-chatgpt/.env" << EOF
OPENAI_API_KEY="your-openai-api-key-here"
CHATGPT_MODEL="gpt-3.5-turbo"
LOG_DIR="$HOME/.config/voice-chatgpt/logs"
EOF
```

## Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd heychat
   ```

2. **Make scripts executable**:
   ```bash
   chmod +x *.sh
   ```

3. **Set up configuration** (see Configuration section above)

4. **Install dependencies** (see Prerequisites section above)

## Usage Examples

### Quick Question
```bash
./quick-ask.sh
# Records 5 seconds, asks "What's the weather like?", gets response
```

### Extended Conversation
```bash
./voice-chatgpt.sh
# Records until Ctrl+C, transcribes, gets ChatGPT response, speaks it back
```

## File Management

- **Audio Files**: Temporarily stored in `$LOG_DIR` and automatically cleaned up
- **Transcripts**: Permanently logged to `$LOG_DIR/transcripts.log`
- **Timestamps**: All interactions are timestamped for easy reference

## Troubleshooting

### Common Issues

1. **"rec: command not found"**
   - Install sox: `brew install sox`

2. **"jq: command not found"**
   - Install jq: `brew install jq`

3. **"Error: .env file not found"**
   - Create the configuration file as described in the Configuration section

4. **API Key Issues**
   - Verify your OpenAI API key is correct and has sufficient credits
   - Check that the API key has access to both Whisper and ChatGPT APIs

5. **Audio Recording Issues**
   - Ensure your microphone is working and accessible
   - Check microphone permissions in System Preferences > Security & Privacy > Privacy > Microphone

### Logs

Check the transcript log for debugging:
```bash
cat "$HOME/.config/voice-chatgpt/logs/transcripts.log"
```

## Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- The `.env` file should be in your `.gitignore` if you plan to share this project
- Audio files are automatically deleted after processing for privacy

## License

This project is provided as-is for personal use. Please ensure you comply with OpenAI's terms of service when using their APIs.

## Contributing

Feel free to submit issues or pull requests to improve the functionality or add new features.
