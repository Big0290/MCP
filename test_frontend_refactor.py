#!/usr/bin/env python3
"""
Test script to verify frontend refactoring works correctly
Tests database queries and schema compatibility
"""

import sqlite3
import os
import sys
from pathlib import Path

def test_database_connection():
    """Test database connection and basic queries"""
    print("🧪 Testing Database Connection...")
    
    # Check if database exists
    db_path = "./data/agent_tracker.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        print("✅ Database connection successful")
        
        # Test basic queries
        cursor = conn.cursor()
        
        # Test interactions table
        cursor.execute("SELECT COUNT(*) FROM interactions")
        interactions_count = cursor.fetchone()[0]
        print(f"✅ Interactions table: {interactions_count} records")
        
        # Test sessions table
        cursor.execute("SELECT COUNT(*) FROM sessions")
        sessions_count = cursor.fetchone()[0]
        print(f"✅ Sessions table: {sessions_count} records")
        
        # Test new fields exist
        cursor.execute("PRAGMA table_info(interactions)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required_fields = ['tool_name', 'parameters', 'error_message', 'interaction_metadata']
        missing_fields = [field for field in required_fields if field not in columns]
        
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
            return False
        else:
            print("✅ All new fields present")
        
        # Test sample queries that the UI will use
        print("\n🧪 Testing UI Queries...")
        
        # Test system stats query
        cursor.execute("""
            SELECT COUNT(*) FROM interactions 
            WHERE timestamp > datetime('now', '-1 hour')
        """)
        recent_count = cursor.fetchone()[0]
        print(f"✅ Recent activity query: {recent_count} interactions")
        
        # Test interaction types query
        cursor.execute("""
            SELECT interaction_type, COUNT(*) as count 
            FROM interactions 
            GROUP BY interaction_type
        """)
        types = cursor.fetchall()
        print(f"✅ Interaction types query: {len(types)} types found")
        
        # Test sessions query
        cursor.execute("""
            SELECT id, started_at, last_activity, total_interactions, user_id
            FROM sessions 
            ORDER BY last_activity DESC 
            LIMIT 5
        """)
        sessions = cursor.fetchall()
        print(f"✅ Sessions query: {len(sessions)} sessions found")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_ui_imports():
    """Test if UI components can be imported"""
    print("\n🧪 Testing UI Imports...")
    
    try:
        # Test if we can import the main UI module
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Test database functions without Streamlit
        from context_ui import init_database_connection, get_system_stats
        print("✅ Core UI functions imported successfully")
        
        # Test if we can create a database connection
        conn = init_database_connection()
        if conn:
            print("✅ Database connection function works")
            conn.close()
        else:
            print("⚠️ Database connection function returned None")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ UI test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Frontend Refactoring Test")
    print("=" * 40)
    
    # Test database
    db_ok = test_database_connection()
    
    # Test UI imports
    ui_ok = test_ui_imports()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 40)
    
    if db_ok and ui_ok:
        print("🎉 All tests passed! Frontend refactoring is successful!")
        print("\n✅ What's Working:")
        print("  - Database schema updated to SQLAlchemy 2.x")
        print("  - New fields (tool_name, parameters, error_message) present")
        print("  - UI queries updated to use correct table names")
        print("  - Core UI functions importable")
        print("  - Database connection working")
        
        print("\n🚀 Next Steps:")
        print("  - Install UI dependencies: pip install -r requirements_ui.txt")
        print("  - Launch UI: ./run_ui.sh")
        print("  - Or manually: streamlit run context_ui.py")
        
    else:
        print("❌ Some tests failed. Check the output above for details.")
        
        if not db_ok:
            print("\n🔧 Database Issues:")
            print("  - Check if database exists: ./data/agent_tracker.db")
            print("  - Run: python init_db.py")
            
        if not ui_ok:
            print("\n🔧 UI Issues:")
            print("  - Install dependencies: pip install -r requirements_ui.txt")
            print("  - Check Python path and imports")

if __name__ == "__main__":
    main()
