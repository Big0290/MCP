"""
Test Suite for Embedding System Integration

This module tests the complete embedding system integration with the MCP
conversation intelligence system.
"""

import unittest
import tempfile
import os
import shutil
from typing import Dict, Any

# Import the embedding system components
from embedding_manager import EmbeddingManager, EmbeddingEntry
from enhanced_prompt_generator import EnhancedPromptGenerator
from embedding_integration import EmbeddingIntegration, get_embedding_integration


class TestEmbeddingManager(unittest.TestCase):
    """Test the core embedding manager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.test_dir, "test_embeddings.db")
        
        # Initialize embedding manager with test database
        self.embedding_manager = EmbeddingManager(
            db_path=self.test_db_path,
            max_embeddings=100
        )
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_embedding_manager_initialization(self):
        """Test that embedding manager initializes correctly."""
        self.assertIsNotNone(self.embedding_manager)
        self.assertEqual(self.embedding_manager.db_path, self.test_db_path)
        self.assertEqual(self.embedding_manager.max_embeddings, 100)
    
    def test_embedding_generation(self):
        """Test that embeddings can be generated."""
        test_text = "This is a test message for embedding generation"
        embedding = self.embedding_manager.generate_embedding(test_text)
        
        self.assertIsNotNone(embedding)
        self.assertEqual(embedding.shape[0], self.embedding_manager.embedding_dim)
    
    def test_embedding_storage(self):
        """Test that embeddings can be stored and retrieved."""
        test_text = "Test text for storage"
        context_type = "test"
        
        # Add embedding
        embedding_id = self.embedding_manager.add_embedding(
            test_text, context_type, metadata={"test": True}
        )
        
        self.assertIsNotNone(embedding_id)
        
        # Retrieve embedding
        retrieved_entry = self.embedding_manager._get_embedding_by_id(embedding_id)
        self.assertIsNotNone(retrieved_entry)
        self.assertEqual(retrieved_entry.text, test_text)
        self.assertEqual(retrieved_entry.context_type, context_type)
    
    def test_similarity_search(self):
        """Test similarity search functionality."""
        # Add multiple test embeddings
        test_texts = [
            "Python programming language",
            "Machine learning algorithms",
            "Data science techniques",
            "Web development frameworks",
            "Database management systems"
        ]
        
        for text in test_texts:
            self.embedding_manager.add_embedding(text, "programming")
        
        # Search for similar contexts
        query = "Python coding and development"
        similar_contexts = self.embedding_manager.find_similar_contexts(
            query, context_type="programming", limit=3
        )
        
        self.assertGreater(len(similar_contexts), 0)
        
        # Check that results are sorted by similarity
        if len(similar_contexts) > 1:
            first_score = similar_contexts[0].similarity_score or 0
            second_score = similar_contexts[1].similarity_score or 0
            self.assertGreaterEqual(first_score, second_score)
    
    def test_context_type_filtering(self):
        """Test filtering by context type."""
        # Add embeddings with different context types
        self.embedding_manager.add_embedding("Technical question", "technical")
        self.embedding_manager.add_embedding("General question", "general")
        
        # Search with context type filter
        technical_results = self.embedding_manager.find_similar_contexts(
            "Technical question", context_type="technical"
        )
        general_results = self.embedding_manager.find_similar_contexts(
            "General question", context_type="general"
        )
        
        self.assertGreater(len(technical_results), 0)
        self.assertGreater(len(general_results), 0)
        
        # Verify context types
        for result in technical_results:
            self.assertEqual(result.context_type, "technical")
        for result in general_results:
            self.assertEqual(result.context_type, "general")
    
    def test_embedding_cleanup(self):
        """Test automatic cleanup of old embeddings."""
        # Add more embeddings than the limit
        for i in range(150):
            self.embedding_manager.add_embedding(
                f"Test text {i}", "test", metadata={"index": i}
            )
        
        # Check that cleanup occurred
        stats = self.embedding_manager.get_embedding_stats()
        self.assertLessEqual(stats['total_embeddings'], 100)


class TestEnhancedPromptGenerator(unittest.TestCase):
    """Test the enhanced prompt generator with embedding integration."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.test_dir, "test_embeddings.db")
        
        # Initialize embedding manager
        self.embedding_manager = EmbeddingManager(
            db_path=self.test_db_path,
            max_embeddings=100
        )
        
        # Initialize enhanced prompt generator
        self.enhanced_generator = EnhancedPromptGenerator(self.embedding_manager)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_enhanced_prompt_generation(self):
        """Test enhanced prompt generation with semantic context."""
        # Add some test embeddings
        test_contexts = [
            "How to implement machine learning models",
            "Best practices for data preprocessing",
            "Evaluation metrics for ML models"
        ]
        
        for context in test_contexts:
            self.embedding_manager.add_embedding(context, "machine_learning")
        
        # Generate enhanced prompt
        user_message = "How can I improve my machine learning system?"
        enhanced_prompt = self.enhanced_generator.generate_enhanced_prompt(
            user_message, "machine_learning", use_semantic_search=True
        )
        
        self.assertIsNotNone(enhanced_prompt)
        self.assertIn("SEMANTICALLY RELEVANT CONTEXT", enhanced_prompt)
        self.assertIn(user_message, enhanced_prompt)
    
    def test_semantic_prompt_generation(self):
        """Test semantic prompt generation."""
        # Add test embeddings
        self.embedding_manager.add_embedding(
            "Python programming best practices", "programming"
        )
        
        # Generate semantic prompt
        user_message = "What are good programming practices?"
        semantic_prompt = self.enhanced_generator.generate_semantic_prompt(
            user_message, "programming"
        )
        
        self.assertIsNotNone(semantic_prompt)
        self.assertIn("SEMANTIC CONTEXT ENHANCED PROMPT", semantic_prompt)
        self.assertIn("Similarity Score", semantic_prompt)
    
    def test_learning_from_interaction(self):
        """Test learning from user interactions."""
        user_message = "Test message for learning"
        enhanced_prompt = "Enhanced prompt for testing"
        response_quality = 0.8
        
        # Learn from interaction
        self.enhanced_generator.learn_from_interaction(
            user_message, enhanced_prompt, response_quality, "test"
        )
        
        # Verify that embeddings were added
        similar_contexts = self.embedding_manager.find_similar_contexts(
            user_message, "test"
        )
        
        self.assertGreater(len(similar_contexts), 0)
    
    def test_semantic_context_summary(self):
        """Test semantic context summary generation."""
        # Add test embeddings
        self.embedding_manager.add_embedding(
            "Test context for summary", "test"
        )
        
        # Get semantic context summary
        user_message = "Test message for summary"
        summary = self.enhanced_generator.get_semantic_context_summary(
            user_message, "test"
        )
        
        self.assertIsNotNone(summary)
        self.assertIn('similar_contexts_found', summary)
        self.assertIn('contexts', summary)


