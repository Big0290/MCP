"""
Embedding Integration Layer for MCP Conversation Intelligence

This module provides seamless integration between the embedding system and existing
MCP tools, allowing easy access to semantic capabilities throughout the system.
"""

import time
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# Import existing systems
from embedding_manager import EmbeddingManager, get_embedding_manager_singleton
from enhanced_prompt_generator import EnhancedPromptGenerator, get_enhanced_prompt_generator_singleton
from prompt_generator import PromptGenerator


class EmbeddingIntegration:
    """
    Integration layer that connects the embedding system with existing MCP tools.
    
    Provides:
    - Easy access to semantic capabilities
    - Integration with existing prompt generation
    - MCP tool registration for embedding functions
    - Seamless fallback to existing systems
    """
    
    def __init__(self):
        """Initialize the embedding integration layer."""
        self.embedding_manager = get_embedding_manager_singleton()
        self.enhanced_generator = get_enhanced_prompt_generator_singleton()
        
        # Integration status
        self.integration_status = {
            'embedding_manager_available': self.embedding_manager is not None,
            'enhanced_generator_available': self.enhanced_generator is not None,
            'last_integration_check': datetime.now().isoformat()
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get the current integration status."""
        return self.integration_status.copy()
    
    def test_integration(self) -> Dict[str, Any]:
        """Test the integration between embedding system and existing tools."""
        test_results = {
            'timestamp': datetime.now().isoformat(),
            'embedding_manager': {},
            'enhanced_generator': {},
            'integration_tests': {},
            'overall_status': 'unknown'
        }
        
        # Test embedding manager
        try:
            if self.embedding_manager:
                # Test basic functionality
                test_text = "Integration test for embedding system"
                embedding_id = self.embedding_manager.add_embedding(
                    test_text, "test", metadata={"test": True}
                )
                
                # Test similarity search
                similar = self.embedding_manager.find_similar_contexts(test_text, limit=1)
                
                test_results['embedding_manager'] = {
                    'status': 'success',
                    'embedding_generated': True,
                    'similarity_search_working': len(similar) > 0,
                    'test_embedding_id': embedding_id
                }
            else:
                test_results['embedding_manager'] = {
                    'status': 'failed',
                    'error': 'Embedding manager not available'
                }
        except Exception as e:
            test_results['embedding_manager'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test enhanced generator
        try:
            if self.enhanced_generator:
                # Test semantic prompt generation
                test_message = "Test message for enhanced generator"
                semantic_prompt = self.enhanced_generator.generate_semantic_prompt(test_message)
                
                test_results['enhanced_generator'] = {
                    'status': 'success',
                    'semantic_prompt_generated': len(semantic_prompt) > 0,
                    'prompt_length': len(semantic_prompt)
                }
            else:
                test_results['enhanced_generator'] = {
                    'status': 'failed',
                    'error': 'Enhanced generator not available'
                }
        except Exception as e:
            test_results['enhanced_generator'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Test integration
        try:
            if (test_results['embedding_manager']['status'] == 'success' and 
                test_results['enhanced_generator']['status'] == 'success'):
                test_results['integration_tests'] = {
                    'status': 'success',
                    'end_to_end_working': True
                }
                test_results['overall_status'] = 'success'
            else:
                test_results['integration_tests'] = {
                    'status': 'failed',
                    'end_to_end_working': False
                }
                test_results['overall_status'] = 'failed'
        except Exception as e:
            test_results['integration_tests'] = {
                'status': 'error',
                'error': str(e)
            }
            test_results['overall_status'] = 'error'
        
        return test_results
    
    def enhance_prompt_with_embeddings(self, 
                                     user_message: str,
                                     context_type: str = "smart",
                                     use_semantic_search: bool = True,
                                     similarity_threshold: float = 0.7) -> str:
        """
        Enhance a prompt using the embedding system.
        
        Args:
            user_message: User message to enhance
            context_type: Context type for enhancement
            use_semantic_search: Whether to use semantic search
            similarity_threshold: Minimum similarity threshold
            
        Returns:
            Enhanced prompt with semantic context
        """
        try:
            if self.enhanced_generator and use_semantic_search:
                return self.enhanced_generator.generate_enhanced_prompt(
                    user_message, context_type, use_semantic_search=True, 
                    similarity_threshold=similarity_threshold
                )
            else:
                # Fallback to base prompt generator
                base_generator = PromptGenerator()
                return base_generator.generate_enhanced_prompt(user_message, context_type)
                
        except Exception as e:
            # Fallback to basic prompt
            return f"User Message: {user_message}\n\nContext: Error in enhancement: {str(e)}"
    
    def find_semantic_contexts(self, 
                              query: str,
                              context_type: Optional[str] = None,
                              limit: int = 5,
                              min_similarity: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Find semantically similar contexts.
        
        Args:
            query: Query text
            context_type: Optional context type filter
            limit: Maximum number of results
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of similar contexts with metadata
        """
        try:
            if self.embedding_manager:
                similar_contexts = self.embedding_manager.find_similar_contexts(
                    query, context_type, limit, min_similarity
                )
                
                # Convert to dictionary format
                results = []
                for context in similar_contexts:
                    results.append({
                        'id': context.id,
                        'text': context.text,
                        'similarity_score': context.similarity_score,
                        'context_type': context.context_type,
                        'session_id': context.session_id,
                        'user_id': context.user_id,
                        'created_at': context.created_at.isoformat(),
                        'metadata': context.metadata
                    })
                
                return results
            else:
                return []
                
        except Exception as e:
            return [{'error': str(e)}]
    
    def add_context_embedding(self, 
                             text: str,
                             context_type: str,
                             session_id: Optional[str] = None,
                             user_id: Optional[str] = None,
                             metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Add a new context embedding.
        
        Args:
            text: Text to embed
            context_type: Context type
            session_id: Optional session ID
            user_id: Optional user ID
            metadata: Additional metadata
            
        Returns:
            Result of the embedding operation
        """
        try:
            if self.embedding_manager:
                embedding_id = self.embedding_manager.add_embedding(
                    text, context_type, session_id, user_id, metadata
                )
                
                return {
                    'status': 'success',
                    'embedding_id': embedding_id,
                    'text_length': len(text),
                    'context_type': context_type,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'failed',
                    'error': 'Embedding manager not available'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_semantic_insights(self, 
                             user_message: str,
                             context_type: str = "conversation") -> Dict[str, Any]:
        """
        Get semantic insights for a user message.
        
        Args:
            user_message: User message to analyze
            context_type: Context type for analysis
            
        Returns:
            Dictionary with semantic insights
        """
        try:
            if self.enhanced_generator:
                # Get semantic context summary
                summary = self.enhanced_generator.get_semantic_context_summary(
                    user_message, context_type
                )
                
                # Add additional insights
                insights = {
                    'user_message': user_message,
                    'context_type': context_type,
                    'analysis_timestamp': datetime.now().isoformat(),
                    'semantic_context': summary,
                    'recommendations': self._generate_semantic_recommendations(summary)
                }
                
                return insights
            else:
                return {
                    'user_message': user_message,
                    'context_type': context_type,
                    'error': 'Enhanced generator not available',
                    'analysis_timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                'user_message': user_message,
                'context_type': context_type,
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def _generate_semantic_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on semantic context summary."""
        recommendations = []
        
        if summary.get('similar_contexts_found', 0) == 0:
            recommendations.append("No similar contexts found - consider expanding your context database")
            recommendations.append("The current query may be unique or require different context types")
        else:
            contexts = summary.get('contexts', [])
            if contexts:
                avg_similarity = sum(c.get('similarity_score', 0) for c in contexts) / len(contexts)
                
                if avg_similarity > 0.8:
                    recommendations.append("High similarity contexts found - excellent context match")
                    recommendations.append("Consider using these contexts for comprehensive responses")
                elif avg_similarity > 0.6:
                    recommendations.append("Good similarity contexts found - solid context match")
                    recommendations.append("Contexts should provide relevant information")
                else:
                    recommendations.append("Low similarity contexts found - consider refining search")
                    recommendations.append("May need to adjust similarity threshold or context type")
        
        return recommendations
    
    def learn_from_interaction(self, 
                              user_message: str,
                              enhanced_prompt: str,
                              response_quality: float,
                              context_type: str = "conversation") -> Dict[str, Any]:
        """
        Learn from user interactions to improve future semantic context selection.
        
        Args:
            user_message: User's original message
            enhanced_prompt: Enhanced prompt that was generated
            response_quality: Quality rating of the response (0.0 to 1.0)
            context_type: Type of context used
            
        Returns:
            Learning result
        """
        try:
            if self.enhanced_generator:
                self.enhanced_generator.learn_from_interaction(
                    user_message, enhanced_prompt, response_quality, context_type
                )
                
                return {
                    'status': 'success',
                    'learning_completed': True,
                    'response_quality': response_quality,
                    'context_type': context_type,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'failed',
                    'error': 'Enhanced generator not available for learning'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics from the embedding system."""
        stats = {
            'integration_status': self.integration_status,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add embedding manager stats
        if self.embedding_manager:
            try:
                embedding_stats = self.embedding_manager.get_embedding_stats()
                stats['embedding_system'] = embedding_stats
            except Exception as e:
                stats['embedding_system'] = {'error': str(e)}
        
        # Add enhanced generator stats
        if self.enhanced_generator:
            try:
                enhanced_stats = self.enhanced_generator.get_enhanced_stats()
                stats['enhanced_generator'] = enhanced_stats
            except Exception as e:
                stats['enhanced_generator'] = {'error': str(e)}
        
        return stats
    
    def clear_system_cache(self, context_type: Optional[str] = None) -> Dict[str, Any]:
        """Clear caches in the embedding system."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'embedding_cache': {},
            'generator_cache': {}
        }
        
        # Clear embedding cache
        if self.embedding_manager:
            try:
                self.embedding_manager.clear_embeddings(context_type)
                results['embedding_cache'] = {
                    'status': 'success',
                    'cleared_context_type': context_type or 'all'
                }
            except Exception as e:
                results['embedding_cache'] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # Clear generator cache
        if self.enhanced_generator:
            try:
                self.enhanced_generator.clear_embedding_cache(context_type)
                results['generator_cache'] = {
                    'status': 'success',
                    'cleared_context_type': context_type or 'all'
                }
            except Exception as e:
                results['generator_cache'] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return results


# Global integration instance
_embedding_integration = None

def get_embedding_integration() -> EmbeddingIntegration:
    """Get or create the global embedding integration instance."""
    global _embedding_integration
    if _embedding_integration is None:
        _embedding_integration = EmbeddingIntegration()
    return _embedding_integration


# Convenience functions for easy access
def enhance_prompt_with_embeddings(user_message: str, **kwargs) -> str:
    """Convenience function to enhance a prompt with embeddings."""
    integration = get_embedding_integration()
    return integration.enhance_prompt_with_embeddings(user_message, **kwargs)


def find_semantic_contexts(query: str, **kwargs) -> List[Dict[str, Any]]:
    """Convenience function to find semantic contexts."""
    integration = get_embedding_integration()
    return integration.find_semantic_contexts(query, **kwargs)


def add_context_embedding(text: str, context_type: str, **kwargs) -> Dict[str, Any]:
    """Convenience function to add a context embedding."""
    integration = get_embedding_integration()
    return integration.add_context_embedding(text, context_type, **kwargs)


def get_semantic_insights(user_message: str, **kwargs) -> Dict[str, Any]:
    """Convenience function to get semantic insights."""
    integration = get_embedding_integration()
    return integration.get_semantic_insights(user_message, **kwargs)


if __name__ == "__main__":
    # Test the embedding integration
    print("=== Testing Embedding Integration ===\n")
    
    integration = get_embedding_integration()
    
    # Test integration status
    status = integration.get_integration_status()
    print("Integration Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Test integration functionality
    test_results = integration.test_integration()
    print("Integration Test Results:")
    print(f"Overall Status: {test_results['overall_status']}")
    
    for component, result in test_results.items():
        if component != 'overall_status':
            print(f"\n{component}:")
            for key, value in result.items():
                print(f"  {key}: {value}")
    
    print("\n" + "="*50 + "\n")
    
    # Test semantic functionality
    test_message = "How to implement semantic search in my system?"
    
    print("Testing Semantic Functionality:")
    
    # Test prompt enhancement
    enhanced = integration.enhance_prompt_with_embeddings(test_message)
    print(f"Enhanced prompt length: {len(enhanced)}")
    
    # Test semantic context search
    contexts = integration.find_semantic_contexts(test_message)
    print(f"Found {len(contexts)} semantic contexts")
    
    # Test semantic insights
    insights = integration.get_semantic_insights(test_message)
    print(f"Generated insights: {len(insights)} keys")
    
    print("\n" + "="*50 + "\n")
    
    # Test system statistics
    stats = integration.get_system_statistics()
    print("System Statistics:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for sub_key, sub_value in value.items():
                print(f"    {sub_key}: {sub_value}")
        else:
            print(f"  {key}: {value}")
