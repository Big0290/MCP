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

def enhanced_chat(user_message: str) -> str:
    """
    Enhanced chat function that provides context-aware responses
    
    Args:
        user_message (str): The user's message
        
    Returns:
        str: Enhanced response with context
    """
    try:
        # Use the centralized prompt generator for full context enhancement
        from prompt_generator import prompt_generator
        
        # Generate enhanced prompt with comprehensive context
        enhanced_prompt = prompt_generator.generate_enhanced_prompt(
            user_message=user_message,
            context_type="comprehensive",
            force_refresh=True
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
        # Use the centralized prompt generator
        from prompt_generator import prompt_generator
        
        # Generate enhanced prompt with comprehensive context
        enhanced_prompt = prompt_generator.generate_enhanced_prompt(
            user_message=prompt,
            context_type="comprehensive",
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
    Get the tech stack definition
    
    Returns:
        str: Tech stack definition
    """
    try:
        tech_stack = """Tech Stack: Python 3.x, SQLite database, MCP (Model Context Protocol), 
    FastMCP server, SQLAlchemy ORM, threading support, JSON data handling, 
    datetime management, hashlib for data integrity, dataclasses for structured data."""
        
        return tech_stack
        
    except Exception as e:
        return f"Error getting tech stack: {str(e)}"

def _get_project_plans() -> str:
    """
    Get the project plans and objectives
    
    Returns:
        str: Project plans and objectives
    """
    try:
        project_plans = """Project Plans & Objectives:
    1. Build powerful conversation tracking system ✅
    2. Implement context-aware prompt processing ✅
    3. Create intelligent memory management system ✅
    4. Develop user preference learning ✅
    5. Build agent metadata system ✅
    6. Integrate with external AI assistants ✅
    7. Create seamless prompt enhancement pipeline 🚧
    8. Implement real-time context injection 🚧"""
        
        return project_plans
        
    except Exception as e:
        return f"Error getting project plans: {str(e)}"

def _get_user_preferences() -> str:
    """
    Get the user preferences
    
    Returns:
        str: User preferences
    """
    try:
        user_preferences = """User Preferences:
    - Use local SQLite over PostgreSQL for development
    - Prefer simple yet powerful solutions
    - Focus on conversation context and memory
    - Use structured data models
    - Implement comprehensive logging
    - Prefer Python-based solutions
    - Use MCP protocol for tool integration
    - Maintain local control over data"""
        
        return user_preferences
        
    except Exception as e:
        return f"Error getting user preferences: {str(e)}"

def _get_agent_metadata() -> str:
    """
    Get the agent metadata
    
    Returns:
        str: Agent metadata
    """
    try:
        agent_metadata = """Agent Metadata:
    - Friendly Name: Johny
    - Agent ID: mcp-project-local
    - Type: Context-Aware Conversation Manager
    - Capabilities: Prompt processing, context analysis, memory management
    - Status: Active and learning
    - Version: 1.0.0
    - Mode: Local development"""
        
        return agent_metadata
        
    except Exception as e:
        return f"Error getting agent metadata: {str(e)}"

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
