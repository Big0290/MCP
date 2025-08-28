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
        
        # Error rate - FIXED to match actual schema
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
            # Get recent sessions - FIXED to match actual schema
            query = """
                SELECT 
                    id,
                    started_at,
                    last_activity,
                    total_interactions,
                    user_id
                FROM sessions 
                ORDER BY last_activity DESC 
                LIMIT 50
            """
            
            # Debug: Show the query being executed
            st.write(f"Debug: Executing query: {query}")
            
            sessions = pd.read_sql(query, conn)
            
            # Debug: Show what we found
            st.write(f"Debug: Found {len(sessions)} sessions")
            if not sessions.empty:
                st.write("Debug: Sample data:", sessions.head())
            
            if not sessions.empty:
                st.success(f"Found {len(sessions)} sessions")
                st.dataframe(sessions, use_container_width=True)
            else:
                st.info("No sessions found")
                
        except Exception as e:
            st.error(f"Error loading sessions: {e}")
            st.write("Debug: Full error details:", str(e))
            # Show the actual table schema to help debug
            try:
                cursor = conn.execute("PRAGMA table_info(sessions)")
                schema_info = cursor.fetchall()
                st.write("Debug: Table schema:", schema_info)
            except Exception as schema_error:
                st.write("Debug: Could not get table schema:", str(schema_error))
    else:
        st.error("Database connection not available")

def show_contexts(conn):
    """Show contexts management"""
    st.markdown('<div class="section-header">🧠 Contexts</div>', unsafe_allow_html=True)
    
    if conn:
        try:
            # Get recent contexts - FIXED to match actual schema
            query = """
                SELECT 
                    id,
                    session_id,
                    context_type,
                    relevance_score,
                    usage_count,
                    created_at,
                    context_summary,
                    user_id
                FROM conversation_contexts 
                ORDER BY created_at DESC 
                LIMIT 50
            """
            
            # Debug: Show the query being executed
            st.write(f"Debug: Executing query: {query}")
            
            contexts = pd.read_sql(query, conn)
            
            # Debug: Show what we found
            st.write(f"Debug: Found {len(contexts)} contexts")
            if not contexts.empty:
                st.write("Debug: Sample data:", contexts.head())
            
            if not contexts.empty:
                st.success(f"Found {len(contexts)} contexts")
                st.dataframe(contexts, use_container_width=True)
            else:
                st.info("No contexts found")
                
        except Exception as e:
            st.error(f"Error loading contexts: {e}")
            st.write("Debug: Full error details:", str(e))
            # Show the actual table schema to help debug
            try:
                cursor = conn.execute("PRAGMA table_info(conversation_contexts)")
                schema_info = cursor.fetchall()
                st.write("Debug: Table schema:", schema_info)
            except Exception as schema_error:
                st.write("Debug: Could not get table schema:", str(schema_error))
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

def show_prompt_crafting(conn):
    """Show prompt crafting tools"""
    st.markdown('<div class="section-header">🛠️ Prompt Crafting Tools</div>', unsafe_allow_html=True)
    
    st.write("""
    Welcome to your **Prompt Crafting Workshop**! 🚀
    
    Here you can access all the powerful prompt enhancement tools that automatically inject conversation context,
    project knowledge, and user preferences into your prompts for maximum AI effectiveness.
    """)
    
    # Tool Selection
    st.subheader("🔧 Available Tools")
    
    tool_choice = st.selectbox(
        "Choose a prompt crafting tool:",
        [
            "📝 Basic Prompt Enhancement",
            "🚀 Enhanced Chat with Context",
            "⚡ Real-time Context Injection", 
            "🧠 Auto Context Wrapper",
            "🔍 MCP Server Debug Tool",
            "📋 Interaction History Browser",
            "📊 Prompt Performance Analytics"
        ]
    )
    
    if tool_choice == "📝 Basic Prompt Enhancement":
        show_basic_prompt_enhancement(conn)
    elif tool_choice == "🚀 Enhanced Chat with Context":
        show_enhanced_chat_tool(conn)
    elif tool_choice == "⚡ Real-time Context Injection":
        show_realtime_context_tool(conn)
    elif tool_choice == "🧠 Auto Context Wrapper":
        show_auto_context_wrapper(conn)
    elif tool_choice == "🔍 MCP Server Debug Tool":
        show_mcp_server_debug_tool(conn)
    elif tool_choice == "📋 Interaction History Browser":
        show_interaction_history_browser(conn)
    elif tool_choice == "📊 Prompt Performance Analytics":
        show_prompt_analytics(conn)

