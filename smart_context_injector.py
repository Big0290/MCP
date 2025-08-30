#!/usr/bin/env python3
"""
Smart Context Injector with Automatic Stack Detection
Automatically detects project tech stacks and injects relevant context
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml
import toml
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartContextInjector:
    """
    Smart context injector that automatically detects tech stacks
    and injects relevant context for any project type
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = project_path or os.getcwd()
        self.detected_stack = None
        self.project_context = {}
        self.user_preferences = self._load_user_preferences()
        
    def _load_user_preferences(self) -> Dict:
        """Load portable user preferences that work across all projects"""
        return {
            "development_style": "simple yet powerful solutions",
            "database_preference": "local SQLite over PostgreSQL",
            "logging_approach": "comprehensive logging",
            "architecture_choices": "structured data models, MCP protocol",
            "problem_solving_approach": "focus on conversation context and memory",
            "communication_style": "clear, detailed explanations",
            "tool_preferences": "local development, comprehensive logging",
            "learning_patterns": "iterative improvement with context awareness"
        }
    
    def detect_tech_stack(self) -> Dict:
        """Automatically detect the tech stack of the current project"""
        logger.info(f"🔍 Detecting tech stack in: {self.project_path}")
        
        # Initialize detection results
        stack_info = {
            "project_type": "unknown",
            "primary_language": "unknown",
            "frameworks": [],
            "databases": [],
            "build_tools": [],
            "package_managers": [],
            "deployment": [],
            "testing": [],
            "confidence_score": 0.0
        }
        
        try:
            # Check for common project files
            project_files = self._scan_project_files()
            
            # Detect based on file patterns
            if self._is_python_project(project_files):
                stack_info.update(self._detect_python_stack(project_files))
            elif self._is_node_project(project_files):
                stack_info.update(self._detect_node_stack(project_files))
            elif self._is_rust_project(project_files):
                stack_info.update(self._detect_rust_stack(project_files))
            elif self._is_go_project(project_files):
                stack_info.update(self._detect_go_stack(project_files))
            elif self._is_java_project(project_files):
                stack_info.update(self._detect_java_stack(project_files))
            elif self._is_php_project(project_files):
                stack_info.update(self._detect_php_stack(project_files))
            elif self._is_dotnet_project(project_files):
                stack_info.update(self._detect_dotnet_stack(project_files))
            
            # Calculate confidence score
            stack_info["confidence_score"] = self._calculate_confidence(stack_info, project_files)
            
            self.detected_stack = stack_info
            logger.info(f"✅ Detected stack: {stack_info['project_type']} ({stack_info['primary_language']})")
            
        except Exception as e:
            logger.error(f"❌ Error detecting tech stack: {e}")
            stack_info["project_type"] = "error"
            stack_info["confidence_score"] = 0.0
        
        return stack_info
    
    def _scan_project_files(self) -> List[str]:
        """Scan project directory for relevant files"""
        files = []
        try:
            for root, dirs, filenames in os.walk(self.project_path):
                # Skip common directories to ignore
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'ui_env', 'target', 'build']]
                
                for filename in filenames:
                    if filename in [
                        # Python
                        'requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', 'poetry.lock',
                        # Node.js
                        'package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
                        # Rust
                        'Cargo.toml', 'Cargo.lock',
                        # Go
                        'go.mod', 'go.sum',
                        # Java
                        'pom.xml', 'build.gradle', 'gradle.properties',
                        # PHP
                        'composer.json', 'composer.lock',
                        # .NET
                        '*.csproj', '*.vbproj', '*.fsproj', '*.sln',
                        # Docker
                        'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
                        # Config files
                        '.env', 'config.yml', 'config.yaml', 'tsconfig.json', 'webpack.config.js'
                    ]:
                        files.append(os.path.join(root, filename))
        except Exception as e:
            logger.error(f"Error scanning project files: {e}")
        
        return files
    
    def _is_python_project(self, files: List[str]) -> bool:
        """Check if this is a Python project"""
        python_indicators = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', 'poetry.lock']
        return any(any(indicator in f for indicator in python_indicators) for f in files)
    
    def _is_node_project(self, files: List[str]) -> bool:
        """Check if this is a Node.js project"""
        node_indicators = ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml']
        return any(any(indicator in f for indicator in node_indicators) for f in files)
    
    def _is_rust_project(self, files: List[str]) -> bool:
        """Check if this is a Rust project"""
        rust_indicators = ['Cargo.toml', 'Cargo.lock']
        return any(any(indicator in f for indicator in rust_indicators) for f in files)
    
    def _is_go_project(self, files: List[str]) -> bool:
        """Check if this is a Go project"""
        go_indicators = ['go.mod', 'go.sum']
        return any(any(indicator in f for indicator in go_indicators) for f in files)
    
    def _is_java_project(self, files: List[str]) -> bool:
        """Check if this is a Java project"""
        java_indicators = ['pom.xml', 'build.gradle', 'gradle.properties']
        return any(any(indicator in f for indicator in java_indicators) for f in files)
    
    def _is_php_project(self, files: List[str]) -> bool:
        """Check if this is a PHP project"""
        php_indicators = ['composer.json', 'composer.lock']
        return any(any(indicator in f for indicator in php_indicators) for f in files)
    
    def _is_dotnet_project(self, files: List[str]) -> bool:
        """Check if this is a .NET project"""
        dotnet_indicators = ['.csproj', '.vbproj', '.fsproj', '.sln']
        return any(any(indicator in f for indicator in dotnet_indicators) for f in files)
    
    def _detect_python_stack(self, files: List[str]) -> Dict:
        """Detect Python-specific tech stack"""
        stack = {
            "project_type": "python_project",
            "primary_language": "Python",
            "frameworks": [],
            "databases": [],
            "build_tools": [],
            "package_managers": [],
            "deployment": [],
            "testing": []
        }
        
        # Check for frameworks
        if any('django' in f.lower() for f in files):
            stack["frameworks"].append("Django")
        if any('flask' in f.lower() for f in files):
            stack["frameworks"].append("Flask")
        if any('fastapi' in f.lower() for f in files):
            stack["frameworks"].append("FastAPI")
        if any('streamlit' in f.lower() for f in files):
            stack["frameworks"].append("Streamlit")
        
        # Check for package managers
        if any('requirements.txt' in f for f in files):
            stack["package_managers"].append("pip")
        if any('Pipfile' in f for f in files):
            stack["package_managers"].append("pipenv")
        if any('poetry.lock' in f for f in files):
            stack["package_managers"].append("poetry")
        
        # Check for databases
        if any('sqlite' in f.lower() for f in files):
            stack["databases"].append("SQLite")
        if any('postgres' in f.lower() for f in files):
            stack["databases"].append("PostgreSQL")
        if any('mysql' in f.lower() for f in files):
            stack["databases"].append("MySQL")
        
        return stack
    
    def _detect_node_stack(self, files: List[str]) -> Dict:
        """Detect Node.js-specific tech stack"""
        stack = {
            "project_type": "node_project",
            "primary_language": "JavaScript/TypeScript",
            "frameworks": [],
            "databases": [],
            "build_tools": [],
            "package_managers": [],
            "deployment": [],
            "testing": []
        }
        
        # Read package.json for detailed info
        package_json_path = next((f for f in files if 'package.json' in f), None)
        if package_json_path:
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    
                # Check for frameworks
                dependencies = package_data.get('dependencies', {})
                dev_dependencies = package_data.get('devDependencies', {})
                
                if 'react' in dependencies or 'react' in dev_dependencies:
                    stack["frameworks"].append("React")
                if 'vue' in dependencies or 'vue' in dev_dependencies:
                    stack["frameworks"].append("Vue.js")
                if 'angular' in dependencies or 'angular' in dev_dependencies:
                    stack["frameworks"].append("Angular")
                if 'express' in dependencies:
                    stack["frameworks"].append("Express.js")
                if 'next' in dependencies:
                    stack["frameworks"].append("Next.js")
                if 'nuxt' in dependencies:
                    stack["frameworks"].append("Nuxt.js")
                
                # Check for databases
                if 'mongoose' in dependencies:
                    stack["databases"].append("MongoDB")
                if 'pg' in dependencies or 'postgres' in dependencies:
                    stack["databases"].append("PostgreSQL")
                if 'mysql2' in dependencies:
                    stack["databases"].append("MySQL")
                if 'sqlite3' in dependencies:
                    stack["databases"].append("SQLite")
                
                # Check for build tools
                if 'webpack' in dev_dependencies:
                    stack["build_tools"].append("Webpack")
                if 'vite' in dev_dependencies:
                    stack["build_tools"].append("Vite")
                if 'rollup' in dev_dependencies:
                    stack["build_tools"].append("Rollup")
                
                # Check for testing
                if 'jest' in dev_dependencies:
                    stack["testing"].append("Jest")
                if 'mocha' in dev_dependencies:
                    stack["testing"].append("Mocha")
                if 'cypress' in dev_dependencies:
                    stack["testing"].append("Cypress")
                    
            except Exception as e:
                logger.error(f"Error reading package.json: {e}")
        
        # Check for package managers
        if any('package-lock.json' in f for f in files):
            stack["package_managers"].append("npm")
        if any('yarn.lock' in f for f in files):
            stack["package_managers"].append("yarn")
        if any('pnpm-lock.yaml' in f for f in files):
            stack["package_managers"].append("pnpm")
        
        return stack
    
    def _detect_rust_stack(self, files: List[str]) -> Dict:
        """Detect Rust-specific tech stack"""
        stack = {
            "project_type": "rust_project",
            "primary_language": "Rust",
            "frameworks": [],
            "databases": [],
            "build_tools": ["Cargo"],
            "package_managers": ["Cargo"],
            "deployment": [],
            "testing": []
        }
        
        # Read Cargo.toml for dependencies
        cargo_path = next((f for f in files if 'Cargo.toml' in f), None)
        if cargo_path:
            try:
                with open(cargo_path, 'r') as f:
                    cargo_content = f.read()
                    
                # Check for web frameworks
                if 'actix-web' in cargo_content:
                    stack["frameworks"].append("Actix Web")
                if 'rocket' in cargo_content:
                    stack["frameworks"].append("Rocket")
                if 'warp' in cargo_content:
                    stack["frameworks"].append("Warp")
                if 'axum' in cargo_content:
                    stack["frameworks"].append("Axum")
                
                # Check for databases
                if 'sqlx' in cargo_content:
                    stack["databases"].append("SQL (via SQLx)")
                if 'diesel' in cargo_content:
                    stack["databases"].append("SQL (via Diesel)")
                if 'mongodb' in cargo_content:
                    stack["databases"].append("MongoDB")
                    
            except Exception as e:
                logger.error(f"Error reading Cargo.toml: {e}")
        
        return stack
    
    def _detect_go_stack(self, files: List[str]) -> Dict:
        """Detect Go-specific tech stack"""
        stack = {
            "project_type": "go_project",
            "primary_language": "Go",
            "frameworks": [],
            "databases": [],
            "build_tools": ["go"],
            "package_managers": ["go modules"],
            "deployment": [],
            "testing": ["go test"]
        }
        
        # Read go.mod for dependencies
        go_mod_path = next((f for f in files if 'go.mod' in f), None)
        if go_mod_path:
            try:
                with open(go_mod_path, 'r') as f:
                    go_mod_content = f.read()
                    
                # Check for web frameworks
                if 'gin-gonic/gin' in go_mod_content:
                    stack["frameworks"].append("Gin")
                if 'gorilla/mux' in go_mod_content:
                    stack["frameworks"].append("Gorilla Mux")
                if 'labstack/echo' in go_mod_content:
                    stack["frameworks"].append("Echo")
                if 'gofiber/fiber' in go_mod_content:
                    stack["frameworks"].append("Fiber")
                
                # Check for databases
                if 'lib/pq' in go_mod_content:
                    stack["databases"].append("PostgreSQL")
                if 'go-sql-driver/mysql' in go_mod_content:
                    stack["databases"].append("MySQL")
                if 'mattn/go-sqlite3' in go_mod_content:
                    stack["databases"].append("SQLite")
                    
            except Exception as e:
                logger.error(f"Error reading go.mod: {e}")
        
        return stack
    
    def _detect_java_stack(self, files: List[str]) -> Dict:
        """Detect Java-specific tech stack"""
        stack = {
            "project_type": "java_project",
            "primary_language": "Java",
            "frameworks": [],
            "databases": [],
            "build_tools": [],
            "package_managers": [],
            "deployment": [],
            "testing": []
        }
        
        # Check for build tools
        if any('pom.xml' in f for f in files):
            stack["build_tools"].append("Maven")
        if any('build.gradle' in f for f in files):
            stack["build_tools"].append("Gradle")
        
        # Read pom.xml for dependencies
        pom_path = next((f for f in files if 'pom.xml' in f), None)
        if pom_path:
            try:
                with open(pom_path, 'r') as f:
                    pom_content = f.read()
                    
                # Check for frameworks
                if 'spring-boot' in pom_content:
                    stack["frameworks"].append("Spring Boot")
                if 'spring-framework' in pom_content:
                    stack["frameworks"].append("Spring Framework")
                if 'hibernate' in pom_content:
                    stack["frameworks"].append("Hibernate")
                    
            except Exception as e:
                logger.error(f"Error reading pom.xml: {e}")
        
        return stack
    
    def _detect_php_stack(self, files: List[str]) -> Dict:
        """Detect PHP-specific tech stack"""
        stack = {
            "project_type": "php_project",
            "primary_language": "PHP",
            "frameworks": [],
            "databases": [],
            "build_tools": [],
            "package_managers": ["Composer"],
            "deployment": [],
            "testing": []
        }
        
        # Read composer.json for dependencies
        composer_path = next((f for f in files if 'composer.json' in f), None)
        if composer_path:
            try:
                with open(composer_path, 'r') as f:
                    composer_data = json.load(f)
                    
                dependencies = composer_data.get('require', {})
                
                # Check for frameworks
                if 'laravel/framework' in dependencies:
                    stack["frameworks"].append("Laravel")
                if 'symfony/symfony' in dependencies:
                    stack["frameworks"].append("Symfony")
                if 'slim/slim' in dependencies:
                    stack["frameworks"].append("Slim")
                    
            except Exception as e:
                logger.error(f"Error reading composer.json: {e}")
        
        return stack
    
    def _detect_dotnet_stack(self, files: List[str]) -> Dict:
        """Detect .NET-specific tech stack"""
        stack = {
            "project_type": "dotnet_project",
            "primary_language": "C#/VB.NET/F#",
            "frameworks": [],
            "databases": [],
            "build_tools": ["MSBuild"],
            "package_managers": ["NuGet"],
            "deployment": [],
            "testing": []
        }
        
        # Check for project files
        for f in files:
            if f.endswith('.csproj'):
                stack["primary_language"] = "C#"
            elif f.endswith('.vbproj'):
                stack["primary_language"] = "VB.NET"
            elif f.endswith('.fsproj'):
                stack["primary_language"] = "F#"
        
        return stack
    
    def _calculate_confidence(self, stack_info: Dict, files: List[str]) -> float:
        """Calculate confidence score for the detected stack"""
        confidence = 0.0
        
        # Base confidence for project type detection
        if stack_info["project_type"] != "unknown":
            confidence += 0.3
        
        # Confidence based on number of framework files
        if len(files) > 0:
            confidence += min(0.2, len(files) * 0.01)
        
        # Confidence based on specific indicators
        if stack_info["frameworks"]:
            confidence += 0.2
        if stack_info["databases"]:
            confidence += 0.1
        if stack_info["build_tools"]:
            confidence += 0.1
        if stack_info["package_managers"]:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def get_project_context(self) -> Dict:
        """Get project-specific context based on detected stack"""
        if not self.detected_stack:
            self.detect_tech_stack()
        
        context = {
            "tech_stack": self.detected_stack,
            "project_patterns": self._get_project_patterns(),
            "best_practices": self._get_best_practices(),
            "common_issues": self._get_common_issues(),
            "development_workflow": self._get_development_workflow()
        }
        
        return context
    
    def _get_project_patterns(self) -> List[str]:
        """Get common patterns for the detected project type"""
        if not self.detected_stack:
            return []
        
        project_type = self.detected_stack["project_type"]
        
        patterns = {
            "python_project": [
                "Virtual environment management",
                "Dependency management with requirements.txt/pyproject.toml",
                "Package structure and imports",
                "Testing with pytest/unittest",
                "Code formatting with black/flake8"
            ],
            "node_project": [
                "Package.json dependency management",
                "Module bundling and transpilation",
                "Component-based architecture (React/Vue)",
                "State management patterns",
                "API integration and routing"
            ],
            "rust_project": [
                "Cargo workspace management",
                "Error handling with Result<T, E>",
                "Ownership and borrowing patterns",
                "Async/await with tokio",
                "Testing with cargo test"
            ],
            "go_project": [
                "Go modules and dependency management",
                "Interface-based design",
                "Goroutines and channels",
                "Error handling patterns",
                "Testing with go test"
            ]
        }
        
        return patterns.get(project_type, ["General software development patterns"])
    
    def _get_best_practices(self) -> List[str]:
        """Get best practices for the detected project type"""
        if not self.detected_stack:
            return []
        
        project_type = self.detected_stack["project_type"]
        
        practices = {
            "python_project": [
                "Use type hints for better code clarity",
                "Follow PEP 8 style guidelines",
                "Implement comprehensive error handling",
                "Use context managers for resource management",
                "Write docstrings for all functions and classes"
            ],
            "node_project": [
                "Use ES6+ features and modern syntax",
                "Implement proper error boundaries",
                "Use TypeScript for type safety",
                "Follow component composition patterns",
                "Implement proper state management"
            ],
            "rust_project": [
                "Leverage Rust's type system for safety",
                "Use Result and Option types effectively",
                "Implement proper error handling",
                "Follow Rust naming conventions",
                "Use cargo clippy for code quality"
            ],
            "go_project": [
                "Follow Go naming conventions",
                "Use interfaces for abstraction",
                "Implement proper error handling",
                "Use goroutines judiciously",
                "Follow Go project layout standards"
            ]
        }
        
        return practices.get(project_type, ["Follow language-specific best practices"])
    
    def _get_common_issues(self) -> List[str]:
        """Get common issues and solutions for the detected project type"""
        if not self.detected_stack:
            return []
        
        project_type = self.detected_stack["project_type"]
        
        issues = {
            "python_project": [
                "Import errors and module resolution",
                "Virtual environment activation issues",
                "Dependency conflicts and versioning",
                "Python path and PYTHONPATH issues",
                "Package installation permissions"
            ],
            "node_project": [
                "Package version conflicts",
                "Module resolution and path issues",
                "Build tool configuration problems",
                "Environment variable management",
                "Cross-platform compatibility issues"
            ],
            "rust_project": [
                "Ownership and borrowing errors",
                "Trait implementation conflicts",
                "Cargo dependency resolution",
                "Cross-compilation issues",
                "Memory management patterns"
            ],
            "go_project": [
                "Go module path issues",
                "Interface implementation conflicts",
                "Goroutine leak prevention",
                "Cross-platform compilation",
                "Dependency management conflicts"
            ]
        }
        
        return issues.get(project_type, ["General debugging and troubleshooting"])
    
    def _get_development_workflow(self) -> List[str]:
        """Get development workflow recommendations for the detected project type"""
        if not self.detected_stack:
            return []
        
        project_type = self.detected_stack["project_type"]
        
        workflows = {
            "python_project": [
                "Set up virtual environment",
                "Install dependencies with pip/poetry",
                "Run tests with pytest",
                "Use pre-commit hooks for code quality",
                "Implement CI/CD with GitHub Actions"
            ],
            "node_project": [
                "Initialize with npm/yarn",
                "Set up build tools and bundlers",
                "Configure testing framework",
                "Use linting and formatting tools",
                "Implement deployment pipeline"
            ],
            "rust_project": [
                "Initialize with cargo new",
                "Add dependencies to Cargo.toml",
                "Run tests with cargo test",
                "Use cargo clippy for linting",
                "Build and run with cargo"
            ],
            "go_project": [
                "Initialize with go mod init",
                "Add dependencies with go get",
                "Run tests with go test",
                "Use go fmt for formatting",
                "Build with go build"
            ]
        }
        
        return workflows.get(project_type, ["General development workflow"])
    
    def inject_smart_context(self, user_message: str) -> str:
        """Inject smart context based on detected tech stack and user preferences"""
        try:
            # Use the centralized prompt generator for smart context
            from prompt_generator import prompt_generator
            
            # Generate smart context enhanced prompt
            enhanced_prompt = prompt_generator.generate_enhanced_prompt(
                user_message=user_message,
                context_type="smart",
                force_refresh=False
            )
            
            return enhanced_prompt
            
        except ImportError:
            # Fallback to original implementation if prompt generator not available
            if not self.detected_stack:
                self.detect_tech_stack()
            
            project_context = self.get_project_context()
            
            # Build enhanced prompt with smart context
            enhanced_prompt = f"""=== SMART CONTEXT ENHANCED PROMPT ===

USER MESSAGE: {user_message}

=== DETECTED TECH STACK ===
Project Type: {self.detected_stack['project_type']}
Primary Language: {self.detected_stack['primary_language']}
Frameworks: {', '.join(self.detected_stack['frameworks']) if self.detected_stack['frameworks'] else 'None detected'}
Databases: {', '.join(self.detected_stack['databases']) if self.detected_stack['databases'] else 'None detected'}
Build Tools: {', '.join(self.detected_stack['build_tools']) if self.detected_stack['build_tools'] else 'None detected'}
Confidence Score: {self.detected_stack['confidence_score']:.1%}

=== PROJECT PATTERNS ===
{chr(10).join(f"• {pattern}" for pattern in project_context['project_patterns'])}

=== BEST PRACTICES ===
{chr(10).join(f"• {practice}" for practice in project_context['best_practices'])}

=== COMMON ISSUES & SOLUTIONS ===
{chr(10).join(f"• {issue}" for issue in project_context['common_issues'])}

=== DEVELOPMENT WORKFLOW ===
{chr(10).join(f"• {workflow}" for workflow in project_context['development_workflow'])}

=== PORTABLE USER PREFERENCES ===
{chr(10).join(f"• {key.replace('_', ' ').title()}: {value}" for key, value in self.user_preferences.items())}

=== INSTRUCTIONS ===
Please respond to the user's message above, taking into account:
1. The detected tech stack and project type
2. Project-specific patterns and best practices
3. Common issues and solutions for this tech stack
4. Recommended development workflow
5. The user's portable preferences and communication style
6. Context-aware suggestions for the specific project type

Provide a comprehensive, tech-stack-aware response that leverages both project-specific knowledge and the user's established preferences.
=== END SMART CONTEXT ENHANCED PROMPT ==="""
            
            return enhanced_prompt.strip()
    
    def get_context_summary(self) -> str:
        """Get a summary of the detected context"""
        if not self.detected_stack:
            self.detect_tech_stack()
        
        return f"""Smart Context Summary:
• Project Type: {self.detected_stack['project_type']}
• Primary Language: {self.detected_stack['primary_language']}
• Frameworks: {', '.join(self.detected_stack['frameworks']) if self.detected_stack['frameworks'] else 'None'}
• Confidence: {self.detected_stack['confidence_score']:.1%}
• User Preferences: {len(self.user_preferences)} portable preferences loaded"""

# Example usage
if __name__ == "__main__":
    # Test the smart context injector
    injector = SmartContextInjector()
    
    # Detect tech stack
    stack = injector.detect_tech_stack()
    print("Detected Stack:", json.dumps(stack, indent=2))
    
    # Get project context
    context = injector.get_project_context()
    print("\nProject Context:", json.dumps(context, indent=2))
    
    # Test context injection
    test_message = "How do I set up a development environment for this project?"
    enhanced = injector.inject_smart_context(test_message)
    print(f"\nEnhanced Prompt ({len(enhanced)} chars):")
    print(enhanced[:500] + "..." if len(enhanced) > 500 else enhanced)
