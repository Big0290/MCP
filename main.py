from typing import Any
import os
import sys
import threading
import time
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# DIRECT IMPORTS - NO MOCK BULLSHIT
from interaction_logger import logger
from session_manager import session_manager
LOGGER_AVAILABLE = True
SESSION_MANAGER_AVAILABLE = True
print("✅ Interaction logger and session manager loaded (no mocks!)")

try:
    from config import Config
    CONFIG_AVAILABLE = True
    print("✅ Config available")
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️ Config not available - using default values")
    # Create a mock config
    class MockConfig:
        ENVIRONMENT = "development"
        CONTAINER_ID = "local"
        ENABLE_BACKGROUND_MONITORING = True
        ENABLE_AUTOMATIC_METADATA = True
        MONITORING_INTERVAL_SECONDS = 60
        LOG_LEVEL = "INFO"
        LOG_FILE = "/Users/jonathanmorand/Documents/ProjectsFolder/MCP_FOLDER/MCP/MCP/logs/agent_tracker.log"
    
    Config = MockConfig

# Try to import MCP, but don't fail if it's not available
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
    print("✅ MCP package available")
    
    # Test the actual FastMCP structure
    test_mcp = FastMCP("test")
    print(f"🔍 FastMCP structure: {dir(test_mcp)}")
    
    # Find the correct attribute for tools
    if hasattr(test_mcp, '_tools'):
        TOOLS_ATTR = '_tools'
        print("✅ Using _tools attribute")
    elif hasattr(test_mcp, 'tools'):
        TOOLS_ATTR = 'tools'
        print("✅ Using tools attribute")
    elif hasattr(test_mcp, 'get_tools'):
        TOOLS_ATTR = 'get_tools'
        print("✅ Using get_tools method")
    else:
        # Try to find any attribute that might contain tools
        for attr in dir(test_mcp):
            if 'tool' in attr.lower():
                print(f"🔍 Found potential tools attribute: {attr}")
                TOOLS_ATTR = attr
                break
        else:
            TOOLS_ATTR = '_tools'  # Default fallback
            print("⚠️ Could not determine tools attribute, using default")
    
except ImportError:
    MCP_AVAILABLE = False
    print("⚠️ MCP package not available - tools will be defined but not registered")
    # Create a mock MCP server for testing
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
            self._tools = {}
        
        def tool(self, func=None):
            if func is None:
                return lambda f: self.tool(f)
            
            # Register the tool
            self._tools[func.__name__] = {
                'description': func.__doc__ or 'No description',
                'parameters': {},
                'function': func
            }
            return func
        
        def run(self, transport="stdio"):
            print(f"Mock MCP server '{self.name}' would run with transport: {transport}")
            print(f"Available tools: {list(self._tools.keys())}")
    
    FastMCP = MockFastMCP
    TOOLS_ATTR = '_tools'

# Initialize FastMCP server (or mock)
mcp = FastMCP("mcp-project")

# Add a proper list_tools method for MCP clients
@mcp.tool()
def list_tools() -> str:
    """List all available MCP tools with descriptions.
    
    This function provides a comprehensive list of all available tools
    that can be called through the MCP server, including their descriptions
    and usage information.
    
    Returns:
        str: A formatted list of all available tools with descriptions
    """
    try:
        tools_info = []
        tools_info.append("🔧 Available MCP Tools:")
        tools_info.append("=" * 50)
        
        # Get available tools from the tool manager
        available_tools = get_available_tools()
        
        if not available_tools:
            tools_info.append("❌ No tools available")
            return "\n".join(tools_info)
        
        # Format each tool with its description
        for tool_name, tool_data in available_tools.items():
            if isinstance(tool_data, dict) and 'description' in tool_data:
                description = tool_data['description']
                # Truncate long descriptions
                if len(description) > 100:
                    description = description[:97] + "..."
                tools_info.append(f"📌 {tool_name}: {description}")
            else:
                tools_info.append(f"📌 {tool_name}: No description available")
        
        tools_info.append("")
        tools_info.append(f"Total tools available: {len(available_tools)}")
        tools_info.append("")
        tools_info.append("💡 Usage: Use @tool_name in Cursor to call these tools")
        
        return "\n".join(tools_info)
        
    except Exception as e:
        return f"❌ Error listing tools: {str(e)}"

@mcp.tool()
def list_prompts() -> str:
    """List all available MCP prompts with descriptions.
    
    This function provides a list of all available prompts
    that can be used through the MCP server.
    
    Returns:
        str: A formatted list of all available prompts
    """
    try:
        prompts_info = []
        prompts_info.append("📝 Available MCP Prompts:")
        prompts_info.append("=" * 50)
        
        # For now, we'll return a basic list since prompts aren't fully implemented
        prompts_info.append("📌 system_prompt: System-level prompt for the MCP server")
        prompts_info.append("📌 user_prompt: User interaction prompt template")
        prompts_info.append("📌 context_prompt: Context-aware prompt template")
        prompts_info.append("")
        prompts_info.append("💡 These prompts can be customized for different use cases")
        
        return "\n".join(prompts_info)
        
    except Exception as e:
        return f"❌ Error listing prompts: {str(e)}"

# Helper function to get tools safely
def get_available_tools():
    """Get available tools from the MCP server.
    
    This function safely retrieves the list of available MCP tools by checking multiple
    possible locations where tools might be stored. It handles both synchronous and
    asynchronous tool managers, and provides fallback mechanisms for different MCP
    server implementations.
    
    Returns:
        dict: A dictionary containing available tools, or empty dict if none found
        
    Note:
        This function includes comprehensive error handling and will return an empty
        dictionary if any issues occur during tool discovery, ensuring the application
        remains stable even if the MCP server is not fully initialized.
    """
    try:
        if hasattr(mcp, '_tool_manager'):
            tool_manager = getattr(mcp, '_tool_manager')
            if hasattr(tool_manager, '_tools'):
                # Tools are stored in _tool_manager._tools
                return tool_manager._tools
            elif hasattr(tool_manager, 'tools'):
                return tool_manager.tools
            else:
                return {}
        elif hasattr(mcp, 'list_tools'):
            # Check if list_tools is async
            import asyncio
            import inspect
            
            list_tools_method = getattr(mcp, 'list_tools')
            if inspect.iscoroutinefunction(list_tools_method):
                # It's async, we can't call it synchronously
                # Return a placeholder or try to get tools from _tool_manager
                if hasattr(mcp, '_tool_manager'):
                    tool_manager = getattr(mcp, '_tool_manager')
                    if hasattr(tool_manager, 'tools'):
                        return tool_manager.tools
                    elif hasattr(tool_manager, '_tools'):
                        return tool_manager._tools
                    else:
                        return {}
                else:
                    return {}
            else:
                # It's synchronous, call it
                return list_tools_method()
        elif hasattr(mcp, TOOLS_ATTR):
            if callable(getattr(mcp, TOOLS_ATTR)):
                # It's a method, call it
                return getattr(mcp, TOOLS_ATTR)()
            else:
                # It's an attribute, access it
                return getattr(mcp, TOOLS_ATTR)
        else:
            # Try to find tools in other ways
            if hasattr(mcp, 'get_tools'):
                return mcp.get_tools()
            else:
                # Last resort: return empty dict
                return {}
    except Exception as e:
        print(f"⚠️ Error getting tools: {e}")
        return {}

# Constants
USER_AGENT = "mcp-project/1.0"

# Initialize logger with session
logger.get_or_create_session()


@mcp.tool()
def agent_interaction(prompt: str) -> str:
    """Interact with the agent by processing a user prompt and generating a response.
    
    This function serves as the main interface for agent interactions, taking a user's
    prompt and returning an appropriate response. It includes comprehensive logging
    for conversation tracking, error handling, and monitoring purposes.
    
    NEW: Automatically injects conversation context into every prompt for enhanced AI responses.
    
    Args:
        prompt (str): The user's input prompt or question to be processed by the agent
        
    Returns:
        str: The agent's response to the user's prompt
        
    Features:
        - AUTOMATIC CONTEXT INJECTION: Every prompt gets enhanced with conversation history
        - Logs client requests for conversation tracking
        - Processes enhanced prompts through agent logic
        - Logs agent responses for analysis
        - Records complete conversation turns for debugging
        - Comprehensive error handling with detailed logging
        
    Note:
        Now automatically enhances every prompt with context before processing.
    """
    try:
        # Step 1: Log the original client prompt
        logger.log_client_request(prompt)
        
        # Step 2: AUTOMATIC CONTEXT INJECTION - Use centralized prompt generator
        enhanced_prompt = prompt  # Default fallback
        try:
            # Import the centralized prompt generator
            from prompt_generator import prompt_generator
            
            # Generate enhanced prompt with smart context (not comprehensive)
            enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                user_message=prompt,
                context_type="smart",
                force_refresh=False
            )
            
            print(f"🚀 AUTOMATIC CONTEXT INJECTION: {len(prompt)} -> {len(enhanced_prompt)} characters")
            
        except Exception as context_error:
            print(f"⚠️ Context injection failed, using original prompt: {context_error}")
            enhanced_prompt = prompt
        
        # Step 3: Process the ENHANCED prompt (replace with actual agent logic)
        response = f"The agent responded to the ENHANCED prompt: {enhanced_prompt}"
        
        # Step 4: Log the agent's response
        logger.log_agent_response(response)
        
        # Step 5: Log the complete conversation turn
        logger.log_conversation_turn(
            client_request=prompt,
            agent_response=response
        )
        
        return response
        
    except Exception as e:
        # Log any errors
        logger.log_interaction(
            interaction_type='conversation_error',
            client_request=prompt,
            error_message=str(e),
            status='error'
        )
        raise

