#!/usr/bin/env python3
"""
Database Migration Script for Enhanced Context Tracking
Adds new fields and tables for decision tree context management
"""

import os
import sys
from sqlalchemy import text, create_engine
from sqlalchemy.exc import OperationalError

def get_database_url():
    """Get database URL from environment or use SQLite as default"""
    from config import Config
    return Config.get_database_url()

def migrate_database():
    """Migrate database to add new context tracking fields"""
    db_url = get_database_url()
    engine = create_engine(db_url)
    
    print(f"🔄 Starting database migration for: {db_url}")
    
    try:
        with engine.connect() as conn:
            # Check if we're using PostgreSQL
            if 'postgresql' in db_url:
                print("📊 Detected PostgreSQL database")
                schema = 'mcp_tracker'
                
                # Check if schema exists
                result = conn.execute(text(f"SELECT schema_name FROM information_schema.schemata WHERE schema_name = '{schema}'"))
                if not result.fetchone():
                    print(f"🔧 Creating schema: {schema}")
                    conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
                    conn.commit()
                
                # Add new columns to agent_interactions table
                print("🔧 Adding new columns to agent_interactions table...")
                
                new_columns = [
                    ('full_content', 'TEXT'),
                    ('context_summary', 'TEXT'),
                    ('semantic_keywords', 'JSONB'),
                    ('topic_category', 'VARCHAR(100)'),
                    ('context_relevance_score', 'FLOAT'),
                    ('conversation_context', 'JSONB')
                ]
                
                for column_name, column_type in new_columns:
                    try:
                        conn.execute(text(f"ALTER TABLE {schema}.agent_interactions ADD COLUMN IF NOT EXISTS {column_name} {column_type}"))
                        print(f"  ✅ Added column: {column_name}")
                    except Exception as e:
                        print(f"  ⚠️ Column {column_name} already exists or error: {e}")
                
                # Create conversation_contexts table
                print("🔧 Creating conversation_contexts table...")
                create_context_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.conversation_contexts (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    user_id VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_summary TEXT NOT NULL,
                    semantic_context JSONB,
                    key_topics JSONB,
                    user_preferences JSONB,
                    project_context JSONB,
                    context_type VARCHAR(50) DEFAULT 'conversation',
                    relevance_score FLOAT DEFAULT 1.0,
                    usage_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    related_interactions JSONB,
                    parent_context_id INTEGER
                );
                """
                
                try:
                    conn.execute(text(create_context_table_sql))
                    print("  ✅ Created conversation_contexts table")
                except Exception as e:
                    print(f"  ⚠️ Table already exists or error: {e}")
                
                # Add indexes for better performance
                print("🔧 Adding indexes...")
                indexes = [
                    f"CREATE INDEX IF NOT EXISTS idx_{schema}_agent_interactions_session_id ON {schema}.agent_interactions(session_id)",
                    f"CREATE INDEX IF NOT EXISTS idx_{schema}_agent_interactions_topic_category ON {schema}.agent_interactions(topic_category)",
                    f"CREATE INDEX IF NOT EXISTS idx_{schema}_conversation_contexts_session_id ON {schema}.conversation_contexts(session_id)",
                    f"CREATE INDEX IF NOT EXISTS idx_{schema}_conversation_contexts_context_type ON {schema}.conversation_contexts(context_type)"
                ]
                
                for index_sql in indexes:
                    try:
                        conn.execute(text(index_sql))
                        print("  ✅ Added index")
                    except Exception as e:
                        print(f"  ⚠️ Index already exists or error: {e}")
                
                # Update sessions table
                print("🔧 Updating sessions table...")
                session_updates = [
                    ('current_context_id', 'INTEGER'),
                    ('context_history', 'JSONB'),
                    ('session_summary', 'TEXT')
                ]
                
                for column_name, column_type in session_updates:
                    try:
                        conn.execute(text(f"ALTER TABLE {schema}.sessions ADD COLUMN IF NOT EXISTS {column_name} {column_type}"))
                        print(f"  ✅ Added column: {column_name}")
                    except Exception as e:
                        print(f"  ⚠️ Column {column_name} already exists or error: {e}")
                
            else:
                print("📊 Detected SQLite database")
                
                # Add new columns to agent_interactions table
                print("🔧 Adding new columns to agent_interactions table...")
                
                new_columns = [
                    ('full_content', 'TEXT'),
                    ('context_summary', 'TEXT'),
                    ('semantic_keywords', 'TEXT'),  # JSON stored as TEXT in SQLite
                    ('topic_category', 'TEXT'),
                    ('context_relevance_score', 'REAL'),
                    ('conversation_context', 'TEXT')  # JSON stored as TEXT in SQLite
                ]
                
                for column_name, column_type in new_columns:
                    try:
                        conn.execute(text(f"ALTER TABLE agent_interactions ADD COLUMN {column_name} {column_type}"))
                        print(f"  ✅ Added column: {column_name}")
                    except Exception as e:
                        print(f"  ⚠️ Column {column_name} already exists or error: {e}")
                
                # Create conversation_contexts table
                print("🔧 Creating conversation_contexts table...")
                create_context_table_sql = """
                CREATE TABLE IF NOT EXISTS conversation_contexts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    context_summary TEXT NOT NULL,
                    semantic_context TEXT,
                    key_topics TEXT,
                    user_preferences TEXT,
                    project_context TEXT,
                    context_type TEXT DEFAULT 'conversation',
                    relevance_score REAL DEFAULT 1.0,
                    usage_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    related_interactions TEXT,
                    parent_context_id INTEGER
                );
                """
                
                try:
                    conn.execute(text(create_context_table_sql))
                    print("  ✅ Created conversation_contexts table")
                except Exception as e:
                    print(f"  ⚠️ Table already exists or error: {e}")
                
                # Add indexes for better performance
                print("🔧 Adding indexes...")
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_agent_interactions_session_id ON agent_interactions(session_id)",
                    "CREATE INDEX IF NOT EXISTS idx_agent_interactions_topic_category ON agent_interactions(topic_category)",
                    "CREATE INDEX IF NOT EXISTS idx_conversation_contexts_session_id ON conversation_contexts(session_id)",
                    "CREATE INDEX IF NOT EXISTS idx_conversation_contexts_context_type ON conversation_contexts(context_type)"
                ]
                
                for index_sql in indexes:
                    try:
                        conn.execute(text(index_sql))
                        print("  ✅ Added index")
                    except Exception as e:
                        print(f"  ⚠️ Index already exists or error: {e}")
                
                # Update sessions table
                print("🔧 Updating sessions table...")
                session_updates = [
                    ('current_context_id', 'INTEGER'),
                    ('context_history', 'TEXT'),  # JSON stored as TEXT in SQLite
                    ('session_summary', 'TEXT')
                ]
                
                for column_name, column_type in session_updates:
                    try:
                        conn.execute(text(f"ALTER TABLE sessions ADD COLUMN {column_name} {column_type}"))
                        print(f"  ✅ Added column: {column_name}")
                    except Exception as e:
                        print(f"  ⚠️ Column {column_name} already exists or error: {e}")
            
            conn.commit()
            print("✅ Database migration completed successfully!")
            
    except Exception as e:
        print(f"❌ Database migration failed: {e}")
        return False
    
    return True

def test_migration():
    """Test the migration by checking if new columns exist"""
    db_url = get_database_url()
    engine = create_engine(db_url)
    
    try:
        with engine.connect() as conn:
            if 'postgresql' in db_url:
                schema = 'mcp_tracker'
                result = conn.execute(text(f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_schema = '{schema}' 
                    AND table_name = 'agent_interactions'
                    AND column_name IN ('full_content', 'context_summary', 'semantic_keywords')
                """))
            else:
                result = conn.execute(text("""
                    PRAGMA table_info(agent_interactions)
                """))
                # For SQLite, we need to check differently
                columns = [row[1] for row in result.fetchall()]
                result = [(col, 'TEXT') for col in columns if col in ['full_content', 'context_summary', 'semantic_keywords']]
            
            new_columns = [row[0] for row in result]
            print(f"🔍 Found new columns: {new_columns}")
            
            if len(new_columns) >= 3:
                print("✅ Migration test passed - new columns are present")
                return True
            else:
                print("❌ Migration test failed - missing expected columns")
                return False
                
    except Exception as e:
        print(f"❌ Migration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database migration for enhanced context tracking...")
    
    # Run migration
    if migrate_database():
        print("\n🧪 Testing migration...")
        if test_migration():
            print("\n🎉 Database migration completed and verified successfully!")
            print("\nNew features available:")
            print("  • Full content retention for interactions")
            print("  • Decision tree-based context analysis")
            print("  • Enhanced user preference inference")
            print("  • Project context extraction")
            print("  • Semantic keyword analysis")
            print("  • Context injection for Cursor agent")
        else:
            print("\n⚠️ Migration completed but verification failed")
    else:
        print("\n❌ Database migration failed")
        sys.exit(1)
