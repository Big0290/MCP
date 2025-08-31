#!/usr/bin/env python3
"""
Dynamic Instruction Processing System
Parses user instructions and updates agent metadata/preferences dynamically
"""

import sys
import os
import re
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class InstructionResult:
    """Result of instruction parsing"""
    instruction_type: str
    field: str
    old_value: Optional[str]
    new_value: str
    confidence: float
    raw_instruction: str
    timestamp: datetime

@dataclass
class DynamicAgentMetadata:
    """Dynamic agent metadata that can be updated via instructions"""
    friendly_name: str = "Johny"
    agent_id: str = "mcp-project-local"
    agent_type: str = "Context-Aware Conversation Manager"
    capabilities: List[str] = None
    status: str = "Active and learning"
    version: str = "1.0.0"
    mode: str = "Local development"
    personality_traits: List[str] = None
    communication_style: str = "technical_expert"
    last_updated: datetime = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = [
                "Prompt processing", 
                "Context analysis", 
                "Memory management",
                "Dynamic instruction processing"
            ]
        if self.personality_traits is None:
            self.personality_traits = [
                "Helpful", 
                "Technical", 
                "Context-aware",
                "Adaptive"
            ]
        if self.last_updated is None:
            self.last_updated = datetime.now()

@dataclass
class DynamicUserPreferences:
    """Dynamic user preferences that can be updated via instructions"""
    preferred_tools: Dict[str, str] = None
    communication_preferences: Dict[str, str] = None
    technical_preferences: Dict[str, str] = None
    workflow_preferences: List[str] = None
    avoid_patterns: List[str] = None
    last_updated: datetime = None
    
    def __post_init__(self):
        # Only set defaults if creating a completely new instance (no existing data)
        # This prevents overriding loaded preferences from JSON files
        if self.preferred_tools is None:
            self.preferred_tools = {
                "database": "SQLite",
                "language": "Python",
                "protocol": "MCP"
            }
        if self.communication_preferences is None:
            self.communication_preferences = {
                "style": "concise",  # Updated default to match user preference
                "format": "structured_responses",
                "level": "technical_expert"
            }
        if self.technical_preferences is None:
            self.technical_preferences = {
                "approach": "simple_yet_powerful",
                "focus": "conversation_context_memory",
                "data_control": "local"
            }
        if self.workflow_preferences is None:
            self.workflow_preferences = [
                "Comprehensive logging",
                "Structured data models",
                "Best practices focus"
            ]
        if self.avoid_patterns is None:
            self.avoid_patterns = []
        if self.last_updated is None:
            self.last_updated = datetime.now()

