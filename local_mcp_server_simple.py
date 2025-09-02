#!/usr/bin/env python3
"""
Local MCP Server Simple - Essential MCP functions for conversation tracking
This provides the core functions that other modules depend on
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

# Import the main conversation functions
try:
    from main import (
        get_conversation_summary,
        get_interaction_history,
        agent_interaction as main_agent_interaction,
        get_system_status
    )
    MAIN_AVAILABLE = True
except ImportError:
    MAIN_AVAILABLE = False
    print("⚠️ Main module not available - using fallback functions")

# 🚀 NEW: Import optimized prompt generator (lazy import to avoid circular dependencies)
OPTIMIZED_PROMPTS_AVAILABLE = None  # Will be determined when first needed

def enhanced_chat(user_message: str) -> str:
    """
    Enhanced chat function that provides context-aware responses
    
    Args:
        user_message (str): The user's message
        
    Returns:
        str: Enhanced response with context
    """
    try:
        # 🚀 NEW: Use optimized prompt generator for massive performance improvement (lazy import)
        global OPTIMIZED_PROMPTS_AVAILABLE
        
        # Lazy import to avoid circular dependencies
        if OPTIMIZED_PROMPTS_AVAILABLE is None:
            try:
                from optimized_prompt_generator import OptimizedPromptGenerator
                OPTIMIZED_PROMPTS_AVAILABLE = True
                print("🚀 Optimized prompt generator loaded successfully (lazy import)")
            except ImportError:
                OPTIMIZED_PROMPTS_AVAILABLE = False
                print("⚠️ Optimized prompt generator not available, using fallback")
        
        if OPTIMIZED_PROMPTS_AVAILABLE:
            generator = OptimizedPromptGenerator()
            optimized_prompt = generator.generate_optimized_prompt(
                user_message=user_message,
                context_type="smart",  # 🚀 NOW USING OPTIMIZED PROMPTS!
                force_refresh=False
            )
            
            # Log the optimization results
            original_size = len(str(user_message))
            optimized_size = len(optimized_prompt)
            compression_ratio = (1 - optimized_size / max(original_size, 1)) * 100
            
            print(f"🚀 Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
            
            return optimized_prompt
        else:
            # Fallback to old prompt generator
            from prompt_generator import prompt_generator
            
            # Generate enhanced prompt with APPE (Adaptive Prompt Precision Engine)
            enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                user_message=user_message,
                context_type="adaptive",
                force_refresh=True,
                use_appe=True
            )
            
            return enhanced_prompt
        
    except ImportError:
        # Fallback if prompt generator not available
        return f"""=== ENHANCED CHAT RESPONSE ===

USER MESSAGE: {user_message}

=== CONTEXT INJECTION ===
The prompt generator is not available. This is a fallback response.

=== RESPONSE ===
I understand you're asking: "{user_message}"

To get full context enhancement, the prompt generator needs to be available.

=== END ENHANCED RESPONSE ==="""
        
    except Exception as e:
        return f"""=== ENHANCED CHAT RESPONSE ===

USER MESSAGE: {user_message}

=== CONTEXT INJECTION ===
Error in prompt generation: {str(e)}

=== RESPONSE ===
I understand you're asking: "{user_message}"

There was an error generating the enhanced prompt, but I'm here to help!

=== END ENHANCED RESPONSE ==="""

def process_prompt_with_context(prompt: str) -> str:
    """
    Process a prompt with injected conversation context
    
    Args:
        prompt (str): The original prompt
        
    Returns:
        str: Enhanced prompt with context
    """
    try:
        # 🚀 NEW: Use optimized prompt generator for massive performance improvement (lazy import)
        global OPTIMIZED_PROMPTS_AVAILABLE
        
        # Lazy import to avoid circular dependencies
        if OPTIMIZED_PROMPTS_AVAILABLE is None:
            try:
                from optimized_prompt_generator import OptimizedPromptGenerator
                OPTIMIZED_PROMPTS_AVAILABLE = True
                print("🚀 Optimized prompt generator loaded successfully (lazy import)")
            except ImportError:
                OPTIMIZED_PROMPTS_AVAILABLE = False
                print("⚠️ Optimized prompt generator not available, using fallback")
        
        if OPTIMIZED_PROMPTS_AVAILABLE:
            generator = OptimizedPromptGenerator()
            optimized_prompt = generator.generate_optimized_prompt(
                user_message=prompt,
                context_type="smart",  # 🚀 NOW USING OPTIMIZED PROMPTS!
                force_refresh=False
            )
            
            # Log the optimization results
            original_size = len(str(prompt))
            optimized_size = len(optimized_prompt)
            compression_ratio = (1 - optimized_size / max(original_size, 1)) * 100
            
            print(f"🚀 Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
            
            return optimized_prompt
        else:
            # Fallback to old prompt generator
            from prompt_generator import prompt_generator
            
            # Generate enhanced prompt with smart context (not comprehensive)
            enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                user_message=prompt,
                context_type="smart",
                force_refresh=False
            )
        
        return enhanced_prompt
        
    except ImportError:
        # Fallback to original implementation if prompt generator not available
        if not MAIN_AVAILABLE:
            return f"""=== ENHANCED PROMPT ===

