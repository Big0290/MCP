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
