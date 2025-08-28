#!/usr/bin/env python3
"""
Conversation Data Extractor Tool
Extracts and formats conversation data from the MCP server database
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional
import docker
import psycopg2
from psycopg2.extras import RealDictCursor

class ConversationExtractor:
    """Extract and format conversation data from MCP server database"""
    
    def __init__(self, container_name: str = "mcp-postgres"):
        self.container_name = container_name
        self.docker_client = docker.from_env()
        
    def get_database_connection(self):
        """Get database connection from the PostgreSQL container"""
        try:
            # Get container info
            container = self.docker_client.containers.get(self.container_name)
            
            # Get database connection details
            env_vars = container.attrs['Config']['Env']
            db_config = {}
            for env_var in env_vars:
                if '=' in env_var:
                    key, value = env_var.split('=', 1)
                    db_config[key] = value
            
            # Connect to database
            conn = psycopg2.connect(
                host='localhost',  # Connect via port forwarding
                port=5432,
                database=db_config.get('POSTGRES_DB', 'mcp_tracker'),
                user=db_config.get('POSTGRES_USER', 'mcp_user'),
                password=db_config.get('POSTGRES_PASSWORD', 'mcp_password')
            )
            return conn
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            return None
    
    def extract_conversations(self, limit: int = 50, session_id: Optional[str] = None, 
                            interaction_type: Optional[str] = None) -> Dict[str, Any]:
        """Extract conversation data with filters"""
        conn = self.get_database_connection()
        if not conn:
            return {"error": "Database connection failed"}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Build query
                query = """
                SELECT 
                    id, timestamp, session_id, interaction_type,
                    prompt, response, full_content, status,
                    meta_data, execution_time_ms
                FROM mcp_tracker.agent_interactions
                WHERE 1=1
                """
                params = []
                
                if session_id:
                    query += " AND session_id = %s"
                    params.append(session_id)
                
                if interaction_type:
                    query += " AND interaction_type = %s"
                    params.append(interaction_type)
                
                query += " ORDER BY timestamp DESC LIMIT %s"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Convert to list of dicts
                conversations = []
                for row in rows:
                    conv = dict(row)
                    # Convert timestamp to string for JSON serialization
                    if conv['timestamp']:
                        conv['timestamp'] = conv['timestamp'].isoformat()
                    conversations.append(conv)
                
                return {
                    "total_found": len(conversations),
                    "limit": limit,
                    "filters": {
                        "session_id": session_id,
                        "interaction_type": interaction_type
                    },
                    "conversations": conversations
                }
                
        except Exception as e:
            return {"error": f"Query failed: {e}"}
        finally:
            conn.close()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get high-level conversation summary"""
        conn = self.get_database_connection()
        if not conn:
            return {"error": "Database connection failed"}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Get total counts by type
                cursor.execute("""
                    SELECT interaction_type, COUNT(*) as count
                    FROM mcp_tracker.agent_interactions
                    GROUP BY interaction_type
                    ORDER BY count DESC
                """)
                rows = cursor.fetchall()
                type_counts = {row['interaction_type']: row['count'] for row in rows}
                
                # Get recent activity
                cursor.execute("""
                    SELECT interaction_type, timestamp, 
                           LEFT(COALESCE(prompt, response), 100) as preview
                    FROM mcp_tracker.agent_interactions
                    WHERE interaction_type IN ('client_request', 'conversation_turn')
                    ORDER BY timestamp DESC
                    LIMIT 10
                """)
                recent_activity = []
                for row in cursor.fetchall():
                    recent_activity.append({
                        "type": row['interaction_type'],
                        "timestamp": row['timestamp'].isoformat() if row['timestamp'] else None,
                        "preview": row['preview']
                    })
                
                # Get session info
                cursor.execute("""
                    SELECT COUNT(*) as total_sessions,
                           COUNT(CASE WHEN last_activity > NOW() - INTERVAL '1 hour' THEN 1 END) as active_sessions
                    FROM mcp_tracker.sessions
                """)
                session_info = dict(cursor.fetchone())
                
                return {
                    "total_interactions": sum(int(v) for v in type_counts.values()),
                    "interaction_type_breakdown": type_counts,
                    "session_info": session_info,
                    "recent_activity": recent_activity,
                    "extracted_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {"error": f"Summary query failed: {e}"}
        finally:
            conn.close()
    
    def export_to_json(self, filename: str, limit: int = 100) -> str:
        """Export conversations to JSON file"""
        data = self.extract_conversations(limit=limit)
        if "error" in data:
            return f"❌ Export failed: {data['error']}"
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return f"✅ Exported {data['total_found']} conversations to {filename}"
        except Exception as e:
            return f"❌ Failed to write file: {e}"
    
    def get_user_conversations(self, user_id: str = "default_user", limit: int = 50) -> Dict[str, Any]:
        """Get conversations for a specific user"""
        conn = self.get_database_connection()
        if not conn:
            return {"error": "Database connection failed"}
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        ai.id, ai.timestamp, ai.session_id, ai.interaction_type,
                        ai.prompt, ai.response, ai.full_content, ai.status,
                        s.started_at, s.last_activity
                    FROM mcp_tracker.agent_interactions ai
                    LEFT JOIN mcp_tracker.sessions s ON ai.session_id = s.id
                    WHERE ai.user_id = %s
                    ORDER BY ai.timestamp DESC
                    LIMIT %s
                """, (user_id, limit))
                
                rows = cursor.fetchall()
                conversations = []
                for row in rows:
                    conv = dict(row)
                    if conv['timestamp']:
                        conv['timestamp'] = conv['timestamp'].isoformat()
                    if conv['started_at']:
                        conv['started_at'] = conv['started_at'].isoformat()
                    if conv['last_activity']:
                        conv['last_activity'] = conv['last_activity'].isoformat()
                    conversations.append(conv)
                
                return {
                    "user_id": user_id,
                    "total_found": len(conversations),
                    "conversations": conversations
                }
                
        except Exception as e:
            return {"error": f"User query failed: {e}"}
        finally:
            conn.close()

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Extract conversation data from MCP server")
    parser.add_argument("--limit", type=int, default=20, help="Number of conversations to extract")
    parser.add_argument("--session", type=str, help="Filter by session ID")
    parser.add_argument("--type", type=str, help="Filter by interaction type")
    parser.add_argument("--user", type=str, default="default_user", help="Filter by user ID")
    parser.add_argument("--export", type=str, help="Export to JSON file")
    parser.add_argument("--summary", action="store_true", help="Show conversation summary")
    parser.add_argument("--user-conversations", action="store_true", help="Show user conversations")
    
    args = parser.parse_args()
    
    extractor = ConversationExtractor()
    
    if args.summary:
        result = extractor.get_conversation_summary()
        print(json.dumps(result, indent=2))
    elif args.user_conversations:
        result = extractor.get_user_conversations(user_id=args.user, limit=args.limit)
        print(json.dumps(result, indent=2))
    elif args.export:
        result = extractor.export_to_json(args.export, limit=args.limit)
        print(result)
    else:
        result = extractor.extract_conversations(
            limit=args.limit,
            session_id=args.session,
            interaction_type=args.type
        )
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
