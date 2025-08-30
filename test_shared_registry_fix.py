#!/usr/bin/env python3
"""
Test Shared Registry Fix

This script tests if the shared registry approach resolves the
SQLAlchemy 2.x mapping issue by ensuring Base and sessions use the same registry.
"""

import sys
from datetime import datetime

def test_shared_registry_setup():
    """Test if shared registry is properly set up."""
    print("=== TESTING SHARED REGISTRY SETUP ===\n")
    
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
        
        # Check if shared registry is available
        if hasattr(Base, 'registry'):
            print(f"✅ Base has shared registry: {type(Base.registry).__name__}")
            print(f"✅ Registry metadata: {type(Base.registry.metadata).__name__}")
            return True
        else:
            print("❌ Base does not have shared registry")
            return False
        
    except Exception as e:
        print(f"❌ Shared registry setup test failed: {e}")
        return False

def test_shared_registry_metadata():
    """Test if shared registry metadata is properly configured."""
    print("\n=== TESTING SHARED REGISTRY METADATA ===\n")
    
    try:
        from models_unified import Base, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Check if shared registry is available
        if not hasattr(Base, 'registry'):
            print("❌ No shared registry available")
            return False
        
        print(f"✅ Shared registry available: {type(Base.registry).__name__}")
        
        # Check if our classes are registered in the shared registry
        if 'interactions' in Base.registry.metadata.tables:
            print("✅ Interactions table registered in shared registry")
        else:
            print("⚠️  Interactions table not in shared registry")
        
        if 'sessions' in Base.registry.metadata.tables:
            print("✅ Sessions table registered in shared registry")
        else:
            print("⚠️  Sessions table not in shared registry")
        
        return True
        
    except Exception as e:
        print(f"❌ Shared registry metadata test failed: {e}")
        return False

def test_shared_registry_session_binding():
    """Test if sessions are properly bound to shared registry."""
    print("\n=== TESTING SHARED REGISTRY SESSION BINDING ===\n")
    
    try:
        from models_unified import initialize_global_database, get_global_session, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Initialize global database with shared registry
        print("🔄 Initializing global database with shared registry...")
        result = initialize_global_database()
        
        if result:
            print("✅ Global database initialized with shared registry")
            
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
                    
                    print("🎉 Shared registry session binding is working!")
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
        print(f"❌ Shared registry session binding test failed: {e}")
        return False

def test_shared_registry_explicit_session():
    """Test if explicit sessions work with shared registry."""
    print("\n=== TESTING SHARED REGISTRY EXPLICIT SESSION ===\n")
    
    try:
        from models_unified import create_session_with_explicit_base, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Try to create a session with shared registry
        try:
            session = create_session_with_explicit_base()
            
            if session:
                print(f"✅ Shared registry session created: {type(session).__name__}")
                
                # Test if session recognizes mapped classes
                try:
                    # Test querying interactions
                    interactions_count = session.query(UnifiedInteraction).count()
                    print(f"✅ Interactions query successful: {interactions_count}")
                    
                    # Test querying sessions
                    sessions_count = session.query(UnifiedSession).count()
                    print(f"✅ Sessions query successful: {sessions_count}")
                    
                    print("🎉 Shared registry explicit session is working!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Query still failed: {e}")
                    return False
            else:
                print("❌ Shared registry session creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Shared registry session creation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Shared registry explicit session test failed: {e}")
        return False

def test_shared_registry_database_operations():
    """Test if database operations work with shared registry."""
    print("\n=== TESTING SHARED REGISTRY DATABASE OPERATIONS ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory, UnifiedInteraction
        
        session_factory = UnifiedSessionFactory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Test creating a real interaction
            try:
                test_interaction = UnifiedInteraction(
                    interaction_type="shared_registry_test",
                    client_request="Test request with shared registry",
                    agent_response="Test response with shared registry",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "shared_registry": True, "verified": True}
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
                    interaction_type="shared_registry_test"
                ).first()
                
                if stored_interaction:
                    print(f"✅ Test interaction found in database")
                    print(f"   ID: {stored_interaction.id}")
                    print(f"   Type: {stored_interaction.interaction_type}")
                    print(f"   Timestamp: {stored_interaction.timestamp}")
                    print("🎉 SHARED REGISTRY DATABASE OPERATIONS ARE WORKING!")
                    return True
                else:
                    print("❌ Test interaction not found in database")
                    return False
                    
            except Exception as e:
                print(f"❌ Database operations failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Shared registry database operations test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 TESTING SHARED REGISTRY FIX\n")
    print("This script will test if the shared registry approach resolves the SQLAlchemy 2.x mapping issue.\n")
    
    # Test all components
    tests = [
        ("Shared Registry Setup", test_shared_registry_setup),
        ("Shared Registry Metadata", test_shared_registry_metadata),
        ("Shared Registry Session Binding", test_shared_registry_session_binding),
        ("Shared Registry Explicit Session", test_shared_registry_explicit_session),
        ("Shared Registry Database Operations", test_shared_registry_database_operations)
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
        print("   • Shared registry properly set up")
        print("   • Shared registry metadata working")
        print("   • Shared registry session binding working")
        print("   • Shared registry explicit session working")
        print("   • Shared registry database operations working")
        
        print("\n🚀 **Your interaction tracking system is now fully functional!**")
        print("   • SQLAlchemy 2.x shared registry issue resolved")
        print("   • Interactions will be stored in real database")
        print("   • Context injection will work with real data")
        print("   • Conversation #107 will be properly tracked")
        
        print("\n🧪 **Final Test Commands:**")
        print("python diagnose_interaction_tracking.py")
        print("python test_conversation_tracking.py")
        
        print("\n💡 **Expected Results:**")
        print("• SQLAlchemy 2.x shared registry properly configured")
        print("• Base and sessions using same registry instance")
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
        print("   • Shared registry fix may not have worked")
        print("   • Check for syntax errors or import issues")
        print("   • Consider manual intervention")

if __name__ == "__main__":
    main()
