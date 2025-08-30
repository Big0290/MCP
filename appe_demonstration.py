#!/usr/bin/env python3
"""
Adaptive Prompt Precision Engine (APPE) Demonstration
====================================================

This script demonstrates the capabilities of the APPE system and shows
how it improves prompt generation for different types of tasks.
"""

import json
import time
from typing import Dict, Any

def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "="*80)
    print(f"🚀 {title}")
    print("="*80)

def print_section(title: str):
    """Print a formatted section."""
    print(f"\n📋 {title}")
    print("-" * 60)

def print_comparison(original: str, enhanced: str, strategy: str):
    """Print a comparison between original and enhanced prompts."""
    print(f"\n🔍 Strategy: {strategy}")
    print(f"📏 Original length: {len(original)} characters")
    print(f"📏 Enhanced length: {len(enhanced)} characters")
    print(f"📈 Enhancement ratio: {len(enhanced) / len(original):.2f}x")
    
    print(f"\n📝 Original prompt:")
    print(f"   '{original}'")
    
    print(f"\n✨ Enhanced prompt preview:")
    preview = enhanced[:300] + "..." if len(enhanced) > 300 else enhanced
    for line in preview.split('\n'):
        print(f"   {line}")

def demonstrate_task_classification():
    """Demonstrate the task classification system."""
    print_header("Task Classification System")
    
    try:
        from adaptive_prompt_engine import TaskClassificationSystem
        
        classifier = TaskClassificationSystem()
        
        test_cases = [
            "Create a secure authentication system with JWT tokens",
            "Fix this memory leak in my Python application", 
            "Design a scalable microservices architecture",
            "Explain how machine learning algorithms work",
            "Refactor this legacy code to use modern patterns",
            "Write comprehensive tests for the API endpoints",
            "Document the REST API with OpenAPI specification",
            "Analyze the performance bottlenecks in this system",
            "Plan the development roadmap for next quarter",
            "Optimize this database query for better performance"
        ]
        
        print("Analyzing different types of user requests:")
        
        for i, message in enumerate(test_cases, 1):
            analysis = classifier.analyze_task(message, {})
            
            print(f"\n{i:2d}. '{message[:50]}{'...' if len(message) > 50 else ''}'")
            print(f"    🎯 Task Type: {analysis.task_type.value}")
            print(f"    📊 Confidence: {analysis.confidence:.2f}")
            print(f"    🔧 Complexity: {analysis.complexity_score:.2f}")
            print(f"    ⚡ Urgency: {analysis.urgency_level:.2f}")
            print(f"    🧠 Technical Depth: {analysis.technical_depth:.2f}")
            print(f"    🎨 Creativity Needed: {analysis.creativity_needed:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Task classification demonstration failed: {e}")
        return False

def demonstrate_strategy_selection():
    """Demonstrate the strategy selection system."""
    print_header("Strategy Selection System")
    
    try:
        from adaptive_prompt_engine import TaskClassificationSystem, PromptStrategySelector
        
        classifier = TaskClassificationSystem()
        selector = PromptStrategySelector()
        
        test_scenarios = [
            {
                "message": "Create a REST API for user management",
                "context": {"tech_stack": "Python, FastAPI, PostgreSQL"}
            },
            {
                "message": "URGENT: Fix production database connection issue",
                "context": {"tech_stack": "Node.js, MongoDB", "urgency": "high"}
            },
            {
                "message": "Design a comprehensive enterprise architecture",
                "context": {"project_type": "enterprise", "complexity": "high"}
            }
        ]
        
        print("Demonstrating strategy selection for different scenarios:")
        
        for i, scenario in enumerate(test_scenarios, 1):
            message = scenario["message"]
            context = scenario["context"]
            
            analysis = classifier.analyze_task(message, context)
            optimization = selector.select_strategy(analysis, context)
            
            print(f"\n{i}. Scenario: '{message}'")
            print(f"   📋 Task Type: {analysis.task_type.value}")
            print(f"   🎯 Selected Strategy: {optimization.strategy.value}")
            print(f"   🧠 Behavioral Steering: {[bs.value for bs in optimization.behavioral_steering]}")
            print(f"   🎚️ Max Tokens: {optimization.max_tokens}")
            print(f"   📈 Enhancement Ratio: {optimization.enhancement_ratio:.2f}x")
            print(f"   🔍 Context Priority: {optimization.context_priority[:3]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Strategy selection demonstration failed: {e}")
        return False

