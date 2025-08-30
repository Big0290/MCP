#!/usr/bin/env python3
"""
Test ORM Mapping Fix

This script tests if the ORM mapping fix worked and the classes
are now properly mapped to the database.
"""

import sys
from datetime import datetime

def test_orm_mapping():
    """Test if the ORM mapping is working."""
    print("=== TESTING ORM MAPPING ===\n")
    
    try:
        # Clear any cached imports
        if 'models_unified' in sys.modules:
            del sys.modules['models_unified']
        
        print("✅ Cleared cached imports")
        
        # Import the fixed version
        from models_unified import UnifiedInteraction, UnifiedSession, SQLALCHEMY_AVAILABLE, Base
        
        print(f"✅ Models imported successfully")
        print(f"   SQLAlchemy available: {SQLALCHEMY_AVAILABLE}")
        print(f"   Base class: {Base}")
        
        if SQLALCHEMY_AVAILABLE and Base:
            print("✅ SQLAlchemy ORM is available")
            
            # Check if classes have table mapping
            if hasattr(UnifiedInteraction, '__tablename__'):
                print(f"   ✅ UnifiedInteraction mapped to table: {UnifiedInteraction.__tablename__}")
            else:
                print("   ❌ UnifiedInteraction not mapped to table")
                return False
                
            if hasattr(UnifiedSession, '__tablename__'):
                print(f"   ✅ UnifiedSession mapped to table: {UnifiedSession.__tablename__}")
            else:
                print("   ❌ UnifiedSession not mapped to table")
                return False
                
            return True
        else:
            print("❌ SQLAlchemy ORM not available")
            return False
                
    except Exception as e:
        print(f"❌ ORM mapping test failed: {e}")
        return False

def test_database_session_creation():
    """Test if database sessions can be created with mapped classes."""
    print("\n=== TESTING DATABASE SESSION CREATION ===\n")
    
    try:
        from models_unified import get_session_factory, UnifiedInteraction, UnifiedSession
        
        session_factory = get_session_factory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Check if we can query the mapped classes
            try:
                # Test querying interactions
                interactions_count = session.query(UnifiedInteraction).count()
                print(f"✅ Interactions query successful: {interactions_count}")
                
                # Test querying sessions
                sessions_count = session.query(UnifiedSession).count()
                print(f"✅ Sessions query successful: {sessions_count}")
                
                return True
                
            except Exception as e:
                print(f"❌ Query failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Database session creation test failed: {e}")
        return False

def test_database_operations():
    """Test if database operations work with mapped classes."""
    print("\n=== TESTING DATABASE OPERATIONS ===\n")
    
    try:
        from models_unified import get_session_factory, UnifiedInteraction
        
        session_factory = get_session_factory()
        print("✅ Session factory retrieved")
        
        with session_factory() as session:
            print(f"✅ Session active: {type(session).__name__}")
            
            # Test creating a real interaction
            try:
                test_interaction = UnifiedInteraction(
                    interaction_type="orm_mapping_test",
                    client_request="Test request after ORM mapping fix",
                    agent_response="Test response after ORM mapping fix",
                    timestamp=datetime.now(),
                    status="success",
                    metadata={"test": True, "orm_mapped": True, "verified": True}
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
                    interaction_type="orm_mapping_test"
                ).first()
                
                if stored_interaction:
                    print(f"✅ Test interaction found in database")
                    print(f"   ID: {stored_interaction.id}")
                    print(f"   Type: {stored_interaction.interaction_type}")
                    print(f"   Timestamp: {stored_interaction.timestamp}")
                    print("🎉 ORM MAPPING IS WORKING!")
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

def test_interaction_logging():
    """Test if interaction logging works with mapped classes."""
    print("\n=== TESTING INTERACTION LOGGING ===\n")
    
    try:
        from interaction_logger import InteractionLogger
        
        logger = InteractionLogger()
        print("✅ InteractionLogger created")
        
        # Test logging a real interaction
        print("🔄 Testing interaction logging...")
        result = logger.log_interaction(
            interaction_type="logger_orm_test",
            client_request="Test request with ORM mapped classes",
            agent_response="Test response with ORM mapped classes",
            status="success",
            metadata={"test": True, "orm_mapped": True, "logger_test": True}
        )
        
        if result:
            print("✅ Interaction logged successfully")
            
            # Verify it's in the database
            try:
                from models_unified import get_session_factory, UnifiedInteraction
                
                session_factory = get_session_factory()
                with session_factory() as session:
                    count = session.query(UnifiedInteraction).count()
                    print(f"   Total interactions in database: {count}")
                    
                    if count > 0:
                        print("✅ Interactions are now being stored in real database!")
                        
                        # Show the real interaction
                        real_interaction = session.query(UnifiedInteraction).filter_by(
                            interaction_type="logger_orm_test"
                        ).first()
                        
                        if real_interaction:
                            print(f"   Real interaction ID: {real_interaction.id}")
                            print(f"   Real interaction timestamp: {real_interaction.timestamp}")
                            print("🎉 INTERACTION LOGGING WITH ORM IS WORKING!")
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
    print("🧪 TESTING ORM MAPPING FIX\n")
    print("This script will test if the ORM mapping fix worked.\n")
    
    # Test all components
    tests = [
        ("ORM Mapping", test_orm_mapping),
        ("Database Session Creation", test_database_session_creation),
        ("Database Operations", test_database_operations),
        ("Interaction Logging", test_interaction_logging)
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
        print("   • ORM mapping working")
        print("   • Database sessions working")
        print("   • Database operations working")
        print("   • Interaction logging working")
        
        print("\n🚀 **Your interaction tracking system is now fully functional!**")
        print("   • Interactions will be stored in real database")
        print("   • Context injection will work with real data")
        print("   • Conversation #107 will be properly tracked")
        
        print("\n🧪 **Test Commands:**")
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
        print("   • ORM mapping fix may not have worked")
        print("   • Check for syntax errors or import issues")
        print("   • Consider manual intervention")

if __name__ == "__main__":
    main()
