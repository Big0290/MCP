#!/bin/bash

# Run the refactored Context Management UI
# This script starts the new intuitive UI with tab-based navigation

echo "🚀 Starting Refactored Context Management UI..."
echo "=================================="
echo ""
echo "✨ New Features:"
echo "  • Tab-based navigation (no more sidebar dropdowns)"
echo "  • Button-based filters (no more selectbox dropdowns)"
echo "  • Card-based layouts for better organization"
echo "  • Modern gradient design with better contrast"
echo "  • Tool grid instead of dropdown selection"
echo "  • Session cards instead of dropdown selection"
echo ""
echo "🌐 The UI will open in your default browser"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing..."
    pip install streamlit
fi

# Check if required dependencies are available
if [ ! -f "requirements_ui.txt" ]; then
    echo "⚠️  requirements_ui.txt not found. Creating basic requirements..."
    cat > requirements_ui.txt << EOF
streamlit>=1.28.0
pandas>=1.5.0
plotly>=5.15.0
sqlite3
EOF
fi

# Install UI requirements
echo "📦 Installing UI requirements..."
pip install -r requirements_ui.txt

# Start the refactored UI
echo "🎯 Starting refactored UI server..."
streamlit run context_ui_refactored.py --server.port 8502 --server.address localhost

echo ""
echo "✅ Refactored UI server stopped"
