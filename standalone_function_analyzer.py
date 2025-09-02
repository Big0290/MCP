#!/usr/bin/env python3
"""
Standalone Function Analyzer Tool

This tool provides on-demand function and class analysis for the MCP system.
It can be called by agents when they need detailed function information
without including it in every prompt.
"""

import os
import ast
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FunctionInfo:
    """Information about a function"""
    name: str
    file: str
    line: int
    args: List[str]
    docstring: str
    is_async: bool = False
    is_class_method: bool = False
    class_name: Optional[str] = None

@dataclass
class ClassInfo:
    """Information about a class"""
    name: str
    file: str
    line: int
    docstring: str
    methods: List[str]
    parent_classes: List[str]

class StandaloneFunctionAnalyzer:
    """
    Standalone function analyzer that can be called on-demand
    to provide detailed function and class information.
    """
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.functions: Dict[str, FunctionInfo] = {}
        self.classes: Dict[str, ClassInfo] = {}
        self._analyzed = False
    
    def analyze_project(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Analyze the entire project for functions and classes.
        
        Args:
            force_refresh: Force re-analysis even if already analyzed
            
        Returns:
            Dictionary containing analysis results
        """
        if self._analyzed and not force_refresh:
            return self._get_analysis_summary()
        
        logger.info(f"🔍 Analyzing project: {self.project_path}")
        
        # Clear previous analysis
        self.functions.clear()
        self.classes.clear()
        
        # Find all Python files
        python_files = self._find_python_files()
        logger.info(f"📁 Found {len(python_files)} Python files")
        
        # Analyze each file
        for file_path in python_files:
            try:
                self._analyze_file(file_path)
            except Exception as e:
                logger.warning(f"⚠️ Failed to analyze {file_path}: {e}")
        
        self._analyzed = True
        logger.info(f"✅ Analysis complete: {len(self.functions)} functions, {len(self.classes)} classes")
        
        return self._get_analysis_summary()
    
    def get_functions_by_file(self, file_path: str) -> List[FunctionInfo]:
        """Get all functions in a specific file"""
        if not self._analyzed:
            self.analyze_project()
        
        return [func for func in self.functions.values() if func.file == file_path]
    
    def get_functions_by_name(self, name_pattern: str) -> List[FunctionInfo]:
        """Get functions matching a name pattern"""
        if not self._analyzed:
            self.analyze_project()
        
        return [func for func in self.functions.values() if name_pattern.lower() in func.name.lower()]
    
    def get_classes_by_file(self, file_path: str) -> List[ClassInfo]:
        """Get all classes in a specific file"""
        if not self._analyzed:
            self.analyze_project()
        
        return [cls for cls in self.classes.values() if cls.file == file_path]
    
    def get_function_details(self, function_name: str) -> Optional[FunctionInfo]:
        """Get detailed information about a specific function"""
        if not self._analyzed:
            self.analyze_project()
        
        return self.functions.get(function_name)
    
    def get_class_details(self, class_name: str) -> Optional[ClassInfo]:
        """Get detailed information about a specific class"""
        if not self._analyzed:
            self.analyze_project()
        
        return self.classes.get(class_name)
    
    def search_functions(self, query: str) -> List[FunctionInfo]:
        """Search functions by name, docstring, or file"""
        if not self._analyzed:
            self.analyze_project()
        
        query_lower = query.lower()
        results = []
        
        for func in self.functions.values():
            if (query_lower in func.name.lower() or 
                query_lower in func.docstring.lower() or 
                query_lower in func.file.lower()):
                results.append(func)
        
        return results
    
    def get_project_summary(self) -> str:
        """Get a compact project summary"""
        if not self._analyzed:
            self.analyze_project()
        
        summary = []
        summary.append("=== 🔧 PROJECT FUNCTION ANALYSIS ===")
        summary.append(f"📊 Total Functions: {len(self.functions)}")
        summary.append(f"🏗️ Total Classes: {len(self.classes)}")
        
        # Group by file
        files_with_functions = {}
        for func in self.functions.values():
            if func.file not in files_with_functions:
                files_with_functions[func.file] = []
            files_with_functions[func.file].append(func)
        
        # Show top files by function count
        top_files = sorted(files_with_functions.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        
        summary.append("\n📁 Top Files by Function Count:")
        for file_path, functions in top_files:
            summary.append(f"  📄 {file_path}: {len(functions)} functions")
        
        return "\n".join(summary)
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        
        for root, dirs, files in os.walk(self.project_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'env', 'ui_env']]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        return python_files
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            relative_path = str(file_path.relative_to(self.project_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self._analyze_function(node, relative_path)
                elif isinstance(node, ast.AsyncFunctionDef):
                    self._analyze_function(node, relative_path, is_async=True)
                elif isinstance(node, ast.ClassDef):
                    self._analyze_class(node, relative_path)
        
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse {file_path}: {e}")
    
    def _analyze_function(self, node: ast.FunctionDef, file_path: str, is_async: bool = False):
        """Analyze a function node"""
        # Extract arguments
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Extract docstring
        docstring = ast.get_docstring(node) or "No docstring"
        
        # Check if it's a class method
        is_class_method = False
        class_name = None
        if hasattr(node, 'parent') and isinstance(node.parent, ast.ClassDef):
            is_class_method = True
            class_name = node.parent.name
        
        func_info = FunctionInfo(
            name=node.name,
            file=file_path,
            line=node.lineno,
            args=args,
            docstring=docstring,
            is_async=is_async,
            is_class_method=is_class_method,
            class_name=class_name
        )
        
        self.functions[node.name] = func_info
    
    def _analyze_class(self, node: ast.ClassDef, file_path: str):
        """Analyze a class node"""
        # Extract docstring
        docstring = ast.get_docstring(node) or "No docstring"
        
        # Extract method names
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)
        
        # Extract parent classes
        parent_classes = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                parent_classes.append(base.id)
        
        class_info = ClassInfo(
            name=node.name,
            file=file_path,
            line=node.lineno,
            docstring=docstring,
            methods=methods,
            parent_classes=parent_classes
        )
        
        self.classes[node.name] = class_info
    
    def _get_analysis_summary(self) -> Dict[str, Any]:
        """Get a summary of the analysis results"""
        return {
            "total_functions": len(self.functions),
            "total_classes": len(self.classes),
            "functions": {name: {
                "name": func.name,
                "file": func.file,
                "line": func.line,
                "args": func.args,
                "docstring": func.docstring,
                "is_async": func.is_async,
                "is_class_method": func.is_class_method,
                "class_name": func.class_name
            } for name, func in self.functions.items()},
            "classes": {name: {
                "name": cls.name,
                "file": cls.file,
                "line": cls.line,
                "docstring": cls.docstring,
                "methods": cls.methods,
                "parent_classes": cls.parent_classes
            } for name, cls in self.classes.items()}
        }

# Global instance for easy access
_analyzer_instance = None

def get_function_analyzer(project_path: str = ".") -> StandaloneFunctionAnalyzer:
    """Get or create the global function analyzer instance"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = StandaloneFunctionAnalyzer(project_path)
    return _analyzer_instance

def analyze_project_functions(project_path: str = ".", force_refresh: bool = False) -> Dict[str, Any]:
    """Convenience function to analyze project functions"""
    analyzer = get_function_analyzer(project_path)
    return analyzer.analyze_project(force_refresh)

def search_functions(query: str, project_path: str = ".") -> List[Dict[str, Any]]:
    """Convenience function to search functions"""
    analyzer = get_function_analyzer(project_path)
    functions = analyzer.search_functions(query)
    return [{
        "name": func.name,
        "file": func.file,
        "line": func.line,
        "args": func.args,
        "docstring": func.docstring,
        "is_async": func.is_async,
        "is_class_method": func.is_class_method,
        "class_name": func.class_name
    } for func in functions]

def get_function_details(function_name: str, project_path: str = ".") -> Optional[Dict[str, Any]]:
    """Convenience function to get function details"""
    analyzer = get_function_analyzer(project_path)
    func = analyzer.get_function_details(function_name)
    if func:
        return {
            "name": func.name,
            "file": func.file,
            "line": func.line,
            "args": func.args,
            "docstring": func.docstring,
            "is_async": func.is_async,
            "is_class_method": func.is_class_method,
            "class_name": func.class_name
        }
    return None

if __name__ == "__main__":
    # Test the analyzer
    analyzer = StandaloneFunctionAnalyzer()
    results = analyzer.analyze_project()
    
    print("🔍 Function Analysis Results:")
    print(f"Total Functions: {results['total_functions']}")
    print(f"Total Classes: {results['total_classes']}")
    
    # Show some example functions
    if results['functions']:
        print("\n📋 Sample Functions:")
        for i, (name, func) in enumerate(list(results['functions'].items())[:5]):
            print(f"  {i+1}. {func['name']}() in {func['file']}")
            print(f"     Args: {func['args']}")
            print(f"     Doc: {func['docstring'][:100]}...")
            print()
