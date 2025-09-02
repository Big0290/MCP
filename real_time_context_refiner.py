#!/usr/bin/env python3
"""
🔄 Real-time Context Refiner - Phase 2 Implementation
Continuously refines context during conversations for optimal AI assistance.
"""

import json
import sqlite3
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
import re

class ContextRefinementTrigger(Enum):
    """Triggers for context refinement"""
    USER_FOLLOW_UP = "user_follow_up"
    CONTEXT_GAP_DETECTED = "context_gap_detected"
    PERFORMANCE_DROP = "performance_drop"
    USER_FEEDBACK = "user_feedback"
    CONVERSATION_SHIFT = "conversation_shift"

class ContextGapType(Enum):
    """Types of context gaps"""
    MISSING_TECHNICAL_CONTEXT = "missing_technical_context"
    MISSING_PROJECT_CONTEXT = "missing_project_context"
    MISSING_CONVERSATION_CONTEXT = "missing_conversation_context"
    MISSING_USER_PREFERENCES = "missing_user_preferences"
    INSUFFICIENT_DETAIL = "insufficient_detail"

@dataclass
class ContextRefinementEvent:
    """A context refinement event"""
    event_id: str
    trigger: ContextRefinementTrigger
    original_context: Dict[str, Any]
    refined_context: Dict[str, Any]
    gaps_detected: List[ContextGapType]
    refinement_reason: str
    user_message: str
    timestamp: datetime = None
    session_id: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

@dataclass
class ContextGap:
    """A detected context gap"""
    gap_type: ContextGapType
    description: str
    severity: str  # "low", "medium", "high"
    suggested_context: List[str]
    confidence: float

class ContextGapDetector:
    """Detects gaps in current context that need filling"""

    def __init__(self):
        self.gap_patterns = {
            ContextGapType.MISSING_TECHNICAL_CONTEXT: {
                "keywords": ["how to", "implement", "code", "function", "class", "database", "api"],
                "severity": "high",
                "suggested_context": ["tech_stack", "best_practices", "common_issues"]
            },
            ContextGapType.MISSING_PROJECT_CONTEXT: {
                "keywords": ["project", "structure", "files", "modules", "architecture"],
                "severity": "medium",
                "suggested_context": ["project_structure", "project_overview", "best_practices"]
            },
            ContextGapType.MISSING_CONVERSATION_CONTEXT: {
                "keywords": ["continue", "previous", "earlier", "yesterday", "before", "what were we"],
                "severity": "medium",
                "suggested_context": ["conversation_summary", "action_history", "recent_topics"]
            },
            ContextGapType.MISSING_USER_PREFERENCES: {
                "keywords": ["prefer", "like", "want", "need", "style", "approach"],
                "severity": "low",
                "suggested_context": ["user_preferences", "workflow_preferences"]
            },
            ContextGapType.INSUFFICIENT_DETAIL: {
                "keywords": ["explain", "detail", "why", "how does", "what is"],
                "severity": "medium",
                "suggested_context": ["best_practices", "common_issues", "detailed_context"]
            }
        }

    def detect_context_gaps(self, user_message: str, current_context: Dict[str, Any]) -> List[ContextGap]:
        """Detect gaps in the current context based on user message"""
        gaps = []
        message_lower = user_message.lower()

        for gap_type, pattern_info in self.gap_patterns.items():
            # Check if keywords are present
            keyword_matches = sum(1 for keyword in pattern_info["keywords"] if keyword in message_lower)
            
            if keyword_matches > 0:
                # Check if suggested context is missing
                missing_context = []
                for suggested in pattern_info["suggested_context"]:
                    if suggested not in current_context or not current_context[suggested]:
                        missing_context.append(suggested)

                if missing_context:
                    # Calculate confidence based on keyword matches
                    confidence = min(keyword_matches / len(pattern_info["keywords"]), 1.0)
                    
                    gap = ContextGap(
                        gap_type=gap_type,
                        description=f"Missing {', '.join(missing_context)} context for {gap_type.value}",
                        severity=pattern_info["severity"],
                        suggested_context=missing_context,
                        confidence=confidence
                    )
                    gaps.append(gap)

        return gaps

    def analyze_context_completeness(self, current_context: Dict[str, Any], user_message: str) -> Dict[str, Any]:
        """Analyze how complete the current context is for the user's message"""
        gaps = self.detect_context_gaps(user_message, current_context)
        
        # Calculate completeness score
        total_suggested = sum(len(gap.suggested_context) for gap in gaps)
        missing_suggested = sum(len(gap.suggested_context) for gap in gaps)
        
        if total_suggested == 0:
            completeness_score = 1.0
        else:
            completeness_score = 1.0 - (missing_suggested / total_suggested)

        return {
            "completeness_score": completeness_score,
            "gaps_detected": len(gaps),
            "severity_distribution": {
                "high": len([g for g in gaps if g.severity == "high"]),
                "medium": len([g for g in gaps if g.severity == "medium"]),
                "low": len([g for g in gaps if g.severity == "low"])
            },
            "gaps": gaps
        }

