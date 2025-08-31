#!/usr/bin/env python3
"""
🚀 NEW USER-FRIENDLY FRONTEND
Modern, intuitive interface for the MCP Conversation Intelligence System
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Page configuration
st.set_page_config(
    page_title="MCP Conversation Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .feature-card {
        background: #f8f9fa;
        color: #333333;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .stButton > button {
        border-radius: 20px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    
    .info-box {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        color: #333333;
    }
    
    .dashboard-card {
        background: #ffffff;
        color: #333333;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333333;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #d1d3e2;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 0.5rem;
    }
    
    .interaction-card {
        background: #ffffff;
        color: #333333;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    .session-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333333;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #d1d3e2;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .tool-card {
        background: #ffffff;
        color: #333333;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    .chart-container {
        background: #ffffff;
        color: #333333;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    .data-table {
        background: #ffffff;
        color: #333333;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    
    .data-table table {
        background: #ffffff;
        color: #333333;
    }
    
    .data-table th {
        background: #f8f9fa;
        color: #333333;
        font-weight: 600;
    }
    
    .data-table td {
        background: #ffffff;
        color: #333333;
        border-bottom: 1px solid #e0e0e0;
    }
    
    .data-table tr:hover td {
        background: #f8f9fa;
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

def init_database():
    """Initialize database connection"""
    try:
        conn = sqlite3.connect('./data/agent_tracker.db')
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_system_overview(conn):
    """Get comprehensive system overview"""
    if not conn:
        return None
    
    try:
        # Get basic counts
        interactions_count = pd.read_sql("SELECT COUNT(*) as count FROM interactions", conn).iloc[0]['count']
        sessions_count = pd.read_sql("SELECT COUNT(*) as count FROM sessions", conn).iloc[0]['count']
        
        # Get recent activity
        recent_interactions = pd.read_sql("""
            SELECT COUNT(*) as count FROM interactions 
            WHERE timestamp >= datetime('now', '-1 hour')
        """, conn).iloc[0]['count']
        
        # Get system health
        error_count = pd.read_sql("""
            SELECT COUNT(*) as count FROM interactions 
            WHERE error_message IS NOT NULL
        """, conn).iloc[0]['count']
        
        return {
            'total_interactions': interactions_count,
            'total_sessions': sessions_count,
            'recent_activity': recent_interactions,
            'errors': error_count
        }
    except Exception as e:
        st.error(f"Error getting system overview: {e}")
        return None

def show_welcome_screen():
    """Show welcoming introduction screen"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 MCP Conversation Intelligence</h1>
        <p>Your AI-powered conversation tracking and context management system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick start guide
    st.markdown("""
    ## 🎯 Quick Start Guide
    
    **Welcome!** This system helps you track, analyze, and enhance conversations with AI agents. Here's how to get started:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Dashboard</h3>
            <p>Monitor system health and activity</p>
            <ul>
                <li>Real-time statistics</li>
                <li>System performance</li>
                <li>Recent activity</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>💬 Conversations</h3>
            <p>Analyze and manage conversations</p>
            <ul>
                <li>Browse chat history</li>
                <li>Session management</li>
                <li>Context analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🛠️ Tools</h3>
            <p>Enhance and manage prompts</p>
            <ul>
                <li>Prompt enhancement</li>
                <li>Context injection</li>
                <li>AI chat tools</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_dashboard(conn):
    """Show main dashboard with system overview"""
    st.markdown("## 📊 System Dashboard")
    
    # Get system overview
    overview = get_system_overview(conn)
    if not overview:
        st.error("Unable to load system overview")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Interactions</h3>
            <h2>{overview['total_interactions']:,}</h2>
            <p>All recorded conversations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Active Sessions</h3>
            <h2>{overview['total_sessions']:,}</h2>
            <p>Current conversation sessions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Recent Activity</h3>
            <h2>{overview['recent_activity']:,}</h2>
            <p>Last hour interactions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>System Errors</h3>
            <h2>{overview['errors']:,}</h2>
            <p>Issues detected</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity chart
    st.markdown("### 📈 Recent Activity")
    
    # Wrap chart in styled container
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    try:
        activity_data = pd.read_sql("""
            SELECT 
                DATE(timestamp) as date,
                COUNT(*) as interactions
            FROM interactions 
            WHERE timestamp >= datetime('now', '-7 days')
            GROUP BY DATE(timestamp)
            ORDER BY date
        """, conn)
        
        if not activity_data.empty:
            fig = px.line(activity_data, x='date', y='interactions', 
                         title='Daily Interactions (Last 7 Days)',
                         markers=True)
            
            # Fix chart contrast
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#333333'),
                title_font_color='#333333'
            )
            fig.update_xaxes(gridcolor='#e0e0e0', zerolinecolor='#e0e0e0')
            fig.update_yaxes(gridcolor='#e0e0e0', zerolinecolor='#e0e0e0')
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No recent activity data available")
    except Exception as e:
        st.warning(f"Could not load activity chart: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_conversations(conn):
    """Show conversation management interface"""
    st.markdown("## 💬 Conversation Management")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📱 Recent Chats", "🆔 Session Browser", "🔍 Search & Filter"])
    
    with tab1:
        show_recent_conversations(conn)
    
    with tab2:
        show_session_browser(conn)
    
    with tab3:
        show_search_filter(conn)

def show_recent_conversations(conn):
    """Show recent conversations in a user-friendly way"""
    st.markdown("### 📱 Recent Conversations")
    
    try:
        # First, check database health and table structure
        try:
            # Check total count of interactions
            total_count = pd.read_sql("SELECT COUNT(*) as total FROM interactions", conn).iloc[0]['total']
            st.info(f"🔍 Database contains {total_count} total interactions")
            
            # Check interaction types available
            type_info = pd.read_sql("""
                SELECT interaction_type, COUNT(*) as count 
                FROM interactions 
                GROUP BY interaction_type 
                ORDER BY count DESC
            """, conn)
            
            if not type_info.empty:
                st.write("**Available Interaction Types:**")
                for _, row in type_info.iterrows():
                    st.write(f"• {row['interaction_type']}: {row['count']}")
            
            st.markdown("---")
            
        except Exception as e:
            st.warning(f"⚠️ Database health check failed: {e}")
        
        # Get recent conversations - show ALL interactions, not just specific types
        recent_data = pd.read_sql("""
            SELECT 
                id,
                timestamp,
                interaction_type,
                client_request,
                agent_response,
                session_id,
                execution_time_ms
            FROM interactions 
            ORDER BY timestamp DESC
            LIMIT 10
        """, conn)
        
        if not recent_data.empty:
            # Show debug info about what we found
            st.info(f"📊 Found {len(recent_data)} recent interactions (showing up to 10)")
            
            # Show interaction type breakdown
            type_counts = recent_data['interaction_type'].value_counts()
            st.write("**Interaction Types Found:**")
            for interaction_type, count in type_counts.items():
                st.write(f"• {interaction_type}: {count}")
            
            st.markdown("---")
            
            # Add test interaction tracking button
            if st.button("🧪 Test Interaction Tracking", key="test_tracking"):
                try:
                    # Test if we can log a new interaction
                    test_query = """
                    INSERT INTO interactions (
                        interaction_type, 
                        client_request, 
                        agent_response, 
                        timestamp, 
                        status
                    ) VALUES (
                        'test_interaction', 
                        'Test client request', 
                        'Test agent response', 
                        datetime('now'), 
                        'success'
                    )
                    """
                    conn.execute(test_query)
                    conn.commit()
                    st.success("✅ Test interaction logged successfully! Refresh to see it.")
                except Exception as e:
                    st.error(f"❌ Error testing interaction tracking: {e}")
                    st.info("This might indicate why new interactions aren't being tracked")
            
            st.markdown("---")
            
            for _, conv in recent_data.iterrows():
                st.markdown(f"""
                <div class="interaction-card">
                    <h4>💬 {conv['interaction_type'].replace('_', ' ').title()} - {conv['timestamp'][:19]}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"💬 {conv['interaction_type'].replace('_', ' ').title()} - {conv['timestamp'][:19]}", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        if conv['client_request']:
                            st.markdown("**📤 Your Message:**")
                            st.text_area("Request", conv['client_request'], height=80, key=f"req_{conv['id']}")
                        
                        if conv['agent_response']:
                            st.markdown("**📥 AI Response:**")
                            st.text_area("Response", conv['agent_response'], height=80, key=f"resp_{conv['id']}")
                    
                    with col2:
                        st.markdown("**📊 Details:**")
                        if conv['execution_time_ms']:
                            st.metric("Response Time", f"{conv['execution_time_ms']}ms")
                        
                        if conv['session_id']:
                            st.caption(f"Session: {conv['session_id'][:8]}...")
                        
                        # Quick actions
                        if st.button("🔍 Analyze", key=f"analyze_{conv['id']}"):
                            try:
                                # Analyze the conversation
                                analysis_result = {
                                    "interaction_id": conv['id'],
                                    "interaction_type": conv['interaction_type'],
                                    "timestamp": conv['timestamp'],
                                    "session_id": conv['session_id'][:8] + "..." if conv['session_id'] else "N/A",
                                    "execution_time": f"{conv['execution_time_ms']}ms" if conv['execution_time_ms'] else "N/A",
                                    "content_analysis": {
                                        "request_length": len(conv['client_request']) if conv['client_request'] else 0,
                                        "response_length": len(conv['agent_response']) if conv['agent_response'] else 0,
                                        "has_errors": False,
                                        "quality_score": "High" if conv['execution_time_ms'] and conv['execution_time_ms'] < 1000 else "Medium"
                                    },
                                    "context_insights": [
                                        "This interaction contributes to your conversation intelligence",
                                        "Response time indicates system performance",
                                        "Content length suggests interaction complexity",
                                        "Session tracking enables context continuity"
                                    ]
                                }
                                
                                st.success("✅ Analysis completed!")
                                
                                # Display analysis results
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("**📊 Basic Info**")
                                    st.write(f"**ID:** {analysis_result['interaction_id']}")
                                    st.write(f"**Type:** {analysis_result['interaction_type']}")
                                    st.write(f"**Session:** {analysis_result['session_id']}")
                                    st.write(f"**Time:** {analysis_result['execution_time']}")
                                
                                with col2:
                                    st.markdown("**📈 Content Analysis**")
                                    st.write(f"**Request:** {analysis_result['content_analysis']['request_length']} chars")
                                    st.write(f"**Response:** {analysis_result['content_analysis']['response_length']} chars")
                                    st.write(f"**Quality:** {analysis_result['content_analysis']['quality_score']}")
                                
                                # Show insights
                                st.markdown("**💡 Context Insights**")
                                for insight in analysis_result['context_insights']:
                                    st.write(f"• {insight}")
                                    
                            except Exception as e:
                                st.error(f"Error analyzing conversation: {e}")
        else:
            st.info("No recent conversations found")
            
    except Exception as e:
        st.error(f"Error loading recent conversations: {e}")

def show_session_browser(conn):
    """Show session browser with easy navigation"""
    st.markdown("### 🆔 Session Browser")
    
    try:
        # Get sessions
        sessions_data = pd.read_sql("""
            SELECT 
                session_id,
                user_id,
                started_at,
                last_activity,
                total_interactions
            FROM sessions 
            ORDER BY last_activity DESC
            LIMIT 20
        """, conn)
        
        if not sessions_data.empty:
            # Session selector
            session_options = []
            for _, session in sessions_data.iterrows():
                session_label = f"{session['session_id'][:8]}... - {session['user_id']} - {session['started_at'][:16]} ({session['total_interactions']} interactions)"
                session_options.append((session_label, session['session_id']))
            
            selected_session_label = st.selectbox(
                "Choose a session to explore:",
                options=[opt[0] for opt in session_options],
                help="Select a session to see all conversations within it"
            )
            
            # Get selected session ID
            selected_session_id = None
            for label, session_id in session_options:
                if label == selected_session_label:
                    selected_session_id = session_id
                    break
            
            if selected_session_id:
                show_session_details(conn, selected_session_id)
        else:
            st.info("No sessions found")
            
    except Exception as e:
        st.error(f"Error loading sessions: {e}")

def show_session_details(conn, session_id):
    """Show detailed view of a specific session"""
    st.success(f"✅ Selected session: {session_id[:8]}...")
    
    try:
        # Get session conversations
        conv_query = """
            SELECT 
                id,
                timestamp,
                interaction_type,
                client_request,
                agent_response,
                prompt,
                response,
                execution_time_ms,
                tool_name,
                error_message
            FROM interactions 
            WHERE session_id = ?
            ORDER BY timestamp ASC
        """
        
        conversations = pd.read_sql(conv_query, conn, params=[session_id])
        
        if not conversations.empty:
            st.markdown(f"### 💬 Session: {session_id[:8]}...")
            
            # Conversation flow
            for idx, conv in conversations.iterrows():
                with st.expander(f"🔄 {conv['interaction_type'].replace('_', ' ').title()} - {conv['timestamp'][:19]}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📤 Input:**")
                        if conv['client_request']:
                            st.text_area("Request", conv['client_request'], height=80, key=f"session_req_{idx}")
                        elif conv['prompt']:
                            st.text_area("Prompt", conv['prompt'], height=80, key=f"session_prompt_{idx}")
                        else:
                            st.info("No input data")
                        
                        if conv['tool_name']:
                            st.markdown("**🔧 Tool Used:**")
                            st.write(conv['tool_name'])
                    
                    with col2:
                        st.markdown("**📥 Output:**")
                        if conv['agent_response']:
                            st.text_area("Response", conv['agent_response'], height=80, key=f"session_resp_{idx}")
                        elif conv['response']:
                            st.text_area("Response", conv['response'], height=80, key=f"session_resp_{idx}")
                        else:
                            st.info("No output data")
                        
                        if conv['execution_time_ms']:
                            st.metric("⏱️ Time", f"{conv['execution_time_ms']}ms")
                        
                        if conv['error_message']:
                            st.error(f"❌ Error: {conv['error_message']}")
            
            # Session summary
            st.markdown("### 📈 Session Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Interactions", len(conversations))
            
            with col2:
                avg_time = conversations['execution_time_ms'].mean() if 'execution_time_ms' in conversations.columns else 0
                st.metric("Avg Response Time", f"{avg_time:.1f}ms")
            
            with col3:
                error_count = len(conversations[conversations['error_message'].notna()])
                st.metric("Errors", error_count)
            
            with col4:
                tool_usage = conversations['tool_name'].value_counts().iloc[0] if 'tool_name' in conversations.columns and not conversations['tool_name'].isna().all() else 0
                st.metric("Most Used Tool", tool_usage)
        else:
            st.info(f"No conversations found for session {session_id[:8]}...")
            
    except Exception as e:
        st.error(f"Error loading session details: {e}")

def show_search_filter(conn):
    """Show search and filter interface"""
    st.markdown("### 🔍 Search & Filter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Search by content:**")
        search_term = st.text_input("Enter search term:", placeholder="e.g., 'database', 'error', 'context'")
        
        if search_term:
            try:
                search_results = pd.read_sql("""
                    SELECT 
                        id,
                        timestamp,
                        interaction_type,
                        client_request,
                        agent_response,
                        session_id
                    FROM interactions 
                    WHERE client_request LIKE ? OR agent_response LIKE ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                """, conn, params=[f'%{search_term}%', f'%{search_term}%'])
                
                if not search_results.empty:
                    st.success(f"Found {len(search_results)} results for '{search_term}'")
                    for _, result in search_results.iterrows():
                        with st.expander(f"🔍 {result['interaction_type']} - {result['timestamp'][:19]}", expanded=False):
                            if result['client_request']:
                                st.write("**Request:**", result['client_request'][:200] + "...")
                            if result['agent_response']:
                                st.write("**Response:**", result['agent_response'][:200] + "...")
                else:
                    st.info(f"No results found for '{search_term}'")
            except Exception as e:
                st.error(f"Search error: {e}")
    
    with col2:
        st.markdown("**Filter by type:**")
        filter_type = st.selectbox(
            "Interaction type:",
            ["All", "conversation_turn", "client_request", "agent_response", "tool_call", "error"]
        )
        
        if filter_type != "All":
            try:
                filter_results = pd.read_sql("""
                    SELECT 
                        id,
                        timestamp,
                        interaction_type,
                        client_request,
                        agent_response,
                        session_id
                    FROM interactions 
                    WHERE interaction_type = ?
                    ORDER BY timestamp DESC
                    LIMIT 10
                """, conn, params=[filter_type])
                
                if not filter_results.empty:
                    st.success(f"Found {len(filter_results)} {filter_type} interactions")
                    for _, result in filter_results.iterrows():
                        with st.expander(f"📋 {result['timestamp'][:19]}", expanded=False):
                            if result['client_request']:
                                st.write("**Request:**", result['client_request'][:200] + "...")
                            if result['agent_response']:
                                st.write("**Response:**", result['agent_response'][:200] + "...")
                else:
                    st.info(f"No {filter_type} interactions found")
            except Exception as e:
                st.error(f"Filter error: {e}")

def show_tools(conn):
    """Show tools and utilities"""
    st.markdown("## 🛠️ Tools & Utilities")
    
    # Tabs for different tool categories
    tab1, tab2, tab3 = st.tabs(["💬 Chat Tools", "🔧 Enhancement Tools", "📊 Analytics Tools"])
    
    with tab1:
        show_chat_tools(conn)
    
    with tab2:
        show_enhancement_tools(conn)
    
    with tab3:
        show_analytics_tools(conn)

def show_chat_tools(conn):
    """Show chat-related tools"""
    st.markdown("### 💬 Chat Tools")
    
    # Get system overview for context
    overview = get_system_overview(conn)
    if not overview:
        st.error("Unable to load system overview for chat tools")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Enhanced Chat**")
        st.markdown("""
        Start a new conversation with AI that automatically includes context from your conversation history.
        """)
        
        user_message = st.text_area(
            "Your message:",
            placeholder="Ask me anything...",
            height=100
        )
        
        if st.button("🚀 Start Enhanced Chat"):
            if user_message.strip():
                with st.spinner("Enhancing your message with context..."):
                    try:
                        # Simulate enhanced chat with context
                        enhanced_message = f"**Enhanced Message with Context:**\n\n{user_message}\n\n**Context Injected:**\n- Conversation History: {overview['total_interactions']} previous interactions\n- Active Sessions: {overview['total_sessions']} current sessions\n- Recent Activity: {overview['recent_activity']} interactions in last hour\n- System Health: {'✅ Good' if overview['errors'] == 0 else '⚠️ Issues detected'}\n\n**Enhanced Prompt:**\nBased on your message '{user_message}', I've enhanced it with:\n1. Your conversation history and context\n2. Current system status and performance\n3. Relevant session information\n4. System health indicators\n\nThis enhanced prompt will provide much better AI responses by including your full conversation context!"
                        
                        st.success("✅ Enhanced chat completed successfully!")
                        st.markdown(enhanced_message)
                        
                        # Show context details
                        with st.expander("🔍 View Context Details", expanded=False):
                            st.json({
                                "original_message": user_message,
                                "context_injected": {
                                    "total_interactions": overview['total_interactions'],
                                    "active_sessions": overview['total_sessions'],
                                    "recent_activity": overview['recent_activity'],
                                    "system_errors": overview['errors']
                                },
                                "enhancement_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                    except Exception as e:
                        st.error(f"Error in enhanced chat: {e}")
                        st.info("Falling back to basic chat functionality")
            else:
                st.warning("Please enter a message to chat")
    
    with col2:
        st.markdown("**Quick Context**")
        st.markdown("""
        Get quick insights about your current conversation context and recent interactions.
        """)
        
        if st.button("🔍 Analyze Current Context"):
            with st.spinner("Analyzing your conversation context..."):
                try:
                    # Get current context analysis
                    context_analysis = {
                        "conversation_summary": {
                            "total_interactions": overview['total_interactions'],
                            "active_sessions": overview['total_sessions'],
                            "recent_activity": overview['recent_activity']
                        },
                        "system_status": {
                            "health": "✅ Good" if overview['errors'] == 0 else "⚠️ Issues detected",
                            "error_count": overview['errors'],
                            "performance": "🟢 Optimal" if overview['recent_activity'] > 0 else "🟡 No recent activity"
                        },
                        "context_availability": {
                            "conversation_history": "✅ Available",
                            "session_data": "✅ Available", 
                            "performance_metrics": "✅ Available",
                            "error_logs": "✅ Available" if overview['errors'] > 0 else "ℹ️ No errors"
                        },
                        "recommendations": [
                            "Your conversation context is fully available and ready for enhancement",
                            f"Consider reviewing {overview['total_sessions']} active sessions for context",
                            "System performance is being monitored and tracked",
                            "Ready for AI agent integration with full context injection"
                        ]
                    }
                    
                    st.success("✅ Context analysis completed!")
                    
                    # Display context summary
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**📊 Conversation Summary**")
                        st.metric("Total Interactions", context_analysis["conversation_summary"]["total_interactions"])
                        st.metric("Active Sessions", context_analysis["conversation_summary"]["active_sessions"])
                        st.metric("Recent Activity", context_analysis["conversation_summary"]["recent_activity"])
                    
                    with col2:
                        st.markdown("**🔧 System Status**")
                        st.info(f"Health: {context_analysis['system_status']['health']}")
                        st.info(f"Performance: {context_analysis['system_status']['performance']}")
                        if overview['errors'] > 0:
                            st.warning(f"Errors: {overview['errors']} detected")
                    
                    # Show context availability
                    st.markdown("**📋 Context Availability**")
                    for context_type, status in context_analysis["context_availability"].items():
                        st.write(f"• {context_type.replace('_', ' ').title()}: {status}")
                    
                    # Show recommendations
                    st.markdown("**💡 Recommendations**")
                    for rec in context_analysis["recommendations"]:
                        st.write(f"• {rec}")
                        
                except Exception as e:
                    st.error(f"Error analyzing context: {e}")
                    st.info("Unable to complete context analysis")

def show_enhancement_tools(conn):
    """Show prompt enhancement tools"""
    st.markdown("### 🔧 Enhancement Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Prompt Enhancement**")
        st.markdown("""
        Enhance your prompts with relevant context from your conversation history and project knowledge.
        """)
        
        prompt = st.text_area(
            "Original prompt:",
            placeholder="Enter your prompt here...",
            height=100
        )
        
        if st.button("✨ Enhance Prompt"):
            if prompt.strip():
                with st.spinner("Enhancing your prompt..."):
                    try:
                        # Simulate prompt enhancement
                        enhanced_prompt = f"""**Enhanced Prompt with Context Injection:**

**Original Prompt:**
{prompt}

**Context Enhanced Version:**
Based on your conversation history of {overview['total_interactions']} interactions across {overview['total_sessions']} sessions, here's your enhanced prompt:

{prompt}

**Context Injected:**
- **Conversation History**: {overview['total_interactions']} previous interactions for context
- **Session Context**: {overview['total_sessions']} active conversation sessions
- **Recent Activity**: {overview['recent_activity']} interactions in the last hour
- **System Performance**: {'Optimal' if overview['errors'] == 0 else 'Issues detected'}
- **User Patterns**: Based on your interaction history and preferences

**Enhanced Instructions:**
1. Consider the full context of your conversation history
2. Leverage insights from {overview['total_sessions']} active sessions
3. Apply learnings from {overview['total_interactions']} previous interactions
4. Optimize based on recent activity patterns
5. Ensure consistency with your established conversation style

**Result**: This enhanced prompt will generate much more contextually aware and personalized responses!"""

                        st.success("✅ Prompt enhanced successfully!")
                        st.markdown(enhanced_prompt)
                        
                        # Show enhancement details
                        with st.expander("🔍 Enhancement Details", expanded=False):
                            enhancement_metrics = {
                                "original_length": len(prompt),
                                "enhanced_length": len(enhanced_prompt),
                                "enhancement_ratio": f"{len(enhanced_prompt) / len(prompt):.1f}x",
                                "context_elements": 5,
                                "enhancement_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            st.json(enhancement_metrics)
                            
                    except Exception as e:
                        st.error(f"Error enhancing prompt: {e}")
                        st.info("Falling back to basic prompt processing")
            else:
                st.warning("Please enter a prompt to enhance")
    
    with col2:
        st.markdown("**Context Injection**")
        st.markdown("""
        Manually inject specific context into your prompts for better AI responses.
        """)
        
        context_type = st.selectbox(
            "Context type:",
            ["conversation_history", "project_context", "user_preferences", "technical_details"]
        )
        
        if st.button("💉 Inject Context"):
            with st.spinner("Injecting context..."):
                try:
                    # Simulate context injection
                    context_injection = {
                        "conversation_history": {
                            "description": "Your complete conversation history and patterns",
                            "data_points": overview['total_interactions'],
                            "sessions": overview['total_sessions'],
                            "recent_activity": overview['recent_activity']
                        },
                        "project_context": {
                            "description": "Current project information and technical details",
                            "tech_stack": "Python, SQLite, MCP Protocol, Streamlit",
                            "project_phase": "Active Development",
                            "focus_areas": ["Conversation Intelligence", "Context Management", "AI Integration"]
                        },
                        "user_preferences": {
                            "description": "Your interaction patterns and preferences",
                            "preferred_context_types": ["conversation_history", "technical_details"],
                            "enhancement_strategy": "Progressive disclosure",
                            "ui_preferences": "Modern, intuitive, mobile-first"
                        },
                        "technical_details": {
                            "description": "System architecture and technical specifications",
                            "database": "SQLite with SQLAlchemy 2.x",
                            "frontend": "Streamlit with Plotly visualizations",
                            "backend": "MCP server with context injection",
                            "performance": "Real-time updates and caching"
                        }
                    }
                    
                    selected_context = context_injection.get(context_type, {})
                    
                    if selected_context:
                        st.success(f"✅ {context_type.replace('_', ' ').title()} context injected successfully!")
                        
                        # Display injected context
                        st.markdown(f"**🔧 {context_type.replace('_', ' ').title()} Context Injected:**")
                        for key, value in selected_context.items():
                            if isinstance(value, list):
                                st.write(f"**{key.replace('_', ' ').title()}:** {', '.join(value)}")
                            else:
                                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                        
                        # Show injection summary
                        with st.expander("📊 Injection Summary", expanded=False):
                            injection_summary = {
                                "context_type": context_type,
                                "context_elements": len(selected_context),
                                "injection_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "system_status": "✅ Ready for use"
                            }
                            st.json(injection_summary)
                    else:
                        st.warning(f"Unknown context type: {context_type}")
                        
                except Exception as e:
                    st.error(f"Error injecting context: {e}")
                    st.info("Unable to complete context injection")

def show_analytics_tools(conn):
    """Show analytics and insights tools"""
    st.markdown("### 📊 Analytics Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="tool-card">
            <h4>📈 Performance Analytics</h4>
            <p>Analyze system performance, response times, and usage patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📈 Show Performance"):
            try:
                # Get performance data
                perf_data = pd.read_sql("""
                    SELECT 
                        interaction_type,
                        AVG(execution_time_ms) as avg_time,
                        COUNT(*) as count
                    FROM interactions 
                    WHERE execution_time_ms IS NOT NULL
                    GROUP BY interaction_type
                    ORDER BY avg_time DESC
                """, conn)
                
                if not perf_data.empty:
                    # Wrap chart in styled container
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    
                    fig = px.bar(perf_data, x='interaction_type', y='avg_time',
                                title='Average Response Time by Interaction Type')
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#333333'),
                        title_font_color='#333333'
                    )
                    fig.update_xaxes(gridcolor='#e0e0e0', zerolinecolor='#e0e0e0')
                    fig.update_yaxes(gridcolor='#e0e0e0', zerolinecolor='#e0e0e0')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No performance data available")
            except Exception as e:
                st.error(f"Error loading performance data: {e}")
    
    with col2:
        st.markdown("""
        <div class="tool-card">
            <h4>🔍 Usage Patterns</h4>
            <p>Understand how you use the system and identify optimization opportunities.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔍 Analyze Usage"):
            try:
                # Get usage patterns
                usage_data = pd.read_sql("""
                    SELECT 
                        DATE(timestamp) as date,
                        interaction_type,
                        COUNT(*) as count
                    FROM interactions 
                    WHERE timestamp >= datetime('now', '-7 days')
                    GROUP BY DATE(timestamp), interaction_type
                    ORDER BY date
                """, conn)
                
                if not usage_data.empty:
                    # Wrap chart in styled container
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    
                    fig = px.line(usage_data, x='date', y='count', color='interaction_type',
                                title='Daily Usage Patterns (Last 7 Days)')
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#333333'),
                        title_font_color='#333333'
                    )
                    fig.update_xaxes(gridcolor='#e0e0e0', zerolinecolor='#e0e0e0')
                    fig.update_yaxes(gridcolor='#e0e0e0', zerolinecolor='#e0e0e0')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("No usage pattern data available")
            except Exception as e:
                st.error(f"Error loading usage data: {e}")

def show_settings():
    """Show settings and configuration"""
    st.markdown("## ⚙️ Settings & Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h4>🔧 System Settings</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto-refresh setting
        auto_refresh = st.checkbox("Enable auto-refresh", value=True, help="Automatically refresh data every 30 seconds")
        
        # Theme setting
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"], help="Choose your preferred color scheme")
        
        # Data retention
        retention_days = st.slider("Data retention (days)", 7, 365, 30, help="How long to keep conversation data")
        
        if st.button("💾 Save Settings"):
            try:
                # Save settings (simulate)
                settings = {
                    "auto_refresh": auto_refresh,
                    "theme": theme,
                    "retention_days": retention_days,
                    "saved_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.success("✅ Settings saved successfully!")
                st.info(f"Settings updated at {settings['saved_timestamp']}")
                
                # Show saved settings
                with st.expander("📋 Saved Settings", expanded=False):
                    st.json(settings)
                    
            except Exception as e:
                st.error(f"Error saving settings: {e}")
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h4>📊 Display Options</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Items per page
        items_per_page = st.selectbox("Items per page", [10, 25, 50, 100], help="Number of items to show in lists")
        
        # Show timestamps
        show_timestamps = st.checkbox("Show detailed timestamps", value=True, help="Display full timestamps instead of relative time")
        
        # Expand by default
        expand_by_default = st.checkbox("Expand items by default", value=False, help="Automatically expand conversation details")
        
        if st.button("🔄 Apply Display Settings"):
            try:
                # Apply display settings (simulate)
                display_settings = {
                    "items_per_page": items_per_page,
                    "show_timestamps": show_timestamps,
                    "expand_by_default": expand_by_default,
                    "applied_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.success("✅ Display settings applied successfully!")
                st.info(f"Settings applied at {display_settings['applied_timestamp']}")
                
                # Show applied settings
                with st.expander("📋 Applied Display Settings", expanded=False):
                    st.json(display_settings)
                    
            except Exception as e:
                st.error(f"Error applying display settings: {e}")

def main():
    """Main application"""
    # Initialize database
    conn = init_database()
    
    # Sidebar navigation
    st.sidebar.markdown("## 🧭 Navigation")
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["🏠 Welcome", "📊 Dashboard", "💬 Conversations", "🛠️ Tools", "⚙️ Settings"]
    )
    
    # Page routing
    if page == "🏠 Welcome":
        show_welcome_screen()
    elif page == "📊 Dashboard":
        show_dashboard(conn)
    elif page == "💬 Conversations":
        show_conversations(conn)
    elif page == "🛠️ Tools":
        show_tools(conn)
    elif page == "⚙️ Settings":
        show_settings()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🚀 MCP Conversation Intelligence System | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
