#!/usr/bin/env python3
"""
Diagnose Interaction Tracking System

This script identifies why your interaction tracking system is broken
and provides solutions to fix it.
"""

import os
import sqlite3
from datetime import datetime, timedelta
import json

def check_database_connection():
    """Check database connection and basic functionality."""
    print("=== DATABASE CONNECTION DIAGNOSIS ===\n")
    
    # Check database files
    db_paths = [
        "./data/agent_tracker.db",
        "./data/agent_tracker_local.db"
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            print(f"✅ Database found: {db_path}")
            print(f"   Size: {os.path.getsize(db_path)} bytes")
            print(f"   Modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
            
            # Try to connect
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"   Tables: {[table[0] for table in tables]}")
                
                # Check interaction count
                if 'interactions' in [table[0] for table in tables]:
                    cursor.execute("SELECT COUNT(*) FROM interactions;")
                    count = cursor.fetchone()[0]
                    print(f"   Total interactions: {count}")
                    
                    # Check recent interactions
                    cursor.execute("SELECT MAX(timestamp) FROM interactions;")
                    latest = cursor.fetchone()[0]
                    if latest:
                        print(f"   Latest interaction: {latest}")
                    else:
                        print("   ⚠️  No interactions found")
                        
                conn.close()
                
            except Exception as e:
                print(f"   ❌ Database error: {e}")
        else:
            print(f"❌ Database not found: {db_path}")
    
    print()

def check_interaction_logger():
    """Check if the interaction logger is working."""
    print("=== INTERACTION LOGGER DIAGNOSIS ===\n")
    
    try:
        from interaction_logger import logger
        
        logger = InteractionLogger()
        print("✅ InteractionLogger imported successfully")
        
        # Check if we can log a test interaction
        try:
            test_interaction = logger.log_interaction(
                interaction_type="test",
                client_request="Test request",
                agent_response="Test response",
                status="success"
            )
            print("✅ Test interaction logged successfully")
            
            # Check if we can retrieve it
            recent = logger.get_context_for_injection("test_user")
            if recent:
                print("✅ Recent interactions retrieved")
            else:
                print("⚠️  No recent interactions retrieved")
                
        except Exception as e:
            print(f"❌ Test interaction failed: {e}")
            
    except ImportError as e:
        print(f"❌ InteractionLogger import failed: {e}")
    except Exception as e:
        print(f"❌ InteractionLogger error: {e}")
    
    print()

def check_session_manager():
    """Check if the session manager is working."""
    print("=== SESSION MANAGER DIAGNOSIS ===\n")
    
    try:
        from session_manager import SessionManager
        
        manager = SessionManager()
        print("✅ SessionManager imported successfully")
        
        # Check active sessions
        try:
            active_sessions = manager.list_active_sessions()
            print(f"✅ Active sessions: {len(active_sessions)}")
            
            for session in active_sessions[:3]:  # Show first 3
                print(f"   Session: {session.get('session_id', 'N/A')[:8]}...")
                print(f"     User: {session.get('user_id', 'N/A')}")
                print(f"     Interactions: {session.get('interaction_count', 0)}")
                print(f"     Last Activity: {session.get('last_activity', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Session listing failed: {e}")
            
    except ImportError as e:
        print(f"❌ SessionManager import failed: {e}")
    except Exception as e:
        print(f"❌ SessionManager error: {e}")
    
    print()

def check_models_unified():
    """Check if the unified models are working."""
    print("=== UNIFIED MODELS DIAGNOSIS ===\n")
    
    try:
        from models_unified import get_local_interactions, get_local_sessions
        
        print("✅ Unified models imported successfully")
        
        # Check local interactions
        try:
            interactions = get_local_interactions(10)
            print(f"✅ Local interactions: {len(interactions)}")
            
            if interactions:
                latest = max(interactions, key=lambda x: getattr(x, 'timestamp', datetime.min))
                print(f"   Latest interaction: {getattr(latest, 'timestamp', 'N/A')}")
                print(f"   Type: {getattr(latest, 'interaction_type', 'N/A')}")
            else:
                print("   ⚠️  No local interactions found")
                
        except Exception as e:
            print(f"❌ Local interactions failed: {e}")
            
        # Check local sessions
        try:
            sessions = get_local_sessions()
            print(f"✅ Local sessions: {len(sessions)}")
            
        except Exception as e:
            print(f"❌ Local sessions failed: {e}")
            
    except ImportError as e:
        print(f"❌ Unified models import failed: {e}")
    except Exception as e:
        print(f"❌ Unified models error: {e}")
    
    print()

def check_mcp_server_status():
    """Check MCP server status."""
    print("=== MCP SERVER STATUS DIAGNOSIS ===\n")
    
    try:
        from main import get_system_status
        
        status = get_system_status()
        print("✅ MCP server status retrieved")
        
        # Check key components
        if 'database' in status:
            db_status = status['database']
            print(f"   Database: {db_status.get('status', 'unknown')}")
            print(f"   Connection: {db_status.get('connection_status', 'unknown')}")
            
        if 'logging' in status:
            logging_status = status['logging']
            print(f"   Logging: {logging_status.get('status', 'unknown')}")
            
        if 'sessions' in status:
            sessions_status = status['sessions']
            print(f"   Sessions: {sessions_status.get('status', 'unknown')}")
            print(f"   Active: {sessions_status.get('active_count', 0)}")
            
    except ImportError as e:
        print(f"❌ MCP server import failed: {e}")
    except Exception as e:
        print(f"❌ MCP server status failed: {e}")
    
    print()

def check_data_directory():
    """Check data directory structure."""
    print("=== DATA DIRECTORY DIAGNOSIS ===\n")
    
    data_dir = "./data"
    if os.path.exists(data_dir):
        print(f"✅ Data directory exists: {data_dir}")
        
        # List contents
        contents = os.listdir(data_dir)
        print(f"   Contents: {contents}")
        
        # Check sessions directory
        sessions_dir = os.path.join(data_dir, "sessions")
        if os.path.exists(sessions_dir):
            session_files = os.listdir(sessions_dir)
            print(f"   Session files: {len(session_files)}")
            
            # Check recent session files
            recent_files = sorted(session_files, key=lambda x: os.path.getmtime(os.path.join(sessions_dir, x)), reverse=True)[:5]
            for file in recent_files:
                file_path = os.path.join(sessions_dir, file)
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                size = os.path.getsize(file_path)
                print(f"     {file}: {size} bytes, modified {mtime}")
        else:
            print("   ⚠️  Sessions directory not found")
    else:
        print(f"❌ Data directory not found: {data_dir}")
    
    print()

def test_interaction_logging():
    """Test if we can actually log interactions."""
    print("=== INTERACTION LOGGING TEST ===\n")
    
    try:
        from interaction_logger import logger
        
        logger = InteractionLogger()
        
        # Test logging a conversation turn
        print("🔄 Testing conversation turn logging...")
        result = logger.log_conversation_turn(
            client_request="This is a test request to check if logging works",
            agent_response="This is a test response to verify the system",
            metadata={"test": True, "timestamp": datetime.now().isoformat()}
        )
        
        if result:
            print("✅ Conversation turn logged successfully")
            
            # Try to retrieve it
            print("🔄 Testing interaction retrieval...")
            recent = logger.get_context_for_injection("test_user")
            if recent:
                print("✅ Recent interactions retrieved successfully")
                print(f"   Context length: {len(recent)} characters")
            else:
                print("⚠️  Recent interactions not retrieved")
        else:
            print("❌ Conversation turn logging failed")
            
    except Exception as e:
        print(f"❌ Interaction logging test failed: {e}")
    
    print()

def provide_solutions():
    """Provide solutions based on the diagnosis."""
    print("=== SOLUTIONS & NEXT STEPS ===\n")
    
    print("🔧 **Immediate Actions:**")
    print("1. Check database permissions and file locks")
    print("2. Verify the MCP server is running properly")
    print("3. Check if background monitoring is active")
    print("4. Verify session persistence is working")
    
    print("\n🔄 **System Restart Steps:**")
    print("1. Stop any running MCP servers")
    print("2. Clear any lock files in ./data/")
    print("3. Restart the MCP server")
    print("4. Test interaction logging")
    
    print("\n📊 **Monitoring Setup:**")
    print("1. Enable background monitoring")
    print("2. Set up interaction logging alerts")
    print("3. Monitor database growth")
    print("4. Check session persistence")
    
    print("\n🧪 **Testing Commands:**")
    print("python test_conversation_tracking.py")
    print("python diagnose_interaction_tracking.py")
    print("python -c \"from main import test_conversation_tracking; test_conversation_tracking('test')\"")

def main():
    """Main diagnostic function."""
    print("🔍 INTERACTION TRACKING SYSTEM DIAGNOSIS\n")
    print("This script will identify why your interaction tracking system")
    print("isn't working and provide solutions to fix it.\n")
    
    # Run all diagnostics
    diagnostics = [
        ("Database Connection", check_database_connection),
        ("Interaction Logger", check_interaction_logger),
        ("Session Manager", check_session_manager),
        ("Unified Models", check_models_unified),
        ("MCP Server Status", check_mcp_server_status),
        ("Data Directory", check_data_directory),
        ("Interaction Logging Test", test_interaction_logging)
    ]
    
    for name, func in diagnostics:
        try:
            print(f"🧪 Running: {name}")
            func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            print()
    
    # Provide solutions
    provide_solutions()
    
    print("\n" + "="*60)
    print("🎯 DIAGNOSIS COMPLETE!")
    print("="*60)
    
    print("\n💡 **Next Steps:**")
    print("1. Review the diagnostic output above")
    print("2. Identify the specific component that's failing")
    print("3. Apply the recommended solutions")
    print("4. Test the system again")
    print("5. Monitor for recurring issues")
    
    print("\n🚨 **If issues persist:**")
    print("• Check system logs for errors")
    print("• Verify database integrity")
    print("• Test individual components")
    print("• Consider database migration if needed")

if __name__ == "__main__":
    main()
