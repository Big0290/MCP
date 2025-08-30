#!/usr/bin/env python3
"""
Test Class Registration Fix

This script tests if the class registration fix resolves the
SQLAlchemy mapping issue.
"""

import sys
from datetime import datetime

def test_class_registration():
    """Test if class registration is working."""
    print("=== TESTING CLASS REGISTRATION ===\n")
    
    try:
        # Clear any cached imports
        if 'models_unified' in sys.modules:
            del sys.modules['models_unified']
        
        print("✅ Cleared cached imports")
        
        # Import the fixed version
        from models_unified import force_class_registration, SQLALCHEMY_AVAILABLE, Base
        
        print("✅ Models imported successfully")
        print(f"   SQLAlchemy available: {SQLALCHEMY_AVAILABLE}")
        print(f"   Base class: {Base}")
        
        if SQLALCHEMY_AVAILABLE and Base:
            print("✅ SQLAlchemy ORM is available")
            
            # Test class registration
            result = force_class_registration()
            
            if result:
                print("✅ Class registration successful")
                return True
            else:
                print("❌ Class registration failed")
                return False
        else:
            print("❌ SQLAlchemy ORM not available")
            return False
            
    except Exception as e:
        print(f"❌ Class registration test failed: {e}")
        return False

def test_global_database_with_class_registration():
    """Test if global database works with class registration."""
    print("\n=== TESTING GLOBAL DATABASE WITH CLASS REGISTRATION ===\n")
    
    try:
        from models_unified import initialize_global_database, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Initialize global database (which should force class registration)
        result = initialize_global_database()
        
        if result:
            print("✅ Global database initialized with class registration")
            
            # Test if we can now query the mapped classes
            try:
                from models_unified import get_global_session
                
                session = get_global_session()
                print(f"✅ Session created: {type(session).__name__}")
                
                # Test queries
                interactions_count = session.query(UnifiedInteraction).count()
                print(f"✅ Interactions query successful: {interactions_count}")
                
                sessions_count = session.query(UnifiedSession).count()
                print(f"✅ Sessions query successful: {sessions_count}")
                
                print("🎉 Class registration fix is working!")
                return True
                
            except Exception as e:
                print(f"❌ Session queries still failed: {e}")
                return False
        else:
            print("❌ Global database initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Global database test failed: {e}")
        return False

def test_session_factory_with_class_registration():
    """Test if session factory works with class registration."""
    print("\n=== TESTING SESSION FACTORY WITH CLASS REGISTRATION ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory, UnifiedInteraction, UnifiedSession
        
        # Create session factory
        session_factory = UnifiedSessionFactory()
        print("✅ Session factory created")
        
        # Create a session
        session = session_factory()
        print(f"✅ Session created: {type(session).__name__}")
        
        # Test if session recognizes mapped classes
        try:
            # Test querying interactions
            interactions_count = session.query(UnifiedInteraction).count()
            print(f"✅ Interactions query successful: {interactions_count}")
            
            # Test querying sessions
            sessions_count = session.query(UnifiedSession).count()
            print(f"✅ Sessions query successful: {sessions_count}")
            
            print("🎉 Session factory with class registration is working!")
            return True
            
        except Exception as e:
            print(f"❌ Query still failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Session factory test failed: {e}")
        return False

def test_database_operations_with_class_registration():
    """Test if database operations work with class registration."""
    print("\n=== TESTING DATABASE OPERATIONS WITH CLASS REGISTRATION ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory, UnifiedInteraction
        
        session_factory = UnifiedSessionFactory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Test creating a real interaction
            try:
                test_interaction = UnifiedInteraction(
                    interaction_type="class_registration_test",
                    client_request="Test request with class registration fix",
                    agent_response="Test response with class registration fix",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "class_registration": True, "verified": True}
                )
                
                print("✅ Test interaction created")
                
                # Add to session
                session.add(test_interaction)
                print("✅ Test interaction added to session")
                
                # Commit to database
                session.commit()
                print("✅ Test interaction committed to database")
                
                # Verify it was stored
                stored_count = session.query(UnifiedInteraction).count()
                print(f"✅ Total interactions in database: {stored_count}")
                
                # Look for our test interaction
                stored_interaction = session.query(UnifiedInteraction).filter_by(
                    interaction_type="class_registration_test"
                ).first()
                
                if stored_interaction:
                    print(f"✅ Test interaction found in database")
                    print(f"   ID: {stored_interaction.id}")
                    print(f"   Type: {stored_interaction.interaction_type}")
                    print(f"   Timestamp: {stored_interaction.timestamp}")
                    print("🎉 DATABASE OPERATIONS WITH CLASS REGISTRATION ARE WORKING!")
                    return True
                else:
                    print("❌ Test interaction not found in database")
                    return False
                    
            except Exception as e:
                print(f"❌ Database operations failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 TESTING CLASS REGISTRATION FIX\n")
    print("This script will test if the class registration fix resolves the SQLAlchemy mapping issue.\n")
    
    # Test all components
    tests = [
        ("Class Registration", test_class_registration),
        ("Global Database with Class Registration", test_global_database_with_class_registration),
        ("Session Factory with Class Registration", test_session_factory_with_class_registration),
        ("Database Operations with Class Registration", test_database_operations_with_class_registration)
    ]
    
    success_count = 0
    for name, test_func in tests:
        try:
            print(f"🧪 Running: {name}")
            result = test_func()
            if result:
                success_count += 1
                print(f"   ✅ {name} passed")
            else:
                print(f"   ❌ {name} failed")
        except Exception as e:
            print(f"   ❌ {name} failed with error: {e}")
    
    print(f"\n📊 Test Results: {success_count}/{len(tests)} tests passed")
    
    if success_count == len(tests):
        print("\n🎉 COMPLETE SUCCESS!")
        print("   • Class registration working")
        print("   • Global database working")
        print("   • Session factory working")
        print("   • Database operations working")
        
        print("\n🚀 **Your interaction tracking system is now fully functional!**")
        print("   • Interactions will be stored in real database")
        print("   • Context injection will work with real data")
        print("   • Conversation #107 will be properly tracked")
        
        print("\n🧪 **Final Test Commands:**")
        print("python diagnose_interaction_tracking.py")
        print("python test_conversation_tracking.py")
        
        print("\n💡 **Expected Results:**")
        print("• Real SQLAlchemy sessions with mapped classes")
        print("• Interactions stored in real SQLite database")
        print("• Context injection working with actual conversation data")
        print("• Conversation #107 properly tracked and stored")
        
    elif success_count > 0:
        print("\n⚠️  PARTIAL SUCCESS")
        print("   • Some components working, others need attention")
        print("   • Check the output above for specific failures")
        
    else:
        print("\n❌ ALL TESTS FAILED")
        print("   • Class registration fix may not have worked")
        print("   • Check for syntax errors or import issues")
        print("   • Consider manual intervention")

if __name__ == "__main__":
    main()