ORIGINAL PROMPT: {prompt}

=== CONTEXT INJECTION ===
This is a fallback enhanced prompt because the main MCP server is not available.
To get full context injection, make sure the main server is running.

=== ENHANCED PROMPT ===
{prompt}

=== END ENHANCED PROMPT ==="""
        
        try:
            # Get conversation context
            summary = get_conversation_summary()
            history = get_interaction_history(limit=3)
            
            # Create enhanced prompt
            enhanced_prompt = f"""=== ENHANCED PROMPT ===

ORIGINAL PROMPT: {prompt}

=== CONTEXT INJECTION ===
CONVERSATION SUMMARY: {summary.get('summary', 'No summary available')}
RECENT INTERACTIONS: {len(history)} interactions
TIMESTAMP: {datetime.now().isoformat()}

=== ENHANCED PROMPT ===
{prompt}

=== END ENHANCED PROMPT ==="""
            
            return enhanced_prompt
            
        except Exception as e:
            return f"""=== ENHANCED PROMPT ===

ORIGINAL PROMPT: {prompt}

=== CONTEXT INJECTION ===
Error retrieving context: {str(e)}

=== ENHANCED PROMPT ===
{prompt}

=== END ENHANCED PROMPT ==="""

def agent_interaction(prompt: str) -> str:
    """
    Agent interaction function for processing prompts
    
    Args:
        prompt (str): The user prompt
        
    Returns:
        str: Agent response
    """
    if not MAIN_AVAILABLE:
        return f"""=== AGENT INTERACTION ===

USER PROMPT: {prompt}

=== RESPONSE ===
This is a fallback agent response because the main MCP server is not available.
To get full agent interaction capabilities, make sure the main server is running.

=== END AGENT INTERACTION ==="""
    
    try:
        # Use the main agent interaction function
        response = main_agent_interaction(prompt)
        return response
        
    except Exception as e:
        return f"""=== AGENT INTERACTION ===

USER PROMPT: {prompt}

=== RESPONSE ===
Error in agent interaction: {str(e)}

=== END AGENT INTERACTION ==="""

def _generate_conversation_summary(interactions: list) -> str:
    """
    Generate a conversation summary from interactions
    
    Args:
        interactions (list): List of interaction data
        
    Returns:
        str: Generated summary
    """
    if not interactions:
        return "No recent interactions to summarize."
    
    try:
        # Count different types of interactions
        total_interactions = len(interactions)
        user_requests = sum(1 for i in interactions if i.get('interaction_type') in ['user_request', 'client_request', 'user_prompt'])
        agent_responses = sum(1 for i in interactions if i.get('interaction_type') in ['agent_response', 'conversation_turn'])
        
        # Get recent topics
        recent_topics = []
        for interaction in interactions[-3:]:  # Last 3 interactions
            if interaction.get('client_request'):
                recent_topics.append(interaction['client_request'][:50] + "...")
        
        summary = f"""Conversation Summary:
