#!/usr/bin/env python3
"""
Test Import Change

This script tests that the import change from main.enhanced_chat to 
enhanced_chat_integration.enhanced_chat works correctly.
"""

def test_import_change():
    """Test that the enhanced chat integration import works."""
    print("=== Testing Import Change ===")
    
    try:
        # Test the new import
        print("1. Testing enhanced_chat_integration import...")
        from enhanced_chat_integration import enhanced_chat
        
        print("✅ Successfully imported enhanced_chat from enhanced_chat_integration")
        
        # Test basic functionality
        print("\n2. Testing basic functionality...")
        test_message = "Hello, this is a test message"
        response = enhanced_chat(test_message)
        
        if isinstance(response, str):
            print(f"✅ Backward compatible response: {len(response)} characters")
            print(f"   Preview: {response[:100]}...")
        elif isinstance(response, dict):
            print(f"✅ Enhanced response: {response.get('status', 'unknown')}")
            print(f"   Original response: {len(response.get('original_response', ''))} characters")
            print(f"   Enhancement ratio: {response.get('performance_metrics', {}).get('enhancement_ratio', 0):.2f}x")
        else:
            print(f"⚠️ Unexpected response type: {type(response)}")
        
        # Test semantic insights
        print("\n3. Testing semantic insights...")
        from enhanced_chat_integration import get_semantic_insights_quick
        
        insights = get_semantic_insights_quick(test_message)
        print(f"✅ Semantic insights: {insights.get('status', 'unknown')}")
        
        # Test context analysis
        print("\n4. Testing context analysis...")
        from enhanced_chat_integration import get_context_analysis_quick
        
        context = get_context_analysis_quick(test_message)
        if 'error' not in context:
            print(f"✅ Context analysis successful")
        else:
            print(f"⚠️ Context analysis: {context.get('error', 'Unknown error')}")
        
        # Test integration status
        print("\n5. Testing integration status...")
        from enhanced_chat_integration import get_enhanced_chat_status
        
        status = get_enhanced_chat_status()
        print(f"✅ Integration status: {status['integration_status']}")
        print(f"   Semantic enhancement: {status['semantic_enhancement_enabled']}")
        print(f"   Bridge available: {status['bridge_available']}")
        print(f"   Enhanced tools available: {status['enhanced_tools_available']}")
        
        print("\n🎉 All tests passed! Import change successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Make sure enhanced_chat_integration.py exists and is properly configured")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Check the error details above")
        return False

def test_original_function():
    """Test that the original enhanced_chat function still works."""
    print("\n=== Testing Original Function ===")
    
    try:
        # Test the original import
        print("1. Testing original enhanced_chat import...")
        from main import enhanced_chat as original_enhanced_chat
        
        print("✅ Successfully imported original enhanced_chat from main")
        
        # Test basic functionality
        print("\n2. Testing original functionality...")
        test_message = "Hello, this is a test message"
        response = original_enhanced_chat(test_message)
        
        print(f"✅ Original function response: {len(response)} characters")
        print(f"   Preview: {response[:100]}...")
        
        print("\n🎉 Original function test passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Original import failed: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Original function test failed: {e}")
        return False

def test_both_functions():
    """Test that both functions work and can be used together."""
    print("\n=== Testing Both Functions Together ===")
    
    try:
        # Import both functions
        from main import enhanced_chat as original_enhanced_chat
        from enhanced_chat_integration import enhanced_chat as enhanced_enhanced_chat
        
        print("✅ Successfully imported both functions")
        
        # Test both with the same message
        test_message = "Compare the responses from both functions"
        
        print(f"\n1. Testing original function...")
        original_response = original_enhanced_chat(test_message)
        print(f"   Original response: {len(original_response)} characters")
        
        print(f"\n2. Testing enhanced function...")
        enhanced_response = enhanced_enhanced_chat(test_message)
        
        if isinstance(enhanced_response, str):
            print(f"   Enhanced response: {len(enhanced_response)} characters")
        elif isinstance(enhanced_response, dict):
            print(f"   Enhanced response: {enhanced_response.get('status', 'unknown')}")
            print(f"   Enhancement ratio: {enhanced_response.get('performance_metrics', {}).get('enhancement_ratio', 0):.2f}x")
        
        print("\n🎉 Both functions work together!")
        return True
        
    except Exception as e:
        print(f"❌ Both functions test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Testing Import Change for Enhanced Chat Integration\n")
    
    # Test the new import
    new_import_success = test_import_change()
    
    # Test the original function
    original_success = test_original_function()
    
    # Test both together
    both_success = test_both_functions()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    print(f"✅ New Import (enhanced_chat_integration): {'PASSED' if new_import_success else 'FAILED'}")
    print(f"✅ Original Import (main): {'PASSED' if original_success else 'FAILED'}")
    print(f"✅ Both Functions Together: {'PASSED' if both_success else 'FAILED'}")
    
    if new_import_success and original_success and both_success:
        print("\n🎉 All tests passed! Your import change is working perfectly!")
        print("\n🔗 **Next Steps:**")
        print("   1. ✅ Import change successful")
        print("   2. ✅ Both functions work")
        print("   3. ✅ Enhanced features available")
        print("   4. 🚀 Enjoy semantic enhancement!")
        
    elif new_import_success:
        print("\n⚠️ Partial success - new import works but original has issues")
        print("💡 This might be expected if you're transitioning to the new system")
        
    else:
        print("\n❌ Import change failed")
        print("💡 Check the error messages above and ensure all dependencies are installed")
        
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
