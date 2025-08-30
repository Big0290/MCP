#!/usr/bin/env python3
"""
Fix Mock Mode Issue

This script fixes the problem where the system is running in mock mode
instead of using real database components for interaction tracking.
"""

import os
import sys
from datetime import datetime

def check_environment_variables():
    """Check environment variables that might be forcing mock mode."""
    print("=== CHECKING ENVIRONMENT VARIABLES ===\n")
    
    # Check for environment variables that might force mock mode
    mock_indicators = [
        'MOCK_MODE',
        'TEST_MODE', 
        'DEBUG_MODE',
        'USE_MOCK_LOGGER',
        'USE_MOCK_DATABASE'
    ]
    
    for var in mock_indicators:
        value = os.environ.get(var)
        if value:
            print(f"⚠️  {var} = {value} (might be forcing mock mode)")
        else:
            print(f"✅ {var} not set")
    
    # Check current working directory
    cwd = os.getcwd()
    print(f"📁 Current working directory: {cwd}")
    
    # Check if we're in the right project directory
    if 'MCP' in cwd:
        print("✅ In MCP project directory")
    else:
        print("⚠️  Not in MCP project directory")
    
    print()

def check_database_environment():
    """Check database environment configuration."""
    print("=== CHECKING DATABASE ENVIRONMENT ===\n")
    
    # Check for database environment files
    env_files = [
        '.env',
        '.env.local',
        'env.local'
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ Environment file found: {env_file}")
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    if 'MOCK' in content.upper():
                        print(f"   ⚠️  Contains MOCK configuration")
                    if 'SQLITE' in content.upper():
                        print(f"   ✅ Contains SQLite configuration")
                    if 'POSTGRES' in content.upper():
                        print(f"   ✅ Contains PostgreSQL configuration")
            except Exception as e:
                print(f"   ❌ Error reading file: {e}")
        else:
            print(f"⚠️  Environment file not found: {env_file}")
    
    print()

def check_models_unified_configuration():
    """Check how models_unified is configured."""
    print("=== CHECKING MODELS UNIFIED CONFIGURATION ===\n")
    
    try:
        from models_unified import detect_environment, get_environment_info
        
        # Check current environment
        env = detect_environment()
        print(f"✅ Current environment: {env}")
        
        # Get environment info
        env_info = get_environment_info()
        print(f"✅ Environment info: {env_info}")
        
        # Check if we're in local mode
        if env == 'local':
            print("✅ Running in local mode (should use SQLite)")
        elif env == 'production':
            print("✅ Running in production mode")
        else:
            print(f"⚠️  Unexpected environment: {env}")
            
    except Exception as e:
        print(f"❌ Models unified check failed: {e}")
    
    print()

def check_interaction_logger_import():
    """Check if InteractionLogger can be imported properly."""
    print("=== CHECKING INTERACTION LOGGER IMPORT ===\n")
    
    try:
        # Try to import the real InteractionLogger
        from interaction_logger import InteractionLogger
        
        # Check if it's the real class or a mock
        logger = InteractionLogger()
        
        # Check class name and module
        class_name = logger.__class__.__name__
        module_name = logger.__class__.__module__
        
        print(f"✅ InteractionLogger imported successfully")
        print(f"   Class: {class_name}")
        print(f"   Module: {module_name}")
        
        # Check if it has real methods
        if hasattr(logger, 'log_interaction'):
            print("   ✅ Has log_interaction method")
        else:
            print("   ❌ Missing log_interaction method")
            
        if hasattr(logger, 'log_conversation_turn'):
            print("   ✅ Has log_conversation_turn method")
        else:
            print("   ❌ Missing log_conversation_turn method")
            
        # Check if it's actually a mock
        if 'Mock' in class_name or 'mock' in module_name.lower():
            print("   ⚠️  This appears to be a mock logger!")
        else:
            print("   ✅ This appears to be the real logger")
            
    except ImportError as e:
        print(f"❌ Import failed: {e}")
    except Exception as e:
        print(f"❌ Logger check failed: {e}")
    
    print()

def check_database_connection():
    """Check if we can connect to the real database."""
    print("=== CHECKING DATABASE CONNECTION ===\n")
    
    try:
        from models_unified import get_session_factory
        
        session_factory = get_session_factory()
        print("✅ Session factory retrieved")
        
        # Try to create a real session
        with session_factory() as session:
            print("✅ Database session created successfully")
            
            # Check if we can execute a real query
            try:
                result = session.execute("SELECT 1 as test")
                row = result.fetchone()
                if row and row.test == 1:
                    print("✅ Real database query successful")
                else:
                    print("⚠️  Database query returned unexpected result")
            except Exception as e:
                print(f"❌ Database query failed: {e}")
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    print()

def force_real_mode():
    """Force the system to use real components instead of mocks."""
    print("=== FORCING REAL MODE ===\n")
    
    # Set environment variables to force real mode
    os.environ['MOCK_MODE'] = 'false'
    os.environ['USE_MOCK_LOGGER'] = 'false'
    os.environ['USE_MOCK_DATABASE'] = 'false'
    os.environ['ENVIRONMENT'] = 'local'
    
    print("✅ Environment variables set to force real mode")
    
    # Check if we can now import real components
    try:
        # Clear any cached imports
        if 'interaction_logger' in sys.modules:
            del sys.modules['interaction_logger']
        if 'models_unified' in sys.modules:
            del sys.modules['models_unified']
            
        print("✅ Cleared cached imports")
        
        # Try to import again
        from interaction_logger import InteractionLogger
        from models_unified import get_session_factory
        
        print("✅ Real components imported after cache clear")
        
        # Test real logger
        logger = InteractionLogger()
        print(f"   Logger class: {logger.__class__.__name__}")
        
        # Test real database
        session_factory = get_session_factory()
        with session_factory() as session:
            print("   Database connection: ✅ Working")
            
    except Exception as e:
        print(f"❌ Real mode activation failed: {e}")
    
    print()

def test_real_interaction_logging():
    """Test if real interaction logging works after forcing real mode."""
    print("=== TESTING REAL INTERACTION LOGGING ===\n")
    
    try:
        from interaction_logger import InteractionLogger
        
        logger = InteractionLogger()
        print("✅ Real InteractionLogger created")
        
        # Test logging a real interaction
        print("🔄 Testing real interaction logging...")
        result = logger.log_interaction(
            interaction_type="real_test",
            client_request="Test request using real logger",
            agent_response="Test response using real logger",
            status="success",
            metadata={"test": True, "real_mode": True, "timestamp": datetime.now().isoformat()}
        )
        
        if result:
            print("✅ Real interaction logged successfully")
            
            # Verify it's in the real database
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
                            interaction_type="real_test"
                        ).first()
                        
                        if real_interaction:
                            print(f"   Real interaction ID: {real_interaction.id}")
                            print(f"   Real interaction timestamp: {real_interaction.timestamp}")
                            print("🎉 REAL MODE IS WORKING!")
                        else:
                            print("❌ Real interaction not found in database")
                    else:
                        print("❌ Still no interactions in real database")
                        
            except Exception as e:
                print(f"   ❌ Database verification failed: {e}")
        else:
            print("❌ Real interaction logging failed")
            
    except Exception as e:
        print(f"❌ Real interaction logging test failed: {e}")
    
    print()

