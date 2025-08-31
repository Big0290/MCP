#!/usr/bin/env python3
"""
Unified Database Models - Consolidates local and production models
Provides a single interface that automatically adapts to the environment
"""

import os
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Union
from enum import Enum

# Environment detection
class Environment(Enum):
    LOCAL = "local"
    PRODUCTION = "production"

def detect_environment() -> Environment:
    """Detect the current environment"""
    # Check for environment variables or configuration
    if os.getenv('MCP_ENVIRONMENT') == 'production':
        return Environment.PRODUCTION
    
    # Check if we're in a containerized environment
    if os.path.exists('/.dockerenv') or os.getenv('DOCKER_CONTAINER'):
        return Environment.PRODUCTION
    
    # Default to local development
    return Environment.LOCAL

# Current environment
_CURRENT_ENV = detect_environment()

# ============================================================================
# UNIFIED MODELS
# ============================================================================

# Import SQLAlchemy for ORM mapping
# Initialize variables with default values
SQLALCHEMY_VERSION = None
SQLALCHEMY_1X = False
SQLALCHEMY_2X = False
SQLALCHEMY_AVAILABLE = False
Base = None
_global_engine = None
_global_session_factory = None

try:
    import sqlalchemy
    SQLALCHEMY_VERSION = sqlalchemy.__version__
    print(f"🔍 SQLAlchemy version detected: {SQLALCHEMY_VERSION}")
    
    # Handle SQLAlchemy 1.x vs 2.x differences
    if SQLALCHEMY_VERSION.startswith('1.'):
        # SQLAlchemy 1.x
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
        Base = declarative_base()
        SQLALCHEMY_1X = True
        SQLALCHEMY_2X = False
        print("✅ Using SQLAlchemy 1.x syntax")
    else:
        # SQLAlchemy 2.x
        from sqlalchemy.orm import DeclarativeBase
        from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
        from sqlalchemy import MetaData
        from sqlalchemy.orm import registry
        
        # Create shared registry for SQLAlchemy 2.x
        _shared_registry = registry()
        
        # Create Base class using the registry
        Base = _shared_registry.generate_base()
        
        SQLALCHEMY_1X = False
        SQLALCHEMY_2X = True
        print("✅ Using SQLAlchemy 2.x syntax with shared registry")
    
    SQLALCHEMY_AVAILABLE = True
    
    # Force class registration function
    def force_class_registration():
        """Force SQLAlchemy to register our mapped classes"""
        try:
            # Import our classes to ensure they're registered with Base
            from models_unified import UnifiedInteraction, UnifiedSession
            
            # Force Base to recognize the mapped classes
            if hasattr(Base, 'metadata'):
                # This should trigger the class registration
                Base.metadata.tables
            
            # For SQLAlchemy 2.x, ensure the registry is configured
            if SQLALCHEMY_2X and hasattr(Base, 'registry'):
                Base.registry.configure()
                print("✅ SQLAlchemy 2.x registry configured")
            
            print("✅ Class registration forced")
            return True
        except Exception as e:
            print(f"⚠️  Class registration warning: {e}")
            return False
    
except ImportError:
    print("⚠️  SQLAlchemy not available, using fallback models")
    
    def force_class_registration():
        return False

