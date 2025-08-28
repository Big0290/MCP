# MCP Agent Tracker

A Model Context Protocol (MCP) server that automatically tracks client-agent conversations without requiring any user interaction.

## Features

### 🗣️ **Automatic Conversation Tracking**

- **Zero User Interaction Required**: All conversations are tracked automatically
- **Client Request Logging**: Every client prompt/request is logged
- **Agent Response Logging**: Every agent response is captured
- **Complete Conversation Turns**: Full request-response pairs are recorded
- **Session Management**: Automatic session creation and tracking

### 🔧 **MCP Tools Available**

- `get_current_weather(city)`: Get weather information for a city
- `agent_interaction(prompt)`: Interact with the agent
- `get_interaction_history(limit, session_id)`: Retrieve conversation history
- `get_conversation_summary(session_id)`: Get conversation statistics and patterns

### 📊 **Automatic Monitoring**

- **Background Health Checks**: Continuous system monitoring every 5 minutes
- **Automatic Metadata Collection**: System info, process details, uptime
- **Error Tracking**: Comprehensive error logging and recovery
- **Performance Metrics**: Execution times and system health

## How It Works

### 1. **Automatic Session Creation**

```python
# Sessions are created automatically when the server starts
# No user input required
logger.get_or_create_session()
```

### 2. **Client Request Tracking**

```python
# Every client request is automatically logged
logger.log_client_request(f"Get weather for {city}")
```

### 3. **Agent Response Tracking**

```python
# Every agent response is automatically captured
logger.log_agent_response(response)
```

### 4. **Complete Conversation Logging**

```python
# Full conversation turns are recorded
logger.log_conversation_turn(
    client_request=f"Get weather for {city}",
    agent_response=response
)
```

### 5. **Background Monitoring**

```python
# System health is monitored continuously
# No user interaction needed
def background_monitoring():
    while True:
        logger.log_interaction(interaction_type='health_check', ...)
        time.sleep(Config.MONITORING_INTERVAL_SECONDS)
```

## Configuration

### Environment Variables

```bash
# Enable/disable features
ENABLE_BACKGROUND_MONITORING=true
MONITORING_INTERVAL_SECONDS=300
ENABLE_AUTOMATIC_METADATA=true

# Database and logging
DATABASE_URL=
DB_PATH=./data/agent_tracker.db
LOG_LEVEL=INFO
```

### Configuration Options

- **`ENABLE_BACKGROUND_MONITORING`**: Enable continuous system monitoring
- **`MONITORING_INTERVAL_SECONDS`**: How often to run health checks (default: 300s)
- **`ENABLE_AUTOMATIC_METADATA`**: Collect system info automatically

## Database Schema

### AgentInteraction Table

```sql
CREATE TABLE agent_interactions (
    id INTEGER PRIMARY KEY,
    timestamp TIMESTAMP,
    session_id VARCHAR(255),
    user_id VARCHAR(255),
    interaction_type VARCHAR(100),  -- 'client_request', 'agent_response', 'conversation_turn'
    prompt TEXT,                    -- Client request
    response TEXT,                  -- Agent response
    status VARCHAR(50),
    error_message TEXT,
    meta_data JSON                  -- Automatic system metadata
);
```

### Session Table

```sql
CREATE TABLE sessions (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    started_at TIMESTAMP,
    last_activity TIMESTAMP,
    total_interactions INTEGER,
    meta_data JSON
);
```

## Usage Examples

### Basic Conversation Tracking

```python
@mcp.tool()
def my_tool(prompt: str) -> str:
    # Client request is automatically logged
    logger.log_client_request(prompt)

    # Process the request
    response = process_request(prompt)

    # Agent response is automatically logged
    logger.log_agent_response(response)

    # Complete conversation turn is recorded
    logger.log_conversation_turn(prompt, response)

    return response
```

### Getting Conversation History

```python
# Get recent conversations
history = get_interaction_history(limit=10)

# Get conversation summary
summary = get_conversation_summary()
```

## Security Features

- **Environment Variables**: All configuration via environment variables
- **No Hardcoded Secrets**: Secure credential management
- **Isolated Database Schema**: Separate schema for tracking data
- **Error Isolation**: Logging failures don't break main functionality

## Getting Started

1. **Copy environment file**:

   ```bash
   cp env.example .env
   ```

2. **Configure your environment**:

   ```bash
   # Edit .env with your settings
   ENABLE_BACKGROUND_MONITORING=true
   MONITORING_INTERVAL_SECONDS=300
   ```

3. **Run the server**:

   ```bash
   python main.py
   ```

4. **Monitor conversations**:

   ```bash
   # Use the MCP tools to interact and track conversations
   ```

## 🚀 Using in Cursor

### Prerequisites

- **Cursor IDE** installed on your system
- **Python 3.8+** with pip/uv package management
- **Git** for cloning the repository

### Step 1: Setup MCP Server

1. **Clone and navigate to your project**:

   ```bash
   cd /path/to/your/mcp/project
   ```