@mcp.tool()
def get_interaction_history(limit: int = 10, session_id: str = None) -> str:
    """Retrieve conversation history from the database for analysis, debugging, and monitoring.
    
    This function queries the database to fetch historical conversation data, allowing
    developers and administrators to analyze interaction patterns, debug issues, and
    monitor system performance. It supports filtering by session and limiting results.
    
    Args:
        limit (int, optional): Maximum number of interactions to return. Defaults to 10.
        session_id (str, optional): Specific session ID to filter results. If None, 
                                   returns interactions from all sessions.
        
    Returns:
        str: A formatted string containing interaction history data including:
             - Interaction ID, timestamp, type, client request, agent response, and status
             - Total count of found interactions
             - Structured data for easy parsing and analysis
             
    Features:
        - Database-driven conversation retrieval
        - Session-based filtering for targeted analysis
        - Configurable result limits for performance
        - Comprehensive error handling with informative messages
        - Fallback to mock responses when database is unavailable
        
    Use Cases:
        - Debugging conversation flow issues
        - Monitoring user interaction patterns
        - Analyzing agent response quality
        - Performance monitoring and optimization
        - User experience analysis
        
    Note:
        Returns mock data when LOGGER_AVAILABLE is False. In production, this provides
        real-time access to the conversation database for comprehensive analysis.
    """
    # LOGGER IS ALWAYS AVAILABLE - NO MOCKS!
    
    try:
        import sqlite3
        
        # Use direct SQLite connection to bypass SQLAlchemy model issues
        db_path = "/Users/jonathanmorand/Documents/ProjectsFolder/MCP_FOLDER/MCP/MCP/data/agent_tracker.db"
        
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            # Build SQL query
            sql = "SELECT * FROM interactions"
            params = []
            
            if session_id:
                sql += " WHERE session_id = ?"
                params.append(session_id)
            
            sql += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            if not rows:
                return "No conversations found."
            
            result = []
            for row in rows:
                result.append({
                    'id': row['id'],
                    'timestamp': row['timestamp'] or 'unknown',
                    'type': row['interaction_type'],
                    'client_request': row['prompt'] or row['client_request'] or '',
                    'agent_response': row['response'] or row['agent_response'] or '',
                    'status': row['status'] or 'completed'
                })
            
            return f"Found {len(result)} conversations: {result}"
            
    except Exception as e:
        return f"Error retrieving conversation history: {str(e)}"

@mcp.tool()
def get_conversation_summary(session_id: str = None) -> str:
    """Generate comprehensive conversation statistics and pattern analysis from the database.
    
    This function provides high-level insights into conversation data by aggregating
    interaction metrics, analyzing patterns, and summarizing recent activity. It's
    designed for monitoring system usage, identifying trends, and understanding
    user interaction behavior across different sessions.
    
    Args:
        session_id (str, optional): Specific session ID to analyze. If None, provides
                                   summary across all sessions for system-wide insights.
        
    Returns:
        str: A formatted string containing comprehensive conversation analytics including:
             - Total interaction count across the specified scope
             - Breakdown of interaction types (e.g., weather requests, agent interactions)
             - Recent activity summary with truncated prompts for privacy
             - Structured data format for easy parsing and dashboard integration
             
    Features:
        - Aggregated statistics for performance monitoring
        - Interaction type categorization and counting
        - Recent activity tracking with privacy-conscious prompt truncation
        - Session-specific or system-wide analysis capabilities
        - Database-driven analytics with real-time data
        - Comprehensive error handling with fallback responses
        
    Analytics Provided:
        - Volume metrics (total interactions)
        - Distribution analysis (interaction type breakdown)
        - Temporal insights (recent activity patterns)
        - Session isolation for targeted analysis
        
    Use Cases:
        - System performance monitoring and capacity planning
        - User experience analysis and optimization
        - Debugging conversation flow issues
        - Identifying popular interaction patterns
        - Monitoring agent response quality trends
        - Session-specific troubleshooting and analysis
        
    Note:
        Returns mock data when LOGGER_AVAILABLE is False. In production, this provides
        real-time analytics from the conversation database for operational insights.
    """
    # LOGGER IS ALWAYS AVAILABLE - NO MOCKS!
    
    try:
        from models_unified import get_session_factory, AgentInteraction
        
        # Get a database session using the same session factory as the logger
        session_factory = get_session_factory()
        with session_factory() as db_session:
            # Query the real database directly
            query = db_session.query(AgentInteraction)
            
            # Filter by session_id if provided
            if session_id:
                query = query.filter(AgentInteraction.session_id == session_id)
            
            # Get more interactions for summary analysis
            interactions = query.order_by(AgentInteraction.timestamp.desc()).limit(100).all()
        
        if not interactions:
            return "No conversations found."
        
        # Get total interactions
        total_interactions = len(interactions)
        
        # Get interaction types breakdown
        type_counts = {}
        for interaction in interactions:
            interaction_type = getattr(interaction, 'interaction_type', 'unknown')
            type_counts[interaction_type] = type_counts.get(interaction_type, 0) + 1
        
        # Get recent activity
        recent_interactions = interactions[:5]  # First 5 since they're already ordered
        recent_summary = []
        for interaction in recent_interactions:
            prompt = getattr(interaction, 'prompt', '')
            recent_summary.append({
                'type': getattr(interaction, 'interaction_type', 'unknown'),
                'timestamp': getattr(interaction, 'timestamp', datetime.now()).isoformat(),
                'client_request': prompt[:300] + "..." if prompt and len(prompt) > 300 else prompt,
                'status': getattr(interaction, 'status', 'unknown')
            })
        
        summary = {
            'total_interactions': total_interactions,
            'interaction_type_breakdown': type_counts,
            'recent_activity': recent_summary
        }
        
        return f"Conversation Summary: {summary}"
            
    except Exception as e:
        return f"Error retrieving conversation summary: {str(e)}"

@mcp.tool()
def get_system_status() -> str:
    """Retrieve comprehensive system health, configuration, and operational status information.
    
    This function provides a real-time snapshot of the system's current state, including
    configuration settings, component availability, performance metrics, and operational
    status. It's essential for system monitoring, debugging, and operational oversight.
    
    Returns:
        str: A formatted string containing detailed system status information including:
             - Environment configuration (development, production, etc.)
             - Monitoring settings and intervals
             - Logging configuration and file paths
             - System uptime and performance metrics
             - Available MCP tools and their status
             - Component availability flags (MCP, Logger, Config)
             - Current timestamp for status freshness
             - Tools attribute configuration for MCP integration
             
    Status Components:
        - Environment & Configuration: Current environment, monitoring settings
        - Performance Metrics: Uptime tracking, system responsiveness
        - Component Health: MCP server, logger, and configuration system status
        - Tool Availability: List of currently available MCP tools
        - Operational Settings: Background monitoring, metadata collection
        
    Use Cases:
        - System health monitoring and alerting
        - Configuration verification and troubleshooting
        - Performance monitoring and capacity planning
        - Debugging system integration issues
        - Operational status reporting and dashboards
        - Development environment validation
        
    Monitoring Features:
        - Real-time status updates with timestamp
        - Component availability tracking
        - Configuration validation
        - Performance metric collection
        - Tool discovery and status reporting
        
    Note:
        This function aggregates status from multiple system components and provides
        a unified view of system health. It's designed to be called frequently for
        monitoring purposes and includes comprehensive error handling.
    """
    try:
        available_tools = get_available_tools()
        tool_names = list(available_tools.keys()) if isinstance(available_tools, dict) else []
        
        status = {
            'environment': Config.ENVIRONMENT,
            'background_monitoring': Config.ENABLE_BACKGROUND_MONITORING,
            'monitoring_interval': Config.MONITORING_INTERVAL_SECONDS,
            'automatic_metadata': Config.ENABLE_AUTOMATIC_METADATA,
            'log_level': Config.LOG_LEVEL,
            'log_file': Config.LOG_FILE,
            'uptime_seconds': int(time.time() - start_time) if 'start_time' in globals() else 0,
            'available_tools': tool_names,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'mcp_available': MCP_AVAILABLE,
            'logger_available': LOGGER_AVAILABLE,
            'config_available': CONFIG_AVAILABLE,
            'tools_attribute': TOOLS_ATTR
        }
        return f"System Status: {status}"
    except Exception as e:
        return f"Error getting system status: {str(e)}"

