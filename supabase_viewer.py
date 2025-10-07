#!/usr/bin/env python3
"""
HeyChat Supabase Database Viewer
Uses the Supabase MCP connector to view real conversation data
"""

import json
import sys
import os
from datetime import datetime
import argparse

class SupabaseViewer:
    def __init__(self):
        self.db_name = "heychat"
        
    def format_timestamp(self, timestamp_str):
        """Format timestamp string to readable format"""
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp_str
    
    def list_conversations(self, limit=10):
        """List conversations from Supabase"""
        print("🗣️  HeyChat Conversations (from Supabase)")
        print("=" * 50)
        
        # This would use the Supabase MCP connector in a real implementation
        # For now, we'll show how it would work
        print("📡 Querying Supabase database...")
        print("")
        
        # Example of what the query would look like:
        sql_query = """
        SELECT 
            c.id,
            c.session_id,
            c.title,
            c.created_at,
            c.updated_at,
            c.is_active,
            COUNT(m.id) as message_count
        FROM conversations c
        LEFT JOIN messages m ON c.id = m.conversation_id
        WHERE c.is_active = TRUE
        GROUP BY c.id, c.session_id, c.title, c.created_at, c.updated_at, c.is_active
        ORDER BY c.updated_at DESC
        LIMIT %s;
        """ % limit
        
        print(f"SQL Query: {sql_query}")
        print("")
        print("📊 Results would be displayed here...")
        print("")
        print("Note: This is a demonstration. In production, this would")
        print("use the Supabase MCP connector to execute the query.")
    
    def show_conversation(self, session_id):
        """Show detailed conversation from Supabase"""
        print(f"🗣️  Conversation: {session_id}")
        print("=" * 60)
        
        # Example SQL query for conversation details
        sql_query = f"""
        SELECT 
            m.timestamp_str,
            m.role,
            m.content,
            m.audio_file_path,
            m.transcription_confidence,
            m.created_at
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.id
        WHERE c.session_id = '{session_id}'
        ORDER BY m.timestamp_str ASC;
        """
        
        print(f"SQL Query: {sql_query}")
        print("")
        print("📊 Conversation messages would be displayed here...")
        print("")
        print("Note: This is a demonstration. In production, this would")
        print("use the Supabase MCP connector to execute the query.")
    
    def search_conversations(self, search_term):
        """Search conversations in Supabase"""
        print(f"🔍 Search Results for: '{search_term}'")
        print("=" * 50)
        
        # Example SQL query for search
        sql_query = f"""
        SELECT DISTINCT
            c.id,
            c.session_id,
            c.title,
            c.created_at,
            m.content as preview
        FROM conversations c
        JOIN messages m ON c.id = m.conversation_id
        WHERE c.is_active = TRUE
        AND (m.content ILIKE '%{search_term}%' OR c.title ILIKE '%{search_term}%')
        ORDER BY c.updated_at DESC;
        """
        
        print(f"SQL Query: {sql_query}")
        print("")
        print("📊 Search results would be displayed here...")
        print("")
        print("Note: This is a demonstration. In production, this would")
        print("use the Supabase MCP connector to execute the query.")
    
    def show_stats(self):
        """Show conversation statistics from Supabase"""
        print("📊 HeyChat Statistics (from Supabase)")
        print("=" * 40)
        
        # Example SQL queries for statistics
        queries = {
            "Total Conversations": "SELECT COUNT(*) FROM conversations WHERE is_active = TRUE;",
            "Total Messages": "SELECT COUNT(*) FROM messages;",
            "Average Messages per Conversation": """
                SELECT AVG(message_count) FROM (
                    SELECT COUNT(*) as message_count 
                    FROM messages m 
                    JOIN conversations c ON m.conversation_id = c.id 
                    WHERE c.is_active = TRUE 
                    GROUP BY c.id
                ) as counts;
            """,
            "Most Active Day": """
                SELECT DATE(created_at) as day, COUNT(*) as conversations
                FROM conversations 
                WHERE is_active = TRUE
                GROUP BY DATE(created_at)
                ORDER BY conversations DESC
                LIMIT 1;
            """
        }
        
        for stat_name, query in queries.items():
            print(f"📈 {stat_name}:")
            print(f"   SQL: {query.strip()}")
            print("")
        
        print("📊 Statistics would be calculated and displayed here...")
        print("")
        print("Note: This is a demonstration. In production, this would")
        print("use the Supabase MCP connector to execute these queries.")
    
    def export_conversation(self, session_id, format='json'):
        """Export conversation from Supabase"""
        print(f"📤 Exporting conversation: {session_id}")
        
        # Example SQL query for export
        sql_query = f"""
        SELECT 
            c.session_id,
            c.title,
            c.created_at,
            c.metadata,
            json_agg(
                json_build_object(
                    'timestamp', m.timestamp_str,
                    'role', m.role,
                    'content', m.content,
                    'audio_file_path', m.audio_file_path,
                    'confidence', m.transcription_confidence
                ) ORDER BY m.timestamp_str
            ) as messages
        FROM conversations c
        LEFT JOIN messages m ON c.id = m.conversation_id
        WHERE c.session_id = '{session_id}'
        GROUP BY c.id, c.session_id, c.title, c.created_at, c.metadata;
        """
        
        print(f"SQL Query: {sql_query}")
        print("")
        print("📊 Export data would be generated here...")
        print("")
        print("Note: This is a demonstration. In production, this would")
        print("use the Supabase MCP connector to execute the query and")
        print("generate the export file.")
    
    def show_database_info(self):
        """Show database connection and table information"""
        print("🗄️  Supabase Database Information")
        print("=" * 40)
        
        print("📡 Connection Details:")
        print("   Database: heychat")
        print("   Provider: Supabase (PostgreSQL)")
        print("   MCP Connector: Available")
        print("")
        
        print("📋 Available Tables:")
        tables = [
            ("conversations", "Stores conversation sessions"),
            ("messages", "Stores individual messages"),
            ("conversation_fusions", "Tracks conversation merges")
        ]
        
        for table_name, description in tables:
            print(f"   📄 {table_name}: {description}")
        
        print("")
        print("🔧 Available Functions:")
        functions = [
            ("generate_session_id()", "Generates unique session IDs"),
            ("fuse_conversations()", "Merges two conversations"),
            ("get_conversation_history_json()", "Gets conversation as JSON")
        ]
        
        for func_name, description in functions:
            print(f"   ⚙️  {func_name}: {description}")
        
        print("")

def main():
    parser = argparse.ArgumentParser(description='HeyChat Supabase Database Viewer')
    parser.add_argument('command', nargs='?', default='info', 
                       choices=['list', 'show', 'search', 'stats', 'export', 'info'],
                       help='Command to execute')
    parser.add_argument('--session-id', help='Session ID for show/export commands')
    parser.add_argument('--search', help='Search term for search command')
    parser.add_argument('--limit', type=int, default=10, help='Limit for list command')
    parser.add_argument('--format', choices=['json', 'txt'], default='json', 
                       help='Export format')
    
    args = parser.parse_args()
    
    viewer = SupabaseViewer()
    
    if args.command == 'list':
        viewer.list_conversations(limit=args.limit)
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
    elif args.command == 'info':
        viewer.show_database_info()

if __name__ == "__main__":
    main()
