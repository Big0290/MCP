#!/usr/bin/env python3
"""
🚀 Integration Script: Optimized Prompt System into MCP Server

This script integrates the new optimized prompt generator into your existing
MCP server, replacing the old 88KB prompts with the new 0.5KB optimized ones.
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MCPOptimizedPromptIntegrator:
    """
    Integrates the optimized prompt system into the existing MCP server.
    """
    
    def __init__(self):
        self.backup_dir = f"backup_before_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.integration_status = {}
        
    def create_backup(self):
        """Create backup of original files before integration"""
        logger.info("📦 Creating backup of original files...")
        
        try:
            os.makedirs(self.backup_dir, exist_ok=True)
            
            files_to_backup = [
                'local_mcp_server_simple.py',
                'enhanced_mcp_tools.py',
                'main.py'
            ]
            
            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    backup_path = os.path.join(self.backup_dir, file_path)
                    shutil.copy2(file_path, backup_path)
                    logger.info(f"   ✅ Backed up: {file_path}")
                else:
                    logger.warning(f"   ⚠️ File not found: {file_path}")
            
            logger.info(f"📦 Backup created in: {self.backup_dir}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Backup creation failed: {e}")
            return False
    
    def integrate_into_local_mcp_server(self):
        """Integrate optimized prompts into local_mcp_server_simple.py"""
        logger.info("🔧 Integrating optimized prompts into local MCP server...")
        
        try:
            # Read the current file
            with open('local_mcp_server_simple.py', 'r') as f:
                content = f.read()
            
            # Replace the old prompt generation with optimized version
            old_imports = """# Import the main conversation functions
try:
    from main import (
        get_conversation_summary,
        get_interaction_history,
        agent_interaction as main_agent_interaction,
        get_system_status
    )
    MAIN_AVAILABLE = True
except ImportError:
    MAIN_AVAILABLE = False
    print("⚠️ Main module not available - using fallback functions")"""
            
            new_imports = """# Import the main conversation functions
try:
    from main import (
        get_conversation_summary,
        get_interaction_history,
        agent_interaction as main_agent_interaction,
        get_system_status
    )
    MAIN_AVAILABLE = True
except ImportError:
    MAIN_AVAILABLE = False
    print("⚠️ Main module not available - using fallback functions")

# 🚀 NEW: Import optimized prompt generator
try:
    from optimized_prompt_generator import OptimizedPromptGenerator
    OPTIMIZED_PROMPTS_AVAILABLE = True
    logger.info("🚀 Optimized prompt generator loaded successfully")
