#!/usr/bin/env python3
"""
MCP Function Analyzer Tool

This module provides MCP tools for on-demand function and class analysis.
It integrates the standalone function analyzer with the MCP system.
"""

import logging
from typing import Dict, List, Any, Optional
from standalone_function_analyzer import get_function_analyzer, analyze_project_functions, search_functions, get_function_details

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_project_functions_mcp(project_path: str = ".", force_refresh: bool = False) -> str:
    """
    MCP tool to analyze all functions and classes in a project.
    
    Args:
        project_path: Path to the project directory (default: current directory)
        force_refresh: Force re-analysis even if already analyzed
        
    Returns:
        Formatted string with analysis results
    """
    try:
        logger.info(f"🔍 Analyzing project functions: {project_path}")
        
        analyzer = get_function_analyzer(project_path)
        results = analyzer.analyze_project(force_refresh)
        
        # Format the results
        output = []
        output.append("=== 🔧 PROJECT FUNCTION ANALYSIS ===")
        output.append(f"📊 Total Functions: {results['total_functions']}")
        output.append(f"🏗️ Total Classes: {results['total_classes']}")
        
        # Group functions by file
        files_with_functions = {}
        for func_data in results['functions'].values():
            file_path = func_data['file']
            if file_path not in files_with_functions:
                files_with_functions[file_path] = []
            files_with_functions[file_path].append(func_data)
        
        # Show top files by function count
        top_files = sorted(files_with_functions.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        
        output.append("\n📁 Top Files by Function Count:")
        for file_path, functions in top_files:
            output.append(f"  📄 {file_path}: {len(functions)} functions")
        
        # Show sample functions
        if results['functions']:
            output.append("\n📋 Sample Functions:")
            for i, (name, func_data) in enumerate(list(results['functions'].items())[:10]):
                args_str = ", ".join(func_data['args'][:3]) if func_data['args'] else "no args"
                if len(func_data['args']) > 3:
                    args_str += "..."
                
                output.append(f"  {i+1}. {func_data['name']}({args_str})")
                output.append(f"     📁 File: {func_data['file']}:{func_data['line']}")
                if func_data['docstring'] and func_data['docstring'] != "No docstring":
                    doc_preview = func_data['docstring'][:100] + "..." if len(func_data['docstring']) > 100 else func_data['docstring']
                    output.append(f"     💬 {doc_preview}")
                output.append("")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"❌ Function analysis failed: {e}")
        return f"❌ Function analysis failed: {str(e)}"

def search_functions_mcp(query: str, project_path: str = ".") -> str:
    """
    MCP tool to search for functions by name, docstring, or file.
    
    Args:
        query: Search query
        project_path: Path to the project directory (default: current directory)
        
    Returns:
        Formatted string with search results
    """
    try:
        logger.info(f"🔍 Searching functions: '{query}' in {project_path}")
        
        functions = search_functions(query, project_path)
        
        if not functions:
            return f"❌ No functions found matching '{query}'"
        
        output = []
        output.append(f"=== 🔍 FUNCTION SEARCH RESULTS: '{query}' ===")
        output.append(f"📊 Found {len(functions)} matching functions")
        output.append("")
        
        for i, func_data in enumerate(functions, 1):
            args_str = ", ".join(func_data['args'][:3]) if func_data['args'] else "no args"
            if len(func_data['args']) > 3:
                args_str += "..."
            
            output.append(f"{i}. {func_data['name']}({args_str})")
            output.append(f"   📁 File: {func_data['file']}:{func_data['line']}")
            
            if func_data['is_async']:
                output.append("   ⚡ Async function")
            if func_data['is_class_method']:
                output.append(f"   🏛️ Method of class: {func_data['class_name']}")
            
            if func_data['docstring'] and func_data['docstring'] != "No docstring":
                doc_preview = func_data['docstring'][:150] + "..." if len(func_data['docstring']) > 150 else func_data['docstring']
                output.append(f"   💬 {doc_preview}")
            
            output.append("")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"❌ Function search failed: {e}")
        return f"❌ Function search failed: {str(e)}"

def get_function_details_mcp(function_name: str, project_path: str = ".") -> str:
    """
    MCP tool to get detailed information about a specific function.
    
    Args:
        function_name: Name of the function to analyze
        project_path: Path to the project directory (default: current directory)
        
    Returns:
        Formatted string with function details
    """
    try:
        logger.info(f"🔍 Getting function details: '{function_name}' in {project_path}")
        
        func_data = get_function_details(function_name, project_path)
        
        if not func_data:
            return f"❌ Function '{function_name}' not found"
        
        output = []
        output.append(f"=== 🔧 FUNCTION DETAILS: {function_name} ===")
        output.append("")
        
        # Basic info
        output.append(f"📝 Name: {func_data['name']}")
        output.append(f"📁 File: {func_data['file']}")
        output.append(f"📍 Line: {func_data['line']}")
        
        # Arguments
        if func_data['args']:
            output.append(f"🔧 Arguments: {', '.join(func_data['args'])}")
        else:
            output.append("🔧 Arguments: None")
        
        # Function type
        if func_data['is_async']:
            output.append("⚡ Type: Async function")
        elif func_data['is_class_method']:
            output.append(f"🏛️ Type: Method of class '{func_data['class_name']}'")
        else:
            output.append("🔧 Type: Regular function")
        
        # Docstring
        if func_data['docstring'] and func_data['docstring'] != "No docstring":
            output.append("")
            output.append("📖 Documentation:")
            output.append(func_data['docstring'])
        else:
            output.append("")
            output.append("📖 Documentation: No docstring available")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"❌ Function details retrieval failed: {e}")
        return f"❌ Function details retrieval failed: {str(e)}"

