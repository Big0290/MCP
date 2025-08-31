#!/usr/bin/env python3
"""
🚀 Centralized Prompt Generator System with Adaptive Precision Engine

This module provides a unified interface for generating enhanced prompts with comprehensive context.
It consolidates all prompt generation logic from various files into one maintainable system.

Features:
- Automatic context injection with conversation history
- Tech stack detection and project context
- User preferences and learning patterns
- Multiple enhancement strategies
- Performance monitoring and caching
- NEW: Adaptive Prompt Precision Engine (APPE) integration
- NEW: Task-aware prompt optimization
- NEW: Behavioral steering and success pattern learning
"""

import logging
import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Import the new Adaptive Prompt Precision Engine
try:
    from adaptive_prompt_engine import (
        AdaptivePromptEngine, 
        get_adaptive_prompt_engine,
        enhance_prompt_with_appe,
        learn_from_appe_interaction
    )
    APPE_AVAILABLE = True
except ImportError:
    APPE_AVAILABLE = False
    print("Warning: Adaptive Prompt Precision Engine not available")

logger = logging.getLogger(__name__)

@dataclass
class PromptContext:
    """Structured context data for prompt enhancement"""
    conversation_summary: str
    action_history: str
    tech_stack: str
    project_plans: str
    user_preferences: str
    agent_metadata: str
    recent_interactions: List[Dict[str, Any]]
    project_patterns: List[str]
    best_practices: List[str]
    common_issues: List[str]
    development_workflow: List[str]
    confidence_score: float
    context_type: str = "comprehensive"
    # New project structure fields
    project_structure: Optional[Dict[str, Any]] = None
    project_overview: Optional[str] = None
    function_summary: Optional[str] = None
    class_summary: Optional[str] = None

