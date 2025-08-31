"""
Enhanced MCP Tools with Embedding Integration

This module provides enhanced MCP tools that integrate the embedding system
with your existing conversation intelligence tools.
"""

import time
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import the bridge
from mcp_embedding_bridge import get_mcp_embedding_bridge, MCPEmbeddingBridge

# Import existing MCP tools for compatibility
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
    print("⚠️ Optimized prompt generator not available in enhanced MCP tools")


class EnhancedMCPTools:
    """
    Enhanced MCP tools that integrate embeddings with existing functionality.
    """
    
    def __init__(self):
        """Initialize enhanced MCP tools."""
        self.bridge = get_mcp_embedding_bridge()
        self.tools_registry = {
            'enhanced_agent_interaction': self.enhanced_agent_interaction,
            'semantic_context_search': self.semantic_context_search,
            'enhanced_conversation_summary': self.enhanced_conversation_summary,
            'semantic_insights': self.semantic_insights,
            'bridge_status': self.bridge_status,
            'test_enhanced_integration': self.test_enhanced_integration,
            'enhanced_prompt_generation': self.enhanced_prompt_generation,
            'comprehensive_context_analysis': self.comprehensive_context_analysis,
            'semantic_learning_enhancement': self.semantic_learning_enhancement,
            'bridge_statistics': self.bridge_statistics,
            'clear_enhanced_cache': self.clear_enhanced_cache
        }
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Get list of available enhanced MCP tools."""
        return {
            'enhanced_tools': list(self.tools_registry.keys()),
            'base_tools': [
                'agent_interaction', 'get_conversation_summary', 
                'get_interaction_history', 'get_system_status',
                'test_conversation_tracking'
            ],
            'total_tools': len(self.tools_registry) + 5,
            'integration_status': self.bridge.get_bridge_status()
        }
    
    def enhanced_agent_interaction(self, prompt: str, 
                                  use_semantic_search: bool = True,
                                  context_type: str = "smart",
                                  similarity_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Enhanced agent interaction with semantic context injection.
        
        Args:
            prompt: User prompt
            use_semantic_search: Whether to use semantic search
            context_type: Context type for enhancement
            similarity_threshold: Minimum similarity threshold
            
        Returns:
            Enhanced interaction result
        """
        start_time = time.time()
        
        try:
            # Generate enhanced prompt with embeddings
            enhanced_prompt = self.bridge.generate_enhanced_prompt_with_embeddings(
                prompt, context_type, use_semantic_search, similarity_threshold
            )
            
            # Use existing agent interaction
            base_response = agent_interaction(prompt)
            
            # Enhance context learning
            learning_result = self.bridge.enhance_context_learning_with_embeddings(
                prompt, enhanced_prompt, 0.8, context_type
            )
            
            processing_time = time.time() - start_time
            
            return {
                'status': 'success',
                'original_prompt': prompt,
                'enhanced_prompt': enhanced_prompt,
                'base_response': base_response,
                'semantic_enhancement': {
                    'enhancement_ratio': len(enhanced_prompt) / len(prompt) if prompt else 1.0,
                    'similarity_threshold': similarity_threshold,
                    'context_type': context_type
                },
                'learning_enhancement': learning_result,
                'processing_time_ms': round(processing_time * 1000, 2),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                'status': 'error',
                'error': str(e),
                'original_prompt': prompt,
                'processing_time_ms': round(processing_time * 1000, 2),
                'timestamp': datetime.now().isoformat()
            }
    
    def semantic_context_search(self, query: str, 
                               context_type: str = "conversation",
                               limit: int = 10,
                               min_similarity: float = 0.7) -> Dict[str, Any]:
        """
        Search for semantically similar contexts.
        
        Args:
            query: Search query
            context_type: Context type to search in
            limit: Maximum number of results
            min_similarity: Minimum similarity threshold
            
        Returns:
            Search results with semantic similarity
        """
        try:
            # Use bridge for semantic search
            similar_contexts = self.bridge.enhance_caching_with_semantic_similarity(
                query, context_type, min_similarity
            )
            
            # Limit results
            limited_results = similar_contexts[:limit]
            
            return {
                'status': 'success',
                'query': query,
                'context_type': context_type,
                'min_similarity': min_similarity,
                'total_found': len(similar_contexts),
                'results_returned': len(limited_results),
                'results': limited_results,
                'search_metadata': {
                    'search_type': 'semantic',
                    'vector_search_available': self.bridge.embedding_integration is not None,
                    'timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'query': query,
                'timestamp': datetime.now().isoformat()
            }
    
    def enhanced_conversation_summary(self, session_id: Optional[str] = None,
                                     include_semantic_insights: bool = True) -> Dict[str, Any]:
        """
        Enhanced conversation summary with semantic insights.
        
        Args:
            session_id: Optional session ID
            include_semantic_insights: Whether to include semantic analysis
            
        Returns:
            Enhanced conversation summary
        """
        try:
            # Get base conversation summary
            base_summary = get_conversation_summary(session_id)
            
            enhanced_summary = {
                'base_summary': base_summary,
                'semantic_enhancements': {},
                'timestamp': datetime.now().isoformat()
            }
            
            if include_semantic_insights:
                try:
                    # Get semantic insights for recent conversations
                    recent_interactions = get_interaction_history(limit=5, session_id=session_id)
                    
                    if recent_interactions and 'interactions' in recent_interactions:
                        # Analyze recent interactions for semantic patterns
                        semantic_analysis = self._analyze_conversation_semantics(recent_interactions['interactions'])
                        enhanced_summary['semantic_enhancements'] = semantic_analysis
                        
                except Exception as e:
                    enhanced_summary['semantic_enhancements']['error'] = str(e)
            
            return enhanced_summary
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def semantic_insights(self, user_message: str, 
                          context_type: str = "conversation",
                          include_recommendations: bool = True) -> Dict[str, Any]:
        """
        Get semantic insights for a user message.
        
        Args:
            user_message: User message to analyze
            context_type: Context type for analysis
            include_recommendations: Whether to include recommendations
            
        Returns:
            Semantic insights and analysis
        """
        try:
            # Get comprehensive context
            context = self.bridge.get_comprehensive_context(user_message)
            
            # Get semantic insights from embedding system
            semantic_insights = {}
            if self.bridge.embedding_integration:
                try:
                    semantic_insights = self.bridge.embedding_integration.get_semantic_insights(
                        user_message, context_type
                    )
                except Exception as e:
                    semantic_insights = {'error': str(e)}
            
            # Build insights response
            insights = {
                'user_message': user_message,
                'context_type': context_type,
                'context_richness_score': context.get('bridge_enhancements', {}).get('context_richness_score', 0),
                'comprehensive_context': context,
                'semantic_insights': semantic_insights,
                'timestamp': datetime.now().isoformat()
            }
            
            if include_recommendations:
                insights['recommendations'] = context.get('bridge_enhancements', {}).get('recommendations', [])
            
            return insights
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'user_message': user_message,
                'timestamp': datetime.now().isoformat()
            }
    
    def bridge_status(self) -> Dict[str, Any]:
        """Get the current bridge integration status."""
        return self.bridge.get_bridge_status()
    
    def test_enhanced_integration(self) -> Dict[str, Any]:
        """Test the enhanced integration between all systems."""
        return self.bridge.test_bridge_integration()
    
    def enhanced_prompt_generation(self, user_message: str,
                                  context_type: str = "smart",
                                  use_semantic_search: bool = True,
                                  similarity_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Enhanced prompt generation with semantic context.
        
        Args:
            user_message: User message
            context_type: Context type
            use_semantic_search: Whether to use semantic search
            similarity_threshold: Minimum similarity threshold
            
        Returns:
            Enhanced prompt generation result
        """
        try:
            start_time = time.time()
            
            # Generate enhanced prompt
            enhanced_prompt = self.bridge.generate_enhanced_prompt_with_embeddings(
                user_message, context_type, use_semantic_search, similarity_threshold
            )
            
            processing_time = time.time() - start_time
            
            return {
                'status': 'success',
                'user_message': user_message,
                'enhanced_prompt': enhanced_prompt,
                'enhancement_metrics': {
                    'original_length': len(user_message),
                    'enhanced_length': len(enhanced_prompt),
                    'enhancement_ratio': len(enhanced_prompt) / len(user_message) if user_message else 1.0,
                    'processing_time_ms': round(processing_time * 1000, 2)
                },
                'context_type': context_type,
                'semantic_search_used': use_semantic_search,
                'similarity_threshold': similarity_threshold,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'user_message': user_message,
                'timestamp': datetime.now().isoformat()
            }
    
    def comprehensive_context_analysis(self, user_message: str,
                                     session_id: Optional[str] = None,
                                     user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Comprehensive context analysis using all available systems.
        
        Args:
            user_message: User message to analyze
            session_id: Optional session ID
            user_id: Optional user ID
            
        Returns:
            Comprehensive context analysis
        """
        return self.bridge.get_comprehensive_context(user_message, session_id, user_id)
    
    def semantic_learning_enhancement(self, user_message: str,
                                     enhanced_prompt: str,
                                     response_quality: float,
                                     context_type: str = "conversation") -> Dict[str, Any]:
        """
        Enhance learning with semantic capabilities.
        
        Args:
            user_message: User message
            enhanced_prompt: Enhanced prompt
            response_quality: Response quality rating
            context_type: Context type
            
        Returns:
            Learning enhancement result
        """
        return self.bridge.enhance_context_learning_with_embeddings(
            user_message, enhanced_prompt, response_quality, context_type
        )
    
    def bridge_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics from the bridge."""
        return self.bridge.get_bridge_statistics()
    
    def clear_enhanced_cache(self, context_type: Optional[str] = None) -> Dict[str, Any]:
        """Clear caches in both existing and embedding systems."""
        return self.bridge.clear_bridge_cache(context_type)
    
    def _analyze_conversation_semantics(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze conversation interactions for semantic patterns."""
        try:
            if not interactions:
                return {'error': 'No interactions to analyze'}
            
            # Extract text content from interactions
            texts = []
            for interaction in interactions:
                if 'client_request' in interaction:
                    texts.append(interaction['client_request'])
                if 'agent_response' in interaction:
                    texts.append(interaction['agent_response'])
            
            if not texts:
                return {'error': 'No text content found in interactions'}
            
            # Analyze semantic patterns
            analysis = {
                'total_interactions': len(interactions),
                'total_text_segments': len(texts),
                'semantic_patterns': {},
                'conversation_themes': [],
                'technical_terms': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Basic text analysis
            all_text = ' '.join(texts).lower()
            
            # Extract technical terms (simple heuristic)
            technical_terms = ['mcp', 'embedding', 'context', 'prompt', 'conversation', 'semantic']
            found_terms = [term for term in technical_terms if term in all_text]
            analysis['technical_terms'] = found_terms
            
            # Extract conversation themes
            themes = []
            if 'embedding' in all_text:
                themes.append('Embedding System')
            if 'context' in all_text:
                themes.append('Context Management')
            if 'prompt' in all_text:
                themes.append('Prompt Enhancement')
            if 'conversation' in all_text:
                themes.append('Conversation Intelligence')
            
            analysis['conversation_themes'] = themes
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Call a specific enhanced MCP tool.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Tool-specific arguments
            
        Returns:
            Tool execution result
        """
        if tool_name in self.tools_registry:
            try:
                return self.tools_registry[tool_name](**kwargs)
            except Exception as e:
                return {
                    'status': 'error',
                    'error': str(e),
                    'tool_name': tool_name,
                    'timestamp': datetime.now().isoformat()
                }
        else:
            return {
                'status': 'error',
                'error': f'Tool "{tool_name}" not found',
                'available_tools': list(self.tools_registry.keys()),
                'timestamp': datetime.now().isoformat()
            }


# Global enhanced MCP tools instance
_enhanced_mcp_tools = None

def get_enhanced_mcp_tools() -> EnhancedMCPTools:
    """Get or create the global enhanced MCP tools instance."""
    global _enhanced_mcp_tools
    if _enhanced_mcp_tools is None:
        _enhanced_mcp_tools = EnhancedMCPTools()
    return _enhanced_mcp_tools


# Convenience functions for easy access
def enhanced_agent_interaction(prompt: str, **kwargs) -> Dict[str, Any]:
    """Enhanced agent interaction with semantic context."""
    tools = get_enhanced_mcp_tools()
    return tools.enhanced_agent_interaction(prompt, **kwargs)


def semantic_context_search(query: str, **kwargs) -> Dict[str, Any]:
    """Search for semantically similar contexts."""
    tools = get_enhanced_mcp_tools()
    return tools.semantic_context_search(query, **kwargs)


def enhanced_conversation_summary(**kwargs) -> Dict[str, Any]:
    """Enhanced conversation summary with semantic insights."""
    tools = get_enhanced_mcp_tools()
    return tools.enhanced_conversation_summary(**kwargs)


def semantic_insights(user_message: str, **kwargs) -> Dict[str, Any]:
    """Get semantic insights for a user message."""
    tools = get_enhanced_mcp_tools()
    return tools.semantic_insights(user_message, **kwargs)


def get_enhanced_tools_status() -> Dict[str, Any]:
    """Get status of enhanced MCP tools."""
    tools = get_enhanced_mcp_tools()
    return tools.get_available_tools()


if __name__ == "__main__":
    # Test the enhanced MCP tools
    print("=== Testing Enhanced MCP Tools ===\n")
    
    tools = get_enhanced_mcp_tools()
    
    # Test tool availability
    available_tools = tools.get_available_tools()
    print("Available Enhanced Tools:")
    for tool in available_tools['enhanced_tools']:
        print(f"  ✅ {tool}")
    
    print(f"\nTotal Enhanced Tools: {available_tools['total_tools']}")
    print(f"Integration Status: {available_tools['integration_status']['bridge_initialized']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test enhanced agent interaction
    test_prompt = "How can I improve my MCP conversation system with embeddings?"
    
    print("Testing Enhanced Agent Interaction:")
    interaction_result = tools.enhanced_agent_interaction(
        test_prompt, use_semantic_search=True, context_type="technical"
    )
    
    print(f"Status: {interaction_result['status']}")
    if interaction_result['status'] == 'success':
        print(f"Enhancement Ratio: {interaction_result['semantic_enhancement']['enhancement_ratio']:.2f}")
        print(f"Processing Time: {interaction_result['processing_time_ms']}ms")
    
    print("\n" + "="*50 + "\n")
    
    # Test semantic context search
    print("Testing Semantic Context Search:")
    search_result = tools.semantic_context_search(
        "MCP conversation system", context_type="conversation", limit=5
    )
    
    print(f"Status: {search_result['status']}")
    if search_result['status'] == 'success':
        print(f"Results Found: {search_result['total_found']}")
        print(f"Results Returned: {search_result['results_returned']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test bridge status
    print("Testing Bridge Status:")
    bridge_status = tools.bridge_status()
    for key, value in bridge_status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Test comprehensive context analysis
    print("Testing Comprehensive Context Analysis:")
    context_result = tools.comprehensive_context_analysis(test_prompt)
    
    if 'error' not in context_result:
        richness_score = context_result.get('bridge_enhancements', {}).get('context_richness_score', 0)
        print(f"Context Richness Score: {richness_score:.2f}")
        
        recommendations = context_result.get('bridge_enhancements', {}).get('recommendations', [])
        if recommendations:
            print("Recommendations:")
            for rec in recommendations[:3]:  # Show first 3
                print(f"  • {rec}")
    else:
        print(f"Error: {context_result['error']}")
    
    print("\n" + "="*50 + "\n")
    
    # Test enhanced prompt generation
    print("Testing Enhanced Prompt Generation:")
    prompt_result = tools.enhanced_prompt_generation(
        test_prompt, context_type="smart", use_semantic_search=True
    )
    
    print(f"Status: {prompt_result['status']}")
    if prompt_result['status'] == 'success':
        metrics = prompt_result['enhancement_metrics']
        print(f"Original Length: {metrics['original_length']}")
        print(f"Enhanced Length: {metrics['enhanced_length']}")
        print(f"Enhancement Ratio: {metrics['enhancement_ratio']:.2f}")
        print(f"Processing Time: {metrics['processing_time_ms']}ms")
    
    print("\n" + "="*50 + "\n")
    
    print("✅ Enhanced MCP Tools Testing Complete!")
    print("\nYou can now use these enhanced tools in your MCP system:")
    print("  • enhanced_agent_interaction() - Enhanced AI interactions")
    print("  • semantic_context_search() - Semantic context search")
    print("  • enhanced_conversation_summary() - Rich conversation summaries")
    print("  • semantic_insights() - Semantic analysis and insights")
    print("  • comprehensive_context_analysis() - Full context analysis")