class DynamicInstructionProcessor:
    """
    Advanced instruction processor that parses user commands and updates system state
    
    Features:
    1. Natural language instruction parsing
    2. Dynamic metadata updates
    3. Persistent preference storage
    4. Confidence scoring
    5. Instruction history tracking
    """
    
    def __init__(self, storage_dir: str = "./data/dynamic_config"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.agent_metadata_file = self.storage_dir / "agent_metadata.json"
        self.user_preferences_file = self.storage_dir / "user_preferences.json"
        self.instruction_history_file = self.storage_dir / "instruction_history.json"
        
        # Load existing data
        self.agent_metadata = self._load_agent_metadata()
        self.user_preferences = self._load_user_preferences()
        self.instruction_history = self._load_instruction_history()
        
        # Instruction patterns
        self._initialize_instruction_patterns()
        
        logger.info("🚀 Dynamic Instruction Processor initialized")
    
    def _initialize_instruction_patterns(self):
        """Initialize instruction parsing patterns"""
        
        # Agent name/identity patterns
        self.name_patterns = [
            (r'your name is ([^.!?]+)', 'friendly_name', 0.9),
            (r'call yourself ([^.!?]+)', 'friendly_name', 0.8),
            (r'you are ([^.!?]+)', 'friendly_name', 0.7),
            (r'i want to call you ([^.!?]+)', 'friendly_name', 0.8),
            (r'from now on you are ([^.!?]+)', 'friendly_name', 0.9),
            (r'your new name is ([^.!?]+)', 'friendly_name', 0.9)
        ]
        
        # Communication style patterns - ENHANCED
        self.style_patterns = [
            (r'be more (concise|brief|short)', 'communication_style', 0.8),
            (r'be more (detailed|verbose|comprehensive)', 'communication_style', 0.8),
            (r'use (formal|informal|casual|technical) language', 'communication_style', 0.8),
            (r'respond in a (.*?) manner', 'communication_style', 0.7),
            (r'your tone should be (.*)', 'communication_style', 0.7),
            # NEW: More flexible preference patterns
            (r'i prefer (.*?) responses?', 'communication_style', 0.7),
            (r'i like (.*?) explanations?', 'communication_style', 0.7),
            (r'give me (.*?) answers?', 'communication_style', 0.6),
            (r'my preference is (.*)', 'communication_style', 0.8),
            (r'i want (.*?) communication', 'communication_style', 0.7)
        ]
        
        # Tool preference patterns
        self.tool_patterns = [
            (r'don\'t use ([^,]+),? use ([^.!?]+)', 'tool_preference', 0.9),
            (r'instead of ([^,]+),? use ([^.!?]+)', 'tool_preference', 0.9),
            (r'prefer ([^,]+) over ([^.!?]+)', 'tool_preference', 0.8),
            (r'always use ([^.!?]+)', 'preferred_tool', 0.7),
            (r'never use ([^.!?]+)', 'avoid_tool', 0.8),
            (r'use ([^,]+) for ([^.!?]+)', 'specific_tool', 0.7)
        ]
        
        # Capability patterns
        self.capability_patterns = [
            (r'you can (.*)', 'add_capability', 0.7),
            (r'you should be able to (.*)', 'add_capability', 0.7),
            (r'your capabilities include (.*)', 'set_capabilities', 0.8),
            (r'you are good at (.*)', 'add_capability', 0.6)
        ]
        
        # Personality patterns
        self.personality_patterns = [
            (r'you are (helpful|friendly|technical|creative|analytical)', 'personality_trait', 0.8),
            (r'be more (patient|understanding|direct|efficient)', 'personality_trait', 0.7),
            (r'your personality is (.*)', 'personality_style', 0.8)
        ]
        
        # NEW: General preference patterns to catch broader statements
        self.general_preference_patterns = [
            (r'i gave some preference', 'general_preference_mention', 0.9),
            (r'my preferences? (?:are|is) (.*)', 'general_preference', 0.8),
            (r'i mentioned (.*?) (?:preference|setting)', 'mentioned_preference', 0.7),
            (r'what i (?:mentioned|said) (?:is|was) (.*)', 'mentioned_preference', 0.7),
            (r'i (?:prefer|like|want) (.*)', 'user_preference', 0.6),
            (r'my (?:style|approach|method) is (.*)', 'user_style', 0.7),
            (r'i (?:always|usually|typically) (.*)', 'user_habit', 0.6),
            (r'remember that i (.*)', 'user_reminder', 0.8),
            (r'don\'t forget (?:that )?i (.*)', 'user_reminder', 0.8)
        ]
    
    def process_instruction(self, user_message: str) -> List[InstructionResult]:
        """
        Process a user message for instructions and return parsed results
        
        Args:
            user_message: The user's message to parse
            
        Returns:
            List of InstructionResult objects
        """
        results = []
        message_lower = user_message.lower().strip()
        
        # Parse different types of instructions
        results.extend(self._parse_name_instructions(message_lower, user_message))
        results.extend(self._parse_style_instructions(message_lower, user_message))
        results.extend(self._parse_tool_instructions(message_lower, user_message))
        results.extend(self._parse_capability_instructions(message_lower, user_message))
        results.extend(self._parse_personality_instructions(message_lower, user_message))
        # NEW: Parse general preferences
        results.extend(self._parse_general_preferences(message_lower, user_message))
        
        # Log and store results
        if results:
            logger.info(f"📝 Processed {len(results)} instructions from user message")
            self._store_instruction_results(results)
        
        return results
    
    def _parse_name_instructions(self, message_lower: str, original_message: str) -> List[InstructionResult]:
        """Parse name/identity instructions"""
        results = []
        
        for pattern, field, confidence in self.name_patterns:
            match = re.search(pattern, message_lower)
            if match:
                new_name = match.group(1).strip().title()
                old_name = self.agent_metadata.friendly_name
                
                result = InstructionResult(
                    instruction_type="agent_metadata",
                    field=field,
                    old_value=old_name,
                    new_value=new_name,
                    confidence=confidence,
                    raw_instruction=original_message,
                    timestamp=datetime.now()
                )
                results.append(result)
                break  # Only take the first match
        
        return results
    
    def _parse_style_instructions(self, message_lower: str, original_message: str) -> List[InstructionResult]:
        """Parse communication style instructions"""
        results = []
        
        for pattern, field, confidence in self.style_patterns:
            match = re.search(pattern, message_lower)
            if match:
                style_value = match.group(1).strip()
                old_style = self.user_preferences.communication_preferences.get("style", "")
                
                result = InstructionResult(
                    instruction_type="user_preferences",
                    field=f"communication_preferences.style",
                    old_value=old_style,
                    new_value=style_value,
                    confidence=confidence,
                    raw_instruction=original_message,
                    timestamp=datetime.now()
                )
                results.append(result)
        
        return results
    
    def _parse_general_preferences(self, message_lower: str, original_message: str) -> List[InstructionResult]:
        """Parse general preference instructions with smart filtering"""
        results = []
        
        # SMART FILTERING: Skip messages that are clearly requests/commands, not preferences
        non_preference_indicators = [
            'show me', 'let me see', 'can we', 'plz', 'please show', 'display', 'generate', 
            'test', 'verify', 'check', 'investigate', 'fix', 'debug', 'see our', 'to see',
            'look at', 'examine', 'lets generate', 'can you show', 'i want to see',
            'i want you to', 'can you', 'could you', 'would you', 'will you'
        ]
        
        # Skip if message contains request/command indicators
        if any(indicator in message_lower for indicator in non_preference_indicators):
            return results
        
        for pattern, field, confidence in self.general_preference_patterns:
            match = re.search(pattern, message_lower)
            if match:
                preference_value = match.group(1).strip() if match.groups() else "mentioned"
                
                # Additional filtering: Skip if the captured value looks like a request
                if any(word in preference_value.lower() for word in ['show', 'see', 'display', 'generate', 'test', 'check', 'our prompt']):
                    continue
                
                result = InstructionResult(
                    instruction_type="user_preferences",
                    field=f"general_preferences.{field}",
                    old_value=None,
                    new_value=preference_value,
                    confidence=confidence,
                    raw_instruction=original_message,
                    timestamp=datetime.now()
                )
                results.append(result)
                
                # Only log as workflow preference if it's a genuine preference
                if field not in ["general_preference_mention"] and confidence > 0.7:
                    workflow_result = InstructionResult(
                        instruction_type="user_preferences",
                        field="workflow_preferences",
                        old_value=None,
                        new_value=f"User mentioned: {preference_value}",
                        confidence=confidence * 0.8,  # Slightly lower confidence
                        raw_instruction=original_message,
                        timestamp=datetime.now()
                    )
                    results.append(workflow_result)
        
        return results
    
    def _parse_tool_instructions(self, message_lower: str, original_message: str) -> List[InstructionResult]:
        """Parse tool preference instructions"""
        results = []
        
        for pattern, field, confidence in self.tool_patterns:
            match = re.search(pattern, message_lower)
            if match:
                if field == "tool_preference" and len(match.groups()) >= 2:
                    avoid_tool = match.group(1).strip()
                    prefer_tool = match.group(2).strip()
                    
                    # Add to avoid patterns
                    result1 = InstructionResult(
                        instruction_type="user_preferences",
                        field="avoid_patterns",
                        old_value=None,
                        new_value=avoid_tool,
                        confidence=confidence,
                        raw_instruction=original_message,
                        timestamp=datetime.now()
                    )
                    results.append(result1)
                    
                    # Add preferred tool
                    result2 = InstructionResult(
                        instruction_type="user_preferences",
                        field="preferred_tools.general",
                        old_value=None,
                        new_value=prefer_tool,
                        confidence=confidence,
                        raw_instruction=original_message,
                        timestamp=datetime.now()
                    )
                    results.append(result2)
                
                elif field in ["preferred_tool", "avoid_tool"]:
                    tool_name = match.group(1).strip()
                    target_field = "preferred_tools.general" if field == "preferred_tool" else "avoid_patterns"
                    
                    result = InstructionResult(
                        instruction_type="user_preferences",
                        field=target_field,
                        old_value=None,
                        new_value=tool_name,
                        confidence=confidence,
                        raw_instruction=original_message,
                        timestamp=datetime.now()
                    )
                    results.append(result)
        
        return results
    
    def _parse_capability_instructions(self, message_lower: str, original_message: str) -> List[InstructionResult]:
        """Parse capability instructions"""
        results = []
        
        for pattern, field, confidence in self.capability_patterns:
            match = re.search(pattern, message_lower)
            if match:
                capability = match.group(1).strip()
                
                result = InstructionResult(
                    instruction_type="agent_metadata",
                    field="capabilities",
                    old_value=None,
                    new_value=capability,
                    confidence=confidence,
                    raw_instruction=original_message,
                    timestamp=datetime.now()
                )
                results.append(result)
        
        return results
    
    def _parse_personality_instructions(self, message_lower: str, original_message: str) -> List[InstructionResult]:
        """Parse personality instructions"""
        results = []
        
        for pattern, field, confidence in self.personality_patterns:
            match = re.search(pattern, message_lower)
            if match:
                trait = match.group(1).strip()
                
                result = InstructionResult(
                    instruction_type="agent_metadata",
                    field="personality_traits",
                    old_value=None,
                    new_value=trait,
                    confidence=confidence,
                    raw_instruction=original_message,
                    timestamp=datetime.now()
                )
                results.append(result)
        
        return results
    
    def apply_instructions(self, instruction_results: List[InstructionResult]) -> Dict[str, Any]:
        """
        Apply parsed instructions to update metadata and preferences
        
        Args:
            instruction_results: List of parsed instructions
            
        Returns:
            Dictionary with update summary
        """
        updates = {
            "agent_metadata_updates": 0,
            "user_preference_updates": 0,
            "total_updates": 0,
            "applied_instructions": [],
            "skipped_instructions": []
        }
        
        for instruction in instruction_results:
            try:
                if instruction.confidence < 0.6:  # Skip low confidence instructions
                    updates["skipped_instructions"].append({
                        "instruction": instruction.raw_instruction,
                        "reason": f"Low confidence: {instruction.confidence}"
                    })
                    continue
                
                applied = False
                
                if instruction.instruction_type == "agent_metadata":
                    applied = self._apply_agent_metadata_update(instruction)
                    if applied:
                        updates["agent_metadata_updates"] += 1
                
                elif instruction.instruction_type == "user_preferences":
                    applied = self._apply_user_preference_update(instruction)
                    if applied:
                        updates["user_preference_updates"] += 1
                
                if applied:
                    updates["applied_instructions"].append({
                        "field": instruction.field,
                        "old_value": instruction.old_value,
                        "new_value": instruction.new_value,
                        "confidence": instruction.confidence
                    })
                    updates["total_updates"] += 1
                
            except Exception as e:
                logger.error(f"❌ Failed to apply instruction: {e}")
                updates["skipped_instructions"].append({
                    "instruction": instruction.raw_instruction,
                    "reason": f"Error: {str(e)}"
                })
        
        # Save updated data
        if updates["total_updates"] > 0:
            self._save_agent_metadata()
            self._save_user_preferences()
            logger.info(f"✅ Applied {updates['total_updates']} dynamic instructions")
        
        return updates
    
    def _apply_agent_metadata_update(self, instruction: InstructionResult) -> bool:
        """Apply an agent metadata update"""
        try:
            field = instruction.field
            new_value = instruction.new_value
            
            if field == "friendly_name":
                self.agent_metadata.friendly_name = new_value
            elif field == "capabilities":
                if new_value not in self.agent_metadata.capabilities:
                    self.agent_metadata.capabilities.append(new_value)
            elif field == "personality_traits":
                if new_value not in self.agent_metadata.personality_traits:
                    self.agent_metadata.personality_traits.append(new_value)
            elif field == "communication_style":
                self.agent_metadata.communication_style = new_value
            elif hasattr(self.agent_metadata, field):
                setattr(self.agent_metadata, field, new_value)
            else:
                return False
            
            self.agent_metadata.last_updated = datetime.now()
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to apply agent metadata update: {e}")
            return False
    
    def _apply_user_preference_update(self, instruction: InstructionResult) -> bool:
        """Apply a user preference update"""
        try:
            field = instruction.field
            new_value = instruction.new_value
            
            if "." in field:
                # Handle nested field updates
                parts = field.split(".")
                if parts[0] == "communication_preferences":
                    self.user_preferences.communication_preferences[parts[1]] = new_value
                elif parts[0] == "preferred_tools":
                    self.user_preferences.preferred_tools[parts[1]] = new_value
                elif parts[0] == "technical_preferences":
                    self.user_preferences.technical_preferences[parts[1]] = new_value
                elif parts[0] == "general_preferences":
                    # Store general preferences in workflow_preferences for now
                    preference_text = f"General: {parts[1]} = {new_value}"
                    if preference_text not in self.user_preferences.workflow_preferences:
                        self.user_preferences.workflow_preferences.append(preference_text)
            elif field == "avoid_patterns":
                if new_value not in self.user_preferences.avoid_patterns:
                    self.user_preferences.avoid_patterns.append(new_value)
            elif field == "workflow_preferences":
                if new_value not in self.user_preferences.workflow_preferences:
                    self.user_preferences.workflow_preferences.append(new_value)
            else:
                return False
            
            self.user_preferences.last_updated = datetime.now()
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to apply user preference update: {e}")
            return False
    
    def get_current_agent_metadata(self) -> Dict[str, Any]:
        """Get current agent metadata as dictionary"""
        return asdict(self.agent_metadata)
    
    def get_current_user_preferences(self) -> Dict[str, Any]:
        """Get current user preferences as dictionary"""
        return asdict(self.user_preferences)
    
    def get_formatted_agent_metadata(self) -> str:
        """Get formatted agent metadata string for prompts"""
        metadata = self.agent_metadata
        
        capabilities_str = ", ".join(metadata.capabilities)
        traits_str = ", ".join(metadata.personality_traits)
        
        return f"""Agent Metadata:
    - Friendly Name: {metadata.friendly_name}
    - Agent ID: {metadata.agent_id}
    - Type: {metadata.agent_type}
    - Capabilities: {capabilities_str}
    - Status: {metadata.status}
    - Version: {metadata.version}
    - Mode: {metadata.mode}
    - Communication Style: {metadata.communication_style}
    - Personality: {traits_str}
    - Last Updated: {metadata.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"""
    
    def get_formatted_user_preferences(self) -> str:
        """Get formatted user preferences string for prompts"""
        prefs = self.user_preferences
        
        pref_lines = []
        
        # Add preferred tools
        for tool_type, tool_name in prefs.preferred_tools.items():
            pref_lines.append(f"Use {tool_name} for {tool_type}")
        
        # Add communication preferences
        for pref_type, pref_value in prefs.communication_preferences.items():
            pref_lines.append(f"Communication {pref_type}: {pref_value}")
        
        # Add technical preferences
        for tech_type, tech_value in prefs.technical_preferences.items():
            pref_lines.append(f"Technical {tech_type}: {tech_value}")
        
        # Add workflow preferences
        for workflow in prefs.workflow_preferences:
            pref_lines.append(f"Workflow: {workflow}")
        
        # Add avoid patterns
        for avoid in prefs.avoid_patterns:
            pref_lines.append(f"Avoid: {avoid}")
        
        formatted = "User Preferences:\n"
        for line in pref_lines:
            formatted += f"    - {line}\n"
        
        formatted += f"    - Last Updated: {prefs.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"
        
        return formatted
    
    def _load_agent_metadata(self) -> DynamicAgentMetadata:
        """Load agent metadata from file"""
        try:
            if self.agent_metadata_file.exists():
                with open(self.agent_metadata_file, 'r') as f:
                    data = json.load(f)
                
                # Convert datetime string back to datetime object
                if 'last_updated' in data and isinstance(data['last_updated'], str):
                    data['last_updated'] = datetime.fromisoformat(data['last_updated'])
                
                return DynamicAgentMetadata(**data)
        except Exception as e:
            logger.warning(f"⚠️ Failed to load agent metadata: {e}")
        
        return DynamicAgentMetadata()
    
    def _load_user_preferences(self) -> DynamicUserPreferences:
        """Load user preferences from file"""
        try:
            if self.user_preferences_file.exists():
                with open(self.user_preferences_file, 'r') as f:
                    data = json.load(f)
                
                # Convert datetime string back to datetime object
                if 'last_updated' in data and isinstance(data['last_updated'], str):
                    data['last_updated'] = datetime.fromisoformat(data['last_updated'])
                
                return DynamicUserPreferences(**data)
        except Exception as e:
            logger.warning(f"⚠️ Failed to load user preferences: {e}")
        
        return DynamicUserPreferences()
    
    def _load_instruction_history(self) -> List[Dict[str, Any]]:
        """Load instruction history from file"""
        try:
            if self.instruction_history_file.exists():
                with open(self.instruction_history_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"⚠️ Failed to load instruction history: {e}")
        
        return []
    
    def _save_agent_metadata(self):
        """Save agent metadata to file"""
        try:
            data = asdict(self.agent_metadata)
            # Convert datetime to string for JSON serialization
            if 'last_updated' in data:
                data['last_updated'] = data['last_updated'].isoformat()
            
            with open(self.agent_metadata_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to save agent metadata: {e}")
    
    def _save_user_preferences(self):
        """Save user preferences to file"""
        try:
            data = asdict(self.user_preferences)
            # Convert datetime to string for JSON serialization
            if 'last_updated' in data:
                data['last_updated'] = data['last_updated'].isoformat()
            
            with open(self.user_preferences_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to save user preferences: {e}")
    
    def _store_instruction_results(self, results: List[InstructionResult]):
        """Store instruction results in history"""
        try:
            for result in results:
                instruction_data = asdict(result)
                # Convert datetime to string for JSON serialization
                instruction_data['timestamp'] = instruction_data['timestamp'].isoformat()
                self.instruction_history.append(instruction_data)
            
            # Keep only last 100 instructions
            self.instruction_history = self.instruction_history[-100:]
            
            with open(self.instruction_history_file, 'w') as f:
                json.dump(self.instruction_history, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Failed to store instruction history: {e}")

# Global instance
dynamic_processor = DynamicInstructionProcessor()

def process_user_instruction(user_message: str) -> Dict[str, Any]:
    """
    Convenience function to process user instructions
    
    Args:
        user_message: The user's message to parse for instructions
        
    Returns:
        Dictionary with processing results and updates
    """
    instructions = dynamic_processor.process_instruction(user_message)
    if instructions:
        updates = dynamic_processor.apply_instructions(instructions)
        return {
            "instructions_found": len(instructions),
            "updates_applied": updates,
            "current_metadata": dynamic_processor.get_current_agent_metadata(),
            "current_preferences": dynamic_processor.get_current_user_preferences()
        }
    
    return {
        "instructions_found": 0,
        "updates_applied": None,
        "current_metadata": dynamic_processor.get_current_agent_metadata(),
        "current_preferences": dynamic_processor.get_current_user_preferences()
    }

if __name__ == "__main__":
    # Test the system
    test_messages = [
        "Your name is SuperBot",
        "Don't use PostgreSQL, use SQLite instead",
        "Be more concise in your responses",
        "You can help with code debugging",
        "You are very analytical"
    ]
    
    print("🧪 Testing Dynamic Instruction Processing:")
    
    for message in test_messages:
        print(f"\n📝 Testing: '{message}'")
        result = process_user_instruction(message)
        
        if result["instructions_found"] > 0:
            print(f"   ✅ Found {result['instructions_found']} instructions")
            updates = result["updates_applied"]
            print(f"   📊 Applied {updates['total_updates']} updates")
            
            for update in updates["applied_instructions"]:
                print(f"      • {update['field']}: {update['old_value']} → {update['new_value']}")
        else:
            print("   ❌ No instructions detected")
    
    print(f"\n🤖 Final Agent Metadata:")
    print(dynamic_processor.get_formatted_agent_metadata())
    
    print(f"\n👤 Final User Preferences:")
    print(dynamic_processor.get_formatted_user_preferences())
