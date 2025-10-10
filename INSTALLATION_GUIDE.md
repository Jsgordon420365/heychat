# HeyChat Installation Guide

Complete installation guide for the HeyChat voice AI assistant system.

## 📋 Prerequisites

### System Requirements
- **macOS** 10.14+ (primary platform)
- **Python** 3.6+ (required for all components)
- **Internet connection** (for OpenAI API calls)
- **Microphone** (for voice recording)
- **Speakers/Headphones** (for text-to-speech output)

### Hardware Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **Network**: Stable internet connection for API calls

## 🚀 Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Jsgordon420365/heychat.git
cd heychat
```

### 2. Install System Dependencies
```bash
# Install sox for audio recording
brew install sox

# Install jq for JSON parsing
brew install jq

# Install Python 3 (if not already installed)
brew install python3
```

### 3. Install Python Dependencies
```bash
# Install GUI dependencies
pip3 install -r requirements_gui.txt

# Or install manually
pip3 install flask flask-cors flask-socketio python-socketio python-engineio werkzeug
```

### 4. Set Up Configuration
```bash
# Create configuration directory
mkdir -p "$HOME/.config/voice-chatgpt"

# Create environment file
cat > "$HOME/.config/voice-chatgpt/.env" << EOF
OPENAI_API_KEY="your-openai-api-key-here"
CHATGPT_MODEL="gpt-3.5-turbo"
LOG_DIR="$HOME/.config/voice-chatgpt/logs"
EOF
```

### 5. Make Scripts Executable
```bash
chmod +x *.sh
chmod +x *.py
```

## 🔧 Detailed Installation

### Step 1: System Dependencies

#### macOS (Homebrew)
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install sox jq python3
```

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install sox jq python3 python3-pip python3-tk
```

#### CentOS/RHEL
```bash
# Install EPEL repository
sudo yum install epel-release

# Install required packages
sudo yum install sox jq python3 python3-pip tkinter
```

### Step 2: Python Environment

#### Option A: System Python (Recommended)
```bash
# Install dependencies globally
pip3 install -r requirements_gui.txt
```

#### Option B: Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_gui.txt
```

#### Option C: Conda Environment
```bash
# Create conda environment
conda create -n heychat python=3.10

# Activate environment
conda activate heychat

# Install dependencies
pip install -r requirements_gui.txt
```

### Step 3: Configuration Setup

#### Environment Variables
Create `~/.config/voice-chatgpt/.env`:

```bash
# OpenAI API Configuration
OPENAI_API_KEY="sk-your-openai-api-key-here"
CHATGPT_MODEL="gpt-3.5-turbo"  # or gpt-4, gpt-4-turbo

# Logging Configuration
LOG_DIR="$HOME/.config/voice-chatgpt/logs"

# Optional: Supabase Configuration (if using database features)
SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supabase-key"
```

#### API Key Setup
1. **Get OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Create account or sign in
   - Navigate to API Keys section
   - Create new secret key
   - Copy the key (starts with `sk-`)

2. **Add to Configuration**:
   ```bash
   # Edit the .env file
   nano "$HOME/.config/voice-chatgpt/.env"
   
   # Replace "your-openai-api-key-here" with your actual key
   OPENAI_API_KEY="sk-proj-abc123..."
   ```

### Step 4: Database Setup (Optional)