class PromptGenerator:
    """
    Centralized prompt generator with multiple enhancement strategies
    """
    
    def __init__(self):
        self.enhancement_stats = {
            'total_generated': 0,
            'successful_generations': 0,
            'failed_generations': 0,
            'average_generation_time': 0.0,
            'last_generation': None,
            'context_cache_hits': 0,
            'context_cache_misses': 0
        }
        self.context_cache = {}
        self.enhancement_strategies = {
            'adaptive': self._generate_smart_prompt,  # NEW: APPE-powered adaptive strategy
            'comprehensive': self._generate_comprehensive_prompt,
            'technical': self._generate_technical_prompt,
            'conversation': self._generate_conversation_prompt,
            'smart': self._generate_smart_prompt,
            'dynamic': self._generate_smart_prompt,  # Dynamic strategy
            'minimal': self._generate_minimal_prompt
        }
    
    def generate_enhanced_prompt(self, 
                               user_message: str, 
                               context_type: str = "adaptive",  # Changed default to adaptive (APPE)
                               force_refresh: bool = False,
                               use_appe: bool = True) -> str:
        """
        Generate an enhanced prompt with the specified context type
        
        Args:
            user_message: The original user message
            context_type: Type of context enhancement (adaptive, comprehensive, technical, conversation, smart, minimal)
            force_refresh: Force refresh context even if cached
            use_appe: Use Adaptive Prompt Precision Engine when available
            
        Returns:
            Enhanced prompt string
        """
        start_time = datetime.now()
        
        try:
            # NEW: Try APPE first if available and requested
            if use_appe and APPE_AVAILABLE and context_type == "adaptive":
                try:
                    # Generate context data for APPE
                    context = self._gather_context_data(user_message, context_type)
                    
                    # Convert to APPE format
                    appe_context = self._convert_to_appe_context(context)
                    
                    # Use APPE for optimal prompt generation
                    enhanced_prompt = enhance_prompt_with_appe(user_message, appe_context)
                    
                    # Update statistics
                    self._update_stats(True, start_time)
                    self.enhancement_stats['appe_generations'] = self.enhancement_stats.get('appe_generations', 0) + 1
                    
                    logger.info(f"🚀 Generated APPE prompt: {len(user_message)} -> {len(enhanced_prompt)} chars")
                    
                    return enhanced_prompt
                    
                except Exception as e:
                    logger.warning(f"APPE generation failed, falling back to standard: {e}")
                    # Fall through to standard generation
            
            # Standard prompt generation (existing logic)
            # Check cache first (unless force refresh)
            cache_key = f"{hash(user_message)}_{context_type}"
            if not force_refresh and cache_key in self.context_cache:
                self.enhancement_stats['context_cache_hits'] += 1
                cached_result = self.context_cache[cache_key]
                if self._is_cache_valid(cached_result):
                    logger.info(f"🎯 Cache hit for prompt type: {context_type}")
                    return cached_result['enhanced_prompt']
            
            self.enhancement_stats['context_cache_misses'] += 1
            
            # Generate context data
            context = self._gather_context_data(user_message, context_type)
            
            # Generate enhanced prompt using selected strategy
            if context_type in self.enhancement_strategies:
                enhanced_prompt = self.enhancement_strategies[context_type](user_message, context)
            else:
                # Default to dynamic prompt generation for better results
                enhanced_prompt = self._generate_smart_prompt(user_message, context)
            
            # Cache the result
            self._cache_result(cache_key, user_message, enhanced_prompt, context_type)
            
            # Update statistics
            self._update_stats(True, start_time)
            
            logger.info(f"✅ Generated {context_type} prompt: {len(user_message)} -> {len(enhanced_prompt)} chars")
            
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"❌ Prompt generation failed: {str(e)}")
            self._update_stats(False, start_time)
            return self._generate_fallback_prompt(user_message, str(e))
    
    def _gather_context_data(self, user_message: str, context_type: str) -> PromptContext:
        """Gather all necessary context data for prompt enhancement"""
        try:
            # Import context functions
            from local_mcp_server_simple import (
                _generate_conversation_summary,
                _extract_action_history,
                _get_tech_stack_definition,
                _get_project_plans,
                _get_user_preferences,
                _get_agent_metadata
            )
            
            # Get recent interactions from database
            import sqlite3
            
            # Use direct SQLite connection to get real database data
            db_path = "/Users/jonathanmorand/Documents/ProjectsFolder/MCP_FOLDER/MCP/MCP/data/agent_tracker.db"
            
            try:
                with sqlite3.connect(db_path) as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT 50")
                    rows = cursor.fetchall()
                    
                    # Convert to dictionaries for compatibility with existing functions
                    all_interactions = []
                    for row in rows:
                        interaction = {
                            'id': row['id'],
                            'interaction_type': row['interaction_type'],
                            'prompt': row['prompt'],
                            'response': row['response'],
                            'client_request': row['client_request'],
                            'agent_response': row['agent_response'],
                            'timestamp': row['timestamp'],
                            'session_id': row['session_id'],
                            'status': row['status'] or 'completed'
                        }
                        all_interactions.append(interaction)
            except Exception as e:
                print(f"Error accessing database: {e}")
                all_interactions = []
            
            # Filter conversation interactions manually
            conversation_interactions = [i for i in all_interactions 
                                       if i.get('interaction_type', '') in ['conversation_turn', 'client_request', 'agent_response', 'user_prompt']][:15]
            
            # Filter system interactions manually
            system_interactions = [i for i in all_interactions 
                                 if i.get('interaction_type', '') in ['health_check', 'monitoring_started', 'module_import']][:5]
            

            
            # Combine them, prioritizing conversations
            recent_interactions = system_interactions + conversation_interactions
            
            # Convert interactions to proper format for summarization functions
            interactions_data = []
            for interaction in recent_interactions:
                timestamp = interaction.get('timestamp', datetime.now())
                # Handle both string and datetime timestamps
                if isinstance(timestamp, str):
                    timestamp_str = timestamp
                elif timestamp:
                    timestamp_str = timestamp.isoformat()
                else:
                    timestamp_str = None
                    
                interactions_data.append({
                    'timestamp': timestamp_str,
                    'interaction_type': interaction.get('interaction_type', 'unknown'),
                    'client_request': interaction.get('prompt', ''),
                    'agent_response': interaction.get('response', ''),
                    'status': interaction.get('status', 'unknown'),
                    'tool_name': interaction.get('tool_name', ''),
                    'parameters': interaction.get('parameters', {}),
                    'execution_time_ms': interaction.get('execution_time_ms', 0),
                    'error_message': interaction.get('error_message', ''),
                    'meta_data': interaction.get('meta_data', {}),
                    'full_content': interaction.get('full_content', ''),
                    'context_summary': interaction.get('context_summary', ''),
                    'semantic_keywords': interaction.get('semantic_keywords', []),
                    'topic_category': interaction.get('topic_category', 'general'),
                    'context_relevance_score': interaction.get('context_relevance_score', 0.0),
                    'conversation_context': interaction.get('conversation_context', {})
                })
            
            # Generate context components
            conversation_summary = _generate_conversation_summary(interactions_data)
            action_history = _extract_action_history(interactions_data)
            tech_stack = _get_tech_stack_definition()
            project_plans = _get_project_plans()
            # Use unified preference manager for single source of truth
            try:
                from unified_preference_manager import get_user_preferences_unified
                user_preferences = get_user_preferences_unified()
            except ImportError:
                # Fallback to old method if unified system not available
                user_preferences = _get_user_preferences()
            agent_metadata = _get_agent_metadata()
            
            # Detect project patterns and best practices
            project_patterns = self._detect_project_patterns(user_message, tech_stack)
            best_practices = self._get_best_practices(context_type)
            common_issues = self._get_common_issues(context_type)
            development_workflow = self._get_development_workflow(context_type)
            
            # Analyze project structure for enhanced context
            project_structure = self._analyze_project_structure()
            project_overview = self._generate_project_overview(project_structure)
            function_summary = self._get_function_summary(project_structure)
            class_summary = self._get_class_summary(project_structure)
            
            # Calculate confidence score based on available data
            confidence_score = self._calculate_confidence_score(
                recent_interactions, tech_stack, project_plans
            )
            
            return PromptContext(
                conversation_summary=conversation_summary,
                action_history=action_history,
                tech_stack=tech_stack,
                project_plans=project_plans,
                user_preferences=user_preferences,
                agent_metadata=agent_metadata,
                recent_interactions=interactions_data,
                project_patterns=project_patterns,
                best_practices=best_practices,
                common_issues=common_issues,
                development_workflow=development_workflow,
                confidence_score=confidence_score,
                context_type=context_type,
                project_structure=project_structure,
                project_overview=project_overview,
                function_summary=function_summary,
                class_summary=class_summary
            )
            
        except Exception as e:
            logger.error(f"Context gathering failed: {str(e)}")
            # Return minimal context
            return PromptContext(
                conversation_summary="Context retrieval failed",
                action_history="No action history available",
                tech_stack="Tech stack detection failed",
                project_plans="Project plans unavailable",
                user_preferences="User preferences not loaded",
                agent_metadata="Agent metadata unavailable",
                recent_interactions=[],
                project_patterns=["General development patterns"],
                best_practices=["Standard development practices"],
                common_issues=["Common development issues"],
                development_workflow=["Standard development workflow"],
                confidence_score=0.0,
                context_type=context_type,
                project_structure=None,
                project_overview="Project structure analysis failed",
                function_summary="Function summary not available",
                class_summary="Class summary not available"
            )
    
    def _generate_comprehensive_prompt(self, user_message: str, context: PromptContext) -> str:
        """Generate a comprehensive prompt with all available context"""
        return f"""=== 🚀 COMPREHENSIVE ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== 📊 CONTEXT INJECTION ===

🎯 CONVERSATION SUMMARY:
{context.conversation_summary}

📝 ACTION HISTORY:
{context.action_history}

⚙️ TECH STACK:
{context.tech_stack}

🎯 PROJECT PLANS & OBJECTIVES:
{context.project_plans}

👤 USER PREFERENCES:
{context.user_preferences}

🤖 AGENT METADATA:
{context.agent_metadata}

🔍 PROJECT PATTERNS:
{chr(10).join(f"• {pattern}" for pattern in context.project_patterns)}

✅ BEST PRACTICES:
{chr(10).join(f"• {practice}" for practice in context.best_practices)}

⚠️ COMMON ISSUES & SOLUTIONS:
{chr(10).join(f"• {issue}" for issue in context.common_issues)}

🔄 DEVELOPMENT WORKFLOW:
{chr(10).join(f"• {workflow}" for workflow in context.development_workflow)}

📈 CONTEXT CONFIDENCE: {context.confidence_score:.1%}

=== 🏗️ PROJECT STRUCTURE & CODEBASE ===

{context.project_overview if context.project_overview else "Project structure analysis not available"}

{context.function_summary if context.function_summary else "Function summary not available"}

{context.class_summary if context.class_summary else "Class summary not available"}

=== 🎯 INSTRUCTIONS ===
Please respond to the user's message above, taking into account:

1. 📚 The current conversation context and recent interactions
2. 🎯 The specific actions and steps taken so far
3. ⚙️ The technical stack and capabilities available
4. 🎯 The project goals and objectives
5. 👤 The user's stated preferences and requirements
6. 🤖 The agent's capabilities and current state
7. 🔍 Project-specific patterns and best practices
8. ⚠️ Common issues and solutions for this context
9. 🔄 Recommended development workflow
10. 📊 The confidence level of available context
11. 🏗️ The complete project structure and codebase organization
12. 🔧 Available functions and classes for implementation
13. 📁 File organization and technology stack details

Provide a comprehensive, context-aware response that:
• Builds upon our conversation history
• Leverages project-specific knowledge
• Addresses the user's preferences
• Suggests actionable next steps
• References relevant technical details
• Maintains conversation continuity

=== 🚀 END ENHANCED PROMPT ===
        """.strip()
    
    def _generate_technical_prompt(self, user_message: str, context: PromptContext) -> str:
        """Generate a technical-focused prompt"""
        return f"""=== ⚙️ TECHNICAL ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== 🔧 TECHNICAL CONTEXT ===

⚙️ TECH STACK:
{context.tech_stack}

🎯 PROJECT PLANS:
{context.project_plans}

🔍 PROJECT PATTERNS:
{chr(10).join(f"• {pattern}" for pattern in context.project_patterns)}

✅ BEST PRACTICES:
{chr(10).join(f"• {practice}" for practice in context.best_practices)}

⚠️ COMMON ISSUES:
{chr(10).join(f"• {issue}" for issue in context.common_issues)}

🔄 DEVELOPMENT WORKFLOW:
{chr(10).join(f"• {workflow}" for workflow in context.development_workflow)}

📈 CONFIDENCE: {context.confidence_score:.1%}

=== 🎯 TECHNICAL INSTRUCTIONS ===
Provide a technical response focusing on:
1. Code examples and implementation details
2. Technical best practices and patterns
3. Performance considerations and optimizations
4. Security and error handling
5. Testing and deployment strategies
6. Integration with existing tech stack

=== ⚙️ END TECHNICAL PROMPT ===
        """.strip()
    
    def _generate_conversation_prompt(self, user_message: str, context: PromptContext) -> str:
        """Generate a conversation-focused prompt"""
        return f"""=== 💬 CONVERSATION ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== 🗣️ CONVERSATION CONTEXT ===

🎯 CONVERSATION SUMMARY:
{context.conversation_summary}

📝 ACTION HISTORY:
{context.action_history}

👤 USER PREFERENCES:
{context.user_preferences}

🤖 AGENT METADATA:
{context.agent_metadata}

📊 RECENT INTERACTIONS: {len(context.recent_interactions)} interactions

=== 🎯 CONVERSATION INSTRUCTIONS ===
Provide a conversational response that:
1. Maintains natural conversation flow
2. References previous interactions appropriately
3. Adapts to user's communication style
4. Builds upon established context
5. Suggests relevant follow-up topics
6. Maintains engagement and helpfulness

=== 💬 END CONVERSATION PROMPT ===
        """.strip()
    
    def _generate_smart_prompt(self, user_message: str, context: PromptContext) -> str:
        """Generate a smart, adaptive prompt"""
        return f"""=== 🧠 SMART CONTEXT ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== 🎯 SMART CONTEXT ===

⚙️ TECH STACK:
{context.tech_stack}

🔍 PROJECT PATTERNS:
{chr(10).join(f"• {pattern}" for pattern in context.project_patterns)}

✅ BEST PRACTICES:
{chr(10).join(f"• {practice}" for practice in context.best_practices)}

⚠️ COMMON ISSUES:
{chr(10).join(f"• {issue}" for issue in context.common_issues)}

🔄 DEVELOPMENT WORKFLOW:
{chr(10).join(f"• {workflow}" for workflow in context.development_workflow)}

👤 USER PREFERENCES:
{chr(10).join(f"• {key.replace('_', ' ').title()}: {value}" for key, value in (json.loads(context.user_preferences).items() if isinstance(context.user_preferences, str) else context.user_preferences.items()))}

📈 CONFIDENCE: {context.confidence_score:.1%}

=== 🧠 SMART INSTRUCTIONS ===
Provide an intelligent response that:
1. Adapts to the detected tech stack and project type
2. Leverages project-specific patterns and best practices
3. Addresses common issues proactively
4. Follows recommended development workflow
5. Respects user preferences and communication style
6. Suggests context-aware improvements

=== 🧠 END SMART PROMPT ===
        """.strip()
    
    def _generate_minimal_prompt(self, user_message: str, context: PromptContext) -> str:
        """Generate a minimal context prompt"""
        return f"""=== 📝 MINIMAL ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== 📊 BASIC CONTEXT ===

🎯 CONVERSATION SUMMARY:
{context.conversation_summary}

⚙️ TECH STACK:
{context.tech_stack}

📈 CONFIDENCE: {context.confidence_score:.1%}

=== 🎯 MINIMAL INSTRUCTIONS ===
Provide a concise response with essential context.

=== 📝 END MINIMAL PROMPT ===
        """.strip()
    
    def _generate_fallback_prompt(self, user_message: str, error_message: str) -> str:
        """Generate a fallback prompt when context generation fails"""
        return f"""=== ⚠️ FALLBACK ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== ⚠️ CONTEXT INJECTION FAILED ===
Error: {error_message}

=== 📝 BASIC PROMPT ===
{user_message}

=== ⚠️ END FALLBACK PROMPT ===
        """.strip()
    
    def _detect_project_patterns(self, user_message: str, tech_stack: str) -> List[str]:
        """Detect project patterns based on user message and tech stack"""
        patterns = []
        
        # Analyze user message for patterns
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ['deploy', 'deployment', 'production']):
            patterns.append("Deployment and production workflows")
        
        if any(word in message_lower for word in ['test', 'testing', 'debug']):
            patterns.append("Testing and debugging practices")
        
        if any(word in message_lower for word in ['api', 'endpoint', 'route']):
            patterns.append("API design and development")
        
        if any(word in message_lower for word in ['database', 'db', 'sql']):
            patterns.append("Database design and optimization")
        
        if any(word in message_lower for word in ['frontend', 'ui', 'ux']):
            patterns.append("Frontend development patterns")
        
        if any(word in message_lower for word in ['backend', 'server', 'service']):
            patterns.append("Backend service architecture")
        
        # Add tech stack specific patterns
        if 'python' in tech_stack.lower():
            patterns.append("Python development best practices")
        
        if 'sqlite' in tech_stack.lower():
            patterns.append("SQLite database patterns")
        
        if 'mcp' in tech_stack.lower():
            patterns.append("Model Context Protocol integration")
        
        return patterns if patterns else ["General development patterns"]
    
    def _get_best_practices(self, context_type: str) -> List[str]:
        """Get best practices based on context type"""
        practices = {
            'technical': [
                "Follow DRY (Don't Repeat Yourself) principle",
                "Implement proper error handling and logging",
                "Write comprehensive tests for critical functionality",
                "Use type hints and documentation",
                "Follow PEP 8 style guidelines",
                "Implement proper security measures"
            ],
            'conversation': [
                "Maintain conversation continuity",
                "Reference previous interactions appropriately",
                "Adapt to user's communication style",
                "Provide clear and actionable responses",
                "Ask clarifying questions when needed"
            ],
            'comprehensive': [
                "Combine technical and conversational approaches",
                "Provide context-aware recommendations",
                "Suggest next steps and improvements",
                "Maintain project awareness",
                "Leverage user preferences effectively"
            ]
        }
        
        return practices.get(context_type, practices['comprehensive'])
    
    def _get_common_issues(self, context_type: str) -> List[str]:
        """Get common issues based on context type"""
        issues = {
            'technical': [
                "Configuration and environment setup",
                "Dependency management and version conflicts",
                "Performance bottlenecks and optimization",
                "Error handling and debugging",
                "Testing and deployment challenges"
            ],
            'conversation': [
                "Context loss between interactions",
                "Unclear user requirements",
                "Communication style mismatches",
                "Information overload in responses"
            ],
            'comprehensive': [
                "Technical and communication challenges",
                "Project context management",
                "User preference adaptation",
                "Performance and usability balance"
            ]
        }
        
        return issues.get(context_type, issues['comprehensive'])
    
    def _get_development_workflow(self, context_type: str) -> List[str]:
        """Get development workflow based on context type"""
        workflows = {
            'technical': [
                "Plan and design the solution",
                "Implement with best practices",
                "Test thoroughly",
                "Review and refactor",
                "Deploy and monitor"
            ],
            'conversation': [
                "Understand user needs",
                "Provide relevant information",
                "Suggest next steps",
                "Maintain engagement"
            ],
            'comprehensive': [
                "Analyze requirements and context",
                "Design comprehensive solution",
                "Implement with best practices",
                "Test and validate",
                "Deploy and monitor",
                "Maintain conversation continuity"
            ]
        }
        
        return workflows.get(context_type, workflows['comprehensive'])
    
    def _calculate_confidence_score(self, 
                                  recent_interactions: List, 
                                  tech_stack: str, 
                                  project_plans: str) -> float:
        """Calculate confidence score based on available data quality"""
        score = 0.0
        
        # Interaction quality (40% weight)
        if recent_interactions:
            score += 0.4 * min(len(recent_interactions) / 10.0, 1.0)
        
        # Tech stack completeness (30% weight)
        if tech_stack and tech_stack != "Tech stack detection failed":
            score += 0.3
        
        # Project plans completeness (30% weight)
        if project_plans and project_plans != "Project plans unavailable":
            score += 0.3
        
        return min(score, 1.0)
    
    def _is_cache_valid(self, cached_result: Dict[str, Any]) -> bool:
        """Check if cached result is still valid"""
        if 'timestamp' not in cached_result:
            return False
        
        cache_age = datetime.now() - datetime.fromisoformat(cached_result['timestamp'])
        return cache_age.total_seconds() < 300  # 5 minutes cache validity
    
    def _cache_result(self, cache_key: str, original: str, enhanced: str, context_type: str):
        """Cache the generated prompt result"""
        self.context_cache[cache_key] = {
            'original': original,
            'enhanced_prompt': enhanced,
            'context_type': context_type,
            'timestamp': datetime.now().isoformat(),
            'enhancement_size': len(enhanced) - len(original)
        }
        
        # Keep cache manageable
        if len(self.context_cache) > 100:
            oldest_keys = sorted(self.context_cache.keys(), 
                               key=lambda k: self.context_cache[k]['timestamp'])[:20]
            for key in oldest_keys:
                del self.context_cache[key]
    
    def _update_stats(self, success: bool, start_time: datetime):
        """Update generation statistics"""
        self.enhancement_stats['total_generated'] += 1
        
        if success:
            self.enhancement_stats['successful_generations'] += 1
            self.enhancement_stats['last_generation'] = datetime.now().isoformat()
            
            # Calculate generation time
            generation_time = (datetime.now() - start_time).total_seconds()
            current_avg = self.enhancement_stats['average_generation_time']
            total_successful = self.enhancement_stats['successful_generations']
            
            # Update running average
            self.enhancement_stats['average_generation_time'] = (
                (current_avg * (total_successful - 1) + generation_time) / total_successful
            )
        else:
            self.enhancement_stats['failed_generations'] += 1
    
    def _convert_to_appe_context(self, context: PromptContext) -> Dict[str, Any]:
        """Convert PromptContext to APPE-compatible format."""
        return {
            "conversation_summary": context.conversation_summary,
            "action_history": context.action_history,
            "tech_stack": context.tech_stack,
            "project_plans": context.project_plans,
            "user_preferences": context.user_preferences,
            "agent_metadata": context.agent_metadata,
            "recent_interactions": context.recent_interactions,
            "project_patterns": context.project_patterns,
            "best_practices": context.best_practices,
            "common_issues": context.common_issues,
            "development_workflow": context.development_workflow,
            "confidence_score": context.confidence_score,
            "project_structure": context.project_structure,
            "project_overview": context.project_overview,
            "function_summary": context.function_summary,
            "class_summary": context.class_summary
        }
    
    def learn_from_interaction(self, 
                             user_message: str, 
                             enhanced_prompt: str,
                             user_feedback: float,
                             response_quality: float,
                             execution_time: float):
        """Learn from interaction outcomes to improve future prompts."""
        if APPE_AVAILABLE:
            try:
                learn_from_appe_interaction(
                    user_message, enhanced_prompt, user_feedback, response_quality, execution_time
                )
                logger.info(f"📚 APPE learned from interaction (feedback: {user_feedback}, quality: {response_quality})")
            except Exception as e:
                logger.warning(f"Failed to update APPE learning: {e}")
    
    def get_appe_status(self) -> Dict[str, Any]:
        """Get APPE system status if available."""
        if APPE_AVAILABLE:
            try:
                appe = get_adaptive_prompt_engine()
                return appe.get_system_status()
            except Exception as e:
                return {"error": f"Failed to get APPE status: {e}"}
        else:
            return {"status": "not_available", "message": "APPE not installed"}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current generation statistics"""
        base_stats = {
            **self.enhancement_stats,
            'cache_size': len(self.context_cache),
            'success_rate': (
                f"{self.enhancement_stats['successful_generations']}/{self.enhancement_stats['total_generated']}"
                if self.enhancement_stats['total_generated'] > 0 else "0/0"
            ),
            'cache_hit_rate': (
                f"{self.enhancement_stats['context_cache_hits']}/{self.enhancement_stats['context_cache_hits'] + self.enhancement_stats['context_cache_misses']}"
                if (self.enhancement_stats['context_cache_hits'] + self.enhancement_stats['context_cache_misses']) > 0 else "0/0"
            ),
            'appe_available': APPE_AVAILABLE
        }
        
        # Add APPE statistics if available
        if APPE_AVAILABLE:
            try:
                appe_status = self.get_appe_status()
                base_stats['appe_status'] = appe_status
            except Exception as e:
                base_stats['appe_error'] = str(e)
        
        return base_stats
    
    def clear_cache(self):
        """Clear the context cache"""
        self.context_cache.clear()
        logger.info("Context cache cleared")
    
    def get_available_strategies(self) -> List[str]:
        """Get list of available enhancement strategies"""
        return list(self.enhancement_strategies.keys())

    def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze complete project directory structure and extract function summaries"""
        try:
            import os
            import ast
            from pathlib import Path
            
            project_root = Path("/Users/jonathanmorand/Documents/ProjectsFolder/MCP_FOLDER/MCP/MCP")
            project_structure = {
                'root': str(project_root),
                'directories': {},
                'files': {},
                'functions': {},
                'classes': {},
                'imports': {},
                'technology_stack': set()
            }
            
            # Walk through project directory
            for root, dirs, files in os.walk(project_root):
                # Skip common directories that don't add value
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'env', 'ui_env']]
                
                rel_path = os.path.relpath(root, project_root)
                if rel_path == '.':
                    rel_path = 'root'
                
                project_structure['directories'][rel_path] = {
                    'path': root,
                    'files': [],
                    'subdirs': dirs
                }
                
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.html', '.css', '.md', '.txt', '.sh', '.sql')):
                        file_path = os.path.join(root, file)
                        rel_file_path = os.path.join(rel_path, file) if rel_path != 'root' else file
                        
                        project_structure['files'][rel_file_path] = {
                            'path': file_path,
                            'size': os.path.getsize(file_path),
                            'type': file.split('.')[-1],
                            'functions': [],
                            'classes': [],
                            'imports': []
                        }
                        
                        project_structure['directories'][rel_path]['files'].append(file)
                        
                        # Analyze Python files for functions and classes
                        if file.endswith('.py'):
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # Parse AST to extract functions and classes
                                try:
                                    tree = ast.parse(content)
                                    for node in ast.walk(tree):
                                        if isinstance(node, ast.FunctionDef):
                                            func_name = f"{rel_file_path}:{node.name}"
                                            project_structure['functions'][func_name] = {
                                                'file': rel_file_path,
                                                'name': node.name,
                                                'lineno': node.lineno,
                                                'args': [arg.arg for arg in node.args.args],
                                                'docstring': ast.get_docstring(node) or "No docstring",
                                                'decorators': [d.id for d in node.decorator_list if hasattr(d, 'id')]
                                            }
                                            
                                        elif isinstance(node, ast.ClassDef):
                                            class_name = f"{rel_file_path}:{node.name}"
                                            project_structure['classes'][class_name] = {
                                                'file': rel_file_path,
                                                'name': node.name,
                                                'lineno': node.lineno,
                                                'docstring': ast.get_docstring(node) or "No docstring",
                                                'methods': [],
                                                'bases': [base.id for base in node.bases if hasattr(base, 'id')]
                                            }
                                            
                                        elif isinstance(node, ast.Import):
                                            for alias in node.names:
                                                project_structure['files'][rel_file_path]['imports'].append(alias.name)
                                                
                                        elif isinstance(node, ast.ImportFrom):
                                            module = node.module or ''
                                            for alias in node.names:
                                                project_structure['files'][rel_file_path]['imports'].append(f"{module}.{alias.name}")
                                
                                except SyntaxError:
                                    # Skip files with syntax errors
                                    pass
                                    
                            except Exception as e:
                                # Skip files that can't be read
                                pass
                        
                        # Detect technology stack based on file extensions and content
                        if file.endswith('.py'):
                            project_structure['technology_stack'].add('Python')
                        elif file.endswith('.js'):
                            project_structure['technology_stack'].add('JavaScript')
                        elif file.endswith('.ts'):
                            project_structure['technology_stack'].add('TypeScript')
                        elif file.endswith('.html'):
                            project_structure['technology_stack'].add('HTML')
                        elif file.endswith('.css'):
                            project_structure['technology_stack'].add('CSS')
                        elif file.endswith('.sql'):
                            project_structure['technology_stack'].add('SQL')
                        elif file.endswith('.sh'):
                            project_structure['technology_stack'].add('Shell')
            
            # Convert set to list for JSON serialization
            project_structure['technology_stack'] = list(project_structure['technology_stack'])
            
            return project_structure
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze project structure: {e}")
            return {
                'root': str(Path.cwd()),
                'directories': {},
                'files': {},
                'functions': {},
                'classes': {},
                'imports': {},
                'technology_stack': ['Python']  # Fallback
            }
    
    def _generate_project_overview(self, project_structure: Dict[str, Any]) -> str:
        """Generate a comprehensive project overview from structure analysis"""
        try:
            overview = []
            overview.append("=== 🏗️ PROJECT STRUCTURE OVERVIEW ===")
            
            # Project root
            overview.append(f"📁 Project Root: {project_structure['root']}")
            overview.append(f"🔧 Technology Stack: {', '.join(project_structure['technology_stack'])}")
            overview.append("")
            
            # Directory structure
            overview.append("📂 Directory Structure:")
            for dir_path, dir_info in project_structure['directories'].items():
                if dir_path == 'root':
                    overview.append(f"  📁 / (root)")
                else:
                    overview.append(f"  📁 /{dir_path}/")
                
                # Show key files in each directory
                key_files = [f for f in dir_info['files'] if not f.startswith('.') and f not in ['__init__.py']]
                if key_files:
                    for file in key_files[:5]:  # Show first 5 files
                        overview.append(f"    📄 {file}")
                    if len(key_files) > 5:
                        overview.append(f"    ... and {len(key_files) - 5} more files")
                overview.append("")
            
            # Function summary
            if project_structure['functions']:
                overview.append("🔧 Key Functions:")
                func_count = 0
                for func_name, func_info in list(project_structure['functions'].items())[:10]:  # Show first 10
                    overview.append(f"  ⚡ {func_info['name']}() - {func_info['docstring'][:100]}...")
                    func_count += 1
                if len(project_structure['functions']) > 10:
                    overview.append(f"  ... and {len(project_structure['functions']) - 10} more functions")
                overview.append("")
            
            # Class summary
            if project_structure['classes']:
                overview.append("🏗️ Key Classes:")
                class_count = 0
                for class_name, class_info in list(project_structure['classes'].items())[:10]:  # Show first 10
                    overview.append(f"  🏛️ {class_info['name']} - {class_info['docstring'][:100]}...")
                    class_count += 1
                if len(project_structure['classes']) > 10:
                    overview.append(f"  ... and {len(project_structure['classes']) - 10} more classes")
                overview.append("")
            
            # File type summary
            file_types = {}
            for file_path, file_info in project_structure['files'].items():
                file_type = file_info['type']
                file_types[file_type] = file_types.get(file_type, 0) + 1
            
            overview.append("📊 File Distribution:")
            for file_type, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
                overview.append(f"  📄 {file_type.upper()}: {count} files")
            
            return "\n".join(overview)
            
        except Exception as e:
            logger.error(f"❌ Failed to generate project overview: {e}")
            return "⚠️ Project overview generation failed"
    
    def _get_function_summary(self, project_structure: Dict[str, Any]) -> str:
        """Generate a detailed function summary for context injection"""
        try:
            if not project_structure['functions']:
                return "No functions found in project structure"
            
            summary = []
            summary.append("=== 🔧 FUNCTION SUMMARY ===")
            
            # Group functions by file
            functions_by_file = {}
            for func_name, func_info in project_structure['functions'].items():
                file_path = func_info['file']
                if file_path not in functions_by_file:
                    functions_by_file[file_path] = []
                functions_by_file[file_path].append(func_info)
            
            # Generate summary by file
            for file_path, functions in functions_by_file.items():
                summary.append(f"📁 {file_path}:")
                for func_info in functions:
                    args_str = ", ".join(func_info['args']) if func_info['args'] else "no args"
                    summary.append(f"  ⚡ {func_info['name']}({args_str})")
                    if func_info['docstring'] and func_info['docstring'] != "No docstring":
                        doc_preview = func_info['docstring'][:80] + "..." if len(func_info['docstring']) > 80 else func_info['docstring']
                        summary.append(f"    💬 {doc_preview}")
                summary.append("")
            
            return "\n".join(summary)
            
        except Exception as e:
            logger.error(f"❌ Failed to generate function summary: {e}")
            return "⚠️ Function summary generation failed"
    
    def _get_class_summary(self, project_structure: Dict[str, Any]) -> str:
        """Generate a detailed class summary for context injection"""
        try:
            if not project_structure['classes']:
                return "No classes found in project structure"
            
            summary = []
            summary.append("=== 🏗️ CLASS SUMMARY ===")
            
            # Group classes by file
            classes_by_file = {}
            for class_name, class_info in project_structure['classes'].items():
                file_path = class_info['file']
                if file_path not in classes_by_file:
                    classes_by_file[file_path] = []
                classes_by_file[file_path].append(class_info)
            
            # Generate summary by file
            for file_path, classes in classes_by_file.items():
                summary.append(f"📁 {file_path}:")
                for class_info in classes:
                    bases_str = f"({', '.join(class_info['bases'])})" if class_info['bases'] else ""
                    summary.append(f"  🏛️ class {class_info['name']}{bases_str}")
                    if class_info['docstring'] and class_info['docstring'] != "No docstring":
                        doc_preview = class_info['docstring'][:80] + "..." if len(class_info['docstring']) > 80 else class_info['docstring']
                        summary.append(f"    💬 {doc_preview}")
                summary.append("")
            
            return "\n".join(summary)
            
        except Exception as e:
            logger.error(f"❌ Failed to generate class summary: {e}")
            return "⚠️ Class summary generation failed"

    def _analyze_user_intent(self, user_message: str, context: PromptContext) -> Dict[str, Any]:
        """Analyze user message to determine intent and required context"""
        intent_analysis = {
            'primary_intent': 'general',
            'context_priority': [],
            'required_sections': [],
            'tone': 'professional',
            'complexity': 'medium',
            'urgency': 'normal'
        }
        
        message_lower = user_message.lower()
        
        # Detect primary intent
        if any(word in message_lower for word in ['error', 'fail', 'break', 'fix', 'issue']):
            intent_analysis['primary_intent'] = 'troubleshooting'
            intent_analysis['urgency'] = 'high'
            intent_analysis['required_sections'] = ['tech_stack', 'error_context', 'recent_actions']
            
        elif any(word in message_lower for word in ['how', 'what', 'explain', 'understand']):
            intent_analysis['primary_intent'] = 'explanation'
            intent_analysis['complexity'] = 'high'
            intent_analysis['required_sections'] = ['project_context', 'tech_stack', 'best_practices', 'project_structure']
            
        elif any(word in message_lower for word in ['create', 'build', 'implement', 'develop']):
            intent_analysis['primary_intent'] = 'development'
            intent_analysis['required_sections'] = ['project_structure', 'tech_stack', 'development_workflow', 'function_summary', 'class_summary']
            
        elif any(word in message_lower for word in ['optimize', 'improve', 'enhance', 'refactor']):
            intent_analysis['primary_intent'] = 'optimization'
            intent_analysis['required_sections'] = ['project_patterns', 'best_practices', 'performance_metrics']
            
        elif any(word in message_lower for word in ['test', 'validate', 'verify', 'check']):
            intent_analysis['primary_intent'] = 'testing'
            intent_analysis['required_sections'] = ['recent_actions', 'error_context', 'development_workflow']
            
        elif any(word in message_lower for word in ['start', 'run', 'launch', 'deploy']):
            intent_analysis['primary_intent'] = 'execution'
            intent_analysis['required_sections'] = ['tech_stack', 'project_context', 'current_status']
        
        # Detect tone and complexity
        if any(word in message_lower for word in ['urgent', 'asap', 'now', 'quick']):
            intent_analysis['urgency'] = 'high'
            intent_analysis['complexity'] = 'low'
            
        if any(word in message_lower for word in ['simple', 'basic', 'easy']):
            intent_analysis['complexity'] = 'low'
            
        if any(word in message_lower for word in ['complex', 'advanced', 'detailed']):
            intent_analysis['complexity'] = 'high'
        
        # Determine context priority based on intent
        if intent_analysis['primary_intent'] == 'troubleshooting':
            intent_analysis['context_priority'] = ['error_context', 'recent_actions', 'tech_stack', 'common_issues']
        elif intent_analysis['primary_intent'] == 'development':
            intent_analysis['context_priority'] = ['project_structure', 'tech_stack', 'development_workflow', 'best_practices']
        elif intent_analysis['primary_intent'] == 'explanation':
            intent_analysis['context_priority'] = ['project_context', 'tech_stack', 'recent_actions', 'user_preferences']
        else:
            intent_analysis['context_priority'] = ['conversation_summary', 'tech_stack', 'project_context', 'recent_actions']
        
        return intent_analysis
    
    def _craft_dynamic_prompt(self, user_message: str, context: PromptContext, intent_analysis: Dict[str, Any]) -> str:
        """Dynamically craft a prompt based on user intent and context"""
        
        # Start with user message
        prompt_parts = [f"USER MESSAGE: {user_message}"]
        
        # Add context based on intent priority
        for section in intent_analysis['context_priority']:
            if section == 'conversation_summary' and context.conversation_summary:
                if intent_analysis['complexity'] == 'low':
                    prompt_parts.append(f"CONTEXT: {context.conversation_summary[:300]}...")
                else:
                    prompt_parts.append(f"CONVERSATION CONTEXT: {context.conversation_summary}")
                    
            elif section == 'tech_stack' and context.tech_stack:
                prompt_parts.append(f"TECH STACK: {context.tech_stack}")
                
            elif section == 'project_context' and context.project_plans:
                prompt_parts.append(f"PROJECT CONTEXT: {context.project_plans}")
                
            elif section == 'recent_actions' and context.action_history:
                if intent_analysis['urgency'] == 'high':
                    prompt_parts.append(f"RECENT ACTIONS: {context.action_history[:400]}...")
                else:
                    prompt_parts.append(f"ACTION HISTORY: {context.action_history}")
                    
            elif section == 'project_structure' and context.project_overview:
                if intent_analysis['complexity'] == 'high':
                    prompt_parts.append(f"PROJECT STRUCTURE:\n{context.project_overview}")
                else:
                    prompt_parts.append(f"PROJECT: {context.project_overview.split('📁')[0] if '📁' in context.project_overview else context.project_overview[:300]}...")
                    
            elif section == 'development_workflow' and context.development_workflow:
                prompt_parts.append(f"WORKFLOW: {' | '.join(context.development_workflow[:3])}")
                
            elif section == 'best_practices' and context.best_practices:
                prompt_parts.append(f"BEST PRACTICES: {' | '.join(context.best_practices[:3])}")
                
            elif section == 'common_issues' and context.common_issues:
                prompt_parts.append(f"COMMON ISSUES: {' | '.join(context.common_issues[:3])}")
                
            elif section == 'user_preferences' and context.user_preferences:
                if intent_analysis['complexity'] == 'high':
                    prompt_parts.append(f"USER PREFERENCES: {context.user_preferences}")
                else:
                    prompt_parts.append(f"PREFERENCES: {context.user_preferences[:300]}...")
        
        # Add project structure information when relevant
        if intent_analysis['primary_intent'] in ['development', 'explanation', 'optimization']:
            if context.project_overview:
                if intent_analysis['complexity'] == 'high':
                    prompt_parts.append(f"🏗️ PROJECT STRUCTURE:\n{context.project_overview}")
                else:
                    prompt_parts.append(f"🏗️ PROJECT: {context.project_overview.split('📁')[0] if '📁' in context.project_overview else context.project_overview[:400]}...")
            
            if context.function_summary and intent_analysis['complexity'] == 'high':
                prompt_parts.append(f"🔧 AVAILABLE FUNCTIONS:\n{context.function_summary}")
            
            if context.class_summary and intent_analysis['complexity'] == 'high':
                prompt_parts.append(f"🏛️ AVAILABLE CLASSES:\n{context.class_summary}")
        
        # Add confidence score if low
        if context.confidence_score < 0.5:
            prompt_parts.append(f"⚠️ CONTEXT CONFIDENCE: {context.confidence_score:.1%} (limited context available)")
        
        # Add urgency indicator
        if intent_analysis['urgency'] == 'high':
            prompt_parts.append("🚨 URGENT: Please provide quick, actionable response")
        
        # Add complexity guidance
        if intent_analysis['complexity'] == 'low':
            prompt_parts.append("💡 Keep response simple and direct")
        elif intent_analysis['complexity'] == 'high':
            prompt_parts.append("🔍 Provide detailed, comprehensive response")
        
        # Add intent-specific instructions
        if intent_analysis['primary_intent'] == 'troubleshooting':
            prompt_parts.append("🎯 FOCUS: Identify and solve the specific issue")
        elif intent_analysis['primary_intent'] == 'development':
            prompt_parts.append("🎯 FOCUS: Provide implementation guidance and code examples")
        elif intent_analysis['primary_intent'] == 'explanation':
            prompt_parts.append("🎯 FOCUS: Explain concepts clearly with examples")
        elif intent_analysis['primary_intent'] == 'optimization':
            prompt_parts.append("🎯 FOCUS: Suggest improvements and optimization strategies")
        
        # Add conversation continuity
        if context.recent_interactions:
            prompt_parts.append("🔄 MAINTAIN: Build upon our conversation history and previous solutions")
        
        # Join all parts with clean separators
        dynamic_prompt = "\n\n".join(prompt_parts)
        
        return dynamic_prompt
    
    def _generate_smart_prompt(self, user_message: str, context: PromptContext) -> str:
        """Generate a smart, context-aware prompt using dynamic crafting"""
        try:
            # Analyze user intent
            intent_analysis = self._analyze_user_intent(user_message, context)
            
            # Craft dynamic prompt
            dynamic_prompt = self._craft_dynamic_prompt(user_message, context, intent_analysis)
            
            # Add metadata for tracking
            prompt_metadata = f"""
=== DYNAMIC PROMPT METADATA ===
Intent: {intent_analysis['primary_intent']}
Complexity: {intent_analysis['complexity']}
Urgency: {intent_analysis['urgency']}
Context Sections: {', '.join(intent_analysis['context_priority'])}
Confidence: {context.confidence_score:.1%}
Generated: {datetime.now(timezone.utc).isoformat()}
=== END METADATA ===

{dynamic_prompt}
            """.strip()
            
            return prompt_metadata
            
        except Exception as e:
            logger.error(f"Smart prompt generation failed: {e}")
            # Fallback to comprehensive prompt
            return self._generate_comprehensive_prompt(user_message, context)