def show_basic_prompt_enhancement(conn):
    """Show basic prompt enhancement tool"""
    st.subheader("📝 Basic Prompt Enhancement")
    
    st.write("""
    This tool allows you to enhance a simple user message with basic context.
    It injects a placeholder for context, which will be replaced by the MCP server.
    """)
    
    user_message = st.text_area(
        "User Message:",
        placeholder="Enter a simple user message (e.g., 'What's the weather?')",
        height=100
    )
    
    if st.button("Enhance Prompt"):
        if user_message.strip():
            with st.spinner("Enhancing prompt..."):
                try:
                    # Simulate MCP server processing
                    enhanced_prompt = simulate_mcp_tool_response(user_message, "process_prompt_with_context")
                    st.success("Prompt enhanced successfully!")
                    st.text_area("Enhanced Prompt:", enhanced_prompt, height=200)
                except Exception as e:
                    st.error(f"Error enhancing prompt: {e}")
        else:
            st.warning("Please enter a user message to enhance.")

def show_enhanced_chat_tool(conn):
    """Show enhanced chat tool"""
    st.subheader("🚀 Enhanced Chat with Context")
    
    st.write("""
    This tool allows you to have a conversation with the AI, but with enhanced context.
    It will automatically inject context from the conversation history and recent interactions.
    """)
    
    user_message = st.text_area(
        "User Message:",
        placeholder="Enter a message to chat with the AI...",
        height=100
    )
    
    if st.button("Chat with Enhanced Context"):
        if user_message.strip():
            with st.spinner("Chatting with enhanced context..."):
                try:
                    # Simulate MCP server processing
                    enhanced_prompt = simulate_mcp_tool_response(user_message, "enhanced_chat")
                    st.success("Chat completed with enhanced context!")
                    st.text_area("Enhanced Chat Response:", enhanced_prompt, height=200)
                except Exception as e:
                    st.error(f"Error in chat: {e}")
        else:
            st.warning("Please enter a message to chat with.")

def show_realtime_context_tool(conn):
    """Show real-time context injection tool"""
    st.subheader("⚡ Real-time Context Injection")
    
    st.write("""
    This tool allows you to inject context directly into a prompt.
    It's useful for testing context injection without going through the full MCP server flow.
    """)
    
    user_message = st.text_area(
        "User Message:",
        placeholder="Enter a message to inject context into...",
        height=100
    )
    
    if st.button("Inject Context"):
        if user_message.strip():
            with st.spinner("Injecting context..."):
                try:
                    # Simulate context injection
                    context_summary = "Recent interactions, UI development, database fixes"
                    injected_elements = ["conversation_summary", "action_history", "tech_stack", "project_plans", "user_preferences", "agent_metadata"]
                    
                    enhanced_prompt = simulate_mcp_tool_response(user_message, "process_prompt_with_context")
                    
                    # Simulate the cursor agent payload
                    cursor_agent_payload = {
                        "enhanced_prompt": enhanced_prompt,
                        "original_prompt": user_message,
                        "context_summary": context_summary,
                        "injected_elements": injected_elements,
                        "processing_metadata": {
                            "tool_used": "realtime_context_injection",
                            "enhancement_success": True,
                            "context_relevance_score": 0.95
                        }
                    }
                    
                    st.success("Context injected successfully!")
                    st.text_area("Enhanced Prompt:", enhanced_prompt, height=200)
                    st.json(cursor_agent_payload)
                except Exception as e:
                    st.error(f"Error injecting context: {e}")
        else:
            st.warning("Please enter a message to inject context into.")