class ContextExpansionEngine:
    """Engine for expanding context to fill detected gaps"""

    def __init__(self):
        self.expansion_strategies = {
            ContextGapType.MISSING_TECHNICAL_CONTEXT: self._expand_technical_context,
            ContextGapType.MISSING_PROJECT_CONTEXT: self._expand_project_context,
            ContextGapType.MISSING_CONVERSATION_CONTEXT: self._expand_conversation_context,
            ContextGapType.MISSING_USER_PREFERENCES: self._expand_user_preferences,
            ContextGapType.INSUFFICIENT_DETAIL: self._expand_detail_context
        }

    def expand_context(self, current_context: Dict[str, Any], gaps: List[ContextGap], 
                      available_context: Dict[str, Any]) -> Dict[str, Any]:
        """Expand context to fill detected gaps"""
        expanded_context = current_context.copy()

        for gap in gaps:
            if gap.gap_type in self.expansion_strategies:
                expansion_func = self.expansion_strategies[gap.gap_type]
                expanded_context = expansion_func(expanded_context, gap, available_context)

        return expanded_context

    def _expand_technical_context(self, context: Dict[str, Any], gap: ContextGap, 
                                available_context: Dict[str, Any]) -> Dict[str, Any]:
        """Expand technical context"""
        for suggested in gap.suggested_context:
            if suggested in available_context and suggested not in context:
                context[suggested] = available_context[suggested]
        
        return context

    def _expand_project_context(self, context: Dict[str, Any], gap: ContextGap, 
                              available_context: Dict[str, Any]) -> Dict[str, Any]:
        """Expand project context"""
        for suggested in gap.suggested_context:
            if suggested in available_context and suggested not in context:
                context[suggested] = available_context[suggested]
        
        return context

    def _expand_conversation_context(self, context: Dict[str, Any], gap: ContextGap, 
                                   available_context: Dict[str, Any]) -> Dict[str, Any]:
        """Expand conversation context"""
        for suggested in gap.suggested_context:
            if suggested in available_context and suggested not in context:
                context[suggested] = available_context[suggested]
        
        return context

    def _expand_user_preferences(self, context: Dict[str, Any], gap: ContextGap, 
                               available_context: Dict[str, Any]) -> Dict[str, Any]:
        """Expand user preferences context"""
        for suggested in gap.suggested_context:
            if suggested in available_context and suggested not in context:
                context[suggested] = available_context[suggested]
        
        return context

    def _expand_detail_context(self, context: Dict[str, Any], gap: ContextGap, 
                             available_context: Dict[str, Any]) -> Dict[str, Any]:
        """Expand detail context"""
        for suggested in gap.suggested_context:
            if suggested in available_context and suggested not in context:
                context[suggested] = available_context[suggested]
        
        return context

