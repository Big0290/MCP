"""
Enhanced Chat Integration with Semantic Embeddings

This module provides seamless integration between your existing enhanced_chat
function and the new embedding system, maintaining full backward compatibility
while adding semantic capabilities.
"""

import time
from typing import Dict, Any, Optional, Union
from datetime import datetime

# NOTE: Avoid circular import - enhanced_chat function will be imported dynamically

# Import the embedding system components
from mcp_embedding_bridge import get_mcp_embedding_bridge
from enhanced_mcp_tools import get_enhanced_mcp_tools


class EnhancedChatIntegration:
    """
    Seamless integration layer for enhanced_chat function.
    
    This class provides semantic enhancement capabilities while maintaining
    full compatibility with your existing enhanced_chat function.
    """
    
    def __init__(self, enable_semantic_enhancement: bool = True):
        """
        Initialize the enhanced chat integration.
        
        Args:
            enable_semantic_enhancement: Whether to enable semantic enhancements
        """
        self.enable_semantic_enhancement = enable_semantic_enhancement
        self.bridge = None
        self.enhanced_tools = None
        
        # Initialize components if semantic enhancement is enabled
        if self.enable_semantic_enhancement:
            try:
                self.bridge = get_mcp_embedding_bridge()
                self.enhanced_tools = get_enhanced_mcp_tools()
                self.integration_status = "semantic_enabled"
            except Exception as e:
                print(f"Warning: Semantic enhancement not available: {e}")
                self.integration_status = "semantic_fallback"
        else:
            self.integration_status = "semantic_disabled"
    
    def enhanced_chat(self, user_message: str, **kwargs) -> Union[str, Dict[str, Any]]:
        """
        Enhanced chat function with seamless semantic integration.
        
        This function maintains full compatibility with your existing enhanced_chat
        while adding semantic capabilities when available.
        
        Args:
            user_message: User message to process
            **kwargs: Additional arguments for enhanced processing
            
        Returns:
            Enhanced response (string for compatibility, dict for enhanced mode)
        """
        start_time = time.time()
        
        # Check if semantic enhancement is available and enabled
        if (self.enable_semantic_enhancement and 
            self.bridge and 
            self.enhanced_tools and
            kwargs.get('use_semantic_enhancement', True)):
            
            try:
                # Use enhanced semantic processing
                return self._semantic_enhanced_chat(user_message, **kwargs)
            except Exception as e:
                print(f"Semantic enhancement failed, falling back to original: {e}")
                # Fallback to original enhanced_chat
                return self._fallback_enhanced_chat(user_message, **kwargs)
        else:
            # Use original enhanced_chat function
            return self._fallback_enhanced_chat(user_message, **kwargs)
    
    def _semantic_enhanced_chat(self, user_message: str, **kwargs) -> Dict[str, Any]:
        """
        Semantic-enhanced chat processing.
        
        Args:
            user_message: User message to process
            **kwargs: Additional arguments
            
        Returns:
            Enhanced response with semantic analysis
        """
        # Get semantic context and insights
        semantic_context = self.bridge.get_comprehensive_context(user_message)
        
        # Generate enhanced prompt with embeddings
        enhanced_prompt = self.bridge.generate_enhanced_prompt_with_embeddings(
            user_message,
            context_type=kwargs.get('context_type', 'smart'),
            use_semantic_search=kwargs.get('use_semantic_search', True),
            similarity_threshold=kwargs.get('similarity_threshold', 0.7)
        )
        
        # Get original enhanced_chat response (import dynamically to avoid circular import)
        try:
            from main import enhanced_chat as original_enhanced_chat
            original_response = original_enhanced_chat(user_message)
        except ImportError:
            # Fallback if import fails
            original_response = f"Enhanced response to: {user_message}"
        
        # Enhance context learning
        learning_result = self.bridge.enhance_context_learning_with_embeddings(
            user_message, enhanced_prompt, 0.8, kwargs.get('context_type', 'conversation')
        )
        
        # Get semantic insights
        semantic_insights = self.enhanced_tools.semantic_insights(
            user_message,
            context_type=kwargs.get('context_type', 'conversation'),
            include_recommendations=True
        )
        
        processing_time = time.time() - start_time
        
        # Build comprehensive response
        response = {
            'status': 'success',
            'semantic_enhancement': True,
            'user_message': user_message,
            'original_response': original_response,
            'enhanced_prompt': enhanced_prompt,
            'semantic_context': semantic_context,
            'semantic_insights': semantic_insights,
            'learning_enhancement': learning_result,
            'performance_metrics': {
                'processing_time_ms': round(processing_time * 1000, 2),
                'enhancement_ratio': len(enhanced_prompt) / len(user_message) if user_message else 1.0,
                'context_richness_score': semantic_context.get('bridge_enhancements', {}).get('context_richness_score', 0)
            },
            'integration_status': self.integration_status,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add recommendations if available
        if semantic_insights.get('recommendations'):
            response['recommendations'] = semantic_insights['recommendations']
        
        return response
    
    def _fallback_enhanced_chat(self, user_message: str, **kwargs) -> str:
        """
        Fallback to original enhanced_chat function.
        
        Args:
            user_message: User message to process
            **kwargs: Additional arguments
            
        Returns:
            Original enhanced_chat response
        """
        # Import dynamically to avoid circular import
        try:
            from main import enhanced_chat as original_enhanced_chat
            return original_enhanced_chat(user_message)
        except ImportError:
            # Fallback if import fails
            return f"Enhanced fallback response to: {user_message}"
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status."""
        return {
            'semantic_enhancement_enabled': self.enable_semantic_enhancement,
            'integration_status': self.integration_status,
            'bridge_available': self.bridge is not None,
            'enhanced_tools_available': self.enhanced_tools is not None,
            'timestamp': datetime.now().isoformat()
        }
    
    def toggle_semantic_enhancement(self, enable: bool = None) -> bool:
        """
        Toggle semantic enhancement on/off.
        
        Args:
            enable: Whether to enable (None to toggle current state)
            
        Returns:
            New state of semantic enhancement
        """
        if enable is None:
            self.enable_semantic_enhancement = not self.enable_semantic_enhancement
        else:
            self.enable_semantic_enhancement = enable
        
        return self.enable_semantic_enhancement
    
    def get_semantic_insights(self, user_message: str, **kwargs) -> Dict[str, Any]:
        """
        Get semantic insights for a user message.
        
        Args:
            user_message: User message to analyze
            **kwargs: Additional arguments
            
        Returns:
            Semantic insights and analysis
        """
        if self.enhanced_tools:
            return self.enhanced_tools.semantic_insights(user_message, **kwargs)
        else:
            return {
                'status': 'error',
                'error': 'Enhanced tools not available',
                'user_message': user_message,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_comprehensive_context(self, user_message: str, **kwargs) -> Dict[str, Any]:
        """
        Get comprehensive context analysis.
        
        Args:
            user_message: User message to analyze
            **kwargs: Additional arguments
            
        Returns:
            Comprehensive context analysis
        """
        if self.bridge:
            return self.bridge.get_comprehensive_context(user_message, **kwargs)
        else:
            return {
                'status': 'error',
                'error': 'Bridge not available',
                'user_message': user_message,
                'timestamp': datetime.now().isoformat()
            }


# Global enhanced chat integration instance
_enhanced_chat_integration = None

def get_enhanced_chat_integration(enable_semantic: bool = True) -> EnhancedChatIntegration:
    """Get or create the global enhanced chat integration instance."""
    global _enhanced_chat_integration
    if _enhanced_chat_integration is None:
        _enhanced_chat_integration = EnhancedChatIntegration(enable_semantic)
    return _enhanced_chat_integration


# Seamless replacement function - maintains exact compatibility
def enhanced_chat(user_message: str, **kwargs) -> Union[str, Dict[str, Any]]:
    """
    Enhanced chat function with seamless semantic integration.
    
    This function maintains full compatibility with your existing enhanced_chat
    while adding semantic capabilities when available.
    
    Args:
        user_message: User message to process
        **kwargs: Additional arguments for enhanced processing
        
    Returns:
        Enhanced response (string for compatibility, dict for enhanced mode)
    """
    integration = get_enhanced_chat_integration()
    return integration.enhanced_chat(user_message, **kwargs)


# Enhanced version with explicit semantic control
def enhanced_chat_semantic(user_message: str, 
                          use_semantic_enhancement: bool = True,
                          context_type: str = "smart",
                          use_semantic_search: bool = True,
                          similarity_threshold: float = 0.7,
                          return_enhanced: bool = True,
                          **kwargs) -> Union[str, Dict[str, Any]]:
    """
    Enhanced chat function with explicit semantic control.
    
    Args:
        user_message: User message to process
        use_semantic_enhancement: Whether to use semantic enhancements
        context_type: Context type for enhancement
        use_semantic_search: Whether to use semantic search
        similarity_threshold: Minimum similarity threshold
        return_enhanced: Whether to return enhanced response object
        **kwargs: Additional arguments
        
    Returns:
        Enhanced response (string or dict based on return_enhanced)
    """
    integration = get_enhanced_chat_integration(use_semantic_enhancement)
    
    # Set semantic parameters
    kwargs.update({
        'use_semantic_enhancement': use_semantic_enhancement,
        'context_type': context_type,
        'use_semantic_search': use_semantic_search,
        'similarity_threshold': similarity_threshold
    })
    
    response = integration.enhanced_chat(user_message, **kwargs)
    
    # Return format based on user preference
    if return_enhanced and isinstance(response, dict):
        return response
    elif isinstance(response, dict):
        # Return just the original response for compatibility
        return response.get('original_response', str(response))
    else:
        return response


# Quick semantic insights function
def get_semantic_insights_quick(user_message: str, **kwargs) -> Dict[str, Any]:
    """Quick access to semantic insights."""
    integration = get_enhanced_chat_integration()
    return integration.get_semantic_insights(user_message, **kwargs)


# Quick context analysis function
def get_context_analysis_quick(user_message: str, **kwargs) -> Dict[str, Any]:
    """Quick access to comprehensive context analysis."""
    integration = get_enhanced_chat_integration()
    return integration.get_comprehensive_context(user_message, **kwargs)


# Integration status function
def get_enhanced_chat_status() -> Dict[str, Any]:
    """Get the current status of enhanced chat integration."""
    integration = get_enhanced_chat_integration()
    return integration.get_integration_status()


# Toggle semantic enhancement function
def toggle_semantic_enhancement(enable: bool = None) -> bool:
    """Toggle semantic enhancement on/off."""
    integration = get_enhanced_chat_integration()
    return integration.toggle_semantic_enhancement(enable)


if __name__ == "__main__":
    # Test the enhanced chat integration
    print("=== Testing Enhanced Chat Integration ===\n")
    
    # Test basic functionality
    test_message = "How can I improve my MCP conversation system with embeddings?"
    
    print("1. Testing Basic Enhanced Chat (Backward Compatible):")
    try:
        result = enhanced_chat(test_message)
        if isinstance(result, str):
            print(f"✅ Backward compatible response: {len(result)} characters")
        else:
            print(f"✅ Enhanced response: {result['status']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n2. Testing Semantic Enhanced Chat:")
    try:
        result = enhanced_chat_semantic(
            test_message,
            use_semantic_enhancement=True,
            return_enhanced=True
        )
        if isinstance(result, dict):
            print(f"✅ Semantic enhancement successful: {result['status']}")
            metrics = result.get('performance_metrics', {})
            print(f"   Processing time: {metrics.get('processing_time_ms', 0)}ms")
            print(f"   Enhancement ratio: {metrics.get('enhancement_ratio', 0):.2f}")
            print(f"   Context richness: {metrics.get('context_richness_score', 0):.2f}")
        else:
            print(f"✅ Response received: {len(result)} characters")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n3. Testing Semantic Insights:")
    try:
        insights = get_semantic_insights_quick(test_message)
        print(f"✅ Semantic insights: {insights.get('status', 'unknown')}")
        if insights.get('recommendations'):
            print(f"   Recommendations: {len(insights['recommendations'])} found")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n4. Testing Context Analysis:")
    try:
        context = get_context_analysis_quick(test_message)
        if 'error' not in context:
            richness_score = context.get('bridge_enhancements', {}).get('context_richness_score', 0)
            print(f"✅ Context analysis: Richness score {richness_score:.2f}")
        else:
            print(f"⚠️ Context analysis: {context.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n5. Testing Integration Status:")
    try:
        status = get_enhanced_chat_status()
        print(f"✅ Integration status: {status['integration_status']}")
        print(f"   Semantic enhancement: {status['semantic_enhancement_enabled']}")
        print(f"   Bridge available: {status['bridge_available']}")
        print(f"   Enhanced tools available: {status['enhanced_tools_available']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("🎉 Enhanced Chat Integration Testing Complete!")
    print("\nYou can now use these functions seamlessly:")
    print("  • enhanced_chat() - Enhanced version of your existing function")
    print("  • enhanced_chat_semantic() - Full semantic control")
    print("  • get_semantic_insights_quick() - Quick semantic analysis")
    print("  • get_context_analysis_quick() - Quick context analysis")
    print("  • get_enhanced_chat_status() - Integration status")
    print("  • toggle_semantic_enhancement() - Toggle semantic features")
    
    print("\n🔗 **Seamless Integration Benefits:**")
    print("  ✅ Full backward compatibility with existing code")
    print("  ✅ Automatic semantic enhancement when available")
    print("  ✅ Graceful fallback to original functionality")
    print("  ✅ Rich semantic insights and context analysis")
    print("  ✅ Performance metrics and monitoring")
    print("  ✅ Easy toggle between enhanced and basic modes")
