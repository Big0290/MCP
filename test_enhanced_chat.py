#!/usr/bin/env python3
"""
Test script for the enhanced_chat function
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_chat():
    """Test the enhanced_chat function directly"""
    try:
        # Import the function
        from local_mcp_server_simple import enhanced_chat
        
        print("🧪 Testing enhanced_chat function...")
        
        # Test with a simple message
        test_message = "Hello, this is a test!"
        result = enhanced_chat(test_message)
        
        print(f"✅ Test successful!")
        print(f"📝 Input: {test_message}")
        print(f"🚀 Output length: {len(result)} characters")
        print(f"✨ Contains enhanced context: {'ENHANCED CONTEXT' in result}")
        
        # Show first 200 characters of output
        print(f"\n📄 Output preview:")
        print(result[:200] + "..." if len(result) > 200 else result)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhanced_chat()
    sys.exit(0 if success else 1)
