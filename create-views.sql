-- Create database views for MCP Agent Tracker
-- This script should be run AFTER the application has created the tables

-- Create a view for monitoring recent interactions
CREATE OR REPLACE VIEW mcp_tracker.recent_interactions AS
SELECT 
    ai.id,
    ai.timestamp,
    ai.session_id,
    ai.user_id,
    ai.interaction_type,
    ai.tool_name,
    ai.status,
    ai.execution_time_ms,
    s.started_at as session_started,
    s.total_interactions
FROM mcp_tracker.agent_interactions ai
LEFT JOIN mcp_tracker.sessions s ON ai.session_id = s.id
ORDER BY ai.timestamp DESC;

-- Create a view for tool performance statistics
CREATE OR REPLACE VIEW mcp_tracker.tool_performance AS
SELECT 
    tool_name,
    COUNT(*) as total_calls,
    AVG(execution_time_ms) as avg_execution_time_ms,
    MIN(execution_time_ms) as min_execution_time_ms,
    MAX(execution_time_ms) as max_execution_time_ms,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as error_count,
    (SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END)::float / COUNT(*)::float * 100)::numeric(5,2) as success_rate_percent
FROM mcp_tracker.agent_interactions 
WHERE interaction_type = 'tool_response'
GROUP BY tool_name
ORDER BY total_calls DESC;

-- Create a view for session analytics
CREATE OR REPLACE VIEW mcp_tracker.session_analytics AS
SELECT 
    s.id as session_id,
    s.user_id,
    s.started_at,
    s.last_activity,
    s.total_interactions,
    EXTRACT(EPOCH FROM (s.last_activity - s.started_at)) as session_duration_seconds,
    COUNT(ai.id) as actual_interactions,
    AVG(ai.execution_time_ms) as avg_tool_execution_time_ms
FROM mcp_tracker.sessions s
LEFT JOIN mcp_tracker.agent_interactions ai ON s.id = ai.session_id
GROUP BY s.id, s.user_id, s.started_at, s.last_activity, s.total_interactions
ORDER BY s.last_activity DESC;

-- Grant access to views
GRANT SELECT ON mcp_tracker.recent_interactions TO mcp_user;
GRANT SELECT ON mcp_tracker.tool_performance TO mcp_user;
GRANT SELECT ON mcp_tracker.session_analytics TO mcp_user;

-- Create a function to clean up old data (useful for maintenance)
CREATE OR REPLACE FUNCTION mcp_tracker.cleanup_old_data(days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    -- Delete old interactions
    DELETE FROM mcp_tracker.agent_interactions 
    WHERE timestamp < NOW() - INTERVAL '1 day' * days_to_keep;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Delete old sessions that have no interactions
    DELETE FROM mcp_tracker.sessions s
    WHERE s.last_activity < NOW() - INTERVAL '1 day' * days_to_keep
    AND NOT EXISTS (
        SELECT 1 FROM mcp_tracker.agent_interactions ai 
        WHERE ai.session_id = s.id
    );
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Grant execute permission on cleanup function
GRANT EXECUTE ON FUNCTION mcp_tracker.cleanup_old_data(INTEGER) TO mcp_user;

-- Log successful view creation
SELECT 'MCP Agent Tracker database views created successfully' as status;
