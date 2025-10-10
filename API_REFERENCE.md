# HeyChat API Reference

Complete reference for the HeyChat REST API and WebSocket events.

## 🌐 Base URL

```
http://localhost:5000
```

## 🔌 WebSocket Endpoint

```
ws://localhost:5000/socket.io
```

## 📡 REST API Endpoints

### Health & System

#### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T12:00:00.000Z",
  "version": "1.0.0"
}
```

#### `GET /api/system/info`
Get system information.

**Response:**
```json
{
  "base_dir": "/Users/gordo/Projects/heychat",
  "log_dir": "/Users/gordo/.config/voice-chatgpt/logs",
  "log_dir_exists": true,
  "env_file": "/Users/gordo/.config/voice-chatgpt/.env",
  "env_file_exists": true,
  "python_version": "Python 3.10.0",
  "timestamp": "2025-01-15T12:00:00.000Z"
}
```

#### `GET /api/system/logs`
Get recent log files.

**Response:**
```json
{
  "success": true,
  "logs": [
    {
      "name": "transcripts.log",
      "path": "/Users/gordo/.config/voice-chatgpt/logs/transcripts.log",
      "size": 1024,
      "modified": "2025-01-15T12:00:00.000Z"
    }
  ]
}
```

#### `GET /api/system/test-connection`
Test database connection.

**Response:**
```json
{
  "success": true,
  "output": "Database connection successful",
  "error": null
}
```

### Voice Controls

#### `POST /api/voice/start`
Start voice chat session.

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "process_id": "voice_chat",
  "description": "Voice Chat"
}
```

#### `POST /api/voice/quick-ask`
Start quick ask (5-second voice query).

**Request Body:**
```json
{}
```

**Response:**
```json
{
  "success": true,
  "process_id": "quick_ask",
  "description": "Quick Ask"
}
```

#### `POST /api/voice/stop/<process_id>`
Stop a voice process.

**Parameters:**
- `process_id` (string): Process identifier

**Response:**
```json
{
  "success": true,
  "message": "Process stopped"
}
```

#### `GET /api/voice/status/<process_id>`
Get voice process status.

**Parameters:**
- `process_id` (string): Process identifier

**Response:**
```json
{
  "running": true,
  "exists": true,
  "return_code": null
}
```

### Conversations

#### `GET /api/conversations/list`
List recent conversations.

**Query Parameters:**
- `limit` (integer, optional): Number of conversations to return (default: 20)

**Example:**
```
GET /api/conversations/list?limit=10
```

**Response:**
```json
{
  "success": true,
  "conversations": [
    {
      "session_id": "session_20250115120000_abc123",
      "title": "Sample Conversation",
      "message_count": 5,
      "last_activity": "2025-01-15T12:00:00.000Z"
    }
  ]
}
```

#### `GET /api/conversations/search`
Search conversations by content.

**Query Parameters:**
- `q` (string, required): Search term

**Example:**
```
GET /api/conversations/search?q=python
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "session_id": "session_20250115120000_abc123",
      "title": "Python Discussion",
      "matches": 3,
      "last_activity": "2025-01-15T12:00:00.000Z"
    }
  ]
}
```

#### `GET /api/conversations/show/<session_id>`
Show specific conversation details.

**Parameters:**
- `session_id` (string): Conversation session ID

**Response:**
```json
{
  "success": true,
  "conversation": {
    "session_id": "session_20250115120000_abc123",
    "title": "Sample Conversation",
    "messages": [
      {
        "timestamp": "2025-01-15T12:00:00.000Z",
        "role": "user",
        "content": "Hello, how are you?"
      },
      {
        "timestamp": "2025-01-15T12:00:05.000Z",
        "role": "assistant",
        "content": "I'm doing well, thank you for asking!"
      }
    ]
  }
}
```

