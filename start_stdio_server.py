#!/usr/bin/env python3
"""
Start MCP Server in stdio mode for interactive communication
This allows the MCP server to communicate via standard input/output
"""

import asyncio
import sys
import os
import signal
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def start_stdio_server():
    """Start the MCP server in stdio mode"""
    try:
        print("🚀 Starting MCP Server in stdio mode...", file=sys.stderr)
        
        # Import the main MCP server and ensure tools are registered
        from main import mcp
        
        print(f"✅ MCP server loaded: {mcp.name}", file=sys.stderr)
        
        # Ensure tools are properly registered
        tools = getattr(mcp._tool_manager, '_tools', {})
        print(f"🔧 Available tools: {len(tools)}", file=sys.stderr)
        
        # List all available tools
        for tool_name in tools.keys():
            print(f"  📌 {tool_name}", file=sys.stderr)
        
        # Check if the server has stdio support
        if hasattr(mcp, 'run_stdio_async'):
            print("✅ Starting stdio server with async support...", file=sys.stderr)
            print("🔌 Server is now listening for stdio communication...", file=sys.stderr)
            print("💡 You can now connect from Cursor or other MCP clients", file=sys.stderr)
            await mcp.run_stdio_async()
        elif hasattr(mcp, 'run_stdio'):
            print("✅ Starting stdio server with sync support...", file=sys.stderr)
            print("🔌 Server is now listening for stdio communication...", file=sys.stderr)
            print("💡 You can now connect from Cursor or other MCP clients", file=sys.stderr)
            mcp.run_stdio()
        else:
            print("❌ MCP server doesn't support stdio mode", file=sys.stderr)
            print("Available methods:", file=sys.stderr)
            for attr in dir(mcp):
                if 'stdio' in attr.lower() or 'run' in attr.lower():
                    print(f"  - {attr}", file=sys.stderr)
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error starting stdio server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🛑 Received signal {signum}, shutting down...", file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🔌 MCP Server stdio mode", file=sys.stderr)
    print("=" * 40, file=sys.stderr)
    
    try:
        # Start the stdio server
        success = asyncio.run(start_stdio_server())
        
        if success:
            print("✅ MCP Server stdio mode started successfully", file=sys.stderr)
        else:
            print("❌ Failed to start MCP Server stdio mode", file=sys.stderr)
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
