#!/bin/bash

# MCP Agent Tracker Startup Script

echo "🚀 Starting MCP Agent Tracker..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if database exists, if not initialize it
if [ ! -f "${DB_PATH:-./data/agent_tracker.db}" ]; then
    echo "📊 Initializing database..."
    python3 init_db.py
    if [ $? -ne 0 ]; then
        echo "❌ Failed to initialize database"
        exit 1
    fi
    echo "✅ Database initialized successfully"
fi

# Run tests if in development mode
if [ "${ENVIRONMENT:-production}" = "development" ]; then
    echo "🧪 Running tests in development mode..."
    python3 test_tracking.py
    if [ $? -ne 0 ]; then
        echo "⚠ Tests failed, but continuing..."
    fi
fi

echo "🔧 Starting MCP server with tracking enabled..."
echo "📝 All interactions will be automatically logged to the database"
echo "💾 Database location: ${DB_PATH:-./data/agent_tracker.db}"
echo "🌍 Environment: ${ENVIRONMENT:-production}"
echo "👤 User ID: ${USER_ID:-anonymous}"
echo ""

# Start the MCP server
exec python3 main.py
