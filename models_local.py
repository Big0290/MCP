from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class AgentInteraction(Base):
    """Enhanced model for tracking client-agent conversations with full content retention"""
    __tablename__ = "agent_interactions"
    # No schema for SQLite compatibility
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    session_id = Column(String(255), nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    interaction_type = Column(String(100), nullable=False)  # 'client_request', 'agent_response', 'conversation_turn', 'error'
    tool_name = Column(String(255), nullable=True)  # Optional: which tool was used
    
    # Enhanced content fields for full retention
    prompt = Column(Text, nullable=True)  # Full client request/prompt (not truncated)
    response = Column(Text, nullable=True)  # Full agent response
    full_content = Column(Text, nullable=True)  # Complete interaction content for context
    
    # Context generation fields
    context_summary = Column(Text, nullable=True)  # Generated context summary
    semantic_keywords = Column(JSON, nullable=True)  # Extracted semantic keywords
    topic_category = Column(String(100), nullable=True)  # Categorized topic
    context_relevance_score = Column(Float, nullable=True)  # Relevance score for context injection
    
    # Tool and execution fields
    parameters = Column(JSON, nullable=True)  # Tool parameters if applicable
    execution_time_ms = Column(Integer, nullable=True)  # Optional: execution time if relevant
    status = Column(String(50), default='success')  # 'success', 'error', 'timeout'
    error_message = Column(Text, nullable=True)
    
    # Enhanced metadata
    meta_data = Column(JSON, nullable=True)  # Additional context like user agent, IP, etc.
    conversation_context = Column(JSON, nullable=True)  # Previous context that influenced this interaction

class ConversationContext(Base):
    """Model for storing conversation context that can be injected into future interactions"""
    __tablename__ = "conversation_contexts"
    # No schema for SQLite compatibility
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=False, index=True)
    user_id = Column(String(255), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Context content
    context_summary = Column(Text, nullable=False)  # Human-readable context summary
    semantic_context = Column(JSON, nullable=True)  # Structured semantic context
    key_topics = Column(JSON, nullable=True)  # List of key topics discussed
    user_preferences = Column(JSON, nullable=True)  # Inferred user preferences
    project_context = Column(JSON, nullable=True)  # Project-specific context
    
    # Context metadata
    context_type = Column(String(50), default='conversation')  # 'conversation', 'project', 'user_preference'
    relevance_score = Column(Float, default=1.0)  # How relevant this context is
    usage_count = Column(Integer, default=0)  # How many times this context has been used
    last_used = Column(DateTime, nullable=True)  # When this context was last injected
    
    # Context relationships
    related_interactions = Column(JSON, nullable=True)  # IDs of related interactions
    parent_context_id = Column(Integer, nullable=True)  # For hierarchical context

class Session(Base):
    """Enhanced model for tracking user sessions with context awareness"""
    __tablename__ = "sessions"
    # No schema for SQLite compatibility
    
    id = Column(String(255), primary_key=True)
    user_id = Column(String(255), nullable=True, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_interactions = Column(Integer, default=0)
    
    # Enhanced session context
    current_context_id = Column(Integer, nullable=True)  # Current active context
    context_history = Column(JSON, nullable=True)  # History of context changes
    session_summary = Column(Text, nullable=True)  # Summary of session so far
    
    meta_data = Column(JSON, nullable=True)

# Database configuration
def get_database_url():
    """Get database URL for local SQLite"""
    # Force local SQLite for local mode
    os.makedirs('./data', exist_ok=True)
    return f"sqlite:///./data/agent_tracker_local.db"

def get_session_factory():
    """Get session factory for local database"""
    engine = init_database()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

def init_database():
    """Initialize local SQLite database and create tables"""
    # Create engine and tables
    db_url = get_database_url()
    print(f"🔧 Initializing local database: {db_url}")
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine
