# Enhanced Conversation Context Injection System

## Overview

The Enhanced Conversation Context Injection System transforms your MCP Agent Tracker from a simple logging tool into an intelligent context-aware system that can inject relevant conversation history, user preferences, and project context into every interaction with your Cursor agent.

## Key Features

### 🌳 Decision Tree Context Analysis
- **Hierarchical Topic Structure**: Organizes conversations into logical branches (technical, project, user, system)
- **Active Branch Detection**: Identifies currently relevant conversation topics
- **Context Relevance Scoring**: Prioritizes context based on recency, interaction type, and content length

### 🧠 Intelligent Context Generation
- **Semantic Keyword Extraction**: Uses NLP techniques to identify meaningful terms
- **Topic Categorization**: Automatically categorizes interactions into 10+ topic types
- **User Preference Inference**: Learns user communication style and technical level
- **Project Context Extraction**: Detects files, technologies, and project patterns

### 🚀 Context Injection for Cursor
- **Enhanced Prompts**: Automatically injects relevant context into every prompt
- **Personalized Responses**: Tailors responses based on user history and preferences
- **Project Awareness**: Provides context about current project structure and tech stack
- **Conversation Continuity**: Maintains context across multiple interactions

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cursor Agent  │───▶│ Context Injection│───▶│ Enhanced Prompt │
└─────────────────┘    │      Tool        │    └─────────────────┘
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Decision Tree    │
                       │ Context Manager  │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Database with    │
                       │ Full Content    │
                       │ Retention       │
                       └──────────────────┘
```

## Installation & Setup

### 1. Database Migration
First, run the database migration to add new context tracking fields:

```bash
python migrate_database.py
```

This will:
- Add new columns to existing tables
- Create the `conversation_contexts` table
- Add performance indexes
- Support both PostgreSQL and SQLite

### 2. Environment Configuration
Ensure your environment variables are set:

```bash
# For PostgreSQL (recommended)
DATABASE_URL=postgresql://mcp_user:mcp_password@localhost:5432/mcp_tracker

# For SQLite (development)
DB_PATH=./data/agent_tracker.db
```

### 3. Start the Enhanced System
The system will automatically start using the enhanced context tracking:

```bash
# Start MCP server with context injection
python main.py

# Or use HTTP server
python mcp_http_server.py
```

## Usage

### Basic Context Injection

The system automatically enhances every interaction with context. Simply use the existing MCP tools:

```python
# Get conversation summary with enhanced context
summary = get_conversation_summary()

# Get detailed context analysis
context = get_conversation_context()
```

### Advanced Context Injection

Use the new context injection tool to enhance prompts for Cursor:

```python
# Inject context into a base prompt
base_prompt = "Help me fix this bug in my React component"
enhanced_prompt = inject_conversation_context(base_prompt)

# The enhanced prompt will include:
# - Recent conversation history
# - User preferences and technical level
# - Project context and tech stack
# - Active conversation branches
# - Semantic keywords and topics
```

### HTTP API Usage

```bash
# Inject context via HTTP
curl -X POST "http://localhost:8000/tool/inject_conversation_context" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Help me optimize this database query"}'

# Get detailed context analysis
curl -X POST "http://localhost:8000/tool/get_conversation_context" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Context Injection Examples

### Example 1: Code Review Request
**Base Prompt:**
```
"Can you review this Python function for best practices?"
```

**Enhanced Prompt:**
```
=== CONVERSATION CONTEXT (Decision Tree Enhanced) ===
🌳 ACTIVE CONVERSATION BRANCHES:
  • coding: Working on Python backend API with FastAPI
  • testing: Implementing unit tests for database models

📋 SUMMARY: Active conversation branches: coding (3 interactions), testing (2 interactions)

🎯 KEY TOPICS: coding, testing, database, api

👤 USER PREFERENCES: Technical Level: intermediate; Preferred Topics: coding, testing; Communication Style: collaborative

📁 PROJECT CONTEXT: Files: main.py, models.py, test_models.py; Tech Stack: backend: fastapi, database: postgresql

🕒 RECENT INTERACTIONS:
  🔥 conversation_turn: Implementing user authentication system with JWT tokens...
  ⚡ tool_call: Running database migration for user table...

🔍 FREQUENT KEYWORDS: python, fastapi, database, test, api, user, authentication

=== END CONTEXT ===

Can you review this Python function for best practices?
```

### Example 2: Debugging Request
**Base Prompt:**
```
"Why is my Docker container failing to start?"
```

