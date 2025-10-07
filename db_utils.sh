#!/bin/bash
# Database utilities for HeyChat PostgreSQL integration

# Database configuration
DB_NAME="heychat"
DB_USER="${USER}"
DB_HOST="localhost"
DB_PORT="5432"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to execute SQL and return result
execute_sql() {
    local sql="$1"
    psql -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -t -c "$sql" 2>/dev/null | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}

# Function to create a new conversation
create_conversation() {
    local session_id="$1"
    local title="${2:-Voice Conversation}"
    local metadata="${3:-{}}"
    
    local sql="INSERT INTO conversations (session_id, title, metadata) VALUES ('$session_id', '$title', '$metadata') RETURNING id;"
    local conv_id=$(execute_sql "$sql")
    echo "$conv_id"
}

# Function to get conversation ID by session ID
get_conversation_id() {
    local session_id="$1"
    local sql="SELECT id FROM conversations WHERE session_id = '$session_id' AND is_active = TRUE LIMIT 1;"
    execute_sql "$sql"
}

# Function to add a message to a conversation
add_message() {
    local conversation_id="$1"
    local timestamp_str="$2"
    local role="$3"
    local content="$4"
    local audio_file_path="${5:-}"
    local confidence="${6:-}"
    
    # Escape single quotes in content
    content=$(echo "$content" | sed "s/'/''/g")
    
    local sql="INSERT INTO messages (conversation_id, timestamp_str, role, content, audio_file_path, transcription_confidence) VALUES ($conversation_id, '$timestamp_str', '$role', '$content', '$audio_file_path', $confidence) RETURNING id;"
    execute_sql "$sql"
}

# Function to get conversation history for API
get_conversation_history() {
    local conversation_id="$1"
    local sql="SELECT json_agg(json_build_object('role', role, 'content', content)) FROM (SELECT role, content FROM messages WHERE conversation_id = $conversation_id ORDER BY timestamp_str ASC) as msgs;"
    execute_sql "$sql"
}

# Function to list active conversations
list_conversations() {
    local sql="SELECT id, session_id, title, created_at, updated_at FROM conversations WHERE is_active = TRUE ORDER BY updated_at DESC;"
    execute_sql "$sql"
}

# Function to get conversation details
get_conversation_details() {
    local conversation_id="$1"
    local sql="SELECT c.id, c.session_id, c.title, c.created_at, c.updated_at, c.metadata, COUNT(m.id) as message_count FROM conversations c LEFT JOIN messages m ON c.id = m.conversation_id WHERE c.id = $conversation_id GROUP BY c.id, c.session_id, c.title, c.created_at, c.updated_at, c.metadata;"
    execute_sql "$sql"
}

# Function to fuse conversations
fuse_conversations() {
    local source_id="$1"
    local target_id="$2"
    local reason="${3:-Manual fusion}"
    
    local sql="SELECT fuse_conversations($source_id, $target_id, '$reason');"
    execute_sql "$sql"
}

# Function to search conversations
search_conversations() {
    local search_term="$1"
    local sql="SELECT DISTINCT c.id, c.session_id, c.title, c.created_at FROM conversations c JOIN messages m ON c.id = m.conversation_id WHERE c.is_active = TRUE AND (m.content ILIKE '%$search_term%' OR c.title ILIKE '%$search_term%') ORDER BY c.updated_at DESC;"
    execute_sql "$sql"
}

# Function to get recent messages
get_recent_messages() {
    local limit="${1:-10}"
    local sql="SELECT m.timestamp_str, m.role, LEFT(m.content, 100) as content_preview, c.title FROM messages m JOIN conversations c ON m.conversation_id = c.id WHERE c.is_active = TRUE ORDER BY m.timestamp_str DESC LIMIT $limit;"
    execute_sql "$sql"
}

# Function to generate session ID
generate_session_id() {
    local timestamp=$(date +%Y%m%d%H%M%S)
    local random=$(openssl rand -hex 4)
    echo "session_${timestamp}_${random}"
}

