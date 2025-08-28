#!/usr/bin/env python3
"""
Quick Test of Cursor Integration
Run this to see how it works
"""

from cursor_config import enhance_cursor_message

def test_integration():
    print("🧪 Testing Cursor Integration...")
    
    # Test message
    user_message = "How do I deploy this application?"
    print(f"📝 Original message: {user_message}")
    
    # Enhance it
    enhanced_message = enhance_cursor_message(user_message)
    print(f"🚀 Enhanced message: {len(enhanced_message)} characters")
    
    # Show the enhanced message
    print("\n✨ Enhanced Message Preview:")
    print("-" * 50)
    print(enhanced_message[:200] + "..." if len(enhanced_message) > 200 else enhanced_message)
    print("-" * 50)
    
    return enhanced_message

if __name__ == "__main__":
    print("🎯 Cursor Integration Test")
    print("=" * 40)
    
    # Run the test
    enhanced = test_integration()
    
    print(f"\n✅ Test completed!")
    print(f"📊 Enhancement ratio: {len(enhanced)} / {len('How do I deploy this application?')} = {len(enhanced)/len('How do I deploy this application?'):.1f}x")
    
    print("\n🎯 To use in your project:")
    print("   1. Import: from cursor_config import enhance_cursor_message")
    print("   2. Call: enhanced = enhance_cursor_message('Your message')")
    print("   3. Send enhanced message to AI")
    print("   4. Enjoy automatic context injection! 🚀")