def get_functions_by_file_mcp(file_path: str, project_path: str = ".") -> str:
    """
    MCP tool to get all functions in a specific file.
    
    Args:
        file_path: Path to the file to analyze
        project_path: Path to the project directory (default: current directory)
        
    Returns:
        Formatted string with functions in the file
    """
    try:
        logger.info(f"🔍 Getting functions in file: '{file_path}' in {project_path}")
        
        analyzer = get_function_analyzer(project_path)
        functions = analyzer.get_functions_by_file(file_path)
        
        if not functions:
            return f"❌ No functions found in file '{file_path}'"
        
        output = []
        output.append(f"=== 📁 FUNCTIONS IN FILE: {file_path} ===")
        output.append(f"📊 Found {len(functions)} functions")
        output.append("")
        
        for i, func in enumerate(functions, 1):
            args_str = ", ".join(func.args[:3]) if func.args else "no args"
            if len(func.args) > 3:
                args_str += "..."
            
            output.append(f"{i}. {func.name}({args_str})")
            output.append(f"   📍 Line: {func.line}")
            
            if func.is_async:
                output.append("   ⚡ Async function")
            if func.is_class_method:
                output.append(f"   🏛️ Method of class: {func.class_name}")
            
            if func.docstring and func.docstring != "No docstring":
                doc_preview = func.docstring[:100] + "..." if len(func.docstring) > 100 else func.docstring
                output.append(f"   💬 {doc_preview}")
            
            output.append("")
        
        return "\n".join(output)
        
    except Exception as e:
        logger.error(f"❌ File function analysis failed: {e}")
        return f"❌ File function analysis failed: {str(e)}"

def get_project_summary_mcp(project_path: str = ".") -> str:
    """
    MCP tool to get a compact project summary.
    
    Args:
        project_path: Path to the project directory (default: current directory)
        
    Returns:
        Formatted string with project summary
    """
    try:
        logger.info(f"🔍 Getting project summary: {project_path}")
        
        analyzer = get_function_analyzer(project_path)
        summary = analyzer.get_project_summary()
        
        return summary
        
    except Exception as e:
        logger.error(f"❌ Project summary failed: {e}")
        return f"❌ Project summary failed: {str(e)}"

# MCP Tool Registry
MCP_FUNCTION_TOOLS = {
    "analyze_project_functions": {
        "description": "Analyze all functions and classes in a project",
        "function": analyze_project_functions_mcp,
        "parameters": {
            "project_path": {"type": "string", "default": ".", "description": "Path to project directory"},
            "force_refresh": {"type": "boolean", "default": False, "description": "Force re-analysis"}
        }
    },
    "search_functions": {
        "description": "Search for functions by name, docstring, or file",
        "function": search_functions_mcp,
        "parameters": {
            "query": {"type": "string", "description": "Search query"},
            "project_path": {"type": "string", "default": ".", "description": "Path to project directory"}
        }
    },
    "get_function_details": {
        "description": "Get detailed information about a specific function",
        "function": get_function_details_mcp,
        "parameters": {
            "function_name": {"type": "string", "description": "Name of the function"},
            "project_path": {"type": "string", "default": ".", "description": "Path to project directory"}
        }
    },
    "get_functions_by_file": {
        "description": "Get all functions in a specific file",
        "function": get_functions_by_file_mcp,
        "parameters": {
            "file_path": {"type": "string", "description": "Path to the file"},
            "project_path": {"type": "string", "default": ".", "description": "Path to project directory"}
        }
    },
    "get_project_summary": {
        "description": "Get a compact project summary",
        "function": get_project_summary_mcp,
        "parameters": {
            "project_path": {"type": "string", "default": ".", "description": "Path to project directory"}
        }
    }
}

def list_function_tools() -> str:
    """List all available function analysis tools"""
    output = []
    output.append("=== 🔧 AVAILABLE FUNCTION ANALYSIS TOOLS ===")
    output.append("")
    
    for tool_name, tool_info in MCP_FUNCTION_TOOLS.items():
        output.append(f"🔧 {tool_name}")
        output.append(f"   📝 {tool_info['description']}")
        output.append(f"   📋 Parameters:")
        for param_name, param_info in tool_info['parameters'].items():
            param_type = param_info['type']
            param_desc = param_info['description']
            if 'default' in param_info:
                param_default = param_info['default']
                output.append(f"     - {param_name} ({param_type}, default: {param_default}): {param_desc}")
            else:
                output.append(f"     - {param_name} ({param_type}): {param_desc}")
        output.append("")
    
    return "\n".join(output)

if __name__ == "__main__":
    # Test the MCP tools
    print("🔧 Testing MCP Function Analysis Tools")
    print("=" * 50)
    
    # Test project summary
    print("\n1. Project Summary:")
    print(get_project_summary_mcp())
    
    # Test function search
    print("\n2. Function Search (test):")
    print(search_functions_mcp("test"))
    
    # Test function details (if any functions exist)
    print("\n3. Function Details (main):")
    print(get_function_details_mcp("main"))
    
    print("\n✅ MCP Function Analysis Tools test complete!")
