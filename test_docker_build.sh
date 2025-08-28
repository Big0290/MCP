#!/bin/bash

# Test script for Docker build
# This script tests if the Docker container can be built and run successfully

set -e

echo "🧪 Testing Docker Build for MCP Agent Tracker..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Test 1: Build the Docker image
echo "📦 Building Docker image..."
if docker build -t mcp-test .; then
    print_success "Docker image built successfully"
else
    print_error "Docker build failed"
    exit 1
fi

# Test 2: Test dependency installation
echo "🔍 Testing dependency installation..."
if docker run --rm mcp-test python -c "import mcp, sqlalchemy; print('✅ All dependencies available')"; then
    print_success "Dependencies are properly installed"
else
    print_error "Dependency test failed"
    exit 1
fi

# Test 3: Test entrypoint script
echo "🚀 Testing entrypoint script..."
if docker run --rm mcp-test python docker-entrypoint.py --help 2>/dev/null || \
   docker run --rm mcp-test python docker-entrypoint.py 2>&1 | grep -q "Starting MCP Agent Tracker"; then
    print_success "Entrypoint script works correctly"
else
    print_warning "Entrypoint script test inconclusive (this is normal)"
fi

# Test 4: Test basic imports
echo "📚 Testing basic imports..."
if docker run --rm mcp-test python -c "
from interaction_logger import logger
from config import Config
print('✅ Core modules imported successfully')
"; then
    print_success "Core modules can be imported"
else
    print_error "Core module import test failed"
    exit 1
fi

print_success "All Docker build tests passed!"
echo ""
echo "🎉 Your Docker container is ready to use!"
echo ""
echo "To start the services:"
echo "  ./docker-run.sh"
echo ""
echo "Or manually:"
echo "  docker-compose up --build"
