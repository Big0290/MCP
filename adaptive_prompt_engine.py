#!/usr/bin/env python3
"""
Adaptive Prompt Precision Engine (APPE)
========================================

Intelligent system that dynamically crafts the most precise prompts based on:
- Real-time analysis of current task context
- Learning patterns from successful interactions  
- Cursor API compliance while maximizing effectiveness
- Behavioral steering through strategic prompt engineering

This system integrates seamlessly with existing PromptGenerator and context systems
while adding advanced task-aware prompt optimization capabilities.
"""

import re
import json
import time
import hashlib
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

# Import existing systems
try:
    from context_learning_system import ContextLearningSystem
    from smart_caching_system import SmartCachingSystem
    from interaction_logger import InteractionLogger
except ImportError:
    # Fallback for testing
    ContextLearningSystem = None
    SmartCachingSystem = None
    InteractionLogger = None


class TaskType(Enum):
    """Classification of different task types for prompt optimization."""
    CODE_GENERATION = "code_generation"
    DEBUGGING = "debugging" 
    ARCHITECTURE = "architecture"
    LEARNING = "learning"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    OPTIMIZATION = "optimization"
    UNKNOWN = "unknown"


class PromptStrategy(Enum):
    """Different prompt strategies for different contexts."""
    PRECISION_TECHNICAL = "precision_technical"
    CREATIVE_EXPLORATION = "creative_exploration"
    STEP_BY_STEP = "step_by_step"
    PROBLEM_SOLVING = "problem_solving"
    EDUCATIONAL = "educational"
    EFFICIENCY_FOCUSED = "efficiency_focused"
    COMPREHENSIVE = "comprehensive"
    MINIMAL = "minimal"


class BehavioralSteering(Enum):
    """Behavioral steering patterns for AI responses."""
    DETAILED_EXPLANATIONS = "detailed_explanations"
    CONCISE_SOLUTIONS = "concise_solutions"
    PROACTIVE_SUGGESTIONS = "proactive_suggestions"
    REACTIVE_RESPONSES = "reactive_responses"
    TEACHING_MODE = "teaching_mode"
    IMPLEMENTATION_MODE = "implementation_mode"
    ANALYSIS_MODE = "analysis_mode"
    CREATIVE_MODE = "creative_mode"
    STEP_BY_STEP = "step_by_step"


@dataclass
class TaskAnalysis:
    """Analysis results for a user task."""
    task_type: TaskType
    complexity_score: float  # 0.0 to 1.0
    urgency_level: float    # 0.0 to 1.0
    context_requirements: List[str]
    technical_depth: float  # 0.0 to 1.0
    creativity_needed: float # 0.0 to 1.0
    confidence: float       # 0.0 to 1.0
    keywords: List[str]
    estimated_tokens: int


@dataclass
class PromptOptimization:
    """Optimization parameters for prompt generation."""
    strategy: PromptStrategy
    behavioral_steering: List[BehavioralSteering]
    max_tokens: int
    context_priority: List[str]
    enhancement_ratio: float
    cursor_optimizations: Dict[str, Any]


@dataclass
class SuccessPattern:
    """Pattern learned from successful interactions."""
    task_type: TaskType
    strategy: PromptStrategy
    user_feedback: float
    response_quality: float
    execution_time: float
    token_efficiency: float
    success_count: int
    last_used: datetime
    effectiveness_score: float


