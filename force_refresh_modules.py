#!/usr/bin/env python3
"""
🚀 Force Refresh All Modules - Clear Python Caching Issues
"""

import sys
import importlib

def force_refresh_modules():
    """Force refresh all relevant modules to clear caching issues."""
    
    print("=== 🚀 FORCING MODULE REFRESH ===\n")
    
    # List of modules to refresh
    modules_to_refresh = [
        'local_mcp_server_simple',
        'main', 
        'enhanced_chat_integration',
        'optimized_prompt_generator',
        'prompt_generator'
    ]
    
    refreshed_count = 0
    
    for module_name in modules_to_refresh:
        try:
            if module_name in sys.modules:
                # Force reload the module
                module = importlib.reload(sys.modules[module_name])
                print(f"✅ REFRESHED: {module_name}")
                refreshed_count += 1
            else:
                print(f"⚠️ NOT LOADED: {module_name}")
        except Exception as e:
            print(f"❌ FAILED TO REFRESH {module_name}: {e}")
    
    print(f"\n🚀 Total modules refreshed: {refreshed_count}")
    
    # Test if the refresh worked
    print("\n=== 🧪 TESTING REFRESH RESULTS ===")
    
    try:
        from local_mcp_server_simple import enhanced_chat as local_enhanced_chat
        result = local_enhanced_chat("test after refresh")
        print(f"✅ Local enhanced_chat: {len(result)} chars, OPTIMIZED: {'🚀 OPTIMIZED PROMPT:' in result}")
    except Exception as e:
        print(f"❌ Local enhanced_chat test failed: {e}")
    
    try:
        from main import enhanced_chat as main_enhanced_chat
        result = main_enhanced_chat("test after refresh")
        print(f"✅ Main enhanced_chat: {len(result)} chars, OPTIMIZED: {'🚀 OPTIMIZED PROMPT:' in result}")
    except Exception as e:
        print(f"❌ Main enhanced_chat test failed: {e}")
    
    print("\n=== 🎯 NEXT STEPS ===")
    print("1. ✅ Modules refreshed")
    print("2. 🔄 Restart your MCP server")
    print("3. 🧪 Test enhanced_chat again")
    print("4. 🚀 Should now see optimized prompts!")

if __name__ == "__main__":
    force_refresh_modules()