class UnifiedModel:
    """Base class for unified models that work in both environments"""
    
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from dictionary"""
        return cls(**data)

# Define the SQLAlchemy models properly
if SQLALCHEMY_AVAILABLE and Base:
    class UnifiedInteraction(Base, UnifiedModel):
        """Unified interaction model that works in both environments"""
        
        __tablename__ = 'interactions'
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        interaction_type = Column(String(100), nullable=False)
        client_request = Column(Text)
        agent_response = Column(Text)
        timestamp = Column(DateTime, default=datetime.now)
        status = Column(String(50))
        interaction_metadata = Column(JSON)
        session_id = Column(String(100))
        user_id = Column(String(100))
        tool_name = Column(String(100))  # Add tool_name field
        parameters = Column(JSON)  # Add parameters field
        error_message = Column(Text)  # Add error_message field
        
        # Additional fields for backward compatibility
        prompt = Column(Text)
        response = Column(Text)
        full_content = Column(Text)
        context_summary = Column(Text)
        semantic_keywords = Column(JSON)
        topic_category = Column(String(100))
        execution_time_ms = Column(Integer)
        meta_data = Column(JSON)
        tool_name = Column(String(100))  # Add tool_name field
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Set all attributes explicitly to ensure they're accessible
            self.id = kwargs.get('id', kwargs.get('interaction_id', None))
            self.interaction_id = kwargs.get('interaction_id', kwargs.get('id', None))
            self.timestamp = kwargs.get('timestamp', datetime.now())
            self.session_id = kwargs.get('session_id', None)
            self.user_id = kwargs.get('user_id', 'anonymous')
            self.interaction_type = kwargs.get('interaction_type', 'conversation_turn')
            self.client_request = kwargs.get('client_request', kwargs.get('prompt', ''))
            self.agent_response = kwargs.get('agent_response', kwargs.get('response', ''))
            self.prompt = kwargs.get('prompt', '')
            self.response = kwargs.get('response', '')
            self.full_content = kwargs.get('full_content', '')
            self.context_summary = kwargs.get('context_summary', '')
            self.semantic_keywords = kwargs.get('semantic_keywords', [])
            self.topic_category = kwargs.get('topic_category', 'general')
            self.status = kwargs.get('status', 'completed')
            self.execution_time_ms = kwargs.get('execution_time_ms', 0)
            self.interaction_metadata = kwargs.get('metadata', kwargs.get('meta_data', {}))
            self.meta_data = kwargs.get('meta_data', {})
            self.tool_name = kwargs.get('tool_name', None)
            
            # Store additional attributes that might be passed
            for key, value in kwargs.items():
                if not hasattr(self, key):
                    setattr(self, key, value)

    class UnifiedSession(Base, UnifiedModel):
        """Unified session model that works in both environments"""
        
        __tablename__ = 'sessions'
        
        id = Column(Integer, primary_key=True, autoincrement=True)
        session_id = Column(String(100), unique=True, nullable=False)
        user_id = Column(String(100))
        started_at = Column(DateTime, default=datetime.now)
        last_activity = Column(DateTime, default=datetime.now)
        total_interactions = Column(Integer, default=0)
        current_context_id = Column(String(100))
        context_history = Column(JSON)
        session_summary = Column(Text)
        meta_data = Column(JSON)
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Handle ID properly - don't override auto-increment id with string
            if 'id' in kwargs and isinstance(kwargs['id'], str):
                # If id is a string, it's actually the session_id
                self.session_id = kwargs['id']
                # Don't set self.id for auto-increment
            else:
                self.session_id = kwargs.get('session_id', None)
                # Only set id if it's an integer (for existing records)
                if 'id' in kwargs and isinstance(kwargs['id'], int):
                    self.id = kwargs['id']
            
            self.user_id = kwargs.get('user_id', 'anonymous')
            self.started_at = kwargs.get('started_at', datetime.now())
            self.last_activity = kwargs.get('last_activity', datetime.now())
            self.total_interactions = kwargs.get('total_interactions', 0)
            self.current_context_id = kwargs.get('current_context_id', None)
            self.context_history = kwargs.get('context_history', [])
            self.session_summary = kwargs.get('session_summary', '')
            self.meta_data = kwargs.get('meta_data', {})

    # ============================================================================
    # DATABASE MODELS
    # ============================================================================
    
    class UnifiedUserPreferences(Base):
        """Unified user preferences - Single source of truth for all systems"""
        __tablename__ = 'user_preferences'
        
        id = Column(Integer, primary_key=True)
        user_id = Column(String(50), nullable=False, default='default')
        preferred_tools = Column(JSON, nullable=False)
        communication_preferences = Column(JSON, nullable=False)
        technical_preferences = Column(JSON, nullable=False)
        workflow_preferences = Column(JSON, nullable=False)
        avoid_patterns = Column(JSON, nullable=False)
        custom_preferences = Column(JSON, nullable=True)
        last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)
        created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Set defaults if not provided
            if self.preferred_tools is None:
                self.preferred_tools = {
                    "database": "SQLite",
                    "language": "Python",
                    "protocol": "MCP"
                }
            if self.communication_preferences is None:
                self.communication_preferences = {
                    "style": "concise",
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
            if self.custom_preferences is None:
                self.custom_preferences = {}
        
        def to_dict(self) -> Dict[str, Any]:
            """Convert to dictionary format"""
            return {
                'id': self.id,
                'user_id': self.user_id,
                'preferred_tools': self.preferred_tools,
                'communication_preferences': self.communication_preferences,
                'technical_preferences': self.technical_preferences,
                'workflow_preferences': self.workflow_preferences,
                'avoid_patterns': self.avoid_patterns,
                'custom_preferences': self.custom_preferences,
                'last_updated': self.last_updated.isoformat() if self.last_updated else None,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        
        def update_from_dict(self, data: Dict[str, Any]):
            """Update from dictionary data"""
            for key, value in data.items():
                if hasattr(self, key) and key not in ['id', 'created_at']:
                    setattr(self, key, value)
            self.last_updated = datetime.utcnow()
        
        def get_formatted_preferences(self) -> str:
            """Get formatted preferences string for prompt injection"""
            formatted = "User Preferences:\n"
            
            # Preferred tools
            if self.preferred_tools:
                for key, value in self.preferred_tools.items():
                    formatted += f"    - Use {value} for {key}\n"
            
            # Communication preferences
            if self.communication_preferences:
                for key, value in self.communication_preferences.items():
                    formatted += f"    - Communication {key}: {value}\n"
            
            # Technical preferences
            if self.technical_preferences:
                for key, value in self.technical_preferences.items():
                    formatted += f"    - Technical {key}: {value}\n"
            
            # Workflow preferences
            if self.workflow_preferences:
                for pref in self.workflow_preferences:
                    formatted += f"    - Workflow: {pref}\n"
            
            # Avoid patterns
            if self.avoid_patterns:
                for pattern in self.avoid_patterns:
                    formatted += f"    - Avoid: {pattern}\n"
            
            # Custom preferences
            if self.custom_preferences:
                for key, value in self.custom_preferences.items():
                    formatted += f"    - {key}: {value}\n"
            
            # Last updated
            if self.last_updated:
                formatted += f"    - Last Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            return formatted

else:
    # Fallback classes when SQLAlchemy is not available
    class UnifiedInteraction(UnifiedModel):
        """Fallback interaction model without SQLAlchemy"""
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Set all attributes explicitly to ensure they're accessible
            self.id = kwargs.get('id', kwargs.get('interaction_id', None))
            self.interaction_id = kwargs.get('interaction_id', kwargs.get('id', None))
            self.timestamp = kwargs.get('timestamp', datetime.now())
            self.session_id = kwargs.get('session_id', None)
            self.user_id = kwargs.get('user_id', 'anonymous')
            self.interaction_type = kwargs.get('interaction_type', 'conversation_turn')
            self.client_request = kwargs.get('client_request', kwargs.get('prompt', ''))
            self.agent_response = kwargs.get('agent_response', kwargs.get('response', ''))
            self.prompt = kwargs.get('prompt', '')
            self.response = kwargs.get('response', '')
            self.full_content = kwargs.get('full_content', '')
            self.context_summary = kwargs.get('context_summary', '')
            self.semantic_keywords = kwargs.get('semantic_keywords', [])
            self.topic_category = kwargs.get('topic_category', 'general')
            self.status = kwargs.get('status', 'completed')
            self.execution_time_ms = kwargs.get('execution_time_ms', 0)
            self.interaction_metadata = kwargs.get('metadata', kwargs.get('meta_data', {}))
            self.meta_data = kwargs.get('meta_data', {})
            self.tool_name = kwargs.get('tool_name', None)
            
            # Store additional attributes that might be passed
            for key, value in kwargs.items():
                if not hasattr(self, key):
                    setattr(self, key, value)

    class UnifiedSession(UnifiedModel):
        """Fallback session model without SQLAlchemy"""
        
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Handle ID properly - don't override auto-increment id with string
            if 'id' in kwargs and isinstance(kwargs['id'], str):
                # If id is a string, it's actually the session_id
                self.session_id = kwargs['id']
                # Don't set self.id for auto-increment
            else:
                self.session_id = kwargs.get('session_id', None)
                # Only set id if it's an integer (for existing records)
                if 'id' in kwargs and isinstance(kwargs['id'], int):
                    self.id = kwargs['id']
            
            self.user_id = kwargs.get('user_id', 'anonymous')
            self.started_at = kwargs.get('started_at', datetime.now())
            self.last_activity = kwargs.get('last_activity', datetime.now())
            self.total_interactions = kwargs.get('total_interactions', 0)
            self.current_context_id = kwargs.get('current_context_id', None)
            self.context_history = kwargs.get('context_history', [])
            self.session_summary = kwargs.get('session_summary', '')
            self.meta_data = kwargs.get('meta_data', {})

class UnifiedConversationContext(UnifiedModel):
    """Unified conversation context model that works in both environments"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.session_id = kwargs.get('session_id', None)
        self.user_id = kwargs.get('user_id', 'anonymous')
        self.context_summary = kwargs.get('context_summary', '')
        self.semantic_context = kwargs.get('semantic_context', {})
        self.key_topics = kwargs.get('key_topics', [])
        self.user_preferences = kwargs.get('user_preferences', {})
        self.project_context = kwargs.get('project_context', {})
        self.context_type = kwargs.get('context_type', 'general')
        self.relevance_score = kwargs.get('relevance_score', 0.0)
        self.usage_count = kwargs.get('usage_count', 0)
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())