#### Supabase Setup
1. **Create Supabase Project**:
   - Visit [Supabase](https://supabase.com/)
   - Create new project
   - Note the project URL and API key

2. **Run Database Schema**:
   ```bash
   # Connect to your Supabase database and run schema.sql
   psql -h your-db-host -U postgres -d postgres -f schema.sql
   ```

3. **Update Configuration**:
   ```bash
   # Add Supabase credentials to .env file
   echo "SUPABASE_URL=https://your-project.supabase.co" >> "$HOME/.config/voice-chatgpt/.env"
   echo "SUPABASE_KEY=your-supabase-anon-key" >> "$HOME/.config/voice-chatgpt/.env"
   ```

## 🧪 Verification

### Test Voice Scripts
```bash
# Test quick ask (5-second recording)
./quick-ask.sh

# Test voice chat (interactive)
./voice-chatgpt.sh
```

### Test GUI Applications
```bash
# Test web server
./launch_web_server.sh
# Open http://localhost:5000 in browser

# Test desktop GUI
./launch_gui.sh
```

### Test Database Tools
```bash
# Test conversation viewer
python3 view_conversations.py list --limit 5

# Test interactive browser
./browse_conversations.py
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "rec: command not found"
```bash
# Install sox
brew install sox  # macOS
sudo apt install sox  # Ubuntu
```

#### 2. "jq: command not found"
```bash
# Install jq
brew install jq  # macOS
sudo apt install jq  # Ubuntu
```

#### 3. "tkinter not available"
```bash
# macOS
brew install python-tk

# Ubuntu
sudo apt install python3-tk

# CentOS
sudo yum install tkinter
```

#### 4. "Flask not found"
```bash
# Install Flask
pip3 install flask flask-cors flask-socketio
```

#### 5. "Permission denied"
```bash
# Make scripts executable
chmod +x *.sh *.py
```

#### 6. "API key not found"
```bash
# Check .env file exists and has correct key
cat "$HOME/.config/voice-chatgpt/.env"

# Verify API key format
echo $OPENAI_API_KEY
```

#### 7. "Port 5000 in use"
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port (edit heychat_web_server.py)
```

### Audio Issues

#### Microphone Not Working
1. **Check System Permissions**:
   - System Preferences → Security & Privacy → Privacy → Microphone
   - Ensure Terminal/Python has microphone access

2. **Test Microphone**:
   ```bash
   # Test with sox
   rec -t wav test.wav trim 0 3
   play test.wav
   rm test.wav
   ```

3. **Check Audio Input**:
   ```bash
   # List audio devices
   sox --version
   ```

#### Text-to-Speech Not Working
1. **Check macOS Speech Settings**:
   - System Preferences → Accessibility → Speech
   - Test system voice

2. **Test with say command**:
   ```bash
   say "Hello, this is a test"
   ```

### Database Issues

#### Supabase Connection Failed
1. **Check Credentials**:
   ```bash
   # Verify environment variables
   echo $SUPABASE_URL
   echo $SUPABASE_KEY
   ```

2. **Test Connection**:
   ```bash
   python3 supabase_viewer.py info
   ```

3. **Check Network**:
   ```bash
   curl -I https://your-project.supabase.co
   ```

## 🚀 Advanced Configuration

### Custom Port Configuration
```bash
# Edit heychat_web_server.py
# Change port from 5000 to desired port
socketio.run(app, host='0.0.0.0', port=8080)
```

### Custom Log Directory
```bash
# Set custom log directory in .env
LOG_DIR="/custom/path/to/logs"
mkdir -p "$LOG_DIR"
```

### Custom Audio Settings
```bash
# Edit voice-chatgpt.sh for custom audio settings
# Change silence detection parameters
rec -t wav "$AUDIO_FILE" trim 0 30 silence 1 0.1 1% 1 4.0 1%
```

### Environment-Specific Configuration
```bash
# Development
export HEYCHAT_ENV=development

# Production
export HEYCHAT_ENV=production
```

## 📊 Performance Optimization

### System Optimization
```bash
# Increase file descriptor limits
ulimit -n 4096

# Optimize Python performance
export PYTHONOPTIMIZE=1
```

### Database Optimization
```sql
-- Add indexes for better performance
CREATE INDEX idx_messages_content ON messages USING gin(to_tsvector('english', content));
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
```

### Web Server Optimization
```python
# Use production WSGI server
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 heychat_web_server:app
```

## 🔒 Security Considerations

### API Key Security
```bash
# Set proper file permissions
chmod 600 "$HOME/.config/voice-chatgpt/.env"

# Never commit API keys to version control
echo ".env" >> .gitignore
```

### Network Security
```bash
# For production, bind to localhost only
socketio.run(app, host='127.0.0.1', port=5000)

# Use HTTPS in production
# Set up reverse proxy with SSL
```

## 📚 Next Steps

After successful installation:

1. **Read the Documentation**:
   - [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) - Complete project overview
   - [GUI_README.md](GUI_README.md) - GUI applications guide
   - [API_REFERENCE.md](API_REFERENCE.md) - API documentation

2. **Start Using HeyChat**:
   ```bash
   # Launch web interface
   ./launch_web_server.sh
   
   # Or use voice scripts directly
   ./voice-chatgpt.sh
   ```

3. **Explore Features**:
   - Voice conversations
   - Database management
   - API integration
   - Real-time monitoring

---

**Congratulations! You've successfully installed HeyChat. Enjoy your voice AI assistant! 🎉**
