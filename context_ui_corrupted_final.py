#!/usr/bin/env python3
"""
Simple Context Management UI - CLEAN VERSION
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

# Custom CSS for better styling - FRESH START
st.markdown("""
<style>
    /* FRESH START - Minimal CSS that won't interfere with charts */
    
    /* Basic dark theme for main containers only */
    .stApp {
        background: #0f172a !important;
    }
    
    .main .block-container {
        background: #1e293b !important;
        color: #f8fafc !important;
    }
    
    /* Sidebar dark theme */
    [data-testid="stSidebar"] {
        background: #1e293b !important;
        color: #f8fafc !important;
    }
    
    /* Basic text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
    }
    
    p, span, div {
        color: #f8fafc !important;
    }
    
    /* Custom headers */
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
    
    /* Basic form elements */
    .stSelectbox, .stTextInput, .stDateInput {
        background: #334155 !important;
        color: #f8fafc !important;
    }
    
    /* Tables */
    .stTable {
        background: #1e293b !important;
        color: #f8fafc !important;
    }
    
    /* NO CHART CSS - Let Plotly handle charts naturally */
</style>
""", unsafe_allow_html=True)

# JavaScript for dark theme enforcement
st.markdown("""
<script>
// Force dark theme on ALL elements
function forceDarkTheme() {
    // Force dark backgrounds everywhere
    const allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        if (el.tagName && !['SCRIPT', 'STYLE'].includes(el.tagName)) {
            // Force dark background
            el.style.setProperty('background', 'linear-gradient(135deg, #0f172a, #1e293b)', 'important');
            el.style.setProperty('background-color', '#0f172a', 'important');
            
            // Force light text
            el.style.setProperty('color', '#f8fafc', 'important');
            
            // Force larger fonts
            el.style.setProperty('font-size', '18px', 'important');
        }
    });
    
    // Force specific Streamlit containers
    const streamlitContainers = document.querySelectorAll('[data-testid]');
    streamlitContainers.forEach(el => {
        el.style.setProperty('background', 'linear-gradient(135deg, #1e293b, #334155)', 'important');
        el.style.setProperty('color', '#f8fafc', 'important');
    });
    
    // Force main app background
    const stApp = document.querySelector('.stApp');
    if (stApp) {
        stApp.style.setProperty('background', 'linear-gradient(135deg, #0f172a, #1e293b)', 'important');
    }
    
    // Force sidebar background
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.setProperty('background', 'linear-gradient(135deg, #1e293b, #334155)', 'important');
    }
    
    // Force main container background
    const mainContainer = document.querySelector('.main .block-container');
    if (mainContainer) {
        mainContainer.style.setProperty('background', 'linear-gradient(135deg, #1e293b, #334155)', 'important');
    }
}

// Run immediately and continuously
forceDarkTheme();
setInterval(forceDarkTheme, 500);

// Also run on DOM changes
const observer = new MutationObserver(forceDarkTheme);
observer.observe(document.body, { childList: true, subtree: true });

// Run when page loads
document.addEventListener('DOMContentLoaded', forceDarkTheme);
window.addEventListener('load', forceDarkTheme);
</script>
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
                
                if not hourly_data.empty:
                    fig = px.bar(hourly_data, x='hour', y='count', 
                               title="Interactions by Hour (Last 24h)")
                    # Fix chart colors for dark theme visibility
                    fig.update_traces(marker_color='#60a5fa', marker_line_color='#f8fafc', marker_line_width=1)
                    fig.update_layout(
                        plot_bgcolor='#1e293b',
                        paper_bgcolor='#1e293b',
                        font=dict(color='#f8fafc', size=14),
                        xaxis=dict(gridcolor='#475569', zerolinecolor='#64748b', color='#f8fafc'),
                        yaxis=dict(gridcolor='#475569', zerolinecolor='#64748b', color='#f8fafc'),
                        title=dict(font=dict(color='#f8fafc'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No recent activity data available")
            except Exception as e:
                st.error(f"Error loading activity data: {e}")
    
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
                
                if not type_data.empty:
                    fig = px.pie(type_data, values='count', names='interaction_type',
                               title="Interaction Type Distribution")
                    # Fix chart colors for dark theme visibility
                    fig.update_traces(marker_colors=['#60a5fa', '#a78bfa', '#34d399', '#f87171'])
                    fig.update_layout(
                        plot_bgcolor='#1e293b',
                        paper_bgcolor='#1e293b',
                        font=dict(color='#f8fafc', size=14),
                        title=dict(font=dict(color='#f8fafc'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No interaction type data available")
            except Exception as e:
                st.error(f"Error loading type data: {e}")

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
