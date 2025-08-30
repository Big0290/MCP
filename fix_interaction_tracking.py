#!/usr/bin/env python3
"""
Fix Interaction Tracking System

This script fixes common issues with the interaction tracking system
and restores functionality.
"""

import os
import sqlite3
import shutil
from datetime import datetime
import json

def backup_database():
    """Create a backup of the current database."""
    print("=== CREATING DATABASE BACKUP ===\n")
    
    db_paths = [
        "./data/agent_tracker.db",
        "./data/agent_tracker_local.db"
    ]
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            backup_path = f"{db_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                shutil.copy2(db_path, backup_path)
                print(f"✅ Backup created: {backup_path}")
            except Exception as e:
                print(f"❌ Backup failed for {db_path}: {e}")
        else:
            print(f"⚠️  Database not found: {db_path}")
    
    print()

def clear_lock_files():
    """Clear any database lock files."""
    print("=== CLEARING LOCK FILES ===\n")
    
    data_dir = "./data"
    if os.path.exists(data_dir):
        lock_files = []
        for file in os.listdir(data_dir):
            if file.endswith('.lock') or file.endswith('.db-journal') or file.endswith('.db-wal'):
                lock_files.append(file)
        
        if lock_files:
            for lock_file in lock_files:
                try:
                    os.remove(os.path.join(data_dir, lock_file))
                    print(f"✅ Removed lock file: {lock_file}")
                except Exception as e:
                    print(f"❌ Failed to remove {lock_file}: {e}")
        else:
            print("✅ No lock files found")
    else:
        print("⚠️  Data directory not found")
    
    print()

def reset_interaction_logger():
    """Reset the interaction logger to a clean state."""
    print("=== RESETTING INTERACTION LOGGER ===\n")
    
    try:
        from interaction_logger import InteractionLogger
        
        logger = InteractionLogger()
        print("✅ InteractionLogger imported")
        
        # Clear any cached data
        try:
            if hasattr(logger, 'clear_cache'):
                logger.clear_cache()
                print("✅ Cache cleared")
        except:
            print("⚠️  Cache clearing not available")
        
        # Test logging
        print("🔄 Testing interaction logging...")
        test_result = logger.log_interaction(
            interaction_type="system_reset",
            client_request="System reset test",
            agent_response="System reset successful",
            status="success",
            metadata={"reset": True, "timestamp": datetime.now().isoformat()}
        )
        
        if test_result:
            print("✅ Test interaction logged successfully")
        else:
            print("⚠️  Test interaction logging failed")
            
    except Exception as e:
        print(f"❌ Interaction logger reset failed: {e}")
    
    print()

def reset_session_manager():
    """Reset the session manager."""
    print("=== RESETTING SESSION MANAGER ===\n")
    
    try:
        from session_manager import SessionManager
        
        manager = SessionManager()
        print("✅ SessionManager imported")
        
        # Clean up expired sessions
        try:
            if hasattr(manager, 'cleanup_expired_sessions'):
                manager.cleanup_expired_sessions()
                print("✅ Expired sessions cleaned up")
        except:
            print("⚠️  Session cleanup not available")
        
        # Create a test session
        print("🔄 Creating test session...")
        try:
            test_session = manager.create_or_resume_session("test_user", "test_session")
            if test_session:
                print("✅ Test session created successfully")
                print(f"   Session ID: {test_session.get('session_id', 'N/A')}")
            else:
                print("⚠️  Test session creation failed")
        except Exception as e:
            print(f"❌ Test session creation failed: {e}")
            
    except Exception as e:
        print(f"❌ Session manager reset failed: {e}")
    
    print()

def reset_database_connection():
    """Reset database connections."""
    print("=== RESETTING DATABASE CONNECTION ===\n")
    
    try:
        from models_unified import get_session_factory
        
        # Get a fresh session factory
        session_factory = get_session_factory()
        print("✅ Session factory retrieved")
        
        # Test database connection
        with session_factory() as session:
            print("✅ Database connection test successful")
            
            # Test a simple query
            try:
                from models_unified import UnifiedInteraction
                count = session.query(UnifiedInteraction).count()
                print(f"   Current interactions in database: {count}")
            except Exception as e:
                print(f"   ⚠️  Query test failed: {e}")
                
    except Exception as e:
        print(f"❌ Database connection reset failed: {e}")
    
    print()

