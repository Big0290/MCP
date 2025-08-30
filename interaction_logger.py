import time
import uuid
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from contextlib import contextmanager
from functools import wraps
import threading

# Try to import dependencies, but don't fail if they're not available
try:
    from models_unified import get_session_factory, AgentInteraction, Session
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False
    print("⚠️ SQLAlchemy models not available - using fallback")

try:
    from config import Config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️ Config not available - using defaults")
    # Create a mock config
    class Config:
        USER_ID = "anonymous"
        ENABLE_AUTOMATIC_METADATA = True

try:
    from context_manager import seamless_context_manager
    CONTEXT_MANAGER_AVAILABLE = True
except ImportError:
    CONTEXT_MANAGER_AVAILABLE = False
    print("⚠️ Context manager not available - using fallback")

try:
    from session_manager import session_manager
    SESSION_MANAGER_AVAILABLE = True
except ImportError:
    SESSION_MANAGER_AVAILABLE = False
    print("⚠️ Session manager not available - using fallback")

class InteractionLogger:
    """Enhanced service for automatically logging client-agent conversations with full content retention"""
    
    def __init__(self):
        self._session_factory = None
        self._session_id = None
        self._user_id = None
        self._lock = threading.Lock()
        self._start_time = time.time()
    
    @property
    def session_factory(self):
        """Lazy initialization of session factory"""
        if self._session_factory is None:
            self._session_factory = get_session_factory()
        return self._session_factory
        
    def get_or_create_session(self, user_id: Optional[str] = None, session_id: Optional[str] = None) -> str:
        """Get existing session ID or create a new one, with support for session resumption"""
        if self._session_id:
            return self._session_id
            
        with self._lock:
            if self._session_id:  # Double-check pattern
                return self._session_id
                
            # Use session manager to create or resume session
            session_id = session_manager.create_or_resume_session(user_id, session_id)
            self._session_id = session_id
            self._user_id = user_id or Config.USER_ID
                
        return session_id
    
    def _get_automatic_metadata(self) -> Dict[str, Any]:
        """Automatically gather metadata without user input"""
        if not Config.ENABLE_AUTOMATIC_METADATA:
            return {}
            
        return {
            'system_info': {
                'hostname': os.uname().nodename if hasattr(os, 'uname') else 'unknown',
                'working_directory': os.getcwd(),
            },
            'process_info': {
                'pid': os.getpid(),
                'uptime_seconds': int(time.time() - self._start_time),
            },
            'timestamp': datetime.utcnow().isoformat(),
        }
    
    def log_interaction(self, 
                       interaction_type: str,
                       client_request: Optional[str] = None,
                       agent_response: Optional[str] = None,
                       error_message: Optional[str] = None,
                       status: str = 'success',
                       metadata: Optional[Dict[str, Any]] = None,
                       tool_name: Optional[str] = None,
                       parameters: Optional[Dict[str, Any]] = None,
                       execution_time_ms: Optional[int] = None):
        """Enhanced logging of client-agent interactions with full content retention"""
        
        # Merge automatic metadata with provided metadata
        auto_metadata = self._get_automatic_metadata()
        if metadata:
            auto_metadata.update(metadata)
        
        session_id = self.get_or_create_session()
        
        # Generate full content for context analysis
        full_content = ""
        if client_request and agent_response:
            full_content = f"Request: {client_request}\nResponse: {agent_response}"
        elif client_request:
            full_content = f"Request: {client_request}"
        elif agent_response:
            full_content = f"Response: {agent_response}"
        
        try:
            if MODELS_AVAILABLE and self.session_factory:
                with self.session_factory() as db_session:
                    interaction = AgentInteraction(
                        session_id=session_id,
                        user_id=self._user_id,
                        interaction_type=interaction_type,
                        tool_name=tool_name,
                        prompt=client_request,  # Store full prompt
                        response=agent_response,  # Store full response
                        full_content=full_content,  # Store complete interaction content
                        parameters=parameters,
                        execution_time_ms=execution_time_ms,
                        error_message=error_message,
                        status=status,
                        meta_data=auto_metadata
                    )
                    
                    db_session.add(interaction)
                    
                    # Update session activity using session manager
                    if SESSION_MANAGER_AVAILABLE:
                        session_manager.update_session_activity(session_id, 1)
                    
                    db_session.commit()
                    
                    # Trigger context update after logging
                    if CONTEXT_MANAGER_AVAILABLE:
                        try:
                            seamless_context_manager.create_or_update_context(session_id, self._user_id)
                        except Exception as e:
                            # Don't fail if context update fails
                            print(f"Warning: Failed to update context: {e}", file=os.sys.stderr)
            else:
                # Fallback: just print the interaction
                print(f"📝 [FALLBACK LOG] {interaction_type}: {client_request[:100] if client_request else 'No request'} -> {agent_response[:100] if agent_response else 'No response'}")
                
                # Try to trigger context update even without database logging
                if CONTEXT_MANAGER_AVAILABLE:
                    try:
                        seamless_context_manager.create_or_update_context(session_id, self._user_id)
                    except Exception as e:
                        print(f"Warning: Failed to update context: {e}", file=os.sys.stderr)
                
        except Exception as e:
            # Log error but don't fail the main application
            print(f"Warning: Failed to log interaction to database: {e}", file=os.sys.stderr)
    
    def log_client_request(self, request: str, metadata: Optional[Dict[str, Any]] = None):
        """Log a client request with full content retention"""
        self.log_interaction(
            interaction_type='client_request',
            client_request=request,
            metadata=metadata
        )
    
    def log_agent_response(self, response: str, metadata: Optional[Dict[str, Any]] = None):
        """Log an agent response with full content retention"""
        self.log_interaction(
            interaction_type='agent_response',
            agent_response=response,
            metadata=metadata
        )
    
    def log_conversation_turn(self, client_request: str, agent_response: str, metadata: Optional[Dict[str, Any]] = None):
        """Log a complete conversation turn with full content retention"""
        self.log_interaction(
            interaction_type='conversation_turn',
            client_request=client_request,
            agent_response=agent_response,
            metadata=metadata
        )
    
    def log_tool_call(self, tool_name: str, parameters: Dict[str, Any], execution_time_ms: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
        """Log a tool call with parameters and execution time"""
        self.log_interaction(
            interaction_type='tool_call',
            tool_name=tool_name,
            parameters=parameters,
            execution_time_ms=execution_time_ms,
            metadata=metadata
        )
    
    def log_tool_response(self, tool_name: str, response: str, execution_time_ms: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None):
        """Log a tool response with execution time"""
        self.log_interaction(
            interaction_type='tool_response',
            tool_name=tool_name,
            agent_response=response,
            execution_time_ms=execution_time_ms,
            metadata=metadata
        )
    
    def log_error(self, error_message: str, interaction_type: str = 'error', metadata: Optional[Dict[str, Any]] = None):
        """Log an error with context"""
        self.log_interaction(
            interaction_type=interaction_type,
            error_message=error_message,
            status='error',
            metadata=metadata
        )
    
    def get_context_for_injection(self, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get conversation context ready for injection into Cursor agent"""
        if not self._session_id:
            return None
        
        try:
            return seamless_context_manager.get_context_for_injection(self._session_id, user_id or self._user_id)
        except Exception as e:
            print(f"Warning: Failed to get context for injection: {e}", file=os.sys.stderr)
            return None
    
    def inject_context_into_prompt(self, base_prompt: str, user_id: Optional[str] = None) -> str:
        """Inject conversation context into a prompt for Cursor agent"""
        context = self.get_context_for_injection(user_id)
        if not context:
            return base_prompt
        
        try:
            return seamless_context_manager.inject_context_into_prompt(base_prompt, context)
        except Exception as e:
            print(f"Warning: Failed to inject context: {e}", file=os.sys.stderr)
            return base_prompt

# Global logger instance
logger = InteractionLogger()