class TaskClassificationSystem:
    """Intelligent task classification system."""
    
    def __init__(self):
        self.classification_patterns = self._initialize_patterns()
        self.learning_data = {}
        
    def _initialize_patterns(self) -> Dict[TaskType, Dict[str, Any]]:
        """Initialize classification patterns for different task types."""
        return {
            TaskType.CODE_GENERATION: {
                "keywords": ["create", "build", "implement", "write", "generate", "add", "make"],
                "patterns": [r"create.*function", r"build.*class", r"implement.*feature", r"write.*code"],
                "context_clues": ["function", "class", "method", "variable", "algorithm"],
                "complexity_indicators": ["complex", "advanced", "sophisticated", "enterprise"]
            },
            TaskType.DEBUGGING: {
                "keywords": ["fix", "debug", "error", "bug", "issue", "problem", "broken"],
                "patterns": [r"fix.*error", r"debug.*issue", r"solve.*problem", r"error.*fix"],
                "context_clues": ["exception", "traceback", "error message", "not working"],
                "urgency_indicators": ["urgent", "critical", "blocking", "production"]
            },
            TaskType.ARCHITECTURE: {
                "keywords": ["design", "architecture", "structure", "pattern", "system", "scalable"],
                "patterns": [r"design.*system", r"architecture.*for", r"structure.*project"],
                "context_clues": ["scalability", "maintainability", "performance", "design pattern"],
                "complexity_indicators": ["enterprise", "distributed", "microservices", "cloud"]
            },
            TaskType.LEARNING: {
                "keywords": ["learn", "understand", "explain", "how", "what", "why", "teach"],
                "patterns": [r"how.*work", r"what.*is", r"explain.*concept", r"learn.*about"],
                "context_clues": ["concept", "principle", "theory", "fundamentals"],
                "depth_indicators": ["deep dive", "comprehensive", "detailed", "thorough"]
            },
            TaskType.REFACTORING: {
                "keywords": ["refactor", "improve", "optimize", "clean", "reorganize", "restructure"],
                "patterns": [r"refactor.*code", r"improve.*structure", r"optimize.*performance"],
                "context_clues": ["code quality", "maintainability", "performance", "clean code"],
                "scope_indicators": ["entire", "whole", "complete", "comprehensive"]
            },
            TaskType.TESTING: {
                "keywords": ["test", "verify", "validate", "check", "ensure", "confirm"],
                "patterns": [r"test.*function", r"verify.*works", r"validate.*input"],
                "context_clues": ["unit test", "integration", "validation", "assertion"],
                "coverage_indicators": ["comprehensive", "thorough", "complete", "all cases"]
            },
            TaskType.DOCUMENTATION: {
                "keywords": ["document", "comment", "readme", "guide", "manual", "docs"],
                "patterns": [r"document.*code", r"write.*readme", r"create.*guide"],
                "context_clues": ["documentation", "comments", "docstring", "manual"],
                "detail_indicators": ["detailed", "comprehensive", "complete", "thorough"]
            },
            TaskType.ANALYSIS: {
                "keywords": ["analyze", "review", "examine", "investigate", "assess", "evaluate"],
                "patterns": [r"analyze.*code", r"review.*implementation", r"examine.*structure"],
                "context_clues": ["analysis", "review", "assessment", "evaluation"],
                "depth_indicators": ["deep", "thorough", "comprehensive", "detailed"]
            },
            TaskType.PLANNING: {
                "keywords": ["plan", "strategy", "roadmap", "approach", "steps", "workflow"],
                "patterns": [r"plan.*project", r"create.*roadmap", r"define.*strategy"],
                "context_clues": ["planning", "strategy", "roadmap", "milestones"],
                "scope_indicators": ["long-term", "comprehensive", "detailed", "strategic"]
            },
            TaskType.OPTIMIZATION: {
                "keywords": ["optimize", "performance", "speed", "efficiency", "faster", "better"],
                "patterns": [r"optimize.*performance", r"improve.*speed", r"make.*faster"],
                "context_clues": ["performance", "optimization", "efficiency", "speed"],
                "impact_indicators": ["significant", "major", "dramatic", "substantial"]
            }
        }
    
    def analyze_task(self, user_message: str, context: Dict[str, Any]) -> TaskAnalysis:
        """Analyze user message to determine task type and characteristics."""
        message_lower = user_message.lower()
        
        # Calculate scores for each task type
        task_scores = {}
        for task_type, patterns in self.classification_patterns.items():
            score = self._calculate_task_score(message_lower, patterns, context)
            task_scores[task_type] = score
        
        # Determine primary task type
        primary_task = max(task_scores, key=task_scores.get)
        confidence = task_scores[primary_task]
        
        # Calculate other characteristics
        complexity = self._calculate_complexity(message_lower, context)
        urgency = self._calculate_urgency(message_lower, context)
        technical_depth = self._calculate_technical_depth(message_lower, context)
        creativity_needed = self._calculate_creativity_needed(message_lower, context)
        
        # Extract keywords and estimate tokens
        keywords = self._extract_keywords(user_message)
        estimated_tokens = self._estimate_tokens(user_message, context)
        
        # Determine context requirements
        context_requirements = self._determine_context_requirements(primary_task, complexity)
        
        return TaskAnalysis(
            task_type=primary_task,
            complexity_score=complexity,
            urgency_level=urgency,
            context_requirements=context_requirements,
            technical_depth=technical_depth,
            creativity_needed=creativity_needed,
            confidence=confidence,
            keywords=keywords,
            estimated_tokens=estimated_tokens
        )
    
    def _calculate_task_score(self, message: str, patterns: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Calculate score for a specific task type."""
        score = 0.0
        
        # Keyword matching
        keyword_matches = sum(1 for keyword in patterns["keywords"] if keyword in message)
        score += keyword_matches * 0.3
        
        # Pattern matching
        pattern_matches = sum(1 for pattern in patterns["patterns"] if re.search(pattern, message))
        score += pattern_matches * 0.4
        
        # Context clue matching
        context_matches = sum(1 for clue in patterns["context_clues"] if clue in message)
        score += context_matches * 0.2
        
        # Context-based scoring
        if context.get("tech_stack"):
            tech_stack = context["tech_stack"].lower()
            if any(clue in tech_stack for clue in patterns["context_clues"]):
                score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_complexity(self, message: str, context: Dict[str, Any]) -> float:
        """Calculate task complexity score."""
        complexity_indicators = [
            "complex", "advanced", "sophisticated", "enterprise", "distributed",
            "scalable", "comprehensive", "detailed", "thorough", "complete"
        ]
        
        matches = sum(1 for indicator in complexity_indicators if indicator in message)
        base_score = min(matches * 0.2, 0.8)
        
        # Adjust based on context
        if context.get("project_plans"):
            if "comprehensive" in context["project_plans"].lower():
                base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _calculate_urgency(self, message: str, context: Dict[str, Any]) -> float:
        """Calculate task urgency level."""
        urgency_indicators = [
            "urgent", "asap", "quickly", "fast", "immediate", "critical",
            "blocking", "production", "emergency", "now"
        ]
        
        matches = sum(1 for indicator in urgency_indicators if indicator in message)
        return min(matches * 0.3, 1.0)
    
    def _calculate_technical_depth(self, message: str, context: Dict[str, Any]) -> float:
        """Calculate required technical depth."""
        technical_indicators = [
            "implementation", "algorithm", "architecture", "design pattern",
            "performance", "optimization", "scalability", "security"
        ]
        
        matches = sum(1 for indicator in technical_indicators if indicator in message)
        base_score = min(matches * 0.25, 0.8)
        
        # Adjust based on tech stack complexity
        if context.get("tech_stack"):
            tech_complexity = len(context["tech_stack"].split(","))
            base_score += min(tech_complexity * 0.05, 0.2)
        
        return min(base_score, 1.0)
    
    def _calculate_creativity_needed(self, message: str, context: Dict[str, Any]) -> float:
        """Calculate creativity requirement."""
        creativity_indicators = [
            "creative", "innovative", "novel", "unique", "original",
            "brainstorm", "explore", "experiment", "alternative"
        ]
        
        matches = sum(1 for indicator in creativity_indicators if indicator in message)
        return min(matches * 0.3, 1.0)
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Extract important keywords from the message."""
        # Simple keyword extraction - can be enhanced with NLP
        words = re.findall(r'\b\w+\b', message.lower())
        
        # Filter out common words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "have",
            "has", "had", "do", "does", "did", "will", "would", "could", "should"
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords[:10]  # Return top 10 keywords
    
    def _estimate_tokens(self, message: str, context: Dict[str, Any]) -> int:
        """Estimate token count for the enhanced prompt."""
        base_tokens = len(message.split()) * 1.3  # Rough token estimation
        
        # Add context overhead
        if context.get("conversation_summary"):
            base_tokens += len(context["conversation_summary"].split()) * 0.5
        
        if context.get("tech_stack"):
            base_tokens += len(context["tech_stack"].split()) * 0.3
        
        if context.get("project_plans"):
            base_tokens += len(context["project_plans"].split()) * 0.4
        
        return int(base_tokens)
    
    def _determine_context_requirements(self, task_type: TaskType, complexity: float) -> List[str]:
        """Determine what context is needed for this task."""
        base_requirements = ["conversation_summary", "user_preferences"]
        
        if task_type in [TaskType.CODE_GENERATION, TaskType.DEBUGGING, TaskType.REFACTORING]:
            base_requirements.extend(["tech_stack", "project_structure"])
        
        if task_type in [TaskType.ARCHITECTURE, TaskType.PLANNING]:
            base_requirements.extend(["project_plans", "best_practices"])
        
        if task_type == TaskType.LEARNING:
            base_requirements.extend(["educational_context", "examples"])
        
        if complexity > 0.7:
            base_requirements.extend(["comprehensive_context", "detailed_examples"])
        
        return base_requirements


class PromptStrategySelector:
    """Intelligent strategy selection for optimal prompt patterns."""
    
    def __init__(self):
        self.strategy_mappings = self._initialize_strategy_mappings()
        self.success_patterns = {}
    
    def _get_user_behavioral_steering(self) -> List[BehavioralSteering]:
        """Get behavioral steering based on user's dynamic preferences."""
        try:
            from dynamic_instruction_processor import dynamic_processor
            user_prefs = dynamic_processor.user_preferences
            
            # Map user communication style to behavioral steering
            style = user_prefs.communication_preferences.get('style', 'detailed_explanations')
            
            if style == 'concise':
                return [BehavioralSteering.CONCISE_SOLUTIONS]
            elif style == 'detailed_explanations':
                return [BehavioralSteering.DETAILED_EXPLANATIONS]
            elif style == 'teaching':
                return [BehavioralSteering.TEACHING_MODE]
            elif style == 'implementation':
                return [BehavioralSteering.IMPLEMENTATION_MODE]
            else:
                # Default fallback
                return [BehavioralSteering.DETAILED_EXPLANATIONS]
                
        except Exception as e:
            # Fallback to default if dynamic preferences not available
            return [BehavioralSteering.DETAILED_EXPLANATIONS]
        
    def _initialize_strategy_mappings(self) -> Dict[TaskType, Dict[str, Any]]:
        """Initialize strategy mappings for different task types."""
        # Get user's preferred behavioral steering from dynamic preferences
        user_behavioral_steering = self._get_user_behavioral_steering()
        
        return {
            TaskType.CODE_GENERATION: {
                "primary_strategy": PromptStrategy.PRECISION_TECHNICAL,
                "behavioral_steering": [
                    BehavioralSteering.IMPLEMENTATION_MODE,
                    *user_behavioral_steering  # Use user's preferred communication style
                ],
                "context_priority": ["tech_stack", "project_structure", "best_practices"],
                "optimization_focus": "accuracy_and_completeness"
            },
            TaskType.DEBUGGING: {
                "primary_strategy": PromptStrategy.PROBLEM_SOLVING,
                "behavioral_steering": [
                    BehavioralSteering.ANALYSIS_MODE,
                    BehavioralSteering.STEP_BY_STEP,
                    *user_behavioral_steering  # Use user's preferred communication style
                ],
                "context_priority": ["error_context", "tech_stack", "recent_changes"],
                "optimization_focus": "systematic_analysis"
            },
            TaskType.ARCHITECTURE: {
                "primary_strategy": PromptStrategy.COMPREHENSIVE,
                "behavioral_steering": [
                    BehavioralSteering.CREATIVE_MODE,
                    *user_behavioral_steering  # Use user's preferred communication style
                ],
                "context_priority": ["project_plans", "scalability_requirements", "best_practices"],
                "optimization_focus": "strategic_thinking"
            },
            TaskType.LEARNING: {
                "primary_strategy": PromptStrategy.EDUCATIONAL,
                "behavioral_steering": [
                    BehavioralSteering.TEACHING_MODE,
                    *user_behavioral_steering  # Use user's preferred communication style
                ],
                "context_priority": ["educational_context", "examples", "fundamentals"],
                "optimization_focus": "clear_explanations"
            },
            TaskType.REFACTORING: {
                "primary_strategy": PromptStrategy.STEP_BY_STEP,
                "behavioral_steering": [
                    BehavioralSteering.ANALYSIS_MODE,
                    BehavioralSteering.IMPLEMENTATION_MODE
                ],
                "context_priority": ["code_quality", "best_practices", "maintainability"],
                "optimization_focus": "incremental_improvement"
            },
            TaskType.TESTING: {
                "primary_strategy": PromptStrategy.PRECISION_TECHNICAL,
                "behavioral_steering": [
                    *user_behavioral_steering,  # Use user's preferred communication style
                    BehavioralSteering.IMPLEMENTATION_MODE
                ],
                "context_priority": ["test_patterns", "coverage_requirements", "quality_standards"],
                "optimization_focus": "comprehensive_coverage"
            },
            TaskType.DOCUMENTATION: {
                "primary_strategy": PromptStrategy.COMPREHENSIVE,
                "behavioral_steering": [
                    *user_behavioral_steering,  # Use user's preferred communication style
                    BehavioralSteering.TEACHING_MODE
                ],
                "context_priority": ["documentation_standards", "audience", "completeness"],
                "optimization_focus": "clarity_and_completeness"
            },
            TaskType.ANALYSIS: {
                "primary_strategy": PromptStrategy.PROBLEM_SOLVING,
                "behavioral_steering": [
                    BehavioralSteering.ANALYSIS_MODE,
                    *user_behavioral_steering  # Use user's preferred communication style
                ],
                "context_priority": ["analysis_framework", "data_context", "objectives"],
                "optimization_focus": "thorough_analysis"
            },
            TaskType.PLANNING: {
                "primary_strategy": PromptStrategy.COMPREHENSIVE,
                "behavioral_steering": [
                    BehavioralSteering.CREATIVE_MODE,
                    BehavioralSteering.PROACTIVE_SUGGESTIONS
                ],
                "context_priority": ["project_goals", "constraints", "resources"],
                "optimization_focus": "strategic_planning"
            },
            TaskType.OPTIMIZATION: {
                "primary_strategy": PromptStrategy.EFFICIENCY_FOCUSED,
                "behavioral_steering": [
                    BehavioralSteering.ANALYSIS_MODE,
                    BehavioralSteering.IMPLEMENTATION_MODE
                ],
                "context_priority": ["performance_metrics", "bottlenecks", "optimization_targets"],
                "optimization_focus": "performance_improvement"
            }
        }
    
    def select_strategy(self, task_analysis: TaskAnalysis, context: Dict[str, Any]) -> PromptOptimization:
        """Select optimal strategy based on task analysis."""
        task_type = task_analysis.task_type
        
        # Handle unknown task type with a default mapping
        if task_type not in self.strategy_mappings:
            user_behavioral_steering = self._get_user_behavioral_steering()
            base_mapping = {
                "primary_strategy": PromptStrategy.COMPREHENSIVE,
                "behavioral_steering": user_behavioral_steering,  # Use user's preferred communication style
                "context_priority": ["conversation_summary", "user_preferences"],
                "optimization_focus": "balanced_approach"
            }
        else:
            base_mapping = self.strategy_mappings[task_type]
        
        # Get base strategy
        strategy = base_mapping["primary_strategy"]
        behavioral_steering = base_mapping["behavioral_steering"].copy()
        context_priority = base_mapping["context_priority"].copy()
        
        # Adjust based on task characteristics
        if task_analysis.urgency_level > 0.7:
            strategy = PromptStrategy.EFFICIENCY_FOCUSED
            behavioral_steering = [BehavioralSteering.CONCISE_SOLUTIONS]
        
        if task_analysis.complexity_score > 0.8:
            if PromptStrategy.COMPREHENSIVE not in [strategy]:
                strategy = PromptStrategy.COMPREHENSIVE
            # Add user's preferred behavioral steering for complex tasks
            user_behavioral_steering = self._get_user_behavioral_steering()
            for steering in user_behavioral_steering:
                if steering not in behavioral_steering:
                    behavioral_steering.append(steering)
        
        if task_analysis.creativity_needed > 0.6:
            if BehavioralSteering.CREATIVE_MODE not in behavioral_steering:
                behavioral_steering.append(BehavioralSteering.CREATIVE_MODE)
        
        # Calculate token limits
        max_tokens = self._calculate_token_limit(task_analysis, context)
        
        # Calculate enhancement ratio
        enhancement_ratio = self._calculate_enhancement_ratio(task_analysis)
        
        # Cursor-specific optimizations
        cursor_optimizations = self._get_cursor_optimizations(task_analysis, strategy)
        
        return PromptOptimization(
            strategy=strategy,
            behavioral_steering=behavioral_steering,
            max_tokens=max_tokens,
            context_priority=context_priority,
            enhancement_ratio=enhancement_ratio,
            cursor_optimizations=cursor_optimizations
        )
    
    def _calculate_token_limit(self, task_analysis: TaskAnalysis, context: Dict[str, Any]) -> int:
        """Calculate optimal token limit for the prompt."""
        base_limit = 4000  # Conservative base limit for Cursor API
        
        # Adjust based on complexity
        if task_analysis.complexity_score > 0.7:
            base_limit = min(base_limit * 1.5, 6000)
        
        # Adjust based on urgency (urgent tasks get more concise prompts)
        if task_analysis.urgency_level > 0.7:
            base_limit = int(base_limit * 0.7)
        
        # Ensure minimum viable prompt size
        return max(base_limit, 1000)
    
    def _calculate_enhancement_ratio(self, task_analysis: TaskAnalysis) -> float:
        """Calculate how much to enhance the base prompt."""
        base_ratio = 2.0
        
        # Increase for complex tasks
        if task_analysis.complexity_score > 0.7:
            base_ratio += 1.0
        
        # Increase for high technical depth
        if task_analysis.technical_depth > 0.6:
            base_ratio += 0.5
        
        # Decrease for urgent tasks
        if task_analysis.urgency_level > 0.7:
            base_ratio *= 0.7
        
        return min(base_ratio, 4.0)
    
    def _get_cursor_optimizations(self, task_analysis: TaskAnalysis, strategy: PromptStrategy) -> Dict[str, Any]:
        """Get Cursor-specific optimizations."""
        return {
            "response_format": self._get_optimal_response_format(task_analysis.task_type),
            "interaction_style": self._get_interaction_style(strategy),
            "error_handling": self._get_error_handling_approach(task_analysis.urgency_level),
            "token_efficiency": self._get_token_efficiency_settings(task_analysis.estimated_tokens)
        }
    
    def _get_optimal_response_format(self, task_type: TaskType) -> str:
        """Get optimal response format for task type."""
        format_mapping = {
            TaskType.CODE_GENERATION: "structured_code_with_explanations",
            TaskType.DEBUGGING: "step_by_step_analysis",
            TaskType.ARCHITECTURE: "comprehensive_design_document",
            TaskType.LEARNING: "educational_with_examples",
            TaskType.DOCUMENTATION: "structured_documentation",
            TaskType.ANALYSIS: "detailed_analysis_report"
        }
        return format_mapping.get(task_type, "balanced_response")
    
    def _get_interaction_style(self, strategy: PromptStrategy) -> str:
        """Get interaction style based on strategy."""
        style_mapping = {
            PromptStrategy.PRECISION_TECHNICAL: "technical_expert",
            PromptStrategy.EDUCATIONAL: "patient_teacher",
            PromptStrategy.PROBLEM_SOLVING: "analytical_consultant",
            PromptStrategy.CREATIVE_EXPLORATION: "creative_collaborator",
            PromptStrategy.EFFICIENCY_FOCUSED: "efficient_assistant"
        }
        return style_mapping.get(strategy, "balanced_assistant")
    
    def _get_error_handling_approach(self, urgency_level: float) -> str:
        """Get error handling approach based on urgency."""
        if urgency_level > 0.7:
            return "immediate_solutions"
        elif urgency_level > 0.4:
            return "balanced_approach"
        else:
            return "comprehensive_analysis"
    
    def _get_token_efficiency_settings(self, estimated_tokens: int) -> Dict[str, Any]:
        """Get token efficiency settings."""
        return {
            "compression_level": "high" if estimated_tokens > 3000 else "medium",
            "context_prioritization": True,
            "redundancy_removal": True,
            "smart_truncation": estimated_tokens > 4000
        }


class PrecisionPromptCrafter:
    """Crafts precision-targeted prompts with behavioral steering."""
    
    def __init__(self):
        self.behavioral_templates = self._initialize_behavioral_templates()
        self.optimization_patterns = self._initialize_optimization_patterns()
        
    def _initialize_behavioral_templates(self) -> Dict[BehavioralSteering, str]:
        """Initialize behavioral steering templates."""
        return {
            BehavioralSteering.DETAILED_EXPLANATIONS: """
Provide comprehensive, detailed explanations for each step and decision.
Include reasoning, alternatives considered, and potential implications.
""",
            BehavioralSteering.CONCISE_SOLUTIONS: """
Focus on efficient, direct solutions with minimal explanation.
Prioritize actionable results over detailed reasoning.
""",
            BehavioralSteering.PROACTIVE_SUGGESTIONS: """
Anticipate follow-up questions and provide proactive recommendations.
Suggest improvements, alternatives, and next steps.
""",
            BehavioralSteering.TEACHING_MODE: """
Explain concepts clearly with examples and analogies.
Build understanding progressively from fundamentals.
""",
            BehavioralSteering.IMPLEMENTATION_MODE: """
Focus on practical implementation with working code.
Provide complete, runnable solutions with error handling.
""",
            BehavioralSteering.ANALYSIS_MODE: """
Provide systematic analysis with clear methodology.
Break down complex problems into manageable components.
""",
            BehavioralSteering.CREATIVE_MODE: """
Explore innovative approaches and alternative solutions.
Consider unconventional methods and creative possibilities.
""",
            BehavioralSteering.STEP_BY_STEP: """
Break down complex tasks into clear, sequential steps.
Provide systematic, methodical approach to problem solving.
"""
        }
    
    def _initialize_optimization_patterns(self) -> Dict[PromptStrategy, str]:
        """Initialize optimization patterns for different strategies."""
        return {
            PromptStrategy.PRECISION_TECHNICAL: """
Focus on technical accuracy, best practices, and implementation details.
Ensure code quality, performance considerations, and maintainability.
""",
            PromptStrategy.PROBLEM_SOLVING: """
Apply systematic problem-solving methodology.
Identify root causes, evaluate solutions, and provide clear action plans.
""",
            PromptStrategy.EDUCATIONAL: """
Structure information for optimal learning and understanding.
Use progressive disclosure and reinforce key concepts.
""",
            PromptStrategy.COMPREHENSIVE: """
Provide thorough coverage of all relevant aspects.
Consider multiple perspectives and long-term implications.
""",
            PromptStrategy.EFFICIENCY_FOCUSED: """
Optimize for speed and efficiency in both process and outcome.
Minimize overhead while maximizing value delivery.
"""
        }
    
    def craft_precision_prompt(
        self, 
        user_message: str, 
        context: Dict[str, Any], 
        optimization: PromptOptimization,
        task_analysis: TaskAnalysis
    ) -> str:
        """Craft a precision-targeted prompt with behavioral steering and comprehensive context."""
        
        # Build the enhanced prompt structure
        prompt_sections = []
        
        # Add strategy-specific optimization
        strategy_guidance = self.optimization_patterns.get(
            optimization.strategy, 
            "Provide balanced, helpful assistance."
        )
        prompt_sections.append(f"=== 🎯 STRATEGY GUIDANCE ===\n{strategy_guidance}")
        
        # Add behavioral steering
        if optimization.behavioral_steering:
            behavioral_guidance = []
            for steering in optimization.behavioral_steering:
                template = self.behavioral_templates.get(steering, "")
                if template:
                    behavioral_guidance.append(template.strip())
            
            if behavioral_guidance:
                prompt_sections.append(
                    f"=== 🧠 BEHAVIORAL GUIDANCE ===\n" + 
                    "\n".join(behavioral_guidance)
                )
        
        # Add task-specific context
        task_context = self._build_task_context(task_analysis, context, optimization)
        if task_context:
            prompt_sections.append(f"=== 📋 TASK CONTEXT ===\n{task_context}")
        
        # 🚀 NEW: Add previous steps and interaction summary
        previous_steps = self._build_previous_steps_summary(context, task_analysis)
        if previous_steps:
            prompt_sections.append(f"=== 📋 PREVIOUS STEPS SUMMARY ===\n{previous_steps}")
        
        # 🚀 NEW: Add comprehensive context injection (like the original system)
        comprehensive_context = self._build_comprehensive_context(context)
        if comprehensive_context:
            prompt_sections.append(f"=== 📊 COMPREHENSIVE CONTEXT ===\n{comprehensive_context}")
        
        # Add Cursor-specific optimizations
        cursor_guidance = self._build_cursor_guidance(optimization.cursor_optimizations)
        if cursor_guidance:
            prompt_sections.append(f"=== ⚙️ RESPONSE OPTIMIZATION ===\n{cursor_guidance}")
        
        # Add the original user message
        prompt_sections.append(f"=== 💬 USER REQUEST ===\n{user_message}")
        
        # Combine all sections
        enhanced_prompt = "\n\n".join(prompt_sections)
        
        # Apply token optimization if needed
        if len(enhanced_prompt.split()) > optimization.max_tokens:
            enhanced_prompt = self._optimize_token_usage(enhanced_prompt, optimization.max_tokens)
        
        return enhanced_prompt
    
    def _build_task_context(
        self, 
        task_analysis: TaskAnalysis, 
        context: Dict[str, Any], 
        optimization: PromptOptimization
    ) -> str:
        """Build task-specific context information."""
        context_parts = []
        
        # Task type and characteristics
        context_parts.append(f"Task Type: {task_analysis.task_type.value}")
        context_parts.append(f"Complexity: {task_analysis.complexity_score:.1f}/1.0")
        context_parts.append(f"Technical Depth: {task_analysis.technical_depth:.1f}/1.0")
        
        if task_analysis.urgency_level > 0.3:
            context_parts.append(f"Urgency: {task_analysis.urgency_level:.1f}/1.0 - Prioritize efficiency")
        
        if task_analysis.creativity_needed > 0.3:
            context_parts.append(f"Creativity Needed: {task_analysis.creativity_needed:.1f}/1.0")
        
        # Key requirements
        if task_analysis.context_requirements:
            context_parts.append(f"Required Context: {', '.join(task_analysis.context_requirements)}")
        
        return "\n".join(context_parts)
    
    def _build_prioritized_context(self, context: Dict[str, Any], priority_list: List[str]) -> str:
        """Build context based on priority list."""
        context_sections = []
        
        for priority_item in priority_list:
            if priority_item in context and context[priority_item]:
                # Truncate long context items
                content = str(context[priority_item])
                if len(content) > 500:
                    content = content[:500] + "..."
                
                context_sections.append(f"{priority_item.replace('_', ' ').title()}: {content}")
        
        return "\n".join(context_sections)
    
    def _build_comprehensive_context(self, context: Dict[str, Any]) -> str:
        """Build comprehensive context like the original system (NO truncation)."""
        context_sections = []
        
        # 🎯 CONVERSATION SUMMARY
        if context.get('conversation_summary'):
            context_sections.append(f"🎯 CONVERSATION SUMMARY:\n{context['conversation_summary']}")
        
        # 📝 ACTION HISTORY  
        if context.get('action_history'):
            context_sections.append(f"📝 ACTION HISTORY:\n{context['action_history']}")
        
        # ⚙️ TECH STACK
        if context.get('tech_stack'):
            context_sections.append(f"⚙️ TECH STACK:\n{context['tech_stack']}")
        
        # 🎯 PROJECT PLANS & OBJECTIVES
        if context.get('project_plans'):
            context_sections.append(f"🎯 PROJECT PLANS & OBJECTIVES:\n{context['project_plans']}")
        
        # 👤 USER PREFERENCES
        if context.get('user_preferences'):
            context_sections.append(f"👤 USER PREFERENCES:\n{context['user_preferences']}")
        
        # 🤖 AGENT METADATA
        if context.get('agent_metadata'):
            context_sections.append(f"🤖 AGENT METADATA:\n{context['agent_metadata']}")
        
        # 🔍 PROJECT PATTERNS
        if context.get('project_patterns'):
            patterns = context['project_patterns']
            if isinstance(patterns, list):
                pattern_text = '\n'.join(f"• {pattern}" for pattern in patterns)
            else:
                pattern_text = str(patterns)
            context_sections.append(f"🔍 PROJECT PATTERNS:\n{pattern_text}")
        
        # 📁 SMART PROJECT STRUCTURE (NEW: Intelligent, context-aware file analysis)
        # Create a mock task analysis for this context since we don't have the real one
        try:
            smart_structure = self._build_smart_project_structure(context, None)
            if smart_structure:
                context_sections.append(f"📁 RELEVANT PROJECT FILES:\n{smart_structure}")
        except Exception as e:
            # Skip smart structure if there's an error
            pass
        
        # ✅ BEST PRACTICES
        if context.get('best_practices'):
            practices = context['best_practices']
            if isinstance(practices, list):
                practice_text = '\n'.join(f"• {practice}" for practice in practices)
            else:
                practice_text = str(practices)
            context_sections.append(f"✅ BEST PRACTICES:\n{practice_text}")
        
        # ⚠️ COMMON ISSUES & SOLUTIONS
        if context.get('common_issues'):
            issues = context['common_issues']
            if isinstance(issues, list):
                issue_text = '\n'.join(f"• {issue}" for issue in issues)
            else:
                issue_text = str(issues)
            context_sections.append(f"⚠️ COMMON ISSUES & SOLUTIONS:\n{issue_text}")
        
        # 🔄 DEVELOPMENT WORKFLOW
        if context.get('development_workflow'):
            context_sections.append(f"🔄 DEVELOPMENT WORKFLOW:\n{context['development_workflow']}")
        
        return "\n\n".join(context_sections)
    
    def _build_previous_steps_summary(self, context: Dict[str, Any], task_analysis: TaskAnalysis) -> str:
        """Build a summary of previous steps and interactions."""
        summary_sections = []
        
        # Extract recent actions from action history
        action_history = context.get('action_history', '')
        if action_history:
            # Parse recent actions to identify key steps
            recent_actions = []
            lines = action_history.split('\n')
            for line in lines[:10]:  # Get last 10 actions
                if line.strip() and ':' in line:
                    # Extract action type and brief description
                    if 'conversation_turn:' in line:
                        action_desc = line.split('conversation_turn:')[1].split('(')[0].strip()
                        if len(action_desc) > 50:
                            action_desc = action_desc[:50] + "..."
                        recent_actions.append(f"💬 User: {action_desc}")
                    elif 'agent_response:' in line and 'No request content' not in line:
                        action_desc = line.split('agent_response:')[1].split('(')[0].strip()
                        if len(action_desc) > 50:
                            action_desc = action_desc[:50] + "..."
                        recent_actions.append(f"🤖 Agent: {action_desc}")
                    elif 'client_request:' in line:
                        action_desc = line.split('client_request:')[1].split('(')[0].strip()
                        if len(action_desc) > 50:
                            action_desc = action_desc[:50] + "..."
                        recent_actions.append(f"📝 Request: {action_desc}")
            
            if recent_actions:
                summary_sections.append("🔄 Recent Interaction Flow:")
                summary_sections.extend(recent_actions[-5:])  # Show last 5 actions
        
        # Add task progression context
        task_type = task_analysis.task_type.value if hasattr(task_analysis.task_type, 'value') else str(task_analysis.task_type)
        
        # Infer current phase based on task type and context
        current_phase = self._infer_current_phase(task_type, context)
        if current_phase:
            summary_sections.append(f"\n🎯 Current Phase: {current_phase}")
        
        # Add completion status of key objectives
        project_plans = context.get('project_plans', '')
        if project_plans and '✅' in project_plans:
            completed_items = []
            for line in project_plans.split('\n'):
                if '✅' in line:
                    item = line.replace('✅', '').strip()
                    if len(item) > 60:
                        item = item[:60] + "..."
                    completed_items.append(f"✅ {item}")
            
            if completed_items:
                summary_sections.append("\n📋 Recently Completed:")
                summary_sections.extend(completed_items[-3:])  # Show last 3 completed items
        
        # Add next logical steps based on task analysis
        next_steps = self._suggest_next_steps(task_type, context)
        if next_steps:
            summary_sections.append(f"\n🚀 Suggested Next Steps:")
            summary_sections.extend([f"• {step}" for step in next_steps])
        
        return "\n".join(summary_sections)
    
    def _infer_current_phase(self, task_type: str, context: Dict[str, Any]) -> str:
        """Infer the current phase of work based on task type and context."""
        phase_mapping = {
            'code_generation': 'Implementation Phase',
            'debugging': 'Debugging & Testing Phase', 
            'testing': 'Quality Assurance Phase',
            'architecture': 'Design & Planning Phase',
            'documentation': 'Documentation Phase',
            'optimization': 'Performance Optimization Phase',
            'deployment': 'Deployment & Release Phase',
            'learning': 'Knowledge Building Phase',
            'analysis': 'Analysis & Research Phase',
            'maintenance': 'Maintenance & Updates Phase'
        }
        return phase_mapping.get(task_type, 'Active Development Phase')
    
    def _suggest_next_steps(self, task_type: str, context: Dict[str, Any]) -> List[str]:
        """Suggest logical next steps based on current task and context."""
        next_steps_mapping = {
            'code_generation': [
                'Test the generated code',
                'Add error handling and validation',
                'Update documentation'
            ],
            'debugging': [
                'Verify the fix works correctly',
                'Add regression tests',
                'Update related documentation'
            ],
            'testing': [
                'Run comprehensive test suite',
                'Check edge cases and error conditions',
                'Validate performance metrics'
            ],
            'architecture': [
                'Create implementation plan',
                'Design system interfaces',
                'Plan testing strategy'
            ],
            'documentation': [
                'Review for completeness',
                'Add usage examples',
                'Update related documentation'
            ],
            'optimization': [
                'Measure performance improvements',
                'Test under different conditions',
                'Document optimization techniques'
            ]
        }
        
        base_steps = next_steps_mapping.get(task_type, [
            'Continue with current implementation',
            'Test and validate changes',
            'Update documentation as needed'
        ])
        
        # Add context-specific suggestions
        if 'APPE' in context.get('conversation_summary', ''):
            base_steps.append('Consider APPE system enhancements')
        
        return base_steps[:3]  # Return top 3 suggestions
    
    def _build_smart_project_structure(self, context: Dict[str, Any], task_analysis: Optional[TaskAnalysis]) -> str:
        """Build intelligent, context-aware project structure information."""
        structure_sections = []
        
        # Get project structure from context
        project_structure = context.get('project_structure', {})
        if not project_structure:
            return ""
        
        # Extract task-relevant information
        if task_analysis:
            task_type = task_analysis.task_type.value if hasattr(task_analysis.task_type, 'value') else str(task_analysis.task_type)
        else:
            # Default to code_generation if no task analysis available
            task_type = 'code_generation'
        
        # Define file relevance patterns based on task type
        relevance_patterns = {
            'code_generation': ['.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs', '.java'],
            'debugging': ['.py', '.log', 'test_', 'debug_', '.js', '.ts'],
            'testing': ['test_', '_test', '.test.', 'spec_', '.spec.'],
            'documentation': ['.md', '.rst', '.txt', 'README', 'CHANGELOG'],
            'architecture': ['.py', '.md', 'config', 'requirements', 'setup'],
            'deployment': ['docker', 'deploy', '.yml', '.yaml', '.json', 'requirements'],
            'optimization': ['.py', 'performance', 'benchmark', 'profile']
        }
        
        # Get relevant patterns for current task
        relevant_extensions = relevance_patterns.get(task_type, ['.py', '.md', '.json'])
        
        # Extract key files from project structure
        key_files = []
        total_files = 0
        
        if isinstance(project_structure, dict) and 'directories' in project_structure:
            directories = project_structure['directories']
            
            # Process root directory
            if 'root' in directories:
                root_info = directories['root']
                if 'files' in root_info:
                    files = root_info['files']
                    total_files = len(files)
                    
                    # Filter files by relevance
                    for file in files[:50]:  # Limit to first 50 files to avoid overwhelming
                        if any(pattern in file.lower() for pattern in relevant_extensions):
                            key_files.append(f"• {file}")
                        elif any(keyword in file.lower() for keyword in ['main', 'app', 'server', 'client', 'api', 'core']):
                            key_files.append(f"• {file} (core)")
                        elif file.lower() in ['readme.md', 'requirements.txt', 'package.json', 'pyproject.toml']:
                            key_files.append(f"• {file} (config)")
        
        # Build smart summary
        if key_files:
            structure_sections.append(f"📊 Project Overview: {total_files} total files")
            structure_sections.append(f"🎯 Task-Relevant Files ({task_type}):")
            structure_sections.extend(key_files[:15])  # Show top 15 relevant files
            
            if len(key_files) > 15:
                structure_sections.append(f"... and {len(key_files) - 15} more relevant files")
        
        # Add context-specific insights
        insights = self._extract_project_insights(key_files, task_type)
        if insights:
            structure_sections.append(f"\n🔍 Project Insights:")
            structure_sections.extend([f"• {insight}" for insight in insights])
        
        return "\n".join(structure_sections)
    
    def _extract_project_insights(self, files: List[str], task_type: str) -> List[str]:
        """Extract intelligent insights from project files."""
        insights = []
        
        # Count file types
        file_types = {}
        for file in files:
            if '.py' in file:
                file_types['Python'] = file_types.get('Python', 0) + 1
            elif '.js' in file or '.ts' in file:
                file_types['JavaScript/TypeScript'] = file_types.get('JavaScript/TypeScript', 0) + 1
            elif 'test_' in file or '_test' in file:
                file_types['Tests'] = file_types.get('Tests', 0) + 1
            elif '.md' in file:
                file_types['Documentation'] = file_types.get('Documentation', 0) + 1
        
        # Generate insights based on file analysis
        if file_types.get('Python', 0) > 5:
            insights.append("Python-heavy project with multiple modules")
        
        if file_types.get('Tests', 0) > 3:
            insights.append("Well-tested codebase with comprehensive test suite")
        
        if file_types.get('Documentation', 0) > 2:
            insights.append("Well-documented project with multiple README files")
        
        # Task-specific insights
        if task_type == 'testing' and file_types.get('Tests', 0) > 0:
            insights.append(f"Found {file_types['Tests']} test files for testing tasks")
        elif task_type == 'code_generation' and file_types.get('Python', 0) > 0:
            insights.append(f"Python environment ready for code generation")
        
        return insights[:3]  # Return top 3 insights
    
    def _build_cursor_guidance(self, cursor_optimizations: Dict[str, Any]) -> str:
        """Build Cursor-specific guidance."""
        guidance_parts = []
        
        response_format = cursor_optimizations.get("response_format")
        if response_format:
            guidance_parts.append(f"Response Format: {response_format}")
        
        interaction_style = cursor_optimizations.get("interaction_style")
        if interaction_style:
            guidance_parts.append(f"Interaction Style: {interaction_style}")
        
        error_handling = cursor_optimizations.get("error_handling")
        if error_handling:
            guidance_parts.append(f"Error Handling: {error_handling}")
        
        token_efficiency = cursor_optimizations.get("token_efficiency", {})
        if token_efficiency.get("compression_level"):
            guidance_parts.append(f"Compression: {token_efficiency['compression_level']}")
        
        return "\n".join(guidance_parts)
    
    def _optimize_token_usage(self, prompt: str, max_tokens: int) -> str:
        """Optimize prompt to fit within token limits."""
        words = prompt.split()
        current_tokens = len(words)
        
        if current_tokens <= max_tokens:
            return prompt
        
        # Calculate reduction needed
        reduction_ratio = max_tokens / current_tokens
        
        # Split into sections
        sections = prompt.split("=== ")
        optimized_sections = []
        
        for section in sections:
            if not section.strip():
                continue
                
            # Keep headers but reduce content
            lines = section.split("\n")
            if len(lines) > 1:
                header = lines[0]
                content = "\n".join(lines[1:])
                
                # Reduce content proportionally
                content_words = content.split()
                target_words = int(len(content_words) * reduction_ratio)
                
                if target_words > 0:
                    reduced_content = " ".join(content_words[:target_words])
                    optimized_sections.append(f"=== {header}\n{reduced_content}")
            else:
                optimized_sections.append(f"=== {section}")
        
        return "\n\n".join(optimized_sections)


class SuccessPatternLearner:
    """Learns from interaction outcomes to improve future prompts."""
    
    def __init__(self, data_file: str = "data/success_patterns.json"):
        self.data_file = data_file
        self.patterns = self._load_patterns()
        
    def _load_patterns(self) -> Dict[str, SuccessPattern]:
        """Load success patterns from storage."""
        try:
            import os
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    patterns = {}
                    for key, pattern_data in data.items():
                        # Convert string values back to enums
                        pattern_data['task_type'] = TaskType(pattern_data['task_type'])
                        pattern_data['strategy'] = PromptStrategy(pattern_data['strategy'])
                        # Convert datetime string back to datetime object
                        pattern_data['last_used'] = datetime.fromisoformat(pattern_data['last_used'])
                        patterns[key] = SuccessPattern(**pattern_data)
                    return patterns
        except Exception as e:
            print(f"Warning: Could not load success patterns: {e}")
        
        return {}
    
    def _save_patterns(self):
        """Save success patterns to storage."""
        try:
            import os
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Convert patterns to serializable format
            data = {}
            for key, pattern in self.patterns.items():
                pattern_dict = asdict(pattern)
                # Convert enum values to strings
                pattern_dict['task_type'] = pattern.task_type.value
                pattern_dict['strategy'] = pattern.strategy.value
                pattern_dict['last_used'] = pattern.last_used.isoformat()
                data[key] = pattern_dict
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save success patterns: {e}")
    
    def learn_from_interaction(
        self,
        task_analysis: TaskAnalysis,
        optimization: PromptOptimization,
        user_feedback: float,
        response_quality: float,
        execution_time: float
    ):
        """Learn from an interaction outcome."""
        pattern_key = f"{task_analysis.task_type.value}_{optimization.strategy.value}"
        
        # Calculate metrics
        token_efficiency = self._calculate_token_efficiency(task_analysis, execution_time)
        effectiveness_score = self._calculate_effectiveness_score(
            user_feedback, response_quality, token_efficiency
        )
        
        if pattern_key in self.patterns:
            # Update existing pattern
            pattern = self.patterns[pattern_key]
            pattern.success_count += 1
            pattern.user_feedback = (pattern.user_feedback + user_feedback) / 2
            pattern.response_quality = (pattern.response_quality + response_quality) / 2
            pattern.execution_time = (pattern.execution_time + execution_time) / 2
            pattern.token_efficiency = (pattern.token_efficiency + token_efficiency) / 2
            pattern.effectiveness_score = effectiveness_score
            pattern.last_used = datetime.now()
        else:
            # Create new pattern
            self.patterns[pattern_key] = SuccessPattern(
                task_type=task_analysis.task_type,
                strategy=optimization.strategy,
                user_feedback=user_feedback,
                response_quality=response_quality,
                execution_time=execution_time,
                token_efficiency=token_efficiency,
                success_count=1,
                last_used=datetime.now(),
                effectiveness_score=effectiveness_score
            )
        
        self._save_patterns()
    
    def get_optimal_strategy(self, task_type: TaskType) -> Optional[PromptStrategy]:
        """Get the most effective strategy for a task type."""
        relevant_patterns = [
            pattern for pattern in self.patterns.values()
            if pattern.task_type == task_type
        ]
        
        if not relevant_patterns:
            return None
        
        # Find pattern with highest effectiveness score
        best_pattern = max(relevant_patterns, key=lambda p: p.effectiveness_score)
        return best_pattern.strategy
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from learned patterns."""
        if not self.patterns:
            return {"message": "No learning data available yet"}
        
        insights = {
            "total_patterns": len(self.patterns),
            "most_effective_strategies": {},
            "task_type_performance": {},
            "recent_improvements": []
        }
        
        # Analyze by task type
        task_performance = {}
        for pattern in self.patterns.values():
            task_type = pattern.task_type.value
            if task_type not in task_performance:
                task_performance[task_type] = []
            task_performance[task_type].append(pattern.effectiveness_score)
        
        for task_type, scores in task_performance.items():
            insights["task_type_performance"][task_type] = {
                "average_effectiveness": sum(scores) / len(scores),
                "pattern_count": len(scores)
            }
        
        # Find most effective strategies
        strategy_performance = {}
        for pattern in self.patterns.values():
            strategy = pattern.strategy.value
            if strategy not in strategy_performance:
                strategy_performance[strategy] = []
            strategy_performance[strategy].append(pattern.effectiveness_score)
        
        for strategy, scores in strategy_performance.items():
            insights["most_effective_strategies"][strategy] = sum(scores) / len(scores)
        
        return insights
    
    def _calculate_token_efficiency(self, task_analysis: TaskAnalysis, execution_time: float) -> float:
        """Calculate token efficiency score."""
        if execution_time == 0:
            return 0.5
        
        # Simple efficiency calculation - can be enhanced
        base_efficiency = min(1.0, 10.0 / execution_time)  # Faster is better
        
        # Adjust for estimated tokens
        if task_analysis.estimated_tokens > 0:
            token_factor = min(1.0, 1000.0 / task_analysis.estimated_tokens)
            base_efficiency = (base_efficiency + token_factor) / 2
        
        return base_efficiency
    
    def _calculate_effectiveness_score(
        self, 
        user_feedback: float, 
        response_quality: float, 
        token_efficiency: float
    ) -> float:
        """Calculate overall effectiveness score."""
        # Weighted combination of metrics
        weights = {
            "user_feedback": 0.4,
            "response_quality": 0.4,
            "token_efficiency": 0.2
        }
        
        score = (
            user_feedback * weights["user_feedback"] +
            response_quality * weights["response_quality"] +
            token_efficiency * weights["token_efficiency"]
        )
        
        return min(score, 1.0)


class AdaptivePromptEngine:
    """Main Adaptive Prompt Precision Engine class."""
    
    def __init__(self):
        self.task_classifier = TaskClassificationSystem()
        self.strategy_selector = PromptStrategySelector()
        self.prompt_crafter = PrecisionPromptCrafter()
        self.pattern_learner = SuccessPatternLearner()
        
        # Integration with existing systems
        self.context_learning = None
        self.smart_cache = None
        self.interaction_logger = None
        
        # Performance tracking
        self.stats = {
            "prompts_generated": 0,
            "average_processing_time": 0.0,
            "success_rate": 0.0,
            "cache_hit_rate": 0.0
        }
        
        self._initialize_integrations()
    
    def _initialize_integrations(self):
        """Initialize integrations with existing systems."""
        try:
            if ContextLearningSystem:
                self.context_learning = ContextLearningSystem(learning_enabled=True)
            if SmartCachingSystem:
                self.smart_cache = SmartCachingSystem()
            if InteractionLogger:
                self.interaction_logger = InteractionLogger()
        except Exception as e:
            print(f"Warning: Could not initialize all integrations: {e}")
    
    def generate_optimal_prompt(
        self, 
        user_message: str, 
        full_context: Dict[str, Any],
        force_refresh: bool = False
    ) -> str:
        """Generate an optimal prompt using the APPE system."""
        start_time = time.time()
        
        try:
            # Check cache first (unless force refresh)
            if not force_refresh and self.smart_cache:
                cache_key = self._generate_cache_key(user_message, full_context)
                cached_result = self.smart_cache.get(cache_key, "adaptive_prompt")
                if cached_result:
                    self._update_stats("cache_hit")
                    return cached_result
            
            # Step 1: Classify the task
            task_analysis = self.task_classifier.analyze_task(user_message, full_context)
            
            # Step 2: Select optimal strategy
            optimization = self.strategy_selector.select_strategy(task_analysis, full_context)
            
            # Check for learned patterns
            learned_strategy = self.pattern_learner.get_optimal_strategy(task_analysis.task_type)
            if learned_strategy and learned_strategy != optimization.strategy:
                # Use learned strategy if it's significantly better
                optimization.strategy = learned_strategy
            
            # Step 3: Craft precision prompt
            enhanced_prompt = self.prompt_crafter.craft_precision_prompt(
                user_message, full_context, optimization, task_analysis
            )
            
            # Cache the result
            if self.smart_cache:
                cache_key = self._generate_cache_key(user_message, full_context)
                self.smart_cache.put(
                    cache_key, 
                    enhanced_prompt, 
                    "adaptive_prompt",
                    optimization.enhancement_ratio,
                    0.8,  # Default feedback
                    0.8   # Default quality
                )
            
            # Update statistics
            processing_time = time.time() - start_time
            self._update_stats("success", processing_time)
            
            return enhanced_prompt
            
        except Exception as e:
            print(f"Error in APPE generation: {e}")
            # Fallback to basic enhancement
            return self._generate_fallback_prompt(user_message, full_context)
    
    def learn_from_interaction_outcome(
        self,
        user_message: str,
        enhanced_prompt: str,
        user_feedback: float,
        response_quality: float,
        execution_time: float
    ):
        """Learn from interaction outcomes to improve future prompts."""
        try:
            # Re-analyze the task to get the same classification
            task_analysis = self.task_classifier.analyze_task(user_message, {})
            
            # Determine what optimization was used (simplified)
            optimization = self.strategy_selector.select_strategy(task_analysis, {})
            
            # Learn from the outcome
            self.pattern_learner.learn_from_interaction(
                task_analysis, optimization, user_feedback, response_quality, execution_time
            )
            
            # Update context learning system if available
            if self.context_learning:
                self.context_learning.learn_from_interaction(
                    user_message, enhanced_prompt, "adaptive", user_feedback, response_quality
                )
            
        except Exception as e:
            print(f"Error in learning from interaction: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        status = {
            "appe_version": "1.0.0",
            "status": "active",
            "statistics": self.stats.copy(),
            "learning_insights": self.pattern_learner.get_learning_insights(),
            "integrations": {
                "context_learning": self.context_learning is not None,
                "smart_cache": self.smart_cache is not None,
                "interaction_logger": self.interaction_logger is not None
            }
        }
        
        return status
    
    def _generate_cache_key(self, user_message: str, context: Dict[str, Any]) -> str:
        """Generate cache key for the prompt."""
        # Create a hash of the message and relevant context
        context_str = json.dumps({
            k: str(v)[:100] for k, v in context.items() 
            if k in ["tech_stack", "project_plans", "user_preferences"]
        }, sort_keys=True)
        
        combined = f"{user_message}:{context_str}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _update_stats(self, event_type: str, processing_time: float = 0.0):
        """Update performance statistics."""
        if event_type == "success":
            self.stats["prompts_generated"] += 1
            # Update average processing time
            current_avg = self.stats["average_processing_time"]
            count = self.stats["prompts_generated"]
            self.stats["average_processing_time"] = (
                (current_avg * (count - 1) + processing_time) / count
            )
        elif event_type == "cache_hit":
            # Update cache hit rate calculation would go here
            pass
    
    def _generate_fallback_prompt(self, user_message: str, context: Dict[str, Any]) -> str:
        """Generate a fallback prompt when APPE fails."""
        return f"""
=== 🔄 FALLBACK PROMPT ENHANCEMENT ===

The Adaptive Prompt Precision Engine encountered an issue, but I'll still provide enhanced assistance.

=== 💬 USER REQUEST ===
{user_message}

=== 🔍 AVAILABLE CONTEXT ===
{json.dumps({k: str(v)[:200] for k, v in context.items()}, indent=2)}

Please provide comprehensive assistance based on the available context.
"""


# Global instance for easy access
_appe_instance = None

def get_adaptive_prompt_engine() -> AdaptivePromptEngine:
    """Get or create the global APPE instance."""
    global _appe_instance
    if _appe_instance is None:
        _appe_instance = AdaptivePromptEngine()
    return _appe_instance


# Integration functions for existing systems
def enhance_prompt_with_appe(user_message: str, context: Dict[str, Any]) -> str:
    """Enhanced prompt generation using APPE."""
    appe = get_adaptive_prompt_engine()
    return appe.generate_optimal_prompt(user_message, context)


def learn_from_appe_interaction(
    user_message: str,
    enhanced_prompt: str, 
    user_feedback: float,
    response_quality: float,
    execution_time: float
):
    """Learn from APPE interaction outcomes."""
    appe = get_adaptive_prompt_engine()
    appe.learn_from_interaction_outcome(
        user_message, enhanced_prompt, user_feedback, response_quality, execution_time
    )


if __name__ == "__main__":
    # Test the APPE system
    appe = AdaptivePromptEngine()
    
    test_message = "Create a Python function to handle user authentication with JWT tokens"
    test_context = {
        "tech_stack": "Python, FastAPI, SQLAlchemy, JWT",
        "project_plans": "Building a secure web API",
        "user_preferences": "Prefer comprehensive solutions with error handling"
    }
    
    enhanced_prompt = appe.generate_optimal_prompt(test_message, test_context)
    print("Enhanced Prompt:")
    print("=" * 80)
    print(enhanced_prompt)
    print("=" * 80)
    
    # Test learning
    appe.learn_from_interaction_outcome(
        test_message, enhanced_prompt, 0.9, 0.8, 2.5
    )
    
    print("\nSystem Status:")
    print(json.dumps(appe.get_system_status(), indent=2, default=str))
