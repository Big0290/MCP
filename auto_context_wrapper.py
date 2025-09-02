#!/usr/bin/env python3
"""
Automated Context Injection System
Seamlessly enhances prompts with context without manual intervention
"""

import sys
import os
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import logging

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutoContextWrapper:
    """
    Automated context injection system that enhances prompts seamlessly
    
    This system automatically:
    1. Intercepts prompt requests
    2. Injects relevant context
    3. Enhances responses with conversation history
    4. Maintains seamless user experience
    """
    
    def __init__(self, auto_enhance: bool = True):
        self.auto_enhance = auto_enhance
        self.context_cache = {}
        self.enhancement_stats = {
            'total_enhanced': 0,
            'successful_enhancements': 0,
            'failed_enhancements': 0,
            'last_enhancement': None,
            'average_enhancement_time': 0.0
        }
        self.enhancement_history = []
        
    def auto_enhance_prompt(self, original_prompt: str, context_type: str = "general") -> str:
        """
        Automatically enhance a prompt with relevant context
        
        Args:
            original_prompt (str): The original user prompt
            context_type (str): Type of context to inject (general, technical, conversation, etc.)
            
        Returns:
            str: Enhanced prompt with injected context
        """
        if not self.auto_enhance:
            return original_prompt
            
        start_time = datetime.now()
        
        try:
            # Step 1: Generate enhanced context
            enhanced_context = self._generate_context_for_prompt(original_prompt, context_type)
            
            # Step 2: Build enhanced prompt
            enhanced_prompt = self._build_enhanced_prompt(original_prompt, enhanced_context)
            
            # Step 3: Update statistics
            self._update_stats(True, start_time)
            
            # Step 4: Cache for future use
            self._cache_enhancement(original_prompt, enhanced_prompt, context_type)
            
            logger.info(f"✅ Auto-enhanced prompt: {len(original_prompt)} -> {len(enhanced_prompt)} chars")
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"❌ Auto-enhancement failed: {str(e)}")
            self._update_stats(False, start_time)
            return original_prompt
    
    def _generate_context_for_prompt(self, prompt: str, context_type: str) -> str:
        """Generate relevant context based on prompt content and type"""
        try:
            # Import context generation functions
            from local_mcp_server_simple import (
                _generate_conversation_summary,
                _extract_action_history,
                _get_tech_stack_definition,
                _get_project_plans,
                _get_user_preferences,
                _get_agent_metadata
            )
            
            # Get recent interactions for context
            from models_unified import get_session_factory, AgentInteraction
            
            # Use local storage for now since database queries aren't working
            from models_unified import get_local_interactions
            recent_interactions = get_local_interactions(20)
            
            # Generate context components based on type
            if context_type == "technical":
                # Focus on tech stack and project plans
                context = f"""
TECH STACK: {_get_tech_stack_definition()}
PROJECT PLANS: {_get_project_plans()}
RECENT ACTIONS: {_extract_action_history(recent_interactions)}
                """.strip()
            elif context_type == "conversation":
                # Focus on conversation history and user preferences
                context = f"""
CONVERSATION SUMMARY: {_generate_conversation_summary(recent_interactions)}
USER PREFERENCES: {_get_user_preferences()}
AGENT METADATA: {_get_agent_metadata()}
                """.strip()
            else:
                # General context with all components
                context = f"""
CONVERSATION SUMMARY: {_generate_conversation_summary(recent_interactions)}
ACTION HISTORY: {_extract_action_history(recent_interactions)}
TECH STACK: {_get_tech_stack_definition()}
PROJECT PLANS: {_get_project_plans()}
USER PREFERENCES: {_get_user_preferences()}
AGENT METADATA: {_get_agent_metadata()}
                """.strip()
            
            return context
            
        except Exception as e:
            logger.error(f"Context generation failed: {str(e)}")
            return f"⚠️ Context generation failed: {str(e)}"
    
    def _build_enhanced_prompt(self, original_prompt: str, enhanced_context: str) -> str:
        """Build the final enhanced prompt with injected context"""
        try:
            # 🚀 NEW: Use optimized prompt generator for clean, efficient prompts
            try:
                from optimized_prompt_generator import OptimizedPromptGenerator
                generator = OptimizedPromptGenerator()
                optimized_prompt = generator.generate_optimized_prompt(
                    user_message=original_prompt,
                    context_type="smart",  # Use smart context selection
                    force_refresh=False
                )
                return optimized_prompt
            except ImportError:
                # Fallback to old prompt generator if optimized not available
                from prompt_generator import prompt_generator
                
                # Generate auto-enhanced prompt with smart context (not comprehensive)
                enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                    user_message=original_prompt,
                    context_type="smart",  # Use smart instead of comprehensive
                    force_refresh=False
                )
                
                return enhanced_prompt
            
        except ImportError:
            # Fallback to original implementation if prompt generator not available
            enhanced_prompt = f"""
=== AUTO-ENHANCED PROMPT ===

USER REQUEST: {original_prompt}

=== INJECTED CONTEXT ===
{enhanced_context}

=== INSTRUCTIONS ===
Please respond to the user's request above, taking into account:
1. The injected context and conversation history
2. The user's preferences and project status
3. The technical capabilities and constraints
4. Previous actions and decisions made

Provide a comprehensive, context-aware response that builds upon our conversation history.
=== END ENHANCED PROMPT ===
            """.strip()
            
            return enhanced_prompt
    
    def _update_stats(self, success: bool, start_time: datetime):
        """Update enhancement statistics"""
        self.enhancement_stats['total_enhanced'] += 1
        
        if success:
            self.enhancement_stats['successful_enhancements'] += 1
            self.enhancement_stats['last_enhancement'] = datetime.now().isoformat()
            
            # Calculate enhancement time
            enhancement_time = (datetime.now() - start_time).total_seconds()
            current_avg = self.enhancement_stats['average_enhancement_time']
            total_successful = self.enhancement_stats['successful_enhancements']
            
            # Update running average
            self.enhancement_stats['average_enhancement_time'] = (
                (current_avg * (total_successful - 1) + enhancement_time) / total_successful
            )
        else:
            self.enhancement_stats['failed_enhancements'] += 1
    
    def _cache_enhancement(self, original: str, enhanced: str, context_type: str):
        """Cache enhancement for future reference"""
        cache_key = f"{hash(original)}_{context_type}"
        self.context_cache[cache_key] = {
            'original': original,
            'enhanced': enhanced,
            'context_type': context_type,
            'timestamp': datetime.now().isoformat(),
            'enhancement_size': len(enhanced) - len(original)
        }
        
        # Keep cache manageable
        if len(self.context_cache) > 100:
            # Remove oldest entries
            oldest_keys = sorted(self.context_cache.keys(), 
                               key=lambda k: self.context_cache[k]['timestamp'])[:20]
            for key in oldest_keys:
                del self.context_cache[key]
    
    def get_enhancement_stats(self) -> Dict[str, Any]:
        """Get current enhancement statistics"""
        return {
            **self.enhancement_stats,
            'cache_size': len(self.context_cache),
            'enhancement_ratio': (
                f"{self.enhancement_stats['successful_enhancements']}/{self.enhancement_stats['total_enhanced']}"
                if self.enhancement_stats['total_enhanced'] > 0 else "0/0"
            )
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

# Global instance for easy access
auto_context_wrapper = AutoContextWrapper()

def auto_enhance_prompt(prompt: str, context_type: str = "general") -> str:
    """
    Convenience function to auto-enhance prompts
    
    Usage:
        enhanced = auto_enhance_prompt("How do I deploy this app?")
        enhanced = auto_enhance_prompt("What's next?", context_type="technical")
    """
    return auto_context_wrapper.auto_enhance_prompt(prompt, context_type)

def get_auto_enhancement_stats() -> Dict[str, Any]:
    """Get auto-enhancement statistics"""
    return auto_context_wrapper.get_enhancement_stats()

def toggle_auto_enhancement() -> bool:
    """Toggle auto-enhancement on/off"""
    return auto_context_wrapper.toggle_auto_enhancement()

if __name__ == "__main__":
    print("🧪 Testing Auto Context Wrapper...")
    
    # Test basic enhancement
    test_prompt = "What should I work on next?"
    enhanced = auto_enhance_prompt(test_prompt)
    
    print(f"📝 Original: {test_prompt}")
    print(f"🚀 Enhanced length: {len(enhanced)} characters")
    print(f"✨ Contains context: {'INJECTED CONTEXT' in enhanced}")
    
    # Show stats
    stats = get_auto_enhancement_stats()
    print(f"📊 Enhancement stats: {stats}")
    
    print("\n✅ Auto context wrapper test completed!")
