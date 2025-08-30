#!/bin/bash

# 🚀 Launch Script for NEW User-Friendly Frontend
# MCP Conversation Intelligence System

echo "🚀 Launching NEW User-Friendly Frontend..."
echo "=========================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements_ui.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, pandas, plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies!"
    echo "Installing required packages..."
    pip install -r requirements_ui.txt
fi

# Launch the new frontend
echo "🚀 Starting NEW User-Friendly Frontend..."
echo "📍 URL: http://localhost:8501"
echo "🔄 Press Ctrl+C to stop"
echo ""

streamlit run context_ui_new.py --server.port 8501 --server.address localhost
