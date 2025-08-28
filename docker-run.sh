#!/bin/bash

# MCP Agent Tracker Docker Runner Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -m, --mode MODE       Run mode: dev, prod, or tools (default: prod)"
    echo "  -b, --build           Build images before running"
    echo "  -c, --clean           Clean up containers and volumes before running"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Modes:"
    echo "  dev     - Development mode with SQLite and source code mounting"
    echo "  prod    - Production mode with PostgreSQL (default)"
    echo "  tools   - Production mode with PostgreSQL + pgAdmin"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run in production mode"
    echo "  $0 -m dev            # Run in development mode"
    echo "  $0 -m tools          # Run with pgAdmin"
    echo "  $0 -b -c             # Build, clean, and run in production mode"
}

# Default values
MODE="prod"
BUILD=false
CLEAN=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -m|--mode)
            MODE="$2"
            shift 2
            ;;
        -b|--build)
            BUILD=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate mode
if [[ ! "$MODE" =~ ^(dev|prod|tools)$ ]]; then
    print_error "Invalid mode: $MODE. Must be dev, prod, or tools."
    exit 1
fi

print_status "Starting MCP Agent Tracker with Conversation Tracking in $MODE mode..."

# Clean up if requested
if [ "$CLEAN" = true ]; then
    print_status "Cleaning up existing containers and volumes..."
    docker-compose down -v 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true
    print_success "Cleanup completed"
fi

# Build if requested
if [ "$BUILD" = true ]; then
    print_status "Building Docker images..."
    docker-compose build
    print_success "Build completed"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Run based on mode
case $MODE in
    "dev")
        print_status "Starting development environment with SQLite and conversation tracking..."
        docker-compose -f docker-compose.dev.yml up --build
        ;;
    "prod")
        print_status "Starting production environment with PostgreSQL and conversation tracking..."
        docker-compose up --build
        ;;
    "tools")
        print_status "Starting production environment with PostgreSQL + pgAdmin and conversation tracking..."
        docker-compose --profile tools up --build
        ;;
esac

print_success "MCP Agent Tracker with Conversation Tracking started successfully in $MODE mode!"
echo ""
echo "🗣️ Conversation Tracking Features:"
echo "  ✅ Automatic client request logging"
echo "  ✅ Automatic agent response logging"
echo "  ✅ Complete conversation turn tracking"
echo "  ✅ Background system monitoring"
echo "  ✅ Automatic metadata collection"
echo "  ✅ Zero user interaction required"
echo ""
echo "Access Information:"
case $MODE in
    "dev")
        echo "  - MCP Server: Running in container (use docker exec to interact)"
        echo "  - Database: SQLite (persistent in ./data/)"
        echo "  - Source Code: Mounted from host directory"
        echo "  - Monitoring: Every 60 seconds (development mode)"
        ;;
    "prod")
        echo "  - MCP Server: Running in container (use docker exec to interact)"
        echo "  - Database: PostgreSQL (port 5432)"
        echo "  - Database User: mcp_user"
        echo "  - Database Password: mcp_password"
        echo "  - Database Name: mcp_tracker"
        echo "  - Monitoring: Every 300 seconds (production mode)"
        ;;
    "tools")
        echo "  - MCP Server: Running in container (use docker exec to interact)"
        echo "  - Database: PostgreSQL (port 5432)"
        echo "  - pgAdmin: http://localhost:8080"
        echo "    - Email: admin@mcp.local"
        echo "    - Password: admin123"
        echo "  - Monitoring: Every 300 seconds (production mode)"
        ;;
esac
echo ""
echo "📊 Conversation Tracking Commands:"
echo "  - View conversation history: docker exec -it mcp-agent-tracker python -c \"from main import get_interaction_history; print(get_interaction_history())\""
echo "  - Get conversation summary: docker exec -it mcp-agent-tracker python -c \"from main import get_conversation_summary; print(get_conversation_summary())\""
echo "  - View tracking logs: docker-compose logs -f mcp-agent-tracker"
echo ""
echo "🔧 General Commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Access container: docker exec -it mcp-agent-tracker bash"
echo "  - View database: docker exec -it mcp-postgres psql -U mcp_user -d mcp_tracker"
echo ""
echo "💡 The system is now automatically tracking all client-agent conversations!"
echo "   No manual intervention is required - everything is logged automatically."
