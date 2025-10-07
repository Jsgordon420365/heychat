# HeyChat GUI - Modern Interface for Voice AI Assistant

This directory contains two modern GUI applications for the HeyChat voice conversation system, providing easy access to all functions and scripts through an attractive user interface.

## 🎨 Available GUI Options

### 1. **Web GUI** (Recommended) 🌐
**File:** `heychat_web_gui.py`  
**Launcher:** `./launch_web_gui.sh`

A modern, responsive web-based interface that works on all platforms and devices.

**Features:**
- 🌐 **Cross-platform compatibility** - Works on any device with a web browser
- 📱 **Responsive design** - Adapts to different screen sizes
- 🎨 **Modern UI** - Beautiful gradient design with smooth animations
- ⚡ **Real-time updates** - Live status and log updates
- 🔄 **Auto-refresh** - Automatic browser opening and updates
- 📊 **Dashboard layout** - Organized sections for different functions

**Launch:**
```bash
./launch_web_gui.sh
```

### 2. **Desktop GUI** (Alternative) 🖥️
**File:** `heychat_gui.py`  
**Launcher:** `./launch_gui.sh`

A native desktop application using Python's tkinter framework.

**Features:**
- 🖥️ **Native desktop app** - Integrated with your operating system
- 🎯 **Tabbed interface** - Organized console, conversations, and logs
- ⌨️ **Keyboard shortcuts** - Quick access to functions
- 🎨 **Custom styling** - Modern dark theme with color coding
- 📋 **Tree view** - Interactive conversation browser

**Launch:**
```bash
./launch_gui.sh
```

## 🚀 Quick Start

### Web GUI (Recommended)
```bash
# Make sure you're in the HeyChat directory
cd /Users/gordo/Projects/heychat

# Launch the web GUI
./launch_web_gui.sh
```

The web interface will automatically open in your browser at `http://localhost:5000`

### Desktop GUI (Alternative)
```bash
# Launch the desktop GUI
./launch_gui.sh
```

## 🎯 GUI Features

### 🎤 Voice Controls
- **Start Voice Chat** - Begin interactive voice conversation
- **Quick Ask (5s)** - Record a 5-second voice query
- **Stop Process** - Terminate any running voice process

### 🗄️ Database Management
- **Browse Conversations** - Interactive conversation browser
- **Search Conversations** - Search by content across all conversations
- **View Recent** - Show recent conversation activity
- **Database Statistics** - View usage statistics and analytics

### 🛠️ Tools & Utilities
- **Export Conversations** - Export in JSON or text format
- **View Logs** - Access system and conversation logs
- **Open GitHub** - Quick access to project repository

### ⚙️ Settings & Configuration
- **Test Connection** - Verify database connectivity
- **Configuration** - View environment settings
- **About** - Application information and help

## 🎨 Interface Design

### Web GUI Design
- **Modern gradient background** with professional color scheme
- **Card-based layout** for organized function grouping
- **Responsive grid system** that adapts to screen size
- **Smooth animations** and hover effects
- **Real-time status updates** and live logging
- **Modal dialogs** for search and export functions

### Desktop GUI Design
- **Dark theme** with professional color coding
- **Tabbed interface** for organized content
- **Tree view** for conversation browsing
- **Color-coded console** with syntax highlighting
- **Status bar** with real-time updates

## 📱 Usage Examples

### Starting a Voice Conversation
1. Click **"Start Voice Chat"** in the Voice Controls section
2. The system will start the voice chat script
3. Monitor the output in the console/logs area
4. Use **"Stop Process"** to terminate if needed

### Searching Conversations
1. Click **"Search"** in the Database section
2. Enter your search term in the modal dialog
3. View results in the console output
4. Results show matching conversations with timestamps

### Exporting Data
1. Click **"Export"** in the Tools section
2. Enter the session ID in the modal dialog
3. Choose format (JSON or Text)
4. Download the exported conversation file

### Viewing Statistics
1. Click **"Statistics"** in the Database section
2. View comprehensive database analytics
3. See conversation counts, message totals, and usage patterns

## 🔧 Technical Details

### Web GUI Architecture
- **Backend:** Flask web framework
- **Frontend:** HTML5, CSS3, JavaScript
- **API:** RESTful endpoints for all functions
- **Real-time:** AJAX-based updates
- **Templates:** Dynamic HTML generation

### Desktop GUI Architecture
- **Framework:** Python tkinter
- **Styling:** Custom ttk themes
- **Threading:** Background process management
- **File I/O:** Real-time log monitoring
- **Cross-platform:** Works on macOS, Windows, Linux

### Dependencies
**Web GUI:**
- Python 3.6+
- Flask (`pip install flask`)

**Desktop GUI:**
- Python 3.6+
- tkinter (usually included with Python)

## 🚨 Troubleshooting

### Web GUI Issues
1. **"Flask not found"**
   ```bash
   pip3 install flask
   ```

2. **"Port 5000 in use"**
   - The script will show an error if port 5000 is occupied
   - Kill the process using port 5000 or modify the port in the script

3. **"Browser doesn't open"**
   - Manually navigate to `http://localhost:5000`
   - Check firewall settings

### Desktop GUI Issues
1. **"tkinter not available"**
   ```bash
   # macOS
   brew install python-tk
   
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   ```

2. **"Permission denied"**
   ```bash
   chmod +x launch_gui.sh
   ```

### General Issues
1. **"Scripts not found"**
   - Ensure you're in the HeyChat project directory
   - Check that all scripts are executable (`chmod +x *.sh`)

2. **"Database connection failed"**
   - Verify Supabase MCP connector is running
   - Check environment variables in `~/.config/voice-chatgpt/.env`

## 🎯 Integration with Voice Scripts

The GUI seamlessly integrates with all HeyChat components:

- **Voice Scripts:** Direct control of `voice-chatgpt.sh` and `quick-ask.sh`
- **Database Tools:** Integration with all viewing and management scripts
- **Export Functions:** Direct access to conversation export capabilities
- **Log Monitoring:** Real-time access to system and conversation logs
- **Settings Management:** Easy access to configuration and testing

## 🔮 Future Enhancements

Planned improvements for the GUI:

- **Real-time transcription display** in the web interface
- **Audio waveform visualization** during recording
- **Conversation timeline** with visual message flow
- **Voice command recognition** for GUI control
- **Mobile app** version for iOS/Android
- **Dark/light theme** toggle
- **Keyboard shortcuts** for power users
- **Plugin system** for custom extensions

## 📚 Documentation

- **Main README:** Complete project documentation
- **VIEWING_TOOLS.md:** Database viewing tools guide
- **GUI_README.md:** This GUI documentation
- **GitHub Repository:** https://github.com/Jsgordon420365/heychat

## 🤝 Contributing

To contribute to the GUI development:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the main README for details.

---

**Enjoy using HeyChat with its modern, intuitive GUI interface! 🎉**
