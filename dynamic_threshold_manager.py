#!/usr/bin/env python3
"""
⚡ Dynamic Threshold Manager - Phase 2 Implementation
Adjusts relevance thresholds based on user behavior and preferences for personalized context selection.
"""

import json
import sqlite3
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import statistics

class UserStyle(Enum):
    """User communication and context preferences"""
    CONCISE = "concise"
    DETAILED = "detailed"
    COMPREHENSIVE = "comprehensive"
    TECHNICAL = "technical"
    GENERAL = "general"

class ThresholdAdjustmentStrategy(Enum):
    """Strategies for adjusting thresholds"""
    CONSERVATIVE = "conservative"      # Small adjustments
    MODERATE = "moderate"             # Medium adjustments
    AGGRESSIVE = "aggressive"         # Large adjustments
    ADAPTIVE = "adaptive"             # Dynamic based on user behavior

@dataclass
class ThresholdProfile:
    """User's threshold profile for context selection"""
    user_id: str
    base_threshold: float
    current_threshold: float
    user_style: UserStyle
    adjustment_history: List[Dict[str, Any]]
    last_adjusted: datetime
    success_rate: float
    total_adjustments: int

@dataclass
class ThresholdAdjustment:
    """A threshold adjustment event"""
    adjustment_id: str
    user_id: str
    old_threshold: float
    new_threshold: float
    adjustment_reason: str
    user_style_detected: UserStyle
    success_impact: Optional[float] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

class UserStyleAnalyzer:
    """Analyzes user behavior to determine preferred style"""

    def __init__(self):
        self.style_indicators = {
            UserStyle.CONCISE: {
                "message_length": {"avg": 50, "max": 100},
                "context_preference": "minimal",
                "response_length": "short",
                "keywords": ["quick", "simple", "brief", "concise"]
            },
            UserStyle.DETAILED: {
                "message_length": {"avg": 150, "max": 300},
                "context_preference": "moderate",
                "response_length": "medium",
                "keywords": ["explain", "detail", "how", "why", "step by step"]
            },
            UserStyle.COMPREHENSIVE: {
                "message_length": {"avg": 300, "max": 600},
                "context_preference": "extensive",
                "response_length": "long",
                "keywords": ["comprehensive", "thorough", "complete", "full", "everything"]
            },
            UserStyle.TECHNICAL: {
                "message_length": {"avg": 200, "max": 400},
                "context_preference": "technical",
                "response_length": "technical",
                "keywords": ["implement", "code", "algorithm", "performance", "optimization"]
            }
        }

    def analyze_user_style(self, conversation_history: List[Dict[str, Any]]) -> UserStyle:
        """Analyze user's communication style from conversation history"""
        if not conversation_history:
            return UserStyle.GENERAL

        # Analyze message characteristics
        message_lengths = []
        technical_keywords = 0
        style_keywords = {style: 0 for style in UserStyle}

        for interaction in conversation_history:
            if "user_message" in interaction:
                message = interaction["user_message"]
                message_lengths.append(len(message))

                # Count style-specific keywords
                message_lower = message.lower()
                for style, indicators in self.style_indicators.items():
                    for keyword in indicators["keywords"]:
                        if keyword in message_lower:
                            style_keywords[style] += 1

                # Count technical keywords
                technical_terms = ["code", "implement", "function", "class", "database", "api"]
                for term in technical_terms:
                    if term in message_lower:
                        technical_keywords += 1

        # Determine primary style
        if message_lengths:
            avg_length = statistics.mean(message_lengths)
            max_length = max(message_lengths)

            # Style detection logic
            if technical_keywords > 5:
                return UserStyle.TECHNICAL
            elif max(style_keywords.values()) > 2:
                # Return the style with most keyword matches
                return max(style_keywords.items(), key=lambda x: x[1])[0]
            elif avg_length < 80:
                return UserStyle.CONCISE
            elif avg_length > 200:
                return UserStyle.COMPREHENSIVE
            else:
                return UserStyle.DETAILED

        return UserStyle.GENERAL

    def get_style_threshold_mapping(self, user_style: UserStyle) -> Dict[str, float]:
        """Get threshold mappings for different user styles"""
        style_thresholds = {
            UserStyle.CONCISE: {
                "base_threshold": 0.7,
                "context_expansion": 0.8,
                "min_context_sections": 2
            },
            UserStyle.DETAILED: {
                "base_threshold": 0.6,
                "context_expansion": 0.7,
                "min_context_sections": 3
            },
            UserStyle.COMPREHENSIVE: {
                "base_threshold": 0.5,
                "context_expansion": 0.6,
                "min_context_sections": 5
            },
            UserStyle.TECHNICAL: {
                "base_threshold": 0.65,
                "context_expansion": 0.75,
                "min_context_sections": 4
            },
            UserStyle.GENERAL: {
                "base_threshold": 0.6,
                "context_expansion": 0.7,
                "min_context_sections": 3
            }
        }

        return style_thresholds.get(user_style, style_thresholds[UserStyle.GENERAL])

class ThresholdAdjustmentEngine:
    """Engine for calculating threshold adjustments"""

    def __init__(self):
        self.adjustment_strategies = {
            ThresholdAdjustmentStrategy.CONSERVATIVE: 0.05,
            ThresholdAdjustmentStrategy.MODERATE: 0.1,
            ThresholdAdjustmentStrategy.AGGRESSIVE: 0.2,
            ThresholdAdjustmentStrategy.ADAPTIVE: 0.15
        }

    def calculate_threshold_adjustment(self, current_threshold: float, user_style: UserStyle,
                                    success_rate: float, recent_performance: List[float],
                                    strategy: ThresholdAdjustmentStrategy = ThresholdAdjustmentStrategy.ADAPTIVE) -> float:
        """Calculate new threshold based on user performance and style"""
        
        # Get style-based target threshold
        style_analyzer = UserStyleAnalyzer()
        style_thresholds = style_analyzer.get_style_threshold_mapping(user_style)
        target_threshold = style_thresholds["base_threshold"]

        # Calculate adjustment based on performance
        if recent_performance:
            avg_recent_performance = statistics.mean(recent_performance)
            performance_gap = target_threshold - avg_recent_performance
        else:
            performance_gap = target_threshold - success_rate

        # Get adjustment magnitude
        base_adjustment = self.adjustment_strategies[strategy]
        
        # Adaptive adjustment based on gap size
        if strategy == ThresholdAdjustmentStrategy.ADAPTIVE:
            if abs(performance_gap) > 0.2:
                base_adjustment *= 1.5  # Larger adjustment for big gaps
            elif abs(performance_gap) < 0.05:
                base_adjustment *= 0.5  # Smaller adjustment for small gaps

        # Calculate new threshold
        if performance_gap > 0:
            # Need to lower threshold (include more context)
            new_threshold = current_threshold - (base_adjustment * min(abs(performance_gap), 0.3))
        else:
            # Need to raise threshold (include less context)
            new_threshold = current_threshold + (base_adjustment * min(abs(performance_gap), 0.3))

        # Ensure threshold stays within reasonable bounds
        new_threshold = max(0.3, min(0.9, new_threshold))

        return round(new_threshold, 3)

    def should_adjust_threshold(self, current_threshold: float, target_threshold: float,
                              last_adjustment: datetime, min_adjustment_interval: int = 10) -> bool:
        """Determine if threshold should be adjusted"""
        
        # Check if enough time has passed since last adjustment
        time_since_last = (datetime.now(timezone.utc) - last_adjustment).total_seconds() / 60
        if time_since_last < min_adjustment_interval:
            return False

        # Check if adjustment is significant enough
        threshold_difference = abs(current_threshold - target_threshold)
        return threshold_difference > 0.05

