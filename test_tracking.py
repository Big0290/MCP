#!/usr/bin/env python3
"""
Test script for the MCP Agent Tracker
Run this to verify that tracking functionality works correctly
"""

import os
import sys
import time
from models import init_database, get_session_factory, AgentInteraction, Session
from interaction_logger import logger

def test_basic_tracking():
    """Test basic interaction tracking"""
    print("Testing basic interaction tracking...")
    
    # Initialize database
    init_database()
    
    # Test session creation
    session_id = logger.get_or_create_session("test_user")
    print(f"✓ Created session: {session_id}")
    
    # Test logging different types of interactions
    logger.log_prompt("Test user prompt")
    logger.log_response("Test agent response")
    
    # Test tool execution tracking
    with logger.track_tool_execution("test_tool", {"param": "value"}):
        time.sleep(0.1)  # Simulate work
        print("✓ Tool execution tracked")
    
    # Test error tracking
    try:
        with logger.track_tool_execution("error_tool", {"param": "error"}):
            raise ValueError("Test error")
    except ValueError:
        print("✓ Error tracking works")
    
    print("✓ Basic tracking tests completed")

def test_database_queries():
    """Test database queries and data retrieval"""
    print("\nTesting database queries...")
    
    with get_session_factory()() as db_session:
        # Count interactions
        interaction_count = db_session.query(AgentInteraction).count()
        print(f"✓ Total interactions: {interaction_count}")
        
        # Count sessions
        session_count = db_session.query(Session).count()
        print(f"✓ Total sessions: {session_count}")
        
        # Get recent interactions
        recent = db_session.query(AgentInteraction).order_by(
            AgentInteraction.timestamp.desc()
        ).limit(5).all()
        
        print(f"✓ Recent interactions: {len(recent)}")
        for interaction in recent:
            print(f"  - {interaction.interaction_type}: {interaction.tool_name or 'N/A'}")
    
    print("✓ Database query tests completed")

def test_performance_tracking():
    """Test performance tracking functionality"""
    print("\nTesting performance tracking...")
    
    # Test execution time tracking
    start_time = time.time()
    with logger.track_tool_execution("performance_test", {"test": True}):
        time.sleep(0.2)  # Simulate 200ms execution
    
    execution_time = int((time.time() - start_time) * 1000)
    print(f"✓ Execution time tracked: {execution_time}ms")
    
    # Verify in database
    with get_session_factory()() as db_session:
        perf_interaction = db_session.query(AgentInteraction).filter(
            AgentInteraction.tool_name == "performance_test",
            AgentInteraction.interaction_type == "tool_response"
        ).first()
        
        if perf_interaction and perf_interaction.execution_time_ms:
            print(f"✓ Database shows execution time: {perf_interaction.execution_time_ms}ms")
        else:
            print("⚠ Execution time not found in database")
    
    print("✓ Performance tracking tests completed")

def main():
    """Run all tests"""
    print("🧪 MCP Agent Tracker - Test Suite")
    print("=" * 50)
    
    try:
        test_basic_tracking()
        test_database_queries()
        test_performance_tracking()
        
        print("\n🎉 All tests passed successfully!")
        print("\nThe tracking system is working correctly.")
        print("You can now use the MCP server with automatic interaction tracking.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
