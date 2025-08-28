#!/usr/bin/env python3
"""
Smart Caching System
Intelligent cache management based on learned patterns and usage analytics
"""

import sys
import os
import time
import hashlib
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import logging
from collections import OrderedDict, defaultdict
import json
import threading

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartCacheEntry:
    """Individual cache entry with metadata and usage tracking"""
    
    def __init__(self, key: str, value: Any, context_type: str = "general"):
        self.key = key
        self.value = value
        self.context_type = context_type
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()
        self.access_count = 0
        self.size_bytes = len(str(value).encode('utf-8'))
        self.enhancement_ratio = 1.0
        self.user_feedback = None
        self.response_quality = None
        
    def access(self):
        """Record an access to this cache entry"""
        self.last_accessed = datetime.now()
        self.access_count += 1
    
    def update_feedback(self, feedback: str, quality: int):
        """Update user feedback and quality rating"""
        self.user_feedback = feedback
        self.response_quality = quality
    
    def get_age(self) -> float:
        """Get age of cache entry in seconds"""
        return (datetime.now() - self.created_at).total_seconds()
    
    def get_access_frequency(self) -> float:
        """Get access frequency (accesses per second)"""
        age = self.get_age()
        return self.access_count / age if age > 0 else 0
    
    def get_value_score(self) -> float:
        """Calculate value score based on usage and feedback"""
        # Base score from access frequency
        frequency_score = min(self.get_access_frequency() * 100, 10.0)
        
        # Quality bonus from user feedback
        quality_bonus = 0
        if self.response_quality is not None:
            quality_bonus = (self.response_quality - 5) * 0.2  # -1 to +1 range
        
        # Enhancement ratio bonus
        enhancement_bonus = min(self.enhancement_ratio - 1, 2.0) * 0.5
        
        return frequency_score + quality_bonus + enhancement_bonus
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert cache entry to dictionary for serialization"""
        return {
            'key': self.key,
            'value': self.value,
            'context_type': self.context_type,
            'created_at': self.created_at.isoformat(),
            'last_accessed': self.last_accessed.isoformat(),
            'access_count': self.access_count,
            'size_bytes': self.size_bytes,
            'enhancement_ratio': self.enhancement_ratio,
            'user_feedback': self.user_feedback,
            'response_quality': self.response_quality
        }

class SmartCachingSystem:
    """
    Intelligent caching system that learns from usage patterns
    
    Features:
    1. Pattern-based cache key generation
    2. Intelligent eviction policies
    3. Usage analytics and optimization
    4. Context-aware caching strategies
    5. Automatic cache optimization
    """
    
    def __init__(self, max_size_mb: int = 100, max_entries: int = 1000):
        self.max_size_mb = max_size_mb
        self.max_entries = max_entries
        self.max_size_bytes = max_size_mb * 1024 * 1024
        
        # Cache storage
        self.cache = OrderedDict()
        self.context_caches = defaultdict(OrderedDict)
        
        # Analytics and learning
        self.cache_stats = {
            'total_hits': 0,
            'total_misses': 0,
            'total_evictions': 0,
            'total_size_bytes': 0,
            'cache_hit_rate': 0.0,
            'average_response_time': 0.0,
            'last_optimization': None
        }
        
        # Learning integration
        self.learning_enabled = True
        self.pattern_weights = defaultdict(float)
        
        # Performance tracking
        self.response_times = []
        self.optimization_history = []
        
        # Thread safety
        self.lock = threading.RLock()
        
        logger.info(f"🚀 Smart caching system initialized (Max: {max_size_mb}MB, {max_entries} entries)")
    
    def get(self, key: str, context_type: str = "general") -> Optional[Any]:
        """
        Get value from cache with intelligent key generation
        
        Args:
            key (str): Cache key
            context_type (str): Type of context for specialized caching
            
        Returns:
            Cached value or None if not found
        """
        start_time = time.time()
        
        with self.lock:
            # Try main cache first
            if key in self.cache:
                entry = self.cache[key]
                entry.access()
                self.cache_stats['total_hits'] += 1
                
                # Move to end (LRU behavior)
                self.cache.move_to_end(key)
                
                # Update response time tracking
                response_time = time.time() - start_time
                self._update_response_time(response_time)
                
                logger.debug(f"✅ Cache hit for key: {key[:20]}...")
                return entry.value
            
            # Try context-specific cache
            if context_type in self.context_caches and key in self.context_caches[context_type]:
                entry = self.context_caches[context_type][key]
                entry.access()
                self.cache_stats['total_hits'] += 1
                
                # Move to end in context cache
                self.context_caches[context_type].move_to_end(key)
                
                # Update response time tracking
                response_time = time.time() - start_time
                self._update_response_time(response_time)
                
                logger.debug(f"✅ Context cache hit for {context_type}: {key[:20]}...")
                return entry.value
            
            # Cache miss
            self.cache_stats['total_misses'] += 1
            self._update_cache_hit_rate()
            
            response_time = time.time() - start_time
            self._update_response_time(response_time)
            
            logger.debug(f"❌ Cache miss for key: {key[:20]}...")
            return None
    
    def put(self, key: str, value: Any, context_type: str = "general", 
            enhancement_ratio: float = 1.0, user_feedback: str = None, 
            response_quality: int = None) -> bool:
        """
        Store value in cache with intelligent placement
        
        Args:
            key (str): Cache key
            value (Any): Value to cache
            context_type (str): Type of context
            enhancement_ratio (float): Enhancement ratio for value scoring
            user_feedback (str): Optional user feedback
            response_quality (int): Optional quality rating (1-10)
            
        Returns:
            bool: True if successfully cached, False otherwise
        """
        with self.lock:
            try:
                # Create cache entry
                entry = SmartCacheEntry(key, value, context_type)
                entry.enhancement_ratio = enhancement_ratio
                if user_feedback:
                    entry.update_feedback(user_feedback, response_quality)
                
                # Check if we need to evict entries
                if self._should_evict(entry):
                    self._evict_entries(entry.size_bytes)
                
                # Store in appropriate cache
                if context_type != "general":
                    # Store in context-specific cache
                    self.context_caches[context_type][key] = entry
                    self.context_caches[context_type].move_to_end(key)
                else:
                    # Store in main cache
                    self.cache[key] = entry
                    self.cache.move_to_end(key)
                
                # Update size tracking
                self.cache_stats['total_size_bytes'] += entry.size_bytes
                
                # Debug logging
                logger.debug(f"Stored entry: {key} in {context_type} cache, total entries: {len(self.cache) + sum(len(cache) for cache in self.context_caches.values())}")
                
                # Learn from this cache operation
                if self.learning_enabled:
                    self._learn_from_cache_operation(key, context_type, enhancement_ratio)
                
                logger.debug(f"💾 Cached {context_type} entry: {key[:20]}... ({entry.size_bytes} bytes)")
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to cache entry: {str(e)}")
                return False
    
    def _should_evict(self, new_entry: SmartCacheEntry) -> bool:
        """Determine if we need to evict entries to make space"""
        # Check entry count limit
        total_entries = len(self.cache) + sum(len(cache) for cache in self.context_caches.values())
        if total_entries >= self.max_entries:
            return True
        
        # Check size limit
        if self.cache_stats['total_size_bytes'] + new_entry.size_bytes > self.max_size_bytes:
            return True
        
        # Don't evict if we have plenty of space
        return False
    
    def _evict_entries(self, required_bytes: int):
        """Evict entries using intelligent eviction policy"""
        evicted_count = 0
        evicted_bytes = 0
        
        # Calculate target eviction size
        target_eviction_bytes = max(required_bytes, self.max_size_bytes * 0.1)  # Evict at least 10%
        
        # Collect all entries for scoring
        all_entries = []
        
        # Add main cache entries
        for key, entry in self.cache.items():
            all_entries.append(('main', key, entry))
        
        # Add context cache entries
        for context_type, cache in self.context_caches.items():
            for key, entry in cache.items():
                all_entries.append((context_type, key, entry))
        
        # Sort by value score (lowest scores first for eviction)
        all_entries.sort(key=lambda x: x[2].get_value_score())
        
        # Evict entries until we have enough space
        for cache_type, key, entry in all_entries:
            if evicted_bytes >= target_eviction_bytes:
                break
            
            # Evict the entry
            if cache_type == 'main':
                del self.cache[key]
            else:
                del self.context_caches[cache_type][key]
            
            evicted_bytes += entry.size_bytes
            evicted_count += 1
            
            # Update stats
            self.cache_stats['total_size_bytes'] -= entry.size_bytes
            self.cache_stats['total_evictions'] += 1
        
        if evicted_count > 0:
            logger.info(f"🧹 Evicted {evicted_count} entries ({evicted_bytes} bytes)")
    
    def _learn_from_cache_operation(self, key: str, context_type: str, enhancement_ratio: float):
        """Learn from cache operations to improve future caching"""
        # Update pattern weights based on enhancement ratio
        pattern_key = f"{context_type}_{enhancement_ratio:.1f}"
        self.pattern_weights[pattern_key] += 0.1
        
        # Normalize weights
        total_weight = sum(self.pattern_weights.values())
        if total_weight > 0:
            for pattern in self.pattern_weights:
                self.pattern_weights[pattern] /= total_weight
    
    def _update_response_time(self, response_time: float):
        """Update response time tracking"""
        self.response_times.append(response_time)
        
        # Keep only recent response times
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
        
        # Update average
        self.cache_stats['average_response_time'] = sum(self.response_times) / len(self.response_times)
    
    def _update_cache_hit_rate(self):
        """Update cache hit rate"""
        total_requests = self.cache_stats['total_hits'] + self.cache_stats['total_misses']
        if total_requests > 0:
            self.cache_stats['cache_hit_rate'] = self.cache_stats['total_hits'] / total_requests
    
    def optimize_cache(self):
        """Optimize cache based on learned patterns and usage analytics"""
        with self.lock:
            start_time = time.time()
            
            logger.info("🔧 Starting cache optimization...")
            
            # Analyze cache performance
            optimization_actions = []
            
            # Check for underutilized context caches
            for context_type, cache in self.context_caches.items():
                if len(cache) < 5:  # Very small context cache
                    optimization_actions.append(f"Consider consolidating {context_type} cache")
            
            # Check for memory pressure
            memory_usage = self.cache_stats['total_size_bytes'] / self.max_size_bytes
            if memory_usage > 0.8:
                optimization_actions.append("High memory usage - consider increasing cache size")
            
            # Check hit rate
            if self.cache_stats['cache_hit_rate'] < 0.5:
                optimization_actions.append("Low hit rate - consider adjusting eviction policy")
            
            # Perform optimization
            if optimization_actions:
                # Aggressive eviction of low-value entries
                self._evict_entries(self.max_size_bytes * 0.2)  # Evict 20%
                
                # Reorganize context caches
                self._reorganize_context_caches()
            
            # Record optimization
            optimization_time = time.time() - start_time
            self.optimization_history.append({
                'timestamp': datetime.now().isoformat(),
                'actions': optimization_actions,
                'duration': optimization_time,
                'cache_size_before': self.cache_stats['total_size_bytes'],
                'cache_size_after': self.cache_stats['total_size_bytes']
            })
            
            self.cache_stats['last_optimization'] = datetime.now().isoformat()
            
            logger.info(f"✅ Cache optimization completed in {optimization_time:.3f}s")
            if optimization_actions:
                logger.info(f"Actions taken: {', '.join(optimization_actions)}")
    
    def _reorganize_context_caches(self):
        """Reorganize context caches for better performance"""
        # Move frequently accessed entries to main cache
        for context_type, cache in self.context_caches.items():
            high_value_entries = []
            
            for key, entry in cache.items():
                if entry.get_value_score() > 5.0:  # High value entries
                    high_value_entries.append((key, entry))
            
            # Move high-value entries to main cache
            for key, entry in high_value_entries:
                if key not in self.cache:
                    self.cache[key] = entry
                    del cache[key]
                    logger.debug(f"🔄 Moved high-value entry to main cache: {key[:20]}...")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        with self.lock:
            # Calculate total entries across all caches
            total_entries = len(self.cache) + sum(len(cache) for cache in self.context_caches.values())
            
            stats = {
                **self.cache_stats,
                'current_entries': total_entries,
                'context_cache_entries': {ctx: len(cache) for ctx, cache in self.context_caches.items()},
                'memory_usage_mb': self.cache_stats['total_size_bytes'] / (1024 * 1024),
                'memory_usage_percent': (self.cache_stats['total_size_bytes'] / self.max_size_bytes) * 100,
                'pattern_weights': dict(self.pattern_weights),
                'optimization_count': len(self.optimization_history)
            }
            
            return stats
    
    def clear_cache(self, context_type: str = None):
        """Clear cache or specific context cache"""
        with self.lock:
            if context_type is None:
                # Clear all caches
                self.cache.clear()
                self.context_caches.clear()
                self.cache_stats['total_size_bytes'] = 0
                logger.info("🧹 All caches cleared")
            else:
                # Clear specific context cache
                if context_type in self.context_caches:
                    cache = self.context_caches[context_type]
                    evicted_bytes = sum(entry.size_bytes for entry in cache.values())
                    cache.clear()
                    self.cache_stats['total_size_bytes'] -= evicted_bytes
                    logger.info(f"🧹 {context_type} cache cleared ({evicted_bytes} bytes freed)")
    
    def export_cache_data(self) -> Dict[str, Any]:
        """Export cache data for analysis"""
        with self.lock:
            export_data = {
                'cache_stats': self.cache_stats,
                'main_cache': {key: entry.to_dict() for key, entry in self.cache.items()},
                'context_caches': {
                    ctx: {key: entry.to_dict() for key, entry in cache.items()}
                    for ctx, cache in self.context_caches.items()
                },
                'pattern_weights': dict(self.pattern_weights),
                'optimization_history': self.optimization_history,
                'export_timestamp': datetime.now().isoformat()
            }
            
            return export_data

# Global instance for easy access
smart_cache = SmartCachingSystem()

def get_from_cache(key: str, context_type: str = "general") -> Optional[Any]:
    """Get value from smart cache"""
    return smart_cache.get(key, context_type)

def put_in_cache(key: str, value: Any, context_type: str = "general", 
                enhancement_ratio: float = 1.0, user_feedback: str = None, 
                response_quality: int = None) -> bool:
    """Store value in smart cache"""
    return smart_cache.put(key, value, context_type, enhancement_ratio, user_feedback, response_quality)

def get_cache_stats() -> Dict[str, Any]:
    """Get smart cache statistics"""
    return smart_cache.get_cache_stats()

def optimize_cache():
    """Optimize smart cache"""
    smart_cache.optimize_cache()

def clear_cache(context_type: str = None):
    """Clear smart cache"""
    smart_cache.clear_cache(context_type)

if __name__ == "__main__":
    print("🧪 Testing Smart Caching System...")
    
    # Test basic caching
    test_data = [
        ("prompt_001", "Enhanced technical response", "technical", 2.5, "Great help!", 9),
        ("prompt_002", "Enhanced conversation response", "conversation", 1.8, "Good", 7),
        ("prompt_003", "Enhanced general response", "general", 2.2, "Helpful", 8)
    ]
    
    for key, value, context_type, ratio, feedback, quality in test_data:
        put_in_cache(key, value, context_type, ratio, feedback, quality)
        print(f"💾 Cached: {key} ({context_type})")
    
    # Test retrieval
    for key, _, context_type, _, _, _ in test_data:
        retrieved = get_from_cache(key, context_type)
        print(f"📥 Retrieved: {key} -> {retrieved[:20]}...")
    
    # Test cache miss
    missing = get_from_cache("nonexistent_key")
    print(f"❌ Cache miss: {missing}")
    
    # Show stats
    stats = get_cache_stats()
    print(f"\n📊 Cache stats: {stats['total_hits']} hits, {stats['total_misses']} misses")
    print(f"💾 Memory usage: {stats['memory_usage_mb']:.2f}MB ({stats['memory_usage_percent']:.1f}%)")
    
    # Test optimization
    optimize_cache()
    
    print("\n✅ Smart caching system test completed!")
