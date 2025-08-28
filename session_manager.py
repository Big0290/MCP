#!/usr/bin/env python3
"""
Enhanced Session Manager for Persistent Conversation Tracking
Handles session persistence across restarts and conversation changes
"""

import os
import json
import hashlib
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from pathlib import Path

from models import get_session_factory, Session, AgentInteraction, ConversationContext
from config import Config

@dataclass
class PersistentSession:
    """Persistent session data that survives restarts"""
    session_id: str
    user_id: str
    created_at: datetime
    last_activity: datetime
    total_interactions: int
    session_file_path: str
    metadata: Dict[str, Any]
    context_summary: Optional[str] = None
    active_topics: Optional[List[str]] = None
    user_preferences: Optional[Dict[str, Any]] = None

class SessionManager:
    """Manages persistent sessions across restarts and conversation changes"""
    
    def __init__(self):
        self._session_factory = None
        self._lock = threading.Lock()
        self._active_sessions: Dict[str, PersistentSession] = {}
        self._session_file_dir = Path("./data/sessions")
        self._session_file_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing sessions from disk
        self._load_persistent_sessions()
    
    @property
    def session_factory(self):
        """Lazy initialization of session factory"""
        if self._session_factory is None:
            self._session_factory = get_session_factory()
        return self._session_factory
    
    def _get_session_file_path(self, session_id: str) -> Path:
        """Get the file path for a session's persistent data"""
        return self._session_file_dir / f"{session_id}.json"
    
    def _load_persistent_sessions(self):
        """Load existing sessions from disk"""
        try:
            for session_file in self._session_file_dir.glob("*.json"):
                try:
                    with open(session_file, 'r') as f:
                        session_data = json.load(f)
                    
                    # Convert datetime strings back to datetime objects
                    session_data['created_at'] = datetime.fromisoformat(session_data['created_at'])
                    session_data['last_activity'] = datetime.fromisoformat(session_data['last_activity'])
                    
                    session = PersistentSession(**session_data)
                    
                    # Check if session is still valid (not too old)
                    if self._is_session_valid(session):
                        self._active_sessions[session.session_id] = session
                        print(f"📁 Loaded persistent session: {session.session_id}")
                    else:
                        # Remove old session file
                        session_file.unlink()
                        print(f"🗑️ Removed expired session: {session.session_id}")
                        
                except Exception as e:
                    print(f"⚠️ Failed to load session from {session_file}: {e}")
                    # Remove corrupted session file
                    session_file.unlink()
                    
        except Exception as e:
            print(f"⚠️ Error loading persistent sessions: {e}")
    
    def _is_session_valid(self, session: PersistentSession) -> bool:
        """Check if a session is still valid (not expired)"""
        # Sessions expire after 7 days of inactivity
        max_age = timedelta(days=7)
        return datetime.utcnow() - session.last_activity < max_age
    
    def _save_session_to_disk(self, session: PersistentSession):
        """Save session data to disk for persistence"""
        try:
            session_data = asdict(session)
            # Convert datetime objects to ISO strings for JSON serialization
            session_data['created_at'] = session.created_at.isoformat()
            session_data['last_activity'] = session.last_activity.isoformat()
            
            with open(session.session_file_path, 'w') as f:
                json.dump(session_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Failed to save session to disk: {e}")
    
    def _load_session_from_disk(self, session_id: str) -> Optional[PersistentSession]:
        """Load a specific session from disk"""
        session_file = self._get_session_file_path(session_id)
        if not session_file.exists():
            return None
        
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            # Convert datetime strings back to datetime objects
            session_data['created_at'] = datetime.fromisoformat(session_data['created_at'])
            session_data['last_activity'] = datetime.fromisoformat(session_data['last_activity'])
            
            return PersistentSession(**session_data)
            
        except Exception as e:
            print(f"⚠️ Failed to load session {session_id} from disk: {e}")
            return None
    
    def create_or_resume_session(self, user_id: Optional[str] = None, 
                                session_id: Optional[str] = None) -> str:
        """Create a new session or resume an existing one"""
        with self._lock:
            # If session_id is provided, try to resume it
            if session_id:
                existing_session = self._active_sessions.get(session_id)
                if existing_session:
                    # Update activity and save
                    existing_session.last_activity = datetime.utcnow()
                    self._save_session_to_disk(existing_session)
                    print(f"🔄 Resumed existing session: {session_id}")
                    return session_id
                
                # Try to load from disk
                disk_session = self._load_session_from_disk(session_id)
                if disk_session and self._is_session_valid(disk_session):
                    self._active_sessions[session_id] = disk_session
                    disk_session.last_activity = datetime.utcnow()
                    self._save_session_to_disk(disk_session)
                    print(f"📁 Resumed session from disk: {session_id}")
                    return session_id
            
            # Create new session
            new_session_id = session_id or self._generate_session_id(user_id)
            user_id = user_id or Config.USER_ID
            
            # Create session file path
            session_file_path = str(self._get_session_file_path(new_session_id))
            
            # Create persistent session
            session = PersistentSession(
                session_id=new_session_id,
                user_id=user_id,
                created_at=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                total_interactions=0,
                session_file_path=session_file_path,
                metadata={
                    'container_id': Config.CONTAINER_ID,
                    'environment': Config.ENVIRONMENT,
                    'created_by': 'session_manager'
                }
            )
            
            # Save to disk and memory
            self._active_sessions[new_session_id] = session
            self._save_session_to_disk(session)
            
            # Create database session record
            try:
                with self.session_factory() as db_session:
                    db_session_record = Session(
                        id=new_session_id,
                        user_id=user_id,
                        meta_data=session.metadata
                    )
                    db_session.add(db_session_record)
                    db_session.commit()
            except Exception as e:
                print(f"⚠️ Failed to create database session record: {e}")
            
            print(f"🆕 Created new persistent session: {new_session_id}")
            return new_session_id
    
    def _generate_session_id(self, user_id: Optional[str] = None) -> str:
        """Generate a unique session ID"""
        timestamp = datetime.utcnow().isoformat()
        user = user_id or Config.USER_ID
        content = f"{user}_{timestamp}_{os.getpid()}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def get_session(self, session_id: str) -> Optional[PersistentSession]:
        """Get a session by ID"""
        return self._active_sessions.get(session_id)
    
    def update_session_activity(self, session_id: str, interaction_count: int = 1):
        """Update session activity and save to disk"""
        with self._lock:
            session = self._active_sessions.get(session_id)
            if session:
                session.last_activity = datetime.utcnow()
                session.total_interactions += interaction_count
                self._save_session_to_disk(session)
                
                # Update database record
                try:
                    with self.session_factory() as db_session:
                        db_session_record = db_session.query(Session).filter(
                            Session.id == session_id
                        ).first()
                        if db_session_record:
                            db_session_record.last_activity = datetime.utcnow()
                            db_session_record.total_interactions = session.total_interactions
                            db_session.commit()
                except Exception as e:
                    print(f"⚠️ Failed to update database session: {e}")
    
    def update_session_context(self, session_id: str, context_summary: str, 
                             active_topics: List[str], user_preferences: Dict[str, Any]):
        """Update session context information"""
        with self._lock:
            session = self._active_sessions.get(session_id)
            if session:
                session.context_summary = context_summary
                session.active_topics = active_topics
                session.user_preferences = user_preferences
                self._save_session_to_disk(session)
    
    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """List all active sessions with their metadata"""
        sessions = []
        for session in self._active_sessions.values():
            sessions.append({
                'session_id': session.session_id,
                'user_id': session.user_id,
                'created_at': session.created_at.isoformat(),
                'last_activity': session.last_activity.isoformat(),
                'total_interactions': session.total_interactions,
                'context_summary': session.context_summary,
                'active_topics': session.active_topics,
                'user_preferences': session.user_preferences
            })
        return sessions
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions from memory and disk"""
        with self._lock:
            expired_sessions = []
            for session_id, session in self._active_sessions.items():
                if not self._is_session_valid(session):
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                session = self._active_sessions.pop(session_id)
                try:
                    # Remove session file
                    Path(session.session_file_path).unlink(missing_ok=True)
                    print(f"🗑️ Cleaned up expired session: {session_id}")
                except Exception as e:
                    print(f"⚠️ Failed to remove expired session file: {e}")
    
    def get_user_sessions(self, user_id: str) -> List[PersistentSession]:
        """Get all sessions for a specific user"""
        return [session for session in self._active_sessions.values() 
                if session.user_id == user_id]
    
    def merge_sessions(self, primary_session_id: str, secondary_session_id: str) -> bool:
        """Merge two sessions, keeping the primary one"""
        try:
            primary = self._active_sessions.get(primary_session_id)
            secondary = self._active_sessions.get(secondary_session_id)
            
            if not primary or not secondary:
                return False
            
            # Merge interaction counts
            primary.total_interactions += secondary.total_interactions
            
            # Merge context information
            if secondary.context_summary and not primary.context_summary:
                primary.context_summary = secondary.context_summary
            
            if secondary.active_topics:
                if not primary.active_topics:
                    primary.active_topics = []
                primary.active_topics.extend(secondary.active_topics)
                primary.active_topics = list(set(primary.active_topics))  # Remove duplicates
            
            if secondary.user_preferences:
                if not primary.user_preferences:
                    primary.user_preferences = {}
                primary.user_preferences.update(secondary.user_preferences)
            
            # Update activity to now
            primary.last_activity = datetime.utcnow()
            
            # Save primary session
            self._save_session_to_disk(primary)
            
            # Remove secondary session
            self._active_sessions.pop(secondary_session_id)
            Path(secondary.session_file_path).unlink(missing_ok=True)
            
            print(f"🔗 Merged session {secondary_session_id} into {primary_session_id}")
            return True
            
        except Exception as e:
            print(f"⚠️ Failed to merge sessions: {e}")
            return False
    
    def export_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Export complete session data for backup or analysis"""
        session = self._active_sessions.get(session_id)
        if not session:
            return None
        
        try:
            # Get database interactions
            with self.session_factory() as db_session:
                interactions = db_session.query(AgentInteraction).filter(
                    AgentInteraction.session_id == session_id
                ).order_by(AgentInteraction.timestamp).all()
                
                interaction_data = []
                for interaction in interactions:
                    interaction_data.append({
                        'id': interaction.id,
                        'timestamp': interaction.timestamp.isoformat(),
                        'type': interaction.interaction_type,
                        'prompt': interaction.prompt,
                        'response': interaction.response,
                        'status': interaction.status,
                        'metadata': interaction.meta_data
                    })
                
                # Get context data
                context = db_session.query(ConversationContext).filter(
                    ConversationContext.session_id == session_id
                ).first()
                
                context_data = None
                if context:
                    context_data = {
                        'context_summary': context.context_summary,
                        'semantic_context': context.semantic_context,
                        'key_topics': context.key_topics,
                        'user_preferences': context.user_preferences,
                        'project_context': context.project_context
                    }
            
            # Build export data with datetime-safe serialization
            session_dict = asdict(session)
            # Convert datetime objects to ISO strings for JSON serialization
            session_dict['created_at'] = session_dict['created_at'].isoformat()
            session_dict['last_activity'] = session_dict['last_activity'].isoformat()
            
            export_data = {
                'session_info': session_dict,
                'interactions': interaction_data,
                'context': context_data,
                'export_timestamp': datetime.utcnow().isoformat(),
                'export_version': '1.0'
            }
            
            return export_data
            
        except Exception as e:
            print(f"⚠️ Failed to export session data: {e}")
            return None

# Global session manager instance
session_manager = SessionManager()
