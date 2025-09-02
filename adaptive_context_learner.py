#!/usr/bin/env python3
"""
🧠 Adaptive Context Learning System - Phase 2 Implementation
Learns from user interactions to continuously improve context selection effectiveness.
"""

import json
import sqlite3
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
import hashlib

class LearningEventType(Enum):
    """Types of learning events"""
    CONTEXT_SELECTION = "context_selection"
    USER_FEEDBACK = "user_feedback"
    RESPONSE_QUALITY = "response_quality"
    THRESHOLD_ADJUSTMENT = "threshold_adjustment"

@dataclass
class ContextLearningEvent:
    """A learning event for context selection improvement"""
    event_id: str
    event_type: LearningEventType
    user_message: str
    selected_context: Dict[str, Any]
    excluded_context: List[str]
    user_satisfaction: Optional[float] = None
    ai_response_quality: Optional[float] = None
    learning_insights: Optional[Dict] = None
    timestamp: datetime = None
    session_id: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        if self.event_id is None:
            self.event_id = self._generate_event_id()

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        content = f"{self.event_type.value}_{self.user_message}_{self.timestamp.isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

@dataclass
class UserContextProfile:
    """User's context selection preferences and patterns"""
    user_id: str
    preferred_context_sections: List[str]
    preferred_context_depth: str  # "concise", "detailed", "comprehensive"
    relevance_threshold: float
    learning_patterns: Dict[str, Any]
    last_updated: datetime
    success_rate: float
    total_interactions: int

