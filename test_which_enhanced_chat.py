#!/usr/bin/env python3
"""
🚀 Test Script: Which enhanced_chat function is being called?
"""

def test_enhanced_chat_sources():
    """Test which enhanced_chat function is being imported and used."""
    
    print("=== 🔍 TESTING ENHANCED_CHAT SOURCES ===\n")
    
    # Test 1: Direct import from local_mcp_server_simple
    try:
        from local_mcp_server_simple import enhanced_chat as local_enhanced_chat
        print("✅ SUCCESS: Imported enhanced_chat from local_mcp_server_simple")
        
        # Test the function
        result = local_enhanced_chat("test message")
        print(f"🚀 Result length: {len(result)}")
        print(f"🚀 Contains OPTIMIZED PROMPT: {'🚀 OPTIMIZED PROMPT:' in result}")
        print(f"🚀 Contains APPE markers: {'=== 🎯 STRATEGY GUIDANCE ===' in result}")
        print()
        
    except Exception as e:
        print(f"❌ FAILED: Import from local_mcp_server_simple: {e}")
        print()
    
    # Test 2: Direct import from main
    try:
        from main import enhanced_chat as main_enhanced_chat
        print("✅ SUCCESS: Imported enhanced_chat from main")
        
        # Test the function
        result = main_enhanced_chat("test message")
        print(f"🚀 Result length: {len(result)}")
        print(f"🚀 Contains OPTIMIZED PROMPT: {'🚀 OPTIMIZED PROMPT:' in result}")
        print(f"🚀 Contains APPE markers: {'=== 🎯 STRATEGY GUIDANCE ===' in result}")
        print()
        
    except Exception as e:
        print(f"❌ FAILED: Import from main: {e}")
        print()
    
    # Test 3: Direct import from enhanced_chat_integration
    try:
        from enhanced_chat_integration import enhanced_chat as integration_enhanced_chat
        print("✅ SUCCESS: Imported enhanced_chat from enhanced_chat_integration")
        
        # Test the function
        result = integration_enhanced_chat("test message")
        print(f"🚀 Result length: {len(result)}")
        print(f"🚀 Contains OPTIMIZED PROMPT: {'🚀 OPTIMIZED PROMPT:' in result}")
        print(f"🚀 Contains APPE markers: {'=== 🎯 STRATEGY GUIDANCE ===' in result}")
        print()
        
    except Exception as e:
        print(f"❌ FAILED: Import from enhanced_chat_integration: {e}")
        print()
    
    # Test 4: Check what the MCP system is actually calling
    print("=== 🔍 MCP SYSTEM ANALYSIS ===")
    try:
        # This simulates what the MCP system might be doing
        import sys
        print(f"🚀 Python path: {sys.path[:3]}...")
        
        # Check if there are multiple enhanced_chat functions
        enhanced_chat_functions = []
        for module_name in ['local_mcp_server_simple', 'main', 'enhanced_chat_integration']:
            try:
                module = __import__(module_name)
                if hasattr(module, 'enhanced_chat'):
                    enhanced_chat_functions.append(f"{module_name}.enhanced_chat")
            except Exception as e:
                print(f"⚠️ Could not check {module_name}: {e}")
        
        print(f"🚀 Found enhanced_chat functions: {enhanced_chat_functions}")
        
    except Exception as e:
        print(f"❌ MCP analysis failed: {e}")

if __name__ == "__main__":
    test_enhanced_chat_sources()
