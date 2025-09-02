#!/usr/bin/env python3
"""
🧪 Test Script: Verify Conversation Context Inclusion for General Questions
"""

def test_conversation_context_inclusion():
    """Test if conversation context is included for general questions"""
    
    print("🧪 TESTING CONVERSATION CONTEXT INCLUSION FOR GENERAL QUESTIONS")
    print("=" * 70)
    
    try:
        # Test 1: Import optimized prompt generator
        print("1️⃣ Testing optimized prompt generator import...")
        from optimized_prompt_generator import OptimizedPromptGenerator
        generator = OptimizedPromptGenerator()
        print("✅ OptimizedPromptGenerator imported successfully")
        
        # Test 2: Create test context with all sections
        print("\n2️⃣ Testing context with all sections...")
        from prompt_generator import PromptContext
        
        # Create test context with all sections
        test_context = PromptContext(
            conversation_summary="Test conversation summary with interactions",
            action_history="Test action history with recent actions",
            tech_stack="Test tech stack",
            project_plans="🎯 PROJECT PLANS & OBJECTIVES:\n1. Build powerful conversation tracking system ✅\n2. Implement context-aware prompt processing ✅\n3. Create intelligent memory management system ✅",
            user_preferences="Test user preferences",
            agent_metadata="Test agent metadata",
            recent_interactions=[],
            project_patterns=[],
            best_practices=[],
            common_issues=[],
            development_workflow=[],
            confidence_score=0.9,
            context_type="test"
        )
        print("✅ Test context created with all sections")
        
        # Test 3: Test context conversion
        print("\n3️⃣ Testing context conversion...")
        context_dict = generator._context_to_dict(test_context)
        print(f"✅ Context converted to dict")
        print(f"📋 Available keys: {list(context_dict.keys())}")
        print(f"💬 Conversation summary: {'conversation_summary' in context_dict}")
        print(f"📝 Action history: {'action_history' in context_dict}")
        print(f"🎯 Project plans: {'project_plans' in context_dict}")
        
        # Test 4: Test intent classification for general question
        print("\n4️⃣ Testing intent classification for general question...")
        if generator.intent_selector:
            relevant_context, intent_analysis = generator.intent_selector.select_relevant_context(
                "test to see if we now get conversation context for general questions", 
                context_dict
            )
            print(f"✅ Intent classified successfully")
            print(f"🎯 Intent: {intent_analysis.primary_intent.value}")
            print(f"📋 Context requirements: {intent_analysis.context_requirements}")
            print(f"🔧 Selected context: {list(relevant_context.keys())}")
        else:
            print("⚠️ Intent selector not available")
        
        # Test 5: Test conversation context formatting
        print("\n5️⃣ Testing conversation context formatting...")
        conversation_context = generator._format_phase1_conversation_context(context_dict)
        print(f"✅ Conversation context formatted")
        print(f"📋 Result length: {len(conversation_context)}")
        print(f"💬 Contains context: {'💬 CONTEXT:' in conversation_context}")
        print(f"📝 Contains recent: {'📝 RECENT:' in conversation_context}")
        print(f"🎯 Contains goals: {'🎯 GOALS:' in conversation_context}")
        print(f"📋 Formatted result:\n{conversation_context}")
        
        # Test 6: Test full prompt generation
        print("\n6️⃣ Testing full prompt generation...")
        try:
            full_prompt = generator._create_phase1_optimized_prompt(
                "test to see if we now get conversation context for general questions",
                test_context,
                "smart"
            )
            print(f"✅ Full prompt generated")
            print(f"📋 Prompt length: {len(full_prompt)}")
            print(f"💬 Contains context: {'💬 CONTEXT:' in full_prompt}")
            print(f"📝 Contains recent: {'📝 RECENT:' in full_prompt}")
            print(f"🎯 Contains goals: {'🎯 GOALS:' in full_prompt}")
            print(f"📋 Prompt preview:\n{full_prompt[:500]}...")
        except Exception as e:
            print(f"❌ Full prompt generation failed: {e}")
        
        print("\n" + "=" * 70)
        print("🧪 TEST COMPLETE")
        
        # Final assessment
        if '💬 CONTEXT:' in conversation_context and '📝 RECENT:' in conversation_context and '🎯 GOALS:' in conversation_context:
            print("🎉 SUCCESS: All conversation context sections are now included!")
        else:
            print("❌ FAILURE: Some conversation context sections are still missing!")
            if '💬 CONTEXT:' not in conversation_context:
                print("   ❌ Missing: 💬 CONTEXT")
            if '📝 RECENT:' not in conversation_context:
                print("   ❌ Missing: 📝 RECENT")
            if '🎯 GOALS:' not in conversation_context:
                print("   ❌ Missing: 🎯 GOALS")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_conversation_context_inclusion()
