# Session Persistence for Conversation Tracking

This document explains the enhanced session persistence system that allows conversation tracking to work across conversation changes and system restarts.

## Overview

The conversation tracking system now includes persistent session management that:

- **Survives system restarts** - Sessions are saved to disk and automatically restored
- **Maintains context across conversations** - User preferences, project context, and conversation history persist
- **Supports session resumption** - Users can resume previous conversations using session IDs
- **Provides session management tools** - List, export, merge, and cleanup sessions

## Key Components

### 1. Session Manager (`session_manager.py`)

The core component that handles persistent session storage and retrieval:

- **PersistentSession**: Data class containing session information
- **SessionManager**: Main class for session operations
- **Disk persistence**: Sessions are automatically saved to `./data/sessions/` directory
- **Automatic cleanup**: Expired sessions (7+ days inactive) are automatically removed

### 2. Enhanced Interaction Logger

Updated to work with the session manager:

- **Session resumption**: Can resume existing sessions by ID
- **Automatic persistence**: Session data is automatically saved
- **Context integration**: Updates session context when logging interactions

### 3. New MCP Tools

Added new tools for session management:

- `resume_session(session_id, user_id)`: Resume an existing session
- `list_sessions(user_id)`: List all active sessions
- `export_session(session_id)`: Export complete session data
- `merge_sessions(primary_id, secondary_id)`: Merge two sessions
- `cleanup_sessions()`: Clean up expired sessions

## How It Works

### Session Creation and Persistence

1. **Initial Creation**: When a user starts a conversation, a new session is created
2. **Automatic Saving**: Session data is automatically saved to disk after each interaction
3. **Context Updates**: Conversation context, user preferences, and topics are tracked
4. **Activity Tracking**: Last activity time and interaction counts are maintained

### Session Resumption

1. **Session ID**: Each session has a unique ID that can be used to resume it
2. **Automatic Loading**: Sessions are automatically loaded from disk on system startup
3. **Context Restoration**: All previous context, preferences, and history are restored
4. **Seamless Continuation**: Users can continue conversations exactly where they left off

### Data Persistence

- **Session Files**: Stored in `./data/sessions/` as JSON files
- **Database Integration**: Sessions are also stored in the database for querying
- **Automatic Backup**: Session data is automatically backed up to disk
- **Error Recovery**: Corrupted session files are automatically detected and removed

## Usage Examples

### Resuming a Session

```python
# Resume an existing session by ID
session_id = "abc123def456"
resumed_id = session_manager.create_or_resume_session(
    user_id="user123", 
    session_id=session_id
)

if resumed_id == session_id:
    print("Session resumed successfully!")
else:
    print("Failed to resume session")
```

### Listing Active Sessions

```python
# Get all active sessions
sessions = session_manager.list_active_sessions()
for session in sessions:
    print(f"Session: {session['session_id']}")
    print(f"User: {session['user_id']}")
    print(f"Interactions: {session['total_interactions']}")
```

### Exporting Session Data

```python
# Export complete session data
export_data = session_manager.export_session_data(session_id)
if export_data:
    # Save to file
    with open(f"session_{session_id}.json", "w") as f:
        json.dump(export_data, f, indent=2)
```

## MCP Tool Usage

### Resume Session

```bash
# Resume a specific session
resume_session("abc123def456", "user123")
```

### List Sessions

```bash
# List all sessions
list_sessions()

# List sessions for specific user
list_sessions("user123")
```

### Export Session

```bash
# Export session data
export_session("abc123def456")
```

### Merge Sessions

```bash
# Merge secondary session into primary
merge_sessions("primary123", "secondary456")
```

### Cleanup Sessions

```bash
# Clean up expired sessions
cleanup_sessions()
```

## Configuration

### Session Expiration

Sessions automatically expire after 7 days of inactivity. This can be modified in `session_manager.py`:

```python
def _is_session_valid(self, session: PersistentSession) -> bool:
    # Sessions expire after 7 days of inactivity
    max_age = timedelta(days=7)  # Change this value
    return datetime.utcnow() - session.last_activity < max_age
```

### Storage Location

Session files are stored in `./data/sessions/` by default. This can be modified in the SessionManager constructor:

```python
def __init__(self):
    # ...
    self._session_file_dir = Path("./data/sessions")  # Change this path
    # ...
```

## Benefits

### For Users

- **Continuous Context**: Maintain conversation context across restarts
- **No Data Loss**: Important conversations and preferences are preserved
- **Easy Resumption**: Simple session ID to continue previous work
- **Personalization**: User preferences and learning patterns are maintained

### For Developers

- **Debugging**: Complete conversation history for troubleshooting
- **Analytics**: Session data for user behavior analysis
- **Backup**: Automatic backup of important conversations
- **Integration**: Easy integration with other tools and systems

### For System Administrators

- **Monitoring**: Track active sessions and system usage
- **Maintenance**: Automatic cleanup of expired sessions
- **Storage Management**: Efficient storage with automatic expiration
- **Recovery**: Easy recovery from system failures

## Testing

Run the test script to verify session persistence:

```bash
python test_session_persistence.py
```

This will:
1. Create test sessions
2. Update session data
3. Test persistence to disk
4. Simulate session resumption
5. Test session merging

## Troubleshooting

### Common Issues

1. **Session Not Found**: Check if session ID is correct and session hasn't expired
2. **Permission Errors**: Ensure write access to `./data/sessions/` directory
3. **Corrupted Files**: Corrupted session files are automatically detected and removed
4. **Database Issues**: Sessions are stored both on disk and in database for redundancy

### Debug Information

Enable debug logging by setting log level in config:

```python
LOG_LEVEL = "DEBUG"
```

Session manager operations are logged with descriptive messages and emojis for easy identification.

## Future Enhancements

- **Session Encryption**: Encrypt sensitive session data
- **Cloud Sync**: Sync sessions across multiple devices
- **Advanced Analytics**: Session pattern analysis and insights
- **API Integration**: REST API for session management
- **Backup Scheduling**: Configurable backup schedules and retention policies

## Conclusion

The session persistence system provides robust, reliable conversation tracking that survives system restarts and maintains context across conversations. This enables users to have continuous, personalized experiences while providing developers and administrators with powerful tools for monitoring and management.