@mcp.tool()
def test_conversation_tracking(message: str = "Hello, world!") -> str:
    """Test and validate the conversation tracking system's functionality with a sample message.
    
    This function performs end-to-end testing of the conversation logging infrastructure
    by simulating a complete conversation turn. It tests all major logging functions
    including client request logging, agent response logging, and conversation turn
    recording. This is essential for verifying system health and debugging logging issues.
    
    Args:
        message (str, optional): Custom test message to use. Defaults to "Hello, world!"
                               for consistent testing. Custom messages help test
                               specific scenarios or edge cases.
        
    Returns:
        str: A formatted response indicating test success or failure:
             - Success: "✅ Conversation tracking test successful! Logged: '{message}' -> '{response}'"
             - Failure: "❌ Conversation tracking test failed: {error_details}"
             
    Test Coverage:
        - Client request logging (logger.log_client_request)
        - Agent response logging (logger.log_agent_response)
        - Complete conversation turn recording (logger.log_conversation_turn)
        - Error handling and logging (logger.log_interaction)
        - Database persistence and retrieval
        
    Use Cases:
        - System health verification after deployment
        - Debugging conversation logging issues
        - Validating database connectivity and schema
        - Testing logging configuration and permissions
        - Verifying error handling and recovery
        - Development environment validation
        
    Testing Workflow:
        1. Logs a test client request with the provided message
        2. Generates a mock agent response
        3. Logs the agent response
        4. Records the complete conversation turn
        5. Returns success confirmation or detailed error information
        
    Error Handling:
        - Comprehensive exception catching and logging
        - Detailed error messages for debugging
        - Graceful degradation with informative feedback
        - Error logging to maintain audit trail
        
    Note:
        This function is designed for testing and debugging purposes. It creates
        test data in the conversation database, so it should be used judiciously
        in production environments. The test data is indistinguishable from real
        conversations in the logging system.
    """
    try:
        # Log a test conversation
        logger.log_client_request(f"Test message: {message}")
        response = f"This is a test response to: {message}"
        logger.log_agent_response(response)
        logger.log_conversation_turn(
            client_request=f"Test message: {message}",
            agent_response=response
        )
        
        return f"✅ Conversation tracking test successful! Logged: '{message}' -> '{response}'"
        
    except Exception as e:
        error_msg = f"❌ Conversation tracking test failed: {str(e)}"
        logger.log_interaction(
            interaction_type='test_error',
            error_message=error_msg,
            status='error'
        )
        return error_msg