#### `GET /api/conversations/stats`
Get database statistics.

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_conversations": 25,
    "total_messages": 150,
    "average_messages_per_conversation": 6.0,
    "most_active_day": "2025-01-15",
    "total_duration": "2h 30m"
  }
}
```

#### `GET /api/conversations/export/<session_id>`
Export conversation to file.

**Parameters:**
- `session_id` (string): Conversation session ID

**Query Parameters:**
- `format` (string, optional): Export format - "json" or "txt" (default: "json")

**Example:**
```
GET /api/conversations/export/session_20250115120000_abc123?format=json
```

**Response:**
- File download with appropriate MIME type
- Filename: `conversation_<session_id>.<format>`

## 🔌 WebSocket Events

### Client → Server Events

#### `connect`
Establish WebSocket connection.

**Emitted by:** Client
**Data:** None

#### `disconnect`
Close WebSocket connection.

**Emitted by:** Client
**Data:** None

#### `subscribe_process`
Subscribe to process updates.

**Emitted by:** Client
**Data:**
```json
{
  "process_id": "voice_chat"
}
```

### Server → Client Events

#### `connected`
Connection confirmation.

**Emitted by:** Server
**Data:**
```json
{
  "message": "Connected to HeyChat server",
  "timestamp": "2025-01-15T12:00:00.000Z"
}
```

#### `process_output`
Real-time process output.

**Emitted by:** Server
**Data:**
```json
{
  "process_id": "voice_chat",
  "output": "Recording... (4s silence = send, or Ctrl+C to stop)",
  "timestamp": "2025-01-15T12:00:00.000Z"
}
```

#### `process_complete`
Process completion notification.

**Emitted by:** Server
**Data:**
```json
{
  "process_id": "voice_chat",
  "return_code": 0,
  "description": "Voice Chat",
  "timestamp": "2025-01-15T12:00:00.000Z"
}
```

#### `process_error`
Process error notification.

**Emitted by:** Server
**Data:**
```json
{
  "process_id": "voice_chat",
  "error": "Process failed to start",
  "timestamp": "2025-01-15T12:00:00.000Z"
}
```

#### `process_status`
Process status update.

**Emitted by:** Server
**Data:**
```json
{
  "process_id": "voice_chat",
  "status": {
    "running": true,
    "exists": true,
    "return_code": null
  },
  "timestamp": "2025-01-15T12:00:00.000Z"
}
```

## 📝 Usage Examples

### JavaScript Client

```javascript
// Connect to WebSocket
const socket = io('http://localhost:5000');

// Listen for events
socket.on('connected', (data) => {
    console.log('Connected:', data.message);
});

socket.on('process_output', (data) => {
    console.log(`Process ${data.process_id}: ${data.output}`);
});

// Start voice chat
fetch('/api/voice/start', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({})
})
.then(response => response.json())
.then(data => {
    console.log('Voice chat started:', data);
});

// Search conversations
fetch('/api/conversations/search?q=python')
.then(response => response.json())
.then(data => {
    console.log('Search results:', data.results);
});
```

### Python Client

```python
import requests
import socketio

# REST API calls
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Start voice chat
response = requests.post('http://localhost:5000/api/voice/start')
print(response.json())

# WebSocket connection
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')

@sio.event
def process_output(data):
    print(f"Process {data['process_id']}: {data['output']}")

sio.connect('http://localhost:5000')
```

### cURL Examples

```bash
# Health check
curl http://localhost:5000/api/health

# Start voice chat
curl -X POST http://localhost:5000/api/voice/start

# List conversations
curl "http://localhost:5000/api/conversations/list?limit=10"

# Search conversations
curl "http://localhost:5000/api/conversations/search?q=python"

# Export conversation
curl -O "http://localhost:5000/api/conversations/export/session_123?format=json"
```

## 🚨 Error Handling

### HTTP Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Endpoint or resource not found
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
  "success": false,
  "error": "Error message description"
}
```

### Common Error Scenarios

1. **Process already running**
   ```json
   {
     "success": false,
     "error": "Process already running"
   }
   ```

2. **Process not found**
   ```json
   {
     "success": false,
     "error": "Process not found"
   }
   ```

3. **Database connection failed**
   ```json
   {
     "success": false,
     "error": "Database connection failed"
   }
   ```

## 🔒 Authentication

**Current Status:** No authentication required (development mode)

**Future Implementation:**
- JWT token-based authentication
- API key authentication
- User session management

## 📊 Rate Limiting

**Current Status:** No rate limiting implemented

**Future Implementation:**
- Request rate limiting per IP
- API key-based rate limiting
- WebSocket connection limits

## 🚀 Performance Considerations

### Response Times
- Health check: < 10ms
- Voice process start: < 100ms
- Conversation list: < 500ms
- Search queries: < 1000ms

### WebSocket Performance
- Real-time output streaming
- Low-latency process monitoring
- Efficient event broadcasting

### Database Optimization
- Indexed conversation queries
- Pagination for large datasets
- Cached statistics

---

**This API reference provides complete documentation for integrating with the HeyChat system programmatically. 🚀**
