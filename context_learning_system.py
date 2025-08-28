#!/usr/bin/env python3
"""
Advanced Context Learning System
Learns from user preferences and conversation patterns for intelligent context enhancement
"""

import sys
import os
import json
import time
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import logging
from collections import defaultdict, Counter
import hashlib
import pickle

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextLearningSystem:
    """
    Advanced context learning system that learns from user interactions
    
    Features:
    1. User preference learning
    2. Conversation pattern recognition
    3. Context effectiveness tracking
    4. Adaptive enhancement strategies
    5. Smart caching based on learned patterns
    """
    
    def __init__(self, learning_enabled: bool = True, data_file: str = "context_learning_data.pkl"):
        self.learning_enabled = learning_enabled
        self.data_file = data_file
        self.learning_data = {
            'user_preferences': {},
            'conversation_patterns': {},
            'context_effectiveness': {},
            'enhancement_strategies': {},
            'learning_history': [],
            'last_updated': datetime.now().isoformat()
        }
        self.pattern_memory = defaultdict(list)
        self.preference_weights = defaultdict(float)
        self.learning_stats = {
            'total_learned': 0,
            'preferences_updated': 0,
            'patterns_recognized': 0,
            'strategies_optimized': 0,
            'last_learning': None
        }
        
        # Load existing learning data
        self._load_learning_data()
        
        # Initialize learning patterns
        self._initialize_learning_patterns()
    
    def _load_learning_data(self):
        """Load existing learning data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'rb') as f:
                    loaded_data = pickle.load(f)
                    self.learning_data.update(loaded_data)
                    logger.info(f"✅ Loaded learning data from {self.data_file}")
            else:
                logger.info(f"📝 No existing learning data found, starting fresh")
        except Exception as e:
            logger.warning(f"⚠️ Could not load learning data: {e}")
    
    def _save_learning_data(self):
        """Save learning data to file"""
        try:
            self.learning_data['last_updated'] = datetime.now().isoformat()
            with open(self.data_file, 'wb') as f:
                pickle.dump(self.learning_data, f)
            logger.info(f"💾 Learning data saved to {self.data_file}")
        except Exception as e:
            logger.error(f"❌ Could not save learning data: {e}")
    
    def _initialize_learning_patterns(self):
        """Initialize learning patterns and strategies"""
        # Initialize default enhancement strategies
        self.learning_data['enhancement_strategies'] = {
            'technical_queries': {
                'context_priority': ['tech_stack', 'project_plans', 'recent_actions'],
                'enhancement_level': 'high',
                'cache_strategy': 'aggressive'
            },
            'conversation_queries': {
                'context_priority': ['conversation_summary', 'user_preferences', 'agent_metadata'],
                'enhancement_level': 'medium',
                'cache_strategy': 'moderate'
            },
            'general_queries': {
                'context_priority': ['conversation_summary', 'action_history', 'tech_stack'],
                'enhancement_level': 'balanced',
                'cache_strategy': 'standard'
            }
        }
        
        # Initialize default user preferences
        self.learning_data['user_preferences'] = {
            'context_detail_level': 'comprehensive',
            'preferred_context_types': ['technical', 'conversation'],
            'response_style': 'detailed',
            'cache_preference': 'aggressive'
        }
    
    def learn_from_interaction(self, prompt: str, enhanced_prompt: str, 
                             context_type: str, user_feedback: Optional[str] = None,
                             response_quality: Optional[int] = None):
        """
        Learn from a user interaction to improve future context enhancement
        
        Args:
            prompt (str): Original user prompt
            enhanced_prompt (str): Enhanced prompt with context
            context_type (str): Type of context used
            user_feedback (str): Optional user feedback
            response_quality (int): Optional quality rating (1-10)
        """
        if not self.learning_enabled:
            return
        
        try:
            interaction_id = hashlib.md5(f"{prompt}_{context_type}_{time.time()}".encode()).hexdigest()
            
            # Extract learning insights
            insights = self._extract_learning_insights(prompt, enhanced_prompt, context_type)
            
            # Update learning data
            self._update_learning_data(insights, user_feedback, response_quality)
            
            # Learn conversation patterns
            self._learn_conversation_patterns(prompt, context_type)
            
            # Optimize enhancement strategies
            self._optimize_enhancement_strategies(insights)
            
            # Update learning statistics
            self.learning_stats['total_learned'] += 1
            self.learning_stats['last_learning'] = datetime.now().isoformat()
            
            # Save learning data periodically
            if self.learning_stats['total_learned'] % 10 == 0:
                self._save_learning_data()
            
            logger.info(f"🧠 Learned from interaction {interaction_id[:8]}: {insights['enhancement_ratio']:.2f}x enhancement")
            
        except Exception as e:
            logger.error(f"❌ Learning failed: {str(e)}")
    
    def _extract_learning_insights(self, prompt: str, enhanced_prompt: str, context_type: str) -> Dict[str, Any]:
        """Extract learning insights from an interaction"""
        original_length = len(prompt)
        enhanced_length = len(enhanced_prompt)
        enhancement_ratio = enhanced_length / original_length if original_length > 0 else 1.0
        
        # Analyze prompt characteristics
        prompt_analysis = {
            'length': original_length,
            'word_count': len(prompt.split()),
            'contains_technical_terms': any(term in prompt.lower() for term in ['code', 'deploy', 'optimize', 'debug', 'api']),
            'contains_questions': '?' in prompt,
            'urgency_indicators': any(indicator in prompt.lower() for indicator in ['urgent', 'asap', 'quick', 'help'])
        }
        
        # Analyze enhancement effectiveness
        enhancement_analysis = {
            'enhancement_ratio': enhancement_ratio,
            'context_injection_size': enhanced_length - original_length,
            'context_type_effectiveness': context_type,
            'enhancement_efficiency': enhancement_ratio / (enhanced_length - original_length) if enhanced_length > original_length else 0
        }
        
        return {
            'prompt_analysis': prompt_analysis,
            'enhancement_analysis': enhancement_analysis,
            'timestamp': datetime.now().isoformat(),
            'interaction_type': 'context_enhancement'
        }
    
    def _update_learning_data(self, insights: Dict[str, Any], user_feedback: str, response_quality: int):
        """Update learning data with new insights"""
        # Update context effectiveness tracking
        context_type = insights['enhancement_analysis']['context_type_effectiveness']
        if context_type not in self.learning_data['context_effectiveness']:
            self.learning_data['context_effectiveness'][context_type] = []
        
        self.learning_data['context_effectiveness'][context_type].append({
            'enhancement_ratio': insights['enhancement_analysis']['enhancement_ratio'],
            'efficiency': insights['enhancement_analysis']['enhancement_efficiency'],
            'timestamp': insights['timestamp'],
            'user_feedback': user_feedback,
            'response_quality': response_quality
        })
        
        # Keep only recent data (last 100 interactions per type)
        if len(self.learning_data['context_effectiveness'][context_type]) > 100:
            self.learning_data['context_effectiveness'][context_type] = \
                self.learning_data['context_effectiveness'][context_type][-100:]
        
        # Update learning history
        self.learning_data['learning_history'].append(insights)
        if len(self.learning_data['learning_history']) > 1000:
            self.learning_data['learning_history'] = self.learning_data['learning_history'][-1000:]
        
        self.learning_stats['preferences_updated'] += 1
    
    def _learn_conversation_patterns(self, prompt: str, context_type: str):
        """Learn conversation patterns for better context prediction"""
        # Extract key terms and patterns
        words = prompt.lower().split()
        key_terms = [word for word in words if len(word) > 3 and word not in ['what', 'when', 'where', 'which', 'about', 'with', 'from']]
        
        # Update pattern memory
        for term in key_terms:
            self.pattern_memory[term].append({
                'context_type': context_type,
                'timestamp': datetime.now(),
                'prompt_length': len(prompt)
            })
        
        # Keep pattern memory manageable
        for term in self.pattern_memory:
            if len(self.pattern_memory[term]) > 50:
                self.pattern_memory[term] = self.pattern_memory[term][-50:]
        
        self.learning_stats['patterns_recognized'] += 1
    
    def _optimize_enhancement_strategies(self, insights: Dict[str, Any]):
        """Optimize enhancement strategies based on learned insights"""
        context_type = insights['enhancement_analysis']['context_type_effectiveness']
        enhancement_ratio = insights['enhancement_analysis']['enhancement_ratio']
        
        # Adjust strategy based on effectiveness
        if context_type in self.learning_data['enhancement_strategies']:
            strategy = self.learning_data['enhancement_strategies'][context_type]
            
            # Optimize enhancement level based on effectiveness
            if enhancement_ratio < 2.0:  # Low enhancement
                strategy['enhancement_level'] = 'high'
            elif enhancement_ratio > 5.0:  # Very high enhancement
                strategy['enhancement_level'] = 'balanced'
            
            # Optimize cache strategy based on usage patterns
            if self._get_context_type_usage_frequency(context_type) > 10:
                strategy['cache_strategy'] = 'aggressive'
            elif self._get_context_type_usage_frequency(context_type) < 3:
                strategy['cache_strategy'] = 'conservative'
        
        self.learning_stats['strategies_optimized'] += 1
    
    def _get_context_type_usage_frequency(self, context_type: str) -> int:
        """Get usage frequency for a specific context type"""
        if context_type in self.learning_data['context_effectiveness']:
            return len(self.learning_data['context_effectiveness'][context_type])
        return 0
    
    def get_optimal_context_strategy(self, prompt: str, context_type: str = "general") -> Dict[str, Any]:
        """
        Get optimal context enhancement strategy based on learned patterns
        
        Args:
            prompt (str): User prompt
            context_type (str): Requested context type
            
        Returns:
            Dict: Optimal enhancement strategy
        """
        try:
            # Get base strategy for context type
            base_strategy = self.learning_data['enhancement_strategies'].get(
                context_type, 
                self.learning_data['enhancement_strategies']['general_queries']
            ).copy()
            
            # Apply learned optimizations
            optimized_strategy = self._apply_learned_optimizations(prompt, base_strategy)
            
            # Adjust based on user preferences
            user_prefs = self.learning_data['user_preferences']
            if user_prefs.get('context_detail_level') == 'minimal':
                optimized_strategy['enhancement_level'] = 'low'
            elif user_prefs.get('context_detail_level') == 'comprehensive':
                optimized_strategy['enhancement_level'] = 'high'
            
            return optimized_strategy
            
        except Exception as e:
            logger.error(f"Strategy optimization failed: {str(e)}")
            return self.learning_data['enhancement_strategies']['general_queries']
    
    def _apply_learned_optimizations(self, prompt: str, base_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learned optimizations to base strategy"""
        optimized = base_strategy.copy()
        
        # Analyze prompt for optimization opportunities
        prompt_lower = prompt.lower()
        
        # Technical term detection
        technical_terms = ['code', 'deploy', 'optimize', 'debug', 'api', 'database', 'server']
        if any(term in prompt_lower for term in technical_terms):
            optimized['context_priority'].insert(0, 'tech_stack')
            optimized['enhancement_level'] = 'high'
        
        # Urgency detection
        urgency_terms = ['urgent', 'asap', 'quick', 'help', 'error', 'broken']
        if any(term in prompt_lower for term in urgency_terms):
            optimized['cache_strategy'] = 'aggressive'
            optimized['context_priority'].insert(0, 'recent_actions')
        
        # Question detection
        if '?' in prompt:
            optimized['context_priority'].insert(0, 'conversation_summary')
        
        return optimized
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from the learning system"""
        insights = {
            'learning_stats': self.learning_stats,
            'context_effectiveness_summary': {},
            'pattern_insights': {},
            'strategy_optimizations': {}
        }
        
        # Analyze context effectiveness
        for context_type, data in self.learning_data['context_effectiveness'].items():
            if data:
                ratios = [item['enhancement_ratio'] for item in data]
                efficiencies = [item['efficiency'] for item in data if item['efficiency'] > 0]
                
                insights['context_effectiveness_summary'][context_type] = {
                    'total_interactions': len(data),
                    'average_enhancement_ratio': sum(ratios) / len(ratios) if ratios else 0,
                    'average_efficiency': sum(efficiencies) / len(efficiencies) if efficiencies else 0,
                    'most_recent': data[-1] if data else None
                }
        
        # Analyze pattern insights
        for term, patterns in self.pattern_memory.items():
            if len(patterns) >= 3:  # Only show terms with significant usage
                context_types = [p['context_type'] for p in patterns]
                context_counter = Counter(context_types)
                
                insights['pattern_insights'][term] = {
                    'usage_count': len(patterns),
                    'preferred_context': context_counter.most_common(1)[0][0] if context_counter else 'unknown',
                    'context_distribution': dict(context_counter),
                    'last_used': patterns[-1]['timestamp'].isoformat() if patterns else None
                }
        
        # Strategy optimization insights
        insights['strategy_optimizations'] = {
            'total_strategies': len(self.learning_data['enhancement_strategies']),
            'optimization_count': self.learning_stats['strategies_optimized'],
            'current_strategies': self.learning_data['enhancement_strategies']
        }
        
        return insights
    
    def update_user_preferences(self, preferences: Dict[str, Any]):
        """Update user preferences based on feedback"""
        try:
            self.learning_data['user_preferences'].update(preferences)
            self.learning_data['last_updated'] = datetime.now().isoformat()
            self._save_learning_data()
            logger.info("✅ User preferences updated")
        except Exception as e:
            logger.error(f"❌ Failed to update user preferences: {str(e)}")
    
    def get_learning_recommendations(self) -> List[str]:
        """Get recommendations for improving context enhancement"""
        recommendations = []
        
        # Analyze context effectiveness for recommendations
        for context_type, data in self.learning_data['context_effectiveness'].items():
            if data and len(data) >= 5:
                recent_data = data[-5:]  # Last 5 interactions
                avg_ratio = sum(item['enhancement_ratio'] for item in recent_data) / len(recent_data)
                
                if avg_ratio < 2.0:
                    recommendations.append(f"Consider increasing context detail for {context_type} queries")
                elif avg_ratio > 6.0:
                    recommendations.append(f"Consider reducing context detail for {context_type} queries")
        
        # Pattern-based recommendations
        for term, patterns in self.pattern_memory.items():
            if len(patterns) >= 5:
                context_types = [p['context_type'] for p in patterns]
                most_common = Counter(context_types).most_common(1)[0]
                
                if most_common[1] >= 3:
                    recommendations.append(f"Term '{term}' strongly associated with {most_common[0]} context")
        
        return recommendations[:5]  # Return top 5 recommendations

# Global instance for easy access
context_learning_system = ContextLearningSystem()

def learn_from_interaction(prompt: str, enhanced_prompt: str, context_type: str, 
                          user_feedback: str = None, response_quality: int = None):
    """Convenience function to learn from interactions"""
    return context_learning_system.learn_from_interaction(
        prompt, enhanced_prompt, context_type, user_feedback, response_quality
    )

def get_optimal_context_strategy(prompt: str, context_type: str = "general") -> Dict[str, Any]:
    """Get optimal context enhancement strategy"""
    return context_learning_system.get_optimal_context_strategy(prompt, context_type)

def get_learning_insights() -> Dict[str, Any]:
    """Get insights from the learning system"""
    return context_learning_system.get_learning_insights()

def get_learning_recommendations() -> List[str]:
    """Get recommendations for improving context enhancement"""
    return context_learning_system.get_learning_recommendations()

def update_user_preferences(preferences: Dict[str, Any]):
    """Update user preferences"""
    context_learning_system.update_user_preferences(preferences)

if __name__ == "__main__":
    print("🧪 Testing Advanced Context Learning System...")
    
    # Test learning from interactions
    test_interactions = [
        ("How do I deploy this app?", "Enhanced version...", "technical", "Great help!", 9),
        ("What's the next step?", "Enhanced version...", "conversation", "Good", 7),
        ("Debug this code error", "Enhanced version...", "technical", "Solved my problem!", 10),
        ("Tell me about our project", "Enhanced version...", "general", "Informative", 8)
    ]
    
    for prompt, enhanced, context_type, feedback, quality in test_interactions:
        learn_from_interaction(prompt, enhanced, context_type, feedback, quality)
        print(f"✅ Learned from: {prompt[:30]}...")
    
    # Test strategy optimization
    test_prompt = "How do I optimize this database query?"
    strategy = get_optimal_context_strategy(test_prompt, "technical")
    print(f"\n🎯 Optimal strategy for technical query: {strategy}")
    
    # Get learning insights
    insights = get_learning_insights()
    print(f"\n📊 Learning insights: {len(insights['context_effectiveness_summary'])} context types analyzed")
    
    # Get recommendations
    recommendations = get_learning_recommendations()
    print(f"\n💡 Recommendations: {len(recommendations)} suggestions available")
    
    print("\n✅ Advanced context learning system test completed!")
