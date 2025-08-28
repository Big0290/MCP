#!/bin/bash

# Context Manager UI Launcher
echo "🧠 Starting Context Manager UI..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "ui_env" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python3 -m venv ui_env
    echo "✅ Virtual environment created"
fi

# Activate virtual environment and install dependencies
echo "📦 Activating virtual environment and checking dependencies..."
source ui_env/bin/activate

# Check if required packages are installed
python3 -c "import streamlit, pandas, plotly, mcp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing. Installing..."
    pip install -r requirements_ui.txt
fi

# Check if database exists
if [ ! -f "./data/agent_tracker_local.db" ]; then
    echo "⚠️  Database not found. Please ensure the context system is running first."
    echo "   Run: python3 init_db.py"
fi

# Launch the UI
echo "🚀 Launching Context Manager UI..."
echo "   The UI will open in your browser at: http://localhost:8501"
echo "   Press Ctrl+C to stop the server"
echo ""

streamlit run context_ui.py --server.port 8501 --server.address 0.0.0.0
