#!/usr/bin/env python3
"""
🚀 Enhanced Context Intelligence - Phase 1 Implementation
Scores and filters context relevance to eliminate clutter and improve prompt quality.
"""

import re
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ContextRelevanceScore:
    """Score for context section relevance"""
    section_name: str
    relevance_score: float
    inclusion_reason: str
    priority: int
    should_include: bool

class ContextRelevanceScorer:
    """Scores how relevant each context section is to the current message"""
    
    def __init__(self):
        self.relevance_threshold = 0.6
        self.section_weights = {
            "user_preferences": 1.0,      # Always relevant
            "agent_metadata": 0.8,        # Usually relevant
            "tech_stack": 0.9,            # High relevance for technical questions
            "conversation_summary": 0.85,  # High relevance - essential for continuity
            "action_history": 0.8,        # High relevance - essential for continuity
            "project_structure": 0.8,     # High relevance for project questions
            "best_practices": 0.8,        # High relevance for technical questions
            "common_issues": 0.7,         # Medium relevance
            "workflow_preferences": 0.5    # Lower relevance
        }
        
        self.keyword_patterns = {
            "tech_stack": [
                r'\b(python|sqlite|mcp|sqlalchemy|database|api|function|class)\b',
                r'\b(implement|code|develop|build|create)\b'
            ],
            "project_structure": [
                r'\b(project|structure|files|modules|packages|organization)\b',
                r'\b(architecture|design|layout|folder|directory)\b'
            ],
            "action_history": [
                r'\b(action|step|implemented|created|built|developed)\b',
                r'\b(working on|building|testing|deploying|optimizing)\b',
                r'\b(phase|stage|milestone|progress|status)\b'
            ],
            "conversation_summary": [
                r'\b(continue|previous|earlier|yesterday|before|resume)\b',
                r'\b(what were we|where did we|how far|next step)\b',
                r'\b(goal|objective|target|aim|purpose)\b',
                r'\b(working on|implementing|building|developing)\b'
            ],
            "best_practices": [
                r'\b(best practice|pattern|approach|methodology|standard)\b',
                r'\b(how to|recommend|suggest|improve|optimize)\b'
            ],
            "common_issues": [
                r'\b(error|bug|issue|problem|troubleshoot|debug)\b',
                r'\b(fix|resolve|solve|workaround)\b'
            ]
        }
    
    def score_context_relevance(self, user_message: str, available_context: Dict) -> Dict[str, ContextRelevanceScore]:
        """Score how relevant each context section is to the current message"""
        message_lower = user_message.lower()
        scores = {}
        
        for section_name, context_data in available_context.items():
            # Get base weight for this section
            base_weight = self.section_weights.get(section_name, 0.5)
            
            # Calculate keyword relevance
            keyword_score = self._calculate_keyword_relevance(message_lower, section_name)
            
            # Calculate content relevance
            content_score = self._calculate_content_relevance(message_lower, context_data)
            
            # Calculate recency relevance
            recency_score = self._calculate_recency_relevance(context_data)
            
            # Combine scores
            final_score = (base_weight * 0.4 + keyword_score * 0.4 + content_score * 0.15 + recency_score * 0.05)
            
            # Determine inclusion reason
            inclusion_reason = self._get_inclusion_reason(section_name, final_score, base_weight)
            
            # Determine priority
            priority = self._calculate_priority(section_name, final_score)
            
            # Determine if should include
            should_include = final_score >= self.relevance_threshold
            
            scores[section_name] = ContextRelevanceScore(
                section_name=section_name,
                relevance_score=final_score,
                inclusion_reason=inclusion_reason,
                priority=priority,
                should_include=should_include
            )
        
        return scores
    
    def _calculate_keyword_relevance(self, message: str, section_name: str) -> float:
        """Calculate relevance based on keyword matching"""
        if section_name not in self.keyword_patterns:
            return 0.5
        
        patterns = self.keyword_patterns[section_name]
        total_matches = 0
        
        for pattern in patterns:
            matches = re.findall(pattern, message)
            total_matches += len(matches)
        
        # Normalize score (0-1)
        return min(total_matches / 3.0, 1.0)
    
    def _calculate_content_relevance(self, message: str, context_data: Any) -> float:
        """Calculate relevance based on content analysis"""
        if not context_data or context_data == "not available":
            return 0.0
        
        # Simple content relevance based on data quality
        if isinstance(context_data, str):
            if len(context_data) < 10:
                return 0.3  # Very short content
            elif len(context_data) < 100:
                return 0.7  # Medium content
            else:
                return 1.0  # Substantial content
        elif isinstance(context_data, dict):
            return 0.9  # Structured data
        elif isinstance(context_data, list):
            return 0.8  # List data
        
        return 0.5
    
    def _calculate_recency_relevance(self, context_data: Any) -> float:
        """Calculate relevance based on data recency"""
        # For now, assume all context is recent
        # In a real implementation, you'd check timestamps
        return 0.8
    
    def _get_inclusion_reason(self, section_name: str, score: float, base_weight: float) -> str:
        """Get human-readable reason for inclusion/exclusion"""
        if score >= self.relevance_threshold:
            if base_weight >= 0.9:
                return "Essential context"
            elif score >= 0.8:
                return "Highly relevant"
            else:
                return "Relevant to user's question"
        else:
            if base_weight >= 0.9:
                return "Essential but low relevance - including anyway"
            else:
                return "Not relevant enough - excluding"
    
    def _calculate_priority(self, section_name: str, score: float) -> int:
        """Calculate priority order for context sections"""
        # Higher score = lower priority number (1 = highest priority)
        if score >= 0.9:
            return 1
        elif score >= 0.8:
            return 2
        elif score >= 0.7:
            return 3
        elif score >= 0.6:
            return 4
        else:
            return 5

