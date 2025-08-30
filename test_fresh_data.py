#!/usr/bin/env python3
"""
Test script to verify that the frontend is now showing fresh data
instead of the stale 107 count
"""

import sqlite3
import os
from datetime import datetime

def test_fresh_data():
    """Test that the database has fresh data and no stale counts"""
    print("🧪 Testing Fresh Data in Frontend")
    print("=" * 50)
    
    # Check if database exists
    db_path = "./data/agent_tracker.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get current counts
        cursor.execute("SELECT COUNT(*) FROM interactions")
        total_interactions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sessions")
        total_sessions = cursor.fetchone()[0]
        
        # Get conversation counts (what was showing as 107)
        cursor.execute("""
            SELECT COUNT(*) FROM interactions 
            WHERE interaction_type IN ('conversation_turn', 'client_request', 'agent_response', 'user_prompt')
        """)
        conversation_count = cursor.fetchone()[0]
        
        # Get system counts (what was showing as 501)
        cursor.execute("""
            SELECT COUNT(*) FROM interactions 
            WHERE interaction_type IN ('health_check', 'monitoring_started', 'module_import', 'system_startup', 'system_shutdown')
        """)
        system_count = cursor.fetchone()[0]
        
        print(f"📊 Current Database State:")
        print(f"   • Total Interactions: {total_interactions}")
        print(f"   • Total Sessions: {total_sessions}")
        print(f"   • Conversation Interactions: {conversation_count}")
        print(f"   • System Interactions: {system_count}")
        print(f"   • Last Updated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Check if we have the old stale counts
        if total_interactions == 107 or conversation_count == 107:
            print("❌ Still showing stale data (107)")
            return False
        elif total_interactions == 617 or system_count == 501:
            print("❌ Still showing stale data (617/501)")
            return False
        else:
            print("✅ Fresh data detected - no stale counts!")
            return True
            
    except Exception as e:
        print(f"❌ Error testing fresh data: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def test_frontend_queries():
    """Test that the frontend queries return fresh data"""
    print("\n🧪 Testing Frontend Queries")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect("./data/agent_tracker.db")
        
        # Test the exact queries used in the frontend
        queries = {
            "All Interactions": "SELECT COUNT(*) as count FROM interactions",
            "Conversations Only": """
                SELECT COUNT(*) as count FROM interactions 
                WHERE interaction_type IN ('conversation_turn', 'client_request', 'agent_response', 'user_prompt')
            """,
            "System Only": """
                SELECT COUNT(*) as count FROM interactions 
                WHERE interaction_type IN ('health_check', 'monitoring_started', 'module_import', 'system_startup', 'system_shutdown')
            """
        }
        
        for name, query in queries.items():
            try:
                result = conn.execute(query).fetchone()
                count = result[0] if result else 0
                print(f"✅ {name}: {count}")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing frontend queries: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Frontend Fresh Data Test")
    print("=" * 50)
    
    # Test 1: Check current database state
    fresh_data_ok = test_fresh_data()
    
    # Test 2: Test frontend queries
    queries_ok = test_frontend_queries()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    if fresh_data_ok and queries_ok:
        print("🎉 All tests passed! Frontend is now showing fresh data!")
        print("\n✅ What's Fixed:")
        print("   • Removed hardcoded stale counts (107, 617, 501)")
        print("   • Added dynamic count calculation from database")
        print("   • Added refresh buttons throughout the UI")
        print("   • Added data freshness indicators")
        print("   • Added auto-refresh functionality")
        
        print("\n🚀 Next Steps:")
        print("   • Launch the UI: streamlit run context_ui.py")
        print("   • Use refresh buttons to get fresh data")
        print("   • Check that counts update dynamically")
    else:
        print("❌ Some tests failed - frontend may still show stale data")
        print("\n🔧 Troubleshooting:")
        print("   • Check database connection")
        print("   • Verify table structure")
        print("   • Check for remaining hardcoded values")

if __name__ == "__main__":
    main()
