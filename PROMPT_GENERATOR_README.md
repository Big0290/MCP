# 🚀 Centralized Prompt Generator System

## Overview

The **Centralized Prompt Generator System** is a unified, maintainable solution that consolidates all prompt generation logic from various files into one comprehensive system. It provides multiple enhancement strategies, better error handling, and more informative prompts.

## ✨ Key Features

### **🎯 Multiple Enhancement Strategies**

- **Comprehensive**: Full context with all available information
- **Technical**: Focused on technical details and best practices
- **Conversation**: Emphasizes conversation flow and user preferences
- **Smart**: Adaptive context based on detected patterns
- **Minimal**: Essential context for quick responses

### **🔧 Centralized Architecture**

- Single source of truth for all prompt generation
- Consistent formatting and structure across all strategies
- Easy maintenance and updates
- Unified error handling and fallbacks

### **📊 Performance & Monitoring**

- Intelligent caching with configurable TTL
- Performance metrics and statistics
- Cache hit/miss tracking
- Generation time monitoring

### **🔄 Fallback Support**

- Graceful degradation when dependencies fail
- Maintains backward compatibility
- Original implementations as fallbacks

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Prompt Generator                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Comprehensive │  │    Technical    │  │ Conversation│ │
│  │     Strategy    │  │    Strategy     │  │  Strategy   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │     Smart       │  │     Minimal     │                  │
│  │    Strategy     │  │    Strategy     │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Context Cache  │
                    │  (5 min TTL)    │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Context Data   │
                    │   Gathering     │
                    └─────────────────┘
```

## 🚀 Usage

### **Basic Usage**

```python
from prompt_generator import prompt_generator

# Generate comprehensive enhanced prompt
enhanced = prompt_generator.generate_enhanced_prompt(
    user_message="How do I set up the database?",
    context_type="comprehensive"
)

# Generate technical-focused prompt
technical = prompt_generator.generate_enhanced_prompt(
    user_message="What's the best way to optimize this query?",
    context_type="technical"
)
```

### **Convenience Functions**

```python
from prompt_generator import (
    generate_comprehensive_prompt,
    generate_technical_prompt,
    generate_conversation_prompt,
    generate_smart_prompt,
    generate_minimal_prompt
)

# Quick access to different strategies
comprehensive = generate_comprehensive_prompt("Your message here")
technical = generate_technical_prompt("Your message here")
```

### **Advanced Usage**

```python
# Force refresh context (ignore cache)
enhanced = prompt_generator.generate_enhanced_prompt(
    user_message="Your message",
    context_type="comprehensive",
    force_refresh=True
)

# Get statistics
stats = prompt_generator.get_stats()
print(f"Success rate: {stats['success_rate']}")
print(f"Cache hit rate: {stats['cache_hit_rate']}")

# Clear cache
prompt_generator.clear_cache()
```

## 🔄 Integration

### **Updated Files**

The following files now use the centralized prompt generator:

1. **`main.py`** - Main agent interaction function
2. **`smart_context_injector.py`** - Smart context injection
3. **`auto_context_wrapper.py`** - Auto context enhancement
4. **`local_mcp_server_simple.py`** - Local MCP server
5. **`cursor_agent_integration.py`** - Cursor integration

### **Fallback Behavior**

Each integration includes fallback logic:

```python
try:
    # Use centralized prompt generator
    from prompt_generator import prompt_generator
    enhanced = prompt_generator.generate_enhanced_prompt(message, "comprehensive")
except ImportError:
    # Fallback to original implementation
    enhanced = original_prompt_generation(message)
```

## 📊 Enhanced Prompt Structure

### **Comprehensive Strategy Example**

```
=== 🚀 COMPREHENSIVE ENHANCED PROMPT ===

USER MESSAGE: How do I set up the database?

=== 📊 CONTEXT INJECTION ===

🎯 CONVERSATION SUMMARY:
Current conversation state: 15 total interactions...

📝 ACTION HISTORY:
Recent actions: Database configuration, MCP server setup...

⚙️ TECH STACK:
Python 3.x, SQLite database, MCP (Model Context Protocol)...

🎯 PROJECT PLANS & OBJECTIVES:
1. Build powerful conversation tracking system ✅
2. Implement centralized prompt generation ✅
3. Create comprehensive context injection...

👤 USER PREFERENCES:
• Database Choice: SQLite over PostgreSQL
• Communication Style: Technical but friendly
• Tool Preferences: Built-in tools over external APIs

🤖 AGENT METADATA:
Friendly name: Johny, Agent ID: mcp-project-001...

🔍 PROJECT PATTERNS:
• Python development best practices
• SQLite database patterns
• Model Context Protocol integration

