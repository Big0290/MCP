#!/usr/bin/env python3
"""
Test script for PostgreSQL connectivity in MCP Agent Tracker
Run this to verify that PostgreSQL connection works correctly
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def test_postgres_connection():
    """Test PostgreSQL connection"""
    print("🧪 Testing PostgreSQL Connection...")
    
    # Test connection string
    db_url = "postgresql://mcp_user:mcp_password@localhost:5432/mcp_tracker"
    print(f"Database URL: {db_url}")
    
    try:
        # Create engine
        engine = create_engine(db_url)
        
        # Test connection
        with engine.connect() as conn:
            # Test basic query
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✓ Connected to PostgreSQL: {version}")
            
            # Test schema
            result = conn.execute(text("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'mcp_tracker'"))
            schema = result.fetchone()
            if schema:
                print("✓ mcp_tracker schema exists")
            else:
                print("⚠ mcp_tracker schema not found")
            
            # Test tables
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'mcp_tracker'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"✓ Tables in mcp_tracker schema: {tables}")
            
            # Test views
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.views 
                WHERE table_schema = 'mcp_tracker'
                ORDER BY table_name
            """))
            views = [row[0] for row in result.fetchall()]
            print(f"✓ Views in mcp_tracker schema: {views}")
            
            # Test functions
            result = conn.execute(text("""
                SELECT routine_name 
                FROM information_schema.routines 
                WHERE routine_schema = 'mcp_tracker'
                ORDER BY routine_name
            """))
            functions = [row[0] for row in result.fetchall()]
            print(f"✓ Functions in mcp_tracker schema: {functions}")
            
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    print("✓ PostgreSQL connection test completed successfully!")
    return True

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🔧 Testing Environment Configuration...")
    
    env_vars = {
        'DATABASE_URL': os.getenv('DATABASE_URL'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB'),
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    }
    
    for var, value in env_vars.items():
        if value:
            print(f"✓ {var}: {value}")
        else:
            print(f"⚠ {var}: Not set")
    
    return True

def main():
    """Run all PostgreSQL tests"""
    print("🐘 MCP Agent Tracker - PostgreSQL Test Suite")
    print("=" * 60)
    
    try:
        # Test environment
        test_environment_variables()
        
        # Test database connection
        if test_postgres_connection():
            print("\n🎉 All PostgreSQL tests passed successfully!")
            print("\nYour PostgreSQL setup is working correctly.")
            print("You can now use the MCP server with PostgreSQL tracking.")
        else:
            print("\n❌ PostgreSQL tests failed.")
            print("Please check your Docker setup and ensure PostgreSQL is running.")
            sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
