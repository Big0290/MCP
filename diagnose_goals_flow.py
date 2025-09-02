#!/usr/bin/env python3
"""
🔍 Diagnostic Script: Check Goals Flow and Updates
"""

def diagnose_goals_flow():
    """Diagnose why the goals flow is broken"""
    
    print("🔍 DIAGNOSING GOALS FLOW AND UPDATES")
    print("=" * 60)
    
    try:
        # Test 1: Check if prompt generator is working
        print("1️⃣ Testing prompt generator availability...")
        from prompt_generator import PromptGenerator
        generator = PromptGenerator()
        print("✅ PromptGenerator available")
        
        # Test 2: Check context gathering
        print("\n2️⃣ Testing context gathering...")
        try:
            context = generator._gather_context_data("test goals flow", "smart")
            print("✅ Context gathering successful")
            print(f"📋 Context type: {type(context)}")
            
            # Check specific fields
            print(f"💬 Conversation summary: {hasattr(context, 'conversation_summary')}")
            print(f"📝 Action history: {hasattr(context, 'action_history')}")
            print(f"🎯 Project plans: {hasattr(context, 'project_plans')}")
            
            if hasattr(context, 'project_plans'):
                print(f"🎯 Project plans content: {context.project_plans[:100]}...")
            else:
                print("❌ Project plans field missing!")
                
        except Exception as e:
            print(f"❌ Context gathering failed: {e}")
            return
        
        # Test 3: Check optimized prompt generator
        print("\n3️⃣ Testing optimized prompt generator...")
        try:
            from optimized_prompt_generator import OptimizedPromptGenerator
            opt_generator = OptimizedPromptGenerator()
            print("✅ OptimizedPromptGenerator available")
            
            # Test context conversion
            context_dict = opt_generator._context_to_dict(context)
            print(f"✅ Context conversion successful")
            print(f"📋 Available keys: {list(context_dict.keys())}")
            print(f"🎯 Project plans in dict: {'project_plans' in context_dict}")
            
        except Exception as e:
            print(f"❌ Optimized prompt generator failed: {e}")
            return
        
        # Test 4: Check intent classification
        print("\n4️⃣ Testing intent classification...")
        try:
            if opt_generator.intent_selector:
                relevant_context, intent_analysis = opt_generator.intent_selector.select_relevant_context(
                    "test goals flow and updates", 
                    context_dict
                )
                print(f"✅ Intent classification successful")
                print(f"🎯 Intent: {intent_analysis.primary_intent.value}")
                print(f"📋 Context requirements: {intent_analysis.context_requirements}")
                print(f"🔧 Selected context: {list(relevant_context.keys())}")
                print(f"🎯 Project plans in selected: {'project_plans' in relevant_context}")
            else:
                print("⚠️ Intent selector not available")
        except Exception as e:
            print(f"❌ Intent classification failed: {e}")
        
        # Test 5: Check conversation context formatting
        print("\n5️⃣ Testing conversation context formatting...")
        try:
            conversation_context = opt_generator._format_phase1_conversation_context(context_dict)
            print(f"✅ Conversation context formatting successful")
            print(f"📋 Result length: {len(conversation_context)}")
            print(f"💬 Contains context: {'💬 CONTEXT:' in conversation_context}")
            print(f"📝 Contains recent: {'📝 RECENT:' in conversation_context}")
            print(f"🎯 Contains goals: {'🎯 GOALS:' in conversation_context}")
            print(f"📋 Formatted result:\n{conversation_context}")
        except Exception as e:
            print(f"❌ Conversation context formatting failed: {e}")
        
        # Test 6: Check essential context safeguard
        print("\n6️⃣ Testing essential context safeguard...")
        try:
            # Create a filtered context that's missing some sections
            filtered_context = {'user_preferences': 'test', 'agent_metadata': 'test'}
            safeguarded_context = opt_generator._ensure_essential_context(filtered_context, context_dict)
            print(f"✅ Essential context safeguard successful")
            print(f"📋 Safeguarded keys: {list(safeguarded_context.keys())}")
            print(f"🎯 Project plans safeguarded: {'project_plans' in safeguarded_context}")
        except Exception as e:
            print(f"❌ Essential context safeguard failed: {e}")
        
        print("\n" + "=" * 60)
        print("🔍 DIAGNOSIS COMPLETE")
        
        # Final assessment
        if '🎯 GOALS:' in conversation_context:
            print("🎉 SUCCESS: Goals flow is working!")
        else:
            print("❌ FAILURE: Goals flow is broken!")
            print("🔍 Check the diagnostic output above for issues")
        
    except Exception as e:
        print(f"❌ Error during diagnosis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_goals_flow()
