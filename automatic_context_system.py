#!/usr/bin/env python3
"""
Real-time Context Injection System
Automatically enhances prompts in real-time as they're processed
"""

import sys
import os
import time
import threading
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
import logging
from queue import Queue
import json

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealTimeContextInjector:
    """
    Real-time context injection system that automatically enhances prompts
    as they're being processed, providing instant context awareness
    """
    
    def __init__(self, auto_start: bool = True):
        self.auto_start = auto_start
        self.is_running = False
        self.context_queue = Queue()
        self.enhanced_responses = {}
        self.processing_thread = None
        self.context_cache = {}
        self.performance_metrics = {
            'total_processed': 0,
            'average_processing_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'last_processed': None
        }
        self.active_sessions = {}
        
        if auto_start:
            self.start()
    
    def start(self):
        """Start the real-time context injection system"""
        if self.is_running:
            logger.info("Real-time context injector is already running")
            return
            
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        logger.info("🚀 Real-time context injection system started")
    
    def stop(self):
        """Stop the real-time context injection system"""
        if not self.is_running:
            logger.info("Real-time context injector is not running")
            return
            
        self.is_running = False
        if self.processing_thread:
            self.processing_thread.join(timeout=5)
        logger.info("🛑 Real-time context injection system stopped")
    
    def inject_context_real_time(self, prompt_id: str, original_prompt: str, 
                               context_type: str = "general", priority: int = 1) -> str:
        """
        Inject context in real-time for immediate processing
        
        Args:
            prompt_id (str): Unique identifier for the prompt
            original_prompt (str): The original user prompt
            context_type (str): Type of context to inject
            priority (int): Processing priority (1=high, 2=normal, 3=low)
            
        Returns:
            str: Enhanced prompt with real-time context
        """
        start_time = time.time()
        
        try:
            # Check cache first for instant response
            cache_key = f"{hash(original_prompt)}_{context_type}"
            if cache_key in self.context_cache:
                cached_result = self.context_cache[cache_key]
                self.performance_metrics['cache_hits'] += 1
                
                # Update with new prompt ID
                enhanced_prompt = cached_result['enhanced'].replace(
                    "USER REQUEST:", f"PROMPT ID: {prompt_id}\nUSER REQUEST:"
                )
                
                logger.info(f"⚡ Cache hit for prompt {prompt_id}: {len(original_prompt)} -> {len(enhanced_prompt)} chars")
                return enhanced_prompt
            
            self.performance_metrics['cache_misses'] += 1
            
            # Generate context in real-time
            enhanced_context = self._generate_real_time_context(original_prompt, context_type)
            enhanced_prompt = self._build_real_time_prompt(prompt_id, original_prompt, enhanced_context)
            
            # Cache the result for future use
            self.context_cache[cache_key] = {
                'enhanced': enhanced_prompt,
                'timestamp': datetime.now().isoformat(),
                'context_type': context_type
            }
            
            # Update performance metrics
            processing_time = time.time() - start_time
            self._update_performance_metrics(processing_time)
            
            logger.info(f"🚀 Real-time context injected for prompt {prompt_id}: {len(original_prompt)} -> {len(enhanced_prompt)} chars in {processing_time:.3f}s")
            
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"❌ Real-time context injection failed for prompt {prompt_id}: {str(e)}")
            return original_prompt
    
    def _generate_real_time_context(self, prompt: str, context_type: str) -> str:
        """Generate context in real-time for immediate use"""
        try:
            # Import context generation functions
            from local_mcp_server_simple import (
                _generate_conversation_summary,
                _extract_action_history,
                _get_tech_stack_definition,
                _get_project_plans,
                _get_user_preferences,
                _get_agent_metadata
            )
            
            # Get recent interactions for context
            from models_local import get_session_factory, AgentInteraction
            
            with get_session_factory()() as db_session:
                recent_interactions = db_session.query(AgentInteraction).order_by(
                    AgentInteraction.timestamp.desc()
                ).limit(10).all()  # Reduced for real-time performance
            
            # Generate context based on type
            if context_type == "technical":
                context = f"""
TECH STACK: {_get_tech_stack_definition()}
PROJECT PLANS: {_get_project_plans()}
RECENT ACTIONS: {_extract_action_history(recent_interactions)}
                """.strip()
            elif context_type == "conversation":
                context = f"""
CONVERSATION SUMMARY: {_generate_conversation_summary(recent_interactions)}
USER PREFERENCES: {_get_user_preferences()}
AGENT METADATA: {_get_agent_metadata()}
                """.strip()
            else:
                context = f"""
CONVERSATION SUMMARY: {_generate_conversation_summary(recent_interactions)}
ACTION HISTORY: {_extract_action_history(recent_interactions)}
TECH STACK: {_get_tech_stack_definition()}
PROJECT PLANS: {_get_project_plans()}
USER PREFERENCES: {_get_user_preferences()}
AGENT METADATA: {_get_agent_metadata()}
                """.strip()
            
            return context
            
        except Exception as e:
            logger.error(f"Real-time context generation failed: {str(e)}")
            return f"⚠️ Real-time context generation failed: {str(e)}"
    
    def _build_real_time_prompt(self, prompt_id: str, original_prompt: str, enhanced_context: str) -> str:
        """Build real-time enhanced prompt with prompt ID tracking"""
        enhanced_prompt = f"""
=== REAL-TIME ENHANCED PROMPT ===
PROMPT ID: {prompt_id}
TIMESTAMP: {datetime.now().isoformat()}
PROCESSING MODE: Real-time

USER REQUEST: {original_prompt}

=== INJECTED CONTEXT ===
{enhanced_context}

=== REAL-TIME INSTRUCTIONS ===
Please respond to the user's request above, taking into account:
1. The real-time injected context and conversation history
2. The user's current preferences and project status
3. The technical capabilities and constraints
4. Previous actions and decisions made

Provide a comprehensive, context-aware response that builds upon our conversation history.
=== END REAL-TIME ENHANCED PROMPT ===
        """.strip()
        
        return enhanced_prompt
    
    def _update_performance_metrics(self, processing_time: float):
        """Update performance metrics with new processing time"""
        self.performance_metrics['total_processed'] += 1
        self.performance_metrics['last_processed'] = datetime.now().isoformat()
        
        # Update running average
        current_avg = self.performance_metrics['average_processing_time']
        total_processed = self.performance_metrics['total_processed']
        
        self.performance_metrics['average_processing_time'] = (
            (current_avg * (total_processed - 1) + processing_time) / total_processed
        )
    
    def _processing_loop(self):
        """Background processing loop for queued context requests"""
        while self.is_running:
            try:
                # Process queued requests
                if not self.context_queue.empty():
                    request = self.context_queue.get(timeout=1)
                    self._process_queued_request(request)
                
                # Clean up old cache entries
                self._cleanup_cache()
                
                time.sleep(0.1)  # Small delay to prevent CPU spinning
                
            except Exception as e:
                logger.error(f"Error in processing loop: {str(e)}")
                time.sleep(1)  # Longer delay on error
    
    def _process_queued_request(self, request: Dict[str, Any]):
        """Process a queued context request"""
        try:
            prompt_id = request['prompt_id']
            original_prompt = request['original_prompt']
            context_type = request['context_type']
            
            # Process the request
            enhanced_prompt = self.inject_context_real_time(prompt_id, original_prompt, context_type)
            
            # Store the result
            self.enhanced_responses[prompt_id] = {
                'enhanced_prompt': enhanced_prompt,
                'processed_at': datetime.now().isoformat(),
                'context_type': context_type
            }
            
        except Exception as e:
            logger.error(f"Failed to process queued request: {str(e)}")
    
    def _cleanup_cache(self):
        """Clean up old cache entries"""
        current_time = datetime.now()
        keys_to_remove = []
        
        for key, value in self.context_cache.items():
            cache_time = datetime.fromisoformat(value['timestamp'])
            if current_time - cache_time > timedelta(hours=1):  # Keep cache for 1 hour
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.context_cache[key]
        
        if keys_to_remove:
            logger.info(f"🧹 Cleaned up {len(keys_to_remove)} old cache entries")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.performance_metrics,
            'cache_size': len(self.context_cache),
            'queue_size': self.context_queue.qsize(),
            'active_sessions': len(self.active_sessions),
            'cache_hit_rate': (
                self.performance_metrics['cache_hits'] / 
                (self.performance_metrics['cache_hits'] + self.performance_metrics['cache_misses'])
                if (self.performance_metrics['cache_hits'] + self.performance_metrics['cache_misses']) > 0 
                else 0
            )
        }
    
    def clear_cache(self):
        """Clear the context cache"""
        self.context_cache.clear()
        logger.info("Context cache cleared")
    
    def get_enhanced_response(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """Get enhanced response for a specific prompt ID"""
        return self.enhanced_responses.get(prompt_id)

# Global instance for easy access
real_time_injector = RealTimeContextInjector()

def inject_context_real_time(prompt_id: str, prompt: str, context_type: str = "general") -> str:
    """
    Convenience function to inject context in real-time
    
    Usage:
        enhanced = inject_context_real_time("prompt_123", "How do I deploy this?")
        enhanced = inject_context_real_time("prompt_124", "What's next?", "technical")
    """
    return real_time_injector.inject_context_real_time(prompt_id, prompt, context_type)

def get_real_time_metrics() -> Dict[str, Any]:
    """Get real-time context injection metrics"""
    return real_time_injector.get_performance_metrics()

def start_real_time_system():
    """Start the real-time context injection system"""
    real_time_injector.start()

def stop_real_time_system():
    """Stop the real-time context injection system"""
    real_time_injector.stop()

if __name__ == "__main__":
    print("🧪 Testing Real-Time Context Injection System...")
    
    # Start the system
    start_real_time_system()
    
    # Test real-time injection
    test_prompts = [
        ("prompt_001", "What should I work on next?", "general"),
        ("prompt_002", "How do I optimize this code?", "technical"),
        ("prompt_003", "What's our conversation about?", "conversation")
    ]
    
    for prompt_id, prompt, context_type in test_prompts:
        enhanced = inject_context_real_time(prompt_id, prompt, context_type)
        print(f"\n📝 {prompt_id}: {prompt}")
        print(f"🚀 Enhanced length: {len(enhanced)} characters")
        print(f"✨ Contains context: {'INJECTED CONTEXT' in enhanced}")
    
    # Show metrics
    metrics = get_real_time_metrics()
    print(f"\n📊 Performance metrics: {metrics}")
    
    # Stop the system
    stop_real_time_system()
    
    print("\n✅ Real-time context injection system test completed!")
