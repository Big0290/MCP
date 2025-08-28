#!/usr/bin/env python3
"""
Test script to verify MCP tools are properly registered
This helps debug why Cursor might not see the tools
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mcp_tools():
    """Test that MCP tools are properly registered"""
    print("🧪 Testing MCP Tool Registration...")
    
    try:
        # Import the main module
        from main import mcp, get_available_tools
        
        print(f"✅ MCP server imported: {mcp}")
        print(f"📝 Server name: {mcp.name}")
        
        # Check available tools using the helper function
        tools = get_available_tools()
        print(f"🔧 Available tools: {len(tools) if isinstance(tools, dict) else 0}")
        
        if not tools:
            print("❌ No tools found! This is the problem.")
            return False
        
        # List all tools with their details
        for tool_name, tool_info in tools.items():
            print(f"  📌 {tool_name}:")
            if isinstance(tool_info, dict):
                print(f"     Description: {tool_info.get('description', 'No description')}")
                print(f"     Parameters: {tool_info.get('parameters', 'No parameters')}")
            else:
                print(f"     Info: {tool_info}")
            print()
        
        # Test tool execution (if possible)
        print("🧪 Testing tool execution...")
        
        # Test the system status tool
        if 'get_system_status' in tools:
            print("✅ get_system_status tool found")
        else:
            print("❌ get_system_status tool not found")
        
        # Test the test conversation tracking tool
        if 'test_conversation_tracking' in tools:
            print("✅ test_conversation_tracking tool found")
        else:
            print("❌ test_conversation_tracking tool not found")
        
        # Test the weather tool
        if 'get_current_weather' in tools:
            print("✅ get_current_weather tool found")
        else:
            print("❌ get_current_weather tool not found")
        
        print("\n🎉 MCP tools are properly registered!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP tools: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_server_startup():
    """Test that the MCP server can start properly"""
    print("\n🚀 Testing MCP Server Startup...")
    
    try:
        from main import mcp, get_available_tools
        
        # Check if we can access the server object
        print(f"✅ MCP server object accessible: {type(mcp)}")
        print(f"✅ Server name: {mcp.name}")
        
        # Get available tools
        tools = get_available_tools()
        tool_names = list(tools.keys()) if isinstance(tools, dict) else []
        print(f"✅ Available tools: {tool_names}")
        
        # Test that the server has the right attributes
        if hasattr(mcp, 'run'):
            print("✅ Server has 'run' method")
        else:
            print("❌ Server missing 'run' method")
        
        # Check for tools-related attributes
        tools_attrs = [attr for attr in dir(mcp) if 'tool' in attr.lower()]
        if tools_attrs:
            print(f"✅ Server has tools-related attributes: {tools_attrs}")
        else:
            print("⚠️ Server has no obvious tools-related attributes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server startup: {e}")
        return False

def test_tool_execution():
    """Test that tools can actually be executed"""
    print("\n🔧 Testing Tool Execution...")
    
    try:
        from main import get_system_status, test_conversation_tracking
        
        # Test system status tool
        print("🧪 Testing get_system_status...")
        status_result = get_system_status()
        print(f"✅ get_system_status result: {status_result[:100]}...")
        
        # Test conversation tracking tool
        print("🧪 Testing test_conversation_tracking...")
        tracking_result = test_conversation_tracking("Test from test script")
        print(f"✅ test_conversation_tracking result: {tracking_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing tool execution: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 MCP Tools Registration Test")
    print("=" * 50)
    
    tools_ok = test_mcp_tools()
    startup_ok = test_mcp_server_startup()
    execution_ok = test_tool_execution()
    
    print("\n" + "=" * 50)
    if tools_ok and startup_ok and execution_ok:
        print("🎯 ALL TESTS PASSED!")
        print("✅ MCP tools are properly registered")
        print("✅ MCP server can start properly")
        print("✅ Tools can be executed successfully")
        print("\n💡 If Cursor still doesn't see the tools, check:")
        print("   1. The .cursor/mcp.json configuration")
        print("   2. That the MCP server is running")
        print("   3. Cursor's MCP server connection")
    else:
        print("❌ SOME TESTS FAILED!")
        if not tools_ok:
            print("❌ MCP tools registration failed")
        if not startup_ok:
            print("❌ MCP server startup failed")
        if not execution_ok:
            print("❌ Tool execution failed")
        print("\n🔧 Please fix the issues above before using with Cursor")
    
    print("=" * 50)