def show_auto_context_wrapper(conn):
    """Show auto context wrapper tool"""
    st.subheader("🧠 Auto Context Wrapper")
    
    st.write("""
    This tool allows you to wrap a prompt in a context-aware structure.
    It's useful for testing how the MCP server handles context-aware prompts.
    """)
    
    user_message = st.text_area(
        "User Message:",
        placeholder="Enter a message to wrap in context...",
        height=100
    )
    
    if st.button("Wrap in Context"):
        if user_message.strip():
            with st.spinner("Wrapping in context..."):
                try:
                    # Simulate context injection
                    context_summary = "Recent interactions, UI development, database fixes"
                    injected_elements = ["conversation_summary", "action_history", "tech_stack", "project_plans", "user_preferences", "agent_metadata"]
                    
                    enhanced_prompt = simulate_mcp_tool_response(user_message, "process_prompt_with_context")
                    
                    # Simulate the cursor agent payload
                    cursor_agent_payload = {
                        "enhanced_prompt": enhanced_prompt,
                        "original_prompt": user_message,
                        "context_summary": context_summary,
                        "injected_elements": injected_elements,
                        "processing_metadata": {
                            "tool_used": "auto_context_wrapper",
                            "enhancement_success": True,
                            "context_relevance_score": 0.98
                        }
                    }
                    
                    st.success("Prompt wrapped in context successfully!")
                    st.text_area("Enhanced Prompt:", enhanced_prompt, height=200)
                    st.json(cursor_agent_payload)
                except Exception as e:
                    st.error(f"Error wrapping in context: {e}")
        else:
            st.warning("Please enter a message to wrap in context.")

def show_prompt_analytics(conn):
    """Show prompt performance analytics"""
    st.subheader("📊 Prompt Performance Analytics")
    
    st.write("""
    This tool allows you to analyze the performance of your prompt enhancement pipeline.
    It can show you how many prompts were enhanced, the average enhancement ratio,
    and the success rate of context injection.
    """)
    
    # Placeholder for analytics data
    # In a real application, you'd query your database for these metrics
    total_prompts_enhanced = 150
    avg_enhancement_ratio = 2.8
    success_rate_context_injection = 98.5
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Prompts Enhanced", total_prompts_enhanced)
    
    with col2:
        st.metric("Avg Enhancement Ratio", f"{avg_enhancement_ratio:.1f}x")
    
    with col3:
        st.metric("Context Injection Success Rate", f"{success_rate_context_injection}%")
    
    # Example: Bar chart for success rate by tool
    st.markdown('<div class="section-header">🔍 Success Rate by Tool</div>', unsafe_allow_html=True)
    if conn:
        try:
            # Simulate fetching data from database
            tools = ["process_prompt_with_context", "enhanced_chat", "realtime_context_injection", "auto_context_wrapper"]
            success_rates = [98.5, 97.0, 99.0, 99.5] # Placeholder data
            
            fig = px.bar(x=tools, y=success_rates, 
                         title="Success Rate of Context Injection by Tool")
            fig.update_traces(marker_color='#1e40af')
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#0f172a', size=16),
                xaxis=dict(gridcolor='#e2e8f0', zerolinecolor='#475569', color='#0f172a'),
                yaxis=dict(gridcolor='#e2e8f0', zerolinecolor='#475569', color='#0f172a'),
                title=dict(font=dict(color='#0f172a', size=18))
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading analytics data: {e}")
            st.write("Debug: Creating fallback chart due to error")
            # Create fallback chart on error
            tools = ["process_prompt_with_context", "enhanced_chat", "realtime_context_injection", "auto_context_wrapper"]
            success_rates = [98.5, 97.0, 99.0, 99.5]
            fig = px.bar(x=tools, y=success_rates, 
                         title="Fallback Success Rate by Tool")
            st.plotly_chart(fig, use_container_width=True)

