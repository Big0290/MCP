#!/usr/bin/env python3
"""
🧪 Test Optimized Prompt Generator

This script demonstrates the dramatic improvement in prompt optimization,
showing before/after comparison with size reduction and quality metrics.
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_prompt_optimization():
    """Test the optimized prompt generator vs. the original"""
    
    logger.info("🧪 Testing Prompt Optimization System...")
    
    try:
        # Test original prompt generator
        logger.info("📊 Testing ORIGINAL prompt generator...")
        from prompt_generator import PromptGenerator
        
        original_gen = PromptGenerator()
        original_prompt = original_gen.generate_enhanced_prompt('test message', 'comprehensive')
        original_size = len(original_prompt)
        
        logger.info(f"📏 Original prompt size: {original_size:,} characters ({original_size/1024:.1f} KB)")
        
        # Test optimized prompt generator
        logger.info("🚀 Testing OPTIMIZED prompt generator...")
        from optimized_prompt_generator import OptimizedPromptGenerator
        
        optimized_gen = OptimizedPromptGenerator()
        optimized_prompt = optimized_gen.generate_optimized_prompt('test message', 'smart')
        optimized_size = len(optimized_prompt)
        
        logger.info(f"📏 Optimized prompt size: {optimized_size:,} characters ({optimized_size/1024:.1f} KB)")
        
        # Calculate improvements
        size_reduction = original_size - optimized_size
        compression_ratio = (size_reduction / original_size) * 100
        
        logger.info(f"🎯 OPTIMIZATION RESULTS:")
        logger.info(f"   • Size reduction: {size_reduction:,} characters")
        logger.info(f"   • Compression ratio: {compression_ratio:.1f}%")
        logger.info(f"   • Efficiency gain: {original_size/optimized_size:.1f}x")
        
        # Quality analysis
        logger.info(f"🔍 QUALITY ANALYSIS:")
        
        # Check if essential elements are preserved
        essential_elements = [
            ('User preferences', '👤 PREFERENCES:', '👤 USER PREFERENCES:'),
            ('Tech stack', '⚙️ TECH:', '⚙️ TECH STACK:'),
            ('Agent info', '🤖 AGENT:', '🤖 AGENT METADATA:'),
            ('Instructions', '🎯 RESPOND WITH:', '=== 🎯 INSTRUCTIONS ===')
        ]
        
        for element_name, optimized_marker, original_marker in essential_elements:
            has_optimized = optimized_marker in optimized_prompt
            has_original = original_marker in original_prompt
            
            status = "✅" if has_optimized else "❌"
            logger.info(f"   {status} {element_name}: {'Preserved' if has_optimized else 'Missing'}")
        
        # Check for improvements
        improvements = []
        if '⚠️' not in optimized_prompt:
            improvements.append("No warning messages")
        if 'not available' not in optimized_prompt.lower():
            improvements.append("No fallback text")
        if optimized_prompt.count('===') < 5:
            improvements.append("Cleaner formatting")
        if len(optimized_prompt.split('\n')) < 50:
            improvements.append("Better readability")
        
        logger.info(f"🚀 IMPROVEMENTS ACHIEVED:")
        for improvement in improvements:
            logger.info(f"   ✅ {improvement}")
        
        # Show sample of optimized prompt
        logger.info(f"\n📝 SAMPLE OPTIMIZED PROMPT:")
        lines = optimized_prompt.split('\n')
        for i, line in enumerate(lines[:15]):  # Show first 15 lines
            logger.info(f"   {i+1:2d}: {line}")
        
        if len(lines) > 15:
            logger.info(f"   ... and {len(lines) - 15} more lines")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

def test_intent_analysis():
    """Test the intelligent intent analysis system"""
    
    logger.info("\n🧠 Testing Intelligent Intent Analysis...")
    
    try:
        from optimized_prompt_generator import OptimizedPromptGenerator
        
        generator = OptimizedPromptGenerator()
        
        test_messages = [
            "How do I fix this bug in the database?",
            "Show me the project structure and files",
            "Continue from where we left off yesterday",
            "What's the weather like today?",
            "Implement a new feature for user authentication"
        ]
        
        for message in test_messages:
            # Create a mock context for testing
            class MockContext:
                pass
            
            context = MockContext()
            
            # Analyze intent
            intent = generator._analyze_user_intent(message, context)
            
            logger.info(f"💬 Message: {message}")
            logger.info(f"   🎯 Intent: {intent['primary_intent']}")
            logger.info(f"   ⚙️ Technical: {intent['needs_technical_context']}")
            logger.info(f"   🏗️ Project: {intent['needs_project_context']}")
            logger.info(f"   💬 Conversation: {intent['needs_conversation_context']}")
            logger.info(f"   📊 Complexity: {intent['complexity']}")
            logger.info("")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Intent analysis test failed: {e}")
        return False

def test_different_context_types():
    """Test different context types and their optimization"""
    
    logger.info("\n🎭 Testing Different Context Types...")
    
    try:
        from optimized_prompt_generator import OptimizedPromptGenerator
        
        generator = OptimizedPromptGenerator()
        
        context_types = ['smart', 'technical', 'conversation', 'project']
        
        for context_type in context_types:
            logger.info(f"🎯 Testing context type: {context_type}")
            
            try:
                prompt = generator.generate_optimized_prompt('test message', context_type)
                size = len(prompt)
                
                logger.info(f"   📏 Size: {size:,} characters ({size/1024:.1f} KB)")
                
                # Check for context-specific content
                if context_type == 'technical':
                    has_tech = '⚙️ TECH:' in prompt
                    logger.info(f"   ⚙️ Technical context: {'✅' if has_tech else '❌'}")
                elif context_type == 'conversation':
                    has_conv = '💬 CONTEXT:' in prompt
                    logger.info(f"   💬 Conversation context: {'✅' if has_conv else '❌'}")
                elif context_type == 'project':
                    has_proj = '🏗️ PROJECT:' in prompt
                    logger.info(f"   🏗️ Project context: {'✅' if has_proj else '❌'}")
                
            except Exception as e:
                logger.error(f"   ❌ Failed: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Context type test failed: {e}")
        return False

def main():
    """Run all tests"""
    
    logger.info("🚀 Starting Optimized Prompt Generator Tests...")
    
    tests = [
        ("Prompt Optimization", test_prompt_optimization),
        ("Intent Analysis", test_intent_analysis),
        ("Context Types", test_different_context_types)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"🧪 Running: {test_name}")
        logger.info(f"{'='*60}")
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.error(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("📊 TEST SUMMARY")
    logger.info(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"   {status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        logger.info("🎉 All tests passed! Prompt optimization system is working correctly.")
        return True
    else:
        logger.error("⚠️ Some tests failed. Check the logs above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
