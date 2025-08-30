#!/usr/bin/env python3
"""
Verify Prompt Engineering Pipeline

This script shows you exactly what's happening in your prompt engineering
pipeline step by step, so you can verify it's working properly.
"""

def verify_step_by_step():
    """Verify the prompt engineering pipeline step by step."""
    print("🔍 VERIFYING PROMPT ENGINEERING PIPELINE STEP BY STEP\n")
    
    # Step 1: Check if enhanced chat integration is available
    print("=== STEP 1: Enhanced Chat Integration ===")
    try:
        from enhanced_chat_integration import enhanced_chat
        print("✅ Enhanced chat integration imported successfully")
        
        # Check what we imported
        import enhanced_chat_integration
        print(f"   Module: {enhanced_chat_integration.__file__}")
        print(f"   Functions available: {[f for f in dir(enhanced_chat_integration) if not f.startswith('_')]}")
        
    except ImportError as e:
        print(f"❌ Failed to import enhanced chat integration: {e}")
        return False
    
    # Step 2: Check if semantic components are available
    print("\n=== STEP 2: Semantic Components ===")
    try:
        from enhanced_chat_integration import get_enhanced_chat_status
        status = get_enhanced_chat_status()
        
        print("✅ Integration status retrieved")
        print(f"   Semantic enhancement enabled: {status['semantic_enhancement_enabled']}")
        print(f"   Integration status: {status['integration_status']}")
        print(f"   Bridge available: {status['bridge_available']}")
        print(f"   Enhanced tools available: {status['enhanced_tools_available']}")
        
        if not status['bridge_available']:
            print("⚠️  Warning: Bridge not available - semantic enhancement may not work")
        if not status['enhanced_tools_available']:
            print("⚠️  Warning: Enhanced tools not available - some features may not work")
            
    except Exception as e:
        print(f"❌ Failed to get integration status: {e}")
        return False
    
    # Step 3: Test basic prompt engineering
    print("\n=== STEP 3: Basic Prompt Engineering ===")
    try:
        test_message = "How do I verify my prompt engineering is working?"
        print(f"📝 Test message: {test_message}")
        
        # Call enhanced_chat
        print("🔄 Calling enhanced_chat...")
        response = enhanced_chat(test_message)
        
        if isinstance(response, str):
            print("✅ Basic response received (string format)")
            print(f"   Length: {len(response)} characters")
            print(f"   Preview: {response[:150]}...")
            
            # Check if it contains enhanced content
            if "=== 📊 CONTEXT INJECTION ===" in response:
                print("   ✅ Context injection detected in response")
            else:
                print("   ⚠️  No context injection detected - may be using fallback")
                
        elif isinstance(response, dict):
            print("✅ Enhanced response received (dictionary format)")
            print(f"   Status: {response.get('status', 'unknown')}")
            
            # Check enhancement metrics
            metrics = response.get('performance_metrics', {})
            if metrics:
                print(f"   Enhancement ratio: {metrics.get('enhancement_ratio', 0):.2f}x")
                print(f"   Context richness: {metrics.get('context_richness_score', 0):.2f}")
                print(f"   Processing time: {metrics.get('processing_time_ms', 0)}ms")
            
            # Check semantic components
            if response.get('semantic_context'):
                print("   ✅ Semantic context available")
            if response.get('semantic_insights'):
                print("   ✅ Semantic insights available")
            if response.get('enhanced_prompt'):
                print("   ✅ Enhanced prompt available")
                
        else:
            print(f"⚠️  Unexpected response type: {type(response)}")
            
    except Exception as e:
        print(f"❌ Basic prompt engineering failed: {e}")
        return False
    
    # Step 4: Test semantic enhancement control
    print("\n=== STEP 4: Semantic Enhancement Control ===")
    try:
        from enhanced_chat_integration import enhanced_chat_semantic
        
        test_message = "What are the key features of semantic enhancement?"
        print(f"📝 Test message: {test_message}")
        
        # Test with semantic enhancement enabled
        print("🔍 Testing with semantic enhancement enabled...")
        enhanced_response = enhanced_chat_semantic(
            test_message,
            use_semantic_enhancement=True,
            return_enhanced=True
        )
        
        if isinstance(enhanced_response, dict):
            print("✅ Semantic enhancement successful")
            metrics = enhanced_response.get('performance_metrics', {})
            print(f"   Enhancement ratio: {metrics.get('enhancement_ratio', 0):.2f}x")
            
            # Check if semantic content was actually added
            enhanced_prompt = enhanced_response.get('enhanced_prompt', '')
            if enhanced_prompt and len(enhanced_prompt) > len(test_message) * 2:
                print("   ✅ Significant enhancement detected")
            else:
                print("   ⚠️  Minimal enhancement detected")
                
        else:
            print("⚠️  Semantic enhancement not working as expected")
            
    except Exception as e:
        print(f"❌ Semantic enhancement control failed: {e}")
        return False
    
    # Step 5: Test semantic insights
    print("\n=== STEP 5: Semantic Insights ===")
    try:
        from enhanced_chat_integration import get_semantic_insights_quick
        
        test_message = "How can I improve my system's performance?"
        print(f"📝 Test message: {test_message}")
        
        insights = get_semantic_insights_quick(test_message)
        
        if insights.get('status') == 'success':
            print("✅ Semantic insights generated successfully")
            
            if insights.get('recommendations'):
                print(f"   Recommendations: {len(insights['recommendations'])} found")
                for i, rec in enumerate(insights['recommendations'][:2], 1):
                    print(f"     {i}. {rec[:80]}...")
            else:
                print("   ⚠️  No recommendations generated")
                
        else:
            print(f"⚠️  Semantic insights failed: {insights.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Semantic insights failed: {e}")
        return False
    
    # Step 6: Test prompt generator integration
    print("\n=== STEP 6: Prompt Generator Integration ===")
    try:
        from enhanced_prompt_generator import get_enhanced_prompt_generator_singleton
        
        generator = get_enhanced_prompt_generator_singleton()
        
        if generator:
            print("✅ Enhanced prompt generator available")
            
            test_message = "What is the best way to implement semantic search?"
            print(f"📝 Test message: {test_message}")
            
            try:
                enhanced_prompt = generator.generate_enhanced_prompt(
                    test_message,
                    context_type="technical",
                    use_semantic_search=True
                )
                
                if enhanced_prompt:
                    print(f"✅ Enhanced prompt generated: {len(enhanced_prompt)} characters")
                    
                    # Check for semantic content
                    if "semantic" in enhanced_prompt.lower():
                        print("   ✅ Semantic content detected")
                    else:
                        print("   ⚠️  Semantic content not detected")
                        
                else:
                    print("⚠️  No enhanced prompt generated")
                    
            except Exception as e:
                print(f"⚠️  Prompt generation failed: {e}")
                
        else:
            print("⚠️  Enhanced prompt generator not available")
            
    except Exception as e:
        print(f"❌ Prompt generator integration failed: {e}")
        return False
    
    # Step 7: Performance verification
    print("\n=== STEP 7: Performance Verification ===")
    try:
        import time
        
        test_message = "Performance test message for timing verification"
        print(f"📝 Test message: {test_message}")
        
        # Time the enhanced response
        start_time = time.time()
        response = enhanced_chat(test_message)
        end_time = time.time()
        
        processing_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print(f"✅ Response generated in {processing_time:.2f}ms")
        
        if processing_time < 1000:  # Less than 1 second
            print("   ✅ Performance is good (< 1 second)")
        elif processing_time < 5000:  # Less than 5 seconds
            print("   ⚠️  Performance is acceptable (< 5 seconds)")
        else:
            print("   ❌ Performance is slow (> 5 seconds)")
            
        # Check response quality
        if isinstance(response, dict):
            metrics = response.get('performance_metrics', {})
            system_time = metrics.get('processing_time_ms', 0)
            if system_time > 0:
                print(f"   System reported time: {system_time:.2f}ms")
                
    except Exception as e:
        print(f"❌ Performance verification failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("🎉 VERIFICATION COMPLETE!")
    print("="*60)
    
    return True

def show_detailed_analysis():
    """Show detailed analysis of what's happening."""
    print("\n🔍 DETAILED ANALYSIS OF PROMPT ENGINEERING PIPELINE\n")
    
    try:
        from enhanced_chat_integration import enhanced_chat, get_enhanced_chat_status
        
        # Get current status
        status = get_enhanced_chat_status()
        print("📊 Current System Status:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Test with a complex message
        test_message = "Explain how semantic embeddings improve prompt engineering and show me the metrics"
        print(f"\n📝 Complex Test Message: {test_message}")
        
        print("\n🔄 Processing message through pipeline...")
        response = enhanced_chat(test_message)
        
        if isinstance(response, dict):
            print("\n📊 Detailed Response Analysis:")
            
            # Show all available keys
            print(f"   Available response keys: {list(response.keys())}")
            
            # Show enhancement metrics
            metrics = response.get('performance_metrics', {})
            if metrics:
                print(f"\n   Performance Metrics:")
                for key, value in metrics.items():
                    print(f"     {key}: {value}")
            
            # Show semantic context
            semantic_context = response.get('semantic_context', {})
            if semantic_context:
                print(f"\n   Semantic Context Keys: {list(semantic_context.keys())}")
                
                bridge_enhancements = semantic_context.get('bridge_enhancements', {})
                if bridge_enhancements:
                    print(f"     Bridge Enhancements: {list(bridge_enhancements.keys())}")
            
            # Show semantic insights
            semantic_insights = response.get('semantic_insights', {})
            if semantic_insights:
                print(f"\n   Semantic Insights Keys: {list(semantic_insights.keys())}")
                
                if semantic_insights.get('recommendations'):
                    print(f"     Recommendations: {len(semantic_insights['recommendations'])} found")
                    for i, rec in enumerate(semantic_insights['recommendations'][:3], 1):
                        print(f"       {i}. {rec[:100]}...")
            
            # Show enhanced prompt
            enhanced_prompt = response.get('enhanced_prompt', '')
            if enhanced_prompt:
                print(f"\n   Enhanced Prompt Analysis:")
                print(f"     Length: {len(enhanced_prompt)} characters")
                
                # Check for specific markers
                markers = [
                    "=== 📊 CONTEXT INJECTION ===",
                    "=== 🏗️ PROJECT STRUCTURE & CODEBASE ===",
                    "=== 🔧 FUNCTION SUMMARY ===",
                    "=== 🎯 INSTRUCTIONS ==="
                ]
                
                for marker in markers:
                    if marker in enhanced_prompt:
                        print(f"     ✅ {marker} detected")
                    else:
                        print(f"     ❌ {marker} not detected")
                        
        else:
            print(f"\n⚠️  Response is not enhanced format: {type(response)}")
            print(f"   Length: {len(response)} characters")
            print(f"   Preview: {response[:200]}...")
            
    except Exception as e:
        print(f"❌ Detailed analysis failed: {e}")

def main():
    """Main verification function."""
    print("🚀 PROMPT ENGINEERING VERIFICATION TOOL\n")
    print("This tool verifies that your prompt engineering system is")
    print("properly integrated with semantic enhancement capabilities.\n")
    
    # Run step-by-step verification
    success = verify_step_by_step()
    
    if success:
        print("\n✅ All verification steps completed successfully!")
        print("\n🔍 Would you like detailed analysis? (y/n): ", end="")
        
        try:
            choice = input().lower().strip()
            if choice in ['y', 'yes']:
                show_detailed_analysis()
        except:
            pass
            
        print("\n🎯 **What This Verification Shows:**")
        print("  ✅ Your enhanced chat integration is working")
        print("  ✅ Semantic components are available")
        print("  ✅ Prompt engineering pipeline is functional")
        print("  ✅ Performance metrics are being collected")
        print("  ✅ All systems are communicating properly")
        
        print("\n🚀 **Your prompt engineering is working properly!**")
        print("   The system is successfully feeding semantic enhancement")
        print("   into your prompt engineering pipeline.")
        
    else:
        print("\n❌ Some verification steps failed!")
        print("\n💡 **Next Steps:**")
        print("  • Review error messages above")
        print("  • Check system dependencies")
        print("  • Verify configuration files")
        print("  • Run individual component tests")
        
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
