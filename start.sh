#!/bin/bash

# Simple startup script for MCP system
# No Docker, no complexity - just Python services

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Directories
LOG_DIR="./logs"
PID_DIR="./pids"

mkdir -p "$LOG_DIR" "$PID_DIR"

log() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date +'%H:%M:%S')] ERROR:${NC} $1"
}

# Check if port is free
check_port() {
    local port="$1"
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Free port if needed
free_port() {
    local port="$1"
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [[ -n "$pids" ]]; then
        log "Port $port is in use. Stopping processes: $pids"
        kill -9 $pids 2>/dev/null || true
        sleep 2
    fi
}

# Start a service
start_service() {
    local name="$1"
    local command="$2"
    local port="$3"
    local pid_file="$PID_DIR/${name}.pid"
    local log_file="$LOG_DIR/${name}.log"
    
    # Check if already running
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            log "$name is already running (PID: $pid)"
            return 0
        fi
    fi
    
    # Free port if needed
    if [[ -n "$port" ]] && check_port "$port"; then
        free_port "$port"
    fi
    
    log "Starting $name..."
    
    # Start service
    eval "$command" > "$log_file" 2>&1 &
    local pid=$!
    echo "$pid" > "$pid_file"
    
    sleep 2
    
    if kill -0 "$pid" 2>/dev/null; then
        log "✅ $name started (PID: $pid)"
    else
        log_error "$name failed to start. Check: $log_file"
        rm -f "$pid_file"
        return 1
    fi
}

# Stop a service
stop_service() {
    local name="$1"
    local pid_file="$PID_DIR/${name}.pid"
    
    if [[ -f "$pid_file" ]]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            log "Stopping $name (PID: $pid)..."
            kill "$pid"
            rm -f "$pid_file"
            log "✅ $name stopped"
        else
            rm -f "$pid_file"
        fi
    fi
}

# Show status
show_status() {
    echo -e "\n📊 Service Status:"
    echo "=================="
    
    local services=("ui")
    
    for service in "${services[@]}"; do
        local pid_file="$PID_DIR/${service}.pid"
        if [[ -f "$pid_file" ]]; then
            local pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                echo -e "${GREEN}✅ $service${NC} - Running (PID: $pid)"
            else
                echo -e "${RED}❌ $service${NC} - Not running"
                rm -f "$pid_file"
            fi
        else
            echo -e "${RED}❌ $service${NC} - Not running"
        fi
    done
    
    echo -e "\n🔗 Access URLs:"
    echo "================"
    echo "🌐 UI: http://localhost:8501"
    echo "🔌 MCP Server: Started on-demand by UI"
}

# Main startup
start_all() {
    log "🚀 Starting MCP System..."
    
    # Activate virtual environment
    if [[ -f "ui_env/bin/activate" ]]; then
        log "🔧 Activating virtual environment..."
        source ui_env/bin/activate
    fi
    
    # Start UI (MCP server will be started when needed by the UI)
    if [[ -f "context_ui.py" ]]; then
        start_service "ui" "streamlit run context_ui.py --server.port 8501 --server.headless true" "8501"
    else
        log "⚠️ UI file not found: context_ui.py"
    fi
    
    # Start MCP stdio server for interactive communication
    if [[ -f "start_stdio_server.py" ]]; then
        log "🔌 MCP stdio server can be started separately with:"
        log "   source ui_env/bin/activate && python3 start_stdio_server.py"
    fi
    
    sleep 3
    show_status
    
    log "🎉 Done! Use './start.sh status' to check status"
}

# Stop all
stop_all() {
    log "🛑 Stopping all services..."
    
    local services=("ui")
    for service in "${services[@]}"; do
        stop_service "$service"
    done
    
    log "✅ All services stopped"
}

# Main function
case "${1:-start}" in
    "start")
        start_all
        ;;
    "stop")
        stop_all
        ;;
    "restart")
        stop_all
        sleep 2
        start_all
        ;;
    "status")
        show_status
        ;;
    "logs")
        if [[ -z "$2" ]]; then
            echo "Usage: $0 logs <service_name>"
            echo "Services: mcp_server, ui"
            exit 1
        fi
        local log_file="$LOG_DIR/$2.log"
        if [[ -f "$log_file" ]]; then
            echo "📝 Logs for $2:"
            tail -f "$log_file"
        else
            echo "Log file not found: $log_file"
        fi
        ;;
    "help"|"-h"|"--help")
        echo "MCP Startup Script"
        echo "=================="
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  start     Start all services (default)"
        echo "  stop      Stop all services"
        echo "  restart   Restart all services"
        echo "  status    Show service status"
        echo "  logs <service>  Show logs for a service"
        echo "  help      Show this help message"
        ;;
    *)
        log_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
