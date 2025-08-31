#!/usr/bin/env python3
"""
🚀 Unified Preference Manager - Single Source of Truth

This module consolidates all user preference loading into one unified system
that uses the database as the single source of truth, eliminating the 
duplication between JSON files and different loading functions.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

# Import our unified models
try:
    from models_unified import UnifiedUserPreferences, get_global_session
    UNIFIED_MODELS_AVAILABLE = True
except ImportError:
    UNIFIED_MODELS_AVAILABLE = False
    print("⚠️ Unified models not available, using fallback")

logger = logging.getLogger(__name__)

@dataclass
class PreferenceData:
    """Structured preference data"""
    preferred_tools: Dict[str, str]
    communication_preferences: Dict[str, str]
    technical_preferences: Dict[str, str]
    workflow_preferences: List[str]
    avoid_patterns: List[str]
    custom_preferences: Dict[str, Any]
    last_updated: datetime
    created_at: datetime

class UnifiedPreferenceManager:
    """
    Unified preference manager that provides a single source of truth
    for all user preferences across the entire system.
    """
    
    def __init__(self, user_id: str = 'default'):
        self.user_id = user_id
        self._preferences = None
        self._last_load_time = None
        self._cache_duration = 300  # 5 minutes cache
        
        # Fallback JSON file path
        self.fallback_json_path = Path("./data/dynamic_config/user_preferences.json")
        
        logger.info(f"🚀 Unified Preference Manager initialized for user: {user_id}")
    
    def get_preferences(self, force_refresh: bool = False) -> PreferenceData:
        """
        Get user preferences - single source of truth for all systems
        
        Args:
            force_refresh: Force refresh from database
            
        Returns:
            PreferenceData object with all preferences
        """
        # Check cache first
        if not force_refresh and self._is_cache_valid():
            return self._preferences
        
        try:
            # Try database first
            if UNIFIED_MODELS_AVAILABLE:
                preferences = self._load_from_database()
                if preferences:
                    self._preferences = preferences
                    self._last_load_time = datetime.now()
                    logger.info("✅ Preferences loaded from database")
                    return preferences
            
            # Fallback to JSON file
            preferences = self._load_from_json()
            if preferences:
                self._preferences = preferences
                self._last_load_time = datetime.now()
                logger.info("✅ Preferences loaded from JSON fallback")
                return preferences
            
            # Create default preferences
            preferences = self._create_default_preferences()
            self._preferences = preferences
            self._last_load_time = datetime.now()
            logger.info("✅ Default preferences created")
            return preferences
            
        except Exception as e:
            logger.error(f"❌ Error loading preferences: {e}")
            # Return cached preferences if available, otherwise defaults
            if self._preferences:
                return self._preferences
            return self._create_default_preferences()
    
    def _load_from_database(self) -> Optional[PreferenceData]:
        """Load preferences from database"""
        try:
            session = get_global_session()
            if not session:
                return None
            
            # Query for user preferences
            db_prefs = session.query(UnifiedUserPreferences).filter(
                UnifiedUserPreferences.user_id == self.user_id
            ).first()
            
            if db_prefs:
                return PreferenceData(
                    preferred_tools=db_prefs.preferred_tools,
                    communication_preferences=db_prefs.communication_preferences,
                    technical_preferences=db_prefs.technical_preferences,
                    workflow_preferences=db_prefs.workflow_preferences,
                    avoid_patterns=db_prefs.avoid_patterns,
                    custom_preferences=db_prefs.custom_preferences or {},
                    last_updated=db_prefs.last_updated,
                    created_at=db_prefs.created_at
                )
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Database load failed: {e}")
            return None
    
    def _load_from_json(self) -> Optional[PreferenceData]:
        """Load preferences from JSON file (fallback)"""
        try:
            if not self.fallback_json_path.exists():
                return None
            
            with open(self.fallback_json_path, 'r') as f:
                data = json.load(f)
            
            # Convert JSON data to PreferenceData
            return PreferenceData(
                preferred_tools=data.get('preferred_tools', {}),
                communication_preferences=data.get('communication_preferences', {}),
                technical_preferences=data.get('technical_preferences', {}),
                workflow_preferences=data.get('workflow_preferences', []),
                avoid_patterns=data.get('avoid_patterns', []),
                custom_preferences=data.get('custom_preferences', {}),
                last_updated=datetime.fromisoformat(data.get('last_updated', datetime.now().isoformat())),
                created_at=datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
            )
            
        except Exception as e:
            logger.error(f"❌ JSON load failed: {e}")
            return None
    
    def _create_default_preferences(self) -> PreferenceData:
        """Create default preferences"""
        now = datetime.now()
        return PreferenceData(
            preferred_tools={
                "database": "SQLite",
                "language": "Python",
                "protocol": "MCP"
            },
            communication_preferences={
                "style": "concise",
                "format": "structured_responses",
                "level": "technical_expert"
            },
            technical_preferences={
                "approach": "simple_yet_powerful",
                "focus": "conversation_context_memory",
                "data_control": "local"
            },
            workflow_preferences=[
                "Comprehensive logging",
                "Structured data models",
                "Best practices focus"
            ],
            avoid_patterns=[
                "Avoid starting responses with \"you're absolutely right\""
            ],
            custom_preferences={},
            last_updated=now,
            created_at=now
        )
    
    def _is_cache_valid(self) -> bool:
        """Check if cached preferences are still valid"""
        if not self._preferences or not self._last_load_time:
            return False
        
        age = (datetime.now() - self._last_load_time).total_seconds()
        return age < self._cache_duration
    
    def update_preferences(self, updates: Dict[str, Any]) -> bool:
        """
        Update user preferences in the database
        
        Args:
            updates: Dictionary with preference updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not UNIFIED_MODELS_AVAILABLE:
                logger.warning("⚠️ Database not available, saving to JSON")
                return self._save_to_json(updates)
            
            session = get_global_session()
            if not session:
                logger.warning("⚠️ No database session, saving to JSON")
                return self._save_to_json(updates)
            
            # Get or create preferences record
            db_prefs = session.query(UnifiedUserPreferences).filter(
                UnifiedUserPreferences.user_id == self.user_id
            ).first()
            
            if not db_prefs:
                db_prefs = UnifiedUserPreferences(user_id=self.user_id)
                session.add(db_prefs)
            
            # Update the record
            db_prefs.update_from_dict(updates)
            
            # Commit changes
            session.commit()
            
            # Update cache
            self._preferences = self._load_from_database()
            self._last_load_time = datetime.now()
            
            logger.info("✅ Preferences updated in database")
            return True
            
        except Exception as e:
            logger.error(f"❌ Database update failed: {e}")
            # Fallback to JSON
            return self._save_to_json(updates)
    
    def _save_to_json(self, updates: Dict[str, Any]) -> bool:
        """Save preferences to JSON file (fallback)"""
        try:
            # Load current preferences
            current = self.get_preferences()
            
            # Apply updates
            for key, value in updates.items():
                if hasattr(current, key):
                    setattr(current, key, value)
            
            # Convert to JSON format
            json_data = {
                'preferred_tools': current.preferred_tools,
                'communication_preferences': current.communication_preferences,
                'technical_preferences': current.technical_preferences,
                'workflow_preferences': current.workflow_preferences,
                'avoid_patterns': current.avoid_patterns,
                'custom_preferences': current.custom_preferences,
                'last_updated': datetime.now().isoformat(),
                'created_at': current.created_at.isoformat()
            }
            
            # Ensure directory exists
            self.fallback_json_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to JSON
            with open(self.fallback_json_path, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            logger.info("✅ Preferences saved to JSON fallback")
            return True
            
        except Exception as e:
            logger.error(f"❌ JSON save failed: {e}")
            return False
    
    def get_formatted_preferences(self) -> str:
        """
        Get formatted preferences string for prompt injection
        This is the unified function that all systems should use
        """
        preferences = self.get_preferences()
        
        formatted = "User Preferences:\n"
        
        # Preferred tools
        if preferences.preferred_tools:
            for key, value in preferences.preferred_tools.items():
                formatted += f"    - Use {value} for {key}\n"
        
        # Communication preferences
        if preferences.communication_preferences:
            for key, value in preferences.communication_preferences.items():
                formatted += f"    - Communication {key}: {value}\n"
        
        # Technical preferences
        if preferences.technical_preferences:
            for key, value in preferences.technical_preferences.items():
                formatted += f"    - Technical {key}: {value}\n"
        
        # Workflow preferences
        if preferences.workflow_preferences:
            for pref in preferences.workflow_preferences:
                formatted += f"    - Workflow: {pref}\n"
        
        # Avoid patterns
        if preferences.avoid_patterns:
            for pattern in preferences.avoid_patterns:
                formatted += f"    - Avoid: {pattern}\n"
        
        # Custom preferences
        if preferences.custom_preferences:
            for key, value in preferences.custom_preferences.items():
                formatted += f"    - {key}: {value}\n"
        
        # Last updated
        if preferences.last_updated:
            formatted += f"    - Last Updated: {preferences.last_updated.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        return formatted
    
    def migrate_from_json(self) -> bool:
        """
        Migrate existing JSON preferences to database
        """
        try:
            if not UNIFIED_MODELS_AVAILABLE:
                logger.warning("⚠️ Database not available for migration")
                return False
            
            # Load from JSON
            json_prefs = self._load_from_json()
            if not json_prefs:
                logger.info("ℹ️ No JSON preferences to migrate")
                return True
            
            # Save to database
            success = self.update_preferences(asdict(json_prefs))
            if success:
                logger.info("✅ Preferences migrated from JSON to database")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            return False

# Global instance
_unified_preference_manager = None

def get_unified_preference_manager(user_id: str = 'default') -> UnifiedPreferenceManager:
    """Get or create global unified preference manager instance"""
    global _unified_preference_manager
    if _unified_preference_manager is None or _unified_preference_manager.user_id != user_id:
        _unified_preference_manager = UnifiedPreferenceManager(user_id)
    return _unified_preference_manager

def get_user_preferences_unified(user_id: str = 'default') -> str:
    """
    Unified function that all systems should use to get user preferences
    This replaces all the different _get_user_preferences functions
    """
    manager = get_unified_preference_manager(user_id)
    return manager.get_formatted_preferences()

def update_user_preferences_unified(updates: Dict[str, Any], user_id: str = 'default') -> bool:
    """
    Unified function to update user preferences
    """
    manager = get_unified_preference_manager(user_id)
    return manager.update_preferences(updates)

def migrate_preferences_to_database(user_id: str = 'default') -> bool:
    """
    Migrate existing JSON preferences to database
    """
    manager = get_unified_preference_manager(user_id)
    return manager.migrate_from_json()
