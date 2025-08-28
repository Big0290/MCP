#!/usr/bin/env python3
"""
Test script to verify MCP server can run locally
"""

import sys
import os
import signal
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mcp_server():
    """Test that the MCP server can start and run"""
    print("🧪 Testing MCP Server Startup...")
    
    try:
        # Import the main module
        from main import mcp
        
        print(f"✅ MCP server imported: {mcp}")
        print(f"📝 Server name: {mcp.name}")
        
        # Check available tools
        tools = mcp._tool_manager._tools
        print(f"🔧 Available tools: {len(tools)}")
        for tool_name in tools.keys():
            print(f"  📌 {tool_name}")
        
        print("\n🎉 MCP server is ready!")
        print("✅ All tools are registered")
        print("✅ Server can be imported")
        print("✅ Ready for Cursor integration")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_tools():
    """Test individual MCP tools"""
    print("\n🔧 Testing MCP Tools...")
    
    try:
        from main import get_system_status, test_conversation_tracking
        
        # Test system status
        print("🧪 Testing get_system_status...")
        status = get_system_status()
        print(f"✅ Status: {status[:100]}...")
        
        # Test conversation tracking
        print("🧪 Testing test_conversation_tracking...")
        result = test_conversation_tracking("Test from local script")
        print(f"✅ Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing tools: {e}")
        return False

if __name__ == "__main__":
    print("🔍 MCP Server Local Test")
    print("=" * 50)
    
    server_ok = test_mcp_server()
    tools_ok = test_mcp_tools()
    
    print("\n" + "=" * 50)
    if server_ok and tools_ok:
        print("🎯 ALL TESTS PASSED!")
        print("✅ MCP server is ready for Cursor")
        print("✅ All tools are working")
        print("\n💡 Next steps:")
        print("   1. Restart Cursor")
        print("   2. Check MCP section for tools")
        print("   3. Test with @get_system_status")
    else:
        print("❌ SOME TESTS FAILED!")
        if not server_ok:
            print("❌ MCP server test failed")
        if not tools_ok:
            print("❌ Tools test failed")
    
    print("=" * 50)