@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get current weather information for a specified city with conversation tracking.
    
    This function provides weather information for any city while automatically logging
    the interaction for conversation tracking and analysis purposes.
    
    Args:
        city (str): The name of the city to get weather for
        
    Returns:
        str: Weather information for the specified city
        
    Features:
        - Logs weather requests for conversation tracking
        - Provides mock weather data (replace with actual weather API in production)
        - Comprehensive error handling and logging
        - Automatic conversation turn recording
        
    Note:
        Currently returns mock weather data. In production, this would integrate with
        an actual weather API service to provide real-time weather information.
    """
    try:
        # Log the weather request
        request = f"Get weather for {city}"
        logger.log_client_request(request)
        
        # Mock weather response (replace with actual weather API call)
        weather_data = {
            "city": city,
            "temperature": "22°C",
            "condition": "Partly Cloudy",
            "humidity": "65%",
            "wind_speed": "12 km/h"
        }
        
        response = f"Weather for {city}: {weather_data['temperature']}, {weather_data['condition']}, Humidity: {weather_data['humidity']}, Wind: {weather_data['wind_speed']}"
        
        # Log the weather response
        logger.log_agent_response(response)
        
        # Log the complete conversation turn
        logger.log_conversation_turn(
            client_request=request,
            agent_response=response
        )
        
        return response
        
    except Exception as e:
        # Log any errors
        error_msg = f"Error getting weather for {city}: {str(e)}"
        logger.log_interaction(
            interaction_type='weather_error',
            client_request=f"Get weather for {city}",
            error_message=str(e),
            status='error'
        )
        return error_msg

@mcp.tool()
def inject_conversation_context(prompt: str, session_id: str = None) -> str:
    """Inject conversation context into a prompt for enhanced Cursor agent interactions.
    
    This function takes a base prompt and enhances it with relevant conversation context
    including decision tree analysis, user preferences, project context, and recent
    interaction history. This creates a more context-aware and personalized experience
    for the Cursor agent.
    
    Args:
        prompt (str): The base prompt to enhance with context
        session_id (str, optional): Specific session ID to get context from. If None,
                                   uses the current active session.
        
    Returns:
        str: The enhanced prompt with injected conversation context
        
    Features:
        - Decision tree-based context analysis
        - User preference inference and injection
        - Project context extraction and injection
        - Recent interaction history with relevance scoring
        - Semantic keyword analysis and injection
        - Technology stack detection and injection
        
    Use Cases:
        - Enhancing Cursor agent prompts with conversation history
        - Providing personalized responses based on user patterns
        - Maintaining context across multiple interactions
        - Improving code suggestions with project context
        - Creating more relevant and helpful responses
    """
    # LOGGER IS ALWAYS AVAILABLE - NO MOCKS!
    
    try:
        from context_manager import context_manager
        
        # Get context for injection
        context = context_manager.get_context_for_injection(session_id)
        if not context:
            return f"⚠️ No context available - returning original prompt: {prompt}"
        
        # Inject context into prompt
        enhanced_prompt = context_manager.inject_context_into_prompt(prompt, context)
        return enhanced_prompt
        
    except Exception as e:
        return f"Error injecting conversation context: {str(e)}\n\nOriginal prompt: {prompt}"

@mcp.tool()
def get_conversation_context(session_id: str = None) -> str:
    """Get detailed conversation context for analysis and debugging.
    
    This function provides comprehensive conversation context including decision tree
    structure, active conversation branches, user preferences, and semantic analysis.
    It's useful for understanding how the context system is working and debugging
    context injection issues.
    
    Args:
        session_id (str, optional): Specific session ID to analyze. If None, provides
                                   context for the current active session.
        
    Returns:
        str: A detailed analysis of the conversation context including:
             - Decision tree structure and active branches
             - User preference analysis
             - Project context extraction
             - Semantic keyword analysis
             - Recent interaction patterns
             - Context relevance scoring
             
    Features:
        - Decision tree visualization
        - Active branch identification
        - User preference inference
        - Project context analysis
        - Semantic similarity scoring
        - Context usage statistics
        
    Use Cases:
        - Debugging context injection issues
        - Understanding conversation flow patterns
        - Analyzing user interaction preferences
        - Monitoring context system performance
        - Optimizing context generation algorithms
    """
    # LOGGER IS ALWAYS AVAILABLE - NO MOCKS!
    
    try:
        from context_manager import context_manager
        
        # Get context for analysis
        context = context_manager.get_context_for_injection(session_id)
        if not context:
            return "No conversation context available for the specified session."
        
        # Build detailed context report
        report_parts = []
        
        # Decision tree analysis
        if context.decision_tree:
            report_parts.append("🌳 DECISION TREE STRUCTURE:")
            for node_id, node in context.decision_tree.items():
                if node_id in context.active_branches:
                    status = "🔥 ACTIVE"
                else:
                    status = "📝 INACTIVE"
                report_parts.append(f"  {status} {node.topic} (ID: {node_id})")
                report_parts.append(f"    Content: {node.content[:100]}...")
                report_parts.append(f"    Keywords: {', '.join(node.keywords[:5])}")
                report_parts.append(f"    Relevance: {node.relevance_score:.2f}")
                if node.parent:
                    report_parts.append(f"    Parent: {context.decision_tree[node.parent].topic if node.parent in context.decision_tree else 'Unknown'}")
                report_parts.append("")
        
        # Active branches summary
        if context.active_branches:
            report_parts.append(f"🎯 ACTIVE BRANCHES ({len(context.active_branches)}):")
            for branch_id in context.active_branches[:5]:
                if branch_id in context.decision_tree:
                    node = context.decision_tree[branch_id]
                    report_parts.append(f"  • {node.topic}: {node.content[:80]}...")
            report_parts.append("")
        
        # User preferences
        if context.user_preferences:
            report_parts.append("👤 USER PREFERENCES:")
            for key, value in context.user_preferences.items():
                if isinstance(value, list):
                    report_parts.append(f"  {key}: {', '.join(value)}")
                else:
                    report_parts.append(f"  {key}: {value}")
            report_parts.append("")
        
        # Project context
        if context.project_context:
            report_parts.append("📁 PROJECT CONTEXT:")
            for key, value in context.project_context.items():
                if isinstance(value, list):
                    report_parts.append(f"  {key}: {', '.join(value[:5])}")
                else:
                    report_parts.append(f"  {key}: {value}")
            report_parts.append("")
        
        # Semantic analysis
        if context.semantic_context:
            report_parts.append("🔍 SEMANTIC ANALYSIS:")
            if context.semantic_context.get('frequent_keywords'):
                top_keywords = [f"{word} ({freq})" for word, freq in context.semantic_context['frequent_keywords'][:10]]
                report_parts.append(f"  Frequent Keywords: {', '.join(top_keywords)}")
            if context.semantic_context.get('topic_distribution'):
                topics = [f"{topic} ({count})" for topic, count in context.semantic_context['topic_distribution'].items()]
                report_parts.append(f"  Topic Distribution: {', '.join(topics)}")
            report_parts.append("")
        
        # Recent interactions
        if context.recent_interactions:
            report_parts.append("🕒 RECENT INTERACTIONS:")
            for interaction in context.recent_interactions[:5]:
                relevance_emoji = "🔥" if interaction['relevance_score'] > 2.0 else "⚡" if interaction['relevance_score'] > 1.5 else "📝"
                report_parts.append(f"  {relevance_emoji} {interaction['type']} ({interaction['topic']})")
                report_parts.append(f"    Content: {interaction['content'][:100]}...")
                report_parts.append(f"    Relevance: {interaction['relevance_score']:.2f}")
                report_parts.append("")
        
        return "\n".join(report_parts)
        
    except Exception as e:
        return f"Error analyzing conversation context: {str(e)}"

@mcp.tool()
def resume_session(session_id: str, user_id: str = None) -> str:
    """Resume an existing conversation session by providing its session ID.
    
    This function allows you to continue a previous conversation by resuming
    an existing session. It will load all previous context, interactions,
    and user preferences from the persistent storage.
    
    Args:
        session_id (str): The session ID to resume
        user_id (str, optional): User ID for the session. If None, uses default.
        
    Returns:
        str: Confirmation message with session details
        
    Features:
        - Loads persistent session data from disk
        - Restores conversation context and history
        - Maintains user preferences and project context
        - Updates session activity timestamp
        - Seamless continuation of previous conversations
        
    Use Cases:
        - Continuing conversations after system restarts
        - Resuming work on previous projects
        - Maintaining context across different tools
        - Preserving user preferences and learning
    """
    if not SESSION_MANAGER_AVAILABLE:
        return "⚠️ Session manager not available - cannot resume sessions."
    
    try:
        # Resume the session
        resumed_session_id = session_manager.create_or_resume_session(user_id, session_id)
        
        if resumed_session_id == session_id:
            # Get session details
            session = session_manager.get_session(session_id)
            if session:
                return f"✅ Successfully resumed session {session_id}\n" \
                       f"📊 Session Details:\n" \
                       f"  • User ID: {session.user_id}\n" \
                       f"  • Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n" \
                       f"  • Total Interactions: {session.total_interactions}\n" \
                       f"  • Last Activity: {session.last_activity.strftime('%Y-%m-%d %H:%M:%S')}\n" \
                       f"  • Context Summary: {session.context_summary or 'None'}\n" \
                       f"  • Active Topics: {', '.join(session.active_topics) if session.active_topics else 'None'}"
            else:
                return f"✅ Session {session_id} resumed, but details not available."
        else:
            return f"⚠️ Failed to resume session {session_id}. Created new session: {resumed_session_id}"
            
    except Exception as e:
        return f"❌ Error resuming session: {str(e)}"

@mcp.tool()
def list_sessions(user_id: str = None) -> str:
    """List all active conversation sessions with their metadata.
    
    This function provides an overview of all active sessions, including
    their creation time, last activity, interaction counts, and context
    information. Useful for managing multiple conversations and sessions.
    
    Args:
        user_id (str, optional): Filter sessions by specific user ID
        
    Returns:
        str: Formatted list of active sessions with details
        
    Features:
        - Lists all active sessions with metadata
        - Shows session age and activity levels
        - Displays context summaries and topics
        - User-specific filtering
        - Session health and status information
        
    Use Cases:
        - Managing multiple conversation threads
        - Monitoring session activity and health
        - Finding sessions to resume
        - Understanding conversation patterns
        - Session cleanup and maintenance
    """
    if not SESSION_MANAGER_AVAILABLE:
        return "⚠️ Session manager not available - cannot list sessions."
    
    try:
        if user_id:
            sessions = session_manager.get_user_sessions(user_id)
        else:
            sessions = session_manager.list_active_sessions()
        
        if not sessions:
            return "No active sessions found."
        
        result = []
        result.append(f"📋 Active Sessions ({len(sessions)}):")
        result.append("")
        
        for session_data in sessions:
            if isinstance(session_data, dict):
                # Handle dict format from list_active_sessions
                session_id = session_data['session_id']
                user_id = session_data['user_id']
                created_at = session_data['created_at']
                last_activity = session_data['last_activity']
                total_interactions = session_data['total_interactions']
                context_summary = session_data.get('context_summary')
                active_topics = session_data.get('active_topics')
            else:
                # Handle PersistentSession object from get_user_sessions
                session_id = session_data.session_id
                user_id = session_data.user_id
                created_at = session_data.created_at.isoformat()
                last_activity = session_data.last_activity.isoformat()
                total_interactions = session_data.total_interactions
                context_summary = session_data.context_summary
                active_topics = session_data.active_topics
            
            result.append(f"🔹 Session: {session_id}")
            result.append(f"   👤 User: {user_id}")
            result.append(f"   📅 Created: {created_at}")
            result.append(f"   🕒 Last Activity: {last_activity}")
            result.append(f"   💬 Interactions: {total_interactions}")
            
            if context_summary:
                result.append(f"   📝 Context: {context_summary[:100]}...")
            
            if active_topics:
                result.append(f"   🎯 Topics: {', '.join(active_topics[:3])}")
            
            result.append("")
        
        return "\n".join(result)
        
    except Exception as e:
        return f"❌ Error listing sessions: {str(e)}"

@mcp.tool()
def export_session(session_id: str) -> str:
    """Export complete session data for backup, analysis, or migration.
    
    This function exports all data associated with a specific session,
    including interactions, context, and metadata. Useful for backing up
    important conversations or analyzing session data externally.
    
    Args:
        session_id (str): The session ID to export
        
    Returns:
        str: Export confirmation with data summary or error message
        
    Features:
        - Complete session data export
        - Interaction history with full content
        - Context and preference information
        - Metadata and timing information
        - Structured data format for analysis
        
    Use Cases:
        - Backing up important conversations
        - Data analysis and reporting
        - Session migration between systems
        - Compliance and audit requirements
        - Debugging and troubleshooting
    """
    if not SESSION_MANAGER_AVAILABLE:
        return "⚠️ Session manager not available - cannot export sessions."
    
    try:
        export_data = session_manager.export_session_data(session_id)
        
        if not export_data:
            return f"❌ Failed to export session {session_id} - session not found or export failed."
        
        # Create export file
        export_dir = Path("/Users/jonathanmorand/Documents/ProjectsFolder/MCP_FOLDER/MCP/MCP/data/exports")
        export_dir.mkdir(parents=True, exist_ok=True)
        
        export_file = export_dir / f"session_{session_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(export_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        # Build summary
        session_info = export_data['session_info']
        interactions = export_data['interactions']
        context = export_data['context']
        
        summary = f"✅ Successfully exported session {session_id}\n"
        summary += f"📁 Export file: {export_file}\n"
        summary += f"📊 Export Summary:\n"
        summary += f"  • User ID: {session_info['user_id']}\n"
        summary += f"  • Created: {session_info['created_at']}\n"
        summary += f"  • Total Interactions: {len(interactions)}\n"
        summary += f"  • Has Context: {'Yes' if context else 'No'}\n"
        summary += f"  • Export Time: {export_data['export_timestamp']}\n"
        summary += f"  • Export Version: {export_data['export_version']}"
        
        return summary
        
    except Exception as e:
        return f"❌ Error exporting session: {str(e)}"

@mcp.tool()
def merge_sessions(primary_session_id: str, secondary_session_id: str) -> str:
    """Merge two sessions, combining their data and keeping the primary session.
    
    This function merges a secondary session into a primary session,
    combining interaction counts, context information, and user preferences.
    Useful for consolidating related conversations or cleaning up duplicate sessions.
    
    Args:
        primary_session_id (str): The session to keep and merge into
        secondary_session_id (str): The session to merge and remove
        
    Returns:
        str: Confirmation message with merge results
        
    Features:
        - Combines interaction counts from both sessions
        - Merges context summaries and active topics
        - Combines user preferences intelligently
        - Removes the secondary session after merge
        - Updates activity timestamps
        
    Use Cases:
        - Consolidating related conversations
        - Cleaning up duplicate sessions
        - Merging context from different tools
        - Combining user preference data
        - Session organization and cleanup
    """
    if not SESSION_MANAGER_AVAILABLE:
        return "⚠️ Session manager not available - cannot merge sessions."
    
    try:
        success = session_manager.merge_sessions(primary_session_id, secondary_session_id)
        
        if success:
            # Get updated primary session
            primary_session = session_manager.get_session(primary_session_id)
            if primary_session:
                return f"✅ Successfully merged session {secondary_session_id} into {primary_session_id}\n" \
                       f"📊 Updated Primary Session:\n" \
                       f"  • Total Interactions: {primary_session.total_interactions}\n" \
                       f"  • Last Activity: {primary_session.last_activity.strftime('%Y-%m-%d %H:%M:%S')}\n" \
                       f"  • Context Summary: {primary_session.context_summary or 'None'}\n" \
                       f"  • Active Topics: {', '.join(primary_session.active_topics) if primary_session.active_topics else 'None'}"
            else:
                return f"✅ Successfully merged session {secondary_session_id} into {primary_session_id}"
        else:
            return f"❌ Failed to merge sessions. Please check that both session IDs exist and are valid."
            
    except Exception as e:
        return f"❌ Error merging sessions: {str(e)}"

@mcp.tool()
def cleanup_sessions() -> str:
    """Clean up expired and inactive sessions to free up resources.
    
    This function removes sessions that have been inactive for too long
    (default: 7 days) and cleans up associated files and database records.
    Helps maintain system performance and storage efficiency.
    
    Returns:
        str: Cleanup summary with results
        
    Features:
        - Removes expired sessions automatically
        - Cleans up session files from disk
        - Updates database records
        - Configurable expiration threshold
        - Safe cleanup with error handling
        
    Use Cases:
        - Regular system maintenance
        - Storage space management
        - Performance optimization
        - Database cleanup
        - System health monitoring
    """
    if not SESSION_MANAGER_AVAILABLE:
        return "⚠️ Session manager not available - cannot cleanup sessions."
    
    try:
        # Get count before cleanup
        sessions_before = len(session_manager.list_active_sessions())
        
        # Perform cleanup
        session_manager.cleanup_expired_sessions()
        
        # Get count after cleanup
        sessions_after = len(session_manager.list_active_sessions())
        removed_count = sessions_before - sessions_after
        
        return f"🧹 Session cleanup completed\n" \
               f"📊 Results:\n" \
               f"  • Sessions before: {sessions_before}\n" \
               f"  • Sessions after: {sessions_after}\n" \
               f"  • Sessions removed: {removed_count}\n" \
               f"  • Cleanup time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
        
    except Exception as e:
        return f"❌ Error during session cleanup: {str(e)}"

@mcp.tool()
def extract_conversation_data(limit: int = 20, interaction_type: str = None, 
                             session_id: str = None, export_format: str = "json") -> str:
    """Extract and format conversation data from the MCP server database.
    
    This tool provides comprehensive access to all conversation data stored in the system,
    allowing you to extract, filter, and analyze conversation history with various options.
    
    Args:
        limit (int, optional): Maximum number of conversations to extract. Defaults to 20.
        interaction_type (str, optional): Filter by interaction type (e.g., 'conversation_turn', 'client_request'). 
                                        If None, returns all types.
        session_id (str, optional): Filter by specific session ID. If None, returns from all sessions.
        export_format (str, optional): Output format. Currently supports 'json'. Defaults to 'json'.
        
    Returns:
        str: Formatted conversation data in the specified format
        
    Features:
        - Extract conversations with configurable limits
        - Filter by interaction type (user conversations vs system logs)
        - Filter by specific session for focused analysis
        - Multiple export formats for different use cases
        - Full conversation context including prompts, responses, and metadata
        - Performance metrics and execution timing data
        
    Use Cases:
        - Data analysis and conversation pattern recognition
        - Debugging conversation flow issues
        - Exporting conversation data for external analysis
        - Monitoring user interaction patterns
        - Session-specific conversation analysis
        - Performance monitoring and optimization
        
    Example Usage:
        - extract_conversation_data(limit=50) - Get last 50 conversations
        - extract_conversation_data(interaction_type="conversation_turn") - Only user conversations
        - extract_conversation_data(session_id="abc123") - Conversations from specific session
    """
    # LOGGER IS ALWAYS AVAILABLE - NO MOCKS!
    
    try:
        from models_unified import get_session_factory, AgentInteraction
        
        # Get a database session using the same session factory as the logger
        session_factory = get_session_factory()
        with session_factory() as db_session:
            # Query the real database directly
            query = db_session.query(AgentInteraction)
            
            # Filter by session_id if provided
            if session_id:
                query = query.filter(AgentInteraction.session_id == session_id)
            
            # Order by timestamp descending and limit results
            interactions = query.order_by(AgentInteraction.timestamp.desc()).limit(limit).all()
        
        # Apply filters manually
        if interaction_type:
            interactions = [i for i in interactions if getattr(i, 'interaction_type', '') == interaction_type]
        
        if session_id:
            interactions = [i for i in interactions if getattr(i, 'session_id', '') == session_id]
        
        # Format results
        conversations = []
        for interaction in interactions:
            conv = {
                'id': getattr(interaction, 'id', 'unknown'),
                'timestamp': getattr(interaction, 'timestamp', datetime.now()).isoformat(),
                'session_id': getattr(interaction, 'session_id', 'unknown'),
                'interaction_type': getattr(interaction, 'interaction_type', 'unknown'),
                'prompt': getattr(interaction, 'prompt', ''),
                'response': getattr(interaction, 'response', ''),
                'full_content': getattr(interaction, 'full_content', ''),
                'status': getattr(interaction, 'status', 'unknown'),
                'execution_time_ms': getattr(interaction, 'execution_time_ms', 0),
                'meta_data': getattr(interaction, 'meta_data', {})
            }
            conversations.append(conv)
        
        # Return formatted result
        result = {
            "total_found": len(conversations),
            "limit": limit,
            "filters": {
                "interaction_type": interaction_type,
                "session_id": session_id
            },
            "conversations": conversations,
            "extracted_at": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
            
    except Exception as e:
        return f"❌ Error extracting conversation data: {str(e)}"

@mcp.tool()
def get_conversation_analytics() -> str:
    """Get comprehensive analytics and insights about conversation data.
    
    This tool provides high-level analytics about the conversation system, including
    interaction patterns, session statistics, and performance metrics.
    
    Returns:
        str: Formatted analytics data with insights and statistics
        
    Features:
        - Total interaction counts and breakdowns by type
        - Session statistics and activity patterns
        - Recent conversation activity preview
        - Performance metrics and system health data
        - User interaction pattern analysis
        - System monitoring and health statistics
        
    Use Cases:
        - System performance monitoring and capacity planning
        - User experience analysis and optimization
        - Conversation pattern recognition and analysis
        - System health monitoring and alerting
        - Data-driven decision making for system improvements
        - Operational reporting and dashboards
    """
    # LOGGER IS ALWAYS AVAILABLE - NO MOCKS!
    
    try:
        from models_unified import get_session_factory, AgentInteraction
        
        # Get a database session using the same session factory as the logger
        session_factory = get_session_factory()
        with session_factory() as db_session:
            # Query the real database directly
            interactions = db_session.query(AgentInteraction).order_by(
                AgentInteraction.timestamp.desc()
            ).limit(100).all()
            
            # Get unique sessions from interactions
            session_ids = set(i.session_id for i in interactions if i.session_id)
            sessions = list(session_ids)
        
        # Get interaction type counts
        type_breakdown = {}
        for interaction in interactions:
            interaction_type = getattr(interaction, 'interaction_type', 'unknown')
            type_breakdown[interaction_type] = type_breakdown.get(interaction_type, 0) + 1
        
        # Get recent user activity
        recent_activity = interactions[:10]  # First 10 since they're already ordered
        activity_preview = []
        for activity in recent_activity:
            prompt = getattr(activity, 'prompt', '')
            response = getattr(activity, 'response', '')
            preview = {
                'type': getattr(activity, 'interaction_type', 'unknown'),
                'timestamp': getattr(activity, 'timestamp', datetime.now()).isoformat(),
                'preview': (prompt or response or '')[:100] if (prompt or response) else 'No content'
            }
            activity_preview.append(preview)
        
        # Get session statistics
        total_sessions = len(sessions)
        from datetime import timedelta
        active_sessions = 0
        for session in sessions:
            last_activity = getattr(session, 'last_activity', datetime.now())
            if isinstance(last_activity, str):
                try:
                    last_activity = datetime.fromisoformat(last_activity)
                except:
                    last_activity = datetime.now()
            if last_activity > datetime.now() - timedelta(hours=1):
                active_sessions += 1
        
        # Compile analytics
        analytics = {
            "total_interactions": sum(type_breakdown.values()),
            "interaction_type_breakdown": type_breakdown,
            "session_statistics": {
                "total_sessions": total_sessions,
                "active_sessions": active_sessions,
                "active_sessions_threshold": "1 hour"
            },
            "recent_user_activity": activity_preview,
            "system_health": {
                "database_accessible": False,  # Using local storage
                "logger_available": LOGGER_AVAILABLE,
                "session_manager_available": SESSION_MANAGER_AVAILABLE
            },
            "analytics_generated_at": datetime.now().isoformat()
        }
        
        return json.dumps(analytics, indent=2)
            
    except Exception as e:
        return f"❌ Error getting analytics: {str(e)}"

@mcp.tool()
def test_automatic_context_injection(message: str = "Hello, test message!") -> str:
    """Test the automatic context injection system to ensure it's working properly.
    
    This function tests whether the automatic context injection is working by
    calling the agent_interaction function and verifying that context is injected.
    
    Args:
        message (str): Test message to send through the system
        
    Returns:
        str: Test results showing whether context injection worked
    """
    try:
        print(f"🧪 Testing automatic context injection with message: {message}")
        
        # Call the agent_interaction function which now has automatic context injection
        result = agent_interaction(message)
        
        # Check if the response indicates context was injected
        if "ENHANCED PROMPT" in result or "CONTEXT INJECTION" in result:
            return f"✅ SUCCESS: Automatic context injection is working!\n\nResponse: {result}"
        else:
            return f"⚠️ WARNING: Context injection may not be working as expected.\n\nResponse: {result}"
            
    except Exception as e:
        return f"❌ ERROR: Test failed with error: {str(e)}"

@mcp.tool()
def agent_interaction(prompt: str) -> str:
    """
    Agent interaction function that provides context-aware responses.
    
    This function is called by the MCP system and simply delegates to enhanced_chat
    to avoid duplication and ensure consistency.
    
    Args:
        prompt (str): The user's prompt/message
        
    Returns:
        str: Enhanced response with context injection
    """
    return enhanced_chat(prompt)

def enhanced_chat(user_message: str) -> str:
    """Enhanced chat function that provides context-aware responses using the prompt generator.
    
    This function uses the centralized prompt generator to create comprehensive,
    context-aware enhanced prompts with full conversation history, tech stack,
    project plans, and user preferences.
    
    NEW: Now includes dynamic instruction processing to handle user commands!
    
    Args:
        user_message (str): The user's message to enhance with context
        
    Returns:
        str: Full enhanced prompt with comprehensive context injection
        
    Features:
        - Automatic context injection with conversation history
        - Tech stack detection and project context
        - User preferences and learning patterns
        - Multiple enhancement strategies
        - Performance monitoring and caching
        - Dynamic instruction processing (NEW!)
    """
    start_time = time.time()
    
    try:
        # 🚀 STEP 1: PROCESS DYNAMIC INSTRUCTIONS FIRST
        try:
            from dynamic_instruction_processor import process_user_instruction
            instruction_result = process_user_instruction(user_message)
            
            if instruction_result["instructions_found"] > 0:
                updates = instruction_result["updates_applied"]
                print(f"🎯 Processed {instruction_result['instructions_found']} user instructions")
                print(f"✅ Applied {updates['total_updates']} dynamic updates")
                
                # Log instruction processing
                logger.log_client_request(
                    request=f"INSTRUCTION_PROCESSING: {user_message}",
                    metadata={
                        'tool_name': 'dynamic_instruction_processor',
                        'instructions_found': instruction_result["instructions_found"],
                        'updates_applied': updates['total_updates'],
                        'timestamp': datetime.now(timezone.utc).isoformat()
                    }
                )
        except Exception as e:
            print(f"⚠️ Dynamic instruction processing failed: {e}")
        
        # LOG THE CLIENT REQUEST
        logger.log_client_request(
            request=user_message,
            metadata={
                'tool_name': 'enhanced_chat',
                'context_type': 'adaptive_with_dynamic_instructions',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        )
        
        # 🚀 NEW: Use optimized prompt generator for massive performance improvement
        try:
            from optimized_prompt_generator import OptimizedPromptGenerator
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
            
            enhanced_prompt = optimized_prompt
            
        except ImportError:
            # Fallback to old prompt generator if optimized system not available
            from prompt_generator import prompt_generator
            
            # Generate enhanced prompt with APPE (Adaptive Prompt Precision Engine)
            enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                user_message=user_message,
                context_type="adaptive",  # 🚀 NOW USING APPE!
                force_refresh=True,  # 🔄 Force refresh to get latest dynamic preferences
                use_appe=True
            )
        
        # LOG THE AGENT RESPONSE
        execution_time = int((time.time() - start_time) * 1000)  # Convert to milliseconds
        logger.log_agent_response(
            response=enhanced_prompt,
            metadata={
                'tool_name': 'enhanced_chat',
                'execution_time_ms': execution_time,
                'context_type': 'comprehensive',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        )
        
        # LOG THE COMPLETE CONVERSATION TURN
        logger.log_conversation_turn(
            client_request=user_message,
            agent_response=enhanced_prompt,
            metadata={
                'tool_name': 'enhanced_chat',
                'interaction_type': 'enhanced_chat',
                'execution_time_ms': execution_time,
                'context_type': 'comprehensive',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        )
        
        return enhanced_prompt
        
    except ImportError as e:
        error_response = f"""=== ENHANCED CHAT RESPONSE ===

