#!/usr/bin/env python3
"""
🧪 Integration Test: Optimized Prompts in MCP Server

This script tests the integration of optimized prompts into the MCP server.
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_local_mcp_server_integration():
    """Test the local MCP server integration"""
    logger.info("🧪 Testing local MCP server integration...")
    
    try:
        # Test the enhanced_chat function
        from local_mcp_server_simple import enhanced_chat
        
        test_message = "How do I fix this database bug?"
        result = enhanced_chat(test_message)
        
        logger.info(f"✅ Enhanced chat function working")
        logger.info(f"📏 Result length: {len(result):,} characters")
        logger.info(f"🚀 Contains optimization markers: {'🚀 OPTIMIZED PROMPT:' in result}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Local MCP server integration test failed: {e}")
        return False

def test_enhanced_mcp_tools_integration():
    """Test the enhanced MCP tools integration"""
    logger.info("🧪 Testing enhanced MCP tools integration...")
    
    try:
        # Test the enhanced prompt generation
        from enhanced_mcp_tools import EnhancedMCPTools
        
        tools = EnhancedMCPTools()
        result = tools.enhanced_prompt_generation("Test message for optimization")
        
        logger.info(f"✅ Enhanced MCP tools working")
        logger.info(f"📊 Result: {result.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Enhanced MCP tools integration test failed: {e}")
        return False

def test_optimized_prompt_wrapper():
    """Test the optimized prompt wrapper"""
    logger.info("🧪 Testing optimized prompt wrapper...")
    
    try:
        from optimized_prompt_wrapper import (
            generate_optimized_prompt_for_mcp,
            quick_optimize,
            technical_optimize
        )
        
        # Test different optimization types
        test_message = "How do I implement user authentication?"
        
        quick_result = quick_optimize(test_message)
        technical_result = technical_optimize(test_message)
        
        logger.info(f"✅ Optimized prompt wrapper working")
        logger.info(f"📏 Quick optimize: {len(quick_result):,} chars")
        logger.info(f"📏 Technical optimize: {len(technical_result):,} chars")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Optimized prompt wrapper test failed: {e}")
        return False

def test_performance_improvement():
    """Test the actual performance improvement"""
    logger.info("🧪 Testing performance improvement...")
    
    try:
        # Compare old vs new prompt generation
        from prompt_generator import PromptGenerator
        from optimized_prompt_generator import OptimizedPromptGenerator
        
        old_generator = PromptGenerator()
        new_generator = OptimizedPromptGenerator()
        
        test_message = "What should I work on next in my project?"
        
        # Generate old prompt
        old_prompt = old_generator.generate_enhanced_prompt(test_message, 'comprehensive')
        old_size = len(old_prompt)
        
        # Generate new prompt
        new_prompt = new_generator.generate_optimized_prompt(test_message, 'smart')
        new_size = len(new_prompt)
        
        # Calculate improvement
        size_reduction = old_size - new_size
        compression_ratio = (size_reduction / old_size) * 100
        efficiency_gain = old_size / new_size
        
        logger.info(f"🎯 PERFORMANCE IMPROVEMENT RESULTS:")
        logger.info(f"   📏 Old prompt size: {old_size:,} characters")
        logger.info(f"   📏 New prompt size: {new_size:,} characters")
        logger.info(f"   🚀 Size reduction: {size_reduction:,} characters")
        logger.info(f"   📊 Compression ratio: {compression_ratio:.1f}%")
        logger.info(f"   ⚡ Efficiency gain: {efficiency_gain:.1f}x")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Performance improvement test failed: {e}")
        return False

def main():
    """Run all integration tests"""
    logger.info("🚀 Starting MCP Integration Tests...")
    
    tests = [
        ("Local MCP Server", test_local_mcp_server_integration),
        ("Enhanced MCP Tools", test_enhanced_mcp_tools_integration),
        ("Optimized Prompt Wrapper", test_optimized_prompt_wrapper),
        ("Performance Improvement", test_performance_improvement)
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
    logger.info("📊 INTEGRATION TEST SUMMARY")
    logger.info(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"   {status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        logger.info("🎉 All integration tests passed! Optimized prompts are working in MCP server.")
        return True
    else:
        logger.error("⚠️ Some integration tests failed. Check the logs above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
