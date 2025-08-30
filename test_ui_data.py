#!/usr/bin/env python3
"""
Test script to verify UI data availability and database connectivity
"""

import sqlite3
import os
from datetime import datetime

def test_database_connection():
    """Test database connection and data availability"""
    print("🔍 Testing Database Connection and Data Availability")
    print("=" * 60)
    
    # Test main database
    db_path = "./data/agent_tracker.db"
    if os.path.exists(db_path):
        print(f"✅ Main database found: {db_path}")
        print(f"📊 Database size: {os.path.getsize(db_path) / (1024*1024):.1f} MB")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Test tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📋 Available tables: {[table[0] for table in tables]}")
            
            # Test data counts
            if 'agent_interactions' in [t[0] for t in tables]:
                cursor.execute("SELECT COUNT(*) FROM agent_interactions")
                count = cursor.fetchone()[0]
                print(f"💬 Total interactions: {count}")
                
                if count > 0:
                    cursor.execute("SELECT timestamp FROM agent_interactions ORDER BY timestamp DESC LIMIT 1")
                    latest = cursor.fetchone()[0]
                    print(f"🕐 Latest interaction: {latest}")
            
            if 'sessions' in [t[0] for t in tables]:
                cursor.execute("SELECT COUNT(*) FROM sessions")
                count = cursor.fetchone()[0]
                print(f"🔄 Total sessions: {count}")
                
                if count > 0:
                    cursor.execute("SELECT last_activity FROM sessions ORDER BY last_activity DESC LIMIT 1")
                    latest = cursor.fetchone()[0]
                    print(f"🕐 Latest session activity: {latest}")
            
            if 'conversation_contexts' in [t[0] for t in tables]:
                cursor.execute("SELECT COUNT(*) FROM conversation_contexts")
                count = cursor.fetchone()[0]
                print(f"🧠 Total contexts: {count}")
            
            conn.close()
            print("✅ Database connection successful")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
    
    else:
        print(f"❌ Main database not found: {db_path}")
    
    # Test local database
    db_path_local = "./data/agent_tracker_local.db"
    if os.path.exists(db_path_local):
        print(f"✅ Local database found: {db_path_local}")
        print(f"📊 Local database size: {os.path.getsize(db_path_local) / (1024*1024):.1f} MB")
    else:
        print(f"❌ Local database not found: {db_path_local}")
    
    print("\n" + "=" * 60)

def test_models_import():
    """Test if the unified models can be imported"""
    print("🔍 Testing Models Import")
    print("=" * 60)
    
    try:
        from models_unified import get_environment_info, get_session_factory
        print("✅ Unified models import successful")
        
        # Test environment info
        env_info = get_environment_info()
        print(f"🌍 Environment: {env_info['environment']}")
        print(f"🗄️ Database URL: {env_info['database_url']}")
        
        # Test session factory
        session_factory = get_session_factory()
        print(f"🏭 Session factory: {type(session_factory).__name__}")
        
    except Exception as e:
        print(f"❌ Models import failed: {e}")
    
    print("\n" + "=" * 60)

def test_ui_dependencies():
    """Test UI dependencies"""
    print("🔍 Testing UI Dependencies")
    print("=" * 60)
    
    try:
        import pandas as pd
        print(f"✅ Pandas available: {pd.__version__}")
    except ImportError:
        print("❌ Pandas not available")
    
    try:
        import streamlit as st
        print("✅ Streamlit available")
    except ImportError:
        print("❌ Streamlit not available - install with: pip install streamlit")
    
    try:
        import plotly
        print(f"✅ Plotly available: {plotly.__version__}")
    except ImportError:
        print("❌ Plotly not available - install with: pip install plotly")
    
    print("\n" + "=" * 60)

def main():
    """Main test function"""
    print("🚀 UI Data Availability Test")
    print("=" * 60)
    print(f"🕐 Test run at: {datetime.now()}")
    print()
    
    test_database_connection()
    test_models_import()
    test_ui_dependencies()
    
    print("🎯 Recommendations:")
    print("1. If Streamlit is not available, install it: pip install streamlit")
    print("2. If data is not showing, check database permissions and table schemas")
    print("3. Use the refresh buttons in the UI to get latest data")
    print("4. Enable auto-refresh for real-time updates")

if __name__ == "__main__":
    main()