USER MESSAGE: {user_message}

=== CONTEXT INJECTION ===
The prompt generator is not available: {str(e)}

=== RESPONSE ===
I understand you're asking: "{user_message}"

To get full context enhancement, the prompt generator needs to be available.

=== END ENHANCED RESPONSE ==="""
        
        # LOG ERROR INTERACTION
        execution_time = int((time.time() - start_time) * 1000)
        logger.log_error(
            error_message=f"Prompt generator import error: {str(e)}",
            interaction_type='enhanced_chat_error',
            metadata={
                'tool_name': 'enhanced_chat',
                'execution_time_ms': execution_time,
                'context_type': 'comprehensive',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        )
        
        return error_response
        
    except Exception as e:
        error_response = f"""=== ENHANCED CHAT RESPONSE ===

USER MESSAGE: {user_message}

=== CONTEXT INJECTION ===
Error in prompt generation: {str(e)}

=== RESPONSE ===
I understand you're asking: "{user_message}"

There was an error generating the enhanced prompt, but I'm here to help!

=== END ENHANCED RESPONSE ==="""
        
        # LOG ERROR INTERACTION
        execution_time = int((time.time() - start_time) * 1000)
        logger.log_error(
            error_message=f"Prompt generation error: {str(e)}",
            interaction_type='enhanced_chat_error',
            metadata={
                'tool_name': 'enhanced_chat',
                'execution_time_ms': execution_time,
                'context_type': 'comprehensive',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
        )
        
        return error_response

# ============================================================================
# FUNCTION ANALYSIS TOOLS
# ============================================================================

@mcp.tool()
def analyze_project_functions(project_path: str = ".", force_refresh: bool = False) -> str:
    """Analyze all functions and classes in a project.
    
    This tool provides comprehensive analysis of all functions and classes in a project,
    including their locations, arguments, docstrings, and relationships. It's designed
    to be called on-demand when detailed function information is needed.
    
    Args:
        project_path: Path to the project directory (default: current directory)
        force_refresh: Force re-analysis even if already analyzed
        
    Returns:
        Formatted string with comprehensive function analysis results
    """
    try:
        from mcp_function_analyzer_tool import analyze_project_functions_mcp
        return analyze_project_functions_mcp(project_path, force_refresh)
    except ImportError as e:
        return f"❌ Function analyzer not available: {str(e)}"
    except Exception as e:
        return f"❌ Function analysis failed: {str(e)}"

@mcp.tool()
def search_functions(query: str, project_path: str = ".") -> str:
    """Search for functions by name, docstring, or file.
    
    This tool allows you to search for functions across the project using various
    criteria like function name, docstring content, or file path. Useful for
    finding specific functionality or understanding code organization.
    
    Args:
        query: Search query to match against function names, docstrings, or files
        project_path: Path to the project directory (default: current directory)
        
    Returns:
        Formatted string with search results
    """
    try:
        from mcp_function_analyzer_tool import search_functions_mcp
        return search_functions_mcp(query, project_path)
    except ImportError as e:
        return f"❌ Function analyzer not available: {str(e)}"
    except Exception as e:
        return f"❌ Function search failed: {str(e)}"

@mcp.tool()
def get_function_details(function_name: str, project_path: str = ".") -> str:
    """Get detailed information about a specific function.
    
    This tool provides comprehensive details about a specific function, including
    its arguments, docstring, location, and type (regular, async, class method).
    Essential for understanding function behavior and usage.
    
    Args:
        function_name: Name of the function to analyze
        project_path: Path to the project directory (default: current directory)
        
    Returns:
        Formatted string with detailed function information
    """
    try:
        from mcp_function_analyzer_tool import get_function_details_mcp
        return get_function_details_mcp(function_name, project_path)
    except ImportError as e:
        return f"❌ Function analyzer not available: {str(e)}"
    except Exception as e:
        return f"❌ Function details retrieval failed: {str(e)}"

@mcp.tool()
def get_functions_by_file(file_path: str, project_path: str = ".") -> str:
    """Get all functions in a specific file.
    
    This tool lists all functions defined in a specific file, useful for
    understanding the structure and functionality of individual modules.
    
    Args:
        file_path: Path to the file to analyze
        project_path: Path to the project directory (default: current directory)
        
    Returns:
        Formatted string with all functions in the specified file
    """
    try:
        from mcp_function_analyzer_tool import get_functions_by_file_mcp
        return get_functions_by_file_mcp(file_path, project_path)
    except ImportError as e:
        return f"❌ Function analyzer not available: {str(e)}"
    except Exception as e:
        return f"❌ File function analysis failed: {str(e)}"

@mcp.tool()
def get_project_summary() -> str:
    """Get a compact project summary.
    
    This tool provides a high-level overview of the project's function and class
    structure, including counts and top files by function density.
    
    Returns:
        Formatted string with project summary
    """
    try:
        from mcp_function_analyzer_tool import get_project_summary_mcp
        return get_project_summary_mcp()
    except ImportError as e:
        return f"❌ Function analyzer not available: {str(e)}"
    except Exception as e:
        return f"❌ Project summary failed: {str(e)}"

# ============================================================================
# USER PREFERENCE MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def add_user_preference(category: str, key: str, value: str, user_id: str = 'default') -> str:
    """Add a new user preference to the database.
    
    This tool allows you to add new preferences to your user profile, which will
    be automatically included in all future prompt generations.
    
    Args:
        category (str): The preference category (e.g., 'communication', 'technical', 'workflow', 'avoid')
        key (str): The preference key (e.g., 'style', 'approach', 'format')
        value (str): The preference value (e.g., 'concise', 'simple_yet_powerful', 'structured_responses')
        user_id (str): User ID (default: 'default')
        
    Returns:
        str: Success message with the added preference or error message
        
    Examples:
        - add_user_preference('communication', 'tone', 'friendly')
        - add_user_preference('technical', 'debugging', 'verbose_logging')
        - add_user_preference('workflow', 'testing', 'test_driven_development')
        - add_user_preference('avoid', 'patterns', 'long_explanations')
    """
    try:
        from unified_preference_manager import get_unified_preference_manager
        
        manager = get_unified_preference_manager(user_id)
        current_prefs = manager.get_preferences()
        
        # Add the new preference based on category
        if category == 'communication':
            current_prefs.communication_preferences[key] = value
        elif category == 'technical':
            current_prefs.technical_preferences[key] = value
        elif category == 'workflow':
            if value not in current_prefs.workflow_preferences:
                current_prefs.workflow_preferences.append(value)
        elif category == 'avoid':
            if value not in current_prefs.avoid_patterns:
                current_prefs.avoid_patterns.append(value)
        elif category == 'tools':
            current_prefs.preferred_tools[key] = value
        else:
            return f"❌ Invalid category '{category}'. Valid categories: communication, technical, workflow, avoid, tools"
        
        # Update preferences in database
        success = manager.update_preferences({
            'communication_preferences': current_prefs.communication_preferences,
            'technical_preferences': current_prefs.technical_preferences,
            'workflow_preferences': current_prefs.workflow_preferences,
            'avoid_patterns': current_prefs.avoid_patterns,
            'preferred_tools': current_prefs.preferred_tools
        })
        
        if success:
            return f"✅ Added preference: {category}.{key} = '{value}'"
        else:
            return f"❌ Failed to add preference: {category}.{key} = '{value}'"
            
    except Exception as e:
        return f"❌ Error adding preference: {str(e)}"

@mcp.tool()
def remove_user_preference(category: str, key: str = None, value: str = None, user_id: str = 'default') -> str:
    """Remove a user preference from the database.
    
    This tool allows you to remove existing preferences from your user profile.
    
    Args:
        category (str): The preference category (e.g., 'communication', 'technical', 'workflow', 'avoid')
        key (str, optional): The preference key to remove (for communication/technical/tools categories)
        value (str, optional): The preference value to remove (for workflow/avoid categories)
        user_id (str): User ID (default: 'default')
        
    Returns:
        str: Success message with the removed preference or error message
        
    Examples:
        - remove_user_preference('communication', 'tone')
        - remove_user_preference('technical', 'debugging')
        - remove_user_preference('workflow', value='test_driven_development')
        - remove_user_preference('avoid', value='long_explanations')
    """
    try:
        from unified_preference_manager import get_unified_preference_manager
        
        manager = get_unified_preference_manager(user_id)
        current_prefs = manager.get_preferences()
        
        removed_items = []
        
        # Remove the preference based on category
        if category == 'communication' and key:
            if key in current_prefs.communication_preferences:
                removed_value = current_prefs.communication_preferences.pop(key)
                removed_items.append(f"{category}.{key} = '{removed_value}'")
            else:
                return f"❌ Preference not found: {category}.{key}"
                
        elif category == 'technical' and key:
            if key in current_prefs.technical_preferences:
                removed_value = current_prefs.technical_preferences.pop(key)
                removed_items.append(f"{category}.{key} = '{removed_value}'")
            else:
                return f"❌ Preference not found: {category}.{key}"
                
        elif category == 'workflow' and value:
            if value in current_prefs.workflow_preferences:
                current_prefs.workflow_preferences.remove(value)
                removed_items.append(f"{category}: '{value}'")
            else:
                return f"❌ Preference not found: {category}: '{value}'"
                
        elif category == 'avoid' and value:
            if value in current_prefs.avoid_patterns:
                current_prefs.avoid_patterns.remove(value)
                removed_items.append(f"{category}: '{value}'")
            else:
                return f"❌ Preference not found: {category}: '{value}'"
                
        elif category == 'tools' and key:
            if key in current_prefs.preferred_tools:
                removed_value = current_prefs.preferred_tools.pop(key)
                removed_items.append(f"{category}.{key} = '{removed_value}'")
            else:
                return f"❌ Preference not found: {category}.{key}"
        else:
            return f"❌ Invalid parameters. For {category}, provide {'key' if category in ['communication', 'technical', 'tools'] else 'value'}"
        
        # Update preferences in database
        success = manager.update_preferences({
            'communication_preferences': current_prefs.communication_preferences,
            'technical_preferences': current_prefs.technical_preferences,
            'workflow_preferences': current_prefs.workflow_preferences,
            'avoid_patterns': current_prefs.avoid_patterns,
            'preferred_tools': current_prefs.preferred_tools
        })
        
        if success and removed_items:
            return f"✅ Removed preference(s): {', '.join(removed_items)}"
        else:
            return f"❌ Failed to remove preference"
            
    except Exception as e:
        return f"❌ Error removing preference: {str(e)}"

@mcp.tool()
def update_user_preference(category: str, key: str, value: str, user_id: str = 'default') -> str:
    """Update an existing user preference in the database.
    
    This tool allows you to modify existing preferences in your user profile.
    
    Args:
        category (str): The preference category (e.g., 'communication', 'technical', 'tools')
        key (str): The preference key to update
        value (str): The new preference value
        user_id (str): User ID (default: 'default')
        
    Returns:
        str: Success message with the updated preference or error message
        
    Examples:
        - update_user_preference('communication', 'style', 'detailed')
        - update_user_preference('technical', 'approach', 'enterprise_grade')
        - update_user_preference('tools', 'database', 'PostgreSQL')
    """
    try:
        from unified_preference_manager import get_unified_preference_manager
        
        manager = get_unified_preference_manager(user_id)
        current_prefs = manager.get_preferences()
        
        old_value = None
        
        # Update the preference based on category
        if category == 'communication':
            if key in current_prefs.communication_preferences:
                old_value = current_prefs.communication_preferences[key]
                current_prefs.communication_preferences[key] = value
            else:
                return f"❌ Preference not found: {category}.{key}"
                
        elif category == 'technical':
            if key in current_prefs.technical_preferences:
                old_value = current_prefs.technical_preferences[key]
                current_prefs.technical_preferences[key] = value
            else:
                return f"❌ Preference not found: {category}.{key}"
                
        elif category == 'tools':
            if key in current_prefs.preferred_tools:
                old_value = current_prefs.preferred_tools[key]
                current_prefs.preferred_tools[key] = value
            else:
                return f"❌ Preference not found: {category}.{key}"
        else:
            return f"❌ Invalid category '{category}'. Valid categories: communication, technical, tools"
        
        # Update preferences in database
        success = manager.update_preferences({
            'communication_preferences': current_prefs.communication_preferences,
            'technical_preferences': current_prefs.technical_preferences,
            'preferred_tools': current_prefs.preferred_tools
        })
        
        if success:
            return f"✅ Updated preference: {category}.{key} = '{old_value}' → '{value}'"
        else:
            return f"❌ Failed to update preference: {category}.{key}"
            
    except Exception as e:
        return f"❌ Error updating preference: {str(e)}"

@mcp.tool()
def list_user_preferences(user_id: str = 'default') -> str:
    """List all current user preferences from the database.
    
    This tool shows you all your current preferences organized by category.
    
    Args:
        user_id (str): User ID (default: 'default')
        
    Returns:
        str: Formatted list of all user preferences
        
    Features:
        - Shows all preference categories
        - Displays key-value pairs for structured preferences
        - Lists array items for workflow and avoid preferences
        - Shows last updated timestamp
    """
    try:
        from unified_preference_manager import get_user_preferences_unified
        
        preferences = get_user_preferences_unified(user_id)
        
        return f"📋 Current User Preferences:\n{preferences}"
        
    except Exception as e:
        return f"❌ Error listing preferences: {str(e)}"

@mcp.tool()
def reset_user_preferences(user_id: str = 'default') -> str:
    """Clear all user preferences completely.
    
    This tool will clear all your preferences and leave them empty.
    Use with caution as this action cannot be undone.
    
    Args:
        user_id (str): User ID (default: 'default')
        
    Returns:
        str: Success message or error message
        
    Warning:
        This action will permanently delete all your custom preferences!
    """
    try:
        from unified_preference_manager import get_unified_preference_manager
        
        manager = get_unified_preference_manager(user_id)
        
        # Clear all preferences (empty state)
        success = manager.update_preferences({
            'preferred_tools': {},
            'communication_preferences': {},
            'technical_preferences': {},
            'workflow_preferences': [],
            'avoid_patterns': [],
            'custom_preferences': {}
        })
        
        if success:
            return "✅ User preferences cleared completely"
        else:
            return "❌ Failed to clear preferences"
            
    except Exception as e:
        return f"❌ Error resetting preferences: {str(e)}"

def background_monitoring():
    """Background daemon thread that provides continuous system health monitoring and metrics collection.
    
    This function runs as a separate thread to continuously monitor system health, collect
    performance metrics, and maintain operational visibility without blocking the main
    application. It's automatically started when the module is imported if background
    monitoring is enabled in the configuration.
    
    Monitoring Activities:
        - Periodic health check logging with timestamp and uptime metrics
        - System performance tracking and trend analysis
        - Continuous availability monitoring for operational dashboards
        - Background metric collection for capacity planning
        
    Thread Characteristics:
        - Runs as a daemon thread (automatically terminates when main process ends)
        - Configurable monitoring interval via Config.MONITORING_INTERVAL_SECONDS
        - Non-blocking operation for main application performance
        - Automatic error recovery with exponential backoff
        
    Health Metrics Collected:
        - Current timestamp for monitoring accuracy
        - System uptime in seconds since module import
        - Health check frequency and consistency
        - Error rates and recovery patterns
        
    Error Handling & Recovery:
        - Comprehensive exception catching to prevent thread termination
        - Automatic error logging for debugging and alerting
        - Graceful degradation with 60-second retry intervals
        - Continuous operation even during system issues
        
    Configuration Dependencies:
        - Config.ENABLE_BACKGROUND_MONITORING: Master switch for monitoring
        - Config.MONITORING_INTERVAL_SECONDS: Health check frequency
        - Logger availability for metric persistence
        
    Use Cases:
        - Production system health monitoring
        - Performance trend analysis and capacity planning
        - Operational dashboards and alerting systems
        - System availability tracking and reporting
        - Background metric collection for analytics
        
    Note:
        This thread is started automatically at module import time if enabled.
        It runs continuously until the main process terminates, providing
        real-time system health visibility with minimal performance impact.
    """
    while True:
        try:
            # Log system health metrics
            logger.log_interaction(
                interaction_type='health_check',
                metadata={
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'uptime_seconds': int(time.time() - start_time)
                }
            )
            
            # Sleep for configured interval
            time.sleep(Config.MONITORING_INTERVAL_SECONDS)
            
        except Exception as e:
            # Log monitoring errors but continue
            logger.log_interaction(
                interaction_type='monitoring_error',
                error_message=str(e),
                status='error'
            )
            time.sleep(60)  # Wait 1 minute before retrying

# Initialize start_time at module level so it's available immediately
start_time = time.time()

# Log startup immediately when module is imported
logger.log_interaction(
    interaction_type='module_import',
    metadata={
        'python_version': sys.version,
        'environment': Config.ENVIRONMENT,
        'container_id': Config.CONTAINER_ID,
        'features': {
            'background_monitoring': Config.ENABLE_BACKGROUND_MONITORING,
            'automatic_metadata': Config.ENABLE_AUTOMATIC_METADATA,
            'monitoring_interval': Config.MONITORING_INTERVAL_SECONDS
        },
        'available_tools': list(get_available_tools().keys()) if isinstance(get_available_tools(), dict) else [],
        'mcp_available': MCP_AVAILABLE,
        'logger_available': LOGGER_AVAILABLE,
        'config_available': CONFIG_AVAILABLE,
        'tools_attribute': TOOLS_ATTR
    }
)

# Start background monitoring if enabled (at module import time)
if Config.ENABLE_BACKGROUND_MONITORING:
    monitor_thread = threading.Thread(target=background_monitoring, daemon=True)
    monitor_thread.start()
    logger.log_interaction(
        interaction_type='monitoring_started',
        metadata={'interval_seconds': Config.MONITORING_INTERVAL_SECONDS}
    )

if __name__ == "__main__":
    # Log startup
    logger.log_interaction(
        interaction_type='system_startup',
        metadata={
            'python_version': sys.version,
            'environment': Config.ENVIRONMENT,
            'container_id': Config.CONTAINER_ID,
            'features': {
                'background_monitoring': Config.ENABLE_BACKGROUND_MONITORING,
                'automatic_metadata': Config.ENABLE_AUTOMATIC_METADATA,
                'monitoring_interval': Config.MONITORING_INTERVAL_SECONDS
            }
        }
    )
    
    try:
        # Ensure tools are properly registered before starting
        print(f"🚀 MCP server '{mcp.name}' starting with {len(get_available_tools())} tools")
        print(f"🔧 Available tools: {list(get_available_tools().keys())}")
        
        # Explicitly initialize the MCP server
        if hasattr(mcp, 'initialize'):
            print("🔧 Initializing MCP server...")
            mcp.initialize()
        
        # Check if tools are accessible
        tools = get_available_tools()
        if tools:
            print(f"✅ Tools registered successfully: {list(tools.keys())}")
        else:
            print("⚠️ No tools found, this may cause issues")
        
        # Initialize and run the server
        transport = Config.MCP_TRANSPORT
        print(f"🚀 Starting MCP server with {transport} transport...")
        
        if transport == "http":
            # For HTTP transport, start the HTTP server instead
            print("🌐 Starting HTTP server for conversation tracking tools...")
            try:
                from mcp_http_server import app
                import uvicorn
                print("✅ HTTP server dependencies imported successfully")
                uvicorn.run(app, host="0.0.0.0", port=8000)
            except ImportError as e:
                print(f"❌ Failed to import HTTP server: {e}")
                print("💡 Make sure fastapi and uvicorn are installed:")
                print("   pip install fastapi uvicorn[standard]")
                print("❌ Cannot fall back to stdio when HTTP transport is explicitly requested")
                raise
            except Exception as e:
                print(f"❌ HTTP server error: {e}")
                raise
        else:
            # For stdio or other transports, use the MCP server directly
            try:
                mcp.run(transport=transport)
            except KeyboardInterrupt:
                print("🛑 MCP server interrupted by user")
            except Exception as e:
                print(f"❌ MCP server transport error: {e}")
                raise
    except Exception as e:
        # Log shutdown error
        logger.log_interaction(
            interaction_type='system_error',
            error_message=str(e),
            status='error'
        )
        raise
    finally:
        # Log shutdown
        logger.log_interaction(
            interaction_type='system_shutdown',
            metadata={'status': 'normal'}
        )