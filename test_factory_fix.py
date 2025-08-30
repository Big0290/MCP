#!/usr/bin/env python3
"""
Test Factory Fix

This script tests if the UnifiedSessionFactory fix worked and now
returns real SQLAlchemy sessions instead of MockSession.
"""

import sys
from datetime import datetime

def test_factory_fix():
    """Test if the factory now returns real sessions."""
    print("=== TESTING FACTORY FIX ===\n")
    
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
        print(f"   Is production: {factory.is_production}")
        
        # Test session creation
        print("🔄 Testing session creation...")
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
    print("\n=== TESTING REAL DATABASE OPERATIONS ===\n")
    
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
                    interaction_type="factory_fix_verification",
                    client_request="Test request after factory fix verification",
                    agent_response="Test response after factory fix verification",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "factory_fixed": True, "verified": True}
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

def main():
    """Main test function."""
    print("🧪 TESTING FACTORY FIX\n")
    print("This script will test if the UnifiedSessionFactory fix worked.\n")
    
    # Test the factory fix
    factory_working = test_factory_fix()
    
    if factory_working:
        print("\n✅ FACTORY FIX WORKED!")
        print("   Now getting real SQLAlchemy sessions")
        
        # Test real database operations
        database_working = test_real_database_operations()
        
        if database_working:
            print("\n🎉 COMPLETE SUCCESS!")
            print("   • Factory returns real sessions")
            print("   • Database persistence working")
            print("   • Interaction tracking should now work")
            
            print("\n🚀 **Next Steps:**")
            print("1. Test your enhanced_chat function")
            print("2. Verify interactions are being logged")
            print("3. Check that context injection works")
            print("4. Monitor database growth")
            
            print("\n🧪 **Test Commands:**")
            print("python diagnose_interaction_tracking.py")
            print("python test_conversation_tracking.py")
            
        else:
            print("\n⚠️  PARTIAL SUCCESS")
            print("   • Factory returns real sessions ✅")
            print("   • Database persistence not working ❌")
            print("   • May need additional database setup")
            
    else:
        print("\n❌ FACTORY FIX DIDN'T WORK")
        print("   Still getting MockSession")
        print("   May need manual intervention")
        
        print("\n🔧 **Troubleshooting:**")
        print("• Check if the file was modified correctly")
        print("• Verify SQLAlchemy is installed")
        print("• Check for syntax errors in models_unified.py")
        print("• Consider manual file editing")

if __name__ == "__main__":
    main()