# Global instance for easy access
prompt_generator = PromptGenerator()

# Convenience functions
def generate_comprehensive_prompt(user_message: str) -> str:
    """Generate a comprehensive enhanced prompt"""
    return prompt_generator.generate_enhanced_prompt(user_message, "comprehensive")

def generate_technical_prompt(user_message: str) -> str:
    """Generate a technical-focused enhanced prompt"""
    return prompt_generator.generate_enhanced_prompt(user_message, "technical")

def generate_conversation_prompt(user_message: str) -> str:
    """Generate a conversation-focused enhanced prompt"""
    return prompt_generator.generate_enhanced_prompt(user_message, "conversation")

def generate_smart_prompt(user_message: str) -> str:
    """Generate a smart, adaptive enhanced prompt"""
    return prompt_generator.generate_enhanced_prompt(user_message, "smart")

def generate_minimal_prompt(user_message: str) -> str:
    """Generate a minimal context enhanced prompt"""
    return prompt_generator.generate_enhanced_prompt(user_message, "minimal")

if __name__ == "__main__":
    # Test the prompt generator
    test_message = "How do I set up the database for this project?"
    
    print("🧪 Testing Prompt Generator...")
    print(f"📝 Original message: {test_message}")
    print()
    
    # Test different strategies
    strategies = ["comprehensive", "technical", "conversation", "smart", "minimal"]
    
    for strategy in strategies:
        print(f"🚀 Testing {strategy.upper()} strategy:")
        enhanced = prompt_generator.generate_enhanced_prompt(test_message, strategy)
        print(f"   Length: {len(test_message)} -> {len(enhanced)} chars (+{len(enhanced) - len(test_message)})")
        print(f"   Preview: {enhanced[:100]}...")
        print()
    
    # Show statistics
    stats = prompt_generator.get_stats()
    print("📊 Generation Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
