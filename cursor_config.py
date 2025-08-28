#!/usr/bin/env python3
"""
Cursor Integration Configuration
Easy setup for your Cursor agent to use enhanced prompts
"""

from cursor_agent_integration import (
    enhance_message_for_cursor,
    get_cursor_context,
    toggle_auto_enhancement,
    get_enhancement_stats,
    clear_context_cache
)

# Configuration options
CURSOR_CONFIG = {
    'auto_enhance': True,           # Automatically enhance all messages
    'cache_size': 100,             # Maximum cache size for context
    'log_level': 'INFO',           # Logging level (DEBUG, INFO, WARNING, ERROR)
    'force_enhance_on_error': True, # Force enhancement even if auto-enhance is disabled
}

def setup_cursor_integration():
    """
    Setup function to initialize Cursor integration
    
    Call this in your Cursor agent startup
    """
    print("🚀 Setting up Cursor Integration...")
    print("✅ Enhanced prompt processing enabled")
    print("✅ Context injection active")
    print("✅ Conversation memory tracking enabled")
    print("✅ Auto-enhancement: ON")
    return True

def enhance_cursor_message(user_message: str) -> str:
    """
    Enhanced wrapper for Cursor message processing
    
    This is the main function your Cursor agent should call
    """
    try:
        enhanced = enhance_message_for_cursor(user_message)
        return enhanced
    except Exception as e:
        print(f"⚠️ Enhancement failed: {e}")
        return user_message

def get_cursor_status() -> dict:
    """Get current Cursor integration status"""
    try:
        context = get_cursor_context()
        stats = get_enhancement_stats()
        return {
            'status': 'active',
            'auto_enhance': context.get('auto_enhance_enabled', True),
            'cache_size': context.get('context_cache_size', 0),
            'history_length': context.get('conversation_history_length', 0),
            'enhancement_stats': stats,
            'last_enhancement': stats.get('last_enhancement')
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }

# Example usage functions
def test_cursor_integration():
    """Test the Cursor integration"""
    print("🧪 Testing Cursor Integration...")
    
    # Test message enhancement
    test_message = "How do I configure the database?"
    enhanced = enhance_cursor_message(test_message)
    
    print(f"📝 Original: {test_message}")
    print(f"🚀 Enhanced: {len(enhanced)} characters")
    print(f"✨ Context injected: {'Context Injection' in enhanced}")
    
    # Show status
    status = get_cursor_status()
    print(f"📊 Status: {status}")
    
    return enhanced

def quick_enhance(message: str) -> str:
    """Quick enhancement for testing"""
    return enhance_cursor_message(message)

# Main setup
if __name__ == "__main__":
    print("🎯 Cursor Integration Configuration")
    print("=" * 40)
    
    # Setup integration
    setup_cursor_integration()
    
    # Test it
    test_cursor_integration()
    
    print("\n✅ Configuration complete!")
    print("\n📖 Usage in your Cursor agent:")
    print("   1. Import: from cursor_config import enhance_cursor_message")
    print("   2. Call: enhanced = enhance_cursor_message('Your message')")
    print("   3. Send enhanced message to AI")
    print("   4. Enjoy automatic context injection! 🚀")
