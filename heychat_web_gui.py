#!/usr/bin/env python3
"""
HeyChat Web GUI - Modern web-based interface for HeyChat voice conversation system
Uses Flask for a responsive web interface that works on all platforms
"""

import os
import sys
import json
import subprocess
import threading
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
import time

app = Flask(__name__)
app.secret_key = 'heychat-secret-key-2025'

class HeyChatWebGUI:
    def __init__(self):
        self.current_process = None
        self.conversation_data = []
        self.logs = []
        
    def log_message(self, message, level="INFO"):
        """Add a message to the logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.logs.append(log_entry)
        # Keep only last 100 log entries
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
    
    def run_command(self, command, description=""):
        """Run a command and return the output"""
        try:
            self.log_message(f"Starting: {description}", "INFO")
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                timeout=30
            )
            
            if result.returncode == 0:
                self.log_message(f"Completed: {description}", "SUCCESS")
                return {"success": True, "output": result.stdout, "error": result.stderr}
            else:
                self.log_message(f"Failed: {description} (exit code: {result.returncode})", "ERROR")
                return {"success": False, "output": result.stdout, "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            self.log_message(f"Timeout: {description}", "ERROR")
            return {"success": False, "output": "", "error": "Command timed out"}
        except Exception as e:
            self.log_message(f"Error running {description}: {str(e)}", "ERROR")
            return {"success": False, "output": "", "error": str(e)}

# Global instance
heychat = HeyChatWebGUI()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Get current status"""
    return jsonify({
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "process_running": heychat.current_process is not None
    })

@app.route('/api/logs')
def api_logs():
    """Get recent logs"""
    return jsonify(heychat.logs[-20:])  # Last 20 log entries

@app.route('/api/voice/start', methods=['POST'])
def api_voice_start():
    """Start voice chat"""
    data = request.get_json()
    mode = data.get('mode', 'chat')  # 'chat' or 'quick'
    
    if mode == 'chat':
        command = "./voice-chatgpt.sh"
        description = "Voice Chat"
    else:
        command = "./quick-ask.sh"
        description = "Quick Ask"
    
    result = heychat.run_command(command, description)
    return jsonify(result)