class ThresholdDatabase:
    """Database for storing threshold profiles and adjustments"""

    def __init__(self, db_path: str = "data/threshold_profiles.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize the threshold database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Threshold profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threshold_profiles (
                user_id TEXT PRIMARY KEY,
                base_threshold REAL NOT NULL,
                current_threshold REAL NOT NULL,
                user_style TEXT NOT NULL,
                adjustment_history TEXT NOT NULL,
                last_adjusted TEXT NOT NULL,
                success_rate REAL NOT NULL,
                total_adjustments INTEGER NOT NULL
            )
        """)

        # Threshold adjustments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threshold_adjustments (
                adjustment_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                old_threshold REAL NOT NULL,
                new_threshold REAL NOT NULL,
                adjustment_reason TEXT NOT NULL,
                user_style_detected TEXT NOT NULL,
                success_impact REAL,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def get_user_profile(self, user_id: str) -> Optional[ThresholdProfile]:
        """Get user's threshold profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM threshold_profiles WHERE user_id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return ThresholdProfile(
                user_id=row[0],
                base_threshold=row[1],
                current_threshold=row[2],
                user_style=UserStyle(row[3]),
                adjustment_history=json.loads(row[4]),
                last_adjusted=datetime.fromisoformat(row[5]),
                success_rate=row[6],
                total_adjustments=row[7]
            )
        return None

    def update_user_profile(self, profile: ThresholdProfile):
        """Update user's threshold profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO threshold_profiles 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.user_id,
            profile.base_threshold,
            profile.current_threshold,
            profile.user_style.value,
            json.dumps(profile.adjustment_history),
            profile.last_adjusted.isoformat(),
            profile.success_rate,
            profile.total_adjustments
        ))

        conn.commit()
        conn.close()

    def store_adjustment(self, adjustment: ThresholdAdjustment):
        """Store a threshold adjustment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO threshold_adjustments 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            adjustment.adjustment_id,
            adjustment.user_id,
            adjustment.old_threshold,
            adjustment.new_threshold,
            adjustment.adjustment_reason,
            adjustment.user_style_detected.value,
            adjustment.success_impact,
            adjustment.timestamp.isoformat()
        ))

        conn.commit()
        conn.close()

