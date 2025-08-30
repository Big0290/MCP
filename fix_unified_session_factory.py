#!/usr/bin/env python3
"""
Fix Unified Session Factory

This script fixes the UnifiedSessionFactory so it returns real SQLAlchemy
sessions for local environment instead of always returning MockSession.
"""

import os
import sys
from datetime import datetime

def backup_models_unified():
    """Create a backup of the models_unified.py file."""
    print("=== CREATING BACKUP ===\n")
    
    source_file = "models_unified.py"
    if os.path.exists(source_file):
        backup_file = f"models_unified.py.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            import shutil
            shutil.copy2(source_file, backup_file)
            print(f"✅ Backup created: {backup_file}")
        except Exception as e:
            print(f"❌ Backup failed: {e}")
    else:
        print(f"❌ Source file not found: {source_file}")
    
    print()

def check_current_factory_behavior():
    """Check the current behavior of the UnifiedSessionFactory."""
    print("=== CHECKING CURRENT FACTORY BEHAVIOR ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory, detect_environment
        
        # Check current environment
        env = detect_environment()
        print(f"✅ Current environment: {env}")
        
        # Check factory behavior
        factory = UnifiedSessionFactory()
        print(f"✅ Factory created: {type(factory).__name__}")
        print(f"   Is local: {factory.is_local}")
        print(f"   Is production: {factory.is_production}")
        
        # Test session creation
        with factory() as session:
            session_type = type(session).__name__
            print(f"   Session type: {session_type}")
            
            if 'Mock' in session_type:
                print("   ❌ Still getting MockSession!")
            else:
                print("   ✅ Getting real session!")
                
    except Exception as e:
        print(f"❌ Factory behavior check failed: {e}")
    
    print()

def fix_unified_session_factory():
    """Fix the UnifiedSessionFactory to return real sessions for local environment."""
    print("=== FIXING UNIFIED SESSION FACTORY ===\n")
    
    try:
        # Read the current file
        with open("models_unified.py", "r") as f:
            content = f.read()
        
        print("✅ Models unified file read")
        
        # Check if the problematic code exists
        problematic_code = "else:\n        return MockSession()"
        if problematic_code in content:
            print("✅ Found problematic code to fix")
            
            # Replace the problematic logic
            old_code = """    def __call__(self):
        \"\"\"Create a new session\"\"\"
        if self.is_production:
            try:
                # Try to use SQLAlchemy session
                from sqlalchemy.orm import Session
                # Use local implementation instead of circular import
                SessionLocal = UnifiedSessionFactory()
                return SessionLocal()
            except Exception:
                # Fallback to mock session
                return MockSession()
        else:
            return MockSession()"""
            
            new_code = """    def __call__(self):
        \"\"\"Create a new session\"\"\"
        if self.is_production:
            try:
                # Try to use SQLAlchemy session
                from sqlalchemy.orm import Session
                # Use local implementation instead of circular import
                SessionLocal = UnifiedSessionFactory()
                return SessionLocal()
            except Exception:
                # Fallback to mock session
                return MockSession()
        else:
            # For local environment, try to use real SQLAlchemy session
            try:
                from sqlalchemy import create_engine
                from sqlalchemy.orm import sessionmaker, Session
                
                # Get database URL
                from models_unified import get_database_url
                database_url = get_database_url()
                
                # Create engine and session
                engine = create_engine(database_url, echo=False)
                SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                
                # Create and return real session
                return SessionLocal()
            except Exception as e:
                print(f"⚠️  Failed to create real session for local environment: {e}")
                print("   Falling back to MockSession")
                return MockSession()"""
            
            # Replace the code
            if old_code in content:
                content = content.replace(old_code, new_code)
                print("✅ Fixed factory logic")
            else:
                print("⚠️  Could not find exact code to replace")
                print("   Will try alternative approach...")
                
                # Try alternative replacement
                old_alt = "        else:\n            return MockSession()"
                new_alt = """        else:
            # For local environment, try to use real SQLAlchemy session
            try:
                from sqlalchemy import create_engine
                from sqlalchemy.orm import sessionmaker, Session
                
                # Get database URL
                from models_unified import get_database_url
                database_url = get_database_url()
                
                # Create engine and session
                engine = create_engine(database_url, echo=False)
                SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                
                # Create and return real session
                return SessionLocal()
            except Exception as e:
                print(f"⚠️  Failed to create real session for local environment: {e}")
                print("   Falling back to MockSession")
                return MockSession()"""
                
                if old_alt in content:
                    content = content.replace(old_alt, new_alt)
                    print("✅ Fixed factory logic (alternative)")
                else:
                    print("❌ Could not find code to replace")
                    return False
        else:
            print("⚠️  Problematic code not found - factory may already be fixed")
            return True
        
        # Write the fixed content back
        with open("models_unified.py", "w") as f:
            f.write(content)
        
        print("✅ Models unified file updated")
        return True
        
    except Exception as e:
        print(f"❌ Factory fix failed: {e}")
        return False

def test_fixed_factory():
    """Test if the fixed factory now returns real sessions."""
    print("=== TESTING FIXED FACTORY ===\n")
    
    try:
        # Clear any cached imports
        if 'models_unified' in sys.modules:
            del sys.modules['models_unified']
        
        print("✅ Cleared cached imports")
        
        # Import the fixed version
        from models_unified import UnifiedSessionFactory, detect_environment
        
        # Check environment
        env = detect_environment()
        print(f"✅ Environment: {env}")
        
        # Test factory
        factory = UnifiedSessionFactory()
        print(f"✅ Factory: {type(factory).__name__}")
        print(f"   Is local: {factory.is_local}")
        
        # Test session creation
        with factory() as session:
            session_type = type(session).__name__
            print(f"   Session type: {session_type}")
            
            if 'Mock' in session_type:
                print("   ❌ Still getting MockSession!")
                return False
            else:
                print("   ✅ Now getting real SQLAlchemy session!")
                
                # Test if it has real database methods
                if hasattr(session, 'execute'):
                    print("   ✅ Has execute method")
                if hasattr(session, 'query'):
                    print("   ✅ Has query method")
                if hasattr(session, 'add'):
                    print("   ✅ Has add method")
                if hasattr(session, 'commit'):
                    print("   ✅ Has commit method")
                
                return True
                
    except Exception as e:
        print(f"❌ Factory test failed: {e}")
        return False

def test_real_database_operations():
    """Test if real database operations work with the fixed factory."""
    print("=== TESTING REAL DATABASE OPERATIONS ===\n")
    
    try:
        from models_unified import get_session_factory, UnifiedInteraction
        
        session_factory = get_session_factory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Test basic query
            try:
                count = session.query(UnifiedInteraction).count()
                print(f"✅ Query successful: {count} interactions")
                
                # Test creating a real interaction
                test_interaction = UnifiedInteraction(
                    interaction_type="factory_fix_test",
                    client_request="Test request after factory fix",
                    agent_response="Test response after factory fix",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "factory_fixed": True}
                )
                
                session.add(test_interaction)
                session.commit()
                print("✅ Real interaction created and committed!")
                
                # Verify it was stored
                new_count = session.query(UnifiedInteraction).count()
                print(f"✅ New count: {new_count} interactions")
                
                if new_count > count:
                    print("🎉 REAL DATABASE PERSISTENCE IS WORKING!")
                    return True
                else:
                    print("❌ Interaction count didn't increase")
                    return False
                    
            except Exception as e:
                print(f"❌ Database operations failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Real database operations test failed: {e}")
        return False