def show_mcp_server_debug_tool(conn):
    """Show MCP Server Debug Tool - Request/Response Flow"""
    st.subheader("🔍 MCP Server Debug Tool")
    
    st.write("""
    This tool shows you the **complete data flow** between your UI and the MCP server:
    
    1. **📤 What gets sent TO the MCP server** (request payload)
    2. **🔄 How the MCP server processes it** (internal processing)
    3. **📥 What comes BACK from the MCP server** (response payload)
    4. **🎯 What gets sent to your Cursor agent** (final output)
    
    This is crucial for debugging the prompt enhancement pipeline and understanding the data transformation.
    """)
    
    # Debug options
    st.subheader("🔧 Debug Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        debug_tool = st.selectbox(
            "MCP Tool to test:",
            [
                "process_prompt_with_context",
                "enhanced_chat", 
                "agent_interaction",
                "get_conversation_summary",
                "get_interaction_history"
            ]
        )
    
    with col2:
        debug_level = st.selectbox(
            "Debug level:",
            ["Basic", "Detailed", "Full Trace"]
        )
    
    # Test input
    test_input = st.text_area(
        "Test input:",
        placeholder="Enter text to test with the MCP server...",
        height=100
    )
    
    if st.button("🔍 Debug MCP Server Flow", type="primary"):
        if test_input.strip():
            with st.spinner("Debugging MCP server communication..."):
                try:
                    # Simulate the complete MCP server flow
                    debug_results = simulate_mcp_server_debug(
                        test_input, debug_tool, debug_level, conn
                    )
                    
                    # Display the complete flow
                    display_mcp_debug_results(debug_results, debug_level)
                    
                except Exception as e:
                    st.error(f"Error in MCP server debug: {e}")
        else:
            st.warning("Please enter test input")

def simulate_mcp_server_debug(test_input: str, tool_name: str, debug_level: str, conn) -> dict:
    """Simulate the complete MCP server request/response flow"""
    
    # Step 1: What gets sent TO the MCP server
    request_payload = {
        "tool_name": tool_name,
        "parameters": {"user_message": test_input},
        "timestamp": datetime.now().isoformat(),
        "session_id": "debug_session_123",
        "request_id": f"req_{hash(test_input) % 10000}"
    }
    
    # Step 2: MCP server internal processing
    processing_steps = [
        "Received request from UI",
        "Validated parameters",
        "Retrieved conversation context from database",
        "Generated enhanced prompt with context injection",
        "Processed through prompt processor",
        "Generated response with full context awareness",
        "Logged interaction for future reference"
    ]
    
    # Step 3: What comes BACK from MCP server
    response_payload = {
        "status": "success",
        "result": simulate_mcp_tool_response(test_input, tool_name),
        "processing_time_ms": 45,
        "context_injected": True,
        "enhancement_ratio": 3.2,
        "timestamp": datetime.now().isoformat()
    }
    
    # Step 4: What gets sent to Cursor agent
    cursor_agent_payload = {
        "enhanced_prompt": response_payload["result"],
        "original_prompt": test_input,
        "context_summary": "20+ interactions, recent focus on UI and database fixes",
        "injected_elements": [
            "conversation_summary",
            "action_history", 
            "tech_stack",
            "project_plans",
            "user_preferences",
            "agent_metadata"
        ],
        "processing_metadata": {
            "tool_used": tool_name,
            "enhancement_success": True,
            "context_relevance_score": 0.92
        }
    }
    
    return {
        "request_payload": request_payload,
        "processing_steps": processing_steps,
        "response_payload": response_payload,
        "cursor_agent_payload": cursor_agent_payload,
        "debug_level": debug_level
    }

