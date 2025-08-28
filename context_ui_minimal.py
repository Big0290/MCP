#!/usr/bin/env python3
"""
Simple Context Management UI - MINIMAL VERSION
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

# MINIMAL CSS - Only basic dark theme, NO chart interference
st.markdown("""
<style>
    /* MINIMAL CSS - Only basic dark theme */
    .stApp {
        background: #0f172a !important;
    }
    
    .main .block-container {
        background: #1e293b !important;
        color: #f8fafc !important;
    }
    
    [data-testid="stSidebar"] {
        background: #1e293b !important;
        color: #f8fafc !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #f8fafc !important;
    }
    
    .main-header {
        color: #f8fafc !important;
        font-size: 3rem !important;
        text-align: center;
        margin: 2rem 0;
    }
    
    .section-header {
        color: #f8fafc !important;
        font-size: 2rem !important;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid #475569;
    }
    
    /* NO CHART CSS - Let Plotly handle charts naturally */
</style>
""", unsafe_allow_html=True)

def init_database_connection():
    """Initialize database connection"""
    try:
        # Try local database first
        db_path = "./data/agent_tracker_local.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            return conn
        
        # Fallback to main database
        db_path = "./data/agent_tracker.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            return conn
            
        return None
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_system_stats(conn):
    """Get system statistics"""
    if not conn:
        return None
    
    try:
        stats = {}
        
        # Total interactions
        result = conn.execute("SELECT COUNT(*) FROM agent_interactions")
        stats['total_interactions'] = result.fetchone()[0]
        
        # Total sessions
        result = conn.execute("SELECT COUNT(*) FROM sessions")
        stats['total_sessions'] = result.fetchone()[0]
        
        # Total contexts
        result = conn.execute("SELECT COUNT(*) FROM conversation_contexts")
        stats['total_contexts'] = result.fetchone()[0]
        
        # Recent activity (last hour)
        result = conn.execute("""
            SELECT COUNT(*) FROM agent_interactions 
            WHERE timestamp > datetime('now', '-1 hour')
        """)
        stats['recent_activity'] = result.fetchone()[0]
        
        # Error rate
        result = conn.execute("""
            SELECT COUNT(*) FROM agent_interactions 
            WHERE status = 'error'
        """)
        error_count = result.fetchone()[0]
        stats['error_rate'] = error_count
        
        return stats
        
    except Exception as e:
        st.error(f"Error getting system stats: {e}")
        return None

def show_dashboard(conn):
    """Show main dashboard"""
    st.markdown('<div class="section-header">📊 System Overview</div>', unsafe_allow_html=True)
    
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
        st.markdown('<div class="section-header">📈 Activity Timeline</div>', unsafe_allow_html=True)
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
                
                # Debug info
                st.write(f"Debug: Found {len(hourly_data)} hourly data points")
                if not hourly_data.empty:
                    st.write("Debug: Sample data:", hourly_data.head())
                
                if not hourly_data.empty:
                    fig = px.bar(hourly_data, x='hour', y='count', 
                               title="Interactions by Hour (Last 24h)")
                    # Use white background with dark text for maximum readability
                    fig.update_traces(marker_color='#1e40af', marker_line_color='#0f172a', marker_line_width=1)
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(color='#0f172a', size=16),
                        xaxis=dict(gridcolor='#e2e8f0', zerolinecolor='#475569', color='#0f172a'),
                        yaxis=dict(gridcolor='#e2e8f0', zerolinecolor='#475569', color='#0f172a'),
                        title=dict(font=dict(color='#0f172a', size=18))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No recent activity data available - showing sample chart")
                    # Create sample chart when no data
                    sample_hours = [str(i).zfill(2) for i in range(24)]
                    sample_counts = [0] * 24
                    sample_data = pd.DataFrame({'hour': sample_hours, 'count': sample_counts})
                    fig = px.bar(sample_data, x='hour', y='count', 
                               title="Sample Activity Timeline (No Data Yet)")
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading activity data: {e}")
                st.write("Debug: Creating fallback chart due to error")
                # Create fallback chart on error
                sample_hours = [str(i).zfill(2) for i in range(24)]
                sample_counts = [0] * 24
                sample_data = pd.DataFrame({'hour': sample_hours, 'count': sample_counts})
                fig = px.bar(sample_data, x='hour', y='count', 
                           title="Fallback Activity Timeline")
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">🔍 Interaction Types</div>', unsafe_allow_html=True)
        if conn:
            try:
                query = """
                    SELECT interaction_type, COUNT(*) as count
                    FROM agent_interactions 
                    GROUP BY interaction_type
                """
                type_data = pd.read_sql(query, conn)
                
                # Debug info
                st.write(f"Debug: Found {len(type_data)} interaction types")
                if not type_data.empty:
                    st.write("Debug: Sample data:", type_data.head())
                
                if not type_data.empty:
                    fig = px.pie(type_data, values='count', names='interaction_type',
                               title="Interaction Type Distribution")
                    # Use white background with dark text for maximum readability
                    fig.update_traces(marker_colors=['#1e40af', '#7c3aed', '#059669', '#dc2626'])
                    fig.update_layout(
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(color='#0f172a', size=16),
                        title=dict(font=dict(color='#0f172a', size=18))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No interaction type data available - showing sample chart")
                    # Create sample chart when no data
                    sample_types = ['client_request', 'agent_response', 'conversation_turn', 'error']
                    sample_counts = [1, 1, 1, 1]  # At least 1 of each to show the chart
                    sample_data = pd.DataFrame({'interaction_type': sample_types, 'count': sample_counts})
                    fig = px.pie(sample_data, values='count', names='interaction_type',
                               title="Sample Interaction Types (No Data Yet)")
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading type data: {e}")
                st.write("Debug: Creating fallback chart due to error")
                # Create fallback chart on error
                sample_types = ['client_request', 'agent_response', 'conversation_turn', 'error']
                sample_counts = [1, 1, 1, 1]
                sample_data = pd.DataFrame({'interaction_type': sample_types, 'count': sample_counts})
                fig = px.pie(sample_data, values='count', names='interaction_type',
                           title="Fallback Interaction Types")
                st.plotly_chart(fig, use_container_width=True)

def show_interactions(conn):
    """Show interactions management"""
    st.markdown('<div class="section-header">💬 Interactions</div>', unsafe_allow_html=True)
    
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
        date_filter = st.date_input(
            "Date",
            value=datetime.now().date()
        )
    
    # Build query
    query = "SELECT * FROM agent_interactions WHERE 1=1"
    params = []
    
    if interaction_type != "All":
        query += " AND interaction_type = ?"
        params.append(interaction_type)
    
    if status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
    
    if date_filter:
        query += " AND DATE(timestamp) = ?"
        params.append(date_filter.strftime('%Y-%m-%d'))
    
    query += " ORDER BY timestamp DESC LIMIT 100"
    
    # Execute query
    if conn:
        try:
            interactions = pd.read_sql(query, conn, params=params)
            
            if not interactions.empty:
                st.success(f"Found {len(interactions)} interactions")
                st.dataframe(interactions, use_container_width=True)
            else:
                st.info("No interactions found with the selected filters")
                
        except Exception as e:
            st.error(f"Error loading interactions: {e}")
    else:
        st.error("Database connection not available")

def show_sessions(conn):
    """Show sessions management"""
    st.markdown('<div class="section-header">🔄 Sessions</div>', unsafe_allow_html=True)
    
    if conn:
        try:
            # Get recent sessions
            query = """
                SELECT 
                    session_id,
                    created_at,
                    last_activity,
                    interaction_count,
                    status
                FROM sessions 
                ORDER BY last_activity DESC 
                LIMIT 50
            """
            sessions = pd.read_sql(query, conn)
            
            if not sessions.empty:
                st.success(f"Found {len(sessions)} sessions")
                st.dataframe(sessions, use_container_width=True)
            else:
                st.info("No sessions found")
                
        except Exception as e:
            st.error(f"Error loading sessions: {e}")
    else:
        st.error("Database connection not available")

def show_contexts(conn):
    """Show contexts management"""
    st.markdown('<div class="section-header">🧠 Contexts</div>', unsafe_allow_html=True)
    
    if conn:
        try:
            # Get recent contexts
            query = """
                SELECT 
                    context_id,
                    session_id,
                    context_type,
                    relevance_score,
                    usage_count,
                    created_at
                FROM conversation_contexts 
                ORDER BY created_at DESC 
                LIMIT 50
            """
            contexts = pd.read_sql(query, conn)
            
            if not contexts.empty:
                st.success(f"Found {len(contexts)} contexts")
                st.dataframe(contexts, use_container_width=True)
            else:
                st.info("No contexts found")
                
        except Exception as e:
            st.error(f"Error loading contexts: {e}")
    else:
        st.error("Database connection not available")

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

def main():
    """Main application"""
    st.markdown('<h1 class="main-header">🧠 Context Manager</h1>', unsafe_allow_html=True)
    
    # Initialize database connection
    conn = init_database_connection()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Dashboard", "💬 Interactions", "🔄 Sessions", "🧠 Contexts", "⚙️ System Status"]
    )
    
    # Page routing
    if page == "📊 Dashboard":
        show_dashboard(conn)
    elif page == "💬 Interactions":
        show_interactions(conn)
    elif page == "🔄 Sessions":
        show_sessions(conn)
    elif page == "🧠 Contexts":
        show_contexts(conn)
    elif page == "⚙️ System Status":
        show_system_status(conn)

if __name__ == "__main__":
    main()