class ConversationFlowAnalyzer:
    """Analyzes conversation flow to detect shifts and context needs"""

    def __init__(self):
        self.topic_keywords = {
            "technical": ["code", "implement", "function", "class", "database", "api", "algorithm"],
            "project": ["project", "structure", "files", "modules", "architecture", "design"],
            "debugging": ["error", "bug", "issue", "problem", "fix", "debug", "troubleshoot"],
            "learning": ["explain", "how", "what", "why", "concept", "principle", "theory"],
            "general": ["hello", "hi", "thanks", "good", "bad", "help"]
        }

    def detect_conversation_shift(self, current_message: str, conversation_history: List[Dict[str, Any]], 
                                window_size: int = 5) -> Optional[str]:
        """Detect if there's a significant shift in conversation topic"""
        if len(conversation_history) < window_size:
            return None

        # Get recent messages
        recent_messages = conversation_history[-window_size:]
        
        # Analyze topic distribution in recent messages
        recent_topics = self._analyze_topic_distribution([msg.get("user_message", "") for msg in recent_messages])
        current_topic = self._analyze_topic_distribution([current_message])
        
        # Check for significant topic shift
        for topic, current_score in current_topic.items():
            if topic in recent_topics:
                recent_score = recent_topics[topic]
                if abs(current_score - recent_score) > 0.3:  # Significant shift threshold
                    return f"shift_to_{topic}"
        
        return None

    def _analyze_topic_distribution(self, messages: List[str]) -> Dict[str, float]:
        """Analyze topic distribution in messages"""
        topic_scores = {topic: 0.0 for topic in self.topic_keywords.keys()}
        
        for message in messages:
            message_lower = message.lower()
            for topic, keywords in self.topic_keywords.items():
                for keyword in keywords:
                    if keyword in message_lower:
                        topic_scores[topic] += 1.0
        
        # Normalize scores
        total_matches = sum(topic_scores.values())
        if total_matches > 0:
            topic_scores = {topic: score / total_matches for topic, score in topic_scores.items()}
        
        return topic_scores

    def get_context_requirements_for_shift(self, shift_type: str) -> List[str]:
        """Get context requirements for detected conversation shift"""
        shift_context_mapping = {
            "shift_to_technical": ["tech_stack", "best_practices", "common_issues"],
            "shift_to_project": ["project_structure", "project_overview", "best_practices"],
            "shift_to_debugging": ["tech_stack", "common_issues", "best_practices"],
            "shift_to_learning": ["conversation_summary", "best_practices", "project_context"],
            "shift_to_general": ["user_preferences", "conversation_summary"]
        }
        
        return shift_context_mapping.get(shift_type, ["user_preferences"])

