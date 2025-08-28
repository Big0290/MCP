#!/usr/bin/env python3
"""
Test performance tracking to verify it's working
"""

import sys
import os
import time

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_performance_tracking():
    """Test that performance tracking is working"""
    print("🧪 Testing Performance Tracking...")
    
    # Import the context manager
    from context_manager import enhance_prompt_seamlessly, get_performance_summary
    
    print("📝 Processing prompts to generate performance data...")
    
    # Process several prompts to generate performance data
    test_prompts = [
        ("How do I deploy this application?", "technical"),
        ("What's our project status?", "conversation"),
        ("Can you help me optimize this code?", "technical"),
        ("What are the next steps?", "general"),
        ("How do I debug this issue?", "technical")
    ]
    
    for i, (prompt, context_type) in enumerate(test_prompts, 1):
        start_time = time.time()
        enhanced = enhance_prompt_seamlessly(prompt, context_type)
        processing_time = time.time() - start_time
        
        print(f"  ✅ Prompt {i}: {len(prompt)} -> {len(enhanced)} chars in {processing_time:.6f}s")
    
    print("\n📊 Performance Summary:")
    performance = get_performance_summary()
    
    for key, value in performance.items():
        if key == 'system_performance':
            print(f"  {key}:")
            for system, stats in value.items():
                print(f"    {system}: {stats}")
        else:
            print(f"  {key}: {value}")
    
    print("\n🎯 Performance tracking is working!")

if __name__ == "__main__":
    test_performance_tracking()