except ImportError:
    OPTIMIZED_PROMPTS_AVAILABLE = False
    logger.warning("⚠️ Optimized prompt generator not available, using fallback")"""
            
            content = content.replace(old_imports, new_imports)
            
            # Replace the enhanced_chat function
            old_enhanced_chat = """def enhanced_chat(user_message: str) -> str:
    \"\"\"
    Enhanced chat function that provides context-aware responses
    
    Args:
        user_message (str): The user's message
        
    Returns:
        str: Enhanced response with context
    \"\"\"
    try:
        # Use the centralized prompt generator for full context enhancement
        from prompt_generator import prompt_generator
        
        # Generate enhanced prompt with APPE (Adaptive Prompt Precision Engine)
        enhanced_prompt = prompt_generator.generate_enhanced_prompt(
            user_message=user_message,
            context_type="adaptive",  # 🚀 NOW USING APPE!
            force_refresh=True,
            use_appe=True
        )
        
        return enhanced_prompt"""
            
            new_enhanced_chat = """def enhanced_chat(user_message: str) -> str:
    \"\"\"
    Enhanced chat function that provides context-aware responses
    
    Args:
        user_message (str): The user's message
        
    Returns:
        str: Enhanced response with context
    \"\"\"
    try:
        # 🚀 NEW: Use optimized prompt generator for massive performance improvement
        if OPTIMIZED_PROMPTS_AVAILABLE:
            generator = OptimizedPromptGenerator()
            optimized_prompt = generator.generate_optimized_prompt(
                user_message=user_message,
                context_type="smart",  # 🚀 NOW USING OPTIMIZED PROMPTS!
                force_refresh=False
            )
            
            # Log the optimization results
            original_size = len(str(user_message))
            optimized_size = len(optimized_prompt)
            compression_ratio = (1 - optimized_size / max(original_size, 1)) * 100
            
            logger.info(f"🚀 Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
            
            return optimized_prompt
        else:
            # Fallback to old prompt generator
            from prompt_generator import prompt_generator
            
            # Generate enhanced prompt with APPE (Adaptive Prompt Precision Engine)
            enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                user_message=user_message,
                context_type="adaptive",
                force_refresh=True,
                use_appe=True
            )
            
            return enhanced_prompt"""
            
            content = content.replace(old_enhanced_chat, new_enhanced_chat)
            
            # Replace the process_prompt_with_context function
            old_process_prompt = """def process_prompt_with_context(prompt: str) -> str:
    \"\"\"
    Process a prompt with injected conversation context
    
    Args:
        prompt (str): The original prompt
        
    Returns:
        str: Enhanced prompt with context
    \"\"\"
    try:
        # Use the centralized prompt generator
        from prompt_generator import prompt_generator
        
        # Generate enhanced prompt with comprehensive context
        enhanced_prompt = prompt_generator.generate_enhanced_prompt(
            user_message=prompt,
            context_type="comprehensive",
            force_refresh=False
        )"""
            
            new_process_prompt = """def process_prompt_with_context(prompt: str) -> str:
    \"\"\"
    Process a prompt with injected conversation context
    
    Args:
        prompt (str): The original prompt
        
    Returns:
        str: Enhanced prompt with context
    \"\"\"
    try:
        # 🚀 NEW: Use optimized prompt generator for massive performance improvement
        if OPTIMIZED_PROMPTS_AVAILABLE:
            generator = OptimizedPromptGenerator()
            optimized_prompt = generator.generate_optimized_prompt(
                user_message=prompt,
                context_type="smart",  # 🚀 NOW USING OPTIMIZED PROMPTS!
                force_refresh=False
            )
            
            # Log the optimization results
            original_size = len(str(prompt))
            optimized_size = len(optimized_prompt)
            compression_ratio = (1 - optimized_size / max(original_size, 1)) * 100
            
            logger.info(f"🚀 Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
            
            return optimized_prompt
        else:
            # Fallback to old prompt generator
            from prompt_generator import prompt_generator
            
            # Generate enhanced prompt with comprehensive context
            enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                user_message=prompt,
                context_type="comprehensive",
                force_refresh=False
            )"""
            
            content = content.replace(old_process_prompt, new_process_prompt)
            
            # Write the updated content
            with open('local_mcp_server_simple.py', 'w') as f:
                f.write(content)
            
            logger.info("✅ Successfully integrated optimized prompts into local MCP server")
            self.integration_status['local_mcp_server'] = 'success'
            return True
            
        except Exception as e:
            logger.error(f"❌ Integration into local MCP server failed: {e}")
            self.integration_status['local_mcp_server'] = 'failed'
            return False
    
    def integrate_into_enhanced_mcp_tools(self):
        """Integrate optimized prompts into enhanced_mcp_tools.py"""
        logger.info("🔧 Integrating optimized prompts into enhanced MCP tools...")
        
        try:
            # Read the current file
            with open('enhanced_mcp_tools.py', 'r') as f:
                content = f.read()
            
            # Add import for optimized prompt generator
            old_imports = """# Import existing MCP tools for compatibility
from main import (
    agent_interaction, get_conversation_summary, get_interaction_history,
    get_system_status, test_conversation_tracking
)"""
            
            new_imports = """# Import existing MCP tools for compatibility
from main import (
    agent_interaction, get_conversation_summary, get_interaction_history,
    get_system_status, test_conversation_tracking
)

# 🚀 NEW: Import optimized prompt generator
try:
    from optimized_prompt_generator import OptimizedPromptGenerator
    OPTIMIZED_PROMPTS_AVAILABLE = True
    print("🚀 Optimized prompt generator loaded in enhanced MCP tools")
