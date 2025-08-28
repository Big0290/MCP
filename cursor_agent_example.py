#!/usr/bin/env python3
"""
Example Cursor Agent with Automatic Context Enhancement
Shows how to integrate the enhanced pipeline with your Cursor agent
"""

from cursor_agent_integration import enhance_message_for_cursor, get_cursor_context

class EnhancedCursorAgent:
    """
    Example Cursor agent that automatically enhances every user message
    with context before processing
    """
    
    def __init__(self):
        self.name = "Enhanced Cursor Agent"
        self.version = "1.0.0"
        self.context_enabled = True
    
    def process_user_message(self, user_message: str) -> str:
        """
        Process a user message with automatic context enhancement
        
        This is what gets called for every message in Cursor
        """
        print(f"🤖 {self.name} processing message...")
        
        if self.context_enabled:
            # Step 1: Automatically enhance the message with context
            enhanced_message = enhance_message_for_cursor(user_message)
            
            print(f"📝 Original message: {user_message[:100]}...")
            print(f"🚀 Enhanced message: {enhanced_message[:200]}...")
            
            # Step 2: Process the enhanced message (this would go to your AI)
            ai_response = self._send_to_ai(enhanced_message)
            
            # Step 3: Return the AI response
            return ai_response
        else:
            # Fallback to direct processing without context
            return self._send_to_ai(user_message)
    
    def _send_to_ai(self, message: str) -> str:
        """
        Send message to AI (this is where you'd integrate with your AI service)
        
        In a real implementation, this would:
        1. Send the enhanced message to your AI assistant
        2. Get the AI response
        3. Return the response
        """
        # For demonstration, we'll simulate an AI response
        if "deploy" in message.lower():
            return "🚀 Based on your enhanced context, here's how to deploy your application..."
        elif "database" in message.lower():
            return "🗄️ Considering your tech stack and preferences, here's the database configuration..."
        else:
            return "💡 I've processed your enhanced message with full context. How can I help you further?"
    
    def get_status(self) -> dict:
        """Get current agent status and context information"""
        context_info = get_cursor_context()
        return {
            'agent_name': self.name,
            'version': self.version,
            'context_enabled': self.context_enabled,
            'context_cache_size': context_info['context_cache_size'],
            'conversation_history_length': context_info['conversation_history_length']
        }

# Example usage in Cursor
def main():
    """Example of how to use the enhanced Cursor agent"""
    
    # Initialize the enhanced agent
    agent = EnhancedCursorAgent()
    
    print("🚀 Enhanced Cursor Agent Example")
    print("=" * 50)
    
    # Example 1: Simple message
    print("\n📝 Example 1: Simple message")
    response1 = agent.process_user_message("How do I deploy this?")
    print(f"🤖 Response: {response1}")
    
    # Example 2: Database question
    print("\n📝 Example 2: Database question")
    response2 = agent.process_user_message("What database should I use?")
    print(f"🤖 Response: {response2}")
    
    # Example 3: General question
    print("\n📝 Example 3: General question")
    response3 = agent.process_user_message("What's next for our project?")
    print(f"🤖 Response: {response3}")
    
    # Show agent status
    print("\n📊 Agent Status:")
    status = agent.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n✅ Enhanced Cursor Agent example completed!")
    print("\n🎯 To use in your actual Cursor agent:")
    print("   1. Import cursor_agent_integration")
    print("   2. Call enhance_message_for_cursor() for every message")
    print("   3. Send enhanced prompts to your AI service")
    print("   4. Enjoy automatic context injection! 🚀")

if __name__ == "__main__":
    main()