class ContextFilter:
    """Filters context based on relevance scores"""
    
    def __init__(self, relevance_threshold: float = 0.6):
        self.relevance_threshold = relevance_threshold
    
    def filter_context_by_relevance(self, context: Dict, scores: Dict[str, ContextRelevanceScore]) -> Dict[str, Any]:
        """Filter context to only include relevant sections"""
        filtered_context = {}
        
        # Sort sections by priority
        sorted_sections = sorted(scores.items(), key=lambda x: x[1].priority)
        
        for section_name, score_info in sorted_sections:
            if score_info.should_include:
                filtered_context[section_name] = context[section_name]
        
        return filtered_context
    
    def get_context_summary(self, scores: Dict[str, ContextRelevanceScore]) -> str:
        """Generate a summary of what context was included/excluded and why"""
        included = []
        excluded = []
        
        for section_name, score_info in scores.items():
            if score_info.should_include:
                included.append(f"{section_name} ({score_info.inclusion_reason})")
            else:
                excluded.append(f"{section_name} ({score_info.inclusion_reason})")
        
        summary = f"📋 Context Selection Summary:\n"
        summary += f"✅ Included ({len(included)}): {', '.join(included)}\n"
        if excluded:
            summary += f"❌ Excluded ({len(excluded)}): {', '.join(excluded)}\n"
        
        return summary

class EnhancedContextIntelligence:
    """Main class for enhanced context intelligence"""
    
    def __init__(self, relevance_threshold: float = 0.6):
        self.scorer = ContextRelevanceScorer()
        self.filter = ContextFilter(relevance_threshold)
    
    def process_context(self, user_message: str, available_context: Dict) -> Tuple[Dict, Dict[str, ContextRelevanceScore], str]:
        """Process context to select only relevant sections"""
        # Score context relevance
        relevance_scores = self.scorer.score_context_relevance(user_message, available_context)
        
        # Filter context based on scores
        filtered_context = self.filter.filter_context_by_relevance(available_context, relevance_scores)
        
        # Generate summary
        summary = self.filter.get_context_summary(relevance_scores)
        
        return filtered_context, relevance_scores, summary
    
    def get_optimization_stats(self, original_context: Dict, filtered_context: Dict) -> Dict[str, Any]:
        """Get statistics about context optimization"""
        original_size = sum(len(str(v)) for v in original_context.values())
        filtered_size = sum(len(str(v)) for v in filtered_context.values())
        
        reduction = (1 - filtered_size / max(original_size, 1)) * 100
        
        return {
            "original_sections": len(original_context),
            "filtered_sections": len(filtered_context),
            "original_size": original_size,
            "filtered_size": filtered_size,
            "reduction_percentage": reduction,
            "efficiency_gain": original_size / max(filtered_size, 1)
        }

# Example usage and testing
if __name__ == "__main__":
    intelligence = EnhancedContextIntelligence()
    
    # Test context
    test_context = {
        "user_preferences": "Use SQLite, Python, MCP | Concise, technical responses",
        "tech_stack": "Python 3.x, SQLite database, MCP protocol, SQLAlchemy ORM",
        "project_structure": "Multiple modules: prompt_generator, context_manager, enhanced_mcp_tools",
        "conversation_summary": "Working on prompt optimization system",
        "action_history": "Recent actions: implemented intent classification, created context filtering",
        "best_practices": "Follow Python PEP8, use type hints, implement error handling",
        "workflow_preferences": "Comprehensive logging, structured data models"
    }
    
    # Test messages
    test_messages = [
        "How do I implement a database connection?",
        "What were we working on yesterday?",
        "Can you explain the project structure?",
        "Create a simple test script"
    ]
    
    for message in test_messages:
        print(f"\n🔍 Testing: {message}")
        filtered_context, scores, summary = intelligence.process_context(message, test_context)
        stats = intelligence.get_optimization_stats(test_context, filtered_context)
        
        print(f"📊 Optimization Stats:")
        print(f"   Sections: {stats['original_sections']} → {stats['filtered_sections']}")
        print(f"   Size: {stats['original_size']:,} → {stats['filtered_size']:,} chars")
        print(f"   Reduction: {stats['reduction_percentage']:.1f}%")
        print(f"   Efficiency Gain: {stats['efficiency_gain']:.1f}x")
        
        print(f"\n{summary}")
        print(f"🔧 Selected Context: {list(filtered_context.keys())}")
