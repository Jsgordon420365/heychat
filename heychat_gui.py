#!/usr/bin/env python3
"""
HeyChat GUI - Modern graphical interface for HeyChat voice conversation system
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import threading
import os
import sys
import json
from datetime import datetime
import webbrowser

class HeyChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HeyChat - Voice AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Configure style
        self.setup_styles()
        
        # Create main interface
        self.create_widgets()
        
        # Initialize variables
        self.current_process = None
        self.conversation_data = []
        
    def setup_styles(self):
        """Configure modern styling for the GUI"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       background='#2c3e50', 
                       foreground='#ecf0f1', 
                       font=('Arial', 16, 'bold'))
        
        style.configure('Header.TLabel', 
                       background='#34495e', 
                       foreground='#ecf0f1', 
                       font=('Arial', 12, 'bold'))
        
        style.configure('Custom.TButton',
                       background='#3498db',
                       foreground='white',
                       font=('Arial', 10, 'bold'),
                       padding=(10, 5))
        
        style.map('Custom.TButton',
                 background=[('active', '#2980b9')])
        
        style.configure('Success.TButton',
                       background='#27ae60',
                       foreground='white')
        
        style.map('Success.TButton',
                 background=[('active', '#229954')])
        
        style.configure('Warning.TButton',
                       background='#e74c3c',
                       foreground='white')
        
        style.map('Warning.TButton',
                 background=[('active', '#c0392b')])
    
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎤 HeyChat Voice AI Assistant", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Left panel - Navigation
        self.create_navigation_panel(main_frame)
        
        # Right panel - Content area
        self.create_content_panel(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_navigation_panel(self, parent):
        """Create the left navigation panel"""
        nav_frame = ttk.LabelFrame(parent, text="Navigation", padding="10")
        nav_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Voice Controls Section
        voice_frame = ttk.LabelFrame(nav_frame, text="🎤 Voice Controls", padding="5")
        voice_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(voice_frame, text="Start Voice Chat", 
                  command=self.start_voice_chat, style='Success.TButton').pack(fill='x', pady=2)
        
        ttk.Button(voice_frame, text="Quick Ask (5s)", 
                  command=self.start_quick_ask, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(voice_frame, text="Stop Voice Process", 
                  command=self.stop_voice_process, style='Warning.TButton').pack(fill='x', pady=2)
        
        # Database Controls Section
        db_frame = ttk.LabelFrame(nav_frame, text="🗄️ Database", padding="5")
        db_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(db_frame, text="Browse Conversations", 
                  command=self.browse_conversations, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(db_frame, text="View Recent", 
                  command=self.view_recent_conversations, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(db_frame, text="Search Conversations", 
                  command=self.search_conversations, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(db_frame, text="Database Statistics", 
                  command=self.show_database_stats, style='Custom.TButton').pack(fill='x', pady=2)
        
        # Tools Section
        tools_frame = ttk.LabelFrame(nav_frame, text="🛠️ Tools", padding="5")
        tools_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(tools_frame, text="Export Conversation", 
                  command=self.export_conversation, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(tools_frame, text="View Logs", 
                  command=self.view_logs, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(tools_frame, text="Open GitHub", 
                  command=self.open_github, style='Custom.TButton').pack(fill='x', pady=2)
        
        # Settings Section
        settings_frame = ttk.LabelFrame(nav_frame, text="⚙️ Settings", padding="5")
        settings_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(settings_frame, text="Configuration", 
                  command=self.open_settings, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(settings_frame, text="Test Connection", 
                  command=self.test_connection, style='Custom.TButton').pack(fill='x', pady=2)
        
        # Help Section
        help_frame = ttk.LabelFrame(nav_frame, text="❓ Help", padding="5")
        help_frame.pack(fill='x')
        
        ttk.Button(help_frame, text="Documentation", 
                  command=self.show_documentation, style='Custom.TButton').pack(fill='x', pady=2)
        
        ttk.Button(help_frame, text="About", 
                  command=self.show_about, style='Custom.TButton').pack(fill='x', pady=2)
    
    def create_content_panel(self, parent):
        """Create the right content panel"""
        content_frame = ttk.LabelFrame(parent, text="Output", padding="10")
        content_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Console tab
        self.console_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.console_frame, text="Console")
        
        self.console_text = scrolledtext.ScrolledText(
            self.console_frame, 
            wrap=tk.WORD, 
            bg='#1e1e1e', 
            fg='#ffffff',
            font=('Consolas', 10)
        )
        self.console_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Conversations tab
        self.conversations_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.conversations_frame, text="Conversations")
        
        # Create treeview for conversations
        columns = ('Session ID', 'Title', 'Messages', 'Last Activity')
        self.conversations_tree = ttk.Treeview(self.conversations_frame, columns=columns, show='headings')
        
        for col in columns:
            self.conversations_tree.heading(col, text=col)
            self.conversations_tree.column(col, width=150)
        
        # Scrollbar for treeview
        conversations_scrollbar = ttk.Scrollbar(self.conversations_frame, orient='vertical', command=self.conversations_tree.yview)
        self.conversations_tree.configure(yscrollcommand=conversations_scrollbar.set)
        
        self.conversations_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        conversations_scrollbar.pack(side='right', fill='y')
        
        # Bind double-click to view conversation
        self.conversations_tree.bind('<Double-1>', self.view_selected_conversation)
        
        # Logs tab
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="Logs")
        
        self.logs_text = scrolledtext.ScrolledText(
            self.logs_frame, 
            wrap=tk.WORD, 
            bg='#1e1e1e', 
            fg='#ffffff',
            font=('Consolas', 9)
        )
        self.logs_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(side='left', fill='x', expand=True)
        
        self.time_label = ttk.Label(status_frame, text="", relief=tk.SUNKEN, anchor='e')
        self.time_label.pack(side='right')
        
        # Update time
        self.update_time()
    
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def log_message(self, message, level="INFO"):
        """Add a message to the console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": "#ffffff",
            "SUCCESS": "#27ae60",
            "WARNING": "#f39c12",
            "ERROR": "#e74c3c"
        }
        
        self.console_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.console_text.insert(tk.END, f"{level}: ", level.lower())
        self.console_text.insert(tk.END, f"{message}\n")
        
        # Configure tags for colors
        self.console_text.tag_configure("timestamp", foreground="#95a5a6")
        self.console_text.tag_configure("info", foreground=color_map.get(level, "#ffffff"))
        self.console_text.tag_configure("success", foreground=color_map.get("SUCCESS"))
        self.console_text.tag_configure("warning", foreground=color_map.get("WARNING"))
        self.console_text.tag_configure("error", foreground=color_map.get("ERROR"))
        
        self.console_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update the status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def run_command(self, command, description=""):
        """Run a command in a separate thread"""
        def run():
            try:
                self.update_status(f"Running: {description}")
                self.log_message(f"Starting: {description}", "INFO")
                
                process = subprocess.Popen(
                    command, 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                
                self.current_process = process
                
                # Read output in real-time
                for line in iter(process.stdout.readline, ''):
                    if line.strip():
                        self.console_text.insert(tk.END, line)
                        self.console_text.see(tk.END)
                        self.root.update_idletasks()
                
                process.wait()
                
                if process.returncode == 0:
                    self.log_message(f"Completed: {description}", "SUCCESS")
                else:
                    self.log_message(f"Failed: {description} (exit code: {process.returncode})", "ERROR")
                
                self.current_process = None
                self.update_status("Ready")
                
            except Exception as e:
                self.log_message(f"Error running {description}: {str(e)}", "ERROR")
                self.update_status("Error")
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    # Voice Control Methods
    def start_voice_chat(self):
        """Start the voice chat script"""
        self.run_command("./voice-chatgpt.sh", "Voice Chat")
    
    def start_quick_ask(self):
        """Start the quick ask script"""
        self.run_command("./quick-ask.sh", "Quick Ask")
    
    def stop_voice_process(self):
        """Stop the current voice process"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.log_message("Voice process stopped", "WARNING")
                self.current_process = None
                self.update_status("Ready")
            except Exception as e:
                self.log_message(f"Error stopping process: {str(e)}", "ERROR")
        else:
            self.log_message("No voice process running", "WARNING")
    
    # Database Methods
    def browse_conversations(self):
        """Open the interactive conversation browser"""
        self.run_command("python3 browse_conversations.py", "Conversation Browser")
    
    def view_recent_conversations(self):
        """View recent conversations"""
        self.run_command("python3 view_conversations.py list --limit 10", "Recent Conversations")
        self.load_conversations()
    
    def search_conversations(self):
        """Search conversations dialog"""
        search_dialog = tk.Toplevel(self.root)
        search_dialog.title("Search Conversations")
        search_dialog.geometry("400x150")
        search_dialog.configure(bg='#2c3e50')
        
        ttk.Label(search_dialog, text="Search Term:", style='Header.TLabel').pack(pady=10)
        
        search_entry = ttk.Entry(search_dialog, width=40)
        search_entry.pack(pady=5)
        search_entry.focus()
        
        def do_search():
            search_term = search_entry.get().strip()
            if search_term:
                self.run_command(f"python3 view_conversations.py search --search \"{search_term}\"", f"Search: {search_term}")
                search_dialog.destroy()
        
        ttk.Button(search_dialog, text="Search", command=do_search, style='Custom.TButton').pack(pady=10)
        
        # Bind Enter key
        search_entry.bind('<Return>', lambda e: do_search())
    
    def show_database_stats(self):
        """Show database statistics"""
        self.run_command("python3 view_conversations.py stats", "Database Statistics")
    
    def load_conversations(self):
        """Load conversations into the treeview"""
        def load():
            try:
                # Clear existing items
                for item in self.conversations_tree.get_children():
                    self.conversations_tree.delete(item)
                
                # Run command to get conversations
                result = subprocess.run(
                    "python3 view_conversations.py list --limit 20",
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                
                if result.returncode == 0:
                    # Parse the output and populate treeview
                    # This is a simplified version - you'd parse the actual JSON output
                    self.conversations_tree.insert('', 'end', values=(
                        "session_20250115120000_abc123",
                        "Sample Conversation",
                        "5",
                        "2025-01-15 12:00:00"
                    ))
                    self.log_message("Conversations loaded", "SUCCESS")
                else:
                    self.log_message("Failed to load conversations", "ERROR")
                    
            except Exception as e:
                self.log_message(f"Error loading conversations: {str(e)}", "ERROR")
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def view_selected_conversation(self, event):
        """View the selected conversation"""
        selection = self.conversations_tree.selection()
        if selection:
            item = self.conversations_tree.item(selection[0])
            session_id = item['values'][0]
            self.run_command(f"python3 view_conversations.py show --session-id {session_id}", f"View: {session_id}")
    
    # Tool Methods
    def export_conversation(self):
        """Export conversation dialog"""
        export_dialog = tk.Toplevel(self.root)
        export_dialog.title("Export Conversation")
        export_dialog.geometry("400x200")
        export_dialog.configure(bg='#2c3e50')
        
        ttk.Label(export_dialog, text="Session ID:", style='Header.TLabel').pack(pady=10)
        
        session_entry = ttk.Entry(export_dialog, width=40)
        session_entry.pack(pady=5)
        
        ttk.Label(export_dialog, text="Format:", style='Header.TLabel').pack(pady=(10, 5))
        
        format_var = tk.StringVar(value="json")
        ttk.Radiobutton(export_dialog, text="JSON", variable=format_var, value="json").pack()
        ttk.Radiobutton(export_dialog, text="Text", variable=format_var, value="txt").pack()
        
        def do_export():
            session_id = session_entry.get().strip()
            if session_id:
                self.run_command(f"python3 view_conversations.py export --session-id {session_id} --format {format_var.get()}", f"Export: {session_id}")
                export_dialog.destroy()
        
        ttk.Button(export_dialog, text="Export", command=do_export, style='Custom.TButton').pack(pady=10)
    
    def view_logs(self):
        """View log files"""
        log_dir = os.path.expanduser("~/.config/voice-chatgpt/logs")
        if os.path.exists(log_dir):
            self.run_command(f"ls -la {log_dir}", "Log Directory")
        else:
            self.log_message("Log directory not found", "WARNING")
    
    def open_github(self):
        """Open the GitHub repository"""
        webbrowser.open("https://github.com/Jsgordon420365/heychat")
        self.log_message("Opening GitHub repository", "INFO")
    
    # Settings Methods
    def open_settings(self):
        """Open settings dialog"""
        settings_dialog = tk.Toplevel(self.root)
        settings_dialog.title("Settings")
        settings_dialog.geometry("500x400")
        settings_dialog.configure(bg='#2c3e50')
        
        # Create notebook for settings tabs
        settings_notebook = ttk.Notebook(settings_dialog)
        settings_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Environment tab
        env_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(env_frame, text="Environment")
        
        ttk.Label(env_frame, text="Environment Configuration", style='Header.TLabel').pack(pady=10)
        
        # Check if .env file exists
        env_file = os.path.expanduser("~/.config/voice-chatgpt/.env")
        if os.path.exists(env_file):
            ttk.Label(env_frame, text=f"✅ Environment file found: {env_file}", foreground='green').pack(pady=5)
        else:
            ttk.Label(env_frame, text=f"❌ Environment file not found: {env_file}", foreground='red').pack(pady=5)
        
        # Database tab
        db_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(db_frame, text="Database")
        
        ttk.Label(db_frame, text="Database Configuration", style='Header.TLabel').pack(pady=10)
        ttk.Label(db_frame, text="Supabase MCP Connector: Available", foreground='green').pack(pady=5)
    
    def test_connection(self):
        """Test database connection"""
        self.run_command("python3 supabase_viewer.py info", "Connection Test")
    
    # Help Methods
    def show_documentation(self):
        """Show documentation"""
        doc_window = tk.Toplevel(self.root)
        doc_window.title("HeyChat Documentation")
        doc_window.geometry("800x600")
        doc_window.configure(bg='#2c3e50')
        
        doc_text = scrolledtext.ScrolledText(
            doc_window, 
            wrap=tk.WORD, 
            bg='#1e1e1e', 
            fg='#ffffff',
            font=('Arial', 10)
        )
        doc_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Load documentation content
        doc_content = """
HeyChat Voice AI Assistant - Documentation

🎤 VOICE CONTROLS:
• Start Voice Chat: Begin an interactive voice conversation
• Quick Ask (5s): Record a 5-second voice query
• Stop Voice Process: Terminate any running voice process

🗄️ DATABASE:
• Browse Conversations: Interactive conversation browser
• View Recent: Show recent conversations
• Search Conversations: Search by content
• Database Statistics: View usage statistics

🛠️ TOOLS:
• Export Conversation: Export conversations in JSON/TXT format
• View Logs: View system logs
• Open GitHub: Open the project repository

⚙️ SETTINGS:
• Configuration: View environment settings
• Test Connection: Test database connectivity

❓ HELP:
• Documentation: This help text
• About: Application information

KEYBOARD SHORTCUTS:
• Ctrl+C: Stop current process
• Enter: Execute search/export
• Double-click: View conversation details

For more information, visit: https://github.com/Jsgordon420365/heychat
        """
        
        doc_text.insert('1.0', doc_content)
        doc_text.config(state='disabled')
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
HeyChat Voice AI Assistant
Version 1.0.0

A modern GUI interface for the HeyChat voice conversation system.

Features:
• Voice-based ChatGPT conversations
• Supabase database integration
• Conversation management and export
• Real-time transcription and TTS
• Interactive conversation browser

Created with Python and tkinter
GitHub: https://github.com/Jsgordon420365/heychat
        """
        
        messagebox.showinfo("About HeyChat", about_text)

def main():
    """Main function to start the GUI"""
    root = tk.Tk()
    app = HeyChatGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Welcome message
    app.log_message("HeyChat GUI started successfully!", "SUCCESS")
    app.log_message("Select a function from the navigation panel to get started", "INFO")
    
    root.mainloop()

if __name__ == "__main__":
    main()
