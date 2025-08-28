#!/usr/bin/env python3
"""
Populate systems with real data and show dashboard
"""

import sys
import os
import time

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def populate_systems():
    """Populate all systems with real data"""
    print("🚀 Populating systems with real data...")
    
    # Populate context manager
    from context_manager import enhance_prompt_seamlessly
    print("📝 Generating context enhancement data...")
    
    test_prompts = [
        "How do I deploy this application?",
        "What's the next step in our project?",
        "How can I optimize this code?",
        "What's our current progress?",
        "Can you help me debug this issue?"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        enhanced = enhance_prompt_seamlessly(prompt, "technical" if i % 2 == 0 else "conversation")
        print(f"  ✅ Prompt {i}: {len(prompt)} -> {len(enhanced)} chars")
        time.sleep(0.1)  # Small delay
    
    # Populate cache system
    from smart_caching_system import put_in_cache
    print("💾 Populating cache system...")
    
    cache_data = [
        ("deploy_app", "Enhanced deployment guide with full context", "technical", 3.2, "Perfect!", 10),
        ("project_status", "Enhanced project overview with progress", "conversation", 2.1, "Very helpful", 9),
        ("optimize_code", "Enhanced optimization guide with examples", "technical", 2.8, "Solved my problem!", 10),
        ("debug_help", "Enhanced debugging guide with solutions", "technical", 2.5, "Great help!", 9),
        ("next_steps", "Enhanced roadmap with priorities", "general", 1.9, "Clear direction", 8)
    ]
    
    for key, value, context_type, ratio, feedback, quality in cache_data:
        put_in_cache(key, value, context_type, ratio, feedback, quality)
        print(f"  ✅ Cached: {key} ({context_type}) - {ratio:.1f}x enhancement")
        time.sleep(0.1)
    
    # Populate learning system
    from context_learning_system import learn_from_interaction
    print("🧠 Populating learning system...")
    
    learning_data = [
        ("How do I deploy this?", "Enhanced deployment guide", "technical", "Excellent help!", 10),
        ("What's the next step?", "Enhanced roadmap", "conversation", "Very helpful", 9),
        ("Debug this code error", "Enhanced debugging guide", "technical", "Solved my problem!", 10),
        ("Tell me about our project", "Enhanced project overview", "general", "Informative", 8),
        ("Optimize this API endpoint", "Enhanced optimization guide", "technical", "Great advice", 9)
    ]
    
    for prompt, enhanced, context_type, feedback, quality in learning_data:
        learn_from_interaction(prompt, enhanced, context_type, feedback, quality)
        print(f"  ✅ Learned from: {prompt[:30]}...")
        time.sleep(0.1)
    
    print("✅ All systems populated with real data!")
    print()

def show_system_status():
    """Show current system status"""
    print("📊 CURRENT SYSTEM STATUS")
    print("=" * 50)
    
    # Context Manager Status
    try:
        from context_manager import get_performance_summary
        context_stats = get_performance_summary()
        print("🔧 Context Manager:")
        print(f"   Active Systems: {context_stats.get('active_systems', 0)}")
        print(f"   Total Processed: {context_stats.get('total_prompts_processed', 0)}")
        print(f"   Avg Processing Time: {context_stats.get('average_processing_time', 0):.6f}s")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Cache System Status
    try:
        from smart_caching_system import get_cache_stats
        cache_stats = get_cache_stats()
        print("\n💾 Cache System:")
        print(f"   Total Entries: {cache_stats.get('current_entries', 0)}")
        print(f"   Hit Rate: {cache_stats.get('cache_hit_rate', 0):.1%}")
        print(f"   Memory Usage: {cache_stats.get('memory_usage_mb', 0):.2f}MB")
        print(f"   Context Caches: {cache_stats.get('context_cache_entries', {})}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Learning System Status
    try:
        from context_learning_system import get_learning_insights
        learning_stats = get_learning_insights()
        stats = learning_stats.get('learning_stats', {})
        print("\n🧠 Learning System:")
        print(f"   Total Learned: {stats.get('total_learned', 0)}")
        print(f"   Patterns Recognized: {stats.get('patterns_recognized', 0)}")
        print(f"   Strategies Optimized: {stats.get('strategies_optimized', 0)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()

def start_dashboard():
    """Start the monitoring dashboard"""
    print("🚀 Starting monitoring dashboard with real data...")
    print("💡 Press Ctrl+C to exit the dashboard")
    print()
    
    try:
        from simple_dashboard import start_simple_dashboard
        start_simple_dashboard(refresh_rate=2.0)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Dashboard failed: {e}")

if __name__ == "__main__":
    print("🧠 Intelligent Context Enhancement System - Data Population & Dashboard")
    print("=" * 70)
    
    # Step 1: Populate systems with real data
    populate_systems()
    
    # Step 2: Show current status
    show_system_status()
    
    # Step 3: Start dashboard
    start_dashboard()
