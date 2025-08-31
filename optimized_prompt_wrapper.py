#!/usr/bin/env python3
"""
🚀 Optimized Prompt Wrapper - Easy Access to Optimized Prompts

This module provides easy access to the optimized prompt system
for integration with existing MCP tools.
"""

from optimized_prompt_generator import OptimizedPromptGenerator, generate_optimized_prompt

# Global instance for easy access
_optimized_generator = None

def get_optimized_generator():
    """Get or create the global optimized prompt generator instance"""
    global _optimized_generator
    if _optimized_generator is None:
        _optimized_generator = OptimizedPromptGenerator()
    return _optimized_generator

def generate_optimized_prompt_for_mcp(user_message: str, context_type: str = "smart") -> str:
    """
    Generate an optimized prompt specifically for MCP usage.
    
    Args:
        user_message: The user's message
        context_type: Type of context to use
        
    Returns:
        str: Optimized prompt string
    """
    try:
        generator = get_optimized_generator()
        optimized_prompt = generator.generate_optimized_prompt(
            user_message=user_message,
            context_type=context_type,
            force_refresh=False
        )
        
        # Log optimization results
        original_size = len(str(user_message))
        optimized_size = len(optimized_prompt)
        compression_ratio = (1 - optimized_size / max(original_size, 1)) * 100
        
        print(f"🚀 MCP Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
        
        return optimized_prompt
        
    except Exception as e:
        print(f"❌ Optimized prompt generation failed: {e}")
        # Return minimal fallback
        return f"🚀 OPTIMIZED PROMPT: {user_message}\n\n👤 PREFERENCES: Concise, technical, structured responses\n⚙️ TECH: Python, SQLite, MCP\n🤖 AGENT: Johny\n\n🎯 Provide helpful, context-aware assistance."

# Convenience functions
def quick_optimize(message: str) -> str:
    """Quick optimization with default settings"""
    return generate_optimized_prompt_for_mcp(message, "smart")

def technical_optimize(message: str) -> str:
    """Technical optimization for code/implementation queries"""
    return generate_optimized_prompt_for_mcp(message, "technical")

def conversation_optimize(message: str) -> str:
    """Conversation optimization for chat continuity"""
    return generate_optimized_prompt_for_mcp(message, "conversation")

def project_optimize(message: str) -> str:
    """Project optimization for structure/analysis queries"""
    return generate_optimized_prompt_for_mcp(message, "project")
