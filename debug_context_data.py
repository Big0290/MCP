#!/usr/bin/env python3
"""
🔍 Debug Script: Test what context data is available
"""

def test_context_data():
    """Test what context data is available"""
    
    print("🔍 DEBUGGING CONTEXT DATA AVAILABILITY")
    print("=" * 50)
    
    try:
        # Test 1: Import prompt generator
        print("1️⃣ Testing prompt generator import...")
        from prompt_generator import PromptGenerator
        generator = PromptGenerator()
        print("✅ PromptGenerator imported successfully")
        
        # Test 2: Test context gathering
        print("\n2️⃣ Testing context gathering...")
        context = generator._gather_context_data("test message", "smart")
        print(f"✅ Context gathered successfully")
        print(f"📋 Context type: {type(context)}")
        
        # Test 3: Check context fields
        print("\n3️⃣ Checking context fields...")
        print(f"📋 Conversation summary: {hasattr(context, 'conversation_summary')}")
        if hasattr(context, 'conversation_summary'):
            print(f"   Content: {context.conversation_summary[:100]}...")
        
        print(f"📋 Action history: {hasattr(context, 'action_history')}")
        if hasattr(context, 'action_history'):
            print(f"   Content: {context.action_history[:100]}...")
        
        print(f"📋 User preferences: {hasattr(context, 'user_preferences')}")
        if hasattr(context, 'user_preferences'):
            print(f"   Content: {context.user_preferences[:100]}...")
        
        print(f"📋 Tech stack: {hasattr(context, 'tech_stack')}")
        if hasattr(context, 'tech_stack'):
            print(f"   Content: {context.tech_stack[:100]}...")
        
        # Test 4: Test optimized prompt generator
        print("\n4️⃣ Testing optimized prompt generator...")
        from optimized_prompt_generator import OptimizedPromptGenerator
        opt_generator = OptimizedPromptGenerator()
        print("✅ OptimizedPromptGenerator imported successfully")
        
        # Test 5: Test context conversion
        print("\n5️⃣ Testing context conversion...")
        context_dict = opt_generator._context_to_dict(context)
        print(f"✅ Context converted to dict")
        print(f"📋 Available keys: {list(context_dict.keys())}")
        
        # Test 6: Test intent classification
        print("\n6️⃣ Testing intent classification...")
        if opt_generator.intent_selector:
            relevant_context, intent_analysis = opt_generator.intent_selector.select_relevant_context(
                "test to see if we now have action history and conversation summary", 
                context_dict
            )
            print(f"✅ Intent classified successfully")
            print(f"🎯 Intent: {intent_analysis.primary_intent.value}")
            print(f"📋 Context requirements: {intent_analysis.context_requirements}")
            print(f"🔧 Selected context: {list(relevant_context.keys())}")
        else:
            print("⚠️ Intent selector not available")
        
        print("\n" + "=" * 50)
        print("🔍 DEBUG COMPLETE")
        
    except Exception as e:
        print(f"❌ Error during debugging: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_context_data()