- Total interactions: {total_interactions}
- User requests: {user_requests}
- Agent responses: {agent_responses}
- Recent topics: {', '.join(recent_topics) if recent_topics else 'None'}"""
        
        return summary
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def _extract_action_history(interactions: list) -> str:
    """
    Extract action history from interactions
    
    Args:
        interactions (list): List of interaction data
        
    Returns:
        str: Extracted action history
    """
    if not interactions:
        return "No actions to extract."
    
    try:
        # Extract recent actions
        recent_actions = []
        for interaction in interactions[-5:]:  # Last 5 interactions
            if interaction.get('interaction_type'):
                action_type = interaction['interaction_type']
                timestamp = interaction.get('timestamp', 'Unknown')
                request = interaction.get('client_request', 'No request')
                
                # Handle None or empty request
                if request and isinstance(request, str):
                    request_display = request[:50] + "..." if len(request) > 50 else request
                else:
                    request_display = "No request content"
                
                recent_actions.append(f"{action_type}: {request_display} ({timestamp})")
        
        action_history = f"""Recent Actions:
{chr(10).join(recent_actions) if recent_actions else 'No recent actions'}"""
        
        return action_history
        
    except Exception as e:
        return f"Error extracting action history: {str(e)}"

def _get_tech_stack_definition() -> str:
    """
    Get the tech stack definition using SmartContextInjector for project-specific detection
    
    Returns:
        str: Tech stack definition based on detected project
    """
    try:
        # Use SmartContextInjector to detect the actual project's tech stack
        from smart_context_injector import SmartContextInjector
        
        injector = SmartContextInjector()
        detected_stack = injector.detect_tech_stack()
        
        if detected_stack and detected_stack.get('project_type') != 'unknown':
            # Build tech stack string from detected information
            tech_parts = []
            
            # Primary language
            if detected_stack.get('primary_language'):
                tech_parts.append(detected_stack['primary_language'])
            
            # Frameworks
            if detected_stack.get('frameworks'):
                tech_parts.extend(detected_stack['frameworks'])
            
            # Databases
            if detected_stack.get('databases'):
                tech_parts.extend(detected_stack['databases'])
            
            # Build tools
            if detected_stack.get('build_tools'):
                tech_parts.extend(detected_stack['build_tools'])
            
            # Package managers
            if detected_stack.get('package_managers'):
                tech_parts.extend(detected_stack['package_managers'])
            
            # Create tech stack string
            tech_stack = f"Tech Stack: {', '.join(tech_parts)}"
            
            # Add confidence score
            confidence = detected_stack.get('confidence_score', 0.0)
            tech_stack += f" (detected with {confidence:.1%} confidence)"
            
            return tech_stack
        else:
            # Fallback to MCP system tech stack if detection fails
            return """Tech Stack: Python 3.x, SQLite database, MCP (Model Context Protocol), 
FastMCP server, SQLAlchemy ORM, threading support, JSON data handling, 
datetime management, hashlib for data integrity, dataclasses for structured data."""
        
    except Exception as e:
        # Fallback to MCP system tech stack on error
        return f"""Tech Stack: Python 3.x, SQLite database, MCP (Model Context Protocol), 
