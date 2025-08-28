#!/usr/bin/env python3
"""
Local Interaction Logger - No Docker Required
Uses local SQLite database for conversation tracking
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from models_local import get_session_factory, AgentInteraction, Session

class InteractionLogger:
    """Enhanced logger for tracking client-agent interactions with full content retention"""
    
    def __init__(self):
        self.session_factory = get_session_factory()
    
    def _get_or_create_session(self, session_id: str = None) -> str:
        """Get existing session or create new one"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        with self.session_factory() as db_session:
            # Check if session exists
            existing_session = db_session.query(Session).filter(Session.id == session_id).first()
            
            if not existing_session:
                # Create new session
                new_session = Session(
                    id=session_id,
                    started_at=datetime.utcnow(),
                    last_activity=datetime.utcnow(),
                    total_interactions=0
                )
                db_session.add(new_session)
                db_session.commit()
                print(f"🆕 Created new persistent session: {session_id}")
            else:
                # Update existing session
                existing_session.last_activity = datetime.utcnow()
                existing_session.total_interactions += 1
                db_session.commit()
        
        return session_id
    
    def log_client_request(self, prompt: str, session_id: str = None, user_id: str = None, 
                          tool_name: str = None, meta_data: Dict = None) -> str:
        """Log a client request/prompt"""
        try:
            session_id = self._get_or_create_session(session_id)
            
            with self.session_factory() as db_session:
                interaction = AgentInteraction(
                    timestamp=datetime.utcnow(),
                    session_id=session_id,
                    user_id=user_id,
                    interaction_type='client_request',
                    tool_name=tool_name,
                    prompt=prompt,
                    full_content=prompt,
                    meta_data=meta_data or {}
                )
                db_session.add(interaction)
                db_session.commit()
                
                print(f"📝 Logged client request: {prompt[:50]}...")
                return session_id
                
        except Exception as e:
            print(f"Warning: Failed to log client request to database: {e}")
            return session_id or str(uuid.uuid4())
    
    def log_agent_response(self, response: str, session_id: str = None, user_id: str = None,
                          tool_name: str = None, execution_time_ms: int = None,
                          meta_data: Dict = None) -> str:
        """Log an agent response"""
        try:
            session_id = self._get_or_create_session(session_id)
            
            with self.session_factory() as db_session:
                interaction = AgentInteraction(
                    timestamp=datetime.utcnow(),
                    session_id=session_id,
                    user_id=user_id,
                    interaction_type='agent_response',
                    tool_name=tool_name,
                    response=response,
                    full_content=response,
                    execution_time_ms=execution_time_ms,
                    meta_data=meta_data or {}
                )
                db_session.add(interaction)
                db_session.commit()
                
                print(f"📝 Logged agent response: {response[:50]}...")
                return session_id
                
        except Exception as e:
            print(f"Warning: Failed to log agent response to database: {e}")
            return session_id or str(uuid.uuid4())
    
    def log_conversation_turn(self, client_request: str, agent_response: str,
                             session_id: str = None, user_id: str = None,
                             tool_name: str = None, execution_time_ms: int = None,
                             meta_data: Dict = None) -> str:
        """Log a complete conversation turn (client request + agent response)"""
        try:
            session_id = self._get_or_create_session(session_id)
            
            with self.session_factory() as db_session:
                # Log the conversation turn
                interaction = AgentInteraction(
                    timestamp=datetime.utcnow(),
                    session_id=session_id,
                    user_id=user_id,
                    interaction_type='conversation_turn',
                    tool_name=tool_name,
                    prompt=client_request,
                    response=agent_response,
                    full_content=f"Client: {client_request}\nAgent: {agent_response}",
                    execution_time_ms=execution_time_ms,
                    meta_data=meta_data or {}
                )
                db_session.add(interaction)
                db_session.commit()
                
                print(f"📝 Logged conversation turn for session: {session_id}")
                return session_id
                
        except Exception as e:
            print(f"Warning: Failed to log conversation turn to database: {e}")
            return session_id or str(uuid.uuid4())
    
    def log_error(self, error_message: str, session_id: str = None, user_id: str = None,
                  tool_name: str = None, meta_data: Dict = None) -> str:
        """Log an error that occurred during interaction"""
        try:
            session_id = self._get_or_create_session(session_id)
            
            with self.session_factory() as db_session:
                interaction = AgentInteraction(
                    timestamp=datetime.utcnow(),
                    session_id=session_id,
                    user_id=user_id,
                    interaction_type='error',
                    tool_name=tool_name,
                    error_message=error_message,
                    full_content=f"Error: {error_message}",
                    status='error',
                    meta_data=meta_data or {}
                )
                db_session.add(interaction)
                db_session.commit()
                
                print(f"❌ Logged error: {error_message[:50]}...")
                return session_id
                
        except Exception as e:
            print(f"Warning: Failed to log error to database: {e}")
            return session_id or str(uuid.uuid4())

# Create global logger instance
logger = InteractionLogger()
