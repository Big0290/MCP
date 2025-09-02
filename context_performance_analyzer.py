#!/usr/bin/env python3
"""
📈 Context Performance Analyzer - Phase 2 Implementation
Tracks and optimizes context selection effectiveness through comprehensive analytics.
"""

import json
import sqlite3
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from enum import Enum
import statistics
import hashlib

class PerformanceMetric(Enum):
    """Types of performance metrics"""
    CONTEXT_RELEVANCE = "context_relevance"
    RESPONSE_QUALITY = "response_quality"
    USER_SATISFACTION = "user_satisfaction"
    RESPONSE_TIME = "response_time"
    CONTEXT_SIZE = "context_size"

class OptimizationStrategy(Enum):
    """Optimization strategies for context selection"""
    THRESHOLD_OPTIMIZATION = "threshold_optimization"
    CONTEXT_PRIORITIZATION = "context_prioritization"
    PATTERN_OPTIMIZATION = "pattern_optimization"
    USER_PERSONALIZATION = "user_personalization"

@dataclass
class ContextPerformanceEvent:
    """A performance event for context selection analysis"""
    event_id: str
    user_message: str
    selected_context: Dict[str, Any]
    excluded_context: List[str]
    context_size: int
    response_time_ms: int
    user_satisfaction: Optional[float] = None
    ai_response_quality: Optional[float] = None
    context_relevance_score: Optional[float] = None
    timestamp: datetime = None
    session_id: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)
        if self.event_id is None:
            self.event_id = self._generate_event_id()

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        content = f"{self.user_message}_{self.timestamp.isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

@dataclass
class PerformanceInsight:
    """Insight derived from performance analysis"""
    insight_type: str
    description: str
    confidence: float
    actionable: bool
    impact_score: float
    recommendations: List[str]
    data_points: int

@dataclass
class OptimizationRecommendation:
    """Recommendation for context selection optimization"""
    recommendation_id: str
    strategy: OptimizationStrategy
    description: str
    expected_impact: float
    implementation_complexity: str  # "low", "medium", "high"
    priority: int  # 1 = highest
    supporting_data: Dict[str, Any]

class PerformanceDatabase:
    """Database for storing performance events and analytics"""

    def __init__(self, db_path: str = "data/context_performance.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the performance database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Performance events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS context_performance_events (
                event_id TEXT PRIMARY KEY,
                user_message TEXT NOT NULL,
                selected_context TEXT NOT NULL,
                excluded_context TEXT NOT NULL,
                context_size INTEGER NOT NULL,
                response_time_ms INTEGER NOT NULL,
                user_satisfaction REAL,
                ai_response_quality REAL,
                context_relevance_score REAL,
                timestamp TEXT NOT NULL,
                session_id TEXT
            )
        """)

        # Performance insights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_insights (
                insight_id TEXT PRIMARY KEY,
                insight_type TEXT NOT NULL,
                description TEXT NOT NULL,
                confidence REAL NOT NULL,
                actionable BOOLEAN NOT NULL,
                impact_score REAL NOT NULL,
                recommendations TEXT NOT NULL,
                data_points INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        # Optimization recommendations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS optimization_recommendations (
                recommendation_id TEXT PRIMARY KEY,
                strategy TEXT NOT NULL,
                description TEXT NOT NULL,
                expected_impact REAL NOT NULL,
                implementation_complexity TEXT NOT NULL,
                priority INTEGER NOT NULL,
                supporting_data TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                implemented_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def store_performance_event(self, event: ContextPerformanceEvent):
        """Store a performance event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO context_performance_events 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.event_id,
            event.user_message,
            json.dumps(event.selected_context),
            json.dumps(event.excluded_context),
            event.context_size,
            event.response_time_ms,
            event.user_satisfaction,
            event.ai_response_quality,
            event.context_relevance_score,
            event.timestamp.isoformat(),
            event.session_id
        ))

        conn.commit()
        conn.close()

    def get_performance_events(self, session_id: str = None, limit: int = 100) -> List[ContextPerformanceEvent]:
        """Get performance events, optionally filtered by session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if session_id:
            cursor.execute("""
                SELECT * FROM context_performance_events 
                WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?
            """, (session_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM context_performance_events 
                ORDER BY timestamp DESC LIMIT ?
            """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        events = []
        for row in rows:
            event = ContextPerformanceEvent(
                event_id=row[0],
                user_message=row[1],
                selected_context=json.loads(row[2]),
                excluded_context=json.loads(row[3]),
                context_size=row[4],
                response_time_ms=row[5],
                user_satisfaction=row[6],
                ai_response_quality=row[7],
                context_relevance_score=row[8],
                timestamp=datetime.fromisoformat(row[9]),
                session_id=row[10]
            )
            events.append(event)

        return events

class PerformanceAnalyzer:
    """Analyzes performance data to extract insights"""

    def __init__(self, performance_db: PerformanceDatabase):
        self.performance_db = performance_db

    def analyze_context_effectiveness(self, session_id: str = None, time_window_hours: int = 24) -> Dict[str, Any]:
        """Analyze overall context selection effectiveness"""
        
        events = self.performance_db.get_performance_events(session_id, limit=1000)
        
        # Filter by time window
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=time_window_hours)
        recent_events = [e for e in events if e.timestamp > cutoff_time]
        
        if not recent_events:
            return {"error": "No performance data available for analysis"}

        # Calculate key metrics
        total_events = len(recent_events)
        avg_context_size = statistics.mean([e.context_size for e in recent_events])
        avg_response_time = statistics.mean([e.response_time_ms for e in recent_events])
        
        # Satisfaction analysis
        satisfaction_events = [e for e in recent_events if e.user_satisfaction is not None]
        avg_satisfaction = statistics.mean([e.user_satisfaction for e in satisfaction_events]) if satisfaction_events else 0
        
        # Quality analysis
        quality_events = [e for e in recent_events if e.ai_response_quality is not None]
        avg_quality = statistics.mean([e.ai_response_quality for e in quality_events]) if quality_events else 0
        
        # Context section analysis
        context_section_usage = {}
        context_section_satisfaction = {}
        
        for event in recent_events:
            for section_name, section_data in event.selected_context.items():
                if section_name not in context_section_usage:
                    context_section_usage[section_name] = 0
                    context_section_satisfaction[section_name] = []
                
                context_section_usage[section_name] += 1
                if event.user_satisfaction is not None:
                    context_section_satisfaction[section_name].append(event.user_satisfaction)

        # Calculate section effectiveness
        section_effectiveness = {}
        for section_name, usage_count in context_section_usage.items():
            if section_name in context_section_satisfaction and context_section_satisfaction[section_name]:
                avg_section_satisfaction = statistics.mean(context_section_satisfaction[section_name])
                section_effectiveness[section_name] = {
                    "usage_count": usage_count,
                    "avg_satisfaction": avg_section_satisfaction,
                    "effectiveness": "high" if avg_section_satisfaction > 0.7 else "medium" if avg_section_satisfaction > 0.5 else "low"
                }

        return {
            "analysis_period": f"Last {time_window_hours} hours",
            "total_events": total_events,
            "avg_context_size": round(avg_context_size, 2),
            "avg_response_time_ms": round(avg_response_time, 2),
            "avg_user_satisfaction": round(avg_satisfaction, 3),
            "avg_ai_response_quality": round(avg_quality, 3),
            "context_section_effectiveness": section_effectiveness,
            "overall_performance": self._calculate_overall_performance(avg_satisfaction, avg_quality, avg_response_time)
        }

    def detect_performance_patterns(self, session_id: str = None) -> List[PerformanceInsight]:
        """Detect patterns in performance data"""
        
        events = self.performance_db.get_performance_events(session_id, limit=500)
        insights = []

        if not events:
            return insights

        # Pattern 1: Context size vs satisfaction correlation
        size_satisfaction_correlation = self._analyze_size_satisfaction_correlation(events)
        if size_satisfaction_correlation:
            insights.append(size_satisfaction_correlation)

        # Pattern 2: Response time vs satisfaction correlation
        time_satisfaction_correlation = self._analyze_time_satisfaction_correlation(events)
        if time_satisfaction_correlation:
            insights.append(time_satisfaction_correlation)

        # Pattern 3: Context section effectiveness patterns
        section_patterns = self._analyze_section_effectiveness_patterns(events)
        insights.extend(section_patterns)

        # Pattern 4: Temporal performance patterns
        temporal_patterns = self._analyze_temporal_patterns(events)
        insights.extend(temporal_patterns)

        return insights

    def generate_optimization_recommendations(self, session_id: str = None) -> List[OptimizationRecommendation]:
        """Generate optimization recommendations based on performance analysis"""
        
        # Analyze performance
        effectiveness_analysis = self.analyze_context_effectiveness(session_id)
        performance_patterns = self.detect_performance_patterns(session_id)
        
        recommendations = []

        # Recommendation 1: Threshold optimization
        if "avg_user_satisfaction" in effectiveness_analysis:
            satisfaction = effectiveness_analysis["avg_user_satisfaction"]
            if satisfaction < 0.6:
                recommendations.append(OptimizationRecommendation(
                    recommendation_id=f"thresh_opt_{int(datetime.now(timezone.utc).timestamp())}",
                    strategy=OptimizationStrategy.THRESHOLD_OPTIMIZATION,
                    description="User satisfaction is below target - consider lowering relevance thresholds",
                    expected_impact=0.15,
                    implementation_complexity="medium",
                    priority=1,
                    supporting_data={"current_satisfaction": satisfaction, "target_satisfaction": 0.7}
                ))

        # Recommendation 2: Context prioritization
        if "context_section_effectiveness" in effectiveness_analysis:
            section_effectiveness = effectiveness_analysis["context_section_effectiveness"]
            low_effectiveness_sections = [
                section for section, data in section_effectiveness.items()
                if data.get("effectiveness") == "low"
            ]
            
            if low_effectiveness_sections:
                recommendations.append(OptimizationRecommendation(
                    recommendation_id=f"context_prio_{int(datetime.now(timezone.utc).timestamp())}",
                    strategy=OptimizationStrategy.CONTEXT_PRIORITIZATION,
                    description=f"Consider deprioritizing low-effectiveness context sections: {', '.join(low_effectiveness_sections)}",
                    expected_impact=0.1,
                    implementation_complexity="low",
                    priority=2,
                    supporting_data={"low_effectiveness_sections": low_effectiveness_sections}
                ))

        # Recommendation 3: Pattern optimization
        pattern_insights = [p for p in performance_patterns if p.actionable and p.impact_score > 0.1]
        if pattern_insights:
            recommendations.append(OptimizationRecommendation(
                recommendation_id=f"pattern_opt_{int(datetime.now(timezone.utc).timestamp())}",
                strategy=OptimizationStrategy.PATTERN_OPTIMIZATION,
                description=f"Implement pattern-based optimizations based on {len(pattern_insights)} insights",
                expected_impact=0.12,
                implementation_complexity="high",
                priority=3,
                supporting_data={"pattern_insights": [p.description for p in pattern_insights]}
            ))

        # Sort by priority
        recommendations.sort(key=lambda x: x.priority)
        return recommendations

    def _calculate_overall_performance(self, satisfaction: float, quality: float, response_time: float) -> str:
        """Calculate overall performance rating"""
        if satisfaction >= 0.8 and quality >= 0.8 and response_time < 1000:
            return "excellent"
        elif satisfaction >= 0.7 and quality >= 0.7 and response_time < 2000:
            return "good"
        elif satisfaction >= 0.6 and quality >= 0.6 and response_time < 3000:
            return "fair"
        else:
            return "needs_improvement"

    def _analyze_size_satisfaction_correlation(self, events: List[ContextPerformanceEvent]) -> Optional[PerformanceInsight]:
        """Analyze correlation between context size and user satisfaction"""
        valid_events = [e for e in events if e.user_satisfaction is not None and e.context_size > 0]
        
        if len(valid_events) < 10:
            return None

        # Calculate correlation
        sizes = [e.context_size for e in valid_events]
        satisfactions = [e.user_satisfaction for e in valid_events]
        
        # Simple correlation calculation
        avg_size = statistics.mean(sizes)
        avg_satisfaction = statistics.mean(satisfactions)
        
        numerator = sum((s - avg_size) * (sat - avg_satisfaction) for s, sat in zip(sizes, satisfactions))
        denominator = (sum((s - avg_size) ** 2 for s in sizes) * sum((sat - avg_satisfaction) ** 2 for sat in satisfactions)) ** 0.5
        
        if denominator == 0:
            return None
            
        correlation = numerator / denominator

        if abs(correlation) > 0.3:
            if correlation > 0:
                description = "Larger context size correlates with higher user satisfaction"
                recommendations = ["Consider increasing context size for better user experience"]
            else:
                description = "Smaller context size correlates with higher user satisfaction"
                recommendations = ["Consider reducing context size to improve user experience"]
            
            return PerformanceInsight(
                insight_type="size_satisfaction_correlation",
                description=description,
                confidence=min(abs(correlation), 1.0),
                actionable=True,
                impact_score=0.15,
                recommendations=recommendations,
                data_points=len(valid_events)
            )
        
        return None

    def _analyze_time_satisfaction_correlation(self, events: List[ContextPerformanceEvent]) -> Optional[PerformanceInsight]:
        """Analyze correlation between response time and user satisfaction"""
        valid_events = [e for e in events if e.user_satisfaction is not None and e.response_time_ms > 0]
        
        if len(valid_events) < 10:
            return None

        # Calculate correlation
        times = [e.response_time_ms for e in valid_events]
        satisfactions = [e.user_satisfaction for e in valid_events]
        
        avg_time = statistics.mean(times)
        avg_satisfaction = statistics.mean(satisfactions)
        
        numerator = sum((t - avg_time) * (sat - avg_satisfaction) for t, sat in zip(times, satisfactions))
        denominator = (sum((t - avg_time) ** 2 for t in times) * sum((sat - avg_satisfaction) ** 2 for sat in satisfactions)) ** 0.5
        
        if denominator == 0:
            return None
            
        correlation = numerator / denominator

        if abs(correlation) > 0.3:
            if correlation < 0:
                description = "Faster response time correlates with higher user satisfaction"
                recommendations = ["Optimize context selection for faster response times"]
            else:
                description = "Slower response time correlates with higher user satisfaction"
                recommendations = ["Consider allowing more time for comprehensive context selection"]
            
            return PerformanceInsight(
                insight_type="time_satisfaction_correlation",
                description=description,
                confidence=min(abs(correlation), 1.0),
                actionable=True,
                impact_score=0.12,
                recommendations=recommendations,
                data_points=len(valid_events)
            )
        
        return None

    def _analyze_section_effectiveness_patterns(self, events: List[ContextPerformanceEvent]) -> List[PerformanceInsight]:
        """Analyze patterns in context section effectiveness"""
        insights = []
        
        # Group events by context sections
        section_events = {}
        for event in events:
            for section_name in event.selected_context.keys():
                if section_name not in section_events:
                    section_events[section_name] = []
                section_events[section_name].append(event)

        # Analyze each section
        for section_name, section_event_list in section_events.items():
            if len(section_event_list) < 5:
                continue
                
            # Calculate section performance
            satisfaction_scores = [e.user_satisfaction for e in section_event_list if e.user_satisfaction is not None]
            if not satisfaction_scores:
                continue
                
            avg_satisfaction = statistics.mean(satisfaction_scores)
            
            if avg_satisfaction < 0.5:
                insights.append(PerformanceInsight(
                    insight_type="section_effectiveness",
                    description=f"Context section '{section_name}' shows low effectiveness (avg satisfaction: {avg_satisfaction:.2f})",
                    confidence=0.8,
                    actionable=True,
                    impact_score=0.1,
                    recommendations=[f"Consider excluding or improving '{section_name}' context"],
                    data_points=len(satisfaction_scores)
                ))
            elif avg_satisfaction > 0.8:
                insights.append(PerformanceInsight(
                    insight_type="section_effectiveness",
                    description=f"Context section '{section_name}' shows high effectiveness (avg satisfaction: {avg_satisfaction:.2f})",
                    confidence=0.8,
                    actionable=True,
                    impact_score=0.05,
                    recommendations=[f"Prioritize '{section_name}' context for better results"],
                    data_points=len(satisfaction_scores)
                ))

        return insights

    def _analyze_temporal_patterns(self, events: List[ContextPerformanceEvent]) -> List[PerformanceInsight]:
        """Analyze temporal patterns in performance"""
        insights = []
        
        if len(events) < 20:
            return insights

        # Group events by hour of day
        hourly_performance = {}
        for event in events:
            hour = event.timestamp.hour
            if hour not in hourly_performance:
                hourly_performance[hour] = []
            hourly_performance[hour].append(event)

        # Analyze hourly patterns
        for hour, hour_events in hourly_performance.items():
            if len(hour_events) < 3:
                continue
                
            satisfaction_scores = [e.user_satisfaction for e in hour_events if e.user_satisfaction is not None]
            if not satisfaction_scores:
                continue
                
            avg_satisfaction = statistics.mean(satisfaction_scores)
            
            if avg_satisfaction < 0.6:
                insights.append(PerformanceInsight(
                    insight_type="temporal_pattern",
                    description=f"Performance is lower during hour {hour}:00 (avg satisfaction: {avg_satisfaction:.2f})",
                    confidence=0.6,
                    actionable=False,
                    impact_score=0.05,
                    recommendations=["Monitor performance during this time period"],
                    data_points=len(satisfaction_scores)
                ))

        return insights

class ContextPerformanceAnalyzer:
    """Main class for context performance analysis"""

    def __init__(self, db_path: str = "data/context_performance.db"):
        self.performance_db = PerformanceDatabase(db_path)
        self.analyzer = PerformanceAnalyzer(self.performance_db)

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        import hashlib
        content = f"performance_event_{datetime.now(timezone.utc).isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def track_performance_event(self, user_message: str, selected_context: Dict, 
                              excluded_context: List[str], response_time_ms: int,
                              user_satisfaction: Optional[float] = None,
                              ai_response_quality: Optional[float] = None,
                              context_relevance_score: Optional[float] = None,
                              session_id: str = "default") -> str:
        """Track a performance event for analysis"""
        
        # Calculate context size
        context_size = sum(len(str(v)) for v in selected_context.values())
        
        # Create performance event
        event = ContextPerformanceEvent(
            event_id=self._generate_event_id(),
            user_message=user_message,
            selected_context=selected_context,
            excluded_context=excluded_context,
            context_size=context_size,
            response_time_ms=response_time_ms,
            user_satisfaction=user_satisfaction,
            ai_response_quality=ai_response_quality,
            context_relevance_score=context_relevance_score,
            session_id=session_id
        )

        # Store the event
        self.performance_db.store_performance_event(event)
        
        return f"Performance event tracked: {context_size} chars, {response_time_ms}ms response time"

    def get_performance_analytics(self, session_id: str = None, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get comprehensive performance analytics"""
        return self.analyzer.analyze_context_effectiveness(session_id, time_window_hours)

    def get_performance_insights(self, session_id: str = None) -> List[PerformanceInsight]:
        """Get performance insights and patterns"""
        return self.analyzer.detect_performance_patterns(session_id)

    def get_optimization_recommendations(self, session_id: str = None) -> List[OptimizationRecommendation]:
        """Get optimization recommendations"""
        return self.analyzer.generate_optimization_recommendations(session_id)

    def get_performance_summary(self, session_id: str = None) -> Dict[str, Any]:
        """Get a summary of performance metrics"""
        analytics = self.get_performance_analytics(session_id)
        insights = self.get_performance_insights(session_id)
        recommendations = self.get_optimization_recommendations(session_id)
        
        return {
            "analytics": analytics,
            "insights_count": len(insights),
            "actionable_insights": len([i for i in insights if i.actionable]),
            "recommendations_count": len(recommendations),
            "high_priority_recommendations": len([r for r in recommendations if r.priority == 1]),
            "overall_status": analytics.get("overall_performance", "unknown")
        }

# Example usage and testing
if __name__ == "__main__":
    analyzer = ContextPerformanceAnalyzer()
    
    # Test tracking a performance event
    test_context = {
        "user_preferences": "Technical, concise responses",
        "tech_stack": "Python, SQLite, MCP"
    }
    
    result = analyzer.track_performance_event(
        user_message="How do I implement a database connection?",
        selected_context=test_context,
        excluded_context=["conversation_summary"],
        response_time_ms=1500,
        user_satisfaction=0.8,
        ai_response_quality=0.9
    )
    
    print(f"📊 Performance Tracking: {result}")
    
    # Test getting analytics
    analytics = analyzer.get_performance_analytics()
    print(f"📈 Performance Analytics: {json.dumps(analytics, indent=2)}")
    
    # Test getting insights
    insights = analyzer.get_performance_insights()
    print(f"🔍 Performance Insights: {len(insights)} found")
    
    # Test getting recommendations
    recommendations = analyzer.get_optimization_recommendations()
    print(f"💡 Optimization Recommendations: {len(recommendations)} found")
    
    # Test getting summary
    summary = analyzer.get_performance_summary()
    print(f"📋 Performance Summary: {json.dumps(summary, indent=2)}")