class UnifiedConversation(UnifiedModel):
    """Unified conversation model that works in both environments"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.session_id = kwargs.get('session_id', None)
        self.user_id = kwargs.get('user_id', 'anonymous')
        self.conversation_type = kwargs.get('conversation_type', 'general')
        self.title = kwargs.get('title', '')
        self.summary = kwargs.get('summary', '')
        self.interaction_count = kwargs.get('interaction_count', 0)
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at', datetime.now())
        self.meta_data = kwargs.get('meta_data', {})

# ============================================================================
# STORAGE AND SESSION FACTORY
# ============================================================================

class UnifiedStorage(UnifiedModel):
    """Unified storage interface that works in both environments"""
    
    def __init__(self):
        super().__init__()
        self._env = _CURRENT_ENV
        self._local_interactions: List[UnifiedInteraction] = []
        self._local_sessions: List[UnifiedSession] = []
        self._local_conversations: List[UnifiedConversation] = []
        
        # Initialize with sample data for local development
        if self.is_local and not self._local_sessions:
            self._initialize_sample_data()
    
    @property
    def is_local(self) -> bool:
        return self._env == Environment.LOCAL
    
    @property
    def is_production(self) -> bool:
        return self._env == Environment.PRODUCTION
    
    def _initialize_sample_data(self):
        """Initialize with sample data for local development"""
        # Create sample session
        sample_session = UnifiedSession(
            session_id="sample-session",
            user_id="sample-user",
            started_at=datetime.now(),
            total_interactions=0
        )
        self._local_sessions.append(sample_session)
    
    def add_interaction(self, interaction: UnifiedInteraction):
        """Add an interaction"""
        if self.is_local:
            self._local_interactions.append(interaction)
        # In production, this would save to database
    
    def get_interactions(self, limit: int = 10) -> List[UnifiedInteraction]:
        """Get interactions"""
        if self.is_local:
            return self._local_interactions[-limit:] if limit else self._local_interactions
        # In production, this would query database
        return []
    
    def add_session(self, session: UnifiedSession):
        """Add a session"""
        if self.is_local:
            self._local_sessions.append(session)
        # In production, this would save to database
    
    def get_sessions(self) -> List[UnifiedSession]:
        """Get sessions"""
        if self.is_local:
            return self._local_sessions
        # In production, this would query database
        return []
    
    def add_conversation(self, conversation: UnifiedConversation):
        """Add a conversation"""
        if self.is_local:
            self._local_conversations.append(conversation)
        # In production, this would save to database
    
    def get_conversations(self) -> List[UnifiedConversation]:
        """Get conversations"""
        if self.is_local:
            return self._local_conversations
        # In production, this would query database
        return []

class UnifiedSessionFactory:
    """Unified session factory that works in both environments"""
    
    def __init__(self):
        self._env = _CURRENT_ENV
        self._engine = None
        self._SessionLocal = None
    
    def _get_engine_and_session(self):
        """Get or create engine and session factory"""
        # Use global database if available
        if _global_engine and _global_session_factory:
            return _global_engine, _global_session_factory
        
        # Initialize global database if not already done
        if not _global_engine:
            initialize_global_database()
        
        # Use global database
        if _global_engine and _global_session_factory:
            return _global_engine, _global_session_factory
        
        # Fallback to local creation
        if self._engine is None:
            try:
                from sqlalchemy import create_engine
                from sqlalchemy.orm import sessionmaker
                
                # Get database URL
                from models_unified import get_database_url
                database_url = get_database_url()
                
                # Create engine
                self._engine = create_engine(database_url, echo=False)
                
                # Create tables if they don't exist
                if SQLALCHEMY_AVAILABLE and Base:
                    Base.metadata.create_all(bind=self._engine)
                
                # Create session factory with explicit Base registry
                self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
                
            except Exception as e:
                print(f"⚠️  Failed to create engine: {e}")
                return None, None
        
        return self._engine, self._SessionLocal
    
    def __call__(self):
        """Create a new session"""
        if self.is_production:
            try:
                # Try to use SQLAlchemy session
                from sqlalchemy.orm import Session
                # Use local implementation instead of circular import
                SessionLocal = UnifiedSessionFactory()
                return SessionLocal()
            except Exception:
                # Fallback to mock session
                return MockSession()
        else:
            # For local environment, try to use real SQLAlchemy session
            try:
                # Try to get a working session directly
                return get_global_session()
                    
            except Exception as e:
                print(f"⚠️  Failed to create real session for local environment: {e}")
                print("   Trying explicit Base session...")
                
                # Try the explicit Base approach
                try:
                    session = create_session_with_explicit_base()
                    if session:
                        return session
                except Exception as e2:
                    print(f"⚠️  Explicit Base session also failed: {e2}")
                
                print("   Falling back to MockSession")
                return MockSession()
    
    @property
    def is_local(self) -> bool:
        return self._env == Environment.LOCAL
    
    @property
    def is_production(self) -> bool:
        return self._env == Environment.PRODUCTION

class MockSession:
    """Mock database session for local development"""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def query(self, model_class):
        return MockQuery(model_class)
    
    def add(self, obj):
        pass
    
    def commit(self):
        pass
    
    def close(self):
        pass

class MockQuery:
    """Mock query for local development"""
    
    def __init__(self, model_class):
        self.model_class = model_class
        self._filters = []
        self._limit = None
    
    def filter(self, *args):
        self._filters.extend(args)
        return self
    
    def limit(self, limit):
        self._limit = limit
        return self
    
    def order_by(self, *args):
        return self
    
    def all(self):
        return []
    
    def first(self):
        return None
    
    def count(self):
        return 0

# ============================================================================
# MOCK COLUMN CLASS FOR BACKWARD COMPATIBILITY
# ============================================================================

class MockColumn:
    """Mock SQLAlchemy column for backward compatibility"""
    
    def __init__(self, name):
        self.name = name
    
    def desc(self):
        return f"{self.name} DESC"
    
    def __ge__(self, other):
        return True  # Always return True for comparison operations
    
    def __le__(self, other):
        return True
    
    def __gt__(self, other):
        return True
    
    def __lt__(self, other):
        return True
    
    def __eq__(self, other):
        return True
    
    def __ne__(self, other):
        return True

# ============================================================================
# COMPATIBILITY ALIASES
# ============================================================================

# For backward compatibility, provide the same names as the original files
# These are now class aliases that maintain the exact same interface

class AgentInteraction(UnifiedInteraction):
    """Backward compatibility wrapper for AgentInteraction"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Session(UnifiedSession):
    """Backward compatibility wrapper for Session"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ConversationContext(UnifiedConversationContext):
    """Backward compatibility wrapper for ConversationContext"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# ============================================================================
