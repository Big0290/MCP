#!/usr/bin/env python3
"""
🧪 Test Script: Verify Goals/Project Plans Inclusion
"""

def test_goals_inclusion():
    """Test if project plans/goals are now included"""
    
    print("🧪 TESTING GOALS INCLUSION IN OPTIMIZED PROMPTS")
    print("=" * 60)
    
    try:
        # Test 1: Import optimized prompt generator
        print("1️⃣ Testing optimized prompt generator import...")
        from optimized_prompt_generator import OptimizedPromptGenerator
        generator = OptimizedPromptGenerator()
        print("✅ OptimizedPromptGenerator imported successfully")
        
        # Test 2: Create test context with project plans
        print("\n2️⃣ Testing context with project plans...")
        from prompt_generator import PromptContext
        
        # Create test context with project plans
        test_context = PromptContext(
            conversation_summary="Test conversation summary",
            action_history="Test action history",
            tech_stack="Test tech stack",
            project_plans="🎯 PROJECT PLANS & OBJECTIVES:\n1. Build powerful conversation tracking system ✅\n2. Implement context-aware prompt processing ✅\n3. Create intelligent memory management system ✅\n4. Develop user preference learning ✅\n5. Build agent metadata system ✅\n6. Integrate with external AI assistants ✅\n7. Create seamless prompt enhancement pipeline ✅\n8. Implement real-time context injection ✅\n9. Build dynamic instruction processing system ✅\n10. Create adaptive, learning AI assistant ✅",
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
        print("✅ Test context created with project plans")
        
        # Test 3: Test context conversion
        print("\n3️⃣ Testing context conversion...")
        context_dict = generator._context_to_dict(test_context)
        print(f"✅ Context converted to dict")
        print(f"📋 Available keys: {list(context_dict.keys())}")
        print(f"🎯 Project plans available: {'project_plans' in context_dict}")
        
        # Test 4: Test intent classification
        print("\n4️⃣ Testing intent classification...")
        if generator.intent_selector:
            relevant_context, intent_analysis = generator.intent_selector.select_relevant_context(
                "test to see if we now have the goals section with project plans", 
                context_dict
            )
            print(f"✅ Intent classified successfully")
            print(f"🎯 Intent: {intent_analysis.primary_intent.value}")
            print(f"📋 Context requirements: {intent_analysis.context_requirements}")
            print(f"🔧 Selected context: {list(relevant_context.keys())}")
            print(f"🎯 Project plans in selected: {'project_plans' in relevant_context}")
        else:
            print("⚠️ Intent selector not available")
        
        # Test 5: Test conversation context formatting
        print("\n5️⃣ Testing conversation context formatting...")
        conversation_context = generator._format_phase1_conversation_context(context_dict)
        print(f"✅ Conversation context formatted")
        print(f"📋 Result length: {len(conversation_context)}")
        print(f"🎯 Contains goals: {'🎯 GOALS:' in conversation_context}")
        print(f"📋 Formatted result:\n{conversation_context}")
        
        print("\n" + "=" * 60)
        print("🧪 TEST COMPLETE")
        
        # Final assessment
        if '🎯 GOALS:' in conversation_context:
            print("🎉 SUCCESS: Goals section is now included!")
        else:
            print("❌ FAILURE: Goals section is still missing!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_goals_inclusion()
