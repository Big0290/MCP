#!/usr/bin/env python3
"""
Test script for the Enhanced Context Injection System
Demonstrates how context is generated and injected into prompts
"""

import requests
import json
import time

def test_context_injection():
    """Test the context injection system with sample interactions"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 Testing Enhanced Context Injection System")
    print("=" * 50)
    
    # Step 1: Create some sample interactions to build context
    print("\n📝 Step 1: Creating sample interactions to build context...")
    
    sample_interactions = [
        {
            "type": "client_request",
            "prompt": "I'm working on a Python FastAPI backend with PostgreSQL database. Can you help me implement user authentication?",
            "response": "I'll help you implement JWT-based user authentication for your FastAPI backend with PostgreSQL."
        },
        {
            "type": "conversation_turn",
            "prompt": "What's the best way to structure the user model and authentication endpoints?",
            "response": "For a FastAPI backend, I recommend using SQLAlchemy with Pydantic models. Here's the structure..."
        },
        {
            "type": "tool_call",
            "prompt": "I need to run database migrations for the user table. Can you help me create the migration script?",
            "response": "I'll help you create an Alembic migration script for the user table with proper constraints."
        },
        {
            "type": "client_request",
            "prompt": "I'm getting a database connection error when trying to run the migrations. The error says 'connection refused'",
            "response": "This looks like a PostgreSQL connection issue. Let's troubleshoot the database connection settings."
        },
        {
            "type": "conversation_turn",
            "prompt": "I fixed the connection issue. Now I want to add password hashing and JWT token generation. Can you show me how?",
            "response": "Great! I'll show you how to implement secure password hashing with bcrypt and JWT token generation."
        }
    ]
    
    # Simulate logging these interactions (we'll use the agent_interaction tool)
    for i, interaction in enumerate(sample_interactions, 1):
        print(f"  {i}. {interaction['type']}: {interaction['prompt'][:60]}...")
        
        # Use the agent_interaction tool to log this
        response = requests.post(f"{base_url}/tool/agent_interaction", 
                               json={"prompt": interaction['prompt']})
        if response.status_code == 200:
            print(f"     ✅ Logged successfully")
        else:
            print(f"     ❌ Failed to log: {response.status_code}")
        
        time.sleep(1)  # Small delay between interactions
    
    print("\n⏳ Waiting for context to be generated...")
    time.sleep(5)  # Give the system time to process and generate context
    
    # Step 2: Test context injection with different types of prompts
    print("\n🔍 Step 2: Testing context injection with different prompts...")
    
    test_prompts = [
        "Help me optimize this database query",
        "I need to add unit tests for the authentication system",
        "What's the best way to deploy this FastAPI app to production?",
        "Can you help me debug this JWT token validation issue?",
        "I want to add user roles and permissions to the system"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n  {i}. Testing prompt: '{prompt}'")
        print("     " + "-" * 40)
        
        # Get the enhanced prompt with context injection
        response = requests.post(f"{base_url}/tool/inject_conversation_context", 
                               json={"prompt": prompt})
        
        if response.status_code == 200:
            result = response.json().get('result', '')
            if '⚠️ No context available' in result:
                print(f"     ⚠️ No context available yet")
            else:
                print(f"     ✅ Context injected successfully!")
                print(f"     📝 Enhanced prompt length: {len(result)} characters")
                
                # Show a preview of the enhanced prompt
                if len(result) > 200:
                    print(f"     🔍 Preview: {result[:200]}...")
                else:
                    print(f"     🔍 Full enhanced prompt: {result}")
        else:
            print(f"     ❌ Failed to inject context: {response.status_code}")
    
    # Step 3: Get detailed context analysis
    print("\n📊 Step 3: Getting detailed context analysis...")
    
    response = requests.post(f"{base_url}/tool/get_conversation_context", json={})
    
    if response.status_code == 200:
        result = response.json().get('result', '')
        if 'No conversation context available' in result:
            print("  ⚠️ No context available yet - this is expected for new sessions")
        else:
            print("  ✅ Context analysis retrieved successfully!")
            print("  📋 Context details:")
            
            # Show key parts of the context
            lines = result.split('\n')
            for line in lines[:20]:  # Show first 20 lines
                if line.strip():
                    print(f"    {line}")
            
            if len(lines) > 20:
                print(f"    ... and {len(lines) - 20} more lines")
    else:
        print(f"  ❌ Failed to get context analysis: {response.status_code}")
    
    # Step 4: Test conversation summary with enhanced context
    print("\n📈 Step 4: Testing enhanced conversation summary...")
    
    response = requests.get(f"{base_url}/tool/get_conversation_summary")
    
    if response.status_code == 200:
        result = response.json().get('result', '')
        print("  ✅ Conversation summary retrieved successfully!")
        print("  📊 Summary preview:")
        
        # Show a preview of the summary
        if len(result) > 300:
            print(f"    {result[:300]}...")
        else:
            print(f"    {result}")
    else:
        print(f"  ❌ Failed to get conversation summary: {response.status_code}")
    
    print("\n🎉 Context injection system test completed!")
    print("\n💡 What this demonstrates:")
    print("  • The system automatically logs and analyzes interactions")
    print("  • Context is generated based on conversation patterns")
    print("  • Prompts can be enhanced with relevant context")
    print("  • The system learns user preferences and project context")
    print("  • Context injection improves Cursor agent responses")

if __name__ == "__main__":
    try:
        test_context_injection()
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("Make sure the MCP server is running on http://localhost:8000")
