#!/usr/bin/env python3
"""
Python-based Docker entrypoint for MCP Agent Tracker
This provides an alternative to the bash script for better reliability
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def print_status(message):
    """Print a status message"""
    print(f"🚀 {message}")

def check_dependencies():
    """Check if required dependencies are available"""
    print_status("Checking dependencies...")
    
    missing_deps = []
    
    try:
        import sqlalchemy
        print_status("✅ SQLAlchemy available")
    except ImportError:
        missing_deps.append("sqlalchemy")
        print_status("❌ SQLAlchemy not available")
    
    try:
        import mcp
        print_status("✅ MCP package available")
    except ImportError:
        missing_deps.append("mcp")
        print_status("❌ MCP package not available")
    
    if missing_deps:
        print_status(f"⚠️ Missing dependencies: {', '.join(missing_deps)}")
        print_status("This might be due to installation issues")
        return False
    
    return True

def wait_for_database():
    """Wait for database to be ready"""
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print_status("Using SQLite database")
        return
    
    print_status("Waiting for database to be ready...")
    
    if database_url.startswith('postgresql://'):
        # Extract PostgreSQL connection details
        try:
            # Simple parsing of DATABASE_URL
            parts = database_url.replace('postgresql://', '').split('@')
            if len(parts) == 2:
                user_pass, host_port_db = parts
                host_port, db_name = host_port_db.split('/', 1)
                host, port = host_port.split(':') if ':' in host_port else (host_port, '5432')
                
                print_status(f"Checking PostgreSQL connection to {host}:{port}...")
                
                # Wait for PostgreSQL to be ready
                max_attempts = 30
                for attempt in range(max_attempts):
                    try:
                        result = subprocess.run([
                            'pg_isready', '-h', host, '-p', port, '-U', user_pass.split(':')[0]
                        ], capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0:
                            print_status("✅ PostgreSQL is ready!")
                            return
                    except Exception as e:
                        pass
                    
                    print_status(f"⏳ PostgreSQL not ready yet, attempt {attempt + 1}/{max_attempts}")
                    time.sleep(2)
                
                print_status("⚠️ PostgreSQL connection timeout, continuing anyway...")
            else:
                print_status("⚠️ Could not parse DATABASE_URL, continuing...")
        except Exception as e:
            print_status(f"⚠️ Error parsing DATABASE_URL: {e}, continuing...")
    
    elif database_url.startswith('mysql://'):
        print_status("✅ MySQL connection ready!")
    else:
        print_status("⚠️ Unknown database type, continuing...")

def initialize_database():
    """Initialize the database"""
    print_status("Initializing database...")
    
    try:
        # Try to run the init script
        if Path('init_db.py').exists():
            result = subprocess.run([sys.executable, 'init_db.py'], 
                                 capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print_status("✅ Database initialized successfully")
            else:
                print_status(f"⚠️ Database initialization failed: {result.stderr}")
        else:
            print_status("⚠️ init_db.py not found, skipping database initialization")
    except Exception as e:
        print_status(f"⚠️ Database initialization error: {e}")

def run_tests():
    """Run tests in development mode"""
    if os.getenv('ENVIRONMENT') == 'development':
        print_status("Running tests in development mode...")
        
        try:
            if Path('test_tracking.py').exists():
                result = subprocess.run([sys.executable, 'test_tracking.py'], 
                                     capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print_status("✅ Tests passed")
                else:
                    print_status(f"⚠️ Tests failed: {result.stderr}")
            else:
                print_status("⚠️ test_tracking.py not found, skipping tests")
        except Exception as e:
            print_status(f"⚠️ Test execution error: {e}")

def show_tracking_config():
    """Display conversation tracking configuration"""
    print_status("Conversation Tracking Configuration:")
    print(f"   📊 Background Monitoring: {os.getenv('ENABLE_BACKGROUND_MONITORING', 'true')}")
    print(f"   ⏱️ Monitoring Interval: {os.getenv('MONITORING_INTERVAL_SECONDS', '300')} seconds")
    print(f"   🔍 Automatic Metadata: {os.getenv('ENABLE_AUTOMATIC_METADATA', 'true')}")
    print(f"   📝 Log Level: {os.getenv('LOG_LEVEL', 'INFO')}")
    print(f"   📁 Log File: {os.getenv('LOG_FILE', '/app/logs/agent_tracker.log')}")
    print()

def main():
    """Main entrypoint function"""
    print_status("Starting MCP Agent Tracker with Conversation Tracking...")
    
    # Check dependencies first
    if not check_dependencies():
        print_status("⚠️ Some dependencies are missing, but continuing...")
    
    # Wait for database
    wait_for_database()
    
    # Initialize database
    initialize_database()
    
    # Run tests in development mode
    run_tests()
    
    # Show tracking configuration
    show_tracking_config()
    
    # Start the MCP server
    print_status("Starting MCP server with conversation tracking enabled...")
    print_status("All client-agent conversations will be automatically logged to the database")
    
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print_status(f"Database: {database_url}")
    else:
        print_status(f"Database: {os.getenv('DB_PATH', '/app/data/agent_tracker.db')}")
    
    print_status(f"Environment: {os.getenv('ENVIRONMENT', 'production')}")
    print_status(f"User ID: {os.getenv('USER_ID', 'anonymous')}")
    print()
    
    # Start the main application
    try:
        # Import and run the main application
        from main import mcp
        from config import Config
        print_status("✅ MCP server imported successfully")
        
        transport = Config.MCP_TRANSPORT
        print_status(f"Starting server with {transport} transport...")
        
        if transport == "http":
            # For HTTP transport, start the HTTP server
            print_status("🌐 Starting HTTP server for conversation tracking tools...")
            try:
                from mcp_http_server import app
                import uvicorn
                print_status("✅ HTTP server dependencies imported successfully")
                uvicorn.run(app, host="0.0.0.0", port=8000)
            except ImportError as e:
                print_status(f"❌ Failed to import HTTP server: {e}")
                print_status("💡 Make sure fastapi and uvicorn are installed:")
                print_status("   pip install fastapi uvicorn[standard]")
                print_status("❌ Cannot fall back to stdio when HTTP transport is explicitly requested")
                raise
            except Exception as e:
                print_status(f"❌ HTTP server error: {e}")
                raise
        else:
            # For stdio or other transports, use the MCP server directly
            mcp.run(transport=transport)
        
    except ImportError as e:
        print_status(f"❌ Import error: {e}")
        print_status("This usually means the MCP package is not installed")
        print_status("Check that pip install completed successfully")
        sys.exit(1)
    except Exception as e:
        print_status(f"❌ Failed to start MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