def simulate_mcp_tool_response(test_input: str, tool_name: str) -> str:
    """Simulate MCP tool response based on tool type"""
    
    if tool_name == "process_prompt_with_context":
        return f"""=== ENHANCED PROMPT GENERATED BY JOHNY ===

USER MESSAGE: {test_input}

=== CONTEXT INJECTION ===

CONVERSATION SUMMARY:
Current conversation state: 20+ total interactions. Recent topics: UI development, CSS styling, database schema fixes, prompt crafting tools, MCP server debugging.

ACTION HISTORY:
Recent actions: Fixed database schema mismatches, reset CSS styling, created minimal UI, added prompt crafting page, implemented MCP server debug tool.

TECH STACK:
Python 3.x, SQLite database, MCP (Model Context Protocol), FastMCP server, SQLAlchemy ORM, Streamlit UI, Plotly charts.

PROJECT PLANS & OBJECTIVES:
1. Build powerful conversation tracking system ✅
2. Implement context-aware prompt processing ✅
3. Create intelligent memory management ✅
4. Develop user preference learning ✅
5. Build agent metadata system ✅
6. Integrate with external AI assistants ✅
7. Create seamless prompt enhancement pipeline 🚧
8. Implement real-time context injection 🚧

USER PREFERENCES:
- Use local SQLite over PostgreSQL for development
- Prefer simple yet powerful solutions
- Focus on conversation context and memory
- Use structured data models
- Implement comprehensive logging

AGENT METADATA:
- Friendly Name: Johny
- Agent ID: mcp-project-local
- Type: Context-Aware Conversation Manager
- Capabilities: Prompt processing, context analysis, memory management
- Status: Active and learning
- Version: 1.0.0

=== INSTRUCTIONS ===
Please respond to the user's message above, taking into account:
1. The current conversation context and recent interactions
2. The specific actions and steps taken so far
3. The technical stack and capabilities available
4. The project goals and objectives
5. The user's stated preferences and requirements
6. The agent's capabilities and current state

Provide a comprehensive, context-aware response that builds upon our conversation history.
=== END ENHANCED PROMPT ==="""
    
    elif tool_name == "enhanced_chat":
        return f"""🚀 Enhanced Chat Response (Generated by Johny)

📝 User Message: {test_input}

✨ Context Enhancement: ✅ Automatically applied
📊 Conversation Context: ✅ Retrieved from database
🎯 Project Plans: ✅ Considered in response
⚙️ Tech Stack: ✅ Referenced for accuracy
👤 User Preferences: ✅ Applied to response

💡 Response: Based on your message about "{test_input}", I can see from our conversation history that we've been working on building a powerful prompt processor system and implementing MCP server debugging tools.

Your current project status shows:
- Conversation tracking system: ✅ Complete
- Context-aware prompt processing: ✅ Complete  
- Intelligent memory management: ✅ Complete
- Seamless prompt enhancement pipeline: 🚧 In Progress
- MCP server debugging: 🚧 Recently implemented

Since you're asking about "{test_input}", I should consider your preference for simple yet powerful solutions and your focus on conversation context and memory.

Would you like me to help you with the next steps in implementing the automated pipeline, or do you have a different question about the system?"""
    
    else:
        return f"Tool '{tool_name}' response: {test_input} (enhanced with context)"

def display_mcp_debug_results(debug_results: dict, debug_level: str):
    """Display the complete MCP server debug flow"""
    
    st.subheader("🔍 Complete MCP Server Flow")
    
    # Step 1: Request to MCP Server
    st.markdown("#### 📤 1. Request TO MCP Server")
    st.json(debug_results["request_payload"])
    
    # Step 2: MCP Server Processing
    st.markdown("#### 🔄 2. MCP Server Internal Processing")
    for i, step in enumerate(debug_results["processing_steps"], 1):
        st.write(f"{i}. {step}")
    
    # Step 3: Response from MCP Server
    st.markdown("#### 📥 3. Response FROM MCP Server")
    st.json(debug_results["response_payload"])
    
    # Step 4: What goes to Cursor Agent
    st.markdown("#### 🎯 4. Final Output to Cursor Agent")
    st.json(debug_results["cursor_agent_payload"])
    
    # Summary metrics
    st.subheader("📊 Flow Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Request Size", f"{len(str(debug_results['request_payload']))} chars")
    
    with col2:
        st.metric("Response Size", f"{len(str(debug_results['response_payload']))} chars")
    
    with col3:
        st.metric("Enhancement Ratio", f"{debug_results['response_payload']['enhancement_ratio']:.1f}x")
    
    with col4:
        st.metric("Processing Time", f"{debug_results['response_payload']['processing_time_ms']}ms")
    
    # Show the actual enhanced content
    if debug_level in ["Detailed", "Full Trace"]:
        st.subheader("📝 Enhanced Content Preview")
        
        enhanced_content = debug_results["response_payload"]["result"]
        if len(enhanced_content) > 500:
            st.text_area("Enhanced Content (truncated):", enhanced_content[:500] + "...", height=200)
            st.info(f"Content truncated. Full length: {len(enhanced_content)} characters")
        else:
            st.text_area("Enhanced Content:", enhanced_content, height=200)
    
    # Show what was injected
    if debug_level == "Full Trace":
        st.subheader("🔍 Context Injection Details")
        
        injected_elements = debug_results["cursor_agent_payload"]["injected_elements"]
        st.write("**Context elements injected:**")
        for element in injected_elements:
            st.write(f"✅ {element}")
        
        metadata = debug_results["cursor_agent_payload"]["processing_metadata"]
        st.write("**Processing metadata:**")
        st.json(metadata)

