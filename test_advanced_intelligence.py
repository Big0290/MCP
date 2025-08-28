#!/usr/bin/env python3
"""
Comprehensive Test: Advanced Context Intelligence System
Tests the complete intelligent context enhancement system
"""

import sys
import os
import time
from datetime import datetime
import hashlib

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_advanced_context_intelligence():
    """Test the complete advanced context intelligence system"""
    print("🧠 Testing Complete Advanced Context Intelligence System")
    print("=" * 60)
    
    try:
        # Test 1: Context Learning System
        print("\n🧪 Test 1: Context Learning System")
        print("-" * 30)
        
        from context_learning_system import (
            learn_from_interaction, get_optimal_context_strategy,
            get_learning_insights, get_learning_recommendations
        )
        
        # Test learning from various interactions
        test_interactions = [
            ("How do I deploy this app?", "Enhanced technical response with full context", "technical", "Excellent help!", 10),
            ("What's the next step in our project?", "Enhanced conversation response", "conversation", "Very helpful", 9),
            ("Debug this database query", "Enhanced technical response with optimization tips", "technical", "Solved my problem!", 10),
            ("Tell me about our progress", "Enhanced general response with project status", "general", "Good overview", 8),
            ("Optimize this API endpoint", "Enhanced technical response with performance tips", "technical", "Great optimization advice", 9)
        ]
        
        for prompt, enhanced, context_type, feedback, quality in test_interactions:
            learn_from_interaction(prompt, enhanced, context_type, feedback, quality)
            print(f"✅ Learned from: {prompt[:40]}...")
        
        # Test strategy optimization
        technical_prompt = "How do I optimize this database query for better performance?"
        strategy = get_optimal_context_strategy(technical_prompt, "technical")
        print(f"\n🎯 Optimal strategy for technical query:")
        print(f"   Enhancement level: {strategy['enhancement_level']}")
        print(f"   Cache strategy: {strategy['cache_strategy']}")
        print(f"   Context priority: {strategy['context_priority'][:3]}...")
        
        # Get learning insights
        insights = get_learning_insights()
        print(f"\n📊 Learning insights: {len(insights['context_effectiveness_summary'])} context types analyzed")
        
        # Get recommendations
        recommendations = get_learning_recommendations()
        print(f"💡 Recommendations: {len(recommendations)} suggestions available")
        
        # Test 2: Smart Caching System
        print("\n🧪 Test 2: Smart Caching System")
        print("-" * 30)
        
        from smart_caching_system import (
            put_in_cache, get_from_cache, get_cache_stats, optimize_cache
        )
        
        # Test intelligent caching with different context types
        cache_test_data = [
            ("deploy_app", "Enhanced deployment guide with full context", "technical", 3.2, "Perfect!", 10),
            ("project_status", "Enhanced project overview with progress", "conversation", 2.1, "Very helpful", 9),
            ("debug_query", "Enhanced debugging guide with examples", "technical", 2.8, "Solved it!", 10),
            ("next_steps", "Enhanced roadmap with priorities", "general", 1.9, "Clear direction", 8)
        ]
        
        for key, value, context_type, ratio, feedback, quality in cache_test_data:
            put_in_cache(key, value, context_type, ratio, feedback, quality)
            print(f"💾 Cached: {key} ({context_type}) - {ratio:.1f}x enhancement")
        
        # Test cache retrieval
        print("\n📥 Testing cache retrieval...")
        for key, _, context_type, _, _, _ in cache_test_data:
            retrieved = get_from_cache(key, context_type)
            if retrieved:
                print(f"  ✅ {key}: {retrieved[:30]}...")
            else:
                print(f"  ❌ {key}: Cache miss")
        
        # Test cache miss
        missing = get_from_cache("nonexistent_key")
        print(f"  ❌ Nonexistent key: {missing}")
        
        # Show cache statistics
        cache_stats = get_cache_stats()
        print(f"\n📊 Cache statistics:")
        print(f"   Hits: {cache_stats['total_hits']}, Misses: {cache_stats['total_misses']}")
        print(f"   Hit rate: {cache_stats['cache_hit_rate']:.1%}")
        print(f"   Memory usage: {cache_stats['memory_usage_mb']:.2f}MB")
        print(f"   Context caches: {cache_stats['context_cache_entries']}")
        
        # Test 3: Integrated Learning and Caching
        print("\n🧪 Test 3: Integrated Learning and Caching")
        print("-" * 30)
        
        # Simulate a real-world scenario with learning and caching
        print("🔄 Simulating real-world usage patterns...")
        
        # Multiple similar queries to test pattern learning
        similar_queries = [
            ("How do I deploy the app?", "technical"),
            ("What's the deployment process?", "technical"),
            ("Can you help me deploy?", "technical"),
            ("Deployment instructions please", "technical")
        ]
        
        for query, context_type in similar_queries:
            # Generate enhanced response
            enhanced = f"Enhanced response for: {query}"
            enhancement_ratio = len(enhanced) / len(query)
            
            # Learn from interaction
            learn_from_interaction(query, enhanced, context_type, "Good help", 8)
            
            # Cache the result
            cache_key = hashlib.md5(query.encode()).hexdigest()[:16]
            put_in_cache(cache_key, enhanced, context_type, enhancement_ratio, "Good help", 8)
            
            print(f"  🔄 Processed: {query[:30]}...")
        
        # Test pattern recognition
        print("\n🧠 Testing pattern recognition...")
        
        # Query with similar terms
        test_query = "How do I deploy something?"
        strategy = get_optimal_context_strategy(test_query, "technical")
        print(f"   Query: {test_query}")
        print(f"   Strategy: {strategy['enhancement_level']} enhancement, {strategy['cache_strategy']} caching")
        
        # Test 4: Performance and Optimization
        print("\n🧪 Test 4: Performance and Optimization")
        print("-" * 30)
        
        # Test cache optimization
        print("🔧 Testing cache optimization...")
        optimize_cache()
        
        # Test rapid access patterns
        print("⚡ Testing rapid access patterns...")
        start_time = time.time()
        
        # Access cached items rapidly
        for _ in range(10):
            for key, _, context_type, _, _, _ in cache_test_data:
                get_from_cache(key, context_type)
        
        total_time = time.time() - start_time
        print(f"   ⚡ 40 cache accesses in {total_time:.3f}s ({total_time/40:.6f}s avg)")
        
        # Final statistics
        print("\n🎯 Final System Statistics")
        print("-" * 30)
        
        # Learning system stats
        final_insights = get_learning_insights()
        learning_stats = final_insights['learning_stats']
        print(f"📚 Learning System:")
        print(f"   Total learned: {learning_stats['total_learned']}")
        print(f"   Patterns recognized: {learning_stats['patterns_recognized']}")
        print(f"   Strategies optimized: {learning_stats['strategies_optimized']}")
        
        # Cache system stats
        final_cache_stats = get_cache_stats()
        print(f"💾 Cache System:")
        print(f"   Hit rate: {final_cache_stats['cache_hit_rate']:.1%}")
        print(f"   Average response time: {final_cache_stats['average_response_time']:.6f}s")
        print(f"   Total evictions: {final_cache_stats['total_evictions']}")
        print(f"   Optimization count: {final_cache_stats['optimization_count']}")
        
        # Context effectiveness
        context_summary = final_insights['context_effectiveness_summary']
        print(f"🎯 Context Effectiveness:")
        for context_type, data in context_summary.items():
            print(f"   {context_type}: {data['total_interactions']} interactions, "
                  f"{data['average_enhancement_ratio']:.2f}x enhancement")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def demo_advanced_features():
    """Demonstrate advanced features and capabilities"""
    print("\n🚀 Advanced Features Demo")
    print("=" * 30)
    
    print("""
🧠 Context Learning:
    • Learns from every user interaction
    • Recognizes conversation patterns
    • Optimizes enhancement strategies
    • Adapts to user preferences

💾 Smart Caching:
    • Context-aware cache placement
    • Intelligent eviction policies
    • Performance analytics
    • Automatic optimization

🎯 Adaptive Enhancement:
    • Dynamic context injection
    • Pattern-based optimization
    • User feedback integration
    • Real-time strategy adjustment

📊 Intelligent Analytics:
    • Usage pattern analysis
    • Performance optimization
    • Learning recommendations
    • System health monitoring
    """)

if __name__ == "__main__":
    print("🧠 Advanced Context Intelligence System Test")
    print("=" * 50)
    
    # Run the main test
    success = test_advanced_context_intelligence()
    
    if success:
        print("\n✅ All advanced intelligence tests completed successfully!")
        print("🚀 Your context enhancement system now has advanced AI capabilities!")
        
        # Show advanced features
        demo_advanced_features()
        
        print("\n🎉 Your advanced context intelligence system is ready for production!")
        print("\n🔮 Next Phase: Production Deployment & Monitoring Dashboard")
        
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)