# BACKWARD COMPATIBILITY ALIASES
# ============================================================================

# For backward compatibility, provide the same names as the original files
# Use the proper SQLAlchemy models when available
if SQLALCHEMY_AVAILABLE and Base:
    AgentInteraction = UnifiedInteraction
    Session = UnifiedSession
    ConversationContext = UnifiedConversationContext
    LocalInteraction = UnifiedInteraction
    LocalSession = UnifiedSession
    LocalConversation = UnifiedConversation
else:
    # Fallback to non-SQLAlchemy models
    AgentInteraction = UnifiedInteraction
    Session = UnifiedSession
    ConversationContext = UnifiedConversationContext
    LocalInteraction = UnifiedInteraction
    LocalSession = UnifiedSession
    LocalConversation = UnifiedConversation

# Storage functions for backward compatibility
_unified_storage = UnifiedStorage()

def add_local_interaction(interaction: UnifiedInteraction):
    """Add a local interaction (backward compatibility)"""
    _unified_storage.add_interaction(interaction)

def get_local_interactions(limit: int = 10) -> List[UnifiedInteraction]:
    """Get local interactions (backward compatibility)"""
    return _unified_storage.get_interactions(limit)

def add_local_session(session: UnifiedSession):
    """Add a local session (backward compatibility)"""
    _unified_storage.add_session(session)

