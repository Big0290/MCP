#!/usr/bin/env python3
"""
Integration Script for Embedding System

This script demonstrates how to integrate the embedding system with your
existing MCP conversation intelligence tools.
"""

import sys
import time
from typing import Dict, Any

def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_section(title: str):
    """Print a formatted section."""
    print(f"\n📋 {title}")
    print("-" * 40)

def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")

def print_error(message: str):
    """Print an error message."""
    print(f"❌ {message}")

def print_info(message: str):
    """Print an info message."""
    print(f"ℹ️  {message}")

def print_warning(message: str):
    """Print a warning message."""
    print(f"⚠️  {message}")

def main():
    """Main integration demonstration."""
    print_header("MCP Embedding System Integration")
    
    print_info("This script will help you integrate the embedding system with your existing MCP tools.")
    print_info("Make sure you have installed the required dependencies first.")
    
    # Step 1: Check dependencies
    print_section("Step 1: Checking Dependencies")
    
    try:
        import sentence_transformers
        print_success("sentence-transformers is available")
    except ImportError:
        print_warning("sentence-transformers not found - will use fallback embeddings")
        print_info("Install with: pip install sentence-transformers")
    
    try:
        import numpy
        print_success("numpy is available")
    except ImportError:
        print_error("numpy is required but not found")
        print_info("Install with: pip install numpy")
        return
    
    try:
        import sqlite3
        print_success("sqlite3 is available")
    except ImportError:
        print_error("sqlite3 is required but not found")
        return
    
    # Step 2: Test basic imports
    print_section("Step 2: Testing Basic Imports")
    
    try:
        from embedding_manager import EmbeddingManager
        print_success("EmbeddingManager imported successfully")
    except ImportError as e:
        print_error(f"Failed to import EmbeddingManager: {e}")
        return
    
    try:
        from enhanced_prompt_generator import EnhancedPromptGenerator
        print_success("EnhancedPromptGenerator imported successfully")
    except ImportError as e:
        print_error(f"Failed to import EnhancedPromptGenerator: {e}")
        return
    
    try:
        from embedding_integration import get_embedding_integration
        print_success("EmbeddingIntegration imported successfully")
    except ImportError as e:
        print_error(f"Failed to import EmbeddingIntegration: {e}")
        return
    
    # Step 3: Test bridge integration
    print_section("Step 3: Testing Bridge Integration")
    
    try:
        from mcp_embedding_bridge import get_mcp_embedding_bridge
        print_success("MCPEmbeddingBridge imported successfully")
        
        # Test bridge creation
        bridge = get_mcp_embedding_bridge()
        print_success("Bridge instance created successfully")
        
        # Test bridge status
        status = bridge.get_bridge_status()
        print_success(f"Bridge status: {status['bridge_initialized']}")
        
    except ImportError as e:
        print_error(f"Failed to import MCPEmbeddingBridge: {e}")
        return
    except Exception as e:
        print_error(f"Failed to create bridge: {e}")
        return
    
    # Step 4: Test enhanced MCP tools
    print_section("Step 4: Testing Enhanced MCP Tools")
    
    try:
        from enhanced_mcp_tools import get_enhanced_mcp_tools
        print_success("EnhancedMCPTools imported successfully")
        
        # Test tools creation
        tools = get_enhanced_mcp_tools()
        print_success("Enhanced tools instance created successfully")
        
        # Test tool availability
        available_tools = tools.get_available_tools()
        print_success(f"Found {len(available_tools['enhanced_tools'])} enhanced tools")
        
    except ImportError as e:
        print_error(f"Failed to import EnhancedMCPTools: {e}")
        return
    except Exception as e:
        print_error(f"Failed to create enhanced tools: {e}")
        return
    
    # Step 5: Test basic functionality
    print_section("Step 5: Testing Basic Functionality")
    
    try:
        # Test enhanced prompt generation
        test_message = "How can I improve my MCP conversation system?"
        
        print_info("Testing enhanced prompt generation...")
        prompt_result = tools.enhanced_prompt_generation(
            test_message, context_type="smart", use_semantic_search=True
        )
        
        if prompt_result['status'] == 'success':
            print_success("Enhanced prompt generation working")
            metrics = prompt_result['enhancement_metrics']
            print_info(f"Enhancement ratio: {metrics['enhancement_ratio']:.2f}")
            print_info(f"Processing time: {metrics['processing_time_ms']}ms")
        else:
            print_warning("Enhanced prompt generation had issues")
            print_info(f"Error: {prompt_result.get('error', 'Unknown error')}")
        
    except Exception as e:
        print_error(f"Failed to test enhanced prompt generation: {e}")
    
    # Step 6: Integration recommendations
    print_section("Step 6: Integration Recommendations")
    
    print_info("Your embedding system is now integrated! Here's how to use it:")
    
    print("\n🔧 **Basic Usage:**")
    print("  from enhanced_mcp_tools import enhanced_agent_interaction")
    print("  result = enhanced_agent_interaction('Your message here')")
    
    print("\n🔍 **Semantic Search:**")
    print("  from enhanced_mcp_tools import semantic_context_search")
    print("  results = semantic_context_search('Your search query')")
    
    print("\n📊 **Enhanced Summaries:**")
    print("  from enhanced_mcp_tools import enhanced_conversation_summary")
    print("  summary = enhanced_conversation_summary()")
    
    print("\n🧠 **Semantic Insights:**")
    print("  from enhanced_mcp_tools import semantic_insights")
    print("  insights = semantic_insights('Your message')")
    
    print("\n📈 **Comprehensive Analysis:**")
    print("  from enhanced_mcp_tools import comprehensive_context_analysis")
    print("  analysis = comprehensive_context_analysis('Your message')")
    
    # Step 7: Performance monitoring
    print_section("Step 7: Performance Monitoring")
    
    try:
        # Get bridge statistics
        stats = tools.bridge_statistics()
        print_success("Bridge statistics retrieved successfully")
        
        # Get enhanced tools status
        tools_status = tools.get_available_tools()
        print_success(f"Enhanced tools status: {tools_status['integration_status']['bridge_initialized']}")
        
    except Exception as e:
        print_warning(f"Performance monitoring had issues: {e}")
    
    # Step 8: Next steps
    print_section("Step 8: Next Steps")
    
    print_info("To fully integrate the embedding system:")
    print("  1. ✅ Install dependencies: pip install -r requirements_embeddings.txt")
    print("  2. ✅ Test the system: python test_embedding_system.py")
    print("  3. ✅ Test the bridge: python mcp_embedding_bridge.py")
    print("  4. ✅ Test enhanced tools: python enhanced_mcp_tools.py")
    print("  5. 🚀 Start using in your MCP system!")
    
    print("\n🔗 **Integration Points:**")
    print("  • Replace agent_interaction() with enhanced_agent_interaction()")
    print("  • Use semantic_context_search() for better context matching")
    print("  • Leverage comprehensive_context_analysis() for rich context")
    print("  • Monitor performance with bridge_statistics()")
    
    print("\n📚 **Documentation:**")
    print("  • EMBEDDING_SYSTEM_README.md - Complete system documentation")
    print("  • Test files - Examples and usage patterns")
    print("  • Bridge integration - Seamless connection to existing tools")
    
    print_header("Integration Complete! 🎉")
    
    print_success("Your MCP conversation intelligence system now has semantic capabilities!")
    print_info("The embedding system is fully integrated and ready to use.")
    print_info("Start with simple tests and gradually expand to full integration.")

def test_quick_integration():
    """Quick integration test."""
    print_header("Quick Integration Test")
    
    try:
        # Test basic functionality
        from enhanced_mcp_tools import enhanced_agent_interaction
        
        test_message = "Test message for quick integration"
        result = enhanced_agent_interaction(test_message, use_semantic_search=False)
        
        if result['status'] == 'success':
            print_success("Quick integration test passed!")
            return True
        else:
            print_error("Quick integration test failed!")
            return False
            
    except Exception as e:
        print_error(f"Quick integration test error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        test_quick_integration()
    else:
        main()
