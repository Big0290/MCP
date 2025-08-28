-- PostgreSQL initialization script for MCP Agent Tracker
-- This script runs when the PostgreSQL container is first created

-- Create extensions for better performance and monitoring
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create a dedicated schema for the MCP tracker
CREATE SCHEMA IF NOT EXISTS mcp_tracker;

-- Set search path to include our schema
SET search_path TO mcp_tracker, public;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON SCHEMA mcp_tracker TO mcp_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA mcp_tracker TO mcp_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA mcp_tracker TO mcp_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA mcp_tracker GRANT ALL ON TABLES TO mcp_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA mcp_tracker GRANT ALL ON SEQUENCES TO mcp_user;

-- Log successful initialization
SELECT 'MCP Agent Tracker PostgreSQL database initialized successfully' as status;
