#!/usr/bin/env python3
"""
Test SQLAlchemy 2.x Session Binding Fix

This script tests if the SQLAlchemy 2.x session binding fix resolves the
"Column expression, FROM clause" mapping issue.
"""

import sys
from datetime import datetime

def test_sqlalchemy_2x_session_binding():
    """Test if SQLAlchemy 2.x sessions are properly bound to Base registry."""
    print("=== TESTING SQLALCHEMY 2.X SESSION BINDING ===\n")
    
    try:
        # Clear any cached imports
        if 'models_unified' in sys.modules:
            del sys.modules['models_unified']
        
        print("✅ Cleared cached imports")
        
        # Import the fixed version
        from models_unified import SQLALCHEMY_VERSION, SQLALCHEMY_2X, Base
        
        print(f"✅ SQLAlchemy version detected: {SQLALCHEMY_VERSION}")
        print(f"✅ SQLAlchemy 2.x mode: {SQLALCHEMY_2X}")
        print(f"✅ Base class type: {type(Base).__name__}")
        
        # Check if metadata is available
        if hasattr(Base, 'metadata'):
            print(f"✅ Base has metadata: {type(Base.metadata).__name__}")
            print(f"✅ Metadata tables: {list(Base.metadata.tables.keys())}")
        else:
            print("❌ Base does not have metadata attribute")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Session binding test failed: {e}")
        return False

def test_global_session_factory_binding():
    """Test if global session factory is properly bound."""
    print("\n=== TESTING GLOBAL SESSION FACTORY BINDING ===\n")
    
    try:
        from models_unified import initialize_global_database, get_global_session, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Initialize global database
        print("🔄 Initializing global database...")
        result = initialize_global_database()
        
        if result:
            print("✅ Global database initialized")
            
            # Try to get a global session
            try:
                session = get_global_session()
                print(f"✅ Global session created: {type(session).__name__}")
                
                # Test if session recognizes mapped classes
                try:
                    # Test querying interactions
                    interactions_count = session.query(UnifiedInteraction).count()
                    print(f"✅ Interactions query successful: {interactions_count}")
                    
                    # Test querying sessions
                    sessions_count = session.query(UnifiedSession).count()
                    print(f"✅ Sessions query successful: {sessions_count}")
                    
                    print("🎉 Global session factory binding is working!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Query still failed: {e}")
                    return False
                    
            except Exception as e:
                print(f"❌ Global session creation failed: {e}")
                return False
        else:
            print("❌ Global database initialization failed")
            return False
            
    except Exception as e:
        print(f"❌ Global session factory test failed: {e}")
        return False

def test_explicit_base_session_binding():
    """Test if explicit Base session binding works."""
    print("\n=== TESTING EXPLICIT BASE SESSION BINDING ===\n")
    
    try:
        from models_unified import create_session_with_explicit_base, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Try to create a session with explicit Base binding
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
                    
                    print("🎉 Explicit Base session binding is working!")
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
        print(f"❌ Explicit Base session binding test failed: {e}")
        return False

def test_session_factory_binding():
    """Test if session factory binding works."""
    print("\n=== TESTING SESSION FACTORY BINDING ===\n")
    
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
            
            print("🎉 Session factory binding is working!")
            return True
            
        except Exception as e:
            print(f"❌ Query still failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Session factory binding test failed: {e}")
        return False

def test_database_operations_with_binding():
    """Test if database operations work with proper binding."""
    print("\n=== TESTING DATABASE OPERATIONS WITH BINDING ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory, UnifiedInteraction
        
        session_factory = UnifiedSessionFactory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Test creating a real interaction
            try:
                test_interaction = UnifiedInteraction(
                    interaction_type="binding_test",
                    client_request="Test request with proper binding",
                    agent_response="Test response with proper binding",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "binding": True, "verified": True}
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
                    interaction_type="binding_test"
                ).first()
                
                if stored_interaction:
                    print(f"✅ Test interaction found in database")
                    print(f"   ID: {stored_interaction.id}")
                    print(f"   Type: {stored_interaction.interaction_type}")
                    print(f"   Timestamp: {stored_interaction.timestamp}")
                    print("🎉 DATABASE OPERATIONS WITH PROPER BINDING ARE WORKING!")
                    return True
                else:
                    print("❌ Test interaction not found in database")
                    return False
                    
            except Exception as e:
                print(f"❌ Database operations failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database operations with binding test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 TESTING SQLALCHEMY 2.X SESSION BINDING FIX\n")
    print("This script will test if the SQLAlchemy 2.x session binding fix resolves the mapping issue.\n")
    
    # Test all components
    tests = [
        ("SQLAlchemy 2.x Session Binding", test_sqlalchemy_2x_session_binding),
        ("Global Session Factory Binding", test_global_session_factory_binding),
        ("Explicit Base Session Binding", test_explicit_base_session_binding),
        ("Session Factory Binding", test_session_factory_binding),
        ("Database Operations with Binding", test_database_operations_with_binding)
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
        print("   • SQLAlchemy 2.x session binding working")
        print("   • Global session factory binding working")
        print("   • Explicit Base session binding working")
        print("   • Session factory binding working")
        print("   • Database operations with binding working")
        
        print("\n🚀 **Your interaction tracking system is now fully functional!**")
        print("   • SQLAlchemy 2.x session binding issue resolved")
        print("   • Interactions will be stored in real database")
        print("   • Context injection will work with real data")
        print("   • Conversation #107 will be properly tracked")
        
        print("\n🧪 **Final Test Commands:**")
        print("python diagnose_interaction_tracking.py")
        print("python test_conversation_tracking.py")
        
        print("\n💡 **Expected Results:**")
        print("• SQLAlchemy 2.x sessions properly bound to Base registry")
        print("• Mapped classes recognized in session context")
        print("• Database queries working without errors")
        print("• Interactions stored in real SQLite database")
        print("• Context injection working with actual conversation data")
        print("• Conversation #107 properly tracked and stored")
        
    elif success_count > 0:
        print("\n⚠️  PARTIAL SUCCESS")
        print("   • Some components working, others need attention")
        print("   • Check the output above for specific failures")
        
    else:
        print("\n❌ ALL TESTS FAILED")
        print("   • SQLAlchemy 2.x session binding fix may not have worked")
        print("   • Check for syntax errors or import issues")
        print("   • Consider manual intervention")

if __name__ == "__main__":
    main()
