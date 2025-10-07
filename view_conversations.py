#!/usr/bin/env python3
"""
HeyChat Conversation Viewer
View and browse conversation data from Supabase
"""

import json
import sys
import os
from datetime import datetime
import argparse

class ConversationViewer:
    def __init__(self):
        self.db_name = "heychat"
        
    def format_timestamp(self, timestamp_str):
        """Format timestamp string to readable format"""
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp_str
    
    def format_duration(self, start_time, end_time):
        """Calculate and format conversation duration"""
        try:
            start = datetime.strptime(start_time, "%Y%m%d%H%M%S")
            end = datetime.strptime(end_time, "%Y%m%d%H%M%S")
            duration = end - start
            return str(duration).split('.')[0]  # Remove microseconds
        except:
            return "Unknown"
    
    def list_conversations(self, limit=10, active_only=True):
        """List recent conversations"""
        print("🗣️  HeyChat Conversations")
        print("=" * 50)
        
        # In a real implementation, this would query Supabase
        # For now, show placeholder data
        conversations = [
            {
                "id": "conv_001",
                "session_id": "session_20251007120000_abc123",
                "title": "Voice Conversation",
                "created_at": "2025-01-15 12:00:00",
                "message_count": 8,
                "duration": "00:05:23"
            },
            {
                "id": "conv_002", 
                "session_id": "session_20251007130000_def456",
                "title": "Voice Conversation",
                "created_at": "2025-01-15 13:00:00",
                "message_count": 12,
                "duration": "00:08:45"
            }
        ]
        
        for i, conv in enumerate(conversations, 1):
            print(f"{i:2d}. {conv['session_id']}")
            print(f"    📅 {conv['created_at']}")
            print(f"    💬 {conv['message_count']} messages")
            print(f"    ⏱️  {conv['duration']}")
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
            }
        ]
        
        for msg in messages:
            timestamp = self.format_timestamp(msg['timestamp_str'])
            role_icon = "👤" if msg['role'] == 'user' else "🤖"
            role_name = "You" if msg['role'] == 'user' else "ChatGPT"
            
            print(f"{role_icon} {role_name} ({timestamp})")
            print(f"   {msg['content']}")
            print()
    
    def search_conversations(self, search_term):
        """Search conversations by content"""
        print(f"🔍 Search Results for: '{search_term}'")
        print("=" * 50)
        
        # In a real implementation, this would query Supabase
        # For now, show placeholder results
        results = [
            {
                "session_id": "session_20251007120000_abc123",
                "timestamp": "2025-01-15 12:00:00",
                "preview": "Hello, how are you today? I'm doing well, thank you for asking!"
            }
        ]
        
        for result in results:
            print(f"📅 {result['timestamp']}")
            print(f"🆔 {result['session_id']}")
            print(f"💬 {result['preview']}")
            print()
    
    def show_stats(self):
        """Show conversation statistics"""
        print("📊 HeyChat Statistics")
        print("=" * 30)
        
        # In a real implementation, this would query Supabase
        stats = {
            "total_conversations": 15,
            "total_messages": 127,
            "total_duration": "02:15:30",
            "avg_messages_per_conversation": 8.5,
            "most_active_day": "2025-01-15",
            "longest_conversation": "00:12:45"
        }
        
        print(f"📈 Total Conversations: {stats['total_conversations']}")
        print(f"💬 Total Messages: {stats['total_messages']}")
        print(f"⏱️  Total Duration: {stats['total_duration']}")
        print(f"📊 Avg Messages/Conversation: {stats['avg_messages_per_conversation']}")
        print(f"📅 Most Active Day: {stats['most_active_day']}")
        print(f"🏆 Longest Conversation: {stats['longest_conversation']}")
        print()
    
    def export_conversation(self, session_id, format='json'):
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
        
        filename = f"conversation_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
        elif format == 'txt':
            with open(filename, 'w') as f:
                f.write(f"Conversation: {session_id}\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                for msg in export_data['messages']:
                    f.write(f"[{msg['timestamp']}] {msg['role'].upper()}: {msg['content']}\n\n")
        
        print(f"✅ Exported to: {filename}")

def main():
    parser = argparse.ArgumentParser(description='HeyChat Conversation Viewer')
    parser.add_argument('command', nargs='?', default='list', 
                       choices=['list', 'show', 'search', 'stats', 'export'],
                       help='Command to execute')
    parser.add_argument('--session-id', help='Session ID for show/export commands')
    parser.add_argument('--search', help='Search term for search command')
    parser.add_argument('--limit', type=int, default=10, help='Limit for list command')
    parser.add_argument('--format', choices=['json', 'txt'], default='json', 
                       help='Export format')
    parser.add_argument('--active-only', action='store_true', default=True,
                       help='Show only active conversations')
    
    args = parser.parse_args()
    
    viewer = ConversationViewer()
    
    if args.command == 'list':
        viewer.list_conversations(limit=args.limit, active_only=args.active_only)
    elif args.command == 'show':
        if not args.session_id:
            print("❌ Error: --session-id required for show command")
            sys.exit(1)
        viewer.show_conversation(args.session_id)
    elif args.command == 'search':
        if not args.search:
            print("❌ Error: --search required for search command")
            sys.exit(1)
        viewer.search_conversations(args.search)
    elif args.command == 'stats':
        viewer.show_stats()
    elif args.command == 'export':
        if not args.session_id:
            print("❌ Error: --session-id required for export command")
            sys.exit(1)
        viewer.export_conversation(args.session_id, args.format)

if __name__ == "__main__":
    main()