class ContextRefinementDatabase:
    """Database for storing context refinement events"""

    def __init__(self, db_path: str = "data/context_refinement.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the refinement database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Context refinement events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context_refinement_events (
                event_id TEXT PRIMARY KEY,
                trigger TEXT NOT NULL,
                original_context TEXT NOT NULL,
                refined_context TEXT NOT NULL,
                gaps_detected TEXT NOT NULL,
                refinement_reason TEXT NOT NULL,
                user_message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                session_id TEXT
            )
        """)

        # Context gaps table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context_gaps (
                gap_id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                gap_type TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                suggested_context TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def store_refinement_event(self, event: ContextRefinementEvent):
        """Store a context refinement event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO context_refinement_events 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.event_id,
            event.trigger.value,
            json.dumps(event.original_context),
            json.dumps(event.refined_context),
            json.dumps([gap.gap_type.value for gap in event.gaps_detected]),
            event.refinement_reason,
            event.user_message,
            event.timestamp.isoformat(),
            event.session_id
        ))

        # Store individual gaps
        for gap in event.gaps_detected:
            gap_id = f"gap_{event.event_id}_{gap.gap_type.value}"
            cursor.execute("""
                INSERT INTO context_gaps 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                gap_id,
                event.event_id,
                gap.gap_type.value,
                gap.description,
                gap.severity,
                json.dumps(gap.suggested_context),
                gap.confidence,
                event.timestamp.isoformat()
            ))

        conn.commit()
        conn.close()

class RealTimeContextRefiner:
    """Main class for real-time context refinement"""

    def __init__(self, db_path: str = "data/context_refinement.db"):
        self.refinement_db = ContextRefinementDatabase(db_path)
        self.gap_detector = ContextGapDetector()
        self.expansion_engine = ContextExpansionEngine()
        self.flow_analyzer = ConversationFlowAnalyzer()

    def refine_context_mid_conversation(self, user_message: str, current_context: Dict[str, Any], 
                                     available_context: Dict[str, Any], 
                                     conversation_history: List[Dict[str, Any]] = None,
                                     session_id: str = "default") -> Tuple[Dict[str, Any], List[ContextGap]]:
        """Refine context during conversation based on user message and flow"""
        
        # Detect context gaps
        gaps = self.gap_detector.detect_context_gaps(user_message, current_context)
        
        # Detect conversation shift
        conversation_shift = None
        if conversation_history:
            conversation_shift = self.flow_analyzer.detect_conversation_shift(user_message, conversation_history)
            if conversation_shift:
                # Add context requirements for the shift
                shift_context_requirements = self.flow_analyzer.get_context_requirements_for_shift(conversation_shift)
                for requirement in shift_context_requirements:
                    if requirement not in current_context and requirement in available_context:
                        gaps.append(ContextGap(
                            gap_type=ContextGapType.MISSING_PROJECT_CONTEXT,  # Default type
                            description=f"Context required for conversation shift to {conversation_shift}",
                            severity="medium",
                            suggested_context=[requirement],
                            confidence=0.8
                        ))

        # Expand context to fill gaps
        refined_context = self.expansion_engine.expand_context(current_context, gaps, available_context)
        
        # Create refinement event
        refinement_event = ContextRefinementEvent(
            event_id=f"refine_{session_id}_{int(datetime.now(timezone.utc).timestamp())}",
            trigger=ContextRefinementTrigger.CONTEXT_GAP_DETECTED if gaps else ContextRefinementTrigger.USER_FOLLOW_UP,
            original_context=current_context,
            refined_context=refined_context,
            gaps_detected=gaps,
            refinement_reason=f"Context refinement triggered by {len(gaps)} gaps detected",
            user_message=user_message,
            session_id=session_id
        )

        # Store the refinement event
        self.refinement_db.store_refinement_event(refinement_event)
        
        return refined_context, gaps

    def detect_context_gaps(self, user_message: str, current_context: Dict[str, Any]) -> List[ContextGap]:
        """Detect gaps in current context"""
        return self.gap_detector.detect_context_gaps(user_message, current_context)

    def analyze_context_completeness(self, current_context: Dict[str, Any], user_message: str) -> Dict[str, Any]:
        """Analyze context completeness"""
        return self.gap_detector.analyze_context_completeness(current_context, user_message)

    def suggest_context_expansion(self, detected_gaps: List[ContextGap]) -> Dict[str, Any]:
        """Suggest context expansion based on detected gaps"""
        suggestions = {
            "high_priority": [],
            "medium_priority": [],
            "low_priority": []
        }
        
        for gap in detected_gaps:
            priority = gap.severity
            suggestions[f"{priority}_priority"].append({
                "gap_type": gap.gap_type.value,
                "description": gap.description,
                "suggested_context": gap.suggested_context,
                "confidence": gap.confidence
            })
        
        return suggestions

    def get_refinement_insights(self, session_id: str = None, limit: int = 50) -> Dict[str, Any]:
        """Get insights about context refinement patterns"""
        # This would query the refinement database for patterns
        # For now, return a summary
        return {
            "total_refinements": 0,  # Would be calculated from database
            "common_gaps": [],       # Would be calculated from database
            "refinement_triggers": {}, # Would be calculated from database
            "effectiveness_score": 0.0  # Would be calculated from database
        }

# Example usage and testing
if __name__ == "__main__":
    refiner = RealTimeContextRefiner()
    
    # Test context gap detection
    test_context = {
        "user_preferences": "Technical, concise responses",
        "tech_stack": "Python, SQLite, MCP"
    }
    
    gaps = refiner.detect_context_gaps(
        "How do I implement a database connection?",
        test_context
    )
    
    print(f"🔍 Detected Gaps: {len(gaps)}")
    for gap in gaps:
        print(f"  - {gap.gap_type.value}: {gap.description}")
    
    # Test context completeness analysis
    completeness = refiner.analyze_context_completeness(
        test_context,
        "How do I implement a database connection?"
    )
    
    print(f"📊 Context Completeness: {completeness['completeness_score']:.2f}")
    
    # Test context refinement
    available_context = {
        "best_practices": "Use connection pooling, implement error handling",
        "common_issues": "Connection timeouts, memory leaks",
        "project_structure": "Multiple modules with clear separation"
    }
    
    refined_context, new_gaps = refiner.refine_context_mid_conversation(
        "How do I implement a database connection?",
        test_context,
        available_context
    )
    
    print(f"🔄 Refined Context: {list(refined_context.keys())}")
    print(f"🔍 New Gaps: {len(new_gaps)}")
    
    # Test conversation shift detection
    conversation_history = [
        {"user_message": "What is the project structure?"},
        {"user_message": "How do I implement a database connection?"}
    ]
    
    shift = refiner.flow_analyzer.detect_conversation_shift(
        "Can you explain the algorithm complexity?",
        conversation_history
    )
    
    if shift:
        print(f"🔄 Conversation Shift Detected: {shift}")
        requirements = refiner.flow_analyzer.get_context_requirements_for_shift(shift)
        print(f"📋 Context Requirements: {requirements}")
