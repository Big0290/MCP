#!/usr/bin/env python3
"""
Test Suite for Adaptive Prompt Precision Engine (APPE)
=====================================================

Comprehensive tests for the APPE system to ensure all components work correctly
and integrate seamlessly with the existing PromptGenerator system.
"""

import json
import time
from datetime import datetime
from typing import Dict, Any

def test_appe_import():
    """Test that APPE can be imported successfully."""
    try:
        from adaptive_prompt_engine import (
            AdaptivePromptEngine,
            TaskClassificationSystem,
            PromptStrategySelector,
            PrecisionPromptCrafter,
            SuccessPatternLearner,
            TaskType,
            PromptStrategy,
            BehavioralSteering
        )
        print("✅ APPE imports successful")
        return True
    except ImportError as e:
        print(f"❌ APPE import failed: {e}")
        return False

def test_task_classification():
    """Test the task classification system."""
    try:
        from adaptive_prompt_engine import TaskClassificationSystem, TaskType
        
        classifier = TaskClassificationSystem()
        
        # Test different types of messages
        test_cases = [
            ("Create a Python function to handle authentication", TaskType.CODE_GENERATION),
            ("Fix this bug in my code", TaskType.DEBUGGING),
            ("Design a scalable architecture for microservices", TaskType.ARCHITECTURE),
            ("Explain how JWT tokens work", TaskType.LEARNING),
            ("Refactor this code to be more maintainable", TaskType.REFACTORING),
            ("Write tests for this function", TaskType.TESTING),
            ("Document this API endpoint", TaskType.DOCUMENTATION),
            ("Analyze the performance of this algorithm", TaskType.ANALYSIS),
            ("Plan the development roadmap", TaskType.PLANNING),
            ("Optimize this database query", TaskType.OPTIMIZATION)
        ]
        
        print("\n🔍 Testing Task Classification:")
        for message, expected_type in test_cases:
            analysis = classifier.analyze_task(message, {})
            print(f"  Message: '{message[:50]}...'")
            print(f"  Classified as: {analysis.task_type.value}")
            print(f"  Expected: {expected_type.value}")
            print(f"  Confidence: {analysis.confidence:.2f}")
            print(f"  Complexity: {analysis.complexity_score:.2f}")
            print()
        
        print("✅ Task classification tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Task classification test failed: {e}")
        return False

def test_strategy_selection():
    """Test the strategy selection system."""
    try:
        from adaptive_prompt_engine import (
            TaskClassificationSystem, 
            PromptStrategySelector,
            TaskAnalysis,
            TaskType,
            PromptStrategy
        )
        
        classifier = TaskClassificationSystem()
        selector = PromptStrategySelector()
        
        # Test strategy selection for different task types
        test_message = "Create a complex authentication system with JWT and OAuth"
        context = {"tech_stack": "Python, FastAPI, PostgreSQL"}
        
        analysis = classifier.analyze_task(test_message, context)
        optimization = selector.select_strategy(analysis, context)
        
        print("\n🎯 Testing Strategy Selection:")
        print(f"  Task Type: {analysis.task_type.value}")
        print(f"  Selected Strategy: {optimization.strategy.value}")
        print(f"  Behavioral Steering: {[bs.value for bs in optimization.behavioral_steering]}")
        print(f"  Max Tokens: {optimization.max_tokens}")
        print(f"  Enhancement Ratio: {optimization.enhancement_ratio}")
        print(f"  Context Priority: {optimization.context_priority}")
        
        print("✅ Strategy selection tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Strategy selection test failed: {e}")
        return False

