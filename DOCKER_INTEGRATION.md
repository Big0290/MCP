# 🐳 Docker Integration Guide

## Overview

The MCP Agent Tracker with Conversation Tracking is now fully integrated with Docker! This guide shows you how to use all the Docker features and how the conversation tracking system works in containers.

## 🚀 Quick Start

### 1. **Production Mode (PostgreSQL)**

```bash
# Start with PostgreSQL database
./docker-run.sh

# Or manually
docker-compose up --build
```

### 2. **Development Mode (SQLite)**

```bash
# Start with SQLite for development
./docker-run.sh -m dev

# Or manually
docker-compose -f docker-compose.dev.yml up --build
```

### 3. **With Database Management Tools**

```bash
# Start with PostgreSQL + pgAdmin
./docker-run.sh -m tools

# Or manually
docker-compose --profile tools up --build
```

## 🗣️ Conversation Tracking in Docker

### **Automatic Features (Zero User Interaction)**

✅ **Client Request Logging**: Every client prompt automatically logged  
✅ **Agent Response Logging**: Every agent response automatically captured  
✅ **Complete Conversation Turns**: Full request-response pairs recorded  
✅ **Background Monitoring**: System health checks every 5 minutes (prod) / 1 minute (dev)  
✅ **Automatic Metadata**: System info, container details, uptime  
✅ **Session Management**: Automatic session creation and tracking  
✅ **Error Handling**: All errors logged without breaking the system

### **What Gets Tracked**

| Feature                   | Production        | Development      |
| ------------------------- | ----------------- | ---------------- |
| **Background Monitoring** | Every 300 seconds | Every 60 seconds |
| **Automatic Metadata**    | ✅ Enabled        | ✅ Enabled       |
| **Log Level**             | INFO              | DEBUG            |
| **Database**              | PostgreSQL        | SQLite           |
| **Source Code Mounting**  | ❌ No             | ✅ Yes           |

## 🔧 Configuration Options

### **Environment Variables**

All conversation tracking features can be configured via environment variables:

```bash
# Enable/disable features
ENABLE_BACKGROUND_MONITORING=true
MONITORING_INTERVAL_SECONDS=300
ENABLE_AUTOMATIC_METADATA=true

# Logging configuration
LOG_LEVEL=INFO
LOG_FILE=/app/logs/agent_tracker.log

# Performance configuration
MAX_EXECUTION_TIME_MS=30000
BATCH_LOG_SIZE=100
```

### **Docker Compose Files**

- **`docker-compose.yml`** - Production with PostgreSQL
- **`docker-compose.dev.yml`** - Development with SQLite
- **`docker-compose.override.yml`** - Testing overrides

## 📊 Monitoring and Analytics

### **Background Health Checks**

The system automatically monitors:

- System uptime
- Process information
- Container health
- Database connectivity
- Error rates

### **Conversation Analytics**

```bash
# View conversation history
docker exec -it mcp-agent-tracker python -c "
from main import get_interaction_history
print(get_interaction_history())
"

# Get conversation summary
docker exec -it mcp-agent-tracker python -c "
from main import get_conversation_summary
print(get_conversation_summary())
"
```

## 🐳 Docker Commands

### **Starting Services**

```bash
# Production mode
docker-compose up --build

# Development mode
docker-compose -f docker-compose.dev.yml up --build

# With database tools
docker-compose --profile tools up --build
```

### **Managing Services**

```bash
# View logs
docker-compose logs -f mcp-agent-tracker

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up --build --force-recreate
```

### **Accessing Containers**

```bash
# Access MCP container
docker exec -it mcp-agent-tracker bash

# Access PostgreSQL
docker exec -it mcp-postgres psql -U mcp_user -d mcp_tracker

# Access pgAdmin (if enabled)
# Open http://localhost:8080 in browser
```

## 📁 File Structure

```
MCP/
├── docker-compose.yml              # Production configuration
├── docker-compose.dev.yml          # Development configuration
├── docker-compose.override.yml     # Testing overrides
├── Dockerfile                      # Container definition
├── docker-entrypoint.sh            # Container startup script
├── docker-run.sh                   # Easy startup script
├── env.docker                      # Docker environment template
├── main.py                         # MCP server with conversation tracking
├── interaction_logger.py           # Conversation tracking system
├── config.py                       # Configuration management
├── models.py                       # Database models
└── logs/                           # Log files directory
```

## 🔍 Health Checks

### **Container Health Monitoring**

The Docker containers include health checks:

```yaml
healthcheck:
  test:
    [
      'CMD',
      'bash',
      '-c',
      'source .venv/bin/activate && python -c "from models import get_session_factory; get_session_factory()()"',
    ]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### **Database Health**

PostgreSQL health is monitored:

```yaml
healthcheck:
  test: ['CMD-SHELL', 'pg_isready -U mcp_user -d mcp_tracker']
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 30s
```

## 📈 Performance Features

### **Production Optimizations**

- **Connection Pooling**: Optimized database connections
- **Shared Buffers**: 256MB PostgreSQL shared buffers
- **Effective Cache**: 1GB effective cache size
- **Max Connections**: 100 concurrent connections
- **pg_stat_statements**: Query performance monitoring

### **Development Features**

- **Source Code Mounting**: Live code changes without rebuilds
- **Faster Monitoring**: 60-second intervals for quick feedback
- **Debug Logging**: Verbose logging for development
- **SQLite**: Lightweight database for development

## 🚨 Troubleshooting

### **Common Issues**

1. **Database Connection Errors**

   ```bash
   # Check database health
   docker-compose ps

   # View database logs
   docker-compose logs postgres
   ```

2. **Conversation Tracking Not Working**

   ```bash
   # Check MCP container logs
   docker-compose logs mcp-agent-tracker

   # Verify configuration
   docker exec -it mcp-agent-tracker env | grep ENABLE
   ```

3. **Performance Issues**

   ```bash
   # Check resource usage
   docker stats

   # View conversation history
   docker exec -it mcp-agent-tracker python -c "from main import get_conversation_summary; print(get_conversation_summary())"
   ```

### **Debug Mode**

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Restart with debug
docker-compose down
docker-compose up --build
```

## 🎯 Best Practices

### **Production Deployment**

1. **Use PostgreSQL**: Better performance and reliability
2. **Monitor Resources**: Watch container resource usage
3. **Regular Backups**: Backup PostgreSQL data regularly
4. **Health Checks**: Monitor container health status
5. **Log Rotation**: Manage log file sizes

### **Development Workflow**

1. **Use Development Mode**: Faster feedback with SQLite
2. **Source Mounting**: Live code changes
3. **Debug Logging**: Verbose output for troubleshooting
4. **Frequent Testing**: Test conversation tracking regularly

## 🔮 Future Enhancements

The Docker integration is designed to support:

- **Kubernetes Deployment**: Easy scaling and orchestration
- **Multi-Environment**: Staging, production, testing
- **Monitoring Integration**: Prometheus, Grafana, etc.
- **CI/CD Pipeline**: Automated testing and deployment
- **Load Balancing**: Multiple MCP server instances

## 📚 Additional Resources

- **README.md**: Complete system documentation
- **env.example**: Environment configuration examples
- **test_conversation_tracking.py**: Testing conversation tracking
- **Docker Hub**: Official Python and PostgreSQL images

---

## 🎉 **Ready to Use!**

Your MCP Agent Tracker with Conversation Tracking is now fully Dockerized and ready for production use. The system will automatically track all client-agent conversations without any user intervention required.

**Start tracking conversations now:**

```bash
./docker-run.sh
```
