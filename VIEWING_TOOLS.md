# HeyChat Database Viewing Tools

This directory contains several tools for viewing and managing conversation data stored in the Supabase database.

## 🛠️ Available Tools

### 1. Interactive Browser (`browse_conversations.py`)
**Recommended for most users**

An interactive terminal interface for browsing conversations with a user-friendly menu system.

```bash
./browse_conversations.py
```

**Features:**
- 📋 List conversations with pagination
- 🔍 Search conversations by content
- 📊 View statistics
- 📤 Export conversations
- 🗣️ View detailed conversation history
- ⌨️ Keyboard navigation

**Commands:**
- `list [n]` - List conversations (n = number to show)
- `show <session_id>` - Show detailed conversation
- `search <term>` - Search conversations
- `stats` - Show statistics
- `export <session_id>` - Export conversation
- `next` / `prev` - Navigate pages
- `help` - Show available commands
- `quit` - Exit browser

### 2. Command Line Viewer (`view_conversations.py`)
**For scripting and automation**

A command-line tool for viewing conversations with various options.

```bash
# List recent conversations
python3 view_conversations.py list --limit 10

# Show specific conversation
python3 view_conversations.py show --session-id session_20251007120000_abc123

# Search conversations
python3 view_conversations.py search --search "python"

# Show statistics
python3 view_conversations.py stats

# Export conversation
python3 view_conversations.py export --session-id session_20251007120000_abc123 --format json
```

### 3. Supabase Viewer (`supabase_viewer.py`)
**For database administrators**

Shows SQL queries and database structure information.

```bash
# Show database information
python3 supabase_viewer.py info

# List conversations (shows SQL queries)
python3 supabase_viewer.py list --limit 5

# Show conversation (shows SQL queries)
python3 supabase_viewer.py show --session-id session_20251007120000_abc123

# Search conversations (shows SQL queries)
python3 supabase_viewer.py search --search "python"

# Show statistics (shows SQL queries)
python3 supabase_viewer.py stats
```

### 4. Quick Access Script (`view_db.sh`)
**Easy entry point**

A shell script that provides a menu to choose between different viewing options.

```bash
./view_db.sh
```

## 📊 Database Schema

### Tables

**`conversations`**
- `id` - Primary key
- `session_id` - Unique session identifier
- `title` - Conversation title
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `is_active` - Whether conversation is active
- `metadata` - JSON metadata (TTS settings, etc.)

**`messages`**
- `id` - Primary key
- `conversation_id` - Foreign key to conversations
- `timestamp_str` - Timestamp in yyyymmddhhmmss format
- `role` - 'user' or 'assistant'
- `content` - Message content
- `audio_file_path` - Path to audio file
- `transcription_confidence` - Whisper confidence score
- `created_at` - Creation timestamp
- `metadata` - JSON metadata

**`conversation_fusions`**
- `id` - Primary key
- `source_conversation_id` - Source conversation ID
- `target_conversation_id` - Target conversation ID
- `fused_at` - Fusion timestamp
- `fusion_reason` - Reason for fusion
- `metadata` - JSON metadata

### Functions

- `generate_session_id()` - Generates unique session IDs
- `fuse_conversations(source_id, target_id, reason)` - Merges conversations
- `get_conversation_history_json(conv_id)` - Gets conversation as JSON

## 🔧 Usage Examples

### View Recent Conversations
```bash
# Interactive browser
./browse_conversations.py

# Command line
python3 view_conversations.py list --limit 5
```

### Search for Specific Topics
```bash
# Interactive browser
./browse_conversations.py
# Then type: search python

# Command line
python3 view_conversations.py search --search "python"
```

### Export Conversation
```bash
# Interactive browser
./browse_conversations.py
# Then type: export session_20251007120000_abc123

# Command line
python3 view_conversations.py export --session-id session_20251007120000_abc123 --format json
```

### View Statistics
```bash
# Interactive browser
./browse_conversations.py
# Then type: stats

# Command line
python3 view_conversations.py stats
```

## 📁 Export Formats

### JSON Format
```json
{
  "session_id": "session_20251007120000_abc123",
  "exported_at": "2025-01-15T12:00:00",
  "messages": [
    {
      "timestamp": "2025-01-15T12:00:00",
      "role": "user",
      "content": "Hello, how are you today?"
    },
    {
      "timestamp": "2025-01-15T12:00:05",
      "role": "assistant",
      "content": "I'm doing well, thank you for asking!"
    }
  ]
}
```

### Text Format
```
Conversation: session_20251007120000_abc123
Exported: 2025-01-15 12:00:00
==================================================

[2025-01-15T12:00:00] USER: Hello, how are you today?

[2025-01-15T12:00:05] ASSISTANT: I'm doing well, thank you for asking!
```

## 🚀 Integration with Voice Scripts

The viewing tools work seamlessly with the voice conversation scripts:

1. **Automatic Storage**: All conversations are automatically saved to Supabase
2. **Session Tracking**: Each voice session gets a unique session ID
3. **Real-time Access**: View conversations immediately after they're created
4. **Cross-session Continuity**: Conversations persist across script restarts

## 🔍 Troubleshooting

### Common Issues

1. **"Python3 not found"**
   - Install Python 3: `brew install python3`

2. **"Permission denied"**
   - Make scripts executable: `chmod +x *.py`

3. **"No conversations found"**
   - Run some voice conversations first using `./voice-chatgpt.sh`

4. **"Database connection failed"**
   - Check Supabase connection and credentials

### Getting Help

- Use `--help` flag with any command-line tool
- Type `help` in the interactive browser
- Check the main README.md for setup instructions

## 📝 Notes

- All timestamps are in yyyymmddhhmmss format as requested
- Conversations can be fused together using the database functions
- Export files are saved in the current directory
- The interactive browser supports keyboard shortcuts and history
