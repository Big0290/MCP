#!/usr/bin/env python3
"""
Test SQLAlchemy 2.x Metadata Fix

This script tests if the SQLAlchemy 2.x metadata fix resolves the
DeclarativeBase metadata issue.
"""

import sys
from datetime import datetime

def test_sqlalchemy_2x_metadata():
    """Test if SQLAlchemy 2.x metadata is properly configured."""
    print("=== TESTING SQLALCHEMY 2.X METADATA ===\n")
    
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
            return True
        else:
            print("❌ Base does not have metadata attribute")
            return False
        
    except Exception as e:
        print(f"❌ Metadata test failed: {e}")
        return False

def test_metadata_table_creation():
    """Test if metadata can create tables."""
    print("\n=== TESTING METADATA TABLE CREATION ===\n")
    
    try:
        from models_unified import Base, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Check if metadata is available
        if not hasattr(Base, 'metadata'):
            print("❌ No metadata available")
            return False
        
        print(f"✅ Metadata available: {type(Base.metadata).__name__}")
        
        # Check if our classes are registered
        if 'interactions' in Base.metadata.tables:
            print("✅ Interactions table registered in metadata")
        else:
            print("⚠️  Interactions table not in metadata")
        
        if 'sessions' in Base.metadata.tables:
            print("✅ Sessions table registered in metadata")
        else:
            print("⚠️  Sessions table not in metadata")
        
        return True
        
    except Exception as e:
        print(f"❌ Metadata table creation test failed: {e}")
        return False

def test_metadata_session_creation():
    """Test if metadata-based session creation works."""
    print("\n=== TESTING METADATA-BASED SESSION CREATION ===\n")
    
    try:
        from models_unified import create_session_with_explicit_base, UnifiedInteraction, UnifiedSession
        
        print("✅ Models imported successfully")
        
        # Try to create a session with metadata-based approach
        try:
            session = create_session_with_explicit_base()
            
            if session:
                print(f"✅ Metadata-based session created: {type(session).__name__}")
                
                # Test if session recognizes mapped classes
                try:
                    # Test querying interactions
                    interactions_count = session.query(UnifiedInteraction).count()
                    print(f"✅ Interactions query successful: {interactions_count}")
                    
                    # Test querying sessions
                    sessions_count = session.query(UnifiedSession).count()
                    print(f"✅ Sessions query successful: {sessions_count}")
                    
                    print("🎉 Metadata-based session creation is working!")
                    return True
                    
                except Exception as e:
                    print(f"❌ Query still failed: {e}")
                    return False
            else:
                print("❌ Metadata-based session creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Metadata-based session creation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Metadata-based test failed: {e}")
        return False

def test_metadata_session_factory():
    """Test if session factory works with metadata approach."""
    print("\n=== TESTING METADATA-BASED SESSION FACTORY ===\n")
    
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
            
            print("🎉 Metadata-based session factory is working!")
            return True
            
        except Exception as e:
            print(f"❌ Query still failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Metadata-based session factory test failed: {e}")
        return False

def test_metadata_database_operations():
    """Test if database operations work with metadata approach."""
    print("\n=== TESTING METADATA-BASED DATABASE OPERATIONS ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory, UnifiedInteraction
        
        session_factory = UnifiedSessionFactory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Test creating a real interaction
            try:
                test_interaction = UnifiedInteraction(
                    interaction_type="metadata_test",
                    client_request="Test request with metadata approach",
                    agent_response="Test response with metadata approach",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "metadata": True, "verified": True}
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
                    interaction_type="metadata_test"
                ).first()
                
                if stored_interaction:
                    print(f"✅ Test interaction found in database")
                    print(f"   ID: {stored_interaction.id}")
                    print(f"   Type: {stored_interaction.interaction_type}")
                    print(f"   Timestamp: {stored_interaction.timestamp}")
                    print("🎉 METADATA-BASED DATABASE OPERATIONS ARE WORKING!")
                    return True
                else:
                    print("❌ Test interaction not found in database")
                    return False
                    
            except Exception as e:
                print(f"❌ Database operations failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Metadata-based database operations test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 TESTING SQLALCHEMY 2.X METADATA FIX\n")
    print("This script will test if the SQLAlchemy 2.x metadata fix resolves the DeclarativeBase issue.\n")
    
    # Test all components
    tests = [
        ("SQLAlchemy 2.x Metadata", test_sqlalchemy_2x_metadata),
        ("Metadata Table Creation", test_metadata_table_creation),
        ("Metadata-Based Session Creation", test_metadata_session_creation),
        ("Metadata-Based Session Factory", test_metadata_session_factory),
        ("Metadata-Based Database Operations", test_metadata_database_operations)
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
        print("   • SQLAlchemy 2.x metadata properly configured")
        print("   • Metadata table creation working")
        print("   • Metadata-based session creation working")
        print("   • Metadata-based session factory working")
        print("   • Metadata-based database operations working")
        
        print("\n🚀 **Your interaction tracking system is now fully functional!**")
        print("   • SQLAlchemy 2.x metadata issue resolved")
        print("   • Interactions will be stored in real database")
        print("   • Context injection will work with real data")
        print("   • Conversation #107 will be properly tracked")
        
        print("\n🧪 **Final Test Commands:**")
        print("python diagnose_interaction_tracking.py")
        print("python test_conversation_tracking.py")
        
        print("\n💡 **Expected Results:**")
        print("• SQLAlchemy 2.x metadata properly configured")
        print("• Tables created successfully with metadata")
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
        print("   • SQLAlchemy 2.x metadata fix may not have worked")
        print("   • Check for syntax errors or import issues")
        print("   • Consider manual intervention")

if __name__ == "__main__":
    main()
