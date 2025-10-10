# HeyChat Documentation Index

Complete index of all HeyChat documentation and resources.

## 📚 Main Documentation

### 🎯 Project Overview
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project overview and architecture
- **[README.md](README.md)** - Main project documentation and quick start
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes

### 🚀 Getting Started
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Detailed installation instructions
- **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API documentation

### 🎨 User Interfaces
- **[GUI_README.md](GUI_README.md)** - GUI applications guide
- **[WEB_SERVER_README.md](WEB_SERVER_README.md)** - Web server documentation
- **[VIEWING_TOOLS.md](VIEWING_TOOLS.md)** - Database viewing tools guide

## 🎤 Voice System

### Core Scripts
- **`voice-chatgpt.sh`** - Interactive voice conversations
- **`quick-ask.sh`** - Quick 5-second voice queries

### Features
- Speech-to-text using OpenAI Whisper API
- AI responses from ChatGPT API
- Text-to-speech using macOS built-in synthesis
- 4-second silence detection
- Voice commands for control
- Conversation memory and context

## 🌐 Web Applications

### Web Server (Full-Featured)
- **`heychat_web_server.py`** - Flask server with REST API
- **`launch_web_server.sh`** - Server launcher script
- **Features**: REST API, WebSocket, process monitoring, file export

### Web GUI (Simple)
- **`heychat_web_gui.py`** - Lightweight web interface
- **`launch_web_gui.sh`** - GUI launcher script
- **Features**: Simple interface, cross-platform, real-time updates

## 🖥️ Desktop Application

### Native GUI
- **`heychat_gui.py`** - tkinter desktop application
- **`launch_gui.sh`** - Desktop launcher script
- **Features**: Native integration, tabbed interface, interactive browser

## 🗄️ Database System

### Integration
- **`supabase_integration.py`** - Database integration script
- **`schema.sql`** - PostgreSQL schema definition

### Viewing Tools
- **`view_conversations.py`** - Command-line conversation viewer
- **`browse_conversations.py`** - Interactive conversation browser
- **`supabase_viewer.py`** - Database viewer with SQL queries
- **`view_db.sh`** - Database tools launcher

### Features
- Conversation persistence with Supabase
- Full-text search capabilities
- Export functionality (JSON/text)
- Session-based tracking
- Database statistics and analytics

## 🔌 API System

### REST Endpoints
- **Health & System**: `/api/health`, `/api/system/info`
- **Voice Controls**: `/api/voice/start`, `/api/voice/stop`
- **Conversations**: `/api/conversations/list`, `/api/conversations/search`
- **Export**: `/api/conversations/export/<id>`

### WebSocket Events
- **Real-time**: `process_output`, `process_complete`
- **Status**: `process_status`, `process_error`
- **Connection**: `connect`, `disconnect`

## ⚙️ Configuration

### Environment Setup
- **Configuration Directory**: `~/.config/voice-chatgpt/`
- **Environment File**: `~/.config/voice-chatgpt/.env`
- **Log Directory**: `~/.config/voice-chatgpt/logs/`

### Required Variables
```bash
OPENAI_API_KEY="your-openai-api-key"
CHATGPT_MODEL="gpt-3.5-turbo"
LOG_DIR="$HOME/.config/voice-chatgpt/logs"
```

### Optional Variables
```bash
SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supabase-key"
```

## 🚀 Quick Start Commands

### Voice Interaction
```bash
# Interactive voice chat
./voice-chatgpt.sh

# Quick 5-second query
./quick-ask.sh
```

### Web Interfaces
```bash
# Full-featured web server
./launch_web_server.sh
# Access at http://localhost:5000

# Simple web GUI
./launch_web_gui.sh
```

### Desktop Application
```bash
# Native desktop GUI
./launch_gui.sh
```

### Database Tools
```bash
# Interactive browser
./browse_conversations.py

# Command-line viewer
python3 view_conversations.py list --limit 10
```

## 📊 System Architecture

### Three-Tier GUI System
1. **Web Server** - Full REST API + WebSocket
2. **Web GUI** - Simple browser interface
3. **Desktop GUI** - Native desktop application

### Database Integration
- **Supabase PostgreSQL** - Managed database
- **Session Management** - Unique conversation tracking
- **Search & Export** - Full-text search and export capabilities

### Process Management
- **Background Processes** - Voice script execution
- **Real-time Monitoring** - WebSocket output streaming
- **Signal Handling** - Graceful process termination

## 🔧 Technical Stack

### Backend
- **Python 3.6+** - Core application language
- **Flask** - Web framework and API
- **Socket.IO** - Real-time communication
- **PostgreSQL** - Database (via Supabase)

### Frontend
- **HTML5/CSS3** - Web interface styling
- **JavaScript** - Client-side interactivity
- **tkinter** - Desktop GUI framework

### External Services
- **OpenAI API** - Whisper and ChatGPT
- **Supabase** - Managed PostgreSQL
- **macOS** - Built-in text-to-speech

## 🎯 Use Cases

### Personal Voice Assistant
- Quick voice queries for information
- Extended conversations with context
- Hands-free interaction while working

### Conversation Management
- Browse and search conversation history
- Export conversations for analysis
- Track usage patterns and statistics

### Development & Integration
- REST API for custom applications
- WebSocket for real-time monitoring
- Database integration for data persistence

### Remote Access
- Access from any device on network
- Mobile-friendly web interface
- Multi-user support capabilities

## 🚨 Troubleshooting

### Common Issues
- **Audio Problems**: Check microphone permissions and sox installation
- **API Errors**: Verify OpenAI API key and internet connection
- **Database Issues**: Check Supabase credentials and network
- **Port Conflicts**: Ensure port 5000 is available or change port

### Getting Help
- Check individual README files for specific issues
- Review installation guide for setup problems
- Consult API reference for integration issues
- Check changelog for known issues and fixes

## 🔮 Future Roadmap

### Planned Features
- User authentication system
- Multi-session support
- Audio playback in browser
- Real-time transcription display
- Advanced search filters
- Voice input from browser
- WebRTC integration
- Mobile app development

### Performance Improvements
- Database query caching
- Pagination for large datasets
- Lazy loading conversations
- Connection pooling
- Static file optimization

## 📄 License & Support

### License
This project is provided as-is for personal and educational use.

### Support
- **GitHub**: https://github.com/Jsgordon420365/heychat
- **Documentation**: This comprehensive documentation suite
- **Issues**: Report bugs in the GitHub Issues section

---

**This documentation index provides complete navigation for all HeyChat resources and documentation. 🚀**