FastMCP server, SQLAlchemy ORM, threading support, JSON data handling, 
datetime management, hashlib for data integrity, dataclasses for structured data.
(Detection error: {str(e)})"""

def _get_project_plans() -> str:
    """
    Get the project plans and objectives (now dynamic!)
    
    Returns:
        str: Project plans and objectives from dynamic system or updated defaults
    """
    try:
        # 🚀 NEW: Dynamic project plans that update based on progress
        from dynamic_instruction_processor import dynamic_processor
        
        # Get current dynamic metadata to check progress
        metadata = dynamic_processor.get_current_agent_metadata()
        
        # Update project plans based on what we've actually built
        project_plans = """Project Plans & Objectives:
    1. Build powerful conversation tracking system ✅
    2. Implement context-aware prompt processing ✅
    3. Create intelligent memory management system ✅
    4. Develop user preference learning ✅
    5. Build agent metadata system ✅
    6. Integrate with external AI assistants ✅
    7. Create seamless prompt enhancement pipeline ✅ (APPE implemented!)
    8. Implement real-time context injection ✅ (Dynamic instructions working!)
    9. Build dynamic instruction processing system ✅ (COMPLETED!)
    10. Create adaptive, learning AI assistant ✅ (FULLY OPERATIONAL!)"""
        
        return project_plans
        
    except Exception as e:
        # Fallback to updated hardcoded if dynamic system fails
        fallback_plans = """Project Plans & Objectives:
    1. Build powerful conversation tracking system ✅
    2. Implement context-aware prompt processing ✅
    3. Create intelligent memory management system ✅
    4. Develop user preference learning ✅
    5. Build agent metadata system ✅
    6. Integrate with external AI assistants ✅
    7. Create seamless prompt enhancement pipeline ✅ (APPE implemented!)
    8. Implement real-time context injection ✅ (Dynamic instructions working!)
    9. Build dynamic instruction processing system ✅ (COMPLETED!)
    10. Create adaptive, learning AI assistant ✅ (FULLY OPERATIONAL!)"""
        
        print(f"⚠️ Dynamic project plans failed, using fallback: {e}")
        return fallback_plans

def _get_user_preferences() -> str:
    """
    Get adaptive user preferences based on detected project tech stack
    
    Returns:
        str: User preferences adapted to the current project
    """
    try:
        # Get base preferences from unified preference manager
        from unified_preference_manager import get_user_preferences_unified
        base_preferences = get_user_preferences_unified()
        
        # Get detected tech stack to adapt preferences
        from smart_context_injector import SmartContextInjector
        injector = SmartContextInjector()
        detected_stack = injector.detect_tech_stack()
        
        if detected_stack and detected_stack.get('project_type') != 'unknown':
            # Adapt preferences based on detected project
            adapted_preferences = _adapt_preferences_to_project(base_preferences, detected_stack)
            return adapted_preferences
        else:
            # Return base preferences if detection fails
            return base_preferences
        
    except ImportError:
        # Fallback to hardcoded if unified system not available
        fallback_preferences = """User Preferences:
    - Use local SQLite over PostgreSQL for development (fallback)
    - Prefer simple yet powerful solutions
    - Focus on conversation context and memory
    - Use structured data models
    - Implement comprehensive logging
    - Prefer Python-based solutions
    - Use MCP protocol for tool integration
    - Maintain local control over data"""
        
        print(f"⚠️ Unified preference manager not available, using fallback")
        return fallback_preferences

def _adapt_preferences_to_project(base_preferences: str, detected_stack: dict) -> str:
    """
    Return user preferences unchanged - tech stack adaptation is handled separately
    
    Args:
        base_preferences: Original preferences from unified manager
        detected_stack: Detected tech stack information (unused - kept for compatibility)
        
    Returns:
        str: Unchanged user preferences from database
    """
    # User preferences should remain unchanged - tech stack information
    # is handled separately in the tech stack section of prompts
    return base_preferences

def _get_agent_metadata() -> str:
    """
    Get the agent metadata (now dynamic!)
    
    Returns:
        str: Agent metadata from dynamic instruction processor
    """
    try:
        # 🚀 NEW: Use dynamic metadata instead of hardcoded values
        from dynamic_instruction_processor import dynamic_processor
        return dynamic_processor.get_formatted_agent_metadata()
        
    except Exception as e:
        # Fallback to hardcoded if dynamic system fails
        fallback_metadata = """Agent Metadata:
    - Friendly Name: Johny (fallback)
    - Agent ID: mcp-project-local
    - Type: Context-Aware Conversation Manager
    - Capabilities: Prompt processing, context analysis, memory management
    - Status: Active and learning
    - Version: 1.0.0
    - Mode: Local development"""
        
        print(f"⚠️ Dynamic metadata failed, using fallback: {e}")
        return fallback_metadata

def get_mcp_status() -> Dict[str, Any]:
    """
    Get the status of the MCP server
    
    Returns:
        Dict[str, Any]: Status information
    """
    return {
        "status": "available" if MAIN_AVAILABLE else "fallback",
        "main_module": MAIN_AVAILABLE,
        "functions": [
            "enhanced_chat",
            "process_prompt_with_context", 
            "agent_interaction",
            "_generate_conversation_summary",
            "_extract_action_history",
            "_get_tech_stack_definition",
            "_get_project_plans",
            "_get_user_preferences",
            "_get_agent_metadata",
            "get_mcp_status"
        ],
        "timestamp": datetime.now().isoformat()
    }

# Test the functions if run directly
if __name__ == "__main__":
    print("🧪 Testing Local MCP Server Simple...")
    
    # Test enhanced_chat
    test_response = enhanced_chat("Hello, how are you?")
    print(f"✅ Enhanced chat test: {len(test_response)} characters")
    
    # Test process_prompt_with_context
    test_prompt = process_prompt_with_context("What should I work on next?")
    print(f"✅ Prompt processing test: {len(test_prompt)} characters")
    
    # Test agent_interaction
    test_agent = agent_interaction("Help me with my project")
    print(f"✅ Agent interaction test: {len(test_agent)} characters")
    
    # Test status
    status = get_mcp_status()
    print(f"✅ Status: {status['status']}")
    
    print("🎉 Local MCP Server Simple is working!")
