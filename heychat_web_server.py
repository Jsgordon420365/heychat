#!/usr/bin/env python3
"""
HeyChat Web Server - Modern HTTP frontend for HeyChat voice conversation system
Provides REST API and web interface for all HeyChat functions
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import subprocess
import threading
import os
import json
import time
from datetime import datetime
from pathlib import Path
import signal

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
current_processes = {}
conversation_cache = []

# Configuration
BASE_DIR = Path(__file__).parent
LOG_DIR = Path.home() / ".config/voice-chatgpt/logs"
ENV_FILE = Path.home() / ".config/voice-chatgpt/.env"

class ProcessManager:
    """Manage background processes"""
    def __init__(self):
        self.processes = {}
        self.output_threads = {}

    def start_process(self, process_id, command, description):
        """Start a new background process"""
        if process_id in self.processes and self.processes[process_id].poll() is None:
            return {"success": False, "error": "Process already running"}

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=BASE_DIR,
                preexec_fn=os.setsid
            )

            self.processes[process_id] = process

            # Start output monitoring thread
            thread = threading.Thread(
                target=self._monitor_output,
                args=(process_id, process, description),
                daemon=True
            )
            thread.start()
            self.output_threads[process_id] = thread

            return {"success": True, "process_id": process_id, "description": description}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _monitor_output(self, process_id, process, description):
        """Monitor process output and emit via WebSocket"""
        try:
            for line in iter(process.stdout.readline, ''):
                if line:
                    socketio.emit('process_output', {
                        'process_id': process_id,
                        'output': line,
                        'timestamp': datetime.now().isoformat()
                    })

            process.wait()

            socketio.emit('process_complete', {
                'process_id': process_id,
                'return_code': process.returncode,
                'description': description,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            socketio.emit('process_error', {
                'process_id': process_id,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })

    def stop_process(self, process_id):
        """Stop a running process"""
        if process_id not in self.processes:
            return {"success": False, "error": "Process not found"}

        process = self.processes[process_id]
        if process.poll() is not None:
            return {"success": False, "error": "Process not running"}

        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=5)
            return {"success": True, "message": "Process stopped"}
        except Exception as e:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except:
                pass
            return {"success": False, "error": str(e)}

    def get_status(self, process_id):
        """Get process status"""
        if process_id not in self.processes:
            return {"running": False, "exists": False}

        process = self.processes[process_id]
        is_running = process.poll() is None

        return {
            "running": is_running,
            "exists": True,
            "return_code": process.returncode if not is_running else None
        }

process_manager = ProcessManager()

# Web Routes
@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

# Voice Control Endpoints
@app.route('/api/voice/start', methods=['POST'])
def start_voice_chat():
    """Start voice chat"""
    result = process_manager.start_process(
        'voice_chat',
        './voice-chatgpt.sh',
        'Voice Chat'
    )
    return jsonify(result)

@app.route('/api/voice/quick-ask', methods=['POST'])
def start_quick_ask():
    """Start quick ask (5s)"""
    result = process_manager.start_process(
        'quick_ask',
        './quick-ask.sh',
        'Quick Ask'
    )
    return jsonify(result)

@app.route('/api/voice/stop/<process_id>', methods=['POST'])
def stop_voice(process_id):
    """Stop voice process"""
    result = process_manager.stop_process(process_id)
    return jsonify(result)

@app.route('/api/voice/status/<process_id>')
def voice_status(process_id):
    """Get voice process status"""
    status = process_manager.get_status(process_id)
    return jsonify(status)

# Database Endpoints
@app.route('/api/conversations/list')
def list_conversations():
    """List recent conversations"""
    try:
        limit = request.args.get('limit', 20, type=int)
        result = subprocess.run(
            f'python3 view_conversations.py list --limit {limit} --format json',
            shell=True,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=10
        )

        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return jsonify({"success": True, "conversations": data})
            except json.JSONDecodeError:
                return jsonify({"success": True, "conversations": [], "raw_output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/conversations/search')
def search_conversations():
    """Search conversations"""
    try:
        search_term = request.args.get('q', '')
        if not search_term:
            return jsonify({"success": False, "error": "Search term required"})

        result = subprocess.run(
            f'python3 view_conversations.py search --search "{search_term}" --format json',
            shell=True,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=10
        )

        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return jsonify({"success": True, "results": data})
            except json.JSONDecodeError:
                return jsonify({"success": True, "results": [], "raw_output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/conversations/show/<session_id>')
def show_conversation(session_id):
    """Show specific conversation"""
    try:
        result = subprocess.run(
            f'python3 view_conversations.py show --session-id {session_id} --format json',
            shell=True,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=10
        )

        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return jsonify({"success": True, "conversation": data})
            except json.JSONDecodeError:
                return jsonify({"success": True, "conversation": {}, "raw_output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/conversations/stats')
def conversation_stats():
    """Get database statistics"""
    try:
        result = subprocess.run(
            'python3 view_conversations.py stats --format json',
            shell=True,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=10
        )

        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return jsonify({"success": True, "stats": data})
            except json.JSONDecodeError:
                return jsonify({"success": True, "stats": {}, "raw_output": result.stdout})
        else:
            return jsonify({"success": False, "error": result.stderr})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/conversations/export/<session_id>')
def export_conversation(session_id):
    """Export conversation"""
    try:
        format_type = request.args.get('format', 'json')
        output_file = f'/tmp/conversation_{session_id}.{format_type}'

        result = subprocess.run(
            f'python3 view_conversations.py export --session-id {session_id} --format {format_type} --output {output_file}',
            shell=True,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=10
        )

        if result.returncode == 0 and os.path.exists(output_file):
            return send_file(
                output_file,
                as_attachment=True,
                download_name=f'conversation_{session_id}.{format_type}'
            )
        else:
            return jsonify({"success": False, "error": result.stderr})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# System Endpoints
@app.route('/api/system/info')
def system_info():
    """Get system information"""
    info = {
        "base_dir": str(BASE_DIR),
        "log_dir": str(LOG_DIR),
        "log_dir_exists": LOG_DIR.exists(),
        "env_file": str(ENV_FILE),
        "env_file_exists": ENV_FILE.exists(),
        "python_version": subprocess.run(['python3', '--version'], capture_output=True, text=True).stdout.strip(),
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(info)

@app.route('/api/system/logs')
def get_logs():
    """Get recent log files"""
    try:
        if not LOG_DIR.exists():
            return jsonify({"success": False, "error": "Log directory not found"})

        logs = []
        for log_file in sorted(LOG_DIR.glob('*.log'), key=os.path.getmtime, reverse=True)[:10]:
            logs.append({
                "name": log_file.name,
                "path": str(log_file),
                "size": log_file.stat().st_size,
                "modified": datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
            })

        return jsonify({"success": True, "logs": logs})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/system/test-connection')
def test_connection():
    """Test database connection"""
    try:
        result = subprocess.run(
            'python3 supabase_viewer.py info',
            shell=True,
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            timeout=10
        )

        return jsonify({
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {
        'message': 'Connected to HeyChat server',
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('subscribe_process')
def handle_subscribe(data):
    """Subscribe to process updates"""
    process_id = data.get('process_id')
    status = process_manager.get_status(process_id)
    emit('process_status', {
        'process_id': process_id,
        'status': status,
        'timestamp': datetime.now().isoformat()
    })

def main():
    """Start the web server"""
    port = 5001
    print(f"""
    ╔════════════════════════════════════════════╗
    ║   HeyChat Web Server                       ║
    ║   Voice AI Assistant - HTTP Interface      ║
    ╚════════════════════════════════════════════╝

    🌐 Server starting...
    📡 API: http://localhost:{port}/api
    🎨 Web UI: http://localhost:{port}
    🔌 WebSocket: ws://localhost:{port}/socket.io

    Press Ctrl+C to stop
    """)

    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main()
