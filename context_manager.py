#!/usr/bin/env python3
"""
Seamless Context Integration Manager
Coordinates all context systems and provides a unified interface
"""

import sys
import os
import uuid
from typing import Dict, Any, Optional, List, Union
from datetime import datetime, timedelta
import logging
import json

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeamlessContextManager:
    """
    Seamless context integration manager that coordinates all context systems
    
    This system provides:
    1. Unified interface for all context operations
    2. Automatic context enhancement for every interaction
    3. Real-time context injection capabilities
    4. Seamless integration with existing systems
    5. Performance monitoring and optimization
    """
    
    def __init__(self, auto_start: bool = True):
        self.auto_start = auto_start
        self.session_id = str(uuid.uuid4())
        self.is_active = False
        self.context_systems = {}
        self.enhancement_pipeline = []
        self.performance_tracker = {}
        self.user_preferences = {}
        self.active_conversations = {}
        
        # Initialize context systems
        self._initialize_context_systems()
        
        if auto_start:
            self.start()
    
    def _initialize_context_systems(self):
        """Initialize all available context systems"""
        try:
            # Import and initialize auto context wrapper
            from auto_context_wrapper import auto_context_wrapper
            self.context_systems['auto_wrapper'] = {
                'instance': auto_context_wrapper,
                'status': 'available',
                'capabilities': ['prompt_enhancement', 'context_injection', 'caching']
            }
            logger.info("✅ Auto context wrapper initialized")
            
        except ImportError as e:
            logger.warning(f"⚠️ Auto context wrapper not available: {e}")
            self.context_systems['auto_wrapper'] = {
                'instance': None,
                'status': 'unavailable',
                'capabilities': []
            }
        
        try:
            # Import and initialize real-time injector
            from automatic_context_system import real_time_injector
            self.context_systems['real_time'] = {
                'instance': real_time_injector,
                'status': 'available',
                'capabilities': ['real_time_injection', 'performance_tracking', 'caching']
            }
            logger.info("✅ Real-time context injector initialized")
            
        except ImportError as e:
            logger.warning(f"⚠️ Real-time context injector not available: {e}")
            self.context_systems['real_time'] = {
                'instance': None,
                'status': 'unavailable',
                'capabilities': []
            }
        
        try:
            # Import MCP server functions
            from local_mcp_server_simple import (
                enhanced_chat, process_prompt_with_context
            )
            self.context_systems['mcp_server'] = {
                'instance': {
                    'enhanced_chat': enhanced_chat,
                    'process_prompt_with_context': process_prompt_with_context
                },
                'status': 'available',
                'capabilities': ['mcp_integration', 'enhanced_chat', 'prompt_processing']
            }
            logger.info("✅ MCP server context functions initialized")
            
        except ImportError as e:
            logger.warning(f"⚠️ MCP server context functions not available: {e}")
            self.context_systems['mcp_server'] = {
                'instance': None,
                'status': 'unavailable',
                'capabilities': []
            }
    
    def start(self):
        """Start the seamless context manager"""
        if self.is_active:
            logger.info("Seamless context manager is already active")
            return
        
        self.is_active = True
        self.session_id = str(uuid.uuid4())
        
        # Start available systems
        for system_name, system_info in self.context_systems.items():
            if system_info['status'] == 'available' and hasattr(system_info['instance'], 'start'):
                try:
                    system_info['instance'].start()
                    logger.info(f"🚀 Started {system_name} context system")
                except Exception as e:
                    logger.error(f"❌ Failed to start {system_name}: {e}")
        
        logger.info(f"🚀 Seamless context manager started (Session: {self.session_id})")
    
    def stop(self):
        """Stop the seamless context manager"""
        if not self.is_active:
            logger.info("Seamless context manager is not active")
            return
        
        self.is_active = False
        
        # Stop available systems
        for system_name, system_info in self.context_systems.items():
            if system_info['status'] == 'available' and hasattr(system_info['instance'], 'stop'):
                try:
                    system_info['instance'].stop()
                    logger.info(f"🛑 Stopped {system_name} context system")
                except Exception as e:
                    logger.error(f"❌ Failed to stop {system_name}: {e}")
        
        logger.info("🛑 Seamless context manager stopped")
    
    def enhance_prompt_seamlessly(self, prompt: str, context_type: str = "general", 
                                use_system: str = "auto") -> str:
        """
        Seamlessly enhance a prompt using the best available context system
        
        Args:
            prompt (str): The original user prompt
            context_type (str): Type of context to inject
            use_system (str): Specific system to use ("auto", "auto_wrapper", "real_time", "mcp_server")
            
        Returns:
            str: Enhanced prompt with injected context
        """
        if not self.is_active:
            logger.warning("⚠️ Context manager not active, returning original prompt")
            return prompt
        
        start_time = datetime.now()
        prompt_id = str(uuid.uuid4())
        
        try:
            # Determine which system to use
            if use_system == "auto":
                system_name = self._select_best_system(context_type)
            else:
                system_name = use_system
            
            # Enhance the prompt using the selected system
            enhanced_prompt = self._enhance_with_system(system_name, prompt_id, prompt, context_type)
            
            # Track performance
            processing_time = (datetime.now() - start_time).total_seconds()
            self._track_performance(system_name, processing_time, len(prompt), len(enhanced_prompt))
            
            # Log the enhancement
            logger.info(f"✅ Seamlessly enhanced prompt {prompt_id[:8]} using {system_name}: {len(prompt)} -> {len(enhanced_prompt)} chars in {processing_time:.3f}s")
            
            return enhanced_prompt
            
        except Exception as e:
            logger.error(f"❌ Seamless enhancement failed: {str(e)}")
            return prompt
    
    def _select_best_system(self, context_type: str) -> str:
        """Select the best available system for the given context type"""
        available_systems = {
            name: info for name, info in self.context_systems.items() 
            if info['status'] == 'available'
        }
        
        if not available_systems:
            return "mcp_server"  # Fallback
        
        # Priority order based on context type
        if context_type == "technical":
            priority_order = ["real_time", "auto_wrapper", "mcp_server"]
        elif context_type == "conversation":
            priority_order = ["auto_wrapper", "mcp_server", "real_time"]
        else:
            priority_order = ["auto_wrapper", "real_time", "mcp_server"]
        
        # Return first available system in priority order
        for system_name in priority_order:
            if system_name in available_systems:
                return system_name
        
        # Fallback to first available system
        return list(available_systems.keys())[0]
    
    def _enhance_with_system(self, system_name: str, prompt_id: str, prompt: str, context_type: str) -> str:
        """Enhance prompt using the specified system"""
        system_info = self.context_systems.get(system_name)
        if not system_info or system_info['status'] != 'available':
            raise ValueError(f"System {system_name} is not available")
        
        system_instance = system_info['instance']
        
        if system_name == "auto_wrapper":
            return system_instance.auto_enhance_prompt(prompt, context_type)
        
        elif system_name == "real_time":
            return system_instance.inject_context_real_time(prompt_id, prompt, context_type)
        
        elif system_name == "mcp_server":
            if context_type == "technical":
                return system_instance['process_prompt_with_context'](prompt)
            else:
                return system_instance['enhanced_chat'](prompt)
        
        else:
            raise ValueError(f"Unknown system: {system_name}")
    
    def _track_performance(self, system_name: str, processing_time: float, 
                          original_length: int, enhanced_length: int):
        """Track performance metrics for each system"""
        if system_name not in self.performance_tracker:
            self.performance_tracker[system_name] = {
                'total_processed': 0,
                'total_processing_time': 0.0,
                'average_processing_time': 0.0,
                'total_enhancement_size': 0,
                'average_enhancement_size': 0
            }
        
        tracker = self.performance_tracker[system_name]
        tracker['total_processed'] += 1
        tracker['total_processing_time'] += processing_time
        tracker['total_enhancement_size'] += (enhanced_length - original_length)
        
        # Update averages
        tracker['average_processing_time'] = tracker['total_processing_time'] / tracker['total_processed']
        tracker['average_enhancement_size'] = tracker['total_enhancement_size'] / tracker['total_processed']
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all context systems"""
        status = {
            'manager_active': self.is_active,
            'session_id': self.session_id,
            'systems': {}
        }
        
        for system_name, system_info in self.context_systems.items():
            status['systems'][system_name] = {
                'status': system_info['status'],
                'capabilities': system_info['capabilities'],
                'performance': self.performance_tracker.get(system_name, {})
            }
        
        return status
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get overall performance summary"""
        total_processed = sum(
            tracker.get('total_processed', 0) 
            for tracker in self.performance_tracker.values()
        )
        
        total_time = sum(
            tracker.get('total_processing_time', 0) 
            for tracker in self.performance_tracker.values()
        )
        
        return {
            'total_prompts_processed': total_processed,
            'total_processing_time': total_time,
            'average_processing_time': total_time / total_processed if total_processed > 0 else 0,
            'system_performance': self.performance_tracker,
            'active_systems': len([s for s in self.context_systems.values() if s['status'] == 'available'])
        }
    
    def create_or_update_context(self, session_id: str, user_id: str = None) -> bool:
        """
        Automatically create or update context for a session based on recent interactions
        
        Args:
            session_id (str): The session ID to create context for
            user_id (str): Optional user ID
            
        Returns:
            bool: True if context was created/updated successfully
        """
        try:
            logger.info(f"🧠 Creating/updating context for session: {session_id}")
            
            # Get recent interactions for this session
            interactions = self._get_session_interactions(session_id)
            if not interactions:
                logger.warning(f"⚠️ No interactions found for session {session_id}")
                return False
            
            # Generate enhanced context
            enhanced_context = self._generate_context_from_interactions(interactions, session_id, user_id)
            
            # Check if context already exists
            existing_context = self._get_existing_context(session_id)
            
            if existing_context:
                # Update existing context
                success = self._update_existing_context(existing_context['id'], enhanced_context)
                logger.info(f"🔄 Updated existing context for session {session_id}")
            else:
                # Create new context
                success = self._create_new_context(enhanced_context)
                logger.info(f"🆕 Created new context for session {session_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Failed to create/update context for session {session_id}: {e}")
            return False
    
    def _get_session_interactions(self, session_id: str) -> List[Dict[str, Any]]:
        """Get recent interactions for a session"""
        try:
            from models_local import get_session_factory, AgentInteraction
            
            session_factory = get_session_factory()
            with session_factory() as db_session:
                # Get interactions from last 24 hours
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                interactions = db_session.query(AgentInteraction).filter(
                    AgentInteraction.session_id == session_id,
                    AgentInteraction.timestamp >= cutoff_time
                ).order_by(AgentInteraction.timestamp.desc()).limit(20).all()
                
                # Convert to dictionaries
                return [
                    {
                        'interaction_type': i.interaction_type,
                        'prompt': i.prompt,
                        'response': i.response,
                        'timestamp': i.timestamp,
                        'status': i.status,
                        'execution_time_ms': i.execution_time_ms
                    }
                    for i in interactions
                ]
                
        except Exception as e:
            logger.error(f"❌ Failed to get session interactions: {e}")
            return []
    
    def _generate_context_from_interactions(self, interactions: List[Dict[str, Any]], 
                                          session_id: str, user_id: str = None) -> Dict[str, Any]:
        """Generate enhanced context from interactions"""
        
        # Extract meaningful content
        prompts = [i['prompt'] for i in interactions if i.get('prompt') and len(str(i['prompt']).strip()) > 5]
        responses = [i['response'] for i in interactions if i.get('response') and len(str(i['response']).strip()) > 5]
        
        # Analyze conversation content
        conversation_themes = self._analyze_conversation_themes(prompts, responses)
        technical_details = self._extract_technical_details(prompts, responses)
        user_intent = self._infer_user_intent(prompts)
        system_status = self._analyze_system_status(interactions)
        
        # Create informative summary
        context_summary = self._create_informative_summary(interactions, conversation_themes, technical_details)
        
        # Enhanced semantic context
        semantic_context = {
            'session_id': session_id,
            'interaction_count': len(interactions),
            'conversation_themes': conversation_themes,
            'technical_focus': technical_details['focus_areas'],
            'user_intent': user_intent,
            'system_performance': system_status,
            'conversation_quality': self._assess_conversation_quality(interactions),
            'key_achievements': self._extract_achievements(responses),
            'challenges_faced': self._extract_challenges(prompts, responses)
        }
        
        # Key topics
        key_topics = list(set(conversation_themes + technical_details['focus_areas'] + user_intent))
        
        # User preferences
        user_preferences = self._infer_detailed_preferences(interactions, prompts, responses)
        
        # Project context
        project_context = {
            'project_name': 'Context Manager System',
            'current_phase': self._determine_project_phase(conversation_themes, technical_details),
            'technologies': technical_details['technologies'],
            'focus_areas': technical_details['focus_areas'],
            'recent_work': self._extract_recent_work(interactions),
            'next_steps': self._infer_next_steps(conversation_themes, technical_details),
            'system_health': system_status
        }
        
        # Calculate relevance
        relevance_score = self._calculate_relevance_score(interactions, conversation_themes, technical_details)
        
        return {
            'session_id': session_id,
            'user_id': user_id,
            'context_summary': context_summary,
            'semantic_context': semantic_context,
            'key_topics': key_topics,
            'user_preferences': user_preferences,
            'project_context': project_context,
            'context_type': 'conversation',
            'relevance_score': relevance_score,
            'usage_count': 0
        }
    
    def _analyze_conversation_themes(self, prompts: List[str], responses: List[str]) -> List[str]:
        """Analyze conversation content for themes"""
        themes = []
        
        for prompt in prompts:
            prompt_lower = str(prompt).lower()
            
            # Technical themes
            if any(word in prompt_lower for word in ['context', 'injection', 'enhancement']):
                themes.append('context enhancement')
            if any(word in prompt_lower for word in ['ui', 'interface', 'dashboard']):
                themes.append('user interface development')
            if any(word in prompt_lower for word in ['database', 'sqlite', 'storage']):
                themes.append('data persistence')
            if any(word in prompt_lower for word in ['mcp', 'protocol', 'server']):
                themes.append('MCP integration')
            if any(word in prompt_lower for word in ['conversation', 'tracking', 'memory']):
                themes.append('conversation management')
            if any(word in prompt_lower for word in ['error', 'fix', 'issue', 'problem']):
                themes.append('troubleshooting')
            if any(word in prompt_lower for word in ['test', 'verify', 'check']):
                themes.append('testing and validation')
            if any(word in prompt_lower for word in ['next', 'step', 'implement', 'build']):
                themes.append('development planning')
        
        # Analyze responses
        for response in responses:
            response_lower = str(response).lower()
            if 'success' in response_lower or 'working' in response_lower:
                themes.append('successful operations')
            if 'error' in response_lower or 'failed' in response_lower:
                themes.append('error handling')
        
        return list(set(themes))
    
    def _extract_technical_details(self, prompts: List[str], responses: List[str]) -> Dict[str, List[str]]:
        """Extract technical details from conversations"""
        technologies = set()
        focus_areas = set()
        
        for prompt in prompts:
            prompt_lower = str(prompt).lower()
            
            # Technologies
            if 'python' in prompt_lower:
                technologies.add('Python')
            if 'sqlite' in prompt_lower:
                technologies.add('SQLite')
            if 'streamlit' in prompt_lower:
                technologies.add('Streamlit')
            if 'mcp' in prompt_lower:
                technologies.add('MCP Protocol')
            if 'sqlalchemy' in prompt_lower:
                technologies.add('SQLAlchemy')
            if 'plotly' in prompt_lower:
                technologies.add('Plotly')
            
            # Focus areas
            if 'context' in prompt_lower:
                focus_areas.add('Context Management')
            if 'ui' in prompt_lower or 'interface' in prompt_lower:
                focus_areas.add('User Interface')
            if 'database' in prompt_lower:
                focus_areas.add('Database Design')
            if 'conversation' in prompt_lower:
                focus_areas.add('Conversation Tracking')
            if 'enhancement' in prompt_lower:
                focus_areas.add('Prompt Enhancement')
        
        return {
            'technologies': list(technologies),
            'focus_areas': list(focus_areas)
        }
    
    def _infer_user_intent(self, prompts: List[str]) -> List[str]:
        """Infer user intent from prompts"""
        intents = []
        
        for prompt in prompts:
            prompt_lower = str(prompt).lower()
            
            if any(word in prompt_lower for word in ['how', 'what', 'why']):
                intents.append('information seeking')
            if any(word in prompt_lower for word in ['fix', 'solve', 'resolve']):
                intents.append('problem solving')
            if any(word in prompt_lower for word in ['build', 'create', 'implement']):
                intents.append('development')
            if any(word in prompt_lower for word in ['test', 'verify', 'check']):
                intents.append('validation')
            if any(word in prompt_lower for word in ['explain', 'understand', 'learn']):
                intents.append('learning')
            if any(word in prompt_lower for word in ['next', 'step', 'continue']):
                intents.append('planning')
        
        return list(set(intents))
    
    def _analyze_system_status(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze system performance and status"""
        total_interactions = len(interactions)
        successful = sum(1 for i in interactions if i.get('status') == 'success')
        errors = sum(1 for i in interactions if i.get('status') == 'error')
        
        # Calculate average execution time
        execution_times = [i.get('execution_time_ms', 0) for i in interactions if i.get('execution_time_ms')]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        return {
            'total_interactions': total_interactions,
            'success_rate': successful / total_interactions if total_interactions > 0 else 0,
            'error_rate': errors / total_interactions if total_interactions > 0 else 0,
            'avg_execution_time_ms': avg_execution_time,
            'system_health': 'healthy' if errors == 0 else 'needs_attention'
        }
    
    def _create_informative_summary(self, interactions: List[Dict[str, Any]], 
                                   themes: List[str], technical_details: Dict[str, List[str]]) -> str:
        """Create informative context summary"""
        if not interactions:
            return "No interactions available"
        
        # Count interaction types
        type_counts = {}
        for interaction in interactions:
            interaction_type = interaction.get('interaction_type', 'unknown')
            type_counts[interaction_type] = type_counts.get(interaction_type, 0) + 1
        
        # Create rich summary
        summary_parts = []
        
        if type_counts.get('client_request', 0) > 0:
            summary_parts.append(f"{type_counts['client_request']} user requests")
        if type_counts.get('agent_response', 0) > 0:
            summary_parts.append(f"{type_counts['agent_response']} system responses")
        if type_counts.get('conversation_turn', 0) > 0:
            summary_parts.append(f"{type_counts['conversation_turn']} conversation turns")
        
        summary = f"Session with {', '.join(summary_parts)}"
        
        # Add technical focus
        if technical_details['focus_areas']:
            summary += f". Focus: {', '.join(technical_details['focus_areas'][:3])}"
        
        # Add key themes
        if themes:
            summary += f". Themes: {', '.join(themes[:3])}"
        
        # Add recent work
        recent_prompts = [i.get('prompt', '') for i in interactions if i.get('prompt') and len(str(i.get('prompt', ''))) > 10][:2]
        if recent_prompts:
            summary += f". Recent: {', '.join([str(p)[:40] + '...' for p in recent_prompts])}"
        
        return summary
    
    def _assess_conversation_quality(self, interactions: List[Dict[str, Any]]) -> str:
        """Assess conversation quality"""
        if not interactions:
            return 'unknown'
        
        meaningful = sum(1 for i in interactions 
                        if i.get('prompt') and len(str(i.get('prompt', '')).strip()) > 10 and 
                           i.get('response') and len(str(i.get('response', '')).strip()) > 10)
        
        ratio = meaningful / len(interactions)
        
        if ratio >= 0.8:
            return 'excellent'
        elif ratio >= 0.6:
            return 'good'
        elif ratio >= 0.4:
            return 'fair'
        else:
            return 'poor'
    
    def _extract_achievements(self, responses: List[str]) -> List[str]:
        """Extract achievements from responses"""
        achievements = []
        
        for response in responses:
            response_lower = str(response).lower()
            if 'success' in response_lower or 'working' in response_lower:
                achievements.append('successful operation')
            if 'created' in response_lower or 'built' in response_lower:
                achievements.append('system creation')
            if 'fixed' in response_lower or 'resolved' in response_lower:
                achievements.append('issue resolution')
            if 'enhanced' in response_lower or 'improved' in response_lower:
                achievements.append('system enhancement')
        
        return list(set(achievements))
    
    def _extract_challenges(self, prompts: List[str], responses: List[str]) -> List[str]:
        """Extract challenges faced"""
        challenges = []
        
        for prompt in prompts:
            prompt_lower = str(prompt).lower()
            if any(word in prompt_lower for word in ['error', 'issue', 'problem', 'fix']):
                challenges.append('technical issues')
            if any(word in prompt_lower for word in ['how', 'what', 'why']):
                challenges.append('information gaps')
            if any(word in prompt_lower for word in ['implement', 'build', 'create']):
                challenges.append('development complexity')
        
        return list(set(challenges))
    
    def _infer_detailed_preferences(self, interactions: List[Dict[str, Any]], 
                                   prompts: List[str], responses: List[str]) -> Dict[str, bool]:
        """Infer user preferences from behavior"""
        preferences = {
            'prefers_local': True,
            'focus_on_context': True,
            'likes_visualization': True,
            'prefers_simple_solutions': True,
            'values_performance': True,
            'appreciates_detailed_responses': True
        }
        
        for prompt in prompts:
            prompt_lower = str(prompt).lower()
            
            if 'simple' in prompt_lower or 'easy' in prompt_lower:
                preferences['prefers_simple_solutions'] = True
            if 'fast' in prompt_lower or 'performance' in prompt_lower:
                preferences['values_performance'] = True
            if 'explain' in prompt_lower or 'detail' in prompt_lower:
                preferences['appreciates_detailed_responses'] = True
            if 'visual' in prompt_lower or 'chart' in prompt_lower:
                preferences['likes_visualization'] = True
        
        return preferences
    
    def _determine_project_phase(self, themes: List[str], technical_details: Dict[str, List[str]]) -> str:
        """Determine current project phase"""
        if 'user interface' in themes or 'dashboard' in themes:
            return 'UI Development & Testing'
        elif 'context enhancement' in themes or 'prompt enhancement' in themes:
            return 'Core System Enhancement'
        elif 'database' in themes or 'data persistence' in themes:
            return 'Data Infrastructure'
        elif 'mcp integration' in themes:
            return 'Protocol Integration'
        elif 'conversation management' in themes:
            return 'Conversation System'
        else:
            return 'General Development'
    
    def _extract_recent_work(self, interactions: List[Dict[str, Any]]) -> List[str]:
        """Extract recent work from interactions"""
        recent_work = []
        
        for interaction in interactions:
            prompt = interaction.get('prompt', '')
            if prompt and len(str(prompt)) > 10:
                prompt_lower = str(prompt).lower()
                if 'test' in prompt_lower:
                    recent_work.append('testing')
                if 'build' in prompt_lower or 'create' in prompt_lower:
                    recent_work.append('development')
                if 'fix' in prompt_lower or 'resolve' in prompt_lower:
                    recent_work.append('troubleshooting')
                if 'enhance' in prompt_lower or 'improve' in prompt_lower:
                    recent_work.append('enhancement')
        
        return list(set(recent_work))
    
    def _infer_next_steps(self, themes: List[str], technical_details: Dict[str, List[str]]) -> List[str]:
        """Infer next steps based on current themes"""
        next_steps = []
        
        if 'user interface' in themes:
            next_steps.append('UI refinement and user testing')
        if 'context enhancement' in themes:
            next_steps.append('Context system optimization')
        if 'database' in themes:
            next_steps.append('Database performance tuning')
        if 'mcp integration' in themes:
            next_steps.append('MCP server enhancement')
        if 'conversation management' in themes:
            next_steps.append('Conversation analytics')
        
        next_steps.extend([
            'System monitoring and optimization',
            'User feedback collection',
            'Performance benchmarking'
        ])
        
        return next_steps
    
    def _calculate_relevance_score(self, interactions: List[Dict[str, Any]], 
                                  themes: List[str], technical_details: Dict[str, List[str]]) -> float:
        """Calculate relevance score based on content richness"""
        base_score = 0.5
        
        if len(themes) > 2:
            base_score += 0.2
        if len(technical_details['focus_areas']) > 1:
            base_score += 0.15
        if len(interactions) > 5:
            base_score += 0.1
        
        if any('enhancement' in theme for theme in themes):
            base_score += 0.05
        if any('integration' in theme for theme in themes):
            base_score += 0.05
        
        return min(base_score, 1.0)
    
    def _get_existing_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get existing context for a session"""
        try:
            from models_local import get_session_factory, ConversationContext
            
            session_factory = get_session_factory()
            with session_factory() as db_session:
                context = db_session.query(ConversationContext).filter(
                    ConversationContext.session_id == session_id
                ).first()
                
                if context:
                    return {
                        'id': context.id,
                        'session_id': context.session_id,
                        'user_id': context.user_id,
                        'context_summary': context.context_summary,
                        'semantic_context': context.semantic_context,
                        'key_topics': context.key_topics,
                        'user_preferences': context.user_preferences,
                        'project_context': context.project_context,
                        'relevance_score': context.relevance_score,
                        'usage_count': context.usage_count
                    }
                return None
                
        except Exception as e:
            logger.error(f"❌ Failed to get existing context: {e}")
            return None
    
    def _update_existing_context(self, context_id: int, enhanced_context: Dict[str, Any]) -> bool:
        """Update existing context with new information"""
        try:
            from models_local import get_session_factory, ConversationContext
            import json
            
            session_factory = get_session_factory()
            with session_factory() as db_session:
                context = db_session.query(ConversationContext).filter(
                    ConversationContext.id == context_id
                ).first()
                
                if context:
                    context.context_summary = enhanced_context['context_summary']
                    context.semantic_context = json.dumps(enhanced_context['semantic_context'])
                    context.key_topics = json.dumps(enhanced_context['key_topics'])
                    context.user_preferences = json.dumps(enhanced_context['user_preferences'])
                    context.project_context = json.dumps(enhanced_context['project_context'])
                    context.relevance_score = enhanced_context['relevance_score']
                    context.updated_at = datetime.now()
                    context.usage_count += 1
                    
                    db_session.commit()
                    return True
                
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to update context: {e}")
            return False
    
    def _create_new_context(self, enhanced_context: Dict[str, Any]) -> bool:
        """Create new context in database"""
        try:
            from models_local import get_session_factory, ConversationContext
            import json
            
            session_factory = get_session_factory()
            with session_factory() as db_session:
                new_context = ConversationContext(
                    session_id=enhanced_context['session_id'],
                    user_id=enhanced_context['user_id'],
                    context_summary=enhanced_context['context_summary'],
                    semantic_context=json.dumps(enhanced_context['semantic_context']),
                    key_topics=json.dumps(enhanced_context['key_topics']),
                    user_preferences=json.dumps(enhanced_context['user_preferences']),
                    project_context=json.dumps(enhanced_context['project_context']),
                    context_type=enhanced_context['context_type'],
                    relevance_score=enhanced_context['relevance_score'],
                    usage_count=enhanced_context['usage_count']
                )
                
                db_session.add(new_context)
                db_session.commit()
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to create new context: {e}")
            return False
    
    def optimize_performance(self):
        """Optimize performance based on current metrics"""
        logger.info("🔧 Optimizing context system performance...")
        
        # Clear caches if they're getting too large
        for system_name, system_info in self.context_systems.items():
            if system_info['status'] == 'available' and hasattr(system_info['instance'], 'clear_cache'):
                try:
                    system_info['instance'].clear_cache()
                    logger.info(f"🧠 Cleared cache for {system_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Could not clear cache for {system_name}: {e}")
        
        logger.info("✅ Performance optimization completed")

# Global instance for easy access
seamless_context_manager = SeamlessContextManager()

def enhance_prompt_seamlessly(prompt: str, context_type: str = "general", 
                            use_system: str = "auto") -> str:
    """
    Convenience function to seamlessly enhance prompts
    
    Usage:
        enhanced = enhance_prompt_seamlessly("How do I deploy this app?")
        enhanced = enhance_prompt_seamlessly("What's next?", "technical", "real_time")
    """
    return seamless_context_manager.enhance_prompt_seamlessly(prompt, context_type, use_system)

def get_context_system_status() -> Dict[str, Any]:
    """Get status of all context systems"""
    return seamless_context_manager.get_system_status()

def get_performance_summary() -> Dict[str, Any]:
    """Get overall performance summary"""
    return seamless_context_manager.get_performance_summary()

def start_seamless_context_manager():
    """Start the seamless context manager"""
    seamless_context_manager.start()

def stop_seamless_context_manager():
    """Stop the seamless context manager"""
    seamless_context_manager.stop()

def optimize_context_performance():
    """Optimize context system performance"""
    seamless_context_manager.optimize_performance()

if __name__ == "__main__":
    print("🧪 Testing Seamless Context Integration Manager...")
    
    # Start the manager
    start_seamless_context_manager()
    
    # Test seamless enhancement
    test_prompts = [
        ("What should I work on next?", "general"),
        ("How do I optimize this code?", "technical"),
        ("What's our conversation about?", "conversation")
    ]
    
    for prompt, context_type in test_prompts:
        enhanced = enhance_prompt_seamlessly(prompt, context_type)
        print(f"\n📝 Original: {prompt}")
        print(f"🚀 Enhanced length: {len(enhanced)} characters")
        print(f"✨ Contains context: {'CONTEXT' in enhanced or 'INJECTED' in enhanced}")
    
    # Show system status
    status = get_context_system_status()
    print(f"\n📊 System status: {json.dumps(status, indent=2)}")
    
    # Show performance summary
    performance = get_performance_summary()
    print(f"\n📈 Performance summary: {json.dumps(performance, indent=2)}")
    
    # Stop the manager
    stop_seamless_context_manager()
    
    print("\n✅ Seamless context integration manager test completed!")