def test_prompt_crafting():
    """Test the precision prompt crafting system."""
    try:
        from adaptive_prompt_engine import (
            TaskClassificationSystem,
            PromptStrategySelector, 
            PrecisionPromptCrafter
        )
        
        classifier = TaskClassificationSystem()
        selector = PromptStrategySelector()
        crafter = PrecisionPromptCrafter()
        
        # Test prompt crafting
        user_message = "Create a REST API endpoint for user registration"
        context = {
            "tech_stack": "Python, FastAPI, SQLAlchemy",
            "project_plans": "Building a secure web application",
            "user_preferences": "Prefer comprehensive solutions with error handling",
            "conversation_summary": "Working on authentication system"
        }
        
        analysis = classifier.analyze_task(user_message, context)
        optimization = selector.select_strategy(analysis, context)
        
        enhanced_prompt = crafter.craft_precision_prompt(
            user_message, context, optimization, analysis
        )
        
        print("\n🛠️ Testing Prompt Crafting:")
        print(f"  Original message length: {len(user_message)} chars")
        print(f"  Enhanced prompt length: {len(enhanced_prompt)} chars")
        print(f"  Enhancement ratio: {len(enhanced_prompt) / len(user_message):.2f}x")
        print("\n  Enhanced prompt preview:")
        print("  " + "="*60)
        print("  " + enhanced_prompt[:500] + "..." if len(enhanced_prompt) > 500 else enhanced_prompt)
        print("  " + "="*60)
        
        print("✅ Prompt crafting tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Prompt crafting test failed: {e}")
        return False

def test_appe_integration():
    """Test the full APPE system integration."""
    try:
        from adaptive_prompt_engine import AdaptivePromptEngine
        
        appe = AdaptivePromptEngine()
        
        # Test full prompt generation
        user_message = "Help me debug this authentication issue"
        context = {
            "tech_stack": "Python, FastAPI, JWT",
            "project_plans": "Building secure API",
            "user_preferences": "Prefer step-by-step solutions",
            "conversation_summary": "Working on auth system",
            "recent_interactions": []
        }
        
        print("\n🚀 Testing Full APPE Integration:")
        start_time = time.time()
        
        enhanced_prompt = appe.generate_optimal_prompt(user_message, context)
        
        processing_time = time.time() - start_time
        
        print(f"  Processing time: {processing_time:.3f} seconds")
        print(f"  Enhanced prompt length: {len(enhanced_prompt)} chars")
        
        # Test learning from interaction
        appe.learn_from_interaction_outcome(
            user_message, enhanced_prompt, 0.9, 0.8, processing_time
        )
        
        # Get system status
        status = appe.get_system_status()
        print(f"  System status: {status['status']}")
        print(f"  Prompts generated: {status['statistics']['prompts_generated']}")
        
        print("✅ APPE integration tests completed")
        return True
        
    except Exception as e:
        print(f"❌ APPE integration test failed: {e}")
        return False

def test_prompt_generator_integration():
    """Test APPE integration with existing PromptGenerator."""
    try:
        from prompt_generator import PromptGenerator
        
        generator = PromptGenerator()
        
        # Test adaptive strategy (should use APPE)
        user_message = "Create a secure login system with proper error handling"
        
        print("\n🔗 Testing PromptGenerator Integration:")
        
        # Test with APPE (adaptive strategy)
        start_time = time.time()
        enhanced_prompt = generator.generate_enhanced_prompt(
            user_message, 
            context_type="adaptive",
            use_appe=True
        )
        appe_time = time.time() - start_time
        
        print(f"  APPE generation time: {appe_time:.3f} seconds")
        print(f"  APPE prompt length: {len(enhanced_prompt)} chars")
        
        # Test fallback (standard strategy)
        start_time = time.time()
        standard_prompt = generator.generate_enhanced_prompt(
            user_message,
            context_type="comprehensive",
            use_appe=False
        )
        standard_time = time.time() - start_time
        
        print(f"  Standard generation time: {standard_time:.3f} seconds")
        print(f"  Standard prompt length: {len(standard_prompt)} chars")
        
        # Compare results
        print(f"  APPE vs Standard ratio: {len(enhanced_prompt) / len(standard_prompt):.2f}x")
        
        # Test learning integration
        generator.learn_from_interaction(
            user_message, enhanced_prompt, 0.9, 0.85, appe_time
        )
        
        # Get statistics
        stats = generator.get_stats()
        print(f"  APPE available: {stats.get('appe_available', False)}")
        print(f"  Total generations: {stats.get('total_generated', 0)}")
        
        print("✅ PromptGenerator integration tests completed")
        return True
        
    except Exception as e:
        print(f"❌ PromptGenerator integration test failed: {e}")
        return False