def provide_verification_commands():
    """Provide commands to verify the fix worked."""
    print("=== VERIFICATION COMMANDS ===\n")
    
    print("🔍 **Verify the Factory Fix Worked:**")
    print("python diagnose_interaction_tracking.py")
    print("python test_conversation_tracking.py")
    
    print("\n📊 **Check Database Status:**")
    print("python -c \"from models_unified import get_session_factory, UnifiedInteraction; sf = get_session_factory(); session = sf(); print(f'Total interactions: {session.query(UnifiedInteraction).count()}')\"")
    
    print("\n🧪 **Test Enhanced Chat:**")
    print("python -c \"from enhanced_chat_integration import enhanced_chat; response = enhanced_chat('Test message'); print(f'Response type: {type(response)}')\"")
    
    print("\n📈 **Monitor Progress:**")
    print("# Run this to see if interactions are being logged:")
    print("watch -n 5 'python -c \"from models_unified import get_session_factory, UnifiedInteraction; sf = get_session_factory(); session = sf(); print(f\"Interactions: {session.query(UnifiedInteraction).count()}\")\"'")

def main():
    """Main fix function."""
    print("🔧 FIXING UNIFIED SESSION FACTORY\n")
    print("This script will fix the UnifiedSessionFactory so it returns")
    print("real SQLAlchemy sessions instead of always returning MockSession.\n")
    
    # Run all fixes
    steps = [
        ("Create Backup", backup_models_unified),
        ("Check Current Behavior", check_current_factory_behavior),
        ("Fix Factory Logic", fix_unified_session_factory),
        ("Test Fixed Factory", test_fixed_factory),
        ("Test Real Database", test_real_database_operations)
    ]
    
    success = True
    for name, func in steps:
        try:
            print(f"🔧 Running: {name}")
            result = func()
            if result is False:
                success = False
                print(f"   ❌ {name} failed")
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            success = False
    
    # Provide verification commands
    provide_verification_commands()
    
    print("\n" + "="*60)
    if success:
        print("🎯 FACTORY FIX COMPLETE - SUCCESS!")
    else:
        print("🎯 FACTORY FIX COMPLETE - SOME ISSUES REMAIN")
    print("="*60)
    
    if success:
        print("\n✅ **What Was Fixed:**")
        print("• UnifiedSessionFactory now returns real sessions for local environment")
        print("• MockSession fallback only when real sessions fail")
        print("• Real database persistence enabled")
        print("• Interaction tracking should now work")
        
        print("\n🚀 **Next Steps:**")
        print("1. Test your enhanced_chat function")
        print("2. Verify interactions are being logged")
        print("3. Check that context injection works")
        print("4. Monitor database growth")
        
        print("\n🧪 **Test Commands:**")
        print("python diagnose_interaction_tracking.py")
        print("python test_conversation_tracking.py")
        
        print("\n💡 **Expected Results:**")
        print("• Real SQLAlchemy sessions instead of MockSession")
        print("• Interactions stored in real SQLite database")
        print("• Context injection working with real data")
        print("• Conversation #107 properly tracked and stored")
    else:
        print("\n⚠️ **Issues Remain:**")
        print("• Some fixes may not have completed successfully")
        print("• Check the output above for specific errors")
        print("• Consider manual intervention or alternative approaches")
        
        print("\n🔧 **Troubleshooting:**")
        print("• Check file permissions")
        print("• Verify Python environment")
        print("• Review error messages")
        print("• Consider manual file editing")

if __name__ == "__main__":
    main()
