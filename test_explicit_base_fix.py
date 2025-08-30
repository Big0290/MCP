#!/usr/bin/env python3
"""
Test Explicit Base Fix

This script tests if the explicit Base approach resolves the
SQLAlchemy mapping issue.
"""

import sys
from datetime import datetime

def test_explicit_base_session_creation():
    """Test if explicit Base session creation works."""
    print("=== TESTING EXPLICIT BASE SESSION CREATION ===\n")
    
    try:
        # Clear any cached imports
        if 'models_unified' in sys.modules:
            del sys.modules['models_unified']
        
        print("✅ Cleared cached imports")
        
        # Import the fixed version
        from models_unified import create_session_with_explicit_base, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Try to create a session with explicit Base
        try:
            session = create_session_with_explicit_base()
            
            if session:
                print(f"✅ Explicit Base session created: {type(session).__name__}")
                
                # Test if session recognizes mapped classes
                try:
                    # Test querying interactions
                    interactions_count = session.query(UnifiedInteraction).count()
                    print(f"✅ Interactions query successful: {interactions_count}")
                    
                    # Test querying sessions
                    sessions_count = session.query(UnifiedSession).count()
                    print(f"✅ Sessions query successful: {sessions_count}")
                    
                    print("🎉 Explicit Base session creation is working!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Query still failed: {e}")
                    return False
            else:
                print("❌ Explicit Base session creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Explicit Base session creation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Explicit Base test failed: {e}")
        return False

def test_session_factory_with_explicit_base():
    """Test if session factory works with explicit Base approach."""
    print("\n=== TESTING SESSION FACTORY WITH EXPLICIT BASE ===\n")
    
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
            
            print("🎉 Session factory with explicit Base is working!")
            return True
            
        except Exception as e:
            print(f"❌ Query still failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Session factory test failed: {e}")
        return False

def test_database_operations_with_explicit_base():
    """Test if database operations work with explicit Base."""
    print("\n=== TESTING DATABASE OPERATIONS WITH EXPLICIT BASE ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory, UnifiedInteraction
        
        session_factory = UnifiedSessionFactory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Test creating a real interaction
            try:
                test_interaction = UnifiedInteraction(
                    interaction_type="explicit_base_test",
                    client_request="Test request with explicit Base",
                    agent_response="Test response with explicit Base",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "explicit_base": True, "verified": True}
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
                    interaction_type="explicit_base_test"
                ).first()
                
                if stored_interaction:
                    print(f"✅ Test interaction found in database")
                    print(f"   ID: {stored_interaction.id}")
                    print(f"   Type: {stored_interaction.interaction_type}")
                    print(f"   Timestamp: {stored_interaction.timestamp}")
                    print("🎉 DATABASE OPERATIONS WITH EXPLICIT BASE ARE WORKING!")
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

def test_interaction_logging_with_explicit_base():
    """Test if interaction logging works with explicit Base."""
    print("\n=== TESTING INTERACTION LOGGING WITH EXPLICIT BASE ===\n")
    
    try:
        from interaction_logger import InteractionLogger
        
        logger = InteractionLogger()
        print("✅ InteractionLogger created")
        
        # Test logging a real interaction
        print("🔄 Testing interaction logging...")
        result = logger.log_interaction(
            interaction_type="logger_explicit_base_test",
            client_request="Test request with explicit Base",
            agent_response="Test response with explicit Base",
            status="success",
            metadata={"test": True, "explicit_base": True, "logger_test": True}
        )
        
        if result:
            print("✅ Interaction logged successfully")
            
            # Verify it's in the database
            try:
                from models_unified import UnifiedSessionFactory, UnifiedInteraction
                
                session_factory = UnifiedSessionFactory()
                with session_factory() as session:
                    count = session.query(UnifiedInteraction).count()
                    print(f"   Total interactions in database: {count}")
                    
                    if count > 0:
                        print("✅ Interactions are now being stored in real database!")
                        
                        # Show the real interaction
                        real_interaction = session.query(UnifiedInteraction).filter_by(
                            interaction_type="logger_explicit_base_test"
                        ).first()
                        
                        if real_interaction:
                            print(f"   Real interaction ID: {real_interaction.id}")
                            print(f"   Real interaction timestamp: {real_interaction.timestamp}")
                            print("🎉 INTERACTION LOGGING WITH EXPLICIT BASE IS WORKING!")
                            return True
                        else:
                            print("❌ Real interaction not found in database")
                            return False
                    else:
                        print("❌ Still no interactions in real database")
                        return False
                        
            except Exception as e:
                print(f"   ❌ Database verification failed: {e}")
                return False
        else:
            print("❌ Interaction logging failed")
            return False
            
    except Exception as e:
        print(f"❌ Interaction logging test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 TESTING EXPLICIT BASE FIX\n")
    print("This script will test if the explicit Base approach resolves the SQLAlchemy mapping issue.\n")
    
    # Test all components
    tests = [
        ("Explicit Base Session Creation", test_explicit_base_session_creation),
        ("Session Factory with Explicit Base", test_session_factory_with_explicit_base),
        ("Database Operations with Explicit Base", test_database_operations_with_explicit_base),
        ("Interaction Logging with Explicit Base", test_interaction_logging_with_explicit_base)
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
        print("   • Explicit Base session working")
        print("   • Session factory working")
        print("   • Database operations working")
        print("   • Interaction logging working")
        
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
        print("   • Explicit Base fix may not have worked")
        print("   • Check for syntax errors or import issues")
        print("   • Consider manual intervention")

if __name__ == "__main__":
    main()
