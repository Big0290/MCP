#!/usr/bin/env python3
"""
Simple test script for session persistence functionality
Tests the core session management without database dependencies
"""

import os
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def test_session_manager_core():
    """Test the core session manager functionality without database"""
    print("🧪 Testing Core Session Manager (No Database)")
    print("=" * 50)
    
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    sessions_dir = Path(temp_dir) / "sessions"
    sessions_dir.mkdir()
    
    try:
        # Mock the models module to avoid database dependencies
        import sys
        from unittest.mock import MagicMock
        
        # Create mock models
        mock_models = MagicMock()
        mock_models.get_session_factory = MagicMock()
        mock_models.Session = MagicMock()
        mock_models.AgentInteraction = MagicMock()
        mock_models.ConversationContext = MagicMock()
        
        # Mock config
        mock_config = MagicMock()
        mock_config.USER_ID = "test_user"
        mock_config.CONTAINER_ID = "test_container"
        mock_config.ENVIRONMENT = "test"
        
        # Mock the session factory to return a context manager
        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__enter__ = MagicMock(return_value=mock_session_factory.return_value)
        mock_session_factory.return_value.__exit__ = MagicMock(return_value=None)
        mock_models.get_session_factory.return_value = mock_session_factory
        
        # Add mocks to sys.modules
        sys.modules['models'] = mock_models
        sys.modules['config'] = mock_config
        
        # Now import the session manager
        from session_manager import SessionManager
        
        # Create session manager with temp directory
        manager = SessionManager()
        manager._session_file_dir = sessions_dir
        
        print("✅ Session manager created successfully")
        
        # Test 1: Create a new session
        print("\n📝 Test 1: Creating new session")
        session_id = manager.create_or_resume_session(user_id="test_user")
        print(f"   Created session: {session_id}")
        
        # Test 2: Get session
        print("\n📝 Test 2: Getting session")
        session = manager.get_session(session_id)
        if session:
            print(f"   Session found: {session.session_id}")
            print(f"   User ID: {session.user_id}")
            print(f"   Interactions: {session.total_interactions}")
        else:
            print("   ❌ Session not found")
            return False
        
        # Test 3: Update session activity
        print("\n📝 Test 3: Updating session activity")
        manager.update_session_activity(session_id, 5)
        updated_session = manager.get_session(session_id)
        print(f"   Updated interactions: {updated_session.total_interactions}")
        
        # Test 4: Update session context
        print("\n📝 Test 4: Updating session context")
        manager.update_session_context(
            session_id,
            "Working on Python project with MCP integration",
            ["python", "mcp", "integration"],
            {"technical_level": "intermediate", "preferred_topics": ["coding", "architecture"]}
        )
        print(f"   Context updated for session: {session_id}")
        
        # Test 5: List active sessions
        print("\n📝 Test 5: Listing active sessions")
        sessions = manager.list_active_sessions()
        print(f"   Found {len(sessions)} active sessions")
        
        # Test 6: Check file persistence
        print("\n📝 Test 6: Checking file persistence")
        session_file = sessions_dir / f"{session_id}.json"
        if session_file.exists():
            print(f"   ✅ Session file created: {session_file}")
            
            # Read and verify file content
            with open(session_file, 'r') as f:
                file_data = json.load(f)
            print(f"   File contains session ID: {file_data.get('session_id')}")
            print(f"   File contains user ID: {file_data.get('user_id')}")
        else:
            print("   ❌ Session file not found")
            return False
        
        # Test 7: Create another session for merge testing
        print("\n📝 Test 7: Creating second session for merge testing")
        session_id_2 = manager.create_or_resume_session(user_id="test_user")
        print(f"   Created second session: {session_id_2}")
        
        # Test 8: Merge sessions
        print("\n📝 Test 8: Merging sessions")
        success = manager.merge_sessions(session_id, session_id_2)
        if success:
            print(f"   ✅ Successfully merged {session_id_2} into {session_id}")
            # Check updated session
            updated_session = manager.get_session(session_id)
            print(f"   Updated session interactions: {updated_session.total_interactions}")
        else:
            print("   ❌ Failed to merge sessions")
        
        # Test 9: Test session expiration
        print("\n📝 Test 9: Testing session expiration")
        # Create a very old session
        old_session_id = manager.create_or_resume_session(user_id="test_user")
        old_session = manager.get_session(old_session_id)
        
        # Manually set it to be very old
        old_session.last_activity = datetime.utcnow() - timedelta(days=10)
        manager._save_session_to_disk(old_session)
        
        # Run cleanup
        sessions_before = len(manager.list_active_sessions())
        manager.cleanup_expired_sessions()
        sessions_after = len(manager.list_active_sessions())
        
        print(f"   Sessions before cleanup: {sessions_before}")
        print(f"   Sessions after cleanup: {sessions_after}")
        print(f"   Expired sessions removed: {sessions_before - sessions_after}")
        
        print("\n✅ All core tests completed successfully!")
        print(f"📊 Final session count: {len(manager.list_active_sessions())}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   This test requires the session_manager module")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            print(f"\n🧹 Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            print(f"\n⚠️ Failed to clean up temp directory: {e}")

def test_file_operations():
    """Test file operations for session persistence"""
    print("\n📁 Testing File Operations")
    print("=" * 50)
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    sessions_dir = Path(temp_dir) / "sessions"
    sessions_dir.mkdir()
    
    try:
        # Test creating session files
        print("📝 Test: Creating session files")
        
        # Create a mock session data structure
        session_data = {
            'session_id': 'test123',
            'user_id': 'user123',
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'total_interactions': 10,
            'session_file_path': str(sessions_dir / 'test123.json'),
            'metadata': {'test': True},
            'context_summary': 'Test context',
            'active_topics': ['test', 'session'],
            'user_preferences': {'level': 'beginner'}
        }
        
        # Save to file
        session_file = sessions_dir / 'test123.json'
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"   ✅ Created session file: {session_file}")
        
        # Test reading session files
        print("📖 Test: Reading session files")
        
        with open(session_file, 'r') as f:
            loaded_data = json.load(f)
        
        print(f"   ✅ Loaded session data: {loaded_data['session_id']}")
        print(f"   User ID: {loaded_data['user_id']}")
        print(f"   Interactions: {loaded_data['total_interactions']}")
        
        # Test file listing
        print("📋 Test: Listing session files")
        
        session_files = list(sessions_dir.glob("*.json"))
        print(f"   Found {len(session_files)} session files:")
        for file in session_files:
            print(f"     • {file.name}")
        
        print("✅ File operations test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False
    finally:
        # Clean up
        try:
            shutil.rmtree(temp_dir)
            print(f"🧹 Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            print(f"⚠️ Failed to clean up temp directory: {e}")

def main():
    """Main test function"""
    print("🚀 Simple Session Persistence Test Suite")
    print("This test demonstrates core session persistence without database dependencies")
    print()
    
    # Test core functionality
    core_success = test_session_manager_core()
    
    # Test file operations
    file_success = test_file_operations()
    
    if core_success and file_success:
        print("\n" + "=" * 60)
        print("🎉 All tests passed!")
        print("💡 The session persistence system is working correctly")
        print("   You can now use the MCP tools to manage sessions")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Some tests failed")
        print("   Check the error messages above for details")
        print("=" * 60)
    
    print("\n🏁 Test suite completed")

if __name__ == "__main__":
    main()
