#!/usr/bin/env python3
"""
Cursor Agent Integration Layer
Automatically enhances every user message with context before processing
"""

import json
import sys
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CursorAgentIntegration:
    """
    Integration layer that automatically enhances Cursor agent interactions
    with context from your MCP server
    """
    
    def __init__(self, auto_enhance: bool = True, cache_size: int = 100):
        self.context_cache = {}
        self.conversation_history = []
        self.auto_enhance = auto_enhance
        self.max_cache_size = cache_size
        self.enhancement_stats = {
            'total_enhanced': 0,
            'successful_enhancements': 0,
            'failed_enhancements': 0,
            'last_enhancement': None
        }
        
    def enhance_user_message(self, user_message: str, force_enhance: bool = False) -> str:
        """
        Automatically enhance a user message with full context
        
        This is what gets called by your Cursor agent for every message
        """
        if not self.auto_enhance and not force_enhance:
            logger.info("Auto-enhancement disabled, returning original message")
            return user_message
            
        try:
            # Step 1: Generate enhanced context using your prompt processor
            enhanced_prompt = self._call_prompt_processor(user_message)
            
            # Step 2: Cache the enhanced context for reference
            self._cache_context(user_message, enhanced_prompt)
            
            # Step 3: Add to conversation history
            self._add_to_history(user_message, enhanced_prompt)
            
            # Step 4: Update statistics
            self.enhancement_stats['total_enhanced'] += 1
            self.enhancement_stats['successful_enhancements'] += 1
            self.enhancement_stats['last_enhancement'] = datetime.utcnow().isoformat()
            
            logger.info(f"✅ Successfully enhanced message: {len(user_message)} -> {len(enhanced_prompt)} chars")
            
            # Step 5: Return the enhanced prompt for the AI to process
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"⚠️ Context enhancement failed: {e}")
            self.enhancement_stats['failed_enhancements'] += 1
            # Fallback to original message if enhancement fails
            return user_message
    
    def _call_prompt_processor(self, user_message: str) -> str:
        """Call your MCP prompt processor to generate enhanced context"""
        try:
            # Import your prompt processor functions
            from local_mcp_server_simple import (
                _generate_conversation_summary,
                _extract_action_history,
                _get_tech_stack_definition,
                _get_project_plans,
                _get_user_preferences,
                _get_agent_metadata,
                _build_enhanced_prompt
            )
            
            # Get recent interactions from database
            from models_local import get_session_factory, AgentInteraction
            
            with get_session_factory()() as db_session:
                recent_interactions = db_session.query(AgentInteraction).order_by(
                    AgentInteraction.timestamp.desc()
                ).limit(20).all()
            
            # Generate context components
            conversation_summary = _generate_conversation_summary(recent_interactions)
            action_history = _extract_action_history(recent_interactions)
            tech_stack = _get_tech_stack_definition()
            project_plans = _get_project_plans()
            user_preferences = _get_user_preferences()
            agent_metadata = _get_agent_metadata()
            
            # Build enhanced prompt
            enhanced_prompt = _build_enhanced_prompt(
                user_message=user_message,
                conversation_summary=conversation_summary,
                action_history=action_history,
                tech_stack=tech_stack,
                project_plans=project_plans,
                user_preferences=user_preferences,
                agent_metadata=agent_metadata
            )
            
            return enhanced_prompt
            
        except ImportError as e:
            logger.warning(f"⚠️ Import error in prompt processor: {e}")
            # Fallback to basic enhancement
            return self._create_basic_enhanced_prompt(user_message)
        except Exception as e:
            logger.error(f"⚠️ Prompt processor failed: {e}")
            # Fallback to basic enhancement
            return self._create_basic_enhanced_prompt(user_message)
    
    def _create_basic_enhanced_prompt(self, user_message: str) -> str:
        """Create a basic enhanced prompt when full processor is unavailable"""
        basic_context = f"""
=== BASIC ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== CONTEXT INJECTION ===

BASIC CONTEXT:
- This message is being processed by your Cursor integration
- Full context enhancement is temporarily unavailable
- Basic enhancement applied for continuity

=== INSTRUCTIONS ===
Please respond to the user's message above, taking into account:
1. This is a Cursor agent interaction
2. Context enhancement is being applied
3. Provide helpful, context-aware assistance

=== END BASIC ENHANCED PROMPT ===
"""
        return basic_context.strip()
    
    def _cache_context(self, user_message: str, enhanced_prompt: str):
        """Cache the enhanced context with size management"""
        self.context_cache[user_message] = enhanced_prompt
        
        # Manage cache size
        if len(self.context_cache) > self.max_cache_size:
            # Remove oldest entries
            oldest_key = next(iter(self.context_cache))
            del self.context_cache[oldest_key]
    
    def _add_to_history(self, user_message: str, enhanced_prompt: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'user_message': user_message,
            'enhanced_prompt': enhanced_prompt,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Keep history manageable
        if len(self.conversation_history) > self.max_cache_size:
            self.conversation_history = self.conversation_history[-self.max_cache_size:]
    
    def get_conversation_context(self) -> Dict[str, Any]:
        """Get current conversation context for debugging"""
        return {
            'context_cache_size': len(self.context_cache),
            'conversation_history_length': len(self.conversation_history),
            'recent_messages': self.conversation_history[-5:] if self.conversation_history else [],
            'cache_keys': list(self.context_cache.keys()),
            'enhancement_stats': self.enhancement_stats,
            'auto_enhance_enabled': self.auto_enhance
        }
    
    def toggle_auto_enhancement(self) -> bool:
        """Toggle automatic enhancement on/off"""
        self.auto_enhance = not self.auto_enhance
        logger.info(f"Auto-enhancement {'enabled' if self.auto_enhance else 'disabled'}")
        return self.auto_enhance
    
    def clear_cache(self):
        """Clear the context cache"""
        self.context_cache.clear()
        logger.info("Context cache cleared")
    
    def get_enhancement_stats(self) -> Dict[str, Any]:
        """Get enhancement statistics"""
        return self.enhancement_stats.copy()

# Global instance for Cursor to use
cursor_integration = CursorAgentIntegration()

def enhance_message_for_cursor(user_message: str, force_enhance: bool = False) -> str:
    """
    Main function that Cursor agent calls to enhance messages
    
    Usage in Cursor:
    - Every user message automatically gets enhanced
    - Enhanced context is injected before AI processing
    - Full conversation history is maintained
    
    Args:
        user_message (str): The original user message
        force_enhance (bool): Force enhancement even if auto-enhance is disabled
    
    Returns:
        str: Enhanced message with full context
    """
    return cursor_integration.enhance_user_message(user_message, force_enhance)

def get_cursor_context() -> Dict[str, Any]:
    """Get current Cursor integration context"""
    return cursor_integration.get_conversation_context()

def toggle_auto_enhancement() -> bool:
    """Toggle automatic enhancement on/off"""
    return cursor_integration.toggle_auto_enhancement()

def get_enhancement_stats() -> Dict[str, Any]:
    """Get enhancement statistics"""
    return cursor_integration.get_enhancement_stats()

def clear_context_cache():
    """Clear the context cache"""
    cursor_integration.clear_cache()

# Example usage for testing
if __name__ == "__main__":
    print("🧪 Testing Cursor Agent Integration...")
    
    # Test message enhancement
    test_message = "How do I deploy this application?"
    enhanced = enhance_message_for_cursor(test_message)
    
    print(f"📝 Original message: {test_message}")
    print(f"🚀 Enhanced message length: {len(enhanced)} characters")
    print(f"✨ Contains context: {'Context Injection' in enhanced}")
    
    # Show context info
    context = get_cursor_context()
    print(f"📊 Context cache size: {context['context_cache_size']}")
    print(f"🔄 Conversation history: {context['conversation_history_length']} messages")
    print(f"📈 Enhancement stats: {context['enhancement_stats']}")
    
    print("\n✅ Cursor integration test completed!")
    print("\n🎯 To use in Cursor:")
    print("   1. Import this module in your Cursor agent")
    print("   2. Call enhance_message_for_cursor() for every user message")
    print("   3. Send enhanced prompts to AI instead of original messages")
    print("   4. Enjoy automatic context injection! 🚀")
    print("\n🔧 Available functions:")
    print("   - enhance_message_for_cursor(user_message)")
    print("   - get_cursor_context()")
    print("   - toggle_auto_enhancement()")
    print("   - get_enhancement_stats()")
    print("   - clear_context_cache()")
