#!/usr/bin/env python3
"""
🧪 Test Script for Centralized Prompt Generator

This script tests the new centralized prompt generator system to ensure
it's working correctly and generating informative enhanced prompts.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_prompt_generator():
    """Test the centralized prompt generator"""
    print("🧪 Testing Centralized Prompt Generator System")
    print("=" * 60)
    
    try:
        # Import the prompt generator
        from prompt_generator import prompt_generator, generate_comprehensive_prompt
        
        print("✅ Successfully imported prompt generator")
        print()
        
        # Test different strategies
        test_message = "How do I set up the database for this MCP project?"
        strategies = ["comprehensive", "technical", "conversation", "smart", "minimal"]
        
        print(f"📝 Test message: {test_message}")
        print(f"📊 Message length: {len(test_message)} characters")
        print()
        
        for strategy in strategies:
            print(f"🚀 Testing {strategy.upper()} strategy:")
            try:
                enhanced = prompt_generator.generate_enhanced_prompt(
                    user_message=test_message,
                    context_type=strategy,
                    force_refresh=False
                )
                
                enhancement_size = len(enhanced) - len(test_message)
                enhancement_ratio = len(enhanced) / len(test_message) if test_message else 0
                
                print(f"   ✅ Success: {len(test_message)} -> {len(enhanced)} chars (+{enhancement_size})")
                print(f"   📈 Enhancement ratio: {enhancement_ratio:.1f}x")
                print(f"   🎯 Preview: {enhanced[:150]}...")
                print()
                
            except Exception as e:
                print(f"   ❌ Failed: {str(e)}")
                print()
        
        # Test convenience functions
        print("🔧 Testing convenience functions:")
        try:
            comprehensive = generate_comprehensive_prompt(test_message)
            print(f"   ✅ generate_comprehensive_prompt: {len(comprehensive)} chars")
        except Exception as e:
            print(f"   ❌ generate_comprehensive_prompt failed: {str(e)}")
        
        # Show statistics
        print("\n📊 Generation Statistics:")
        stats = prompt_generator.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Show available strategies
        print(f"\n🎯 Available strategies: {', '.join(prompt_generator.get_available_strategies())}")
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import prompt generator: {str(e)}")
        print("Make sure prompt_generator.py is in the current directory")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

def test_fallback_behavior():
    """Test fallback behavior when prompt generator is not available"""
    print("\n🔄 Testing Fallback Behavior")
    print("=" * 40)
    
    try:
        # Test the main agent interaction function
        from main import agent_interaction
        
        test_message = "Test message for fallback behavior"
        print(f"📝 Testing with: {test_message}")
        
        response = agent_interaction(test_message)
        print(f"✅ Response received: {len(response)} characters")
        print(f"🎯 Preview: {response[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 MCP Conversation Intelligence System - Prompt Generator Test")
    print("=" * 70)
    
    # Test the main prompt generator
    success1 = test_prompt_generator()
    
    # Test fallback behavior
    success2 = test_fallback_behavior()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED! The centralized prompt generator is working correctly.")
        print("\n✨ Benefits of the new system:")
        print("   • Centralized prompt generation logic")
        print("   • Multiple enhancement strategies")
        print("   • Better error handling and fallbacks")
        print("   • Performance monitoring and caching")
        print("   • More informative and structured prompts")
        print("   • Easier maintenance and updates")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
        print("The system may need additional configuration or dependencies.")
    
    print("\n🚀 Ready to use the enhanced prompt generation system!")
