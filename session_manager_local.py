#!/usr/bin/env python3
"""
Local Session Manager - No Docker Required
Manages conversation sessions using local SQLite database
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from models_local import get_session_factory, Session, AgentInteraction

class SessionManager:
    """Manages conversation sessions and context"""
    
    def __init__(self):
        self.session_factory = get_session_factory()
    
    def create_session(self, user_id: str = None, meta_data: Dict = None) -> str:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        
        with self.session_factory() as db_session:
            new_session = Session(
                id=session_id,
                user_id=user_id,
                started_at=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                total_interactions=0,
                meta_data=meta_data or {}
            )
            db_session.add(new_session)
            db_session.commit()
            
        print(f"🆕 Created new session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID"""
        with self.session_factory() as db_session:
            return db_session.query(Session).filter(Session.id == session_id).first()
    
    def update_session_activity(self, session_id: str, interaction_count: int = 1) -> bool:
        """Update session activity timestamp and interaction count"""
        try:
            with self.session_factory() as db_session:
                session = db_session.query(Session).filter(Session.id == session_id).first()
                if session:
                    session.last_activity = datetime.utcnow()
                    session.total_interactions += interaction_count
                    db_session.commit()
                    return True
                return False
        except Exception as e:
            print(f"Warning: Failed to update session activity: {e}")
            return False
    
    def get_active_sessions(self, hours_threshold: int = 1) -> List[Session]:
        """Get sessions active within the specified hours threshold"""
        with self.session_factory() as db_session:
            threshold_time = datetime.utcnow() - timedelta(hours=hours_threshold)
            return db_session.query(Session).filter(
                Session.last_activity > threshold_time
            ).all()
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of a session including interaction count and recent activity"""
        with self.session_factory() as db_session:
            session = db_session.query(Session).filter(Session.id == session_id).first()
            if not session:
                return {}
            
            # Get recent interactions for this session
            recent_interactions = db_session.query(AgentInteraction).filter(
                AgentInteraction.session_id == session_id
            ).order_by(AgentInteraction.timestamp.desc()).limit(5).all()
            
            summary = {
                'session_id': session.id,
                'user_id': session.user_id,
                'started_at': session.started_at.isoformat() if session.started_at else None,
                'last_activity': session.last_activity.isoformat() if session.last_activity else None,
                'total_interactions': session.total_interactions,
                'recent_interactions': []
            }
            
            for interaction in recent_interactions:
                summary['recent_interactions'].append({
                    'type': interaction.interaction_type,
                    'timestamp': interaction.timestamp.isoformat() if interaction.timestamp else None,
                    'preview': (interaction.prompt or interaction.response or '')[:100] if (interaction.prompt or interaction.response) else None
                })
            
            return summary
    
    def cleanup_old_sessions(self, days_threshold: int = 30) -> int:
        """Clean up sessions older than the specified days threshold"""
        try:
            with self.session_factory() as db_session:
                threshold_time = datetime.utcnow() - timedelta(days=days_threshold)
                old_sessions = db_session.query(Session).filter(
                    Session.last_activity < threshold_time
                ).all()
                
                deleted_count = 0
                for session in old_sessions:
                    # Delete related interactions first
                    db_session.query(AgentInteraction).filter(
                        AgentInteraction.session_id == session.id
                    ).delete()
                    
                    # Delete the session
                    db_session.delete(session)
                    deleted_count += 1
                
                db_session.commit()
                print(f"🧹 Cleaned up {deleted_count} old sessions")
                return deleted_count
                
        except Exception as e:
            print(f"Warning: Failed to cleanup old sessions: {e}")
            return 0

# Create global session manager instance
session_manager = SessionManager()