def get_local_sessions() -> List[UnifiedSession]:
    """Get local sessions (backward compatibility)"""
    return _unified_storage.get_sessions()

def add_local_conversation(conversation: UnifiedConversation):
    """Add a local conversation (backward compatibility)"""
    _unified_storage.add_conversation(conversation)

def get_local_conversations() -> List[UnifiedConversation]:
    """Get local conversations (backward compatibility)"""
    return _unified_storage.get_conversations()

# Database functions for backward compatibility
def get_session_factory():
    """Get database session factory (backward compatibility)"""
    return UnifiedSessionFactory()

def get_database_url():
    """Get database URL (backward compatibility)"""
    if _CURRENT_ENV == Environment.PRODUCTION:
        try:
            from config import Config
            return Config.get_database_url()
        except ImportError:
            pass
    
    # Default to local SQLite with absolute path
    return "sqlite:////Users/jonathanmorand/Documents/ProjectsFolder/MCP_FOLDER/MCP/MCP/data/agent_tracker.db"

def initialize_global_database():
    """Initialize global database engine and session factory"""
    global _global_engine, _global_session_factory
    
    if not SQLALCHEMY_AVAILABLE or not Base:
        return False
    
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # Create engine
        database_url = get_database_url()
        _global_engine = create_engine(database_url, echo=False)
        
        # Force class registration before creating tables
        force_class_registration()
        
        # Force Base configuration before creating tables
        try:
            if SQLALCHEMY_2X:
                # SQLAlchemy 2.x: use our shared registry
                if hasattr(Base, 'registry'):
                    Base.registry.configure()
                    print("✅ Base shared registry configured (SQLAlchemy 2.x)")
                else:
                    # Fallback to creating new registry
                    from sqlalchemy.orm import registry
                    reg = registry()
                    reg.configure()
                    print("✅ Base fallback registry configured (SQLAlchemy 2.x)")
            else:
                # SQLAlchemy 1.x: use configure_mappers()
                from sqlalchemy.orm import configure_mappers
                configure_mappers()
                print("✅ Base mappers configured (SQLAlchemy 1.x)")
        except Exception as e:
            print(f"⚠️  Base configuration warning: {e}")
        
        # Ensure all models are imported and registered
        try:
            from models_unified import UnifiedInteraction, UnifiedSession
            print("✅ Models imported for registration")
        except Exception as e:
            print(f"⚠️  Model import warning: {e}")
        
        # Create tables - handle both SQLAlchemy versions
        try:
            if SQLALCHEMY_2X and hasattr(Base, 'metadata'):
                Base.metadata.create_all(bind=_global_engine)
                print("✅ Tables created with SQLAlchemy 2.x metadata")
            elif hasattr(Base, 'metadata'):
                Base.metadata.create_all(bind=_global_engine)
                print("✅ Tables created with SQLAlchemy 1.x metadata")
            else:
                print("⚠️  No metadata available for table creation")
        except Exception as e:
            print(f"⚠️  Table creation warning: {e}")
        
        # Create session factory with proper SQLAlchemy 2.x binding
        if SQLALCHEMY_2X:
            # SQLAlchemy 2.x: use our shared registry
            if hasattr(Base, 'registry'):
                Base.registry.configure()
                print("✅ Using shared registry for session factory")
            else:
                # Fallback to creating new registry
                from sqlalchemy.orm import registry
                reg = registry()
                reg.configure()
                print("✅ Using fallback registry for session factory")
            
            # Create session factory
            _global_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=_global_engine)
            
            # Test the session factory immediately
            try:
                test_session = _global_session_factory()
                from models_unified import UnifiedInteraction, UnifiedSession
                
                # Test if session recognizes mapped classes
                test_session.query(UnifiedInteraction).count()
                test_session.query(UnifiedSession).count()
                
                test_session.close()
                print("✅ Global session factory properly bound to Base registry")
                
            except Exception as e:
                print(f"⚠️  Global session factory test failed: {e}")
                # Try to diagnose the issue
                try:
                    print(f"   Base type: {type(Base)}")
                    print(f"   Base metadata: {hasattr(Base, 'metadata')}")
                    print(f"   Base registry: {hasattr(Base, 'registry')}")
                    if hasattr(Base, 'registry'):
                        print(f"   Registry type: {type(Base.registry)}")
                except Exception as diag_e:
                    print(f"   Diagnosis failed: {diag_e}")
                
        else:
            # SQLAlchemy 1.x: traditional approach
            _global_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=_global_engine)
        
        print("✅ Global database initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to initialize global database: {e}")
        return False

