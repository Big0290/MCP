#!/bin/bash

# Conversation Data Extractor - Easy Usage Script
# This script makes it simple to extract conversation data from the MCP server

echo "🔍 MCP Conversation Data Extractor"
echo "=================================="

# Check if Python script exists
if [ ! -f "conversation_extractor.py" ]; then
    echo "❌ Error: conversation_extractor.py not found!"
    echo "Please make sure the script is in the current directory."
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "Installing dependencies in current environment..."
    pip install -r requirements_extractor.txt
else
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
fi

# Function to show usage
show_usage() {
    echo ""
    echo "Usage Examples:"
    echo "==============="
    echo ""
    echo "📊 Get conversation summary:"
    echo "   ./extract_conversations.sh --summary"
    echo ""
    echo "💬 Extract recent conversations:"
    echo "   ./extract_conversations.sh --limit 20"
    echo ""
    echo "👤 Get user conversations:"
    echo "   ./extract_conversations.sh --user-conversations --user default_user"
    echo ""
    echo "📁 Export to JSON file:"
    echo "   ./extract_conversations.sh --export conversations.json --limit 100"
    echo ""
    echo "🔍 Filter by session:"
    echo "   ./extract_conversations.sh --session SESSION_ID --limit 50"
    echo ""
    echo "📝 Filter by interaction type:"
    echo "   ./extract_conversations.sh --type conversation_turn --limit 30"
    echo ""
    echo "📋 All available options:"
    echo "   python conversation_extractor.py --help"
}

# Check if no arguments provided
if [ $# -eq 0 ]; then
    echo ""
    echo "No arguments provided. Here are some useful commands:"
    show_usage
    exit 0
fi

# Run the Python script with all arguments
echo ""
echo "🚀 Running conversation extractor..."
echo "Command: python conversation_extractor.py $@"
echo ""

python conversation_extractor.py "$@"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Extraction completed successfully!"
else
    echo ""
    echo "❌ Extraction failed. Check the error messages above."
    echo ""
    echo "💡 Troubleshooting tips:"
    echo "   - Make sure the MCP server containers are running"
    echo "   - Check that PostgreSQL is accessible on port 5432"
    echo "   - Verify the container names match (mcp-postgres)"
    echo "   - Ensure you have the required Python packages installed"
fi
