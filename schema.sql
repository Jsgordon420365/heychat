-- HeyChat Database Schema
-- Supports distinct conversations that can be fused together

-- Create the database (run this separately)
-- CREATE DATABASE heychat;

-- Connect to heychat database and create tables

-- Conversations table - represents distinct conversation sessions
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(50) UNIQUE NOT NULL,  -- Unique identifier for each session
    title VARCHAR(255),                      -- Optional conversation title
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,          -- Whether conversation is still active
    metadata JSONB                           -- Additional metadata (TTS settings, etc.)
);

-- Messages table - stores individual messages within conversations
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    timestamp_str VARCHAR(14) NOT NULL,      -- yyyymmddhhmmss format as requested
    role VARCHAR(20) NOT NULL,               -- 'user' or 'assistant'
    content TEXT NOT NULL,                   -- The actual message content
    audio_file_path VARCHAR(500),            -- Path to audio file if available
    transcription_confidence DECIMAL(3,2),   -- Confidence score from Whisper
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB                           -- Additional message metadata
);

-- Conversation fusions table - tracks when conversations are merged
CREATE TABLE IF NOT EXISTS conversation_fusions (
    id SERIAL PRIMARY KEY,
    source_conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    target_conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    fused_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fusion_reason TEXT,                      -- Why the conversations were fused
    metadata JSONB
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_conversations_active ON conversations(is_active);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp_str ON messages(timestamp_str);
CREATE INDEX IF NOT EXISTS idx_messages_role ON messages(role);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

CREATE INDEX IF NOT EXISTS idx_fusions_source ON conversation_fusions(source_conversation_id);
CREATE INDEX IF NOT EXISTS idx_fusions_target ON conversation_fusions(target_conversation_id);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_conversations_updated_at 
    BEFORE UPDATE ON conversations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to generate session ID
CREATE OR REPLACE FUNCTION generate_session_id()
RETURNS VARCHAR(50) AS $$
BEGIN
    RETURN 'session_' || to_char(CURRENT_TIMESTAMP, 'YYYYMMDDHH24MISS') || '_' || 
           substring(md5(random()::text) from 1 for 8);
END;
$$ LANGUAGE plpgsql;

-- Function to fuse conversations
CREATE OR REPLACE FUNCTION fuse_conversations(
    source_id INTEGER,
    target_id INTEGER,
    reason TEXT DEFAULT 'Manual fusion'
)
RETURNS BOOLEAN AS $$
BEGIN
    -- Update all messages from source conversation to target conversation
    UPDATE messages 
    SET conversation_id = target_id 
    WHERE conversation_id = source_id;
    
    -- Record the fusion
    INSERT INTO conversation_fusions (source_conversation_id, target_conversation_id, fusion_reason)
    VALUES (source_id, target_id, reason);
    
    -- Mark source conversation as inactive
    UPDATE conversations 
    SET is_active = FALSE 
    WHERE id = source_id;
    
    -- Update target conversation timestamp
    UPDATE conversations 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = target_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Function to get conversation history for API
CREATE OR REPLACE FUNCTION get_conversation_messages(conv_id INTEGER)
RETURNS TABLE(
    role VARCHAR(20),
    content TEXT,
    timestamp_str VARCHAR(14)
) AS $$
BEGIN
    RETURN QUERY
    SELECT m.role, m.content, m.timestamp_str
    FROM messages m
    WHERE m.conversation_id = conv_id
    ORDER BY m.timestamp_str ASC;
END;
$$ LANGUAGE plpgsql;

-- Sample data for testing
INSERT INTO conversations (session_id, title, metadata) VALUES 
    (generate_session_id(), 'Test Conversation 1', '{"tts_enabled": true, "model": "gpt-4"}'),
    (generate_session_id(), 'Test Conversation 2', '{"tts_enabled": false, "model": "gpt-3.5-turbo"}')
ON CONFLICT (session_id) DO NOTHING;

-- Get the conversation IDs for sample messages
DO $$
DECLARE
    conv1_id INTEGER;
    conv2_id INTEGER;
BEGIN
    SELECT id INTO conv1_id FROM conversations WHERE title = 'Test Conversation 1' LIMIT 1;
    SELECT id INTO conv2_id FROM conversations WHERE title = 'Test Conversation 2' LIMIT 1;
    
    -- Insert sample messages
    INSERT INTO messages (conversation_id, timestamp_str, role, content) VALUES
        (conv1_id, to_char(CURRENT_TIMESTAMP - INTERVAL '10 minutes', 'YYYYMMDDHH24MISS'), 'user', 'Hello, how are you?'),
        (conv1_id, to_char(CURRENT_TIMESTAMP - INTERVAL '9 minutes', 'YYYYMMDDHH24MISS'), 'assistant', 'I am doing well, thank you for asking! How can I help you today?'),
        (conv2_id, to_char(CURRENT_TIMESTAMP - INTERVAL '5 minutes', 'YYYYMMDDHH24MISS'), 'user', 'What is the weather like?'),
        (conv2_id, to_char(CURRENT_TIMESTAMP - INTERVAL '4 minutes', 'YYYYMMDDHH24MISS'), 'assistant', 'I do not have access to real-time weather data, but you can check your local weather app or website for current conditions.');
END $$;