✅ BEST PRACTICES:
• Follow DRY (Don't Repeat Yourself) principle
• Implement proper error handling and logging
• Write comprehensive tests for critical functionality

⚠️ COMMON ISSUES & SOLUTIONS:
• Configuration and environment setup
• Dependency management and version conflicts
• Performance bottlenecks and optimization

🔄 DEVELOPMENT WORKFLOW:
• Analyze requirements and context
• Design comprehensive solution
• Implement with best practices
• Test and validate
• Deploy and monitor
• Maintain conversation continuity

📈 CONTEXT CONFIDENCE: 95.0%

=== 🎯 INSTRUCTIONS ===
Please respond to the user's message above, taking into account:

1. 📚 The current conversation context and recent interactions
2. 🎯 The specific actions and steps taken so far
3. ⚙️ The technical stack and capabilities available
4. 🎯 The project goals and objectives
5. 👤 The user's stated preferences and requirements
6. 🤖 The agent's capabilities and current state
7. 🔍 Project-specific patterns and best practices
8. ⚠️ Common issues and solutions for this context
9. 🔄 Recommended development workflow
10. 📊 The confidence level of available context

Provide a comprehensive, context-aware response that:
• Builds upon our conversation history
• Leverages project-specific knowledge
• Addresses the user's preferences
• Suggests actionable next steps
• References relevant technical details
• Maintains conversation continuity

=== 🚀 END ENHANCED PROMPT ===
```

## 🧪 Testing

### **Run Tests**

```bash
python test_prompt_generator.py
```

### **Test Coverage**

- ✅ All enhancement strategies
- ✅ Convenience functions
- ✅ Fallback behavior
- ✅ Performance monitoring
- ✅ Cache functionality
- ✅ Error handling

## 📈 Performance Metrics

### **Monitoring**

The system tracks:

- Total prompts generated
- Success/failure rates
- Average generation time
- Cache hit/miss rates
- Context confidence scores

### **Optimization**

- 5-minute cache TTL for context data
- Intelligent cache size management
- Performance tracking for optimization
- Fallback strategies for reliability

## 🔧 Configuration

### **Cache Settings**

```python
# Cache TTL (5 minutes)
CACHE_TTL_SECONDS = 300

# Maximum cache size
MAX_CACHE_SIZE = 100

# Cache cleanup threshold
CACHE_CLEANUP_THRESHOLD = 20
```

### **Enhancement Strategies**

```python
ENHANCEMENT_STRATEGIES = {
    'comprehensive': _generate_comprehensive_prompt,
    'technical': _generate_technical_prompt,
    'conversation': _generate_conversation_prompt,
    'smart': _generate_smart_prompt,
    'minimal': _generate_minimal_prompt
}
```

## 🚀 Benefits

### **For Developers**

- **Maintainability**: Single file to update prompt logic
- **Consistency**: Uniform prompt structure across all strategies
- **Debugging**: Centralized error handling and logging
- **Testing**: Easy to test all prompt generation logic

### **For Users**

- **Better Context**: More informative and structured prompts
- **Faster Responses**: Intelligent caching reduces generation time
- **Reliability**: Fallback strategies ensure system availability
- **Flexibility**: Multiple enhancement strategies for different needs

### **For System**

- **Performance**: Optimized caching and monitoring
- **Scalability**: Easy to add new enhancement strategies
- **Monitoring**: Comprehensive performance metrics
- **Stability**: Robust error handling and fallbacks

## 🔮 Future Enhancements

### **Planned Features**

- Machine learning-based context optimization
- Dynamic strategy selection based on user patterns
- Integration with external knowledge bases
- Real-time context adaptation

### **Extensibility**

- Plugin system for custom enhancement strategies
- Configurable prompt templates
- Multi-language support
- Advanced caching strategies

## 📚 API Reference

### **PromptGenerator Class**

#### **Methods**

- `generate_enhanced_prompt(user_message, context_type, force_refresh)`
- `get_stats()`
- `clear_cache()`
- `get_available_strategies()`

#### **Properties**

- `enhancement_stats`: Performance metrics
- `context_cache`: Cached prompt results
- `enhancement_strategies`: Available strategies

### **Convenience Functions**

- `generate_comprehensive_prompt(user_message)`
- `generate_technical_prompt(user_message)`
- `generate_conversation_prompt(user_message)`
- `generate_smart_prompt(user_message)`
- `generate_minimal_prompt(user_message)`

## 🎉 Conclusion

The Centralized Prompt Generator System represents a significant improvement in the MCP Conversation Intelligence System:

- **🎯 Unified**: All prompt generation logic in one place
- **🚀 Enhanced**: More informative and structured prompts
- **🔧 Maintainable**: Easy to update and extend
- **📊 Monitored**: Performance tracking and optimization
- **🔄 Reliable**: Robust fallback strategies

This system provides a solid foundation for future enhancements while maintaining backward compatibility and improving the overall user experience.
