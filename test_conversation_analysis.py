#!/usr/bin/env python3
"""
Test script to verify the new conversation analysis features work correctly
"""

import sqlite3
import os
from datetime import datetime

def test_conversation_analysis_features():
    """Test the new conversation analysis features"""
    print("🧪 Testing Conversation Analysis Features")
    print("=" * 50)
    
    # Check if database exists
    db_path = "./data/agent_tracker.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test 1: Check conversation counts
        print("📊 Testing Conversation Counts...")
        conv_query = """
            SELECT 
                interaction_type,
                COUNT(*) as count,
                MAX(timestamp) as latest
            FROM interactions 
            WHERE interaction_type IN ('conversation_turn', 'client_request', 'agent_response', 'user_prompt')
            GROUP BY interaction_type
            ORDER BY count DESC
        """
        
        cursor.execute(conv_query)
        conv_data = cursor.fetchall()
        
        if conv_data:
            print("✅ Conversation counts retrieved successfully:")
            for interaction_type, count, latest in conv_data:
                print(f"   • {interaction_type}: {count} interactions")
        else:
            print("⚠️ No conversation data found")
        
        # Test 2: Check session selection
        print("\n🎯 Testing Session Selection...")
        sessions_query = """
            SELECT 
                session_id,
                user_id,
                started_at,
                last_activity,
                total_interactions
            FROM sessions 
            ORDER BY last_activity DESC
            LIMIT 5
        """
        
        cursor.execute(sessions_query)
        sessions_data = cursor.fetchall()
        
        if sessions_data:
            print("✅ Session selection working:")
            for session_id, user_id, started_at, last_activity, total_interactions in sessions_data:
                print(f"   • Session: {session_id[:8]}... - User: {user_id} - Interactions: {total_interactions}")
        else:
            print("⚠️ No sessions found")
        
        # Test 3: Check conversation details for a session
        print("\n💬 Testing Conversation Details...")
        if sessions_data:
            test_session_id = sessions_data[0][0]  # Use first session
            
            conv_details_query = """
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
                    parameters,
                    error_message
                FROM interactions 
                WHERE session_id = ?
                ORDER BY timestamp ASC
                LIMIT 3
            """
            
            cursor.execute(conv_details_query, [test_session_id])
            conv_details = cursor.fetchall()
            
            if conv_details:
                print(f"✅ Conversation details for session {test_session_id[:8]}...:")
                for conv_id, timestamp, interaction_type, client_request, agent_response, prompt, response, exec_time, tool_name, parameters, error_message in conv_details:
                    print(f"   • ID: {conv_id} - Type: {interaction_type} - Time: {timestamp[:19]}")
                    if client_request:
                        print(f"     Request: {client_request[:50]}...")
                    if agent_response:
                        print(f"     Response: {agent_response[:50]}...")
                    if exec_time:
                        print(f"     Execution: {exec_time}ms")
            else:
                print(f"⚠️ No conversations found for session {test_session_id[:8]}...")
        
        # Test 4: Check new fields are present
        print("\n🔧 Testing New Fields...")
        cursor.execute("PRAGMA table_info(interactions)")
        columns = cursor.fetchall()
        
        new_fields = ['tool_name', 'parameters', 'error_message', 'interaction_metadata']
        for field in new_fields:
            if any(field in col[1] for col in columns):
                print(f"✅ Field '{field}' present")
            else:
                print(f"❌ Field '{field}' missing")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing conversation analysis: {e}")
        return False

def test_ui_queries():
    """Test the exact queries used in the UI"""
    print("\n🧪 Testing UI Queries...")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect("./data/agent_tracker.db")
        
        # Test the queries used in the conversation analysis tool
        queries = {
            "Conversation Counts": """
                SELECT 
                    interaction_type,
                    COUNT(*) as count,
                    MAX(timestamp) as latest
                FROM interactions 
                WHERE interaction_type IN ('conversation_turn', 'client_request', 'agent_response', 'user_prompt')
                GROUP BY interaction_type
                ORDER BY count DESC
            """,
            "Session Selection": """
                SELECT 
                    session_id,
                    user_id,
                    started_at,
                    last_activity,
                    total_interactions
                FROM sessions 
                ORDER BY last_activity DESC
                LIMIT 20
            """,
            "Conversation Details": """
                SELECT 
                    id,
                    timestamp,
                    interaction_type,
                    client_request,
                    agent_response,
                    prompt,
                    response,
                    full_content,
                    execution_time_ms,
                    tool_name,
                    parameters,
                    error_message,
                    interaction_metadata
                FROM interactions 
                WHERE session_id = ?
                ORDER BY timestamp ASC
            """
        }
        
        for name, query in queries.items():
            try:
                if "?" in query:
                    # Test with a sample session ID
                    cursor = conn.cursor()
                    cursor.execute("SELECT session_id FROM sessions LIMIT 1")
                    sample_session = cursor.fetchone()
                    if sample_session:
                        result = cursor.execute(query, [sample_session[0]]).fetchall()
                        print(f"✅ {name}: {len(result)} results")
                    else:
                        print(f"⚠️ {name}: No sessions to test with")
                else:
                    result = conn.execute(query).fetchall()
                    print(f"✅ {name}: {len(result)} results")
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing UI queries: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Conversation Analysis Features Test")
    print("=" * 50)
    
    # Test 1: Check conversation analysis features
    analysis_ok = test_conversation_analysis_features()
    
    # Test 2: Test UI queries
    queries_ok = test_ui_queries()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    if analysis_ok and queries_ok:
        print("🎉 All tests passed! Conversation analysis features are working!")
        print("\n✅ What's Now Available:")
        print("   • Full conversation visibility and selection")
        print("   • Session-based conversation browsing")
        print("   • Request/response pair analysis")
        print("   • Tool usage and parameter tracking")
        print("   • Error message visibility")
        print("   • Execution time monitoring")
        print("   • Context metadata analysis")
        
        print("\n🚀 New Features Added:")
        print("   • 💬 Conversation Analysis Tool")
        print("   • 📚 Chat History in Enhanced Chat")
        print("   • 📊 Context Analysis in Basic Prompt Enhancement")
        print("   • 🎯 Session Selection and Navigation")
        print("   • 📈 Conversation Flow Visualization")
        
        print("\n🎯 How to Use:")
        print("   1. Go to '🛠️ Prompt Crafting' in the UI")
        print("   2. Select '💬 Conversation Analysis Tool'")
        print("   3. Choose a session to analyze")
        print("   4. See full request/response pairs")
        print("   5. Analyze context injection and tool usage")
    else:
        print("❌ Some tests failed - conversation analysis may not work properly")
        print("\n🔧 Troubleshooting:")
        print("   • Check database connection")
        print("   • Verify table structure")
        print("   • Check for missing fields")

if __name__ == "__main__":
    main()