2. **Install dependencies**:

   ```bash
   # Using pip
   pip install -r requirements.txt

   # Or using uv (recommended)
   uv sync
   ```

3. **Configure environment**:

   ```bash
   cp env.example .env
   # Edit .env with your preferred settings
   ```

### Step 2: Configure Cursor for MCP

1. **Open Cursor Settings**:

   - Press `Cmd+,` (Mac) or `Ctrl+,` (Windows/Linux)
   - Or go to `Cursor → Preferences → Settings`

2. **Add MCP Configuration**:

   ```json
   {
     "mcpServers": {
       "mcp-project": {
         "command": "python",
         "args": ["/absolute/path/to/your/project/main.py"],
         "env": {
           "PYTHONPATH": "/absolute/path/to/your/project"
         }
       }
     }
   }
   ```

3. **Alternative: Use relative paths** (if Cursor is opened in project directory):

   ```json
   {
     "mcpServers": {
       "mcp-project": {
         "command": "python",
         "args": ["./main.py"]
       }
     }
   }
   ```

### Step 3: Test MCP Integration

1. **Restart Cursor** after adding MCP configuration

2. **Open Command Palette** (`Cmd+Shift+P` or `Ctrl+Shift+P`)

3. **Type "MCP"** to see available MCP commands

4. **Test a tool**:
   - Use `get_current_weather("New York")` to test weather functionality
   - Use `agent_interaction("Hello, how are you?")` to test conversation tracking
   - Use `get_system_status()` to check system health

### Step 4: Use MCP Tools in Cursor

#### Available Tools

- **`get_current_weather(city)`**: Get weather for any city
- **`agent_interaction(prompt)`**: Interact with the agent and track conversations
- **`get_interaction_history(limit, session_id)`**: View conversation history
- **`get_conversation_summary(session_id)`**: Get conversation analytics
- **`get_system_status()`**: Check system health and configuration
- **`test_conversation_tracking(message)`**: Test the tracking system

#### Example Usage in Cursor

1. **Open Command Palette** (`Cmd+Shift+P`)

2. **Type MCP command**:

   ```
   MCP: mcp-project: get_current_weather
   ```

3. **Enter parameters** when prompted:

   ```
   city: San Francisco
   ```

4. **View results** in the output panel

### Step 5: Monitor and Debug

#### View Conversation History

```bash
# In Cursor terminal or via MCP tools
python -c "
from main import get_interaction_history
print(get_interaction_history(limit=5))
"
```

#### Check System Status

```bash
# Via MCP tools in Cursor
get_system_status()
```

#### Test Conversation Tracking

```bash
# Via MCP tools in Cursor
test_conversation_tracking("Test message from Cursor")
```

### Troubleshooting

#### Common Issues

1. **"MCP server not found"**:

   - Check the absolute path in your Cursor settings
   - Ensure the Python path is correct
   - Verify the server is running

2. **"Import errors"**:

   - Check `PYTHONPATH` in MCP configuration
   - Ensure all dependencies are installed
   - Verify you're in the correct directory

3. **"Permission denied"**:
   - Make sure `main.py` is executable
   - Check file permissions
   - Try running with `python3` instead of `python`

#### Debug Commands

```bash
# Test MCP server directly
python main.py

# Check dependencies
pip list | grep mcp

# Verify configuration
python -c "from config import Config; print(Config.ENVIRONMENT)"
```

### Advanced Configuration

#### Custom MCP Server Names

```json
{
  "mcpServers": {
    "my-custom-mcp": {
      "command": "python",
      "args": ["./main.py"],
      "env": {
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

#### Multiple MCP Servers

```json
{
  "mcpServers": {
    "mcp-project": { "command": "python", "args": ["./main.py"] },
    "another-mcp": { "command": "python", "args": ["./other_mcp.py"] }
  }
}
```

### Benefits in Cursor

✅ **Seamless Integration**: Use MCP tools directly in your IDE  
✅ **Real-time Monitoring**: Track conversations as you work  
✅ **Debugging Tools**: Built-in testing and monitoring functions  
✅ **Performance Insights**: Monitor system health and usage  
✅ **Conversation Analytics**: Analyze interaction patterns  
✅ **Zero Configuration**: Automatic setup and tracking

Your MCP server will now be fully integrated with Cursor, providing powerful conversation tracking and monitoring capabilities right in your development environment!

## What Gets Tracked Automatically

✅ **Client Requests**: Every prompt, question, or request  
✅ **Agent Responses**: Every response, answer, or action  
✅ **Conversation Flow**: Complete request-response pairs  
✅ **System Health**: Background monitoring and metrics  
✅ **Error Handling**: All errors and exceptions  
✅ **Session Data**: User sessions and activity  
✅ **Metadata**: System info, timestamps, environment

❌ **Tool Usage**: Internal MCP tool executions are not tracked  
❌ **User Input**: No manual logging required  
❌ **Configuration**: Automatic setup and management

The system is designed to be completely hands-off - once started, it will track all client-agent conversations automatically without any intervention needed.
