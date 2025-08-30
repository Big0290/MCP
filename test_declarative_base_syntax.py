#!/usr/bin/env python3
"""
Test DeclarativeBase Syntax Fix

This script tests if the DeclarativeBase syntax fix resolves the
"takes no arguments" error.
"""

def test_declarative_base_import():
    """Test if DeclarativeBase can be imported without syntax errors."""
    print("=== TESTING DECLARATIVEBASE SYNTAX FIX ===\n")
    
    try:
        # Clear any cached imports
        import sys
        if 'models_unified' in sys.modules:
            del sys.modules['models_unified']
        
        print("✅ Cleared cached imports")
        
        # Try to import the fixed version
        from models_unified import SQLALCHEMY_VERSION, SQLALCHEMY_2X, Base
        
        print(f"✅ SQLAlchemy version detected: {SQLALCHEMY_VERSION}")
        print(f"✅ SQLAlchemy 2.x mode: {SQLALCHEMY_2X}")
        print(f"✅ Base class type: {type(Base).__name__}")
        
        # Check if metadata is available
        if hasattr(Base, 'metadata'):
            print(f"✅ Base has metadata: {type(Base.metadata).__name__}")
            return True
        else:
            print("❌ Base does not have metadata attribute")
            return False
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_models_import():
    """Test if basic models can be imported."""
    print("\n=== TESTING BASIC MODELS IMPORT ===\n")
    
    try:
        from models_unified import UnifiedInteraction, UnifiedSession
        
        print("✅ UnifiedInteraction imported successfully")
        print("✅ UnifiedSession imported successfully")
        
        # Check if they have the expected attributes
        if hasattr(UnifiedInteraction, '__tablename__'):
            print(f"✅ UnifiedInteraction has __tablename__: {UnifiedInteraction.__tablename__}")
        else:
            print("⚠️  UnifiedInteraction missing __tablename__")
        
        if hasattr(UnifiedSession, '__tablename__'):
            print(f"✅ UnifiedSession has __tablename__: {UnifiedSession.__tablename__}")
        else:
            print("⚠️  UnifiedSession missing __tablename__")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic models import failed: {e}")
        return False

def test_session_factory_import():
    """Test if session factory can be imported."""
    print("\n=== TESTING SESSION FACTORY IMPORT ===\n")
    
    try:
        from models_unified import UnifiedSessionFactory
        
        print("✅ UnifiedSessionFactory imported successfully")
        
        # Try to create a factory instance
        factory = UnifiedSessionFactory()
        print("✅ Session factory instance created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Session factory import failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 TESTING DECLARATIVEBASE SYNTAX FIX\n")
    print("This script will test if the DeclarativeBase syntax fix resolves the import error.\n")
    
    # Test all components
    tests = [
        ("DeclarativeBase Import", test_declarative_base_import),
        ("Basic Models Import", test_basic_models_import),
        ("Session Factory Import", test_session_factory_import)
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
        print("   • DeclarativeBase syntax error resolved")
        print("   • Basic models importing successfully")
        print("   • Session factory importing successfully")
        
        print("\n🚀 **Your interaction tracking system can now be imported!**")
        print("   • Next step: Test database operations")
        print("   • Run: python test_sqlalchemy_2x_metadata_fix.py")
        
    elif success_count > 0:
        print("\n⚠️  PARTIAL SUCCESS")
        print("   • Some components working, others need attention")
        print("   • Check the output above for specific failures")
        
    else:
        print("\n❌ ALL TESTS FAILED")
        print("   • DeclarativeBase syntax fix may not have worked")
        print("   • Check for syntax errors or import issues")
        print("   • Consider manual intervention")

if __name__ == "__main__":
    main()