def get_global_session():
    """Get a session from the global database with proper Base context"""
    if not _global_session_factory:
        initialize_global_database()
    
    if _global_session_factory:
        # Create session and ensure it knows about our mapped classes
        session = _global_session_factory()
        
        # Force the session to recognize our mapped classes
        try:
            # Import our classes in the session context
            from models_unified import UnifiedInteraction, UnifiedSession
            
            # Force SQLAlchemy to recognize our mapped classes
            # This is the key fix - we need to ensure the classes are registered
            if hasattr(session, 'registry'):
                # For SQLAlchemy 2.0+
                session.registry.configure()
            else:
                # For SQLAlchemy 1.x
                from sqlalchemy.orm import configure_mappers
                configure_mappers()
            
            # Test if session can see the mapped classes
            session.query(UnifiedInteraction).count()
            session.query(UnifiedSession).count()
            
            return session
        except Exception as e:
            print(f"⚠️  Session mapping issue: {e}")
            # Try to diagnose the issue
            try:
                print(f"   Session type: {type(session)}")
                print(f"   Session registry: {hasattr(session, 'registry')}")
                if hasattr(session, 'registry'):
                    print(f"   Registry type: {type(session.registry)}")
            except Exception as diag_e:
                print(f"   Diagnosis failed: {diag_e}")
            
            # Try to fix by refreshing the session
            session.close()
            session = _global_session_factory()
            return session
    else:
        raise Exception("Global database not initialized")