def demonstrate_prompt_crafting():
    """Demonstrate the precision prompt crafting system."""
    print_header("Precision Prompt Crafting")
    
    try:
        from adaptive_prompt_engine import (
            TaskClassificationSystem, PromptStrategySelector, PrecisionPromptCrafter
        )
        
        classifier = TaskClassificationSystem()
        selector = PromptStrategySelector()
        crafter = PrecisionPromptCrafter()
        
        # Test different types of prompts
        test_cases = [
            {
                "message": "Create a login function with error handling",
                "context": {
                    "tech_stack": "Python, FastAPI, JWT",
                    "user_preferences": "Prefer comprehensive solutions",
                    "project_plans": "Building secure web application"
                }
            },
            {
                "message": "Explain how neural networks learn",
                "context": {
                    "user_preferences": "Learning mode, step-by-step explanations",
                    "conversation_summary": "Discussing machine learning concepts"
                }
            },
            {
                "message": "Quick fix for CSS layout issue",
                "context": {
                    "tech_stack": "HTML, CSS, JavaScript",
                    "user_preferences": "Concise solutions",
                    "urgency": "high"
                }
            }
        ]
        
        print("Demonstrating precision prompt crafting:")
        
        for i, test_case in enumerate(test_cases, 1):
            message = test_case["message"]
            context = test_case["context"]
            
            analysis = classifier.analyze_task(message, context)
            optimization = selector.select_strategy(analysis, context)
            enhanced_prompt = crafter.craft_precision_prompt(message, context, optimization, analysis)
            
            print(f"\n{i}. Test Case: '{message}'")
            print_comparison(message, enhanced_prompt, optimization.strategy.value)
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt crafting demonstration failed: {e}")
        return False

def demonstrate_full_appe_system():
    """Demonstrate the full APPE system integration."""
    print_header("Full APPE System Integration")
    
    try:
        from adaptive_prompt_engine import AdaptivePromptEngine
        
        appe = AdaptivePromptEngine()
        
        # Comprehensive test scenario
        user_message = "Help me build a scalable e-commerce platform with microservices"
        context = {
            "tech_stack": "Python, FastAPI, PostgreSQL, Redis, Docker, Kubernetes",
            "project_plans": "Building enterprise e-commerce platform with high availability",
            "user_preferences": "Comprehensive solutions with best practices and security",
            "conversation_summary": "Discussing system architecture and scalability",
            "recent_interactions": [
                {"type": "architecture", "topic": "microservices design"},
                {"type": "technical", "topic": "database optimization"}
            ]
        }
        
        print("Demonstrating full APPE system with comprehensive scenario:")
        print(f"\n📝 User Message: '{user_message}'")
        print(f"🔍 Context: {json.dumps({k: str(v)[:50] + '...' if len(str(v)) > 50 else str(v) for k, v in context.items()}, indent=2)}")
        
        # Generate optimal prompt
        start_time = time.time()
        enhanced_prompt = appe.generate_optimal_prompt(user_message, context)
        processing_time = time.time() - start_time
        
        print(f"\n⚡ Processing Time: {processing_time:.3f} seconds")
        print_comparison(user_message, enhanced_prompt, "adaptive")
        
        # Simulate learning from interaction
        print(f"\n📚 Learning from interaction...")
        appe.learn_from_interaction_outcome(
            user_message, enhanced_prompt, 0.9, 0.85, processing_time
        )
        
        # Get system status
        status = appe.get_system_status()
        print(f"\n📊 System Status:")
        print(f"   Status: {status['status']}")
        print(f"   Prompts Generated: {status['statistics']['prompts_generated']}")
        print(f"   Average Processing Time: {status['statistics']['average_processing_time']:.3f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Full APPE demonstration failed: {e}")
        return False

def demonstrate_prompt_generator_integration():
    """Demonstrate APPE integration with PromptGenerator."""
    print_header("PromptGenerator Integration")
    
    try:
        from prompt_generator import PromptGenerator
        
        generator = PromptGenerator()
        
        user_message = "Create a secure API endpoint for file uploads"
        
        print("Comparing different prompt generation strategies:")
        
        # Test different strategies
        strategies = ["adaptive", "comprehensive", "technical", "minimal"]
        
        for strategy in strategies:
            start_time = time.time()
            
            if strategy == "adaptive":
                enhanced_prompt = generator.generate_enhanced_prompt(
                    user_message, context_type=strategy, use_appe=True
                )
            else:
                enhanced_prompt = generator.generate_enhanced_prompt(
                    user_message, context_type=strategy, use_appe=False
                )
            
            processing_time = time.time() - start_time
            
            print(f"\n🎯 Strategy: {strategy}")
            print(f"   ⚡ Processing Time: {processing_time:.3f}s")
            print(f"   📏 Output Length: {len(enhanced_prompt)} chars")
            print(f"   📈 Enhancement Ratio: {len(enhanced_prompt) / len(user_message):.2f}x")
        
        # Get statistics
        stats = generator.get_stats()
        print(f"\n📊 Generator Statistics:")
        print(f"   APPE Available: {stats.get('appe_available', False)}")
        print(f"   Total Generations: {stats.get('total_generated', 0)}")
        print(f"   Success Rate: {stats.get('success_rate', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ PromptGenerator integration demonstration failed: {e}")
        return False