# Function to get current conversation ID or create new one
get_or_create_conversation() {
    local session_id="$1"
    local title="${2:-Voice Conversation}"
    local metadata="${3:-{}}"
    
    # Try to get existing conversation
    local conv_id=$(get_conversation_id "$session_id")
    
    if [ -z "$conv_id" ] || [ "$conv_id" = "" ]; then
        # Create new conversation
        conv_id=$(create_conversation "$session_id" "$title" "$metadata")
        echo -e "${GREEN}Created new conversation: $conv_id${NC}" >&2
    else
        echo -e "${BLUE}Using existing conversation: $conv_id${NC}" >&2
    fi
    
    echo "$conv_id"
}

# Function to save conversation to database
save_conversation() {
    local session_id="$1"
    local user_message="$2"
    local assistant_message="$3"
    local audio_file_path="${4:-}"
    local confidence="${5:-}"
    
    # Get or create conversation
    local conv_id=$(get_or_create_conversation "$session_id")
    
    # Generate timestamp
    local timestamp=$(date +%Y%m%d%H%M%S)
    
    # Add user message
    add_message "$conv_id" "$timestamp" "user" "$user_message" "$audio_file_path" "$confidence"
    
    # Add assistant message (with slight delay to ensure different timestamp)
    sleep 1
    local timestamp_assistant=$(date +%Y%m%d%H%M%S)
    add_message "$conv_id" "$timestamp_assistant" "assistant" "$assistant_message"
    
    echo "$conv_id"
}

# Function to load conversation history for API
load_conversation_for_api() {
    local session_id="$1"
    
    # Get conversation ID
    local conv_id=$(get_conversation_id "$session_id")
    
    if [ -z "$conv_id" ] || [ "$conv_id" = "" ]; then
        echo "[]"
        return
    fi
    
    # Get conversation history
    get_conversation_history "$conv_id"
}

# Main function for command line usage
main() {
    case "$1" in
        "create")
            create_conversation "$2" "$3" "$4"
            ;;
        "get-id")
            get_conversation_id "$2"
            ;;
        "add-message")
            add_message "$2" "$3" "$4" "$5" "$6" "$7"
            ;;
        "get-history")
            get_conversation_history "$2"
            ;;
        "list")
            list_conversations
            ;;
        "details")
            get_conversation_details "$2"
            ;;
        "fuse")
            fuse_conversations "$2" "$3" "$4"
            ;;
        "search")
            search_conversations "$2"
            ;;
        "recent")
            get_recent_messages "$2"
            ;;
        "session-id")
            generate_session_id
            ;;
        "save")
            save_conversation "$2" "$3" "$4" "$5" "$6"
            ;;
        "load")
            load_conversation_for_api "$2"
            ;;
        "test")
            echo -e "${BLUE}Testing database connection...${NC}"
            local result=$(execute_sql "SELECT 1;")
            if [ "$result" = "1" ]; then
                echo -e "${GREEN}Database connection successful!${NC}"
            else
                echo -e "${RED}Database connection failed!${NC}"
            fi
            ;;
        *)
            echo -e "${BLUE}HeyChat Database Utilities${NC}"
            echo "Usage: $0 <command> [args...]"
            echo ""
            echo "Commands:"
            echo "  create <session_id> [title] [metadata]  - Create new conversation"
            echo "  get-id <session_id>                     - Get conversation ID"
            echo "  add-message <conv_id> <timestamp> <role> <content> [audio_path] [confidence]"
            echo "  get-history <conv_id>                   - Get conversation history"
            echo "  list                                    - List active conversations"
            echo "  details <conv_id>                       - Get conversation details"
            echo "  fuse <source_id> <target_id> [reason]   - Fuse conversations"
            echo "  search <term>                           - Search conversations"
            echo "  recent [limit]                          - Get recent messages"
            echo "  session-id                              - Generate session ID"
            echo "  save <session_id> <user_msg> <assistant_msg> [audio_path] [confidence]"
            echo "  load <session_id>                       - Load conversation for API"
            echo "  test                                    - Test database connection"
            ;;
    esac
}

# Run main function if script is executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
