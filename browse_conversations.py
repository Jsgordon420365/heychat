#!/usr/bin/env python3
"""
HeyChat Interactive Conversation Browser
Interactive terminal interface for browsing conversations
"""

import json
import sys
import os
from datetime import datetime
import readline

class InteractiveBrowser:
    def __init__(self):
        self.db_name = "heychat"
        self.current_page = 0
        self.page_size = 5
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Print the application header"""
        print("🗣️  HeyChat Conversation Browser")
        print("=" * 50)
        print("Type 'help' for commands, 'quit' to exit")
        print()
    
    def format_timestamp(self, timestamp_str):
        """Format timestamp string to readable format"""
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp_str
    
    def show_help(self):
        """Show available commands"""
        print("📖 Available Commands:")
        print("  list [n]           - List conversations (n = number to show)")
        print("  show <session_id>  - Show detailed conversation")
        print("  search <term>      - Search conversations")
        print("  stats              - Show statistics")
        print("  export <session_id> - Export conversation")
        print("  next               - Next page of conversations")
        print("  prev               - Previous page of conversations")
        print("  clear              - Clear screen")
        print("  help               - Show this help")
        print("  quit/exit          - Exit browser")
        print()
    
    def list_conversations(self, limit=None):
        """List conversations with pagination"""
        if limit:
            self.page_size = int(limit)
        
        print(f"📋 Conversations (Page {self.current_page + 1})")
        print("-" * 50)
        
        # In a real implementation, this would query Supabase with pagination
        # For now, show placeholder data
        conversations = [
            {
                "id": "conv_001",
                "session_id": "session_20251007120000_abc123",
                "title": "Voice Conversation",
                "created_at": "2025-01-15 12:00:00",
                "message_count": 8,
                "duration": "00:05:23",
                "last_message": "Can you help me with a coding problem?"
            },
            {
                "id": "conv_002", 
                "session_id": "session_20251007130000_def456",
                "title": "Voice Conversation",
                "created_at": "2025-01-15 13:00:00",
                "message_count": 12,
                "duration": "00:08:45",
                "last_message": "Thank you for your help!"
            },
            {
                "id": "conv_003",
                "session_id": "session_20251007140000_ghi789",
                "title": "Voice Conversation", 
                "created_at": "2025-01-15 14:00:00",
                "message_count": 6,
                "duration": "00:03:12",
                "last_message": "What's the weather like today?"
            },
            {
                "id": "conv_004",
                "session_id": "session_20251007150000_jkl012",
                "title": "Voice Conversation",
                "created_at": "2025-01-15 15:00:00", 
                "message_count": 15,
                "duration": "00:12:30",
                "last_message": "Can you explain machine learning?"
            },
            {
                "id": "conv_005",
                "session_id": "session_20251007160000_mno345",
                "title": "Voice Conversation",
                "created_at": "2025-01-15 16:00:00",
                "message_count": 4,
                "duration": "00:02:15",
                "last_message": "Goodbye!"
            }
        ]
        
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        page_conversations = conversations[start_idx:end_idx]
        
        if not page_conversations:
            print("No more conversations to show.")
            return
        
        for i, conv in enumerate(page_conversations, start_idx + 1):
            print(f"{i:2d}. {conv['session_id']}")
            print(f"    📅 {conv['created_at']}")
            print(f"    💬 {conv['message_count']} messages | ⏱️  {conv['duration']}")
            print(f"    💭 {conv['last_message'][:60]}{'...' if len(conv['last_message']) > 60 else ''}")
            print()
        
        print(f"Showing {len(page_conversations)} of {len(conversations)} conversations")
        print("Use 'next' or 'prev' to navigate pages")
        print()
    
    def show_conversation(self, session_id):
        """Show detailed conversation"""
        print(f"🗣️  Conversation: {session_id}")
        print("=" * 60)
        
        # In a real implementation, this would query Supabase
        # For now, show placeholder conversation
        messages = [
            {
                "timestamp_str": "20251007120000",
                "role": "user",
                "content": "Hello, how are you today?"
            },
            {
                "timestamp_str": "20251007120005",
                "role": "assistant", 
                "content": "I'm doing well, thank you for asking! How can I help you today?"
            },
            {
                "timestamp_str": "20251007120015",
                "role": "user",
                "content": "Can you help me with a coding problem?"
            },
            {
                "timestamp_str": "20251007120020",
                "role": "assistant",
                "content": "Of course! I'd be happy to help you with a coding problem. What programming language are you working with and what specific issue are you facing?"
            },
            {
                "timestamp_str": "20251007120030",
                "role": "user",
                "content": "I'm working with Python and I'm having trouble with list comprehensions."
            },
            {
                "timestamp_str": "20251007120035",
                "role": "assistant",
                "content": "List comprehensions are a powerful feature in Python! They provide a concise way to create lists. The basic syntax is: [expression for item in iterable if condition]. Would you like me to show you some examples?"
            }
        ]
        
        for msg in messages:
            timestamp = self.format_timestamp(msg['timestamp_str'])
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            role_name = "You" if msg['role'] == 'user' else "ChatGPT"
            
            print(f"{role_icon} {role_name} ({timestamp})")
            print(f"   {msg['content']}")
            print()
        
        print("Press Enter to continue...")
        input()
    
    def search_conversations(self, search_term):
        """Search conversations by content"""
        print(f"🔍 Search Results for: '{search_term}'")
        print("-" * 50)
        
        # In a real implementation, this would query Supabase
        # For now, show placeholder results
        results = [
            {
                "session_id": "session_20251007120000_abc123",
                "timestamp": "2025-01-15 12:00:00",
                "preview": "Hello, how are you today? I'm doing well, thank you for asking!",
                "match_count": 2
            },
            {
                "session_id": "session_20251007130000_def456", 
                "timestamp": "2025-01-15 13:00:00",
                "preview": "Can you help me with a coding problem? Of course! I'd be happy to help...",
                "match_count": 1
            }
        ]
        
        for result in results:
            print(f"📅 {result['timestamp']}")
            print(f"🆔 {result['session_id']}")
            print(f"💬 {result['preview']}")
            print(f"🎯 {result['match_count']} matches")
            print()
        
        print("Press Enter to continue...")
        input()
    
    def show_stats(self):
        """Show conversation statistics"""
        print("📊 HeyChat Statistics")
        print("-" * 30)
        
        # In a real implementation, this would query Supabase
        stats = {
            "total_conversations": 15,
            "total_messages": 127,
            "total_duration": "02:15:30",
            "avg_messages_per_conversation": 8.5,
            "most_active_day": "2025-01-15",
            "longest_conversation": "00:12:45",
            "most_common_words": ["help", "python", "code", "problem", "thank"]
        }
        
        print(f"📈 Total Conversations: {stats['total_conversations']}")
        print(f"💬 Total Messages: {stats['total_messages']}")
        print(f"⏱️  Total Duration: {stats['total_duration']}")
        print(f"📊 Avg Messages/Conversation: {stats['avg_messages_per_conversation']}")
        print(f"📅 Most Active Day: {stats['most_active_day']}")
        print(f"🏆 Longest Conversation: {stats['longest_conversation']}")
        print(f"🔤 Most Common Words: {', '.join(stats['most_common_words'])}")
        print()
        
        print("Press Enter to continue...")
        input()
    
    def export_conversation(self, session_id):
        """Export conversation to file"""
        print(f"📤 Exporting conversation: {session_id}")
        
        # In a real implementation, this would query Supabase and export
        export_data = {
            "session_id": session_id,
            "exported_at": datetime.now().isoformat(),
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
        
        filename = f"conversation_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Exported to: {filename}")
        print("Press Enter to continue...")
        input()
    
    def next_page(self):
        """Go to next page"""
        self.current_page += 1
        self.list_conversations()
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.list_conversations()
        else:
            print("Already on first page.")
            print()
    
    def run(self):
        """Main interactive loop"""
        self.clear_screen()
        self.print_header()
        self.show_help()
        
        while True:
            try:
                command = input("🗣️  > ").strip().lower()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0]
                
                if cmd in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'clear':
                    self.clear_screen()
                    self.print_header()
                elif cmd == 'list':
                    limit = parts[1] if len(parts) > 1 else None
                    self.list_conversations(limit)
                elif cmd == 'show':
                    if len(parts) < 2:
                        print("❌ Usage: show <session_id>")
                        continue
                    session_id = parts[1]
                    self.show_conversation(session_id)
                elif cmd == 'search':
                    if len(parts) < 2:
                        print("❌ Usage: search <term>")
                        continue
                    search_term = ' '.join(parts[1:])
                    self.search_conversations(search_term)
                elif cmd == 'stats':
                    self.show_stats()
                elif cmd == 'export':
                    if len(parts) < 2:
                        print("❌ Usage: export <session_id>")
                        continue
                    session_id = parts[1]
                    self.export_conversation(session_id)
                elif cmd == 'next':
                    self.next_page()
                elif cmd == 'prev':
                    self.prev_page()
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("Type 'help' for available commands.")
                    print()
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

def main():
    browser = InteractiveBrowser()
    browser.run()

if __name__ == "__main__":
    main()
