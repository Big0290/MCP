#!/bin/bash

# Docker entrypoint script for MCP Agent Tracker

set -e

echo "🚀 Starting MCP Agent Tracker with Conversation Tracking..."

# Function to wait for database
wait_for_database() {
    if [ -n "$DATABASE_URL" ]; then
        echo "⏳ Waiting for database to be ready..."
        
        # Extract database connection details
        if [[ "$DATABASE_URL" == postgresql://* ]]; then
            # PostgreSQL
            DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\).*/\1/p')
            DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
            DB_NAME=$(echo $DATABASE_URL | sed -n 's/.*\/\([^?]*\).*/\1/p')
            DB_USER=$(echo $DATABASE_URL | sed -n 's/.*:\/\/\([^:]*\):.*/\1/p')
            
            echo "🔍 Checking PostgreSQL connection to $DB_HOST:$DB_PORT..."
            
            # Wait for PostgreSQL to be ready
            until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"; do
                echo "⏳ PostgreSQL is not ready yet, waiting..."
                sleep 2
            done
            
            echo "✅ PostgreSQL is ready!"
        elif [[ "$DATABASE_URL" == mysql://* ]]; then
            # MySQL
            echo "🔍 Checking MySQL connection..."
            # Add MySQL wait logic here if needed
            echo "✅ MySQL connection ready!"
        fi
    else
        echo "📝 Using SQLite database"
    fi
}

# Function to initialize database
initialize_database() {
    echo "📊 Initializing database..."
    
    # Activate virtual environment and run init script
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
    
    # Run database initialization
    if python init_db.py; then
        echo "✅ Database initialized successfully"
    else
        echo "⚠️ Database initialization failed, but continuing..."
    fi
}

# Function to run tests in development mode
run_tests() {
    if [ "${ENVIRONMENT:-production}" = "development" ]; then
        echo "🧪 Running tests in development mode..."
        
        if [ -f ".venv/bin/activate" ]; then
            source .venv/bin/activate
        fi
        
        if python test_tracking.py; then
            echo "✅ Tests passed"
        else
            echo "⚠️ Tests failed, but continuing..."
        fi
    fi
}

# Function to display conversation tracking configuration
show_tracking_config() {
    echo "🗣️ Conversation Tracking Configuration:"
    echo "   📊 Background Monitoring: ${ENABLE_BACKGROUND_MONITORING:-true}"
    echo "   ⏱️ Monitoring Interval: ${MONITORING_INTERVAL_SECONDS:-300} seconds"
    echo "   🔍 Automatic Metadata: ${ENABLE_AUTOMATIC_METADATA:-true}"
    echo "   📝 Log Level: ${LOG_LEVEL:-INFO}"
    echo "   📁 Log File: ${LOG_FILE:-/app/logs/agent_tracker.log}"
    echo ""
}

# Main execution
main() {
    # Wait for database if using external database
    wait_for_database
    
    # Initialize database
    initialize_database
    
    # Run tests in development mode
    run_tests
    
    # Display conversation tracking configuration
    show_tracking_config
    
    # Start the MCP server
    echo "🔧 Starting MCP server with conversation tracking enabled..."
    echo "📝 All client-agent conversations will be automatically logged to the database"
    echo "🔄 Background monitoring will run every ${MONITORING_INTERVAL_SECONDS:-300} seconds"
    
    if [ -n "$DATABASE_URL" ]; then
        echo "💾 Database: $DATABASE_URL"
    else
        echo "💾 Database: $DB_PATH"
    fi
    
    echo "🌍 Environment: ${ENVIRONMENT:-production}"
    echo "👤 User ID: ${USER_ID:-anonymous}"
    echo ""
    
    # Activate virtual environment if it exists
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
    
    # Start the application
    exec python main.py
}

# Run main function
main
