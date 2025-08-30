"""
Enhanced Prompt Generator with Embedding Integration

This module extends the existing PromptGenerator with semantic embedding capabilities
to provide more intelligent and contextually relevant prompt enhancement.
"""

import time
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

# Import existing systems
from prompt_generator import PromptGenerator, PromptContext
from embedding_manager import EmbeddingManager, get_embedding_manager_singleton


class EnhancedPromptGenerator(PromptGenerator):
    """
    Enhanced prompt generator that uses semantic embeddings for intelligent context injection.
    
    Extends the base PromptGenerator with:
    - Semantic similarity search for context matching
    - Intelligent context selection based on embeddings
    - Enhanced confidence scoring using similarity metrics
    - Automatic embedding generation and management
    """
    
    def __init__(self, embedding_manager: Optional[EmbeddingManager] = None):
        """
        Initialize the enhanced prompt generator.
        
        Args:
            embedding_manager: Optional embedding manager instance
        """
        super().__init__()
        
        # Initialize embedding manager
        self.embedding_manager = embedding_manager or get_embedding_manager_singleton()
        
        # Enhanced statistics
        self.embedding_stats = {
            'semantic_searches': 0,
            'context_matches_found': 0,
            'embedding_generation_time': 0.0,
            'similarity_threshold_met': 0
        }
    
    def generate_enhanced_prompt(self, 
                                user_message: str, 
                                context_type: str = "smart",
                                force_refresh: bool = False,
                                use_semantic_search: bool = True,
                                similarity_threshold: float = 0.7) -> str:
        """
        Generate an enhanced prompt using semantic embeddings.
        
        Args:
            user_message: The user's message to enhance
            context_type: Type of context to use
            force_refresh: Force refresh of cached results
            use_semantic_search: Whether to use semantic similarity search
            similarity_threshold: Minimum similarity score for context inclusion
            
        Returns:
            Enhanced prompt with semantically relevant context
        """
        start_time = time.time()
        
        try:
            # Generate base enhanced prompt
            base_prompt = super().generate_enhanced_prompt(user_message, context_type, force_refresh)
            
            # Enhance with semantic context if enabled
            if use_semantic_search:
                enhanced_prompt = self._enhance_with_semantic_context(
                    user_message, base_prompt, context_type, similarity_threshold
                )
            else:
                enhanced_prompt = base_prompt
            
            # Update statistics
            self._update_embedding_stats(time.time() - start_time)
            
            return enhanced_prompt
            
        except Exception as e:
            self.logger.error(f"Error in enhanced prompt generation: {e}")
            # Fallback to base prompt
            return super().generate_enhanced_prompt(user_message, context_type, force_refresh)
    
    def _enhance_with_semantic_context(self, 
                                     user_message: str,
                                     base_prompt: str,
                                     context_type: str,
                                     similarity_threshold: float) -> str:
        """
        Enhance the base prompt with semantically relevant context.
        
        Args:
            user_message: Original user message
            base_prompt: Base enhanced prompt
            context_type: Context type for filtering
            similarity_threshold: Minimum similarity score
            
        Returns:
            Enhanced prompt with semantic context
        """
        try:
            # Find semantically similar contexts
            similar_contexts = self.embedding_manager.find_similar_contexts(
                query=user_message,
                context_type=context_type,
                limit=5,
                min_similarity=similarity_threshold
            )
            
            if not similar_contexts:
                return base_prompt
            
            # Update statistics
            self.embedding_stats['semantic_searches'] += 1
            self.embedding_stats['context_matches_found'] += len(similar_contexts)
            
            # Build semantic context section
            semantic_context = self._build_semantic_context_section(similar_contexts)
            
            # Inject semantic context into the prompt
            enhanced_prompt = self._inject_semantic_context(base_prompt, semantic_context)
            
            return enhanced_prompt
            
        except Exception as e:
            self.logger.error(f"Error in semantic context enhancement: {e}")
            return base_prompt
    
    def _build_semantic_context_section(self, similar_contexts: List) -> str:
        """
        Build a semantic context section from similar contexts.
        
        Args:
            similar_contexts: List of similar embedding entries
            
        Returns:
            Formatted semantic context section
        """
        if not similar_contexts:
            return ""
        
        # Sort by similarity score
        sorted_contexts = sorted(similar_contexts, 
                               key=lambda x: x.similarity_score or 0, 
                               reverse=True)
        
        context_section = "\n\n=== 🔍 SEMANTICALLY RELEVANT CONTEXT ===\n"
        context_section += "Based on semantic similarity analysis, here are relevant contexts:\n\n"
        
        for i, context in enumerate(sorted_contexts[:3], 1):  # Top 3 most similar
            similarity = context.similarity_score or 0
            context_section += f"{i}. **Relevance: {similarity:.3f}**\n"
            context_section += f"   **Context:** {context.text}\n"
            
            if context.metadata:
                metadata_str = ", ".join([f"{k}: {v}" for k, v in context.metadata.items()])
                context_section += f"   **Metadata:** {metadata_str}\n"
            
            context_section += "\n"
        
        context_section += "This context has been automatically selected based on semantic similarity "
        context_section += "to your current query, ensuring the most relevant information is included.\n"
        
        return context_section
    
    def _inject_semantic_context(self, base_prompt: str, semantic_context: str) -> str:
        """
        Inject semantic context into the base prompt.
        
        Args:
            base_prompt: Base enhanced prompt
            semantic_context: Semantic context section
            
        Returns:
            Prompt with injected semantic context
        """
        # Find a good insertion point (after the main context, before instructions)
        insertion_points = [
            "=== 🎯 INSTRUCTIONS ===",
            "=== 🚀 END ENHANCED PROMPT ===",
            "Please respond to the user's message above"
        ]
        
        for point in insertion_points:
            if point in base_prompt:
                # Insert before the insertion point
                parts = base_prompt.split(point)
                if len(parts) == 2:
                    return parts[0] + semantic_context + "\n\n" + point + parts[1]
        
        # If no good insertion point found, append at the end
        return base_prompt + semantic_context
    
    def generate_semantic_prompt(self, 
                                user_message: str,
                                context_type: str = "conversation",
                                max_similar_contexts: int = 5,
                                similarity_threshold: float = 0.6) -> str:
        """
        Generate a prompt specifically optimized for semantic context.
        
        Args:
            user_message: User message to enhance
            context_type: Context type for filtering
            max_similar_contexts: Maximum number of similar contexts to include
            similarity_threshold: Minimum similarity score
            
        Returns:
            Semantically optimized prompt
        """
        try:
            # Find semantically similar contexts
            similar_contexts = self.embedding_manager.find_similar_contexts(
                query=user_message,
                context_type=context_type,
                limit=max_similar_contexts,
                min_similarity=similarity_threshold
            )
            
            # Build semantic prompt
            semantic_prompt = self._build_semantic_prompt(user_message, similar_contexts)
            
            # Update statistics
            self.embedding_stats['semantic_searches'] += 1
            self.embedding_stats['context_matches_found'] += len(similar_contexts)
            
            return semantic_prompt
            
        except Exception as e:
            self.logger.error(f"Error in semantic prompt generation: {e}")
            # Fallback to basic prompt
            return f"User Message: {user_message}\n\nContext: Unable to generate semantic context due to error."
    
    def _build_semantic_prompt(self, user_message: str, similar_contexts: List) -> str:
        """
        Build a semantic prompt from similar contexts.
        
        Args:
            user_message: User message
            similar_contexts: List of similar contexts
            
        Returns:
            Formatted semantic prompt
        """
        prompt = f"=== 🚀 SEMANTIC CONTEXT ENHANCED PROMPT ===\n\n"
        prompt += f"USER MESSAGE: {user_message}\n\n"
        
        if similar_contexts:
            prompt += "=== 🔍 SEMANTICALLY RELEVANT CONTEXTS ===\n"
            prompt += "The following contexts were selected based on semantic similarity:\n\n"
            
            for i, context in enumerate(similar_contexts, 1):
                similarity = context.similarity_score or 0
                prompt += f"{i}. **Similarity Score: {similarity:.3f}**\n"
                prompt += f"   **Context:** {context.text}\n"
                
                if context.metadata:
                    for key, value in context.metadata.items():
                        prompt += f"   **{key.title()}:** {value}\n"
                
                prompt += "\n"
            
            prompt += "=== 🎯 INSTRUCTIONS ===\n"
            prompt += "Please respond to the user's message, taking into account:\n"
            prompt += "1. The semantically relevant contexts above\n"
            prompt += "2. The similarity scores to understand context relevance\n"
            prompt += "3. Any metadata that provides additional context\n"
            prompt += "4. The user's specific query and intent\n\n"
            prompt += "Provide a response that leverages the most relevant contexts "
            prompt += "while addressing the user's current needs.\n"
        else:
            prompt += "=== ⚠️ NO SEMANTIC CONTEXTS FOUND ===\n"
            prompt += "No semantically similar contexts were found for this query.\n"
            prompt += "Please provide a general response based on your knowledge.\n"
        
        prompt += "\n=== 🚀 END SEMANTIC PROMPT ==="
        return prompt
    
    def learn_from_interaction(self, 
                              user_message: str,
                              enhanced_prompt: str,
                              response_quality: float,
                              context_type: str = "conversation"):
        """
        Learn from user interactions to improve future semantic context selection.
        
        Args:
            user_message: User's original message
            enhanced_prompt: Enhanced prompt that was generated
            response_quality: Quality rating of the response (0.0 to 1.0)
            context_type: Type of context used
        """
        try:
            # Add the user message as an embedding for future reference
            self.embedding_manager.add_embedding(
                text=user_message,
                context_type=context_type,
                metadata={
                    'response_quality': response_quality,
                    'enhanced_prompt_length': len(enhanced_prompt),
                    'timestamp': datetime.now().isoformat(),
                    'source': 'enhanced_prompt_generator'
                }
            )
            
            # Add the enhanced prompt as well for context learning
            self.embedding_manager.add_embedding(
                text=enhanced_prompt[:500],  # Limit length for embedding
                context_type=f"{context_type}_enhanced",
                metadata={
                    'original_message_length': len(user_message),
                    'response_quality': response_quality,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'enhanced_prompt_generator'
                }
            )
            
            self.logger.info(f"Learned from interaction with quality {response_quality}")
            
        except Exception as e:
            self.logger.error(f"Error learning from interaction: {e}")
    
    def get_semantic_context_summary(self, 
                                   user_message: str,
                                   context_type: str = "conversation",
                                   limit: int = 3) -> Dict[str, Any]:
        """
        Get a summary of semantically relevant contexts for a user message.
        
        Args:
            user_message: User message to analyze
            context_type: Context type for filtering
            limit: Maximum number of contexts to return
            
        Returns:
            Dictionary with semantic context summary
        """
        try:
            similar_contexts = self.embedding_manager.find_similar_contexts(
                query=user_message,
                context_type=context_type,
                limit=limit
            )
            
            summary = {
                'user_message': user_message,
                'context_type': context_type,
                'similar_contexts_found': len(similar_contexts),
                'contexts': []
            }
            
            for context in similar_contexts:
                summary['contexts'].append({
                    'text': context.text,
                    'similarity_score': context.similarity_score,
                    'metadata': context.metadata,
                    'created_at': context.created_at.isoformat()
                })
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error getting semantic context summary: {e}")
            return {
                'user_message': user_message,
                'context_type': context_type,
                'error': str(e),
                'similar_contexts_found': 0,
                'contexts': []
            }
    
    def _update_embedding_stats(self, processing_time: float):
        """Update embedding-related statistics."""
        self.embedding_stats['embedding_generation_time'] += processing_time
        
        # Update base stats
        if hasattr(self, '_update_stats'):
            self._update_stats(True, processing_time)
    
    def get_enhanced_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics including embedding metrics."""
        base_stats = super().get_stats() if hasattr(self, 'get_stats') else {}
        
        # Combine base stats with embedding stats
        enhanced_stats = {
            **base_stats,
            'embedding_stats': self.embedding_stats.copy(),
            'embedding_manager_available': self.embedding_manager is not None
        }
        
        # Add embedding manager stats if available
        if self.embedding_manager:
            try:
                embedding_stats = self.embedding_manager.get_embedding_stats()
                enhanced_stats['embedding_system_stats'] = embedding_stats
            except Exception as e:
                enhanced_stats['embedding_system_stats'] = {'error': str(e)}
        
        return enhanced_stats
    
    def clear_embedding_cache(self, context_type: Optional[str] = None):
        """Clear embedding cache for specific context type or all."""
        if self.embedding_manager:
            try:
                self.embedding_manager.clear_embeddings(context_type)
                self.logger.info(f"Cleared embedding cache for {context_type or 'all'}")
            except Exception as e:
                self.logger.error(f"Error clearing embedding cache: {e}")


# Convenience functions for easy integration
def create_enhanced_prompt_generator(**kwargs) -> EnhancedPromptGenerator:
    """Create a new enhanced prompt generator instance."""
    return EnhancedPromptGenerator(**kwargs)


def get_enhanced_prompt_generator_singleton() -> EnhancedPromptGenerator:
    """Get or create a singleton enhanced prompt generator instance."""
    if not hasattr(get_enhanced_prompt_generator_singleton, '_instance'):
        get_enhanced_prompt_generator_singleton._instance = create_enhanced_prompt_generator()
    return get_enhanced_prompt_generator_singleton._instance


if __name__ == "__main__":
    # Test the enhanced prompt generator
    generator = create_enhanced_prompt_generator()
    
    # Test semantic prompt generation
    test_message = "How can I improve my prompt generation system?"
    
    print("=== Testing Enhanced Prompt Generator ===\n")
    
    # Generate semantic prompt
    semantic_prompt = generator.generate_semantic_prompt(test_message)
    print("Semantic Prompt:")
    print(semantic_prompt)
    print("\n" + "="*50 + "\n")
    
    # Generate enhanced prompt with semantic context
    enhanced_prompt = generator.generate_enhanced_prompt(test_message, use_semantic_search=True)
    print("Enhanced Prompt with Semantic Context:")
    print(enhanced_prompt[:500] + "..." if len(enhanced_prompt) > 500 else enhanced_prompt)
    print("\n" + "="*50 + "\n")
    
    # Get semantic context summary
    summary = generator.get_semantic_context_summary(test_message)
    print("Semantic Context Summary:")
    print(f"Contexts found: {summary['similar_contexts_found']}")
    for i, context in enumerate(summary['contexts'], 1):
        print(f"{i}. Similarity: {context['similarity_score']:.3f}")
        print(f"   Text: {context['text'][:100]}...")
    
    print("\n" + "="*50 + "\n")
    
    # Get enhanced stats
    stats = generator.get_enhanced_stats()
    print("Enhanced Statistics:")
    for key, value in stats.items():
        if key == 'embedding_stats':
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")