def create_session_with_explicit_base():
    """Create a session with explicit Base registry to ensure mapping works"""
    try:
        # Force class registration first
        force_class_registration()
        
        # Create a new engine and session factory with explicit Base
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        database_url = get_database_url()
        engine = create_engine(database_url, echo=False)
        
        # Create tables with our Base - handle both SQLAlchemy versions
        try:
            if hasattr(Base, 'metadata'):
                Base.metadata.create_all(bind=engine)
                print("✅ Tables created with Base metadata")
            else:
                print("⚠️  No metadata available for table creation")
        except Exception as e:
            print(f"⚠️  Table creation warning: {e}")
        
        # Create session factory with explicit Base binding
        if SQLALCHEMY_2X:
            # SQLAlchemy 2.x: use our shared registry
            if hasattr(Base, 'registry'):
                Base.registry.configure()
                print("✅ Using shared registry for explicit session")
            else:
                # Fallback to creating new registry
                from sqlalchemy.orm import registry
                reg = registry()
                reg.configure()
                print("✅ Using fallback registry for explicit session")
            
            # Create session factory bound to our registry
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session = SessionLocal()
            
            # Force the session to recognize our mapped classes
            try:
                # Import our classes in the session context
                from models_unified import UnifiedInteraction, UnifiedSession
                
                # Test if session can see the mapped classes
                session.query(UnifiedInteraction).count()
                session.query(UnifiedSession).count()
                
                print("✅ SQLAlchemy 2.x session bound to shared registry")
                return session
                
            except Exception as e:
                print(f"⚠️  Session binding failed: {e}")
                # Try to diagnose the issue
                try:
                    print(f"   Session type: {type(session)}")
                    print(f"   Session registry: {hasattr(session, 'registry')}")
                    if hasattr(session, 'registry'):
                        print(f"   Registry type: {type(session.registry)}")
                except Exception as diag_e:
                    print(f"   Diagnosis failed: {diag_e}")
                
                # Try alternative approach
                try:
                    # Use the global database session instead
                    return get_global_session()
                except Exception as e2:
                    print(f"⚠️  Global session also failed: {e2}")
                    return None
        else:
            # SQLAlchemy 1.x: traditional approach
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session = SessionLocal()
            
            # Force mapper configuration
            try:
                from sqlalchemy.orm import configure_mappers
                configure_mappers()
            except Exception as e:
                print(f"⚠️  Mapper configuration warning: {e}")
            
            print("✅ Session created with explicit Base registry (SQLAlchemy 1.x)")
            return session
        
    except Exception as e:
        print(f"❌ Failed to create session with explicit Base: {e}")
        return None