def demonstrate_learning_system():
    """Demonstrate the success pattern learning system."""
    print_header("Success Pattern Learning System")
    
    try:
        from adaptive_prompt_engine import SuccessPatternLearner, TaskType
        
        learner = SuccessPatternLearner("data/demo_success_patterns.json")
        
        print("Demonstrating learning from interaction outcomes:")
        
        # Simulate multiple interactions with different outcomes
        learning_scenarios = [
            {"task_type": TaskType.CODE_GENERATION, "feedback": 0.9, "quality": 0.85},
            {"task_type": TaskType.DEBUGGING, "feedback": 0.8, "quality": 0.9},
            {"task_type": TaskType.ARCHITECTURE, "feedback": 0.95, "quality": 0.8},
            {"task_type": TaskType.CODE_GENERATION, "feedback": 0.85, "quality": 0.9},
            {"task_type": TaskType.LEARNING, "feedback": 0.9, "quality": 0.85}
        ]
        
        for i, scenario in enumerate(learning_scenarios, 1):
            print(f"\n{i}. Learning from {scenario['task_type'].value} interaction")
            print(f"   👤 User Feedback: {scenario['feedback']:.2f}")
            print(f"   🎯 Response Quality: {scenario['quality']:.2f}")
        
        # Get learning insights
        insights = learner.get_learning_insights()
        
        print(f"\n📈 Learning Insights:")
        print(f"   Total Patterns: {insights['total_patterns']}")
        
        if insights['task_type_performance']:
            print(f"   Task Performance:")
            for task_type, performance in insights['task_type_performance'].items():
                print(f"     {task_type}: {performance['average_effectiveness']:.3f}")
        
        if insights['most_effective_strategies']:
            print(f"   Most Effective Strategies:")
            for strategy, effectiveness in insights['most_effective_strategies'].items():
                print(f"     {strategy}: {effectiveness:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Learning system demonstration failed: {e}")
        return False

def run_full_demonstration():
    """Run the complete APPE demonstration."""
    print_header("Adaptive Prompt Precision Engine (APPE) Demonstration")
    
    print("""
🎯 Welcome to the APPE Demonstration!

The Adaptive Prompt Precision Engine is an intelligent system that:
• Automatically classifies different types of tasks
• Selects optimal prompt strategies for each task type  
• Crafts precision-targeted prompts with behavioral steering
• Learns from interaction outcomes to improve over time
• Integrates seamlessly with existing prompt generation systems

Let's explore each component:
""")
    
    demonstrations = [
        ("Task Classification", demonstrate_task_classification),
        ("Strategy Selection", demonstrate_strategy_selection), 
        ("Prompt Crafting", demonstrate_prompt_crafting),
        ("Full APPE System", demonstrate_full_appe_system),
        ("PromptGenerator Integration", demonstrate_prompt_generator_integration),
        ("Learning System", demonstrate_learning_system)
    ]
    
    results = {}
    
    for demo_name, demo_func in demonstrations:
        try:
            print(f"\n🔄 Running {demo_name} demonstration...")
            results[demo_name] = demo_func()
        except Exception as e:
            print(f"❌ {demo_name} demonstration failed: {e}")
            results[demo_name] = False
    
    # Summary
    print_header("Demonstration Summary")
    
    successful = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"📊 Results: {successful}/{total} demonstrations successful")
    
    for demo_name, result in results.items():
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"   {demo_name:<30} {status}")
    
    if successful == total:
        print(f"""
🎉 All demonstrations completed successfully!

The APPE system is now ready to enhance your prompt generation with:
• Intelligent task classification and strategy selection
• Precision-crafted prompts with behavioral steering  
• Continuous learning from interaction outcomes
• Seamless integration with existing systems

To use APPE in your code:

```python
from adaptive_prompt_engine import AdaptivePromptEngine

appe = AdaptivePromptEngine()
enhanced_prompt = appe.generate_optimal_prompt(user_message, context)
```

Or through the integrated PromptGenerator:

```python  
from prompt_generator import PromptGenerator

generator = PromptGenerator()
enhanced_prompt = generator.generate_enhanced_prompt(
    user_message, context_type="adaptive", use_appe=True
)
```
""")
    else:
        print(f"""
⚠️ Some demonstrations failed. Please check the output above for details.
The APPE system may still be functional for basic use cases.
""")
    
    return successful == total

if __name__ == "__main__":
    success = run_full_demonstration()
    exit(0 if success else 1)
