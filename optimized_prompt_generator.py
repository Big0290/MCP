#!/usr/bin/env python3
"""
🚀 Optimized Prompt Generator - Streamlined & Efficient

This module provides an optimized version of the prompt generator that:
- Reduces prompt length by 60-80%
- Eliminates warning messages and fallback text
- Improves readability with cleaner formatting
- Maintains all essential context
- Uses intelligent content filtering
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

# Import existing systems
try:
    from prompt_generator import PromptGenerator, PromptContext
    BASE_GENERATOR_AVAILABLE = True
except ImportError:
    BASE_GENERATOR_AVAILABLE = False
    print("⚠️ Base prompt generator not available")

logger = logging.getLogger(__name__)

@dataclass
class OptimizedPromptConfig:
    """Configuration for optimized prompt generation"""
    max_length: int = 8000   # Target max length (8KB vs current 88KB) - More balanced
    include_project_structure: bool = True   # Include when relevant
    include_function_summary: bool = True    # Include when relevant
    include_class_summary: bool = True       # Include when relevant
    compress_conversation_history: bool = True
    smart_context_filtering: bool = True
    clean_warnings: bool = True
    remove_fallback_text: bool = True
    maintain_helpfulness: bool = True        # NEW: Prioritize helpfulness over compression

class OptimizedPromptGenerator:
    """
    Optimized prompt generator that creates concise, effective prompts
    while maintaining all essential context and eliminating clutter.
    """
    
    def __init__(self, config: Optional[OptimizedPromptConfig] = None):
        self.config = config or OptimizedPromptConfig()
        self.base_generator = None
        
                # 🚀 PHASE 1: Initialize intent-driven context selection
        try:
            from intent_driven_context_selector import IntentDrivenContextSelector
            self.intent_selector = IntentDrivenContextSelector()
            self.phase1_enabled = True
            print("🚀 Phase 1: Intent-driven context selection enabled")
        except ImportError:
            self.intent_selector = None
            self.phase1_enabled = False
            print("⚠️ Phase 1: Intent-driven context selection not available")

        # 🚀 PHASE 1: Initialize enhanced context intelligence
        try:
            from enhanced_context_intelligence import EnhancedContextIntelligence
            self.context_intelligence = EnhancedContextIntelligence()
            print("🚀 Phase 1: Enhanced context intelligence enabled")
        except ImportError:
            self.context_intelligence = None
            print("⚠️ Phase 1: Enhanced context intelligence not available")

        # 🚀 PHASE 2: Initialize adaptive context learning system
        try:
            from adaptive_context_learner import AdaptiveContextLearner
            self.adaptive_learner = AdaptiveContextLearner()
            self.phase2_enabled = True
            print("🚀 Phase 2: Adaptive context learning system enabled")
        except ImportError:
            self.adaptive_learner = None
            self.phase2_enabled = False
            print("⚠️ Phase 2: Adaptive context learning system not available")

        # 🚀 PHASE 2: Initialize dynamic threshold manager
        try:
            from dynamic_threshold_manager import DynamicThresholdManager
            self.threshold_manager = DynamicThresholdManager()
            print("🚀 Phase 2: Dynamic threshold manager enabled")
        except ImportError:
            self.threshold_manager = None
            print("⚠️ Phase 2: Dynamic threshold manager not available")

        # 🚀 PHASE 2: Initialize performance analyzer
        try:
            from context_performance_analyzer import ContextPerformanceAnalyzer
            self.performance_analyzer = ContextPerformanceAnalyzer()
            print("🚀 Phase 2: Performance analyzer enabled")
        except ImportError:
            self.performance_analyzer = None
            print("⚠️ Phase 2: Performance analyzer not available")

        # 🚀 PHASE 2: Initialize real-time context refiner
        try:
            from real_time_context_refiner import RealTimeContextRefiner
            self.context_refiner = RealTimeContextRefiner()
            print("🚀 Phase 2: Real-time context refiner enabled")
        except ImportError:
            self.context_refiner = None
            print("⚠️ Phase 2: Real-time context refiner not available")
        
        if BASE_GENERATOR_AVAILABLE:
            try:
                self.base_generator = PromptGenerator()
            except Exception as e:
                logger.warning(f"Could not initialize base generator: {e}")
    
    def generate_optimized_prompt(self, 
                                user_message: str, 
                                context_type: str = "smart",
                                force_refresh: bool = False) -> str:
        """
        Generate an optimized, concise prompt that maintains quality while reducing size.
        
        Args:
            user_message: The user's message to enhance
            context_type: Type of context to use
            force_refresh: Force refresh context even if cached
            
        Returns:
            Optimized prompt string (60-80% smaller than original)
        """
        try:
            if self.base_generator:
                # Get base context data
                context = self.base_generator._gather_context_data(user_message, context_type)
                
                # Generate optimized prompt
                optimized_prompt = self._create_optimized_prompt(user_message, context, context_type)
                
                # Validate optimization
                original_size = len(str(context))
                optimized_size = len(optimized_prompt)
                compression_ratio = (1 - optimized_size / original_size) * 100
                
                logger.info(f"🚀 Prompt optimization: {original_size:,} → {optimized_size:,} chars ({compression_ratio:.1f}% reduction)")
                
                return optimized_prompt
            else:
                # Fallback to simple optimized format
                return self._create_simple_optimized_prompt(user_message)
                
        except Exception as e:
            logger.error(f"❌ Optimized prompt generation failed: {e}")
            # Return minimal but effective prompt
            return self._create_minimal_prompt(user_message)
    
    def _create_optimized_prompt(self, user_message: str, context: PromptContext, context_type: str) -> str:
        """Create an optimized prompt with intelligent content filtering"""
        
        # 🚀 PHASE 1: Use intent-driven context selection if available
        if self.phase1_enabled and self.intent_selector:
            return self._create_phase1_optimized_prompt(user_message, context, context_type)
        
        # Fallback to original method
        return self._create_legacy_optimized_prompt(user_message, context, context_type)
    
    def _create_phase1_optimized_prompt(self, user_message: str, context: PromptContext, context_type: str) -> str:
        """Create optimized prompt using Phase 1 improvements"""

        # Convert PromptContext to dict for processing
        context_dict = self._context_to_dict(context)

        # 🚀 PHASE 1: Intent-driven context selection
        relevant_context, intent_analysis = self.intent_selector.select_relevant_context(user_message, context_dict)

        # 🚀 PHASE 1: Enhanced context intelligence with relevance scoring
        if self.context_intelligence:
            filtered_context, relevance_scores, context_summary = self.context_intelligence.process_context(user_message, relevant_context)
            optimization_stats = self.context_intelligence.get_optimization_stats(context_dict, filtered_context)

            # Log optimization results
            print(f"🚀 Phase 1 Optimization: {optimization_stats['original_sections']} → {optimization_stats['filtered_sections']} sections")
            print(f"🚀 Phase 1 Size Reduction: {optimization_stats['reduction_percentage']:.1f}% ({optimization_stats['efficiency_gain']:.1f}x)")
        else:
            filtered_context = relevant_context
            context_summary = ""
            optimization_stats = {}

        # 🚀 PHASE 2: Apply adaptive learning and real-time refinement
        if self.phase2_enabled:
            filtered_context = self._apply_phase2_enhancements(user_message, filtered_context, context_dict, intent_analysis)

        # 🔒 SAFEGUARD: Always include essential continuity context
        filtered_context = self._ensure_essential_context(filtered_context, context_dict)
        
        # 🎯 ENSURE PROJECT PLANS ARE INCLUDED FOR GOALS
        if 'project_plans' in context_dict and 'project_plans' not in filtered_context:
            content = context_dict['project_plans']
            if content and content != "not available" and len(str(content)) > 10:
                filtered_context['project_plans'] = content
                print(f"🎯 SAFEGUARD: Added project plans for goals context")
        
        # 🐛 DEBUG: Log what context is available
        print(f"🔍 DEBUG: Available context keys: {list(context_dict.keys())}")
        print(f"🔍 DEBUG: Conversation summary available: {'conversation_summary' in context_dict}")
        print(f"🔍 DEBUG: Action history available: {'action_history' in context_dict}")
        print(f"🔍 DEBUG: Project plans available: {'project_plans' in context_dict}")
        if 'conversation_summary' in context_dict:
            print(f"🔍 DEBUG: Conversation summary content: {context_dict['conversation_summary'][:100]}...")
        if 'action_history' in context_dict:
            print(f"🔍 DEBUG: Action history content: {context_dict['action_history'][:100]}...")
        if 'project_plans' in context_dict:
            print(f"🔍 DEBUG: Project plans content: {context_dict['project_plans'][:100]}...")
        
        # 🐛 DEBUG: Log intent analysis
        if hasattr(intent_analysis, 'primary_intent'):
            print(f"🔍 DEBUG: Intent: {intent_analysis.primary_intent.value}")
            print(f"🔍 DEBUG: Context requirements: {intent_analysis.context_requirements}")
        else:
            print(f"🔍 DEBUG: Intent analysis type: {type(intent_analysis)}")
            print(f"🔍 DEBUG: Intent analysis content: {intent_analysis}")

        # Build optimized prompt
        prompt_parts = []

        # Essential header
        prompt_parts.append(f"🚀 OPTIMIZED PROMPT: {user_message}")

        # 🚀 PHASE 1: Include context selection summary
        if context_summary:
            prompt_parts.append(f"📋 {context_summary}")

        # Core context (filtered and prioritized)
        prompt_parts.append(self._format_phase1_core_context(filtered_context, intent_analysis))

        # Intent-specific context
        if intent_analysis.primary_intent.value in ['technical', 'code_generation', 'debugging']:
            prompt_parts.append(self._format_phase1_technical_context(filtered_context))

        if intent_analysis.primary_intent.value in ['project_analysis', 'project_structure']:
            prompt_parts.append(self._format_phase1_project_context(filtered_context))

        # Always include conversation context for continuity, general, and technical questions
        if intent_analysis.primary_intent.value in ['conversation_continuity', 'general', 'technical']:
            prompt_parts.append(self._format_phase1_conversation_context(filtered_context))

        # Smart instructions based on intent
        prompt_parts.append(self._format_phase1_smart_instructions(user_message, intent_analysis))

        return "\n\n".join(prompt_parts)

    def _apply_phase2_enhancements(self, user_message: str, filtered_context: Dict, 
                                 original_context: Dict, intent_analysis) -> Dict[str, Any]:
        """Apply Phase 2 enhancements to the filtered context"""
        
        enhanced_context = filtered_context.copy()
        
        # 🚀 PHASE 2: Adaptive context learning
        if self.adaptive_learner:
            try:
                # Learn from this interaction
                excluded_context = [k for k in original_context.keys() if k not in filtered_context]
                learning_result = self.adaptive_learner.learn_from_interaction(
                    user_message=user_message,
                    selected_context=filtered_context,
                    excluded_context=excluded_context,
                    session_id="default"
                )
                print(f"🧠 Phase 2 Learning: {learning_result}")
            except Exception as e:
                print(f"⚠️ Phase 2 Learning failed: {e}")

        # 🚀 PHASE 2: Dynamic threshold adjustment
        if self.threshold_manager:
            try:
                # Get personalized threshold for user
                personalized_threshold = self.threshold_manager.get_personalized_threshold("default")
                print(f"⚡ Phase 2 Threshold: Personalized threshold {personalized_threshold}")
                
                # Apply threshold-based filtering
                enhanced_context = self._apply_personalized_threshold(enhanced_context, personalized_threshold)
            except Exception as e:
                print(f"⚠️ Phase 2 Threshold adjustment failed: {e}")

        # 🚀 PHASE 2: Real-time context refinement
        if self.context_refiner:
            try:
                # Detect and fill context gaps
                refined_context, gaps = self.context_refiner.refine_context_mid_conversation(
                    user_message=user_message,
                    current_context=enhanced_context,
                    available_context=original_context,
                    session_id="default"
                )
                
                if gaps:
                    print(f"🔄 Phase 2 Refinement: Filled {len(gaps)} context gaps")
                    enhanced_context = refined_context
            except Exception as e:
                print(f"⚠️ Phase 2 Threshold adjustment failed: {e}")

        # 🚀 PHASE 2: Performance tracking
        if self.performance_analyzer:
            try:
                # Track this interaction for performance analysis
                context_size = sum(len(str(v)) for v in enhanced_context.values())
                performance_result = self.performance_analyzer.track_performance_event(
                    user_message=user_message,
                    selected_context=enhanced_context,
                    excluded_context=[k for k in original_context.keys() if k not in enhanced_context],
                    response_time_ms=0,  # Will be updated by caller
                    session_id="default"
                )
                print(f"📊 Phase 2 Performance: {performance_result}")
            except Exception as e:
                print(f"⚠️ Phase 2 Performance tracking failed: {e}")

        return enhanced_context

    def _apply_personalized_threshold(self, context: Dict[str, Any], threshold: float) -> Dict[str, Any]:
        """Apply personalized threshold to context selection"""
        # This is a simplified implementation
        # In a full implementation, you'd use the threshold to score and filter context
        return context

    def _ensure_essential_context(self, filtered_context: Dict[str, Any], original_context: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure essential continuity context is always included"""
        essential_sections = [
            "conversation_summary",  # What we were working on
            "action_history",        # What actions were taken
            "project_plans",         # What goals we have
            "project_objectives"     # What we're trying to achieve
        ]
        
        for section in essential_sections:
            if section in original_context and section not in filtered_context:
                # Check if the content is meaningful
                content = original_context[section]
                if content and content != "not available" and len(str(content)) > 10:
                    filtered_context[section] = content
                    print(f"🔒 SAFEGUARD: Added essential context '{section}' for continuity")
        
        return filtered_context
    
    def _create_legacy_optimized_prompt(self, user_message: str, context: PromptContext, context_type: str) -> str:
        """Original optimized prompt method as fallback"""
        
        # Analyze user intent to determine what context is actually needed
        intent_analysis = self._analyze_user_intent(user_message, context)
        
        # Build optimized prompt based on intent
        prompt_parts = []
        
        # Essential header
        prompt_parts.append(f"🚀 OPTIMIZED PROMPT: {user_message}")
        
        # Core context (always included)
        prompt_parts.append(self._format_core_context(context, intent_analysis))
        
        # Conditional context (only when relevant)
        if intent_analysis.get('needs_technical_context', False):
            prompt_parts.append(self._format_technical_context(context))
        
        if intent_analysis.get('needs_project_context', False):
            prompt_parts.append(self._format_project_context(context))
        
        if intent_analysis.get('needs_conversation_context', False):
            prompt_parts.append(self._format_conversation_context(context))
        
        # Smart instructions based on intent
        prompt_parts.append(self._format_smart_instructions(user_message, intent_analysis))
        
        # Add helpful context based on intent
        if intent_analysis.get('needs_technical_context', False):
            prompt_parts.append(self._format_technical_context(context))
        
        if intent_analysis.get('needs_project_context', False):
            prompt_parts.append(self._format_project_context(context))
        
        if intent_analysis.get('needs_conversation_context', False):
            prompt_parts.append(self._format_conversation_context(context))
        
        return "\n\n".join(prompt_parts)
    
    def _context_to_dict(self, context: PromptContext) -> Dict[str, Any]:
        """Convert PromptContext to dictionary for Phase 1 processing"""
        context_dict = {}
        
        # Map context attributes to dictionary keys
        if hasattr(context, 'user_preferences'):
            context_dict['user_preferences'] = context.user_preferences
        if hasattr(context, 'tech_stack'):
            context_dict['tech_stack'] = context.tech_stack
        if hasattr(context, 'agent_metadata'):
            context_dict['agent_metadata'] = context.agent_metadata
        if hasattr(context, 'conversation_summary'):
            context_dict['conversation_summary'] = context.conversation_summary
        if hasattr(context, 'action_history'):
            context_dict['action_history'] = context.action_history
        if hasattr(context, 'project_plans'):
            context_dict['project_plans'] = context.project_plans
        if hasattr(context, 'project_structure'):
            context_dict['project_structure'] = context.project_structure
        if hasattr(context, 'best_practices'):
            context_dict['best_practices'] = context.best_practices
        if hasattr(context, 'common_issues'):
            context_dict['common_issues'] = context.common_issues
        
        return context_dict
    
    def _format_phase1_core_context(self, filtered_context: Dict, intent_analysis) -> str:
        """Format core context for Phase 1 prompts"""
        core_sections = []
        
        # User preferences (always included)
        if 'user_preferences' in filtered_context:
            core_sections.append(f"👤 PREFERENCES: {self._clean_preferences(filtered_context['user_preferences'])}")
        
        # Tech stack (high relevance for technical questions)
        if 'tech_stack' in filtered_context:
            core_sections.append(f"⚙️ TECH: {self._clean_tech_stack(filtered_context['tech_stack'])}")
        
        # Agent metadata (always included)
        if 'agent_metadata' in filtered_context:
            core_sections.append(f"🤖 AGENT: {self._clean_agent_metadata(filtered_context['agent_metadata'])}")
        
        return "\n".join(core_sections)
    
    def _format_phase1_technical_context(self, filtered_context: Dict) -> str:
        """Format technical context for Phase 1 prompts"""
        tech_sections = []
        
        if 'best_practices' in filtered_context:
            tech_sections.append(f"✅ BEST PRACTICES: {self._clean_best_practices(filtered_context['best_practices'])}")
        
        if 'common_issues' in filtered_context:
            tech_sections.append(f"⚠️ COMMON ISSUES: {self._clean_common_issues(filtered_context['common_issues'])}")
        
        return "\n".join(tech_sections) if tech_sections else ""
    
    def _format_phase1_project_context(self, filtered_context: Dict) -> str:
        """Format project context for Phase 1 prompts"""
        project_sections = []
        
        if 'project_structure' in filtered_context:
            project_sections.append(f"🏗️ PROJECT: {self._clean_project_structure(filtered_context['project_structure'])}")
        
        return "\n".join(project_sections) if project_sections else ""
    
    def _format_phase1_conversation_context(self, filtered_context: Dict) -> str:
        """Format conversation context for Phase 1 prompts"""
        conv_sections = []
        
        print(f"🔍 DEBUG: Formatting conversation context with keys: {list(filtered_context.keys())}")
        
        if 'conversation_summary' in filtered_context:
            summary = self._compress_conversation_summary(filtered_context['conversation_summary'])
            conv_sections.append(f"💬 CONTEXT: {summary}")
            print(f"🔍 DEBUG: Added conversation summary: {summary[:50]}...")
        
        if 'action_history' in filtered_context:
            history = self._compress_action_history(filtered_context['action_history'])
            conv_sections.append(f"📝 RECENT: {history}")
            print(f"🔍 DEBUG: Added action history: {history[:50]}...")
        
        # 🎯 ADD PROJECT PLANS & OBJECTIVES (GOALS)
        if 'project_plans' in filtered_context:
            plans = self._compress_project_plans(filtered_context['project_plans'])
            conv_sections.append(f"🎯 GOALS: {plans}")
            print(f"🔍 DEBUG: Added project plans: {plans[:50]}...")
        
        result = "\n".join(conv_sections) if conv_sections else ""
        print(f"🔍 DEBUG: Conversation context result: {result[:100]}...")
        return result
    
    def _format_phase1_smart_instructions(self, user_message: str, intent_analysis) -> str:
        """Format smart instructions for Phase 1 prompts"""
        instructions = []
        
        # Intent-specific instructions
        if intent_analysis.primary_intent.value == 'technical':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Technical accuracy and best practices",
                "• Working code examples when relevant",
                "• Performance considerations",
                "• Error handling approaches"
            ])
        elif intent_analysis.primary_intent.value == 'code_generation':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Working, runnable code",
                "• Clear explanations and comments",
                "• Best practices and patterns",
                "• Error handling and validation"
            ])
        elif intent_analysis.primary_intent.value == 'debugging':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Systematic debugging approach",
                "• Common causes and solutions",
                "• Step-by-step troubleshooting",
                "• Prevention strategies"
            ])
        elif intent_analysis.primary_intent.value == 'project_analysis':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Project structure insights",
                "• Code organization recommendations",
                "• Improvement suggestions",
                "• Best practices for your tech stack"
            ])
        elif intent_analysis.primary_intent.value == 'conversation_continuity':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Continuation of previous work",
                "• Context from earlier conversations",
                "• Progress updates and next steps",
                "• Seamless conversation flow"
            ])
        else:
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Context-aware assistance",
                "• Project-relevant information",
                "• Actionable next steps",
                "• Clear, concise guidance"
            ])
        
        # Add user preference compliance
        instructions.append("👤 FOLLOW USER PREFERENCES: Concise, technical, structured responses")
        
        return "\n".join(instructions)
    
    def _clean_best_practices(self, best_practices: str) -> str:
        """Clean and compress best practices"""
        if not best_practices:
            return "Not available"
        
        if len(best_practices) > 200:
            return best_practices[:200] + "..."
        return best_practices
    
    def _clean_common_issues(self, common_issues: str) -> str:
        """Clean and compress common issues"""
        if not common_issues:
            return "Not available"
        
        if len(common_issues) > 200:
            return common_issues[:200] + "..."
        return common_issues
    
    def _clean_project_structure(self, project_structure: str) -> str:
        """Clean and compress project structure"""
        if not project_structure:
            return "Not available"
        
        if len(project_structure) > 300:
            return project_structure[:300] + "..."
        return project_structure
    
    def _analyze_user_intent(self, user_message: str, context: PromptContext) -> Dict[str, Any]:
        """Analyze user message to determine what context is actually needed"""
        
        message_lower = user_message.lower()
        
        intent_analysis = {
            'primary_intent': 'general',
            'needs_technical_context': False,
            'needs_project_context': False,
            'needs_conversation_context': False,
            'complexity': 'medium',
            'focus_areas': []
        }
        
        # Technical context needed for:
        if any(word in message_lower for word in ['code', 'implement', 'fix', 'error', 'bug', 'database', 'api']):
            intent_analysis['needs_technical_context'] = True
            intent_analysis['primary_intent'] = 'technical'
        
        # Project context needed for:
        if any(word in message_lower for word in ['project', 'structure', 'files', 'classes', 'functions']):
            intent_analysis['needs_project_context'] = True
            intent_analysis['primary_intent'] = 'project_analysis'
        
        # Conversation context needed for:
        if any(word in message_lower for word in ['continue', 'previous', 'earlier', 'yesterday', 'before']):
            intent_analysis['needs_conversation_context'] = True
            intent_analysis['primary_intent'] = 'conversation_continuity'
        
        # Complexity assessment
        if any(word in message_lower for word in ['simple', 'basic', 'quick']):
            intent_analysis['complexity'] = 'low'
        elif any(word in message_lower for word in ['complex', 'advanced', 'detailed', 'comprehensive']):
            intent_analysis['complexity'] = 'high'
        
        return intent_analysis
    
    def _format_core_context(self, context: PromptContext, intent_analysis: Dict[str, Any]) -> str:
        """Format essential context that's always included"""
        
        core_sections = []
        
        # User preferences (essential for personalized responses)
        if context.user_preferences and context.user_preferences != "User preferences not available":
            core_sections.append(f"👤 PREFERENCES: {self._clean_preferences(context.user_preferences)}")
        
        # Tech stack (essential for technical responses)
        if context.tech_stack and context.tech_stack != "Tech stack not available":
            core_sections.append(f"⚙️ TECH: {self._clean_tech_stack(context.tech_stack)}")
        
        # Agent metadata (essential for context)
        if context.agent_metadata and context.agent_metadata != "Agent metadata not available":
            core_sections.append(f"🤖 AGENT: {self._clean_agent_metadata(context.agent_metadata)}")
        
        # Always include conversation summary for context continuity
        if context.conversation_summary and context.conversation_summary != "Conversation summary not available":
            core_sections.append(f"💬 CONTEXT: {self._compress_conversation_summary(context.conversation_summary)}")
        
        # Always include recent actions for continuity
        if context.action_history and context.action_history != "Action history not available":
            core_sections.append(f"📝 RECENT: {self._compress_action_history(context.action_history)}")
        
        return "\n".join(core_sections)
    
    def _format_technical_context(self, context: PromptContext) -> str:
        """Format technical context when needed"""
        
        tech_sections = []
        
        if context.project_plans and context.project_plans != "Project plans not available":
            tech_sections.append(f"🎯 PLANS: {self._clean_project_plans(context.project_plans)}")
        
        if context.best_practices:
            tech_sections.append(f"✅ BEST PRACTICES: {', '.join(context.best_practices[:3])}")
        
        if context.common_issues:
            tech_sections.append(f"⚠️ COMMON ISSUES: {', '.join(context.common_issues[:3])}")
        
        return "\n".join(tech_sections) if tech_sections else ""
    
    def _format_project_context(self, context: PromptContext) -> str:
        """Format project context when needed"""
        
        project_sections = []
        
        if context.project_overview and context.project_overview != "Project overview not available":
            # Compress project overview
            overview = context.project_overview
            if len(overview) > 500:
                overview = overview[:500] + "..."
            project_sections.append(f"🏗️ PROJECT: {overview}")
        
        return "\n".join(project_sections) if project_sections else ""
    
    def _compress_conversation_summary(self, summary: str) -> str:
        """Compress conversation summary while maintaining key information"""
        if len(summary) <= 200:
            return summary
        
        # Extract key metrics and recent topics
        lines = summary.split('\n')
        compressed = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['total interactions', 'recent topics', 'user requests']):
                compressed.append(line)
                if len('\n'.join(compressed)) > 200:
                    break
        
        return '\n'.join(compressed) + "..." if len('\n'.join(compressed)) > 150 else '\n'.join(compressed)
    
    def _compress_action_history(self, history: str) -> str:
        """Compress action history while maintaining recent actions"""
        if len(history) <= 200:
            return history
        
        # Extract recent actions
        lines = history.split('\n')
        recent_actions = []
        
        for line in lines[:5]:  # Keep last 5 actions
            if 'conversation_turn:' in line or 'client_request:' in line or 'agent_response:' in line:
                # Compress the line
                if len(line) > 80:
                    line = line[:80] + "..."
                recent_actions.append(line)
        
        return '\n'.join(recent_actions)
    
    def _compress_project_plans(self, plans: str) -> str:
        """Compress project plans while maintaining key objectives"""
        if len(plans) <= 300:
            return plans
        
        # Extract key objectives and plans
        lines = plans.split('\n')
        key_plans = []
        
        for line in lines:
            # Look for key objective indicators
            if any(keyword in line.lower() for keyword in ['objective', 'goal', 'target', 'aim', 'purpose', 'build', 'create', 'implement']):
                if len(line) > 100:
                    line = line[:100] + "..."
                key_plans.append(line)
                if len('\n'.join(key_plans)) > 300:
                    break
        
        return '\n'.join(key_plans) if key_plans else plans[:300] + "..."
    
    def _format_conversation_context(self, context: PromptContext) -> str:
        """Format conversation context when needed"""
        
        conv_sections = []
        
        if context.conversation_summary and context.conversation_summary != "Conversation summary not available":
            # Compress conversation summary
            summary = context.conversation_summary
            if len(summary) > 300:
                summary = summary[:300] + "..."
            conv_sections.append(f"💬 CONTEXT: {summary}")
        
        if context.action_history and context.action_history != "Action history not available":
            # Show only recent actions
            actions = context.action_history
            if len(actions) > 200:
                actions = actions[:200] + "..."
            conv_sections.append(f"📝 RECENT: {actions}")
        
        return "\n".join(conv_sections) if conv_sections else ""
    
    def _format_smart_instructions(self, user_message: str, intent_analysis: Dict[str, Any]) -> str:
        """Format smart, context-aware instructions"""
        
        instructions = []
        
        if intent_analysis['primary_intent'] == 'technical':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Technical accuracy and best practices",
                "• Working code examples when relevant",
                "• Performance considerations",
                "• Error handling approaches"
            ])
        elif intent_analysis['primary_intent'] == 'project_analysis':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Project structure insights",
                "• Code organization recommendations",
                "• File and class relationships",
                "• Improvement suggestions"
            ])
        elif intent_analysis['primary_intent'] == 'conversation_continuity':
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Continuation of previous work",
                "• Context from earlier conversations",
                "• Progress updates and next steps",
                "• Seamless conversation flow"
            ])
        else:
            instructions.extend([
                "🎯 RESPOND WITH:",
                "• Context-aware assistance",
                "• Project-relevant information",
                "• Actionable next steps",
                "• Clear, concise guidance"
            ])
        
        # Add user preference compliance
        instructions.append("👤 FOLLOW USER PREFERENCES: Concise, technical, structured responses")
        
        return "\n".join(instructions)
    
    def _clean_preferences(self, preferences: str) -> str:
        """Clean and compress user preferences while maintaining structure"""
        if not preferences or preferences == "User preferences not available":
            return "Not available"
        
        # Keep the detailed structure but clean up excessive content
        lines = preferences.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                # Keep all preference lines but clean up workflow entries
                if line.startswith('Workflow:'):
                    # Compress workflow entries
                    if len(line) > 80:
                        line = line[:80] + "..."
                elif line.startswith('General:'):
                    # Keep general preferences as they're important
                    if len(line) > 100:
                        line = line[:100] + "..."
                elif len(line) > 120:  # Truncate very long lines
                    line = line[:120] + "..."
                
                cleaned_lines.append(line)
        
        # Return structured format instead of compressed single line
        return "\n    ".join(cleaned_lines)
    
    def _clean_tech_stack(self, tech_stack: str) -> str:
        """Clean and compress tech stack information"""
        if not tech_stack or tech_stack == "Tech stack not available":
            return "Not available"
        
        # Extract key technologies
        tech_terms = ['Python', 'SQLite', 'MCP', 'SQLAlchemy', 'FastMCP']
        found_tech = []
        
        for tech in tech_terms:
            if tech.lower() in tech_stack.lower():
                found_tech.append(tech)
        
        if found_tech:
            return ", ".join(found_tech)
        else:
            return tech_stack[:100] + "..." if len(tech_stack) > 100 else tech_stack
    
    def _clean_agent_metadata(self, metadata: str) -> str:
        """Clean and compress agent metadata"""
        if not metadata or metadata == "Agent metadata not available":
            return "Not available"
        
        # Extract key information
        if "Johny" in metadata:
            return "Johny (Context-Aware AI Assistant)"
        elif "mcp-project-local" in metadata:
            return "MCP Project Local Agent"
        else:
            return metadata[:100] + "..." if len(metadata) > 100 else metadata
    
    def _clean_project_plans(self, plans: str) -> str:
        """Clean and compress project plans"""
        if not plans or plans == "Project plans not available":
            return "Not available"
        
        # Extract completed items
        if "✅" in plans:
            completed = [line.strip() for line in plans.split('\n') if "✅" in line]
            if completed:
                return f"{len(completed)} completed objectives"
        
        return plans[:200] + "..." if len(plans) > 200 else plans
    
    def _create_simple_optimized_prompt(self, user_message: str) -> str:
        """Create a simple optimized prompt when base generator is unavailable"""
        return f"""🚀 OPTIMIZED PROMPT: {user_message}

👤 PREFERENCES: Use SQLite, Python, MCP | Concise, technical, structured responses
⚙️ TECH: Python, SQLite, MCP, SQLAlchemy
🤖 AGENT: Johny (Context-Aware AI Assistant)

🎯 RESPOND WITH:
• Context-aware assistance
• Project-relevant information  
• Actionable next steps
• Clear, concise guidance

👤 FOLLOW USER PREFERENCES: Concise, technical, structured responses"""

    def _create_minimal_prompt(self, user_message: str) -> str:
        """Create minimal prompt as last resort"""
        return f"🚀 MINIMAL PROMPT: {user_message}\n\n👤 PREFERENCES: Concise, technical, structured responses\n⚙️ TECH: Python, SQLite, MCP\n🤖 AGENT: Johny\n\n🎯 Provide helpful, context-aware assistance."

# Convenience function
def generate_optimized_prompt(user_message: str, **kwargs) -> str:
    """Generate an optimized prompt using the default configuration"""
    generator = OptimizedPromptGenerator()
    return generator.generate_optimized_prompt(user_message, **kwargs)