def init_database():
    """Initialize database (backward compatibility)"""
    if _CURRENT_ENV == Environment.PRODUCTION:
        try:
            # Use local implementation instead of circular import
            return None
        except ImportError:
            pass
    
    # For local development, just ensure the data directory exists
    os.makedirs("./data", exist_ok=True)
    return None

# ============================================================================
# ENVIRONMENT INFORMATION
# ============================================================================

def get_environment_info() -> Dict[str, Any]:
    """Get information about the current environment"""
    return {
        'environment': _CURRENT_ENV.value,
        'is_local': _CURRENT_ENV == Environment.LOCAL,
        'is_production': _CURRENT_ENV == Environment.PRODUCTION,
        'database_url': get_database_url(),
        'models_available': {
            'UnifiedInteraction': True,
            'UnifiedSession': True,
            'UnifiedConversationContext': True,
            'UnifiedConversation': True,
            'UnifiedStorage': True,
            'UnifiedSessionFactory': True
        }
    }

def switch_environment(env: Environment):
    """Switch to a different environment (for testing)"""
    global _CURRENT_ENV
    _CURRENT_ENV = env
    print(f"🔄 Switched to {env.value} environment")

# ============================================================================
# INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    # Print environment information
    info = get_environment_info()
    print("🚀 Unified Models System")
    print("=" * 40)
    print(f"Environment: {info['environment']}")
    print(f"Database: {info['database_url']}")
    print(f"Models: {', '.join(info['models_available'].keys())}")
    print("=" * 40)