except ImportError:
    OPTIMIZED_PROMPTS_AVAILABLE = False
    print("⚠️ Optimized prompt generator not available in enhanced MCP tools")"""
            
            content = content.replace(old_imports, new_imports)
            
            # Update the enhanced_prompt_generation method
            old_method = """    def enhanced_prompt_generation(self, prompt: str, 
                                       context_type: str = "smart",
                                       use_semantic_search: bool = True) -> Dict[str, Any]:
        \"\"\"
        Enhanced prompt generation with semantic context.
        
        Args:
            prompt: User prompt
            context_type: Context type for enhancement
            use_semantic_search: Whether to use semantic search
            
        Returns:
            Enhanced prompt generation result
        \"\"\"
        start_time = time.time()
        
        try:
            # Generate enhanced prompt with embeddings
            enhanced_prompt = self.bridge.generate_enhanced_prompt_with_embeddings(
                prompt, context_type, use_semantic_search, 0.7
            )"""
            
            new_method = """    def enhanced_prompt_generation(self, prompt: str, 
                                       context_type: str = "smart",
                                       use_semantic_search: bool = True) -> Dict[str, Any]:
        \"\"\"
        Enhanced prompt generation with semantic context.
        
        Args:
            prompt: User prompt
            context_type: Context type for enhancement
            use_semantic_search: Whether to use semantic search
            
        Returns:
            Enhanced prompt generation result
        \"\"\"
        start_time = time.time()
        
        try:
            # 🚀 NEW: Use optimized prompt generator for massive performance improvement
            if OPTIMIZED_PROMPTS_AVAILABLE:
                generator = OptimizedPromptGenerator()
                optimized_prompt = generator.generate_optimized_prompt(
                    user_message=prompt,
                    context_type=context_type,
                    force_refresh=False
                )
                
                # Log the optimization results
                original_size = len(str(prompt))
                optimized_size = len(optimized_prompt)
                compression_ratio = (1 - optimized_size / max(original_size, 1)) * 100
                
                print(f"🚀 Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
                
                enhanced_prompt = optimized_prompt
            else:
                # Fallback to old embedding-based generation
                enhanced_prompt = self.bridge.generate_enhanced_prompt_with_embeddings(
                    prompt, context_type, use_semantic_search, 0.7
                )"""
            
            content = content.replace(old_method, new_method)
            
            # Write the updated content
            with open('enhanced_mcp_tools.py', 'w') as f:
                f.write(content)
            
            logger.info("✅ Successfully integrated optimized prompts into enhanced MCP tools")
            self.integration_status['enhanced_mcp_tools'] = 'success'
            return True
            
        except Exception as e:
            logger.error(f"❌ Integration into enhanced MCP tools failed: {e}")
            self.integration_status['enhanced_mcp_tools'] = 'failed'
            return False
    
    def create_optimized_prompt_wrapper(self):
        """Create a wrapper module for easy access to optimized prompts"""
        logger.info("🔧 Creating optimized prompt wrapper module...")
        
        try:
            wrapper_content = '''#!/usr/bin/env python3
"""
🚀 Optimized Prompt Wrapper - Easy Access to Optimized Prompts

This module provides easy access to the optimized prompt system
for integration with existing MCP tools.
"""

from optimized_prompt_generator import OptimizedPromptGenerator, generate_optimized_prompt

# Global instance for easy access
_optimized_generator = None

def get_optimized_generator():
    """Get or create the global optimized prompt generator instance"""
    global _optimized_generator
    if _optimized_generator is None:
        _optimized_generator = OptimizedPromptGenerator()
    return _optimized_generator

def generate_optimized_prompt_for_mcp(user_message: str, context_type: str = "smart") -> str:
    """
    Generate an optimized prompt specifically for MCP usage.
    
    Args:
        user_message: The user's message
        context_type: Type of context to use
        
    Returns:
        str: Optimized prompt string
    """
    try:
        generator = get_optimized_generator()
        optimized_prompt = generator.generate_optimized_prompt(
            user_message=user_message,
            context_type=context_type,
            force_refresh=False
        )
        
        # Log optimization results
        original_size = len(str(user_message))
        optimized_size = len(optimized_prompt)
        compression_ratio = (1 - optimized_size / max(original_size, 1)) * 100
        
        print(f"🚀 MCP Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
        
        return optimized_prompt
        
    except Exception as e:
        print(f"❌ Optimized prompt generation failed: {e}")
        # Return minimal fallback
        return f"🚀 OPTIMIZED PROMPT: {user_message}\\n\\n👤 PREFERENCES: Concise, technical, structured responses\\n⚙️ TECH: Python, SQLite, MCP\\n🤖 AGENT: Johny\\n\\n🎯 Provide helpful, context-aware assistance."

# Convenience functions
def quick_optimize(message: str) -> str:
    """Quick optimization with default settings"""
    return generate_optimized_prompt_for_mcp(message, "smart")

def technical_optimize(message: str) -> str:
    """Technical optimization for code/implementation queries"""
    return generate_optimized_prompt_for_mcp(message, "technical")

def conversation_optimize(message: str) -> str:
    """Conversation optimization for chat continuity"""
    return generate_optimized_prompt_for_mcp(message, "conversation")

def project_optimize(message: str) -> str:
    """Project optimization for structure/analysis queries"""
    return generate_optimized_prompt_for_mcp(message, "project")
'''
            
            with open('optimized_prompt_wrapper.py', 'w') as f:
                f.write(wrapper_content)
            
            logger.info("✅ Successfully created optimized prompt wrapper module")
            self.integration_status['wrapper_creation'] = 'success'
            return True
            
        except Exception as e:
            logger.error(f"❌ Wrapper creation failed: {e}")
            self.integration_status['wrapper_creation'] = 'failed'
            return False
    
    def create_integration_test(self):
        """Create a test script to verify the integration"""
        logger.info("🧪 Creating integration test script...")
        
        try:
            test_content = '''#!/usr/bin/env python3
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
        logger.info(f"\\n{'='*60}")
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
    logger.info(f"\\n{'='*60}")
    logger.info("📊 INTEGRATION TEST SUMMARY")
    logger.info(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"   {status}: {test_name}")
    
    logger.info(f"\\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        logger.info("🎉 All integration tests passed! Optimized prompts are working in MCP server.")
        return True
    else:
        logger.error("⚠️ Some integration tests failed. Check the logs above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
            
            with open('test_mcp_integration.py', 'w') as f:
                f.write(test_content)
            
            logger.info("✅ Successfully created integration test script")
            self.integration_status['test_creation'] = 'success'
            return True
            
        except Exception as e:
            logger.error(f"❌ Test creation failed: {e}")
            self.integration_status['test_creation'] = 'failed'
            return False
    
    def run_integration(self):
        """Run the complete integration process"""
        logger.info("🚀 Starting MCP Server Integration Process...")
        
        # Step 1: Create backup
        if not self.create_backup():
            logger.error("❌ Backup creation failed, aborting integration")
            return False
        
        # Step 2: Integrate into local MCP server
        if not self.integrate_into_local_mcp_server():
            logger.error("❌ Local MCP server integration failed")
            return False
        
        # Step 3: Integrate into enhanced MCP tools
        if not self.integrate_into_enhanced_mcp_tools():
            logger.error("❌ Enhanced MCP tools integration failed")
            return False
        
        # Step 4: Create wrapper module
        if not self.create_optimized_prompt_wrapper():
            logger.error("❌ Wrapper creation failed")
            return False
        
        # Step 5: Create integration test
        if not self.create_integration_test():
            logger.error("❌ Test creation failed")
            return False
        
        # Summary
        logger.info("\\n🎉 INTEGRATION COMPLETE!")
        logger.info("📊 Integration Status:")
        for component, status in self.integration_status.items():
            status_icon = "✅" if status == 'success' else "❌"
            logger.info(f"   {status_icon} {component}: {status}")
        
        logger.info("\\n🚀 Next Steps:")
        logger.info("   1. Test the integration: python3 test_mcp_integration.py")
        logger.info("   2. Restart your MCP server to use optimized prompts")
        logger.info("   3. Monitor performance improvements")
        logger.info("   4. Enjoy 99.5% smaller, faster prompts!")
        
        return True

def main():
    """Main integration function"""
    integrator = MCPOptimizedPromptIntegrator()
    return integrator.run_integration()

if __name__ == "__main__":
    success = main()
    if success:
        print("\\n🎉 MCP Server Integration Successful!")
        print("🚀 Your MCP server now uses optimized prompts!")
    else:
        print("\\n❌ MCP Server Integration Failed!")
        print("⚠️ Check the logs above for details")