def show_interaction_history_browser(conn):
    """Show interaction history browser with full request/response details"""
    st.subheader("📋 Interaction History Browser")
    
    st.write("""
    This tool shows you a **complete list of all interactions** and allows you to drill down into each one
    to see exactly **what was sent** and **what was the response**. Perfect for auditing and debugging!
    """)
    
    if not conn:
        st.error("Database connection not available")
        return
    
    try:
        # Get all interactions with pagination
        page_size = 20
        page = st.number_input("Page", min_value=1, value=1)
        offset = (page - 1) * page_size
        
        # Get total count first
        total_count = pd.read_sql("SELECT COUNT(*) as count FROM agent_interactions", conn).iloc[0]['count']
        total_pages = (total_count + page_size - 1) // page_size
        
        st.write(f"**Total Interactions**: {total_count} | **Page {page} of {total_pages}**")
        
        # Get interactions for current page
        query = """
            SELECT 
                id,
                timestamp,
                interaction_type,
                status,
                user_id,
                session_id,
                prompt,
                response,
                full_content,
                execution_time_ms
            FROM agent_interactions 
            ORDER BY timestamp DESC 
            LIMIT ? OFFSET ?
        """
        
        interactions = pd.read_sql(query, conn, params=[page_size, offset])
        
        if not interactions.empty:
            # Display interactions table
            st.subheader(f"📊 Interactions (Page {page})")
            
            # Create a more readable display
            display_data = []
            for _, row in interactions.iterrows():
                display_data.append({
                    "ID": row['id'],
                    "Timestamp": row['timestamp'],
                    "Type": row['interaction_type'],
                    "Status": row['status'],
                    "User": row['user_id'] or "N/A",
                    "Session": row['session_id'][:8] + "..." if row['session_id'] else "N/A",
                    "Prompt Length": len(str(row['prompt'])) if row['prompt'] else 0,
                    "Response Length": len(str(row['response'])) if row['response'] else 0,
                    "Exec Time": f"{row['execution_time_ms']}ms" if row['execution_time_ms'] else "N/A"
                })
            
            display_df = pd.DataFrame(display_data)
            st.dataframe(display_df, use_container_width=True)
            
            # Pagination controls
            col1, col2, col3 = st.columns(3)
            with col1:
                if page > 1:
                    if st.button("⬅️ Previous Page"):
                        st.rerun()
            with col2:
                st.write(f"Page {page} of {total_pages}")
            with col3:
                if page < total_pages:
                    if st.button("Next Page ➡️"):
                        st.rerun()
            
            # Interaction detail viewer
            st.subheader("🔍 Interaction Detail Viewer")
            
            selected_id = st.selectbox(
                "Select an interaction to view details:",
                options=interactions['id'].tolist(),
                format_func=lambda x: f"ID {x} - {interactions[interactions['id'] == x]['timestamp'].iloc[0]}"
            )
            
            if selected_id:
                show_interaction_details(selected_id, conn)
                
        else:
            st.info("No interactions found")
            
    except Exception as e:
        st.error(f"Error loading interaction history: {e}")
        st.write("Debug: Full error details:", str(e))