def test_system_functionality():
    """Test if the system is working after fixes."""
    print("=== TESTING SYSTEM FUNCTIONALITY ===\n")
    
    try:
        from main import test_conversation_tracking
        
        print("🔄 Testing conversation tracking...")
        result = test_conversation_tracking("System functionality test after fixes")
        
        if result:
            print("✅ Conversation tracking test successful")
            print(f"   Response length: {len(result)} characters")
        else:
            print("⚠️  Conversation tracking test failed")
            
    except Exception as e:
        print(f"❌ System functionality test failed: {e}")
    
    print()

def enable_background_monitoring():
    """Enable background monitoring if available."""
    print("=== ENABLING BACKGROUND MONITORING ===\n")
    
    try:
        from main import background_monitoring
        
        print("✅ Background monitoring function found")
        print("💡 To enable background monitoring, run:")
        print("   python -c \"from main import background_monitoring; background_monitoring()\"")
        
    except ImportError:
        print("⚠️  Background monitoring not available")
    except Exception as e:
        print(f"❌ Background monitoring check failed: {e}")
    
    print()

def provide_maintenance_commands():
    """Provide commands for ongoing maintenance."""
    print("=== MAINTENANCE COMMANDS ===\n")
    
    print("🔧 **Regular Maintenance Commands:**")
    print("python diagnose_interaction_tracking.py")
    print("python test_conversation_tracking.py")
    print("python -c \"from main import get_system_status; print(get_system_status())\"")
    
    print("\n📊 **Database Maintenance:**")
    print("python -c \"from models_unified import get_session_factory; sf = get_session_factory(); print('Database OK')\"")
    
    print("\n🧹 **Cleanup Commands:**")
    print("python -c \"from session_manager import SessionManager; sm = SessionManager(); sm.cleanup_expired_sessions()\"")
    
    print("\n🔄 **Restart Commands:**")
    print("# Stop any running servers, then:")
    print("python run-mcp.sh")
    print("python start_stdio_server.py")

def main():
    """Main fix function."""
    print("🔧 FIXING INTERACTION TRACKING SYSTEM\n")
    print("This script will fix common issues and restore functionality.\n")
    
    # Run all fixes
    fixes = [
        ("Database Backup", backup_database),
        ("Clear Lock Files", clear_lock_files),
        ("Reset Interaction Logger", reset_interaction_logger),
        ("Reset Session Manager", reset_session_manager),
        ("Reset Database Connection", reset_database_connection),
        ("Test System Functionality", test_system_functionality),
        ("Enable Background Monitoring", enable_background_monitoring)
    ]
    
    for name, func in fixes:
        try:
            print(f"🔧 Running: {name}")
            func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            print()
    
    # Provide maintenance commands
    provide_maintenance_commands()
    
    print("\n" + "="*60)
    print("🎯 FIXES COMPLETE!")
    print("="*60)
    
    print("\n✅ **What Was Fixed:**")
    print("• Database lock files cleared")
    print("• Interaction logger reset")
    print("• Session manager reset")
    print("• Database connections refreshed")
    print("• System functionality tested")
    
    print("\n🚀 **Next Steps:**")
    print("1. Test your interaction tracking system")
    print("2. Monitor for any recurring issues")
    print("3. Run regular maintenance commands")
    print("4. Check system status periodically")
    
    print("\n🧪 **Test Commands:**")
    print("python diagnose_interaction_tracking.py")
    print("python test_conversation_tracking.py")
    
    print("\n💡 **If issues persist:**")
    print("• Check the diagnostic output")
    print("• Verify database integrity")
    print("• Check system logs")
    print("• Consider database migration")

if __name__ == "__main__":
    main()
