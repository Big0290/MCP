#!/usr/bin/env python3
"""
Local MCP server that connects to the HTTP endpoints of the Docker container
This allows MCP clients to use stdio transport while the actual server runs in Docker
"""

import json
import sys
import requests
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

# HTTP server URL
HTTP_SERVER_URL = "http://localhost:8000"

# Initialize FastMCP server
mcp = FastMCP("mcp-project")

def make_http_request(tool_name: str, **kwargs) -> str:
    """Make HTTP request to the Docker container"""
    try:
        # Debug: Print the request details
        print(f"🔍 Making HTTP request to: {HTTP_SERVER_URL}/tool/{tool_name}")
        print(f"🔍 Request parameters: {kwargs}")
        
        response = requests.post(
            f"{HTTP_SERVER_URL}/tool/{tool_name}",
            json=kwargs,
            timeout=30
        )
        
        # Debug: Print response details
        print(f"🔍 Response status: {response.status_code}")
        print(f"🔍 Response headers: {dict(response.headers)}")
        
        response.raise_for_status()
        result = response.json()
        
        # Debug: Print the result
        print(f"🔍 Response result: {result}")
        
        return result.get("result", "No result returned")
    except requests.exceptions.RequestException as e:
        error_msg = f"Error making HTTP request: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg
    except Exception as e:
        error_msg = f"Error processing response: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

@mcp.tool()
def get_conversation_summary(session_id: str = None) -> str:
    """Generate comprehensive conversation statistics and pattern analysis from the database."""
    return make_http_request("get_conversation_summary", session_id=session_id)

@mcp.tool()
def get_interaction_history(limit: int = 10, session_id: str = None) -> str:
    """Retrieve conversation history from the database for analysis, debugging, and monitoring."""
    return make_http_request("get_interaction_history", limit=limit, session_id=session_id)

@mcp.tool()
def get_system_status(random_string: str = None) -> str:
    """Get comprehensive system status including health, tool availability, and configuration."""
    return make_http_request("get_system_status")

@mcp.tool()
def agent_interaction(prompt: str) -> str:
    """Interact with the agent by processing a user prompt and generating a response."""
    return make_http_request("agent_interaction", prompt=prompt)

@mcp.tool()
def test_conversation_tracking(message: str = "Hello, world!") -> str:
    """Test the conversation tracking system by logging a test message."""
    return make_http_request("test_conversation_tracking", message=message)

@mcp.tool()
def get_current_weather(city: str = "") -> str:
    """Get current weather information for a specified city with conversation tracking."""
    return make_http_request("get_current_weather", city=city)

@mcp.tool()
def inject_conversation_context(prompt: str, session_id: str = None) -> str:
    """Inject conversation context into a prompt for enhanced AI responses."""
    return make_http_request("inject_conversation_context", prompt=prompt, session_id=session_id)

@mcp.tool()
def get_conversation_context(session_id: str = None) -> str:
    """Get detailed conversation context for a specific session."""
    return make_http_request("get_conversation_context", session_id=session_id)

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
    """
    return make_http_request("extract_conversation_data", 
                           limit=limit, 
                           interaction_type=interaction_type, 
                           session_id=session_id, 
                           export_format=export_format)

@mcp.tool()
def get_conversation_analytics() -> str:
    """Get comprehensive analytics and insights about conversation data.
    
    This tool provides high-level analytics about the conversation system, including
    interaction patterns, session statistics, and performance metrics.
    
    Returns:
        str: Formatted analytics data with insights and statistics
    """
    return make_http_request("get_conversation_analytics")

if __name__ == "__main__":
    print("🚀 Starting Local MCP Server...")
    print("🔗 Connecting to Docker HTTP server at:", HTTP_SERVER_URL)
    print("📋 Available tools:")
    print("   - get_conversation_summary")
    print("   - get_interaction_history")
    print("   - get_system_status")
    print("   - agent_interaction")
    print("   - test_conversation_tracking")
    print("   - get_current_weather")
    print("   - inject_conversation_context")
    print("   - get_conversation_context")
    print("   - extract_conversation_data")
    print("   - get_conversation_analytics")
    
    try:
        # Test connection to HTTP server
        response = requests.get(f"{HTTP_SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ HTTP server is accessible")
        else:
            print("⚠️ HTTP server returned status:", response.status_code)
    except Exception as e:
        print("❌ Cannot connect to HTTP server:", str(e))
        print("💡 Make sure the Docker containers are running:")
        print("   docker-compose -f docker-compose.mcp.yml up -d")
        sys.exit(1)
    
    print("🚀 Starting MCP server with stdio transport...")
    mcp.run(transport="stdio")
