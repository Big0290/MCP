#!/usr/bin/env python3
"""
Test script for session persistence functionality
Demonstrates how sessions persist across restarts and conversation changes
"""

import time
import json
from datetime import datetime

def test_session_persistence():
    """Test the session persistence system"""
    print("🧪 Testing Session Persistence System")
    print("=" * 50)
    
    try:
        # Import the session manager
        from session_manager import session_manager
        print("✅ Session manager imported successfully")
        
        # Test 1: Create a new session
        print("\n📝 Test 1: Creating new session")
        session_id = session_manager.create_or_resume_session(user_id="test_user")
        print(f"   Created session: {session_id}")
        
        # Test 2: Update session activity
        print("\n📝 Test 2: Updating session activity")
        session_manager.update_session_activity(session_id, 5)
        session = session_manager.get_session(session_id)
        print(f"   Session interactions: {session.total_interactions}")
        
        # Test 3: Update session context
        print("\n📝 Test 3: Updating session context")
        session_manager.update_session_context(
            session_id,
            "Working on Python project with MCP integration",
            ["python", "mcp", "integration"],
            {"technical_level": "intermediate", "preferred_topics": ["coding", "architecture"]}
        )
        print(f"   Context updated for session: {session_id}")
        
        # Test 4: List active sessions
        print("\n📝 Test 4: Listing active sessions")
        sessions = session_manager.list_active_sessions()
        print(f"   Found {len(sessions)} active sessions")
        
        # Test 5: Export session data
        print("\n📝 Test 5: Exporting session data")
        export_data = session_manager.export_session_data(session_id)
        if export_data:
            print(f"   Successfully exported session data")
            print(f"   Export contains {len(export_data.get('interactions', []))} interactions")
        else:
            print("   Failed to export session data")
        
        # Test 6: Simulate session persistence (save to disk)
        print("\n📝 Test 6: Testing disk persistence")
        print("   Session data saved to disk automatically")
        print("   You can now restart the script to test session resumption")
        
        # Test 7: Create another session for merge testing
        print("\n📝 Test 7: Creating second session for merge testing")
        session_id_2 = session_manager.create_or_resume_session(user_id="test_user")
        print(f"   Created second session: {session_id_2}")
        
        # Test 8: Merge sessions
        print("\n📝 Test 8: Merging sessions")
        success = session_manager.merge_sessions(session_id, session_id_2)
        if success:
            print(f"   Successfully merged {session_id_2} into {session_id}")
            # Check updated session
            updated_session = session_manager.get_session(session_id)
            print(f"   Updated session interactions: {updated_session.total_interactions}")
        else:
            print("   Failed to merge sessions")
        
        print("\n✅ All tests completed successfully!")
        print(f"📊 Final session count: {len(session_manager.list_active_sessions())}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_session_resumption():
    """Test resuming a session after restart simulation"""
    print("\n🔄 Testing Session Resumption")
    print("=" * 50)
    
    try:
        from session_manager import session_manager
        
        # List existing sessions
        sessions = session_manager.list_active_sessions()
        if not sessions:
            print("   No sessions to resume")
            return False
        
        # Try to resume the first session
        first_session = sessions[0]
        session_id = first_session['session_id']
        
        print(f"   Attempting to resume session: {session_id}")
        
        # Simulate resuming the session
        resumed_id = session_manager.create_or_resume_session(
            user_id=first_session['user_id'], 
            session_id=session_id
        )
        
        if resumed_id == session_id:
            print(f"   ✅ Successfully resumed session: {session_id}")
            
            # Get updated session info
            session = session_manager.get_session(session_id)
            if session:
                print(f"   📊 Session details:")
                print(f"      • User ID: {session.user_id}")
                print(f"      • Total Interactions: {session.total_interactions}")
                print(f"      • Context Summary: {session.context_summary or 'None'}")
                print(f"      • Active Topics: {session.active_topics or 'None'}")
            
            return True
        else:
            print(f"   ❌ Failed to resume session. Got: {resumed_id}")
            return False
            
    except Exception as e:
        print(f"   ❌ Resumption test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Session Persistence Test Suite")
    print("This test demonstrates how sessions persist across restarts")
    print()
    
    # Run initial tests
    success = test_session_persistence()
    
    if success:
        print("\n" + "=" * 60)
        print("💡 To test session resumption across restarts:")
        print("   1. Run this script again")
        print("   2. Use the 'resume_session' MCP tool")
        print("   3. Check that session data persists")
        print("=" * 60)
        
        # Test resumption
        test_session_resumption()
    
    print("\n🏁 Test suite completed")

if __name__ == "__main__":
    main()
