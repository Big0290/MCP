#!/bin/bash

# 🚀 MCP Conversation Intelligence System - One-Click Installer
# This script makes it incredibly easy to install MCP Intelligence in any project

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${1}${2}${NC}"
}

print_header() {
    echo ""
    print_color $PURPLE "🚀 MCP Conversation Intelligence System - One-Click Installer"
    print_color $PURPLE "=================================================================="
    echo ""
}

print_success() {
    print_color $GREEN "✅ $1"
}

print_info() {
    print_color $BLUE "ℹ️  $1"
}

print_warning() {
    print_color $YELLOW "⚠️  $1"
}

print_error() {
    print_color $RED "❌ $1"
}

# Check if Python 3 is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        print_info "Please install Python 3.8+ and try again"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]]; then
        print_error "Python 3.8+ is required, but found $python_version"
        exit 1
    fi
    
    print_success "Python $python_version found"
}

# Check if pip is available
check_pip() {
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_error "pip is required but not installed"
        print_info "Please install pip and try again"
        exit 1
    fi
    
    print_success "pip found"
}

# Get project path
get_project_path() {
    if [ -n "$1" ]; then
        PROJECT_PATH="$1"
    else
        PROJECT_PATH="$(pwd)"
    fi
    
    # Convert to absolute path
    PROJECT_PATH=$(cd "$PROJECT_PATH" && pwd)
    
    print_info "Project path: $PROJECT_PATH"
}

# Check if we're in a git repository
check_git() {
    if [ -d "$PROJECT_PATH/.git" ]; then
        print_success "Git repository detected"
    else
        print_warning "Not in a git repository - consider initializing one"
    fi
}

# Install dependencies
install_dependencies() {
    print_info "Installing MCP Intelligence dependencies..."
    
    # Check if requirements file exists
    if [ -f "$PROJECT_PATH/requirements_mcp_intelligence.txt" ]; then
        pip3 install -r "$PROJECT_PATH/requirements_mcp_intelligence.txt"
        print_success "Dependencies installed from requirements_mcp_intelligence.txt"
    else
        # Install core dependencies directly
        pip3 install httpx mcp[cli] sqlalchemy fastapi uvicorn[standard] psycopg2-binary pymysql
        print_success "Core dependencies installed"
    fi
}

# Initialize database
init_database() {
    print_info "Initializing database..."
    
    if [ -f "$PROJECT_PATH/init_db.py" ]; then
        cd "$PROJECT_PATH"
        python3 init_db.py
        print_success "Database initialized"
    else
        print_warning "Database initialization script not found"
    fi
}

# Test the installation
test_installation() {
    print_info "Testing installation..."
    
    cd "$PROJECT_PATH"
    
    # Test basic imports
    python3 -c "
try:
    from smart_context_injector import SmartContextInjector
    from prompt_generator import prompt_generator
    print('✅ Core imports successful')
    
    # Test initialization
    injector = SmartContextInjector('$PROJECT_PATH')
    stack_info = injector.detect_tech_stack()
    print(f'✅ Project detection successful: {stack_info[\"project_type\"]}')
    
    # Test prompt generation
    test_prompt = prompt_generator.generate_enhanced_prompt('Test message', 'smart')
    print('✅ Prompt generation successful')
    
    print('🎉 All tests passed!')
    
except Exception as e:
    print(f'❌ Test failed: {e}')
    exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_success "Installation test passed"
    else
        print_error "Installation test failed"
        exit 1
    fi
}

# Show next steps
show_next_steps() {
    echo ""
    print_color $GREEN "🎉 Installation Complete!"
    echo ""
    print_info "Next steps:"
    echo "  1. Start the system:"
    echo "     cd $PROJECT_PATH"
    echo "     ./start_mcp_intelligence.sh"
    echo ""
    echo "  2. Or start manually:"
    echo "     python3 local_mcp_server_simple.py"
    echo ""
    echo "  3. Read the usage guide:"
    echo "     cat MCP_INTELLIGENCE_USAGE.md"
    echo ""
    echo "  4. For Cursor IDE integration:"
    echo "     cat cursor_mcp_config.json"
    echo ""
    print_info "Your project now has intelligent AI assistance with:"
    echo "  • Automatic tech stack detection"
    echo "  • Context-aware prompt enhancement"
    echo "  • Conversation tracking and memory"
    echo "  • User preference learning"
    echo "  • Real-time context refinement"
    echo ""
}

# Main installation function
main() {
    print_header
    
    # Parse arguments
    PROJECT_PATH=""
    INTERACTIVE=true
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --project-path)
                PROJECT_PATH="$2"
                shift 2
                ;;
            --no-interactive)
                INTERACTIVE=false
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [--project-path PATH] [--no-interactive]"
                echo ""
                echo "Options:"
                echo "  --project-path PATH    Install in specific project directory"
                echo "  --no-interactive       Skip interactive prompts"
                echo "  --help, -h            Show this help message"
                echo ""
                echo "Examples:"
                echo "  $0                                    # Install in current directory"
                echo "  $0 --project-path /path/to/project   # Install in specific project"
                echo "  $0 --no-interactive                  # Non-interactive installation"
                exit 0
                ;;
            *)
                if [ -z "$PROJECT_PATH" ]; then
                    PROJECT_PATH="$1"
                fi
                shift
                ;;
        esac
    done
    
    # Get project path
    get_project_path "$PROJECT_PATH"
    
    # Check prerequisites
    check_python
    check_pip
    check_git
    
    # Run the Python setup script
    print_info "Running MCP Intelligence setup..."
    
    if [ "$INTERACTIVE" = true ]; then
        python3 setup_mcp_intelligence.py --project-path "$PROJECT_PATH"
    else
        python3 setup_mcp_intelligence.py --project-path "$PROJECT_PATH" --no-interactive
    fi
    
    if [ $? -ne 0 ]; then
        print_error "Setup script failed"
        exit 1
    fi
    
    # Install dependencies
    install_dependencies
    
    # Initialize database
    init_database
    
    # Test installation
    test_installation
    
    # Show next steps
    show_next_steps
}

# Run main function with all arguments
main "$@"
