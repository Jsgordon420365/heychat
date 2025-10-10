# HeyChat Web Server

Modern HTTP/WebSocket frontend for the HeyChat voice conversation system.

## Features

### 🌐 Web-Based Interface
- Modern, responsive web UI accessible from any browser
- Real-time updates via WebSocket connections
- No desktop installation required
- Mobile-friendly design

### 🎤 Voice Controls
- Start voice chat sessions
- Quick ask (5-second voice queries)
- Real-time process output streaming
- Stop/manage running voice processes

### 🗄️ Database Management
- Browse recent conversations
- Search conversations by content
- View detailed conversation history
- Export conversations in JSON/TXT format
- Database statistics and analytics

### 📊 Real-Time Monitoring
- Live console output
- WebSocket-based process monitoring
- System status indicators
- Connection health checks

## Quick Start

### 1. Install Dependencies

```bash
# Install Flask and related packages
pip install -r requirements_gui.txt
```

Or install manually:
```bash
pip install flask flask-cors flask-socketio python-socketio python-engineio werkzeug
```

### 2. Launch the Server

```bash
# Using the launcher script (recommended)
./launch_web_server.sh

# Or directly with Python
python3 heychat_web_server.py
```

### 3. Access the Interface

Open your browser and navigate to:
- **Web UI**: http://localhost:5000
- **API Docs**: http://localhost:5000/api/health

## Architecture

### Backend (Flask + SocketIO)
- `heychat_web_server.py` - Main Flask application
- REST API endpoints for all HeyChat functions
- WebSocket support for real-time updates
- Process management for voice scripts
- Background thread monitoring

### Frontend (HTML/CSS/JS)
- `templates/index.html` - Single-page web application
- Vanilla JavaScript (no framework dependencies)
- Socket.IO client for real-time communication
- Responsive CSS with modern design

## API Endpoints

### Health & System
- `GET /api/health` - Health check
- `GET /api/system/info` - System information
- `GET /api/system/logs` - List log files
- `GET /api/system/test-connection` - Test database connection

### Voice Controls
- `POST /api/voice/start` - Start voice chat
- `POST /api/voice/quick-ask` - Start quick ask
- `POST /api/voice/stop/<process_id>` - Stop voice process
- `GET /api/voice/status/<process_id>` - Get process status

### Conversations
- `GET /api/conversations/list?limit=N` - List recent conversations
- `GET /api/conversations/search?q=term` - Search conversations
- `GET /api/conversations/show/<session_id>` - Show specific conversation
- `GET /api/conversations/stats` - Database statistics
- `GET /api/conversations/export/<session_id>?format=json` - Export conversation

## WebSocket Events

### Client → Server
- `connect` - Establish connection
- `disconnect` - Close connection
- `subscribe_process` - Subscribe to process updates

### Server → Client
- `connected` - Connection confirmation
- `process_output` - Real-time process output
- `process_complete` - Process completion notification
- `process_error` - Process error notification
- `process_status` - Process status update

## Configuration

### Environment Variables
The server uses the same configuration as the main HeyChat system:
- Configuration directory: `~/.config/voice-chatgpt/`
- Environment file: `~/.config/voice-chatgpt/.env`
- Log directory: `~/.config/voice-chatgpt/logs/`

### Port Configuration
Default port: 5000

To change the port, edit `heychat_web_server.py`:
```python
socketio.run(app, host='0.0.0.0', port=5000)  # Change port here
```

## Process Management

The web server includes a sophisticated process manager that:
- Starts voice scripts in background processes
- Monitors output in real-time
- Streams output to connected clients via WebSocket
- Handles graceful process termination
- Tracks process status and exit codes

## Security Considerations

### Current Setup (Development)
- Server binds to all interfaces (0.0.0.0)
- No authentication required
- CORS enabled for all origins
- Suitable for local development only

### Production Recommendations
1. Enable authentication
2. Use HTTPS/WSS
3. Restrict CORS origins
4. Add rate limiting
5. Use a production WSGI server (gunicorn/uwsgi)
6. Set up reverse proxy (nginx/apache)

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process or use a different port
```

### Dependencies Not Found
```bash
# Ensure you're using the correct Python environment
which python3
pip list | grep flask

# Reinstall dependencies
pip install --force-reinstall -r requirements_gui.txt
```

### WebSocket Connection Failed
- Check browser console for errors
- Verify firewall settings
- Ensure Socket.IO versions match (client/server)
- Try different browser

### Voice Scripts Not Running
- Verify script paths are correct
- Check script permissions (`chmod +x voice-chatgpt.sh`)
- Ensure scripts are in the same directory as the server
- Check console output for error messages

## Development

### Adding New Endpoints

```python
@app.route('/api/your-endpoint')
def your_function():
    return jsonify({"success": True, "data": "your data"})
```

### Adding WebSocket Events

```python
@socketio.on('your_event')
def handle_your_event(data):
    emit('response_event', {'result': 'data'})
```

### Frontend Integration

```javascript
// Call API endpoint
const response = await fetch('/api/your-endpoint');
const data = await response.json();

// Listen for WebSocket event
socket.on('response_event', (data) => {
    console.log(data);
});
```

## Comparison: Desktop GUI vs Web Server

### Desktop GUI (tkinter)
- ✅ No server required
- ✅ Native OS integration
- ✅ Lower latency
- ❌ Single machine only
- ❌ Requires X11/display

### Web Server (Flask)
- ✅ Remote access
- ✅ Multi-user support
- ✅ Mobile-friendly
- ✅ No display required
- ❌ Requires web server
- ❌ Network dependency

## Future Enhancements

### Planned Features
- [ ] User authentication
- [ ] Multi-session support
- [ ] Audio playback in browser
- [ ] Real-time transcription display
- [ ] Conversation threading
- [ ] Advanced search filters
- [ ] Export multiple formats
- [ ] Voice input from browser
- [ ] WebRTC integration
- [ ] Dark/light theme toggle

### Performance Improvements
- [ ] Database query caching
- [ ] Pagination for large datasets
- [ ] Lazy loading conversations
- [ ] Connection pooling
- [ ] Static file optimization

## License

Same as HeyChat main project.

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/Jsgordon420365/heychat
- Report bugs in the Issues section

## Credits

Built with:
- Flask - Web framework
- Socket.IO - Real-time communication
- Vanilla JavaScript - Frontend interactivity
- Python subprocess - Process management
