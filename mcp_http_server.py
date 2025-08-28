#!/usr/bin/env python3
"""
HTTP-based MCP server for conversation tracking tools
This allows external tools to connect to the Docker container
"""

import json
import asyncio
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# Import the conversation tools
from main import (
    get_conversation_summary,
    get_interaction_history, 
    get_system_status,
    agent_interaction,
    test_conversation_tracking,
    get_current_weather,
    inject_conversation_context,
    get_conversation_context,
    extract_conversation_data,
    get_conversation_analytics
)

app = FastAPI(title="MCP Conversation Tracker", version="1.0.0")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "mcp-conversation-tracker"}

@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    return {
        "tools": [
            "get_conversation_summary",
            "get_interaction_history", 
            "get_system_status",
            "agent_interaction",
            "test_conversation_tracking",
            "get_current_weather",
            "inject_conversation_context",
            "get_conversation_context",
            "extract_conversation_data",
            "get_conversation_analytics"
        ]
    }

@app.post("/tool/get_conversation_summary")
async def tool_get_conversation_summary(request: dict):
    """Get conversation summary"""
    try:
        session_id = request.get('session_id')
        result = get_conversation_summary(session_id)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/get_interaction_history")
async def tool_get_interaction_history(request: dict):
    """Get interaction history"""
    try:
        limit = request.get('limit', 10)
        session_id = request.get('session_id')
        result = get_interaction_history(limit, session_id)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/get_system_status")
async def tool_get_system_status():
    """Get system status"""
    try:
        result = get_system_status()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/agent_interaction")
async def tool_agent_interaction(request: dict):
    """Agent interaction"""
    try:
        prompt = request.get('prompt', '')
        result = agent_interaction(prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/test_conversation_tracking")
async def tool_test_conversation_tracking(request: dict):
    """Test conversation tracking"""
    try:
        message = request.get('message', 'Hello, world!')
        result = test_conversation_tracking(message)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/get_current_weather")
async def tool_get_current_weather(request: dict):
    """Get current weather for a city"""
    try:
        city = request.get('city', '')
        result = get_current_weather(city)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/inject_conversation_context")
async def tool_inject_conversation_context(request: dict):
    """Inject conversation context into a prompt"""
    try:
        prompt = request.get('prompt', '')
        session_id = request.get('session_id')
        result = inject_conversation_context(prompt, session_id)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/get_conversation_context")
async def tool_get_conversation_context(request: dict):
    """Get detailed conversation context"""
    try:
        session_id = request.get('session_id')
        result = get_conversation_context(session_id)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/extract_conversation_data")
async def tool_extract_conversation_data(request: dict):
    """Extract and format conversation data from the database"""
    try:
        limit = request.get('limit', 20)
        interaction_type = request.get('interaction_type')
        session_id = request.get('session_id')
        export_format = request.get('export_format', 'json')
        result = extract_conversation_data(limit, interaction_type, session_id, export_format)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tool/get_conversation_analytics")
async def tool_get_conversation_analytics():
    """Get comprehensive analytics about conversation data"""
    try:
        result = get_conversation_analytics()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting HTTP-based MCP server...")
    print("📊 Conversation tracking tools available at:")
    print("   - GET  /health")
    print("   - GET  /tools") 
    print("   - POST /tool/get_conversation_summary")
    print("   - POST /tool/get_interaction_history")
    print("   - POST /tool/get_system_status")
    print("   - POST /tool/agent_interaction")
    print("   - POST /tool/test_conversation_tracking")
    print("   - POST /tool/get_current_weather")
    print("   - POST /tool/extract_conversation_data")
    print("   - POST /tool/get_conversation_analytics")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