def test_success_pattern_learning():
    """Test the success pattern learning system."""
    try:
        from adaptive_prompt_engine import SuccessPatternLearner, TaskType, PromptStrategy, TaskAnalysis
        
        learner = SuccessPatternLearner("data/test_success_patterns.json")
        
        print("\n📚 Testing Success Pattern Learning:")
        
        # Simulate learning from multiple interactions
        for i in range(5):
            # Create mock task analysis
            task_analysis = TaskAnalysis(
                task_type=TaskType.CODE_GENERATION,
                complexity_score=0.7,
                urgency_level=0.3,
                context_requirements=["tech_stack"],
                technical_depth=0.8,
                creativity_needed=0.4,
                confidence=0.9,
                keywords=["function", "create", "python"],
                estimated_tokens=150
            )
            
            # Create mock optimization
            from adaptive_prompt_engine import PromptOptimization, BehavioralSteering
            optimization = PromptOptimization(
                strategy=PromptStrategy.PRECISION_TECHNICAL,
                behavioral_steering=[BehavioralSteering.IMPLEMENTATION_MODE],
                max_tokens=2000,
                context_priority=["tech_stack"],
                enhancement_ratio=2.5,
                cursor_optimizations={}
            )
            
            # Learn from interaction
            learner.learn_from_interaction(
                task_analysis, optimization, 0.8 + i*0.05, 0.7 + i*0.05, 2.0 - i*0.1
            )
        
        # Get learning insights
        insights = learner.get_learning_insights()
        print(f"  Total patterns learned: {insights['total_patterns']}")
        print(f"  Task type performance: {list(insights['task_type_performance'].keys())}")
        
        # Test optimal strategy retrieval
        optimal_strategy = learner.get_optimal_strategy(TaskType.CODE_GENERATION)
        print(f"  Optimal strategy for code generation: {optimal_strategy.value if optimal_strategy else 'None'}")
        
        print("✅ Success pattern learning tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Success pattern learning test failed: {e}")
        return False

def test_performance_benchmarks():
    """Test APPE performance benchmarks."""
    try:
        from adaptive_prompt_engine import AdaptivePromptEngine
        
        appe = AdaptivePromptEngine()
        
        print("\n⚡ Testing Performance Benchmarks:")
        
        # Test messages of different complexities
        test_messages = [
            "Fix bug",  # Simple
            "Create a Python function for user authentication",  # Medium
            "Design and implement a comprehensive microservices architecture with authentication, authorization, caching, and monitoring systems"  # Complex
        ]
        
        context = {
            "tech_stack": "Python, FastAPI, PostgreSQL, Redis, Docker",
            "project_plans": "Building enterprise web application",
            "user_preferences": "Comprehensive solutions with best practices"
        }
        
        for i, message in enumerate(test_messages):
            print(f"\n  Test {i+1}: {message[:50]}{'...' if len(message) > 50 else ''}")
            
            start_time = time.time()
            enhanced_prompt = appe.generate_optimal_prompt(message, context)
            processing_time = time.time() - start_time
            
            print(f"    Processing time: {processing_time:.3f}s")
            print(f"    Input length: {len(message)} chars")
            print(f"    Output length: {len(enhanced_prompt)} chars")
            print(f"    Enhancement ratio: {len(enhanced_prompt) / len(message):.2f}x")
            print(f"    Throughput: {len(enhanced_prompt) / processing_time:.0f} chars/sec")
        
        print("✅ Performance benchmark tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmark test failed: {e}")
        return False

def run_all_tests():
    """Run all APPE tests."""
    print("🧪 Starting Adaptive Prompt Precision Engine Test Suite")
    print("=" * 70)
    
    tests = [
        ("Import Test", test_appe_import),
        ("Task Classification", test_task_classification),
        ("Strategy Selection", test_strategy_selection),
        ("Prompt Crafting", test_prompt_crafting),
        ("APPE Integration", test_appe_integration),
        ("PromptGenerator Integration", test_prompt_generator_integration),
        ("Success Pattern Learning", test_success_pattern_learning),
        ("Performance Benchmarks", test_performance_benchmarks)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Results Summary:")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! APPE is ready for use.")
    else:
        print("⚠️  Some tests failed. Please review the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