class ContextLearningDatabase:
    """Database for storing learning events and user profiles"""

    def __init__(self, db_path: str = "data/context_learning.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the learning database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Learning events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context_learning_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                user_message TEXT NOT NULL,
                selected_context TEXT NOT NULL,
                excluded_context TEXT NOT NULL,
                user_satisfaction REAL,
                ai_response_quality REAL,
                learning_insights TEXT,
                timestamp TEXT NOT NULL,
                session_id TEXT
            )
        """)

        # User context profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_context_profiles (
                user_id TEXT PRIMARY KEY,
                preferred_context_sections TEXT NOT NULL,
                preferred_context_depth TEXT NOT NULL,
                relevance_threshold REAL NOT NULL,
                learning_patterns TEXT NOT NULL,
                last_updated TEXT NOT NULL,
                success_rate REAL NOT NULL,
                total_interactions INTEGER NOT NULL
            )
        """)

        # Learning patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                success_rate REAL NOT NULL,
                usage_count INTEGER NOT NULL,
                last_used TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def store_learning_event(self, event: ContextLearningEvent):
        """Store a learning event in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO context_learning_events 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.event_id,
            event.event_type.value,
            event.user_message,
            json.dumps(event.selected_context),
            json.dumps(event.excluded_context),
            event.user_satisfaction,
            event.ai_response_quality,
            json.dumps(event.learning_insights) if event.learning_insights else None,
            event.timestamp.isoformat(),
            event.session_id
        ))

        conn.commit()
        conn.close()

    def get_user_profile(self, user_id: str) -> Optional[UserContextProfile]:
        """Get user's context profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM user_context_profiles WHERE user_id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return UserContextProfile(
                user_id=row[0],
                preferred_context_sections=json.loads(row[1]),
                preferred_context_depth=row[2],
                relevance_threshold=row[3],
                learning_patterns=json.loads(row[4]),
                last_updated=datetime.fromisoformat(row[5]),
                success_rate=row[6],
                total_interactions=row[7]
            )
        return None

    def update_user_profile(self, profile: UserContextProfile):
        """Update user's context profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO user_context_profiles 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.user_id,
            json.dumps(profile.preferred_context_sections),
            profile.preferred_context_depth,
            profile.relevance_threshold,
            json.dumps(profile.learning_patterns),
            profile.last_updated.isoformat(),
            profile.success_rate,
            profile.total_interactions
        ))

        conn.commit()
        conn.close()

class ContextLearningAnalyzer:
    """Analyzes learning events to extract insights"""

    def __init__(self, learning_db: ContextLearningDatabase):
        self.learning_db = learning_db

    def analyze_context_effectiveness(self, user_id: str, limit: int = 100) -> Dict[str, Any]:
        """Analyze which context sections are most effective for a user"""
        conn = sqlite3.connect(self.learning_db.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT selected_context, user_satisfaction, ai_response_quality
            FROM context_learning_events 
            WHERE session_id = ? AND user_satisfaction IS NOT NULL
            ORDER BY timestamp DESC LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"insights": "No learning data available", "recommendations": []}

        # Analyze context section effectiveness
        section_scores = {}
        total_events = len(rows)

        for row in rows:
            selected_context = json.loads(row[0])
            satisfaction = row[1] or 0.5
            quality = row[2] or 0.5
            combined_score = (satisfaction + quality) / 2

            for section_name, section_data in selected_context.items():
                if section_name not in section_scores:
                    section_scores[section_name] = {"total_score": 0, "count": 0}
                
                section_scores[section_name]["total_score"] += combined_score
                section_scores[section_name]["count"] += 1

        # Calculate average scores and generate recommendations
        insights = {}
        recommendations = []

        for section_name, scores in section_scores.items():
            avg_score = scores["total_score"] / scores["count"]
            insights[section_name] = {
                "average_score": avg_score,
                "usage_count": scores["count"],
                "effectiveness": "high" if avg_score > 0.7 else "medium" if avg_score > 0.5 else "low"
            }

            if avg_score < 0.5:
                recommendations.append(f"Consider excluding {section_name} (low effectiveness: {avg_score:.2f})")
            elif avg_score > 0.8:
                recommendations.append(f"Prioritize {section_name} (high effectiveness: {avg_score:.2f})")

        return {
            "insights": insights,
            "recommendations": recommendations,
            "total_events_analyzed": total_events
        }

    def detect_learning_patterns(self, user_id: str) -> Dict[str, Any]:
        """Detect patterns in user's context preferences"""
        conn = sqlite3.connect(self.learning_db.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_message, selected_context, excluded_context, timestamp
            FROM context_learning_events 
            WHERE session_id = ?
            ORDER BY timestamp DESC LIMIT 50
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return {"patterns": "No pattern data available"}

        # Analyze patterns
        patterns = {
            "message_types": {},
            "context_preferences": {},
            "temporal_patterns": {},
            "exclusion_patterns": {}
        }

        for row in rows:
            message = row[0].lower()
            selected = json.loads(row[1])
            excluded = json.loads(row[2])
            timestamp = datetime.fromisoformat(row[3])

            # Message type patterns
            if "how" in message or "implement" in message:
                patterns["message_types"]["how_to"] = patterns["message_types"].get("how_to", 0) + 1
            elif "what" in message or "explain" in message:
                patterns["message_types"]["explanation"] = patterns["message_types"].get("explanation", 0) + 1
            elif "debug" in message or "error" in message:
                patterns["message_types"]["debugging"] = patterns["message_types"].get("debugging", 0) + 1

            # Context preference patterns
            for section in selected:
                patterns["context_preferences"][section] = patterns["context_preferences"].get(section, 0) + 1

            # Exclusion patterns
            for section in excluded:
                patterns["exclusion_patterns"][section] = patterns["exclusion_patterns"].get(section, 0) + 1

        return {"patterns": patterns, "total_events": len(rows)}

class AdaptiveContextLearner:
    """Main class for adaptive context learning"""

    def __init__(self, db_path: str = "data/context_learning.db"):
        self.learning_db = ContextLearningDatabase(db_path)
        self.analyzer = ContextLearningAnalyzer(self.learning_db)

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import hashlib
        content = f"context_learning_{datetime.now(timezone.utc).isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def learn_from_interaction(self, user_message: str, selected_context: Dict, 
                             excluded_context: List[str], user_satisfaction: Optional[float] = None,
                             ai_response_quality: Optional[float] = None, session_id: str = "default") -> str:
        """Learn from a user interaction to improve future context selection"""
        
        # Create learning event
        event = ContextLearningEvent(
            event_id=self._generate_event_id(),
            event_type=LearningEventType.CONTEXT_SELECTION,
            user_message=user_message,
            selected_context=selected_context,
            excluded_context=excluded_context,
            user_satisfaction=user_satisfaction,
            ai_response_quality=ai_response_quality,
            session_id=session_id
        )

        # Store the learning event
        self.learning_db.store_learning_event(event)

        # Analyze for insights
        insights = self._extract_learning_insights(event)
        event.learning_insights = insights

        # Update the event with insights
        self.learning_db.store_learning_event(event)

        return f"Learned from interaction: {insights.get('summary', 'No insights available')}"

    def get_user_optimization_recommendations(self, user_id: str = "default") -> Dict[str, Any]:
        """Get personalized optimization recommendations for a user"""
        
        # Analyze context effectiveness
        effectiveness_analysis = self.analyzer.analyze_context_effectiveness(user_id)
        
        # Detect learning patterns
        pattern_analysis = self.analyzer.detect_learning_patterns(user_id)
        
        # Generate recommendations
        recommendations = {
            "context_optimization": effectiveness_analysis.get("recommendations", []),
            "pattern_insights": pattern_analysis.get("patterns", {}),
            "personalization_suggestions": self._generate_personalization_suggestions(effectiveness_analysis, pattern_analysis)
        }

        return recommendations

    def _extract_learning_insights(self, event: ContextLearningEvent) -> Dict[str, Any]:
        """Extract learning insights from an event"""
        insights = {
            "summary": "",
            "context_effectiveness": {},
            "improvement_opportunities": []
        }

        # Analyze selected context effectiveness
        if event.user_satisfaction is not None and event.ai_response_quality is not None:
            combined_score = (event.user_satisfaction + event.ai_response_quality) / 2
            
            if combined_score < 0.5:
                insights["summary"] = "Low satisfaction detected - context selection needs improvement"
                insights["improvement_opportunities"].append("Review context relevance criteria")
            elif combined_score > 0.8:
                insights["summary"] = "High satisfaction - context selection working well"
            else:
                insights["summary"] = "Moderate satisfaction - some room for improvement"

        # Analyze context section usage
        for section_name, section_data in event.selected_context.items():
            insights["context_effectiveness"][section_name] = {
                "included": True,
                "data_quality": len(str(section_data)) if section_data else 0
            }

        for section_name in event.excluded_context:
            insights["context_effectiveness"][section_name] = {
                "included": False,
                "reason": "Below relevance threshold"
            }

        return insights

    def _generate_personalization_suggestions(self, effectiveness_analysis: Dict, pattern_analysis: Dict) -> List[str]:
        """Generate personalization suggestions based on analysis"""
        suggestions = []

        # Context effectiveness suggestions
        if "insights" in effectiveness_analysis:
            for section_name, data in effectiveness_analysis["insights"].items():
                if data.get("effectiveness") == "low":
                    suggestions.append(f"Consider reducing frequency of {section_name} context")
                elif data.get("effectiveness") == "high":
                    suggestions.append(f"Prioritize {section_name} context for better results")

        # Pattern-based suggestions
        if "patterns" in pattern_analysis:
            patterns = pattern_analysis["patterns"]
            
            if patterns.get("message_types", {}).get("how_to", 0) > 10:
                suggestions.append("User frequently asks how-to questions - prioritize technical context")
            
            if patterns.get("message_types", {}).get("debugging", 0) > 5:
                suggestions.append("User often needs debugging help - include error context and best practices")

        return suggestions

# Example usage and testing
if __name__ == "__main__":
    learner = AdaptiveContextLearner()
    
    # Test learning from interaction
    test_context = {
        "user_preferences": "Technical, concise responses",
        "tech_stack": "Python, SQLite, MCP"
    }
    
    excluded = ["conversation_summary", "action_history"]
    
    result = learner.learn_from_interaction(
        user_message="How do I implement a database connection?",
        selected_context=test_context,
        excluded_context=excluded,
        user_satisfaction=0.8,
        ai_response_quality=0.9
    )
    
    print(f"🧠 Learning Result: {result}")
    
    # Test getting recommendations
    recommendations = learner.get_user_optimization_recommendations("test_user")
    print(f"📊 Recommendations: {json.dumps(recommendations, indent=2)}")
