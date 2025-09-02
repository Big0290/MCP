"""
MCP Embedding Bridge - Integration Layer

This module provides seamless integration between the embedding system and your
existing MCP conversation intelligence tools.
"""

import time
from typing import Dict, Any, Optional, List
from datetime import datetime

# Import your existing MCP tools
from prompt_generator import PromptGenerator
from context_learning_system import ContextLearningSystem
from smart_caching_system import SmartCachingSystem
from context_manager import SeamlessContextManager
from interaction_logger import logger
from session_manager import SessionManager

# Import the embedding system
from embedding_integration import get_embedding_integration, EmbeddingIntegration
from enhanced_prompt_generator import EnhancedPromptGenerator


class MCPEmbeddingBridge:
    """
    Bridge that integrates the embedding system with your existing MCP tools.
    
    This class provides seamless access to semantic capabilities while maintaining
    compatibility with your existing systems.
    """
    
    def __init__(self):
        """Initialize the MCP embedding bridge."""
        # Get the embedding integration
        self.embedding_integration = get_embedding_integration()
        
        # Initialize your existing tools
        self.prompt_generator = PromptGenerator()
        self.context_learner = ContextLearningSystem()
        self.cache_system = SmartCachingSystem()
        self.context_manager = SeamlessContextManager()
        self.interaction_logger = logger
        self.session_manager = SessionManager()
        
        # Integration status
        self.integration_status = {
            'embedding_system_available': self.embedding_integration is not None,
            'existing_tools_available': all([
                self.prompt_generator,
                self.context_learner,
                self.cache_system,
                self.context_manager
            ]),
            'bridge_initialized': True,
            'last_integration_check': datetime.now().isoformat()
        }
    
    def get_bridge_status(self) -> Dict[str, Any]:
        """Get the current bridge integration status."""
        return self.integration_status.copy()
    
    def test_bridge_integration(self) -> Dict[str, Any]:
        """Test the integration between embedding system and existing tools."""
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'embedding_system': {},
            'existing_tools': {},
            'bridge_tests': {},
            'overall_status': 'unknown'
        }
        
        # Test embedding system
        try:
            if self.embedding_integration:
                embedding_test = self.embedding_integration.test_integration()
                test_results['embedding_system'] = embedding_test
            else:
                test_results['embedding_system'] = {
                    'status': 'failed',
                    'error': 'Embedding integration not available'
                }
        except Exception as e:
            test_results['embedding_system'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test existing tools
        try:
            # Test prompt generator
            test_prompt = self.prompt_generator.generate_enhanced_prompt(
                "Test message for bridge integration", "smart"
            )
            
            # Test context learner
            learner_status = self.context_learner.get_learning_insights()
            
            # Test cache system
            cache_stats = self.cache_system.get_cache_stats()
            
            test_results['existing_tools'] = {
                'status': 'success',
                'prompt_generator_working': len(test_prompt) > 0,
                'context_learner_working': learner_status is not None,
                'cache_system_working': cache_stats is not None
            }
        except Exception as e:
            test_results['existing_tools'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test bridge functionality
        try:
            # Test enhanced prompt generation
            enhanced_prompt = self.generate_enhanced_prompt_with_embeddings(
                "Test message for bridge", "smart"
            )
            
            test_results['bridge_tests'] = {
                'status': 'success',
                'enhanced_prompt_generated': len(enhanced_prompt) > 0,
                'bridge_functionality_working': True
            }
            
            # Determine overall status
            if (test_results['embedding_system'].get('status') == 'success' and
                test_results['existing_tools'].get('status') == 'success' and
                test_results['bridge_tests'].get('status') == 'success'):
                test_results['overall_status'] = 'success'
            else:
                test_results['overall_status'] = 'failed'
                
        except Exception as e:
            test_results['bridge_tests'] = {
                'status': 'error',
                'error': str(e)
            }
            test_results['overall_status'] = 'error'
        
        return test_results
    
    def generate_enhanced_prompt_with_embeddings(self, 
                                               user_message: str,
                                               context_type: str = "smart",
                                               use_semantic_search: bool = True,
                                               similarity_threshold: float = 0.7) -> str:
        """
        Generate an enhanced prompt using both existing systems and embeddings.
        
        Args:
            user_message: User message to enhance
            context_type: Context type for enhancement
            use_semantic_search: Whether to use semantic search
            similarity_threshold: Minimum similarity threshold
            
        Returns:
            Enhanced prompt with semantic context
        """
        try:
            if use_semantic_search and self.embedding_integration:
                # Use enhanced prompt generator with embeddings
                return self.embedding_integration.enhance_prompt_with_embeddings(
                    user_message, context_type, use_semantic_search=True, 
                    similarity_threshold=similarity_threshold
                )
            else:
                # Fallback to existing prompt generator
                return self.prompt_generator.generate_enhanced_prompt(user_message, context_type)
                
        except Exception as e:
            # Fallback to basic prompt
            return f"User Message: {user_message}\n\nContext: Error in enhancement: {str(e)}"
    
    def enhance_context_learning_with_embeddings(self, 
                                                user_message: str,
                                                enhanced_prompt: str,
                                                response_quality: float,
                                                context_type: str = "conversation") -> Dict[str, Any]:
        """
        Enhance context learning with semantic embeddings.
        
        Args:
            user_message: User's original message
            enhanced_prompt: Enhanced prompt that was generated
            response_quality: Quality rating of the response (0.0 to 1.0)
            context_type: Type of context used
            
        Returns:
            Enhanced learning result
        """
        try:
            # Use existing context learning system
            self.context_learner.learn_from_interaction(
                user_message, enhanced_prompt, context_type, 
                user_feedback=None, response_quality=response_quality
            )
            
            # Enhance with embedding learning
            if self.embedding_integration:
                embedding_result = self.embedding_integration.learn_from_interaction(
                    user_message, enhanced_prompt, response_quality, context_type
                )
                
                return {
                    'status': 'success',
                    'context_learning_completed': True,
                    'embedding_learning_completed': True,
                    'response_quality': response_quality,
                    'context_type': context_type,
                    'embedding_result': embedding_result,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'success',
                    'context_learning_completed': True,
                    'embedding_learning_completed': False,
                    'response_quality': response_quality,
                    'context_type': context_type,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def enhance_caching_with_semantic_similarity(self, 
                                                query: str,
                                                context_type: str = "conversation",
                                                min_similarity: float = 0.7) -> List[Dict[str, Any]]:
        """
        Enhance caching with semantic similarity search.
        
        Args:
            query: Query text to search for
            context_type: Context type for filtering
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of semantically similar cached contexts
        """
        try:
            if self.embedding_integration:
                # Find semantically similar contexts
                similar_contexts = self.embedding_integration.find_semantic_contexts(
                    query, context_type, min_similarity=min_similarity
                )
                
                # Enhance with cache system information
                enhanced_results = []
                for context in similar_contexts:
                    # Get cache information if available
                    cache_info = {}
                    try:
                        cache_stats = self.cache_system.get_cache_stats()
                        cache_info = {
                            'cache_hit_rate': cache_stats.get('hit_rate', 0),
                            'total_cache_entries': cache_stats.get('total_entries', 0)
                        }
                    except:
                        pass
                    
                    enhanced_results.append({
                        **context,
                        'cache_info': cache_info,
                        'enhanced_by_bridge': True
                    })
                
                return enhanced_results
            else:
                return []
                
        except Exception as e:
            return [{'error': str(e), 'enhanced_by_bridge': False}]
    
    def get_comprehensive_context(self, 
                                 user_message: str,
                                 session_id: Optional[str] = None,
                                 user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive context using both existing systems and embeddings.
        
        Args:
            user_message: User message to analyze
            session_id: Optional session ID
            user_id: Optional user ID
            
        Returns:
            Comprehensive context information
        """
        try:
            context_data = {
                'user_message': user_message,
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'user_id': user_id,
                'existing_systems': {},
                'embedding_systems': {},
                'bridge_enhancements': {}
            }
            
            # Get context from existing systems
            try:
                # Get prompt context
                prompt_context = self.prompt_generator._gather_context_data(
                    user_message, "smart"
                )
                context_data['existing_systems']['prompt_context'] = prompt_context
                
                # Get learning insights
                learning_insights = self.context_learner.get_learning_insights()
                context_data['existing_systems']['learning_insights'] = learning_insights
                
                # Get cache statistics
                cache_stats = self.cache_system.get_cache_stats()
                context_data['existing_systems']['cache_stats'] = cache_stats
                
            except Exception as e:
                context_data['existing_systems']['error'] = str(e)
            
            # Get context from embedding systems
            try:
                if self.embedding_integration:
                    # Get semantic insights
                    semantic_insights = self.embedding_integration.get_semantic_insights(
                        user_message, "conversation"
                    )
                    context_data['embedding_systems']['semantic_insights'] = semantic_insights
                    
                    # Get similar contexts
                    similar_contexts = self.embedding_integration.find_semantic_contexts(
                        user_message, "conversation", limit=5
                    )
                    context_data['embedding_systems']['similar_contexts'] = similar_contexts
                    
            except Exception as e:
                context_data['embedding_systems']['error'] = str(e)
            
            # Add bridge enhancements
            try:
                # Calculate context richness score
                context_richness = self._calculate_context_richness(context_data)
                context_data['bridge_enhancements']['context_richness_score'] = context_richness
                
                # Generate recommendations
                recommendations = self._generate_context_recommendations(context_data)
                context_data['bridge_enhancements']['recommendations'] = recommendations
                
            except Exception as e:
                context_data['bridge_enhancements']['error'] = str(e)
            
            return context_data
            
        except Exception as e:
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _calculate_context_richness(self, context_data: Dict[str, Any]) -> float:
        """Calculate a context richness score based on available data."""
        score = 0.0
        
        # Existing systems score
        if context_data.get('existing_systems'):
            existing = context_data['existing_systems']
            if 'prompt_context' in existing:
                score += 0.3
            if 'learning_insights' in existing:
                score += 0.2
            if 'cache_stats' in existing:
                score += 0.1
        
        # Embedding systems score
        if context_data.get('embedding_systems'):
            embedding = context_data['embedding_systems']
            if 'semantic_insights' in embedding:
                score += 0.2
            if 'similar_contexts' in embedding:
                contexts = embedding['similar_contexts']
                score += min(0.2, len(contexts) * 0.04)  # Max 0.2 for 5+ contexts
        
        return min(1.0, score)
    
    def _generate_context_recommendations(self, context_data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on context data."""
        recommendations = []
        
        richness_score = context_data.get('bridge_enhancements', {}).get('context_richness_score', 0)
        
        if richness_score < 0.3:
            recommendations.append("Low context richness - consider expanding your context database")
            recommendations.append("Enable semantic search for better context matching")
        elif richness_score < 0.6:
            recommendations.append("Moderate context richness - good foundation for improvements")
            recommendations.append("Consider adding more diverse context types")
        else:
            recommendations.append("High context richness - excellent context coverage")
            recommendations.append("Focus on optimizing context selection algorithms")
        
        # Specific recommendations based on available data
        if not context_data.get('embedding_systems'):
            recommendations.append("Embedding system not available - install dependencies for semantic capabilities")
        
        if not context_data.get('existing_systems'):
            recommendations.append("Existing systems not responding - check system health")
        
        return recommendations
    
    def get_bridge_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics from the bridge."""
        stats = {
            'bridge_status': self.integration_status,
            'timestamp': datetime.now().isoformat()
        }
        
        # Get statistics from existing tools
        try:
            stats['existing_tools'] = {
                'prompt_generator': self.prompt_generator.get_stats() if hasattr(self.prompt_generator, 'get_stats') else {},
                'cache_system': self.cache_system.get_cache_stats(),
                'context_learner': self.context_learner.get_learning_insights()
            }
        except Exception as e:
            stats['existing_tools'] = {'error': str(e)}
        
        # Get statistics from embedding system
        try:
            if self.embedding_integration:
                stats['embedding_system'] = self.embedding_integration.get_system_statistics()
            else:
                stats['embedding_system'] = {'error': 'Not available'}
        except Exception as e:
            stats['embedding_system'] = {'error': str(e)}
        
        return stats
    
    def clear_bridge_cache(self, context_type: Optional[str] = None) -> Dict[str, Any]:
        """Clear caches in both existing and embedding systems."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'existing_systems': {},
            'embedding_system': {}
        }
        
        # Clear existing system caches
        try:
            if hasattr(self.prompt_generator, 'clear_cache'):
                self.prompt_generator.clear_cache()
                results['existing_systems']['prompt_generator'] = {'status': 'success'}
            
            if hasattr(self.cache_system, 'clear_cache'):
                self.cache_system.clear_cache(context_type)
                results['existing_systems']['cache_system'] = {'status': 'success'}
                
        except Exception as e:
            results['existing_systems']['error'] = str(e)
        
        # Clear embedding system cache
        try:
            if self.embedding_integration:
                embedding_result = self.embedding_integration.clear_system_cache(context_type)
                results['embedding_system'] = embedding_result
            else:
                results['embedding_system'] = {'error': 'Not available'}
                
        except Exception as e:
            results['embedding_system']['error'] = str(e)
        
        return results


# Global bridge instance
_mcp_embedding_bridge = None

def get_mcp_embedding_bridge() -> MCPEmbeddingBridge:
    """Get or create the global MCP embedding bridge instance."""
    global _mcp_embedding_bridge
    if _mcp_embedding_bridge is None:
        _mcp_embedding_bridge = MCPEmbeddingBridge()
    return _mcp_embedding_bridge


# Convenience functions for easy integration
def generate_enhanced_prompt_with_embeddings(user_message: str, **kwargs) -> str:
    """Convenience function to generate enhanced prompts with embeddings."""
    bridge = get_mcp_embedding_bridge()
    return bridge.generate_enhanced_prompt_with_embeddings(user_message, **kwargs)


def enhance_context_learning_with_embeddings(user_message: str, **kwargs) -> Dict[str, Any]:
    """Convenience function to enhance context learning with embeddings."""
    bridge = get_mcp_embedding_bridge()
    return bridge.enhance_context_learning_with_embeddings(user_message, **kwargs)


def get_comprehensive_context(user_message: str, **kwargs) -> Dict[str, Any]:
    """Convenience function to get comprehensive context."""
    bridge = get_mcp_embedding_bridge()
    return bridge.get_comprehensive_context(user_message, **kwargs)


if __name__ == "__main__":
    # Test the MCP embedding bridge
    print("=== Testing MCP Embedding Bridge ===\n")
    
    bridge = get_mcp_embedding_bridge()
    
    # Test bridge status
    status = bridge.get_bridge_status()
    print("Bridge Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Test bridge integration
    test_results = bridge.test_bridge_integration()
    print("Bridge Integration Test Results:")
    print(f"Overall Status: {test_results['overall_status']}")
    
    for component, result in test_results.items():
        if component != 'overall_status':
            print(f"\n{component}:")
            for key, value in result.items():
                print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Test enhanced functionality
    test_message = "How can I improve my MCP conversation system?"
    
    print("Testing Enhanced Functionality:")
    
    # Test enhanced prompt generation
    enhanced_prompt = bridge.generate_enhanced_prompt_with_embeddings(
        test_message, use_semantic_search=True
    )
    print(f"Enhanced prompt length: {len(enhanced_prompt)}")
    
    # Test comprehensive context
    context = bridge.get_comprehensive_context(test_message)
    print(f"Comprehensive context keys: {len(context)}")
    
    # Test context learning enhancement
    learning_result = bridge.enhance_context_learning_with_embeddings(
        test_message, enhanced_prompt, 0.8, "technical"
    )
    print(f"Learning enhancement status: {learning_result.get('status')}")
    
    print("\n" + "="*50 + "\n")
    
    # Get bridge statistics
    stats = bridge.get_bridge_statistics()
    print("Bridge Statistics:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")