@app.route('/api/voice/stop', methods=['POST'])
def api_voice_stop():
    """Stop voice process"""
    if heychat.current_process:
        try:
            heychat.current_process.terminate()
            heychat.current_process = None
            heychat.log_message("Voice process stopped", "WARNING")
            return jsonify({"success": True, "message": "Process stopped"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    else:
        return jsonify({"success": False, "error": "No process running"})

@app.route('/api/db/conversations')
def api_db_conversations():
    """Get conversations list"""
    result = heychat.run_command("python3 view_conversations.py list --limit 20", "List Conversations")
    return jsonify(result)

@app.route('/api/db/search', methods=['POST'])
def api_db_search():
    """Search conversations"""
    data = request.get_json()
    search_term = data.get('term', '')
    
    if not search_term:
        return jsonify({"success": False, "error": "Search term required"})
    
    result = heychat.run_command(f'python3 view_conversations.py search --search "{search_term}"', f"Search: {search_term}")
    return jsonify(result)

@app.route('/api/db/stats')
def api_db_stats():
    """Get database statistics"""
    result = heychat.run_command("python3 view_conversations.py stats", "Database Statistics")
    return jsonify(result)

@app.route('/api/db/export', methods=['POST'])
def api_db_export():
    """Export conversation"""
    data = request.get_json()
    session_id = data.get('session_id', '')
    format_type = data.get('format', 'json')
    
    if not session_id:
        return jsonify({"success": False, "error": "Session ID required"})
    
    result = heychat.run_command(f"python3 view_conversations.py export --session-id {session_id} --format {format_type}", f"Export: {session_id}")
    return jsonify(result)

@app.route('/api/tools/logs')
def api_tools_logs():
    """Get system logs"""
    log_dir = os.path.expanduser("~/.config/voice-chatgpt/logs")
    if os.path.exists(log_dir):
        result = heychat.run_command(f"ls -la {log_dir}", "Log Directory")
    else:
        result = {"success": False, "error": "Log directory not found"}
    return jsonify(result)

@app.route('/api/test/connection')
def api_test_connection():
    """Test database connection"""
    result = heychat.run_command("python3 supabase_viewer.py info", "Connection Test")
    return jsonify(result)

# Create templates directory and HTML files
def create_templates():
    """Create the HTML templates"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Main template
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HeyChat - Voice AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            margin: 5px;
            display: inline-block;
            text-decoration: none;
        }
        
        .btn:hover {
            background: linear-gradient(45deg, #2980b9, #1f5f8b);
            transform: translateY(-2px);
        }
        
        .btn-success {
            background: linear-gradient(45deg, #27ae60, #229954);
        }
        
        .btn-success:hover {
            background: linear-gradient(45deg, #229954, #1e8449);
        }
        
        .btn-warning {
            background: linear-gradient(45deg, #e74c3c, #c0392b);
        }
        
        .btn-warning:hover {
            background: linear-gradient(45deg, #c0392b, #a93226);
        }
        
        .status-bar {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .output-area {
            background: #1e1e1e;
            color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
            line-height: 1.5;
            max-height: 400px;
            overflow-y: auto;
            margin-top: 20px;
        }
        
        .log-entry {
            margin-bottom: 5px;
        }
        
        .log-info { color: #ffffff; }
        .log-success { color: #27ae60; }
        .log-warning { color: #f39c12; }
        .log-error { color: #e74c3c; }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        
        .modal-content {
            background-color: white;
            margin: 15% auto;
            padding: 20px;
            border-radius: 10px;
            width: 80%;
            max-width: 500px;
        }
        
        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
        }
        
        .close:hover {
            color: black;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .loading {
            display: none;
            text-align: center;
            color: #3498db;
            font-weight: 600;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎤 HeyChat Voice AI Assistant</h1>
            <p>Modern web interface for voice-based ChatGPT conversations</p>
        </div>
        
        <div class="status-bar">
            <div>
                <strong>Status:</strong> <span id="status">Ready</span>
            </div>
            <div>
                <strong>Time:</strong> <span id="current-time"></span>
            </div>
        </div>
        
        <div class="dashboard">
            <!-- Voice Controls -->
            <div class="card">
                <h3>🎤 Voice Controls</h3>
                <button class="btn btn-success" onclick="startVoiceChat()">Start Voice Chat</button>
                <button class="btn" onclick="startQuickAsk()">Quick Ask (5s)</button>
                <button class="btn btn-warning" onclick="stopVoiceProcess()">Stop Process</button>
            </div>
            
            <!-- Database -->
            <div class="card">
                <h3>🗄️ Database</h3>
                <button class="btn" onclick="loadConversations()">Browse Conversations</button>
                <button class="btn" onclick="searchConversations()">Search</button>
                <button class="btn" onclick="showStats()">Statistics</button>
            </div>
            
            <!-- Tools -->
            <div class="card">
                <h3>🛠️ Tools</h3>
                <button class="btn" onclick="exportConversation()">Export</button>
                <button class="btn" onclick="viewLogs()">View Logs</button>
                <button class="btn" onclick="openGitHub()">GitHub</button>
            </div>
            
            <!-- Settings -->
            <div class="card">
                <h3>⚙️ Settings</h3>
                <button class="btn" onclick="testConnection()">Test Connection</button>
                <button class="btn" onclick="showAbout()">About</button>
            </div>
        </div>
        
        <div class="output-area" id="output">
            <div class="log-entry log-info">[12:00:00] INFO: HeyChat Web GUI started successfully!</div>
            <div class="log-entry log-info">[12:00:00] INFO: Select a function from the dashboard to get started</div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div>Processing...</div>
        </div>
    </div>
    
    <!-- Search Modal -->
    <div id="searchModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('searchModal')">&times;</span>
            <h3>Search Conversations</h3>
            <div class="form-group">
                <label for="searchTerm">Search Term:</label>
                <input type="text" id="searchTerm" placeholder="Enter search term...">
            </div>
            <button class="btn" onclick="performSearch()">Search</button>
        </div>
    </div>
    
    <!-- Export Modal -->
    <div id="exportModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal('exportModal')">&times;</span>
            <h3>Export Conversation</h3>
            <div class="form-group">
                <label for="sessionId">Session ID:</label>
                <input type="text" id="sessionId" placeholder="Enter session ID...">
            </div>
            <div class="form-group">
                <label for="exportFormat">Format:</label>
                <select id="exportFormat">
                    <option value="json">JSON</option>
                    <option value="txt">Text</option>
                </select>
            </div>
            <button class="btn" onclick="performExport()">Export</button>
        </div>
    </div>
    
    <script>
        // Update time
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
        updateTime();
        
        // API functions
        async function apiCall(endpoint, method = 'GET', data = null) {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            
            if (data) {
                options.body = JSON.stringify(data);
            }
            
            try {
                const response = await fetch(endpoint, options);
                return await response.json();
            } catch (error) {
                console.error('API call failed:', error);
                return { success: false, error: error.message };
            }
        }
        
        function addLog(message, level = 'info') {
            const output = document.getElementById('output');
            const timestamp = new Date().toLocaleTimeString();
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${level}`;
            logEntry.textContent = `[${timestamp}] ${level.toUpperCase()}: ${message}`;
            output.appendChild(logEntry);
            output.scrollTop = output.scrollHeight;
        }
        
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }
        
        function hideLoading() {
            document.getElementById('loading').style.display = 'none';
        }
        
        // Voice functions
        async function startVoiceChat() {
            showLoading();
            const result = await apiCall('/api/voice/start', 'POST', { mode: 'chat' });
            hideLoading();
            
            if (result.success) {
                addLog('Voice chat started successfully', 'success');
                document.getElementById('status').textContent = 'Voice Chat Running';
            } else {
                addLog(`Failed to start voice chat: ${result.error}`, 'error');
            }
        }
        
        async function startQuickAsk() {
            showLoading();
            const result = await apiCall('/api/voice/start', 'POST', { mode: 'quick' });
            hideLoading();
            
            if (result.success) {
                addLog('Quick ask started successfully', 'success');
                document.getElementById('status').textContent = 'Quick Ask Running';
            } else {
                addLog(`Failed to start quick ask: ${result.error}`, 'error');
            }
        }
        
        async function stopVoiceProcess() {
            const result = await apiCall('/api/voice/stop', 'POST');
            
            if (result.success) {
                addLog('Voice process stopped', 'warning');
                document.getElementById('status').textContent = 'Ready';
            } else {
                addLog(`Failed to stop process: ${result.error}`, 'error');
            }
        }
        
        // Database functions
        async function loadConversations() {
            showLoading();
            const result = await apiCall('/api/db/conversations');
            hideLoading();
            
            if (result.success) {
                addLog('Conversations loaded successfully', 'success');
                addLog(result.output, 'info');
            } else {
                addLog(`Failed to load conversations: ${result.error}`, 'error');
            }
        }
        
        function searchConversations() {
            document.getElementById('searchModal').style.display = 'block';
        }
        
        async function performSearch() {
            const term = document.getElementById('searchTerm').value.trim();
            if (!term) {
                alert('Please enter a search term');
                return;
            }
            
            closeModal('searchModal');
            showLoading();
            
            const result = await apiCall('/api/db/search', 'POST', { term: term });
            hideLoading();
            
            if (result.success) {
                addLog(`Search completed for: ${term}`, 'success');
                addLog(result.output, 'info');
            } else {
                addLog(`Search failed: ${result.error}`, 'error');
            }
        }
        
        async function showStats() {
            showLoading();
            const result = await apiCall('/api/db/stats');
            hideLoading();
            
            if (result.success) {
                addLog('Database statistics retrieved', 'success');
                addLog(result.output, 'info');
            } else {
                addLog(`Failed to get statistics: ${result.error}`, 'error');
            }
        }
        
        // Tool functions
        function exportConversation() {
            document.getElementById('exportModal').style.display = 'block';
        }
        
        async function performExport() {
            const sessionId = document.getElementById('sessionId').value.trim();
            const format = document.getElementById('exportFormat').value;
            
            if (!sessionId) {
                alert('Please enter a session ID');
                return;
            }
            
            closeModal('exportModal');
            showLoading();
            
            const result = await apiCall('/api/db/export', 'POST', { 
                session_id: sessionId, 
                format: format 
            });
            hideLoading();
            
            if (result.success) {
                addLog(`Export completed for session: ${sessionId}`, 'success');
                addLog(result.output, 'info');
            } else {
                addLog(`Export failed: ${result.error}`, 'error');
            }
        }
        
        async function viewLogs() {
            showLoading();
            const result = await apiCall('/api/tools/logs');
            hideLoading();
            
            if (result.success) {
                addLog('System logs retrieved', 'success');
                addLog(result.output, 'info');
            } else {
                addLog(`Failed to get logs: ${result.error}`, 'error');
            }
        }
        
        function openGitHub() {
            window.open('https://github.com/Jsgordon420365/heychat', '_blank');
            addLog('Opening GitHub repository', 'info');
        }
        
        // Settings functions
        async function testConnection() {
            showLoading();
            const result = await apiCall('/api/test/connection');
            hideLoading();
            
            if (result.success) {
                addLog('Connection test successful', 'success');
                addLog(result.output, 'info');
            } else {
                addLog(`Connection test failed: ${result.error}`, 'error');
            }
        }
        
        function showAbout() {
            alert('HeyChat Voice AI Assistant\\n\\nVersion 1.0.0\\n\\nA modern web interface for voice-based ChatGPT conversations.\\n\\nGitHub: https://github.com/Jsgordon420365/heychat');
        }
        
        // Modal functions
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modals = document.getElementsByClassName('modal');
            for (let modal of modals) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            }
        }
        
        // Load recent logs on startup
        async function loadRecentLogs() {
            const result = await apiCall('/api/logs');
            if (result && result.length > 0) {
                const output = document.getElementById('output');
                output.innerHTML = '';
                result.forEach(log => {
                    const logEntry = document.createElement('div');
                    logEntry.className = `log-entry log-${log.level.toLowerCase()}`;
                    logEntry.textContent = `[${log.timestamp}] ${log.level}: ${log.message}`;
                    output.appendChild(logEntry);
                });
            }
        }
        
        // Initialize
        loadRecentLogs();
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
        f.write(index_html)

def main():
    """Main function to start the web GUI"""
    print("🎤 HeyChat Web GUI Starting...")
    
    # Create templates
    create_templates()
    
    # Start the Flask app
    print("✅ Templates created")
    print("🌐 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    
    # Open browser automatically
    def open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()
