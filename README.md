# HeyChat

A comprehensive voice-based ChatGPT interface that allows you to have conversations with ChatGPT using your voice. The project includes bash scripts for voice interaction, database integration for conversation persistence, and modern GUI applications for easy access to all functions.

## Features

- **Voice Recording**: Record audio using your microphone
- **Speech-to-Text**: Automatic transcription using OpenAI's Whisper API
- **AI Responses**: Get responses from ChatGPT
- **Text-to-Speech**: Hear responses using macOS built-in speech synthesis
- **Conversation Logging**: Keep track of your voice conversations
- **Two Interaction Modes**: Quick questions or extended conversations
- **Database Integration**: Persistent conversation storage with Supabase
- **Modern GUI**: Web and desktop interfaces for easy access
- **Conversation Management**: Browse, search, and export conversations
- **Real-time Monitoring**: Live status updates and logging

## Project Structure

```
heychat/
├── quick-ask.sh              # Quick 5-second voice queries
├── voice-chatgpt.sh          # Interactive voice conversations
├── heychat_gui.py            # Desktop GUI application
├── heychat_web_gui.py        # Web-based GUI application
├── launch_gui.sh             # Desktop GUI launcher
├── launch_web_gui.sh         # Web GUI launcher
├── view_conversations.py     # Command-line conversation viewer
├── browse_conversations.py   # Interactive conversation browser
├── supabase_viewer.py        # Database viewer with SQL queries
├── view_db.sh                # Database viewing launcher
├── supabase_integration.py   # Database integration script
├── schema.sql                # Database schema definition
├── README.md                 # Main documentation
├── GUI_README.md             # GUI documentation
├── VIEWING_TOOLS.md          # Database tools documentation
└── requirements_gui.txt      # GUI dependencies
```

## Scripts

### 1. `voice-chatgpt.sh` - Interactive Voice Chat

**Purpose**: Full interactive voice conversation with ChatGPT

**Features**:
- **Continuous Conversation**: Keeps listening after each response for ongoing dialogue
- **Conversation Memory**: Maintains context across multiple interactions
- **Optional Text-to-Speech**: Toggle speech output on/off during conversation
- **Voice Commands**: Special voice commands for control (quit, clear, help, tts on/off)
- **Smart Recording**: Records audio with 4-second silence detection or manual Ctrl+C stop
- **Transcription**: Uses OpenAI Whisper API for accurate speech-to-text
- **AI Responses**: Gets contextual responses from ChatGPT
- **Conversation Logging**: Saves full conversation history to `$LOG_DIR/transcripts.log`
- **Color-coded Output**: Enhanced terminal interface with status indicators
- **Timestamped Logs**: All interactions are timestamped for easy reference

**Usage**:
```bash
# Start with text-to-speech enabled (default)
./voice-chatgpt.sh

# Start with text-to-speech disabled
./voice-chatgpt.sh --no-tts
```

**Voice Commands** (speak these during recording):
- `"quit"` or `"exit"` - End the conversation
- `"clear"` - Clear conversation history
- `"help"` - Show available commands
- `"tts on"` - Enable text-to-speech
- `"tts off"` - Disable text-to-speech

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

## GUI Applications

HeyChat includes two modern GUI applications for easy access to all functions:

### 🌐 Web GUI (Recommended)
A responsive web-based interface that works on any device with a browser.

```bash
# Launch the web GUI
./launch_web_gui.sh
```

**Features:**
- Modern, responsive design
- Real-time status updates
- Cross-platform compatibility
- Dashboard layout with organized sections
- Live logging and monitoring

### 🖥️ Desktop GUI (Alternative)
A native desktop application with tabbed interface.

```bash
# Launch the desktop GUI
./launch_gui.sh
```

**Features:**
- Native desktop integration
- Tabbed interface (Console, Conversations, Logs)
- Interactive conversation browser
- Color-coded output
- Keyboard shortcuts

**GUI Capabilities:**
- **Voice Controls**: Start/stop voice chat and quick ask
- **Database Management**: Browse, search, and export conversations
- **Real-time Monitoring**: Live status updates and logging
- **Settings**: Configuration and connection testing
- **Tools**: Log viewing and GitHub access

For detailed GUI documentation, see [GUI_README.md](GUI_README.md).

## Database Integration

HeyChat includes comprehensive database integration for persistent conversation storage:

### 🗄️ Supabase Integration
- **Persistent Storage**: All conversations saved to Supabase database
- **Session Management**: Unique session IDs for conversation tracking
- **Search & Export**: Full-text search and export capabilities
- **Statistics**: Usage analytics and conversation metrics

### 📊 Database Tools
```bash
# Interactive conversation browser
./browse_conversations.py

# Command-line viewer
python3 view_conversations.py list --limit 10

# Search conversations
python3 view_conversations.py search --search "python"

# Export conversation
python3 view_conversations.py export --session-id session_123 --format json
```

For detailed database documentation, see [VIEWING_TOOLS.md](VIEWING_TOOLS.md).

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
# Records until 4 seconds of silence or Ctrl+C, transcribes, gets ChatGPT response, speaks it back
```

## File Management

- **Audio Files**: Temporarily stored in `$LOG_DIR` and automatically cleaned up
- **Transcripts**: Permanently logged to `$LOG_DIR/transcripts.log`
- **Conversation History**: Maintained in `$LOG_DIR/conversation.json` for context
- **Timestamps**: All interactions are timestamped for easy reference

## Conversation Features

### Continuous Dialogue
The enhanced `voice-chatgpt.sh` now supports ongoing conversations:
- **Memory**: Remembers previous parts of the conversation
- **Context**: ChatGPT can reference earlier parts of your discussion
- **Natural Flow**: No need to restart the script for follow-up questions

### Voice Commands
Control the conversation using voice commands:
- Say `"quit"` or `"exit"` to end the session
- Say `"clear"` to reset conversation history
- Say `"help"` to see available commands
- Say `"tts on"` or `"tts off"` to toggle speech output

### Text-to-Speech Control
- **Default**: Text-to-speech is enabled by default
- **Disable at Start**: Use `./voice-chatgpt.sh --no-tts`
- **Toggle During**: Use voice commands `"tts on"` or `"tts off"`
- **Visual Feedback**: Clear indicators when TTS is enabled/disabled

### Smart Recording
- **Automatic Send**: 4 seconds of silence automatically sends your message
- **Manual Control**: Press Ctrl+C to manually stop recording
- **Maximum Duration**: Recording stops after 30 seconds maximum
- **No Audio Detection**: Warns if no audio is detected

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