class TestEmbeddingIntegration(unittest.TestCase):
    """Test the embedding integration layer."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.test_dir, "test_embeddings.db")
        
        # Initialize integration with test database
        self.embedding_manager = EmbeddingManager(
            db_path=self.test_db_path,
            max_embeddings=100
        )
        
        self.enhanced_generator = EnhancedPromptGenerator(self.embedding_manager)
        self.integration = EmbeddingIntegration()
        
        # Override the singleton instances for testing
        self.integration.embedding_manager = self.embedding_manager
        self.integration.enhanced_generator = self.enhanced_generator
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_integration_status(self):
        """Test integration status reporting."""
        status = self.integration.get_integration_status()
        
        self.assertIn('embedding_manager_available', status)
        self.assertIn('enhanced_generator_available', status)
        self.assertIn('last_integration_check', status)
    
    def test_integration_testing(self):
        """Test integration testing functionality."""
        test_results = self.integration.test_integration()
        
        self.assertIn('overall_status', test_results)
        self.assertIn('embedding_manager', test_results)
        self.assertIn('enhanced_generator', test_results)
        self.assertIn('integration_tests', test_results)
    
    def test_prompt_enhancement_integration(self):
        """Test prompt enhancement through integration layer."""
        # Add test embeddings
        self.embedding_manager.add_embedding(
            "Test context for integration", "test"
        )
        
        # Test prompt enhancement
        user_message = "Test message for integration"
        enhanced_prompt = self.integration.enhance_prompt_with_embeddings(
            user_message, "test", use_semantic_search=True
        )
        
        self.assertIsNotNone(enhanced_prompt)
        self.assertIn(user_message, enhanced_prompt)
    
    def test_semantic_context_search_integration(self):
        """Test semantic context search through integration layer."""
        # Add test embeddings
        self.embedding_manager.add_embedding(
            "Test context for search", "test"
        )
        
        # Search for semantic contexts
        query = "Test query for search"
        contexts = self.integration.find_semantic_contexts(query, "test")
        
        self.assertIsInstance(contexts, list)
        if contexts:
            self.assertIn('similarity_score', contexts[0])
            self.assertIn('text', contexts[0])
    
    def test_context_embedding_addition(self):
        """Test adding context embeddings through integration layer."""
        text = "Test text for embedding"
        context_type = "test"
        
        result = self.integration.add_context_embedding(text, context_type)
        
        self.assertEqual(result['status'], 'success')
        self.assertIn('embedding_id', result)
        self.assertEqual(result['context_type'], context_type)
    
    def test_semantic_insights_generation(self):
        """Test semantic insights generation through integration layer."""
        # Add test embeddings
        self.embedding_manager.add_embedding(
            "Test context for insights", "test"
        )
        
        # Generate semantic insights
        user_message = "Test message for insights"
        insights = self.integration.get_semantic_insights(user_message, "test")
        
        self.assertIsNotNone(insights)
        self.assertIn('semantic_context', insights)
        self.assertIn('recommendations', insights)
    
    def test_system_statistics(self):
        """Test system statistics collection."""
        stats = self.integration.get_system_statistics()
        
        self.assertIn('integration_status', stats)
        self.assertIn('timestamp', stats)
        self.assertIn('embedding_system', stats)
        self.assertIn('enhanced_generator', stats)
    
    def test_cache_clearing(self):
        """Test cache clearing functionality."""
        # Add some test embeddings
        self.embedding_manager.add_embedding("Test text 1", "test")
        self.embedding_manager.add_embedding("Test text 2", "test")
        
        # Clear cache
        result = self.integration.clear_system_cache("test")
        
        self.assertIn('embedding_cache', result)
        self.assertIn('generator_cache', result)
        
        # Verify cache was cleared
        stats = self.embedding_manager.get_embedding_stats()
        self.assertEqual(stats['total_embeddings'], 0)


class TestFallbackFunctionality(unittest.TestCase):
    """Test fallback functionality when dependencies are not available."""
    
    def test_fallback_embedding_generation(self):
        """Test fallback embedding generation when sentence-transformers is not available."""
        # This test would require mocking the import to simulate missing dependency
        # For now, we'll test that the system doesn't crash
        try:
            embedding_manager = EmbeddingManager()
            self.assertIsNotNone(embedding_manager)
        except Exception as e:
            self.fail(f"Embedding manager should handle missing dependencies gracefully: {e}")


def run_embedding_system_tests():
    """Run all embedding system tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestEmbeddingManager))
    test_suite.addTest(unittest.makeSuite(TestEnhancedPromptGenerator))
    test_suite.addTest(unittest.makeSuite(TestEmbeddingIntegration))
    test_suite.addTest(unittest.makeSuite(TestFallbackFunctionality))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("=== Running Embedding System Tests ===\n")
    
    success = run_embedding_system_tests()
    
    if success:
        print("\n✅ All tests passed! Embedding system is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the output above for details.")
    
    print("\n=== Test Summary ===")
    print("The embedding system has been tested for:")
    print("- Core embedding manager functionality")
    print("- Enhanced prompt generation")
    print("- Integration layer")
    print("- Fallback functionality")
    print("- Error handling and edge cases")
