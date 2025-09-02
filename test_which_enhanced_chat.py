#!/usr/bin/env python3
"""
🧪 Test Script: Identify Which Enhanced Chat Function is Being Called
"""

def test_which_enhanced_chat():
    """Test which enhanced_chat function is being called"""
    
    print("🧪 TESTING WHICH ENHANCED CHAT FUNCTION IS BEING CALLED")
    print("=" * 70)
    
    try:
        # Test 1: Check main.py enhanced_chat
        print("1️⃣ Testing main.py enhanced_chat...")
        try:
            from main import enhanced_chat as main_enhanced_chat
            print("✅ main.py enhanced_chat imported successfully")
            
            # Test if it works
            result = main_enhanced_chat("test message")
            print(f"✅ main.py enhanced_chat result length: {len(result)}")
            print(f"📋 Contains context: {'💬 CONTEXT:' in result}")
            print(f"📝 Contains recent: {'📝 RECENT:' in result}")
            print(f"🎯 Contains goals: {'🎯 GOALS:' in result}")
            
        except Exception as e:
            print(f"❌ main.py enhanced_chat failed: {e}")
        
        # Test 2: Check local_mcp_server_simple.py enhanced_chat
        print("\n2️⃣ Testing local_mcp_server_simple.py enhanced_chat...")
        try:
            from local_mcp_server_simple import enhanced_chat as local_enhanced_chat
            print("✅ local_mcp_server_simple.py enhanced_chat imported successfully")
            
            # Test if it works
            result = local_enhanced_chat("test message")
            print(f"✅ local_mcp_server_simple.py enhanced_chat result length: {len(result)}")
            print(f"📋 Contains context: {'💬 CONTEXT:' in result}")
            print(f"📝 Contains recent: {'📝 RECENT:' in result}")
            print(f"🎯 Contains goals: {'🎯 GOALS:' in result}")
            
        except Exception as e:
            print(f"❌ local_mcp_server_simple.py enhanced_chat failed: {e}")
        
        # Test 3: Check which one the MCP system is using
        print("\n3️⃣ Checking MCP system integration...")
        try:
            # Try to import the MCP tools
            from enhanced_mcp_tools import enhanced_prompt_generation
            print("✅ enhanced_mcp_tools.enhanced_prompt_generation available")
            
            # Test the MCP tool
            result = enhanced_prompt_generation("test message")
            print(f"✅ MCP tool result length: {len(result)}")
            print(f"📋 Contains context: {'💬 CONTEXT:' in result}")
            print(f"📝 Contains recent: {'📝 RECENT:' in result}")
            print(f"🎯 Contains goals: {'🎯 GOALS:' in result}")
            
        except Exception as e:
            print(f"❌ MCP tool failed: {e}")
        
        print("\n" + "=" * 70)
        print("🧪 TEST COMPLETE")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_which_enhanced_chat()