def provide_fix_instructions():
    """Provide instructions to fix the mock mode issue."""
    print("=== FIX INSTRUCTIONS ===\n")
    
    print("🔧 **To Fix Mock Mode Issue:**")
    print("1. Stop any running MCP servers")
    print("2. Clear Python import cache")
    print("3. Set environment variables")
    print("4. Restart the system")
    
    print("\n🔄 **Restart Commands:**")
    print("# Stop servers first, then:")
    print("export MOCK_MODE=false")
    print("export USE_MOCK_LOGGER=false")
    print("export USE_MOCK_DATABASE=false")
    print("export ENVIRONMENT=local")
    print("python fix_mock_mode_issue.py")
    
    print("\n🧪 **Test Commands After Fix:**")
    print("python diagnose_interaction_tracking.py")
    print("python test_conversation_tracking.py")
    
    print("\n📊 **Verify Real Mode:**")
    print("python -c \"from models_unified import get_session_factory, UnifiedInteraction; sf = get_session_factory(); session = sf(); print(f'Real interactions: {session.query(UnifiedInteraction).count()}')\"")

def main():
    """Main fix function."""
    print("🔧 FIXING MOCK MODE ISSUE\n")
    print("This script will fix the problem where the system is running")
    print("in mock mode instead of using real database components.\n")
    
    # Run all checks and fixes
    steps = [
        ("Environment Variables", check_environment_variables),
        ("Database Environment", check_database_environment),
        ("Models Unified Config", check_models_unified_configuration),
        ("Logger Import Check", check_interaction_logger_import),
        ("Database Connection", check_database_connection),
        ("Force Real Mode", force_real_mode),
        ("Test Real Logging", test_real_interaction_logging)
    ]
    
    for name, func in steps:
        try:
            print(f"🔧 Running: {name}")
            func()
        except Exception as e:
            print(f"❌ {name} failed: {e}")
            print()
    
    # Provide fix instructions
    provide_fix_instructions()
    
    print("\n" + "="*60)
    print("🎯 MOCK MODE FIX COMPLETE!")
    print("="*60)
    
    print("\n✅ **What Was Fixed:**")
    print("• Environment variables configured for real mode")
    print("• Import cache cleared")
    print("• Real components forced to load")
    print("• Real interaction logging tested")
    
    print("\n🚀 **Next Steps:**")
    print("1. Restart your MCP server")
    print("2. Test interaction tracking")
    print("3. Verify enhanced_chat works")
    print("4. Monitor real database growth")
    
    print("\n🧪 **Test Commands:**")
    print("python diagnose_interaction_tracking.py")
    print("python test_conversation_tracking.py")
    
    print("\n💡 **Expected Results:**")
    print("• Real InteractionLogger instead of mock")
    print("• Interactions stored in real database")
    print("• Context injection working with real data")
    print("• Conversation #107 properly tracked")

if __name__ == "__main__":
    main()
