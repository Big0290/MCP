#!/usr/bin/env python3
"""
Database initialization script for the MCP Agent Tracker
Run this script to create the database tables and initial setup
"""

import os
import sys
from models_unified import init_database, get_session_factory, Session, AgentInteraction

def main():
    """Initialize the database and create tables"""
    print("Initializing MCP Agent Tracker database...")
    
    try:
        # Initialize database and create tables
        engine = init_database()
        print(f"✓ Database initialized successfully")
        print(f"✓ Database URL: {engine.url}")
        
        # Test database connection
        with get_session_factory()() as db_session:
            # Test query
            session_count = db_session.query(Session).count()
            interaction_count = db_session.query(AgentInteraction).count()
            
            print(f"✓ Database connection test successful")
            print(f"✓ Current sessions: {session_count}")
            print(f"✓ Current interactions: {interaction_count}")
        
        print("\n🎉 Database setup completed successfully!")
        print("\nThe following tables have been created:")
        print("  - sessions: Tracks user sessions")
        print("  - agent_interactions: Tracks all agent interactions and tool calls")
        
        print("\nEnvironment variables you can set:")
        print("  - DATABASE_URL: Full database connection string")
        print("  - DB_PATH: Path for SQLite database (default: /app/data/agent_tracker.db)")
        print("  - USER_ID: Default user ID for sessions")
        print("  - ENVIRONMENT: Environment name (default: production)")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
