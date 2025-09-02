# 🚀 MCP Conversation Intelligence System - Easy Setup

This guide makes it incredibly simple to set up the MCP Conversation Intelligence System in any project.

## 🎯 What This System Provides

- **Automatic Tech Stack Detection** - Detects Python, Node.js, Rust, Go, Java, PHP, .NET projects
- **Context-Aware AI Assistance** - Enhances prompts with project-specific context
- **Conversation Memory** - Remembers your interactions and preferences
- **Real-Time Learning** - Adapts to your development style over time
- **Cursor IDE Integration** - Works seamlessly with Cursor AI assistant

## 🚀 One-Click Installation

### Option 1: Super Simple (Recommended)

```bash
# Download and run the installer
curl -fsSL https://raw.githubusercontent.com/your-repo/setup_mcp_intelligence.py | python3

# Or if you have the files locally
./install_mcp_intelligence.sh
```

### Option 2: Manual Setup

```bash
# 1. Copy the setup script to your project
cp setup_mcp_intelligence.py /path/to/your/project/

# 2. Run the setup
cd /path/to/your/project
python3 setup_mcp_intelligence.py

# 3. Install dependencies
pip install -r requirements_mcp_intelligence.txt

# 4. Initialize database
python3 init_db.py

# 5. Start the system
./start_mcp_intelligence.sh
```

## 📋 What Gets Installed

### Core Files

- `smart_context_injector.py` - Automatic tech stack detection
- `prompt_generator.py` - Context-aware prompt enhancement
- `local_mcp_server_simple.py` - MCP server for AI integration
- `unified_preference_manager.py` - User preference learning
- `optimized_prompt_generator.py` - Performance-optimized prompts

### Optional Advanced Features

- `real_time_context_refiner.py` - Real-time context improvement
- `intent_driven_context_selector.py` - Smart context selection
- `enhanced_context_intelligence.py` - Advanced context analysis
- `adaptive_context_learner.py` - Machine learning for context
- `context_performance_analyzer.py` - Performance monitoring

### Database & Configuration

- `init_db.py` - Database initialization
- `mcp_intelligence_config.json` - Project configuration
- `cursor_mcp_config.json` - Cursor IDE integration
- `requirements_mcp_intelligence.txt` - Dependencies

### UI & Management

- `context_ui.py` - Web interface for conversation management
- `start_mcp_intelligence.sh` - Quick start script
- `MCP_INTELLIGENCE_USAGE.md` - Detailed usage guide

## 🎨 Supported Project Types

### Python Projects

- **Frameworks**: Django, Flask, FastAPI, Streamlit
- **Package Managers**: pip, pipenv, poetry
- **Databases**: SQLite, PostgreSQL, MySQL
- **Testing**: pytest, unittest

### Node.js Projects

- **Frameworks**: React, Vue.js, Angular, Express.js, Next.js
- **Package Managers**: npm, yarn, pnpm
- **Build Tools**: Webpack, Vite, Rollup
- **Testing**: Jest, Mocha, Cypress

### Rust Projects

- **Frameworks**: Actix Web, Rocket, Warp, Axum
- **Build Tools**: Cargo
- **Databases**: SQLx, Diesel
- **Testing**: cargo test

### Go Projects

- **Frameworks**: Gin, Gorilla Mux, Echo, Fiber
- **Build Tools**: go modules
- **Testing**: go test

### Java Projects

- **Frameworks**: Spring Boot, Hibernate
- **Build Tools**: Maven, Gradle
- **Testing**: JUnit, TestNG

### PHP Projects

- **Frameworks**: Laravel, Symfony, Slim
- **Package Managers**: Composer

### .NET Projects

- **Languages**: C#, VB.NET, F#
- **Build Tools**: MSBuild
- **Package Managers**: NuGet

## 🔧 Cursor IDE Integration

After installation, the system automatically creates a Cursor configuration:

1. **Copy the configuration**:

   ```bash
   cat cursor_mcp_config.json
   ```

2. **Add to Cursor settings**:

   - Open Cursor Settings (`Cmd+,` or `Ctrl+,`)
   - Add the configuration to your `settings.json` under `mcpServers`

3. **Restart Cursor** and enjoy enhanced AI assistance!

## 📖 Usage Examples

### Basic Usage

```python
from smart_context_injector import SmartContextInjector
from prompt_generator import prompt_generator

# Initialize with your project
injector = SmartContextInjector("/path/to/your/project")

# Detect tech stack automatically
stack_info = injector.detect_tech_stack()
print(f"Detected: {stack_info['project_type']}")

# Generate enhanced prompt
enhanced_prompt = prompt_generator.generate_enhanced_prompt(
    user_message="How do I set up authentication?",
    context_type="smart"
)
```

### Advanced Usage

```python
# Use optimized prompt generator
from optimized_prompt_generator import OptimizedPromptGenerator

generator = OptimizedPromptGenerator()
optimized_prompt = generator.generate_optimized_prompt(
    user_message="Help me debug this error",
    context_type="smart"
)

# Use real-time context refinement
from real_time_context_refiner import RealTimeContextRefiner

refiner = RealTimeContextRefiner()
refined_context, gaps = refiner.refine_context_mid_conversation(
    user_message="The API is returning 500 errors",
    current_context={},
    available_context={},
    conversation_history=[]
)
```

## 🎯 What Makes This Special

### 1. **Automatic Adaptation**

- Detects your project type automatically
- Adapts suggestions to your tech stack
- Learns your development preferences

### 2. **Context Intelligence**

- Remembers conversation history
- Provides project-specific guidance
- Maintains context across sessions

### 3. **Performance Optimized**

- Cached context for speed
- Optimized prompt generation
- Real-time context refinement

### 4. **Universal Compatibility**

- Works with any project type
- Integrates with any AI assistant
- Portable across different environments

## 🚨 Troubleshooting

### Common Issues

**"Python 3 not found"**

```bash
# Install Python 3.8+
# macOS
brew install python3

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# Windows
# Download from python.org
```

**"Dependencies failed to install"**

```bash
# Try upgrading pip first
pip install --upgrade pip

# Then install dependencies
pip install -r requirements_mcp_intelligence.txt
```

**"Database initialization failed"**

```bash
# Check permissions
ls -la data/

# Create data directory manually
mkdir -p data
chmod 755 data
```

**"Cursor integration not working"**

```bash
# Check the configuration
cat cursor_mcp_config.json

# Verify the path is correct
python3 -c "import sys; print(sys.executable)"
```

### Getting Help

1. **Check the logs**: `tail -f logs/mcp_intelligence.log`
2. **Read the usage guide**: `cat MCP_INTELLIGENCE_USAGE.md`
3. **Test the installation**: `python3 -c "from smart_context_injector import SmartContextInjector; print('OK')"`

## 🎉 Success

Once installed, you'll have:

- ✅ **Intelligent AI assistance** that understands your project
- ✅ **Automatic tech stack detection** for any project type
- ✅ **Context-aware responses** that build on conversation history
- ✅ **User preference learning** that adapts to your style
- ✅ **Real-time context refinement** for optimal responses
- ✅ **Cursor IDE integration** for seamless AI assistance

Your AI assistant is now **project-aware** and will provide much more relevant and helpful responses! 🚀