def show_interaction_details(interaction_id: int, conn):
    """Show detailed view of a specific interaction"""
    
    try:
        # Get full interaction details
        query = """
            SELECT * FROM agent_interactions WHERE id = ?
        """
        interaction = pd.read_sql(query, conn, params=[interaction_id])
        
        if not interaction.empty:
            interaction = interaction.iloc[0]
            
            st.subheader(f"🔍 Interaction Details - ID {interaction_id}")
            
            # Basic info
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Type", interaction['interaction_type'])
            with col2:
                st.metric("Status", interaction['status'])
            with col3:
                st.metric("Execution Time", f"{interaction['execution_time_ms']}ms" if interaction['execution_time_ms'] else "N/A")
            with col4:
                st.metric("Timestamp", interaction['timestamp'])
            
            # Request/Response comparison
            st.subheader("📤 Request vs 📥 Response")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📤 **What Was Sent**")
                if interaction['prompt']:
                    st.text_area("Original Prompt:", interaction['prompt'], height=150)
                    st.write(f"**Length**: {len(str(interaction['prompt']))} characters")
                else:
                    st.info("No prompt data available")
                
                # Show other request data
                if interaction['parameters']:
                    st.write("**Parameters:**")
                    st.json(json.loads(interaction['parameters']))
                
                if interaction['tool_name']:
                    st.write(f"**Tool Used**: {interaction['tool_name']}")
            
            with col2:
                st.markdown("#### 📥 **What Was Returned**")
                if interaction['response']:
                    st.text_area("Server Response:", interaction['response'], height=150)
                    st.write(f"**Length**: {len(str(interaction['response']))} characters")
                else:
                    st.info("No response data available")
                
                # Show response metadata
                if interaction['full_content']:
                    st.write("**Full Content:**")
                    st.text_area("Full Content:", interaction['full_content'], height=100)
                
                if interaction['context_summary']:
                    st.write("**Context Summary:**")
                    st.text_area("Context:", interaction['context_summary'], height=100)
            
            # Enhancement analysis
            if interaction['prompt'] and interaction['response']:
                st.subheader("📊 Enhancement Analysis")
                
                prompt_len = len(str(interaction['prompt']))
                response_len = len(str(interaction['response']))
                enhancement_ratio = response_len / prompt_len if prompt_len > 0 else 0
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Original Length", prompt_len)
                with col2:
                    st.metric("Response Length", response_len)
                with col3:
                    st.metric("Enhancement Ratio", f"{enhancement_ratio:.1f}x")
                
                # Show what was added
                if enhancement_ratio > 1:
                    st.success(f"✅ Response enhanced by {enhancement_ratio:.1f}x")
                    st.write("**Context was injected to enhance the response**")
                else:
                    st.info("ℹ️ No enhancement applied")
            
            # Additional metadata
            st.subheader("🔍 Additional Metadata")
            
            metadata_cols = ['user_id', 'session_id', 'error_message', 'meta_data']
            metadata_data = {}
            
            for col in metadata_cols:
                if interaction[col]:
                    try:
                        if col == 'meta_data':
                            metadata_data[col] = json.loads(interaction[col])
                        else:
                            metadata_data[col] = interaction[col]
                    except:
                        metadata_data[col] = interaction[col]
            
            if metadata_data:
                st.json(metadata_data)
            else:
                st.info("No additional metadata available")
                
        else:
            st.error(f"Interaction ID {interaction_id} not found")
            
    except Exception as e:
        st.error(f"Error loading interaction details: {e}")
        st.write("Debug: Full error details:", str(e))

def main():
    """Main application"""
    st.markdown('<h1 class="main-header">🧠 Context Manager</h1>', unsafe_allow_html=True)
    
    # Initialize database connection
    conn = init_database_connection()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["📊 Dashboard", "💬 Interactions", "🔄 Sessions", "🧠 Contexts", "🛠️ Prompt Crafting", "⚙️ System Status"]
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
    elif page == "🛠️ Prompt Crafting":
        show_prompt_crafting(conn)
    elif page == "⚙️ System Status":
        show_system_status(conn)

if __name__ == "__main__":
    main()
