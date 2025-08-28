#!/usr/bin/env python3
"""
Cursor Integration Example Usage
Show how to use enhanced prompts in your Cursor agent
"""

from cursor_config import (
    enhance_cursor_message,
    get_cursor_status,
    toggle_auto_enhancement,
    get_enhancement_stats
)

def demonstrate_cursor_integration():
    """Demonstrate the Cursor integration in action"""
    
    print("🚀 Cursor Integration Demo")
    print("=" * 40)
    
    # Example 1: Basic message enhancement
    print("\n📝 Example 1: Basic Message Enhancement")
    user_message = "How do I implement user authentication?"
    enhanced_message = enhance_cursor_message(user_message)
    
    print(f"Original: {user_message}")
    print(f"Enhanced: {len(enhanced_message)} characters")
    print(f"Contains context: {'Context Injection' in enhanced_message}")
    
    # Example 2: Code assistance
    print("\n💻 Example 2: Code Assistance")
    code_question = "What's the best way to structure my database models?"
    enhanced_code_question = enhance_cursor_message(code_question)
    
    print(f"Code question: {code_question}")
    print(f"Enhanced: {len(enhanced_code_question)} characters")
    
    # Example 3: Project planning
    print("\n🎯 Example 3: Project Planning")
    planning_question = "What should I focus on next in my project?"
    enhanced_planning = enhance_cursor_message(planning_question)
    
    print(f"Planning question: {planning_question}")
    print(f"Enhanced: {len(enhanced_planning)} characters")
    
    # Show current status
    print("\n📊 Current Integration Status")
    status = get_cursor_status()
    print(f"Status: {status['status']}")
    print(f"Auto-enhance: {status['auto_enhance']}")
    print(f"Cache size: {status['cache_size']}")
    print(f"History length: {status['history_length']}")
    
    # Show enhancement statistics
    print("\n📈 Enhancement Statistics")
    stats = get_enhancement_stats()
    print(f"Total enhanced: {stats['total_enhanced']}")
    print(f"Successful: {stats['successful_enhancements']}")
    print(f"Failed: {stats['failed_enhancements']}")
    print(f"Last enhancement: {stats['last_enhancement']}")
    
    return {
        'original_messages': [user_message, code_question, planning_question],
        'enhanced_messages': [enhanced_message, enhanced_code_question, enhanced_planning],
        'status': status,
        'stats': stats
    }

def show_ai_integration_example():
    """Show how to integrate with AI services"""
    
    print("\n🤖 AI Integration Example")
    print("=" * 40)
    
    # Simulate AI service integration
    def simulate_ai_service(enhanced_prompt: str) -> str:
        """Simulate sending enhanced prompt to AI service"""
        return f"AI Response: I understand your enhanced request with {len(enhanced_prompt)} characters of context. Here's my response..."
    
    # Example usage
    user_question = "How do I optimize my database queries?"
    enhanced_question = enhance_cursor_message(user_question)
    
    print(f"User question: {user_question}")
    print(f"Enhanced prompt: {len(enhanced_question)} characters")
    
    # Send to AI (replace with your actual AI service)
    ai_response = simulate_ai_service(enhanced_question)
    print(f"AI response: {ai_response}")
    
    return {
        'user_question': user_question,
        'enhanced_question': enhanced_question,
        'ai_response': ai_response
    }

def demonstrate_control_functions():
    """Demonstrate control functions"""
    
    print("\n🎛️ Control Functions Demo")
    print("=" * 40)
    
    # Toggle auto-enhancement
    print("Current auto-enhancement status:")
    current_status = get_cursor_status()['auto_enhance']
    print(f"Auto-enhance: {current_status}")
    
    # Toggle it
    new_status = toggle_auto_enhancement()
    print(f"Toggled to: {new_status}")
    
    # Toggle back
    final_status = toggle_auto_enhancement()
    print(f"Toggled back to: {final_status}")
    
    return {
        'initial_status': current_status,
        'toggled_status': new_status,
        'final_status': final_status
    }

if __name__ == "__main__":
    print("🎯 Cursor Integration Example Usage")
    print("=" * 50)
    
    # Run all demonstrations
    demo_results = demonstrate_cursor_integration()
    ai_results = show_ai_integration_example()
    control_results = demonstrate_control_functions()
    
    print("\n✅ Demo completed successfully!")
    print("\n🎯 Key Takeaways:")
    print("   1. Every message gets automatically enhanced with context")
    print("   2. Enhanced prompts are much longer and more informative")
    print("   3. AI services get full context without manual work")
    print("   4. You can control enhancement behavior")
    print("   5. Everything is tracked and monitored")
    
    print("\n📖 Next Steps:")
    print("   1. Import cursor_config in your Cursor agent")
    print("   2. Use enhance_cursor_message() for every user input")
    print("   3. Send enhanced prompts to your AI service")
    print("   4. Enjoy automatic context injection! 🚀")
