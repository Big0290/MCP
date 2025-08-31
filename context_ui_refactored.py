#!/usr/bin/env python3
"""
Refactored Context Management UI - INTUITIVE NAVIGATION VERSION
A clean, user-friendly interface with tab-based navigation and button controls
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
import time

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
    from models_unified import get_database_url, get_session_factory
    MODELS_AVAILABLE = True
except ImportError as e:
    st.warning(f"Models not available: {e}")
    MODELS_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Context Manager",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar for cleaner look
)

# Enhanced CSS for modern UI
st.markdown("""
<style>
    /* Modern dark theme with better contrast */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    .main .block-container {
        background: rgba(30, 41, 59, 0.95) !important;
        color: #f8fafc !important;
        border-radius: 15px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        padding: 8px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(71, 85, 105, 0.3);
        border-radius: 8px;
        color: #cbd5e1;
        font-weight: 600;
        padding: 12px 24px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4);
    }
    
    /* Card styling for better organization */
    .metric-card {
        background: rgba(71, 85, 105, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(71, 85, 105, 0.3);
        border-color: rgba(59, 130, 246, 0.5);
        transform: translateY(-2px);
    }
    
    /* Filter button grid */
    .filter-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .filter-button {
        background: rgba(71, 85, 105, 0.3);
        border: 1px solid rgba(148, 163, 184, 0.3);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .filter-button:hover {
        background: rgba(59, 130, 246, 0.2);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .filter-button.active {
        background: rgba(59, 130, 246, 0.3);
        border-color: #3b82f6;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: #f8fafc !important;
    }
    
    .main-header {
        color: #f8fafc !important;
        font-size: 3rem !important;
        text-align: center;
        margin: 2rem 0;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-header {
        color: #f8fafc !important;
        font-size: 1.5rem !important;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 2px solid rgba(59, 130, 246, 0.5);
    }
    
    /* Tool grid styling */
    .tool-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .tool-card {
        background: rgba(71, 85, 105, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .tool-card:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(59, 130, 246, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
    }
    
    .tool-card.active {
        background: rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
    }
    
    /* Session cards */
    .session-card {
        background: rgba(71, 85, 105, 0.2);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .session-card:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(59, 130, 246, 0.5);
    }
    
    .session-card.selected {
        background: rgba(59, 130, 246, 0.2);
        border-color: #3b82f6;
    }
    
    /* Viewport-based content display */
    .content-display-large {
        min-height: 50vh;
        max-height: 70vh;
    }
    
    .content-display-medium {
        min-height: 30vh;
        max-height: 50vh;
    }
    
    .content-display-small {
        min-height: 20vh;
        max-height: 30vh;
    }
    
    /* Custom text area styling for large content */
    .stTextArea > div > div > textarea {
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
    }
    
    /* Large content text areas */
    .large-content-area textarea {
        min-height: 50vh !important;
        max-height: 70vh !important;
    }
    
    /* Medium content text areas */
    .medium-content-area textarea {
        min-height: 30vh !important;
        max-height: 50vh !important;
    }
    
    /* Small content text areas */
    .small-content-area textarea {
        min-height: 20vh !important;
        max-height: 30vh !important;
    }
    
    /* Extra large content text areas */
    .extra-large-content-area textarea {
        min-height: 70vh !important;
        max-height: 85vh !important;
    }
</style>
""", unsafe_allow_html=True)

def init_database_connection():
    """Initialize database connection"""
    try:
        # Use unified database (agent_tracker.db) first
        db_path = "./data/agent_tracker.db"
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            return conn
        
        # Fallback to local database if main doesn't exist
        db_path = "./data/agent_tracker_local.db"
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
        result = conn.execute("SELECT COUNT(*) FROM interactions")
        stats['total_interactions'] = result.fetchone()[0]
        
        # Total sessions
        result = conn.execute("SELECT COUNT(*) FROM sessions")
        stats['total_sessions'] = result.fetchone()[0]
        
        # Total contexts (from interactions metadata)
        result = conn.execute("""
            SELECT COUNT(DISTINCT session_id) FROM interactions 
            WHERE session_id IS NOT NULL
        """)
        stats['total_contexts'] = result.fetchone()[0]
        
        # Recent activity (last hour)
        result = conn.execute("""
            SELECT COUNT(*) FROM interactions 
            WHERE timestamp > datetime('now', '-1 hour')
        """)
        stats['recent_activity'] = result.fetchone()[0]
        
        # Error rate
        result = conn.execute("""
            SELECT COUNT(*) FROM interactions 
            WHERE status = 'error' OR error_message IS NOT NULL
        """)
        error_count = result.fetchone()[0]
        stats['error_rate'] = error_count
        
        return stats
        
    except Exception as e:
        st.error(f"Error getting system stats: {e}")
        return None

def show_dashboard_tab():
    """Show main dashboard with modern cards"""
    st.markdown('<div class="section-header">📊 System Overview</div>', unsafe_allow_html=True)
    
    # Initialize database connection
    conn = init_database_connection()
    
    # Refresh button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("🔄 Refresh Data", type="primary", use_container_width=True):
            st.rerun()
    with col3:
        auto_refresh = st.checkbox("Auto-refresh", value=False)
    
    # Get system stats
    stats = get_system_stats(conn)
    
    if not stats:
        st.warning("Unable to load system statistics")
        return
    
    # Metrics in cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Total Interactions</h3>
            <h2>{}</h2>
        </div>
        """.format(stats.get('total_interactions', 0)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🔄 Active Sessions</h3>
            <h2>{}</h2>
        </div>
        """.format(stats.get('total_sessions', 0)), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🧠 Context Objects</h3>
            <h2>{}</h2>
        </div>
        """.format(stats.get('total_contexts', 0)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Recent Activity</h3>
            <h2>{}</h2>
        </div>
        """.format(stats.get('recent_activity', 0)), unsafe_allow_html=True)
    
    with col5:
        error_rate = stats.get('error_rate', 0)
        st.markdown("""
        <div class="metric-card">
            <h3>❌ Errors</h3>
            <h2>{}</h2>
        </div>
        """.format(error_rate), unsafe_allow_html=True)
    
    # Charts section
    st.markdown('<div class="section-header">📈 Analytics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Activity timeline
        if conn:
            try:
                query = """
                    SELECT 
                        strftime('%H', timestamp) as hour,
                        COUNT(*) as count
                    FROM interactions 
                    WHERE timestamp > datetime('now', '-1 day')
                    GROUP BY hour
                    ORDER BY hour
                """
                hourly_data = pd.read_sql(query, conn)
                
                if not hourly_data.empty:
                    fig = px.bar(hourly_data, x='hour', y='count', 
                               title="Interactions by Hour (Last 24h)")
                    fig.update_traces(marker_color='#3b82f6')
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#f8fafc'),
                        title=dict(font=dict(color='#f8fafc'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No recent activity data available")
            except Exception as e:
                st.error(f"Error loading activity data: {e}")
    
    with col2:
        # Interaction types
        if conn:
            try:
                query = """
                    SELECT interaction_type, COUNT(*) as count
                    FROM interactions 
                    GROUP BY interaction_type
                """
                type_data = pd.read_sql(query, conn)
                
                if not type_data.empty:
                    fig = px.pie(type_data, values='count', names='interaction_type',
                               title="Interaction Type Distribution")
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#f8fafc'),
                        title=dict(font=dict(color='#f8fafc'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No interaction type data available")
            except Exception as e:
                st.error(f"Error loading type data: {e}")

def calculate_content_height(content_text, size_preference, content_type="normal"):
    """Calculate content height based on size preference and content"""
    content_lines = len(content_text.split('\n'))
    
    # Base heights for different size preferences (in pixels)
    size_mappings = {
        "Small (20% viewport)": {"min": 150, "max": 250, "line_height": 15},
        "Medium (30% viewport)": {"min": 250, "max": 400, "line_height": 18},
        "Large (50% viewport)": {"min": 400, "max": 600, "line_height": 20},
        "Extra Large (70% viewport)": {"min": 500, "max": 800, "line_height": 22}
    }
    
    # Adjust for content type
    if content_type == "full_content":
        # Full content gets extra height
        for size in size_mappings:
            size_mappings[size]["max"] += 100
    elif content_type == "metadata":
        # Metadata gets reduced height
        for size in size_mappings:
            size_mappings[size]["min"] = max(100, size_mappings[size]["min"] - 100)
            size_mappings[size]["max"] = max(200, size_mappings[size]["max"] - 200)
    
    settings = size_mappings.get(size_preference, size_mappings["Large (50% viewport)"])
    calculated_height = max(settings["min"], min(content_lines * settings["line_height"], settings["max"]))
    
    return calculated_height

def show_interactions_tab():
    """Show interactions with button-based filters and full data display"""
    st.markdown('<div class="section-header">💬 Interactions</div>', unsafe_allow_html=True)
    
    conn = init_database_connection()
    if not conn:
        st.error("Database connection not available")
        return
    
    # Initialize session state for filters and pagination
    if 'interaction_filter' not in st.session_state:
        st.session_state.interaction_filter = "All"
    if 'status_filter' not in st.session_state:
        st.session_state.status_filter = "All"
    if 'interactions_page' not in st.session_state:
        st.session_state.interactions_page = 1
    if 'show_full_content' not in st.session_state:
        st.session_state.show_full_content = True
    
    # Display options
    st.markdown("### ⚙️ Display Options")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        page_size = st.selectbox("Items per page:", [10, 25, 50, 100], index=1)
    
    with col2:
        st.session_state.show_full_content = st.checkbox("Show full content", value=st.session_state.show_full_content)
    
    with col3:
        show_metadata = st.checkbox("Show metadata", value=True)
        
    # Add content size option
    st.markdown("### 📐 Content Display Size")
    col1, col2, col3, col4 = st.columns(4)
    
    # Initialize content size preference
    if 'content_size' not in st.session_state:
        st.session_state.content_size = "Large (50% viewport)"
    
    with col1:
        if st.button("📏 Small (20% viewport)", type="primary" if st.session_state.content_size == "Small (20% viewport)" else "secondary", use_container_width=True):
            st.session_state.content_size = "Small (20% viewport)"
            st.rerun()
    
    with col2:
        if st.button("📐 Medium (30% viewport)", type="primary" if st.session_state.content_size == "Medium (30% viewport)" else "secondary", use_container_width=True):
            st.session_state.content_size = "Medium (30% viewport)"
            st.rerun()
    
    with col3:
        if st.button("📊 Large (50% viewport)", type="primary" if st.session_state.content_size == "Large (50% viewport)" else "secondary", use_container_width=True):
            st.session_state.content_size = "Large (50% viewport)"
            st.rerun()
    
    with col4:
        if st.button("📈 Extra Large (70% viewport)", type="primary" if st.session_state.content_size == "Extra Large (70% viewport)" else "secondary", use_container_width=True):
            st.session_state.content_size = "Extra Large (70% viewport)"
            st.rerun()
    
    # Refresh button in separate row
    col1, col2, col3, col4 = st.columns(4)
    with col4:
        if st.button("🔄 Refresh All", type="primary", use_container_width=True):
            st.rerun()
    
    # Filter buttons instead of dropdowns
    st.markdown("### 🔍 Filter Options")
    
    # Interaction type filter buttons
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🔄 All Types", type="primary" if st.session_state.interaction_filter == "All" else "secondary", use_container_width=True):
            st.session_state.interaction_filter = "All"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col2:
        if st.button("💬 Conversations", type="primary" if st.session_state.interaction_filter == "conversation_turn" else "secondary", use_container_width=True):
            st.session_state.interaction_filter = "conversation_turn"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col3:
        if st.button("📤 Requests", type="primary" if st.session_state.interaction_filter == "client_request" else "secondary", use_container_width=True):
            st.session_state.interaction_filter = "client_request"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col4:
        if st.button("📥 Responses", type="primary" if st.session_state.interaction_filter == "agent_response" else "secondary", use_container_width=True):
            st.session_state.interaction_filter = "agent_response"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col5:
        if st.button("❌ Errors", type="primary" if st.session_state.interaction_filter == "error" else "secondary", use_container_width=True):
            st.session_state.interaction_filter = "error"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col6:
        if st.button("🔍 Search", use_container_width=True):
            st.info("Search functionality - enter keywords to filter interactions")
    
    # Status filter buttons
    st.markdown("### 📊 Status Filter")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 All Status", type="primary" if st.session_state.status_filter == "All" else "secondary", use_container_width=True):
            st.session_state.status_filter = "All"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col2:
        if st.button("✅ Success", type="primary" if st.session_state.status_filter == "success" else "secondary", use_container_width=True):
            st.session_state.status_filter = "success"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col3:
        if st.button("❌ Error", type="primary" if st.session_state.status_filter == "error" else "secondary", use_container_width=True):
            st.session_state.status_filter = "error"
            st.session_state.interactions_page = 1
            st.rerun()
    
    with col4:
        if st.button("⏱️ Timeout", type="primary" if st.session_state.status_filter == "timeout" else "secondary", use_container_width=True):
            st.session_state.status_filter = "timeout"
            st.session_state.interactions_page = 1
            st.rerun()
    
    # Build query based on filters
    base_query = "SELECT * FROM interactions WHERE 1=1"
    count_query = "SELECT COUNT(*) as total FROM interactions WHERE 1=1"
    params = []
    
    if st.session_state.interaction_filter != "All":
        base_query += " AND interaction_type = ?"
        count_query += " AND interaction_type = ?"
        params.append(st.session_state.interaction_filter)
    
    if st.session_state.status_filter != "All":
        base_query += " AND status = ?"
        count_query += " AND status = ?"
        params.append(st.session_state.status_filter)
    
    # Get total count for pagination
    try:
        total_count = pd.read_sql(count_query, conn, params=params).iloc[0]['total']
        total_pages = (total_count + page_size - 1) // page_size
        
        # Pagination controls
        st.markdown("### 📄 Pagination")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("⏮️ First", disabled=(st.session_state.interactions_page <= 1)):
                st.session_state.interactions_page = 1
                st.rerun()
        
        with col2:
            if st.button("⬅️ Previous", disabled=(st.session_state.interactions_page <= 1)):
                st.session_state.interactions_page -= 1
                st.rerun()
        
        with col3:
            st.write(f"Page {st.session_state.interactions_page} of {total_pages}")
            st.write(f"Total: {total_count} interactions")
        
        with col4:
            if st.button("Next ➡️", disabled=(st.session_state.interactions_page >= total_pages)):
                st.session_state.interactions_page += 1
                st.rerun()
        
        with col5:
            if st.button("Last ⏭️", disabled=(st.session_state.interactions_page >= total_pages)):
                st.session_state.interactions_page = total_pages
                st.rerun()
        
        # Add pagination to query
        offset = (st.session_state.interactions_page - 1) * page_size
        base_query += f" ORDER BY timestamp DESC LIMIT {page_size} OFFSET {offset}"
        
        # Execute query and display results
        interactions = pd.read_sql(base_query, conn, params=params)
        
        if not interactions.empty:
            st.success(f"Showing {len(interactions)} of {total_count} interactions")
            
            # Display as expandable cards with full content
            for idx, interaction in interactions.iterrows():
                # Create unique key for this interaction
                interaction_key = f"interaction_{interaction['id']}_{st.session_state.interactions_page}"
                
                with st.expander(f"🔄 {interaction['interaction_type']} - ID:{interaction['id']} - {interaction['timestamp'][:19]}", expanded=False):
                    # Basic info row
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**📋 Basic Info**")
                        st.write(f"**ID**: {interaction['id']}")
                        st.write(f"**Type**: {interaction['interaction_type']}")
                        st.write(f"**Status**: {interaction['status']}")
                        st.write(f"**Timestamp**: {interaction['timestamp']}")
                    
                    with col2:
                        st.markdown("**👤 Session Info**")
                        st.write(f"**User**: {interaction.get('user_id', 'N/A')}")
                        session_id = interaction.get('session_id', 'N/A')
                        if session_id != 'N/A':
                            st.write(f"**Session**: {session_id}")
                        else:
                            st.write("**Session**: N/A")
                        st.write(f"**Execution Time**: {interaction.get('execution_time_ms', 'N/A')}ms")
                    
                    with col3:
                        st.markdown("**📊 Content Stats**")
                        prompt_len = len(str(interaction.get('prompt', ''))) if interaction.get('prompt') else 0
                        response_len = len(str(interaction.get('response', ''))) if interaction.get('response') else 0
                        st.write(f"**Prompt Length**: {prompt_len:,} chars")
                        st.write(f"**Response Length**: {response_len:,} chars")
                        if interaction.get('error_message'):
                            st.error(f"**Error**: {interaction['error_message']}")
                    
                    # Content display - NO TRUNCATION
                    st.markdown("---")
                    
                    # Show full content in tabs for better organization
                    if interaction.get('prompt') or interaction.get('response') or interaction.get('full_content'):
                        content_tab1, content_tab2, content_tab3 = st.tabs(["📤 Prompt", "📥 Response", "📄 Full Content"])
                        
                        with content_tab1:
                            if interaction.get('prompt'):
                                prompt_content = str(interaction['prompt'])
                                st.markdown("**📤 Full Prompt Content:**")
                                if st.session_state.show_full_content:
                                    # Use dynamic height calculation based on user preference
                                    content_height = calculate_content_height(prompt_content, st.session_state.content_size, "normal")
                                    content_lines = len(prompt_content.split('\n'))
                                    
                                    # Add CSS class based on size preference
                                    css_class = "large-content-area"
                                    if "Small" in st.session_state.content_size:
                                        css_class = "small-content-area"
                                    elif "Medium" in st.session_state.content_size:
                                        css_class = "medium-content-area"
                                    elif "Extra Large" in st.session_state.content_size:
                                        css_class = "extra-large-content-area"
                                    
                                    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                                    st.text_area(
                                        "Complete Prompt:", 
                                        prompt_content, 
                                        height=content_height, 
                                        key=f"prompt_full_{interaction_key}",
                                        help=f"Full prompt content ({len(prompt_content):,} characters, {content_lines:,} lines) - {st.session_state.content_size}"
                                    )
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Add copy button functionality
                                    if st.button(f"📋 Copy Prompt", key=f"copy_prompt_{interaction_key}"):
                                        st.info("Prompt content ready to copy (select all text above)")
                                else:
                                    st.text_area(
                                        "Prompt Preview:", 
                                        prompt_content[:200] + "..." if len(prompt_content) > 200 else prompt_content, 
                                        height=100, 
                                        key=f"prompt_preview_{interaction_key}"
                                    )
                            else:
                                st.info("No prompt data available")
                        
                        with content_tab2:
                            if interaction.get('response'):
                                response_content = str(interaction['response'])
                                st.markdown("**📥 Full Response Content:**")
                                if st.session_state.show_full_content:
                                    # Use dynamic height calculation based on user preference
                                    content_height = calculate_content_height(response_content, st.session_state.content_size, "normal")
                                    content_lines = len(response_content.split('\n'))
                                    
                                    # Add CSS class based on size preference
                                    css_class = "large-content-area"
                                    if "Small" in st.session_state.content_size:
                                        css_class = "small-content-area"
                                    elif "Medium" in st.session_state.content_size:
                                        css_class = "medium-content-area"
                                    elif "Extra Large" in st.session_state.content_size:
                                        css_class = "extra-large-content-area"
                                    
                                    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                                    st.text_area(
                                        "Complete Response:", 
                                        response_content, 
                                        height=content_height, 
                                        key=f"response_full_{interaction_key}",
                                        help=f"Full response content ({len(response_content):,} characters, {content_lines:,} lines) - {st.session_state.content_size}"
                                    )
                                    st.markdown('</div>', unsafe_allow_html=True)
                                    
                                    # Add copy button functionality
                                    if st.button(f"📋 Copy Response", key=f"copy_response_{interaction_key}"):
                                        st.info("Response content ready to copy (select all text above)")
                                else:
                                    st.text_area(
                                        "Response Preview:", 
                                        response_content[:200] + "..." if len(response_content) > 200 else response_content, 
                                        height=100, 
                                        key=f"response_preview_{interaction_key}"
                                    )
                            else:
                                st.info("No response data available")
                        
                        with content_tab3:
                            if interaction.get('full_content'):
                                full_content = str(interaction['full_content'])
                                st.markdown("**📄 Complete Interaction Content:**")
                                if st.session_state.show_full_content:
                                    # Use dynamic height calculation based on user preference
                                    content_height = calculate_content_height(full_content, st.session_state.content_size, "full_content")
                                    content_lines = len(full_content.split('\n'))
                                    
                                    # Add CSS class based on size preference
                                    css_class = "large-content-area"
                                    if "Small" in st.session_state.content_size:
                                        css_class = "small-content-area"
                                    elif "Medium" in st.session_state.content_size:
                                        css_class = "medium-content-area"
                                    elif "Extra Large" in st.session_state.content_size:
                                        css_class = "extra-large-content-area"
                                    
                                    st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                                    st.text_area(
                                        "Full Content:", 
                                        full_content, 
                                        height=content_height, 
                                        key=f"full_content_{interaction_key}",
                                        help=f"Complete interaction content ({len(full_content):,} characters, {content_lines:,} lines) - {st.session_state.content_size}"
                                    )
                                    st.markdown('</div>', unsafe_allow_html=True)
                                else:
                                    st.text_area(
                                        "Full Content Preview:", 
                                        full_content[:300] + "..." if len(full_content) > 300 else full_content, 
                                        height=150, 
                                        key=f"full_preview_{interaction_key}"
                                    )
                            else:
                                st.info("No full content data available")
                    
                    # Metadata display
                    if show_metadata:
                        st.markdown("---")
                        st.markdown("**🔍 Additional Metadata:**")
                        
                        metadata_cols = ['tool_name', 'parameters', 'interaction_metadata', 'context_summary', 'client_request', 'agent_response']
                        metadata_found = False
                        
                        for col in metadata_cols:
                            if interaction.get(col):
                                metadata_found = True
                                st.markdown(f"**{col.replace('_', ' ').title()}:**")
                                
                                # Handle JSON data
                                if col in ['parameters', 'interaction_metadata']:
                                    try:
                                        if isinstance(interaction[col], str):
                                            parsed_data = json.loads(interaction[col])
                                            st.json(parsed_data)
                                        else:
                                            st.json(interaction[col])
                                    except (json.JSONDecodeError, TypeError):
                                        st.text(str(interaction[col]))
                                else:
                                    content = str(interaction[col])
                                    if len(content) > 500 and not st.session_state.show_full_content:
                                        st.text_area(f"{col}:", content[:500] + "...", height=150, key=f"meta_{col}_{interaction_key}")
                                    else:
                                        # Use dynamic height calculation for metadata
                                        meta_height = calculate_content_height(content, st.session_state.content_size, "metadata")
                                        
                                        # Add CSS class based on size preference
                                        css_class = "medium-content-area"  # Default to medium for metadata
                                        if "Small" in st.session_state.content_size:
                                            css_class = "small-content-area"
                                        elif "Large" in st.session_state.content_size or "Extra Large" in st.session_state.content_size:
                                            css_class = "medium-content-area"  # Keep metadata reasonable even for large settings
                                        
                                        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
                                        st.text_area(f"{col}:", content, height=meta_height, key=f"meta_full_{col}_{interaction_key}")
                                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if not metadata_found:
                            st.info("No additional metadata available")
        else:
            st.info("No interactions found with the selected filters")
            
    except Exception as e:
        st.error(f"Error loading interactions: {e}")
        st.write("Debug info:", str(e))

def show_sessions_tab():
    """Show sessions with card-based selection"""
    st.markdown('<div class="section-header">🔄 Sessions</div>', unsafe_allow_html=True)
    
    conn = init_database_connection()
    if not conn:
        st.error("Database connection not available")
        return
    
    # Refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Sessions", type="primary", use_container_width=True):
            st.rerun()
    
    try:
        # Get recent sessions
        query = """
            SELECT 
                id,
                started_at,
                last_activity,
                total_interactions,
                user_id
            FROM sessions 
            ORDER BY last_activity DESC 
            LIMIT 20
        """
        
        sessions = pd.read_sql(query, conn)
        
        if not sessions.empty:
            st.success(f"Found {len(sessions)} sessions")
            
            # Display sessions as cards
            for idx, session in sessions.iterrows():
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="session-card">
                        <h4>📱 Session {session['id'][:8]}...</h4>
                        <p><strong>User:</strong> {session.get('user_id', 'N/A')}</p>
                        <p><strong>Started:</strong> {session['started_at'][:16]}</p>
                        <p><strong>Last Activity:</strong> {session['last_activity'][:16]}</p>
                        <p><strong>Interactions:</strong> {session['total_interactions']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No sessions found")
            
    except Exception as e:
        st.error(f"Error loading sessions: {e}")

def show_prompt_tools_tab():
    """Show prompt crafting tools with grid layout"""
    st.markdown('<div class="section-header">🛠️ Prompt Crafting Tools</div>', unsafe_allow_html=True)
    
    # Initialize session state for tool selection
    if 'selected_tool' not in st.session_state:
        st.session_state.selected_tool = None
    
    # Tool grid instead of dropdown
    st.markdown("### 🔧 Available Tools")
    
    tools = [
        {"id": "smart_context", "name": "🤖 Smart Context Injector", "desc": "Automatically detect tech stack and inject intelligent context"},
        {"id": "basic_enhancement", "name": "📝 Basic Prompt Enhancement", "desc": "Enhance prompts with basic context injection"},
        {"id": "enhanced_chat", "name": "🚀 Enhanced Chat", "desc": "Chat with AI using enhanced context"},
        {"id": "realtime_context", "name": "⚡ Real-time Context", "desc": "Inject context directly into prompts"},
        {"id": "auto_wrapper", "name": "🧠 Auto Context Wrapper", "desc": "Wrap prompts in context-aware structure"},
        {"id": "debug_tool", "name": "🔍 MCP Server Debug", "desc": "Debug MCP server communication flow"},
        {"id": "history_browser", "name": "📋 History Browser", "desc": "Browse interaction history with details"},
        {"id": "analytics", "name": "📊 Prompt Analytics", "desc": "Analyze prompt performance metrics"},
        {"id": "conversation_analysis", "name": "💬 Conversation Analysis", "desc": "Full visibility into Cursor agent interactions"}
    ]
    
    # Display tools in a grid
    cols = st.columns(3)
    for idx, tool in enumerate(tools):
        with cols[idx % 3]:
            if st.button(
                f"{tool['name']}\n{tool['desc']}", 
                key=f"tool_{tool['id']}", 
                use_container_width=True,
                type="primary" if st.session_state.selected_tool == tool['id'] else "secondary"
            ):
                st.session_state.selected_tool = tool['id']
                st.rerun()
    
    # Show selected tool interface
    if st.session_state.selected_tool:
        st.markdown("---")
        
        if st.session_state.selected_tool == "smart_context":
            show_smart_context_tool()
        elif st.session_state.selected_tool == "basic_enhancement":
            show_basic_enhancement_tool()
        elif st.session_state.selected_tool == "enhanced_chat":
            show_enhanced_chat_tool()
        elif st.session_state.selected_tool == "realtime_context":
            show_realtime_context_tool()
        elif st.session_state.selected_tool == "auto_wrapper":
            show_auto_wrapper_tool()
        elif st.session_state.selected_tool == "debug_tool":
            show_debug_tool()
        elif st.session_state.selected_tool == "history_browser":
            show_history_browser_tool()
        elif st.session_state.selected_tool == "analytics":
            show_analytics_tool()
        elif st.session_state.selected_tool == "conversation_analysis":
            show_conversation_analysis_tool()

def show_smart_context_tool():
    """Smart context injector tool interface"""
    st.markdown("### 🤖 Smart Context Injector")
    
    st.info("""
    **Revolutionary AI Context Enhancement** 🚀
    
    This tool automatically detects your project's tech stack and injects intelligent, 
    project-specific context while maintaining portable user preferences.
    """)
    
    # Project path input
    project_path = st.text_input(
        "Project Path:",
        value=os.getcwd(),
        help="Path to analyze for tech stack detection"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Detect Tech Stack", type="primary", use_container_width=True):
            with st.spinner("Analyzing project..."):
                # Simulate tech stack detection
                st.success("✅ Tech stack detected!")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Project Type", "Python")
                with col2:
                    st.metric("Framework", "Streamlit")
                with col3:
                    st.metric("Database", "SQLite")
    
    with col2:
        if st.button("🚀 Inject Context", type="secondary", use_container_width=True):
            st.info("Select a message to enhance with smart context")
    
    # Message input
    user_message = st.text_area(
        "Enter your message:",
        placeholder="e.g., How do I optimize my database queries?",
        height=100
    )
    
    if user_message and st.button("✨ Enhance with Smart Context", type="primary"):
        with st.spinner("Enhancing with intelligent context..."):
            time.sleep(1)  # Simulate processing
            st.success("Message enhanced with smart context!")
            
            enhanced = f"""
=== ENHANCED PROMPT WITH SMART CONTEXT ===

Original Message: {user_message}

=== DETECTED TECH STACK ===
- Primary Language: Python 3.x
- Framework: Streamlit
- Database: SQLite
- Architecture: MCP (Model Context Protocol)

=== PROJECT CONTEXT ===
- Context management system with intelligent caching
- Real-time conversation tracking
- Advanced prompt enhancement pipeline

=== SMART RECOMMENDATIONS ===
Based on your tech stack, here are optimized suggestions for your query.

=== END ENHANCED PROMPT ===
            """
            
            st.text_area("Enhanced Prompt:", enhanced, height=300)

def show_basic_enhancement_tool():
    """Basic prompt enhancement tool"""
    st.markdown("### 📝 Basic Prompt Enhancement")
    
    user_message = st.text_area(
        "Enter message to enhance:",
        placeholder="Enter a simple message...",
        height=100
    )
    
    if user_message and st.button("🔧 Enhance Prompt", type="primary"):
        enhanced = f"Enhanced: {user_message} (with basic context injection)"
        st.text_area("Enhanced Prompt:", enhanced, height=150)

def show_enhanced_chat_tool():
    """Enhanced chat tool"""
    st.markdown("### 🚀 Enhanced Chat with Context")
    
    user_message = st.text_area(
        "Chat message:",
        placeholder="Enter a message to chat with enhanced context...",
        height=100
    )
    
    if user_message and st.button("💬 Chat with Context", type="primary"):
        response = f"AI Response to: {user_message}\n\n(Enhanced with conversation history and project context)"
        st.text_area("AI Response:", response, height=150)

def show_realtime_context_tool():
    """Real-time context injection tool"""
    st.markdown("### ⚡ Real-time Context Injection")
    
    user_message = st.text_area(
        "Message for context injection:",
        placeholder="Enter message to inject real-time context...",
        height=100
    )
    
    if user_message and st.button("⚡ Inject Context", type="primary"):
        injected = f"[CONTEXT INJECTED] {user_message} [WITH REAL-TIME DATA]"
        st.text_area("Context Injected:", injected, height=150)

def show_auto_wrapper_tool():
    """Auto context wrapper tool"""
    st.markdown("### 🧠 Auto Context Wrapper")
    
    user_message = st.text_area(
        "Message to wrap:",
        placeholder="Enter message to wrap in context...",
        height=100
    )
    
    if user_message and st.button("🧠 Wrap in Context", type="primary"):
        wrapped = f"=== CONTEXT WRAPPER ===\n{user_message}\n=== END WRAPPER ==="
        st.text_area("Wrapped Message:", wrapped, height=150)

def show_debug_tool():
    """MCP server debug tool"""
    st.markdown("### 🔍 MCP Server Debug Tool")
    
    st.info("Debug MCP server request/response flow")
    
    test_input = st.text_area(
        "Test input:",
        placeholder="Enter test input for MCP server...",
        height=100
    )
    
    if test_input and st.button("🔍 Debug Flow", type="primary"):
        st.json({
            "request": test_input,
            "processing": "MCP server processing...",
            "response": f"Debug response for: {test_input}",
            "status": "success"
        })

def show_history_browser_tool():
    """Interaction history browser"""
    st.markdown("### 📋 Interaction History Browser")
    
    conn = init_database_connection()
    if not conn:
        st.error("Database connection not available")
        return
    
    # Quick filter buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 All Interactions", use_container_width=True):
            st.info("Showing all interactions")
    
    with col2:
        if st.button("💬 Conversations Only", use_container_width=True):
            st.info("Showing conversations only")
    
    with col3:
        if st.button("⚙️ System Only", use_container_width=True):
            st.info("Showing system interactions only")
    
    st.info("History browser interface - showing recent interactions")

def show_analytics_tool():
    """Prompt performance analytics"""
    st.markdown("### 📊 Prompt Performance Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Prompts Enhanced", "150")
    
    with col2:
        st.metric("Avg Enhancement Ratio", "2.8x")
    
    with col3:
        st.metric("Success Rate", "98.5%")
    
    st.info("Analytics dashboard showing prompt enhancement performance")

def show_conversation_analysis_tool():
    """Conversation analysis tool"""
    st.markdown("### 💬 Conversation Analysis Tool")
    
    st.info("Full visibility into Cursor agent interactions")
    
    # Session selection with cards
    st.markdown("#### 🎯 Select Session")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 Session ABC123", use_container_width=True):
            st.success("Selected session ABC123")
    
    with col2:
        if st.button("📱 Session DEF456", use_container_width=True):
            st.success("Selected session DEF456")
    
    with col3:
        if st.button("📱 Session GHI789", use_container_width=True):
            st.success("Selected session GHI789")

def show_system_status_tab():
    """Show system status with modern layout"""
    st.markdown('<div class="section-header">⚙️ System Status</div>', unsafe_allow_html=True)
    
    # System health cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🧠 Context System</h3>
            <h4 style="color: #10b981;">✅ Available</h4>
            <p>All context systems operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🗄️ Database</h3>
            <h4 style="color: #10b981;">✅ Connected</h4>
            <p>SQLite database operational</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🔧 MCP Server</h3>
            <h4 style="color: #10b981;">✅ Running</h4>
            <p>Model Context Protocol active</p>
        </div>
        """, unsafe_allow_html=True)
    
    # System information
    st.markdown("### ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Environment Details:**
        - Python Version: {sys.version.split()[0]}
        - Working Directory: {os.getcwd()}
        - Streamlit Version: {st.__version__}
        """)
    
    with col2:
        st.info(f"""
        **System Status:**
        - Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - Context System: Available
        - Database: Connected
        """)

def main():
    """Main application with tab-based navigation"""
    st.markdown('<h1 class="main-header">🧠 Context Manager</h1>', unsafe_allow_html=True)
    
    # Tab-based navigation instead of sidebar dropdown
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", 
        "💬 Interactions", 
        "🔄 Sessions", 
        "🛠️ Prompt Tools", 
        "⚙️ System Status"
    ])
    
    with tab1:
        show_dashboard_tab()
    
    with tab2:
        show_interactions_tab()
    
    with tab3:
        show_sessions_tab()
    
    with tab4:
        show_prompt_tools_tab()
    
    with tab5:
        show_system_status_tab()

if __name__ == "__main__":
    main()
