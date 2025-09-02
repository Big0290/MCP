#!/usr/bin/env python3
"""
🧪 Test Script: Verify Goals Flow Fix for Technical Questions
"""

def test_goals_flow_fix():
    """Test if technical questions now include conversation context"""
    
    print("🧪 TESTING GOALS FLOW FIX FOR TECHNICAL QUESTIONS")
    print("=" * 70)
    
    try:
        # Test 1: Import optimized prompt generator
        print("1️⃣ Testing optimized prompt generator import...")
        from optimized_prompt_generator import OptimizedPromptGenerator
        generator = OptimizedPromptGenerator()
        print("✅ OptimizedPromptGenerator imported successfully")
        
        # Test 2: Create test context
        print("\n2️⃣ Testing with technical question...")
        from prompt_generator import PromptContext
        
        test_context = PromptContext(
            conversation_summary="Test conversation summary",
            action_history="Test action history",
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
        
        # Test 3: Test intent classification for technical question
        print("\n3️⃣ Testing intent classification for technical question...")
        context_dict = generator._context_to_dict(test_context)
        
        if generator.intent_selector:
            relevant_context, intent_analysis = generator.intent_selector.select_relevant_context(
                "test goals flow and updates", 
                context_dict
            )
            print(f"✅ Intent classification successful")
            print(f"🎯 Intent: {intent_analysis.primary_intent.value}")
            print(f"📋 Context requirements: {intent_analysis.context_requirements}")
            print(f"🔧 Selected context: {list(relevant_context.keys())}")
        else:
            print("⚠️ Intent selector not available")
            return
        
        # Test 4: Test full prompt generation
        print("\n4️⃣ Testing full prompt generation...")
        try:
            full_prompt = generator._create_phase1_optimized_prompt(
                "test goals flow and updates",
                test_context,
                "smart"
            )
            print(f"✅ Full prompt generated")
            print(f"📋 Prompt length: {len(full_prompt)}")
            print(f"💬 Contains context: {'💬 CONTEXT:' in full_prompt}")
            print(f"📝 Contains recent: {'📝 RECENT:' in full_prompt}")
            print(f"🎯 Contains goals: {'🎯 GOALS:' in full_prompt}")
            
            # Show the relevant section
            if '💬 CONTEXT:' in full_prompt:
                context_start = full_prompt.find('💬 CONTEXT:')
                context_end = full_prompt.find('\n\n', context_start)
                if context_end == -1:
                    context_end = len(full_prompt)
                context_section = full_prompt[context_start:context_end]
                print(f"📋 Conversation context section:\n{context_section}")
            else:
                print("❌ No conversation context section found!")
                
        except Exception as e:
            print(f"❌ Full prompt generation failed: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 70)
        print("🧪 TEST COMPLETE")
        
        # Final assessment
        if '💬 CONTEXT:' in full_prompt and '🎯 GOALS:' in full_prompt:
            print("🎉 SUCCESS: Technical questions now include conversation context with goals!")
        else:
            print("❌ FAILURE: Technical questions still missing conversation context!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_goals_flow_fix()
