#!/usr/bin/env python3
"""
Simple Context Management UI
A clean, user-friendly interface for managing our context system
"""

import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our context system
try:
    from context_manager import SeamlessContextManager
    CONTEXT_SYSTEM_AVAILABLE = True
except ImportError as e:
    st.error(f"Context system not available: {e}")
    st.info("💡 Make sure all dependencies are installed: pip install -r requirements_ui.txt")
    CONTEXT_SYSTEM_AVAILABLE = False

try:
    from models_local import get_database_url, get_session_factory
    MODELS_AVAILABLE = True
except ImportError as e:
    st.warning(f"Models not available: {e}")
    MODELS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Context Manager",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-success { color: #28a745; }
    .status-warning { color: #ffc107; }
    .status-error { color: #dc3545; }
    .sidebar .sidebar-content { background-color: #f8f9fa; }
</style>
""", unsafe_allow_html=True)

def init_database_connection():
    """Initialize database connection"""
    try:
        db_path = Path("./data/agent_tracker_local.db")
        if not db_path.exists():
            st.warning("Database not found. Please ensure the context system is running.")
            return None
        
        conn = sqlite3.connect(str(db_path))
        return conn
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

def get_system_stats(conn):
    """Get system statistics from database"""
    if not conn:
        return {}
    
    try:
        # Basic counts
        interactions_count = pd.read_sql("SELECT COUNT(*) as count FROM agent_interactions", conn).iloc[0]['count']
        sessions_count = pd.read_sql("SELECT COUNT(*) as count FROM sessions", conn).iloc[0]['count']
        contexts_count = pd.read_sql("SELECT COUNT(*) as count FROM conversation_contexts", conn).iloc[0]['count']
        
        # Recent activity
        recent_interactions = pd.read_sql("""
            SELECT COUNT(*) as count FROM agent_interactions 
            WHERE timestamp > datetime('now', '-1 hour')
        """, conn).iloc[0]['count']
        
        # Error rate
        error_count = pd.read_sql("""
            SELECT COUNT(*) as count FROM agent_interactions 
            WHERE status = 'error'
        """, conn).iloc[0]['count']
        
        return {
            'total_interactions': interactions_count,
            'total_sessions': sessions_count,
            'total_contexts': contexts_count,
            'recent_activity': recent_interactions,
            'error_rate': error_count
        }
    except Exception as e:
        st.error(f"Error getting stats: {e}")
        return {}

def get_recent_interactions(conn, limit=10):
    """Get recent interactions"""
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                id, timestamp, session_id, interaction_type, 
                status, execution_time_ms,
                LENGTH(prompt) as prompt_length,
                LENGTH(response) as response_length
            FROM agent_interactions 
            ORDER BY timestamp DESC 
            LIMIT ?
        """
        return pd.read_sql(query, conn, params=(limit,))
    except Exception as e:
        st.error(f"Error getting interactions: {e}")
        return pd.DataFrame()

def get_session_summary(conn):
    """Get session summary"""
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                id, user_id, started_at, last_activity, 
                total_interactions,
                current_context_id
            FROM sessions 
            ORDER BY last_activity DESC
        """
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error getting sessions: {e}")
        return pd.DataFrame()

def get_context_summary(conn):
    """Get context summary"""
    if not conn:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                id, session_id, context_type, created_at, 
                relevance_score, usage_count, last_used
            FROM conversation_contexts 
            ORDER BY created_at DESC
        """
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error getting contexts: {e}")
        return pd.DataFrame()

def main():
    """Main application"""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Context Manager</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Dashboard", "Interactions", "Sessions", "Contexts", "System Status"]
    )
    
    # Initialize database connection
    conn = init_database_connection()
    
    if page == "Dashboard":
        show_dashboard(conn)
    elif page == "Interactions":
        show_interactions(conn)
    elif page == "Sessions":
        show_sessions(conn)
    elif page == "Contexts":
        show_contexts(conn)
    elif page == "System Status":
        show_system_status(conn)

def show_dashboard(conn):
    """Show main dashboard"""
    st.header("📊 System Overview")
    
    # Get system stats
    stats = get_system_stats(conn)
    
    if not stats:
        st.warning("Unable to load system statistics")
        return
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Interactions", stats.get('total_interactions', 0))
    
    with col2:
        st.metric("Active Sessions", stats.get('total_sessions', 0))
    
    with col3:
        st.metric("Context Objects", stats.get('total_contexts', 0))
    
    with col4:
        st.metric("Recent Activity (1h)", stats.get('recent_activity', 0))
    
    with col5:
        error_rate = stats.get('error_rate', 0)
        st.metric("Errors", error_rate, delta=None, delta_color="inverse")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Activity Timeline")
        if conn:
            try:
                # Get hourly activity for last 24 hours
                query = """
                    SELECT 
                        strftime('%H', timestamp) as hour,
                        COUNT(*) as count
                    FROM agent_interactions 
                    WHERE timestamp > datetime('now', '-1 day')
                    GROUP BY hour
                    ORDER BY hour
                """
                hourly_data = pd.read_sql(query, conn)
                
                if not hourly_data.empty:
                    fig = px.bar(hourly_data, x='hour', y='count', 
                               title="Interactions by Hour (Last 24h)")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No recent activity data available")
            except Exception as e:
                st.error(f"Error loading activity data: {e}")
    
    with col2:
        st.subheader("🔍 Interaction Types")
        if conn:
            try:
                query = """
                    SELECT interaction_type, COUNT(*) as count
                    FROM agent_interactions 
                    GROUP BY interaction_type
                """
                type_data = pd.read_sql(query, conn)
                
                if not type_data.empty:
                    fig = px.pie(type_data, values='count', names='interaction_type',
                               title="Interaction Type Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No interaction type data available")
            except Exception as e:
                st.error(f"Error loading type data: {e}")

def show_interactions(conn):
    """Show interactions management"""
    st.header("💬 Interactions")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        interaction_type = st.selectbox(
            "Interaction Type",
            ["All", "client_request", "agent_response", "conversation_turn", "error"]
        )
    
    with col2:
        status_filter = st.selectbox(
            "Status",
            ["All", "success", "error", "timeout"]
        )
    
    with col3:
        limit = st.slider("Show last N interactions", 10, 100, 20)
    
    # Get interactions
    interactions = get_recent_interactions(conn, limit)
    
    if interactions.empty:
        st.info("No interactions found")
        return
    
    # Apply filters
    if interaction_type != "All":
        interactions = interactions[interactions['interaction_type'] == interaction_type]
    
    if status_filter != "All":
        interactions = interactions[interactions['status'] == status_filter]
    
    # Display interactions
    st.subheader(f"📋 Recent Interactions ({len(interactions)} found)")
    
    # Format timestamp
    interactions['timestamp'] = pd.to_datetime(interactions['timestamp'])
    interactions['timestamp'] = interactions['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Display as table
    st.dataframe(
        interactions,
        use_container_width=True,
        hide_index=True
    )
    
    # Export option
    if st.button("📥 Export to CSV"):
        csv = interactions.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"interactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def show_sessions(conn):
    """Show sessions management"""
    st.header("🔄 Sessions")
    
    sessions = get_session_summary(conn)
    
    if sessions.empty:
        st.info("No sessions found")
        return
    
    # Format timestamps
    sessions['started_at'] = pd.to_datetime(sessions['started_at'])
    sessions['last_activity'] = pd.to_datetime(sessions['last_activity'])
    sessions['started_at'] = sessions['started_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    sessions['last_activity'] = sessions['last_activity'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Display sessions
    st.subheader(f"📋 Active Sessions ({len(sessions)} total)")
    
    st.dataframe(
        sessions,
        use_container_width=True,
        hide_index=True
    )
    
    # Session details
    if st.checkbox("Show session details"):
        selected_session = st.selectbox(
            "Select session to view details:",
            sessions['id'].tolist()
        )
        
        if selected_session and conn:
            try:
                # Get session interactions
                query = """
                    SELECT id, timestamp, interaction_type, status, prompt, response
                    FROM agent_interactions 
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                """
                session_interactions = pd.read_sql(query, conn, params=(selected_session,))
                
                if not session_interactions.empty:
                    st.subheader(f"Session: {selected_session}")
                    st.dataframe(session_interactions, use_container_width=True)
                else:
                    st.info("No interactions found for this session")
            except Exception as e:
                st.error(f"Error loading session details: {e}")

def show_contexts(conn):
    """Show contexts management"""
    st.header("🧠 Contexts")
    
    contexts = get_context_summary(conn)
    
    if contexts.empty:
        st.info("No contexts found")
        return
    
    # Format timestamps
    contexts['created_at'] = pd.to_datetime(contexts['created_at'])
    contexts['last_used'] = pd.to_datetime(contexts['last_used'])
    contexts['created_at'] = contexts['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    contexts['last_used'] = contexts['last_used'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Display contexts
    st.subheader(f"📋 Context Objects ({len(contexts)} total)")
    
    st.dataframe(
        contexts,
        use_container_width=True,
        hide_index=True
    )
    
    # Context analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Context Usage")
        if not contexts.empty:
            fig = px.histogram(contexts, x='usage_count', 
                             title="Context Usage Distribution",
                             nbins=10)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Relevance Scores")
        if not contexts.empty:
            fig = px.box(contexts, y='relevance_score', 
                        title="Context Relevance Distribution")
            st.plotly_chart(fig, use_container_width=True)

def show_system_status(conn):
    """Show system status and health"""
    st.header("⚙️ System Status")
    
    # Context system status
    st.subheader("🧠 Context System")
    
    if CONTEXT_SYSTEM_AVAILABLE:
        st.success("✅ Context system is available")
        
        # Try to initialize context manager
        try:
            with st.spinner("Initializing context manager..."):
                context_manager = SeamlessContextManager(auto_start=False)
                st.success("✅ Context manager initialized successfully")
                
                # Show system capabilities
                st.subheader("🔧 Available Capabilities")
                for system_name, system_info in context_manager.context_systems.items():
                    status_color = "🟢" if system_info['status'] == 'available' else "🔴"
                    st.write(f"{status_color} **{system_name}**: {system_info['status']}")
                    
                    if system_info['capabilities']:
                        st.write(f"   Capabilities: {', '.join(system_info['capabilities'])}")
                
        except Exception as e:
            st.error(f"❌ Failed to initialize context manager: {e}")
    else:
        st.error("❌ Context system is not available")
    
    # Database status
    st.subheader("🗄️ Database Status")
    
    if conn:
        st.success("✅ Database connection successful")
        
        # Test queries
        try:
            # Test basic queries
            test_interactions = pd.read_sql("SELECT COUNT(*) as count FROM agent_interactions", conn)
            test_sessions = pd.read_sql("SELECT COUNT(*) as count FROM sessions", conn)
            test_contexts = pd.read_sql("SELECT COUNT(*) as count FROM conversation_contexts", conn)
            
            st.write(f"✅ Interactions table: {test_interactions.iloc[0]['count']} records")
            st.write(f"✅ Sessions table: {test_sessions.iloc[0]['count']} records")
            st.write(f"✅ Contexts table: {test_contexts.iloc[0]['count']} records")
            
        except Exception as e:
            st.error(f"❌ Database test failed: {e}")
    else:
        st.error("❌ Database connection failed")
    
    # System info
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Python Version**: {sys.version}")
        st.write(f"**Working Directory**: {os.getcwd()}")
        if MODELS_AVAILABLE:
            st.write(f"**Database Path**: {get_database_url()}")
        else:
            st.write("**Database Path**: N/A (models not available)")
    
    with col2:
        st.write(f"**Current Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**Streamlit Version**: {st.__version__}")
        st.write(f"**Pandas Version**: {pd.__version__}")

if __name__ == "__main__":
    main()