class DynamicThresholdManager:
    """Main class for dynamic threshold management"""

    def __init__(self, db_path: str = "data/threshold_profiles.db"):
        self.threshold_db = ThresholdDatabase(db_path)
        self.style_analyzer = UserStyleAnalyzer()
        self.adjustment_engine = ThresholdAdjustmentEngine()

    def analyze_user_style(self, conversation_history: List[Dict[str, Any]]) -> UserStyle:
        """Analyze user's communication style"""
        return self.style_analyzer.analyze_user_style(conversation_history)

    def get_personalized_threshold(self, user_id: str, conversation_history: List[Dict[str, Any]] = None) -> float:
        """Get personalized threshold for a user"""
        
        # Get existing profile
        profile = self.threshold_db.get_user_profile(user_id)
        
        if profile:
            # Check if we should adjust the threshold
            if conversation_history:
                user_style = self.analyze_user_style(conversation_history)
                if user_style != profile.user_style:
                    # User style changed, recalculate threshold
                    profile.user_style = user_style
                    profile.current_threshold = self._calculate_new_threshold(profile, conversation_history)
                    self.threshold_db.update_user_profile(profile)
            
            return profile.current_threshold
        else:
            # Create new profile
            user_style = self.analyze_user_style(conversation_history) if conversation_history else UserStyle.GENERAL
            style_thresholds = self.style_analyzer.get_style_threshold_mapping(user_style)
            
            new_profile = ThresholdProfile(
                user_id=user_id,
                base_threshold=style_thresholds["base_threshold"],
                current_threshold=style_thresholds["base_threshold"],
                user_style=user_style,
                adjustment_history=[],
                last_adjusted=datetime.now(timezone.utc),
                success_rate=0.7,
                total_adjustments=0
            )
            
            self.threshold_db.update_user_profile(new_profile)
            return new_profile.current_threshold

    def adjust_threshold(self, user_id: str, success_rate: float, 
                        recent_performance: List[float] = None) -> Optional[float]:
        """Adjust user's threshold based on performance"""
        
        profile = self.threshold_db.get_user_profile(user_id)
        if not profile:
            return None

        # Calculate new threshold
        new_threshold = self._calculate_new_threshold(profile, recent_performance or [success_rate])
        
        # Check if adjustment is needed
        if not self.adjustment_engine.should_adjust_threshold(
            profile.current_threshold, new_threshold, profile.last_adjusted
        ):
            return profile.current_threshold

        # Create adjustment record
        adjustment = ThresholdAdjustment(
            adjustment_id=f"adj_{user_id}_{int(datetime.now(timezone.utc).timestamp())}",
            user_id=user_id,
            old_threshold=profile.current_threshold,
            new_threshold=new_threshold,
            adjustment_reason=f"Performance-based adjustment (success rate: {success_rate:.2f})",
            user_style_detected=profile.user_style,
            success_impact=success_rate - profile.success_rate
        )

        # Update profile
        profile.current_threshold = new_threshold
        profile.last_adjusted = datetime.now(timezone.utc)
        profile.success_rate = success_rate
        profile.total_adjustments += 1
        profile.adjustment_history.append({
            "timestamp": adjustment.timestamp.isoformat(),
            "old_threshold": adjustment.old_threshold,
            "new_threshold": adjustment.new_threshold,
            "reason": adjustment.adjustment_reason
        })

        # Store updates
        self.threshold_db.update_user_profile(profile)
        self.threshold_db.store_adjustment(adjustment)

        return new_threshold

    def _calculate_new_threshold(self, profile: ThresholdProfile, 
                                recent_performance: List[float]) -> float:
        """Calculate new threshold using the adjustment engine"""
        return self.adjustment_engine.calculate_threshold_adjustment(
            current_threshold=profile.current_threshold,
            user_style=profile.user_style,
            success_rate=profile.success_rate,
            recent_performance=recent_performance
        )

    def get_threshold_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user's threshold adjustments"""
        profile = self.threshold_db.get_user_profile(user_id)
        if not profile:
            return {"error": "User profile not found"}

        # Get style recommendations
        style_thresholds = self.style_analyzer.get_style_threshold_mapping(profile.user_style)
        
        insights = {
            "current_threshold": profile.current_threshold,
            "base_threshold": profile.base_threshold,
            "user_style": profile.user_style.value,
            "style_recommendation": style_thresholds["base_threshold"],
            "adjustment_history": profile.adjustment_history,
            "total_adjustments": profile.total_adjustments,
            "success_rate": profile.success_rate,
            "last_adjusted": profile.last_adjusted.isoformat(),
            "recommendations": []
        }

        # Generate recommendations
        if profile.current_threshold > style_thresholds["base_threshold"] + 0.1:
            insights["recommendations"].append("Consider lowering threshold to include more context")
        elif profile.current_threshold < style_thresholds["base_threshold"] - 0.1:
            insights["recommendations"].append("Consider raising threshold to focus context selection")

        if profile.total_adjustments > 5:
            insights["recommendations"].append("Frequent adjustments detected - consider reviewing base settings")

        return insights

# Example usage and testing
if __name__ == "__main__":
    manager = DynamicThresholdManager()
    
    # Test conversation history
    test_history = [
        {"user_message": "How do I implement a database connection?"},
        {"user_message": "Can you explain the project structure?"},
        {"user_message": "What were we working on yesterday?"}
    ]
    
    # Test user style analysis
    user_style = manager.analyze_user_style(test_history)
    print(f"🎯 Detected User Style: {user_style.value}")
    
    # Test personalized threshold
    threshold = manager.get_personalized_threshold("test_user", test_history)
    print(f"⚡ Personalized Threshold: {threshold}")
    
    # Test threshold adjustment
    new_threshold = manager.adjust_threshold("test_user", 0.8, [0.7, 0.8, 0.9])
    if new_threshold:
        print(f"🔄 Adjusted Threshold: {new_threshold}")
    
    # Test insights
    insights = manager.get_threshold_insights("test_user")
    print(f"📊 Threshold Insights: {json.dumps(insights, indent=2)}")
