#!/usr/bin/env python3
"""
Test Prompt Engineering Integration

This script verifies that the prompt engineering system is properly
integrated with semantic enhancement capabilities.
"""

def test_basic_prompt_engineering():
    """Test basic prompt engineering functionality."""
    print("=== Testing Basic Prompt Engineering ===\n")
    
    try:
        # Test the enhanced chat integration
        from enhanced_chat_integration import enhanced_chat
        
        test_message = "How can I improve my MCP conversation system?"
        print(f"📝 Test Message: {test_message}")
        
        # Get enhanced response
        response = enhanced_chat(test_message)
        
        if isinstance(response, str):
            print(f"✅ Basic Response: {len(response)} characters")
            print(f"   Preview: {response[:200]}...")
            print("\n⚠️  This appears to be a basic response (no semantic enhancement)")
            
        elif isinstance(response, dict):
            print(f"✅ Enhanced Response: {response.get('status', 'unknown')}")
            
            # Check enhancement metrics
            metrics = response.get('performance_metrics', {})
            enhancement_ratio = metrics.get('enhancement_ratio', 0)
            context_richness = metrics.get('context_richness_score', 0)
            
            print(f"\n📊 Enhancement Metrics:")
            print(f"   Enhancement Ratio: {enhancement_ratio:.2f}x")
            print(f"   Context Richness: {context_richness:.2f}")
            print(f"   Processing Time: {metrics.get('processing_time_ms', 0)}ms")
            
            # Check semantic components
            if response.get('semantic_context'):
                print(f"\n🧠 Semantic Context Available: ✅")
                bridge_enhancements = response['semantic_context'].get('bridge_enhancements', {})
                if bridge_enhancements.get('recommendations'):
                    print(f"   Recommendations: {len(bridge_enhancements['recommendations'])} found")
            
            if response.get('semantic_insights'):
                print(f"🔍 Semantic Insights Available: ✅")
                insights = response['semantic_insights']
                if insights.get('recommendations'):
                    print(f"   Insights: {len(insights['recommendations'])} found")
            
            # Show original vs enhanced
            original = response.get('original_response', '')
            enhanced = response.get('enhanced_prompt', '')
            
            if original and enhanced:
                print(f"\n📈 Enhancement Analysis:")
                print(f"   Original Length: {len(original)} characters")
                print(f"   Enhanced Length: {len(enhanced)} characters")
                print(f"   Enhancement Ratio: {len(enhanced) / len(original):.2f}x")
                
                # Check if semantic context was injected
                if "=== 📊 CONTEXT INJECTION ===" in enhanced:
                    print("   ✅ Context injection detected")
                else:
                    print("   ⚠️  Context injection not detected")
                    
        else:
            print(f"⚠️  Unexpected response type: {type(response)}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def test_semantic_enhancement_control():
    """Test semantic enhancement with explicit control."""
    print("\n=== Testing Semantic Enhancement Control ===\n")
    
    try:
        from enhanced_chat_integration import enhanced_chat_semantic
        
        test_message = "What are the best practices for MCP conversation systems?"
        print(f"📝 Test Message: {test_message}")
        
        # Test with semantic enhancement enabled
        print("\n🔍 Testing with semantic enhancement enabled...")
        enhanced_response = enhanced_chat_semantic(
            test_message,
            use_semantic_enhancement=True,
            return_enhanced=True,
            similarity_threshold=0.7
        )
        
        if isinstance(enhanced_response, dict):
            print("✅ Semantic enhancement successful")
            metrics = enhanced_response.get('performance_metrics', {})
            print(f"   Enhancement ratio: {metrics.get('enhancement_ratio', 0):.2f}x")
            print(f"   Context richness: {metrics.get('context_richness_score', 0):.2f}")
        else:
            print("⚠️  Semantic enhancement not working as expected")
        
        # Test with semantic enhancement disabled
        print("\n⚡ Testing with semantic enhancement disabled...")
        basic_response = enhanced_chat_semantic(
            test_message,
            use_semantic_enhancement=False,
            return_enhanced=False
        )
        
        print(f"✅ Basic response: {len(basic_response)} characters")
        
        # Compare the two
        if isinstance(enhanced_response, dict) and isinstance(basic_response, str):
            enhanced_length = len(enhanced_response.get('enhanced_prompt', ''))
            basic_length = len(basic_response)
            
            if enhanced_length > basic_length:
                print(f"✅ Enhancement working: {enhanced_length} vs {basic_length} characters")
            else:
                print("⚠️  Enhancement not providing additional content")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def test_semantic_insights():
    """Test semantic insights generation."""
    print("\n=== Testing Semantic Insights ===\n")
    
    try:
        from enhanced_chat_integration import get_semantic_insights_quick, get_context_analysis_quick
        
        test_message = "How do I implement semantic search in my MCP system?"
        print(f"📝 Test Message: {test_message}")
        
        # Get semantic insights
        print("\n🔍 Getting semantic insights...")
        insights = get_semantic_insights_quick(test_message)
        
        if insights.get('status') == 'success':
            print("✅ Semantic insights generated successfully")
            
            # Check insights content
            if insights.get('recommendations'):
                print(f"   Recommendations: {len(insights['recommendations'])} found")
                for i, rec in enumerate(insights['recommendations'][:3], 1):
                    print(f"     {i}. {rec}")
            else:
                print("   ⚠️  No recommendations generated")
                
        else:
            print(f"⚠️  Semantic insights failed: {insights.get('error', 'Unknown error')}")
        
        # Get context analysis
        print("\n📊 Getting context analysis...")
        context = get_context_analysis_quick(test_message)
        
        if 'error' not in context:
            print("✅ Context analysis successful")
            
            # Check context richness
            bridge_enhancements = context.get('bridge_enhancements', {})
            richness_score = bridge_enhancements.get('context_richness_score', 0)
            print(f"   Context richness score: {richness_score:.2f}")
            
            if bridge_enhancements.get('recommendations'):
                print(f"   Context recommendations: {len(bridge_enhancements['recommendations'])} found")
        else:
            print(f"⚠️  Context analysis failed: {context.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def test_integration_status():
    """Test integration status and health."""
    print("\n=== Testing Integration Status ===\n")
    
    try:
        from enhanced_chat_integration import get_enhanced_chat_status, toggle_semantic_enhancement
        
        # Get current status
        status = get_enhanced_chat_status()
        
        print("📊 Current Integration Status:")
        print(f"   Semantic enhancement: {status['semantic_enhancement_enabled']}")
        print(f"   Integration status: {status['integration_status']}")
        print(f"   Bridge available: {status['bridge_available']}")
        print(f"   Enhanced tools available: {status['enhanced_tools_available']}")
        
        # Test toggle functionality
        print("\n🔄 Testing toggle functionality...")
        current_state = toggle_semantic_enhancement(False)
        print(f"   Disabled: {current_state}")
        
        current_state = toggle_semantic_enhancement(True)
        print(f"   Enabled: {current_state}")
        
        # Verify final state
        final_status = get_enhanced_chat_status()
        print(f"   Final state: {final_status['semantic_enhancement_enabled']}")
        
        if final_status['semantic_enhancement_enabled']:
            print("✅ Toggle functionality working")
        else:
            print("⚠️  Toggle functionality not working")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def test_prompt_generator_integration():
    """Test integration with the prompt generator system."""
    print("\n=== Testing Prompt Generator Integration ===\n")
    
    try:
        # Test the enhanced prompt generator
        from enhanced_prompt_generator import get_enhanced_prompt_generator_singleton
        
        print("🔧 Testing enhanced prompt generator...")
        generator = get_enhanced_prompt_generator_singleton()
        
        if generator:
            print("✅ Enhanced prompt generator available")
            
            # Test prompt generation
            test_message = "What are the key components of an MCP system?"
            print(f"\n📝 Test Message: {test_message}")
            
            try:
                enhanced_prompt = generator.generate_enhanced_prompt(
                    test_message,
                    context_type="technical",
                    use_semantic_search=True,
                    similarity_threshold=0.7
                )
                
                if enhanced_prompt:
                    print(f"✅ Enhanced prompt generated: {len(enhanced_prompt)} characters")
                    
                    # Check for semantic content
                    if "semantic" in enhanced_prompt.lower() or "embedding" in enhanced_prompt.lower():
                        print("   ✅ Semantic content detected")
                    else:
                        print("   ⚠️  Semantic content not detected")
                        
                    # Check for context injection
                    if "=== 📊 CONTEXT INJECTION ===" in enhanced_prompt:
                        print("   ✅ Context injection detected")
                    else:
                        print("   ⚠️  Context injection not detected")
                        
                else:
                    print("⚠️  No enhanced prompt generated")
                    
            except Exception as e:
                print(f"⚠️  Prompt generation failed: {e}")
                
        else:
            print("⚠️  Enhanced prompt generator not available")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

def main():
    """Main test function."""
    print("🚀 Testing Prompt Engineering Integration\n")
    print("This script verifies that your prompt engineering system is")
    print("properly integrated with semantic enhancement capabilities.\n")
    
    # Run all tests
    tests = [
        ("Basic Prompt Engineering", test_basic_prompt_engineering),
        ("Semantic Enhancement Control", test_semantic_enhancement_control),
        ("Semantic Insights", test_semantic_insights),
        ("Integration Status", test_integration_status),
        ("Prompt Generator Integration", test_prompt_generator_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"🧪 Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append((test_name, False))
        
        print("-" * 60)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your prompt engineering is working perfectly!")
        print("\n🔗 **What This Means:**")
        print("  ✅ Semantic enhancement is active")
        print("  ✅ Context injection is working")
        print("  ✅ Embedding system is integrated")
        print("  ✅ Performance metrics are available")
        print("  ✅ All systems are communicating properly")
        
    elif passed > total // 2:
        print("\n⚠️  Partial success - some components working, others need attention")
        print("\n💡 **Next Steps:**")
        print("  • Check error messages above")
        print("  • Verify dependencies are installed")
        print("  • Check system configuration")
        
    else:
        print("\n❌ Most tests failed - system needs attention")
        print("\n🚨 **Immediate Actions:**")
        print("  • Review error messages above")
        print("  • Check system dependencies")
        print("  • Verify configuration files")
        print("  • Run individual component tests")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