**Enhanced Prompt:**
```
=== CONVERSATION CONTEXT (Decision Tree Enhanced) ===
🌳 ACTIVE CONVERSATION BRANCHES:
  • deployment: Setting up Docker containers for microservices
  • debugging: Troubleshooting container startup issues

📋 SUMMARY: Active conversation branches: deployment (5 interactions), debugging (3 interactions)

🎯 KEY TOPICS: deployment, debugging, docker, microservices

👤 USER PREFERENCES: Technical Level: advanced; Preferred Topics: deployment, debugging; Communication Style: direct

📁 PROJECT CONTEXT: Files: docker-compose.yml, Dockerfile, .env; Tech Stack: devops: docker, kubernetes; backend: node, python

🕒 RECENT INTERACTIONS:
  🔥 conversation_turn: Setting up multi-service Docker environment with shared networks...
  ⚡ tool_call: Checking container logs and resource usage...

🔍 FREQUENT KEYWORDS: docker, container, service, network, environment, compose, kubernetes

=== END CONTEXT ===

Why is my Docker container failing to start?
```

## Context Types & Categories

### Topic Categories
- **coding**: Programming, algorithms, data structures
- **architecture**: System design, patterns, scalability
- **deployment**: CI/CD, containers, infrastructure
- **testing**: Unit tests, integration tests, QA
- **debugging**: Error handling, troubleshooting, monitoring
- **project_management**: Planning, collaboration, timelines
- **data_analysis**: Analytics, visualization, ML/AI
- **user_experience**: UI/UX, design, usability
- **system_administration**: Servers, security, maintenance
- **documentation**: Guides, APIs, knowledge bases

### User Preference Types
- **Technical Level**: beginner, intermediate, advanced
- **Communication Style**: direct, collaborative, analytical
- **Preferred Topics**: Most discussed technical areas
- **Project Focus**: Current project emphasis

### Project Context Types
- **Files**: Source code, configuration files
- **Technology Stack**: Frontend, backend, database, DevOps tools
- **Project Names**: Repository names, domain references
- **Architecture Patterns**: Microservices, monolith, serverless

## Performance & Optimization

### Relevance Scoring
The system uses a sophisticated scoring algorithm:

- **Time-based**: Recent interactions get higher scores (1.8x for <1 hour, 1.5x for <6 hours)
- **Interaction Type**: Conversation turns (1.5x), client requests (1.3x), agent responses (1.2x)
- **Content Length**: Longer content gets higher scores (1.3x for >200 chars, 1.2x for >100 chars)
- **Status**: Successful interactions get 1.1x boost

### Caching & Performance
- **Context Cache**: Frequently accessed contexts are cached in memory
- **Database Indexes**: Optimized queries for session and topic lookups
- **Lazy Loading**: Context is generated on-demand, not pre-computed

## Monitoring & Debugging

### Context Analysis Tool
Use `get_conversation_context()` to debug context generation:

```python
# Get detailed context breakdown
context = get_conversation_context()
print(context)
```

This shows:
- Decision tree structure
- Active conversation branches
- User preference analysis
- Project context extraction
- Semantic analysis results

### Logging & Metrics
The system logs:
- Context generation success/failure
- Decision tree building statistics
- Context injection performance
- User preference learning patterns

## Integration with Cursor

### Automatic Context Injection
The system automatically enhances every interaction by:
1. **Analyzing** recent conversation history
2. **Building** decision tree structure
3. **Extracting** relevant context
4. **Injecting** context into prompts
5. **Learning** from user responses

### Custom Context Injection
For specific use cases, manually inject context:

```python
# Get context for specific session
context = get_conversation_context(session_id="user-123")

# Inject context into custom prompt
enhanced_prompt = inject_conversation_context(
    "Help me refactor this legacy code",
    session_id="user-123"
)
```

## Future Enhancements

### Planned Features
- **Embedding-based Similarity**: Use vector embeddings for better semantic matching
- **Machine Learning**: Learn context patterns from user feedback
- **Multi-modal Context**: Support for code, images, and documents
- **Context Sharing**: Share context across team members
- **Context Templates**: Pre-defined context patterns for common scenarios

### Extensibility
The system is designed to be easily extended:
- Add new topic categories
- Implement custom relevance scoring
- Create specialized context extractors
- Integrate with external tools and APIs

## Troubleshooting

### Common Issues

**Context Not Available**
```bash
# Check database connection
python test_postgres.py

# Verify migration completed
python migrate_database.py
```

**Poor Context Quality**
```bash
# Analyze context generation
context = get_conversation_context()
print(context)

# Check interaction logging
summary = get_conversation_summary()
print(summary)
```

**Performance Issues**
```bash
# Check database indexes
# Monitor context generation time
# Verify caching is working
```

### Debug Mode
Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python main.py
```

## Support & Contributing

### Getting Help
- Check the logs for error messages
- Use `get_conversation_context()` for debugging
- Verify database schema with migration script
- Test individual components

### Contributing
- Add new topic categories
- Improve relevance scoring algorithms
- Enhance context extraction patterns
- Optimize performance and caching

---

**The Enhanced Conversation Context Injection System transforms your Cursor agent into a context-aware, personalized coding assistant that remembers your preferences, understands your projects, and provides more relevant and helpful responses.**
