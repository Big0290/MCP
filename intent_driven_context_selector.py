#!/usr/bin/env python3
"""
🚀 Intent-Driven Context Selector - Phase 1 Implementation
Eliminates irrelevant context to improve prompt quality and AI response relevance.
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class IntentType(Enum):
    """Types of user intents"""
    TECHNICAL = "technical"
    PROJECT_ANALYSIS = "project_analysis"
    CONVERSATION_CONTINUITY = "conversation_continuity"
    CODE_GENERATION = "code_generation"
    DEBUGGING = "debugging"
    LEARNING = "learning"
    GENERAL = "general"

@dataclass
class IntentAnalysis:
    """Result of intent analysis"""
    primary_intent: IntentType
    confidence: float
    secondary_intents: List[IntentType]
    keywords: List[str]
    complexity: str  # "low", "medium", "high"
    context_requirements: List[str]

class IntentClassifier:
    """Classifies user messages to determine intent and context needs"""
    
    def __init__(self):
        self.intent_patterns = {
            IntentType.TECHNICAL: [
                r'\b(code|implement|fix|error|bug|database|api|function|class|method)\b',
                r'\b(performance|optimization|algorithm|data structure)\b',
                r'\b(debug|test|deploy|build|compile)\b'
            ],
            IntentType.PROJECT_ANALYSIS: [
                r'\b(project|structure|files|architecture|design)\b',
                r'\b(organize|refactor|restructure|modularize)\b',
                r'\b(folder|directory|module|package)\b'
            ],
            IntentType.CONVERSATION_CONTINUITY: [
                r'\b(continue|previous|earlier|yesterday|before|continue|resume)\b',
                r'\b(what were we|where did we|how far)\b',
                r'\b(next step|continue with|keep going)\b',
                r'\b(test.*see.*have|check.*have|verify.*have)\b',
                r'\b(action history|conversation summary|context sections)\b',
                r'\b(missing|don.*t have|seem.*don.*t)\b'
            ],
            IntentType.CODE_GENERATION: [
                r'\b(create|write|generate|build|make)\b',
                r'\b(script|program|application|tool)\b',
                r'\b(example|sample|template|boilerplate)\b'
            ],
            IntentType.DEBUGGING: [
                r'\b(debug|troubleshoot|error|issue|problem|fix)\b',
                r'\b(not working|broken|failed|crash)\b',
                r'\b(log|trace|stack|exception)\b'
            ],
            IntentType.LEARNING: [
                r'\b(learn|understand|explain|how|what is|why)\b',
                r'\b(concept|principle|theory|approach)\b',
                r'\b(tutorial|guide|documentation|example)\b'
            ],
            IntentType.GENERAL: [
                r'\b(test|check|verify|see|have|show)\b',
                r'\b(general|basic|simple|basic)\b'
            ]
        }
        
        self.complexity_indicators = {
            "low": [r'\b(simple|basic|quick|easy|straightforward)\b'],
            "high": [r'\b(complex|advanced|detailed|comprehensive|thorough)\b']
        }
    
    def classify_intent(self, user_message: str) -> IntentAnalysis:
        """Analyze user message to determine intent and context needs"""
        message_lower = user_message.lower()
        
        # Score each intent type
        intent_scores = {}
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            matched_keywords = []
            for pattern in patterns:
                matches = re.findall(pattern, message_lower)
                if matches:
                    score += len(matches) * 2
                    matched_keywords.extend(matches)
            if score > 0:
                intent_scores[intent_type] = (score, matched_keywords)
        
        # Determine primary intent
        if intent_scores:
            primary_intent = max(intent_scores.keys(), key=lambda x: intent_scores[x][0])
            confidence = min(intent_scores[primary_intent][0] / 10.0, 1.0)
            keywords = intent_scores[primary_intent][1]
        else:
            primary_intent = IntentType.GENERAL
            confidence = 0.5
            keywords = []
        
        # Get secondary intents
        secondary_intents = [
            intent for intent, (score, _) in intent_scores.items() 
            if intent != primary_intent and score > 2
        ]
        
        # Determine complexity
        complexity = self._analyze_complexity(message_lower)
        
        # Determine context requirements
        context_requirements = self._get_context_requirements(primary_intent, complexity)
        
        return IntentAnalysis(
            primary_intent=primary_intent,
            confidence=confidence,
            secondary_intents=secondary_intents,
            keywords=keywords,
            complexity=complexity,
            context_requirements=context_requirements
        )
    
    def _analyze_complexity(self, message: str) -> str:
        """Analyze message complexity"""
        for complexity, patterns in self.complexity_indicators.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    return complexity
        return "medium"
    
    def _get_context_requirements(self, intent: IntentType, complexity: str) -> List[str]:
        """Get required context sections for the intent"""
        requirements = {
            IntentType.TECHNICAL: ["tech_stack", "best_practices", "common_issues"],
            IntentType.PROJECT_ANALYSIS: ["project_structure", "project_overview", "best_practices"],
            IntentType.CONVERSATION_CONTINUITY: ["conversation_summary", "action_history", "recent_topics"],
            IntentType.CODE_GENERATION: ["tech_stack", "project_structure", "best_practices"],
            IntentType.DEBUGGING: ["tech_stack", "common_issues", "best_practices"],
            IntentType.LEARNING: ["conversation_summary", "best_practices", "project_context"],
            IntentType.GENERAL: ["user_preferences", "conversation_summary", "action_history"]
        }
        
        base_requirements = requirements.get(intent, ["user_preferences"])
        
        # Add complexity-based requirements
        if complexity == "high":
            base_requirements.extend(["project_overview", "detailed_context"])
        elif complexity == "low":
            base_requirements = base_requirements[:2]  # Keep only essential
        
        return base_requirements

class ContextMapper:
    """Maps intents to relevant context sections"""
    
    def __init__(self):
        self.context_mapping = {
            "tech_stack": "⚙️ TECH",
            "project_structure": "🏗️ PROJECT",
            "project_overview": "📊 PROJECT OVERVIEW",
            "conversation_summary": "💬 CONTEXT",
            "action_history": "📝 RECENT",
            "best_practices": "✅ BEST PRACTICES",
            "common_issues": "⚠️ COMMON ISSUES",
            "user_preferences": "👤 PREFERENCES",
            "agent_metadata": "🤖 AGENT",
            "detailed_context": "🔍 DETAILED CONTEXT"
        }
    
    def map_intent_to_context(self, intent_analysis: IntentAnalysis, available_context: Dict) -> Dict[str, Any]:
        """Select only context sections relevant to the detected intent"""
        relevant_context = {}
        
        for requirement in intent_analysis.context_requirements:
            if requirement in available_context:
                relevant_context[requirement] = available_context[requirement]
        
        # Always include core context
        core_sections = ["user_preferences", "agent_metadata"]
        for section in core_sections:
            if section in available_context:
                relevant_context[section] = available_context[section]
        
        return relevant_context
    
    def get_context_priority(self, intent_analysis: IntentAnalysis, context_sections: List[str]) -> List[str]:
        """Return context sections in order of relevance to detected intent"""
        priority_order = []
        
        # Add required context first
        for requirement in intent_analysis.context_requirements:
            if requirement in context_sections:
                priority_order.append(requirement)
        
        # Add remaining context
        for section in context_sections:
            if section not in priority_order:
                priority_order.append(section)
        
        return priority_order

class IntentDrivenContextSelector:
    """Main class for intent-driven context selection"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.context_mapper = ContextMapper()
    
    def select_relevant_context(self, user_message: str, available_context: Dict) -> Tuple[Dict, IntentAnalysis]:
        """Select only context relevant to the user's intent"""
        # Analyze user intent
        intent_analysis = self.intent_classifier.classify_intent(user_message)
        
        # Map intent to relevant context
        relevant_context = self.context_mapper.map_intent_to_context(intent_analysis, available_context)
        
        return relevant_context, intent_analysis
    
    def get_context_priority(self, intent_analysis: IntentAnalysis, context_sections: List[str]) -> List[str]:
        """Get priority order for context sections"""
        return self.context_mapper.get_context_priority(intent_analysis, context_sections)

# Example usage and testing
if __name__ == "__main__":
    selector = IntentDrivenContextSelector()
    
    # Test cases
    test_messages = [
        "How do I implement a database connection?",
        "What were we working on yesterday?",
        "Can you explain the project structure?",
        "Create a simple test script",
        "Debug this error in my code"
    ]
    
    for message in test_messages:
        print(f"\n🔍 Testing: {message}")
        # Simulate available context
        mock_context = {
            "tech_stack": "Python, SQLite, MCP",
            "project_structure": "Multiple modules and packages",
            "conversation_summary": "Previous work on optimization",
            "user_preferences": "Technical, concise responses"
        }
        
        relevant_context, intent_analysis = selector.select_relevant_context(message, mock_context)
        print(f"🎯 Intent: {intent_analysis.primary_intent.value} (confidence: {intent_analysis.confidence:.2f})")
        print(f"📋 Context Requirements: {intent_analysis.context_requirements}")
        print(f"🔧 Selected Context: {list(relevant_context.keys())}")
