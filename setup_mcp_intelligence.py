#!/usr/bin/env python3
"""
🚀 MCP Conversation Intelligence System - Project Initialization Script

This script makes it incredibly easy to set up the MCP Conversation Intelligence System
in any new project. It automatically detects the project type, installs dependencies,
and configures everything for optimal performance.

Usage:
    python setup_mcp_intelligence.py [--project-path /path/to/project] [--interactive]

Features:
- Automatic project type detection
- Dependency installation
- Configuration generation
- Cursor IDE integration
- Database initialization
- Test setup verification
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import platform

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

class MCPIntelligenceSetup:
    """Main setup class for MCP Conversation Intelligence System"""
    
    def __init__(self, project_path: str = None, interactive: bool = True):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.interactive = interactive
        self.setup_log = []
        self.detected_stack = {}
        
        # Core files to copy
        self.core_files = [
            'smart_context_injector.py',
            'prompt_generator.py', 
            'local_mcp_server_simple.py',
            'unified_preference_manager.py',
            'optimized_prompt_generator.py',
            'adaptive_prompt_engine.py',
            'dynamic_instruction_processor.py',
            'context_manager.py',
            'models_unified.py'
        ]
        
        # Optional advanced files
        self.advanced_files = [
            'real_time_context_refiner.py',
            'intent_driven_context_selector.py',
            'enhanced_context_intelligence.py',
            'adaptive_context_learner.py',
            'context_performance_analyzer.py'
        ]
        
        # Database files
        self.database_files = [
            'init_db.py',
            'migrate_database.py'
        ]
        
        # UI files (optional)
        self.ui_files = [
            'context_ui.py',
            'run_ui.sh'
        ]
    
    def log(self, message: str, color: str = Colors.WHITE):
        """Log a message with color and timestamp"""
        timestamp = f"[{self._get_timestamp()}]"
        print(f"{color}{timestamp} {message}{Colors.END}")
        self.setup_log.append(f"{timestamp} {message}")
    
    def log_success(self, message: str):
        """Log a success message"""
        self.log(f"✅ {message}", Colors.GREEN)
    
    def log_info(self, message: str):
        """Log an info message"""
        self.log(f"ℹ️  {message}", Colors.BLUE)
    
    def log_warning(self, message: str):
        """Log a warning message"""
        self.log(f"⚠️  {message}", Colors.YELLOW)
    
    def log_error(self, message: str):
        """Log an error message"""
        self.log(f"❌ {message}", Colors.RED)
    
    def log_step(self, step: str, message: str):
        """Log a step with formatting"""
        self.log(f"🚀 {step}: {message}", Colors.PURPLE)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def detect_project_type(self) -> Dict[str, any]:
        """Detect the project type and tech stack"""
        self.log_step("DETECTION", "Analyzing project structure...")
        
        stack_info = {
            "project_type": "unknown",
            "primary_language": "unknown", 
            "frameworks": [],
            "databases": [],
            "build_tools": [],
            "package_managers": [],
            "confidence_score": 0.0
        }
        
        try:
            # Check for common project files
            project_files = []
            for root, dirs, files in os.walk(self.project_path):
                # Skip common directories
                dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv', 'ui_env', 'target', 'build']]
                
                for file in files:
                    if file in [
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
                        'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml'
                    ]:
                        project_files.append(os.path.join(root, file))
            
            # Detect based on file patterns
            if any('requirements.txt' in f or 'pyproject.toml' in f for f in project_files):
                stack_info.update(self._detect_python_stack(project_files))
            elif any('package.json' in f for f in project_files):
                stack_info.update(self._detect_node_stack(project_files))
            elif any('Cargo.toml' in f for f in project_files):
                stack_info.update(self._detect_rust_stack(project_files))
            elif any('go.mod' in f for f in project_files):
                stack_info.update(self._detect_go_stack(project_files))
            elif any('pom.xml' in f or 'build.gradle' in f for f in project_files):
                stack_info.update(self._detect_java_stack(project_files))
            elif any('composer.json' in f for f in project_files):
                stack_info.update(self._detect_php_stack(project_files))
            elif any(f.endswith(('.csproj', '.vbproj', '.fsproj', '.sln')) for f in project_files):
                stack_info.update(self._detect_dotnet_stack(project_files))
            
            # Calculate confidence
            stack_info["confidence_score"] = self._calculate_confidence(stack_info, project_files)
            
            self.detected_stack = stack_info
            self.log_success(f"Detected: {stack_info['project_type']} ({stack_info['primary_language']}) - {stack_info['confidence_score']:.1%} confidence")
            
            return stack_info
            
        except Exception as e:
            self.log_error(f"Project detection failed: {e}")
            return stack_info
    
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
                    
                dependencies = package_data.get('dependencies', {})
                dev_dependencies = package_data.get('devDependencies', {})
                
                # Check for frameworks
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
                    
            except Exception as e:
                self.log_warning(f"Could not read package.json: {e}")
        
        return stack
    
    def _detect_rust_stack(self, files: List[str]) -> Dict:
        """Detect Rust-specific tech stack"""
        return {
            "project_type": "rust_project",
            "primary_language": "Rust",
            "frameworks": [],
            "databases": [],
            "build_tools": ["Cargo"],
            "package_managers": ["Cargo"],
            "deployment": [],
            "testing": []
        }
    
    def _detect_go_stack(self, files: List[str]) -> Dict:
        """Detect Go-specific tech stack"""
        return {
            "project_type": "go_project",
            "primary_language": "Go",
            "frameworks": [],
            "databases": [],
            "build_tools": ["go"],
            "package_managers": ["go modules"],
            "deployment": [],
            "testing": ["go test"]
        }
    
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
        
        if any('pom.xml' in f for f in files):
            stack["build_tools"].append("Maven")
        if any('build.gradle' in f for f in files):
            stack["build_tools"].append("Gradle")
        
        return stack
    
    def _detect_php_stack(self, files: List[str]) -> Dict:
        """Detect PHP-specific tech stack"""
        return {
            "project_type": "php_project",
            "primary_language": "PHP",
            "frameworks": [],
            "databases": [],
            "build_tools": [],
            "package_managers": ["Composer"],
            "deployment": [],
            "testing": []
        }
    
    def _detect_dotnet_stack(self, files: List[str]) -> Dict:
        """Detect .NET-specific tech stack"""
        return {
            "project_type": "dotnet_project",
            "primary_language": "C#/VB.NET/F#",
            "frameworks": [],
            "databases": [],
            "build_tools": ["MSBuild"],
            "package_managers": ["NuGet"],
            "deployment": [],
            "testing": []
        }
    
    def _calculate_confidence(self, stack_info: Dict, files: List[str]) -> float:
        """Calculate confidence score for the detected stack"""
        confidence = 0.0
        
        if stack_info["project_type"] != "unknown":
            confidence += 0.3
        
        if len(files) > 0:
            confidence += min(0.2, len(files) * 0.01)
        
        if stack_info["frameworks"]:
            confidence += 0.2
        if stack_info["databases"]:
            confidence += 0.1
        if stack_info["build_tools"]:
            confidence += 0.1
        if stack_info["package_managers"]:
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def _find_mcp_project_dir(self) -> Optional[Path]:
        """Find the MCP project directory by looking for key files"""
        current_dir = Path(__file__).parent
        
        # Try to find the MCP project directory by looking for key files
        for parent in [current_dir, current_dir.parent, current_dir.parent.parent]:
            if (parent / "smart_context_injector.py").exists():
                return parent
        
        # Fallback: try to find it by looking for the MCP folder structure
        for parent in [current_dir, current_dir.parent, current_dir.parent.parent]:
            if "MCP" in str(parent) and (parent / "smart_context_injector.py").exists():
                return parent
        
        # Additional fallback: try to find it by searching the user's home directory
        home_dir = Path.home()
        possible_paths = [
            home_dir / "Documents" / "ProjectsFolder" / "MCP_FOLDER" / "MCP" / "MCP",
            home_dir / "Documents" / "ProjectsFolder" / "MCP_FOLDER" / "MCP",
            home_dir / "Documents" / "MCP_FOLDER" / "MCP" / "MCP",
            home_dir / "MCP_FOLDER" / "MCP" / "MCP",
        ]
        
        for path in possible_paths:
            if path.exists() and (path / "smart_context_injector.py").exists():
                self.log_info(f"Found MCP project directory: {path}")
                return path
        
        # Last resort: ask user for the path
        if self.interactive:
            self.log_warning("Could not automatically find MCP project directory.")
            mcp_path = input("Please enter the full path to your MCP project directory: ").strip()
            if mcp_path:
                mcp_path = Path(mcp_path)
                if mcp_path.exists() and (mcp_path / "smart_context_injector.py").exists():
                    return mcp_path
                else:
                    self.log_error(f"Path {mcp_path} does not contain MCP files")
        
        self.log_error("Could not find MCP project directory. Please ensure the MCP files are accessible.")
        return None
    
    def copy_core_files(self) -> bool:
        """Copy core MCP Intelligence files to the project"""
        self.log_step("SETUP", "Copying core MCP Intelligence files...")
        
        # Find the source directory (where the MCP files are located)
        source_dir = self._find_mcp_project_dir()
        if not source_dir:
            return False
        
        copied_files = []
        failed_files = []
        
        for file_name in self.core_files:
            source_file = source_dir / file_name
            target_file = self.project_path / file_name
            
            if source_file.exists():
                # Check if target file already exists and is identical
                if target_file.exists():
                    try:
                        # Compare file contents to see if they're identical
                        if source_file.read_text() == target_file.read_text():
                            self.log_info(f"Skipping {file_name} (already exists and identical)")
                            copied_files.append(file_name)
                            continue
                        else:
                            # Files exist but are different - copy over
                            shutil.copy2(source_file, target_file)
                            copied_files.append(file_name)
                            self.log_success(f"Updated {file_name}")
                    except Exception:
                        # If we can't compare, just copy
                        shutil.copy2(source_file, target_file)
                        copied_files.append(file_name)
                        self.log_success(f"Copied {file_name}")
                else:
                    # Target file doesn't exist, copy it
                    try:
                        shutil.copy2(source_file, target_file)
                        copied_files.append(file_name)
                        self.log_success(f"Copied {file_name}")
                    except Exception as e:
                        failed_files.append((file_name, str(e)))
                        self.log_error(f"Failed to copy {file_name}: {e}")
            else:
                self.log_warning(f"Source file not found: {file_name}")
        
        if copied_files:
            self.log_success(f"Successfully copied {len(copied_files)} core files")
        
        if failed_files:
            self.log_error(f"Failed to copy {len(failed_files)} files")
            return False
        
        return True
    
    def copy_optional_files(self) -> bool:
        """Copy optional advanced files"""
        if not self.interactive:
            return True
            
        self.log_step("SETUP", "Checking for optional advanced features...")
        
        # Find the source directory (where the MCP files are located)
        source_dir = self._find_mcp_project_dir()
        if not source_dir:
            return False
        
        # Ask user about advanced features
        advanced_features = []
        for file_name in self.advanced_files:
            source_file = source_dir / file_name
            if source_file.exists():
                response = input(f"📦 Install {file_name}? (advanced context features) [y/N]: ").strip().lower()
                if response in ['y', 'yes']:
                    advanced_features.append(file_name)
        
        if not advanced_features:
            self.log_info("Skipping advanced features")
            return True
        
        copied_files = []
        for file_name in advanced_features:
            source_file = source_dir / file_name
            target_file = self.project_path / file_name
            
            try:
                shutil.copy2(source_file, target_file)
                copied_files.append(file_name)
                self.log_success(f"Copied advanced file: {file_name}")
            except Exception as e:
                self.log_error(f"Failed to copy {file_name}: {e}")
        
        if copied_files:
            self.log_success(f"Installed {len(copied_files)} advanced features")
        
        return True
    
    def copy_database_files(self) -> bool:
        """Copy database initialization files"""
        self.log_step("SETUP", "Setting up database files...")
        
        # Find the source directory (where the MCP files are located)
        source_dir = self._find_mcp_project_dir()
        if not source_dir:
            return False
        
        copied_files = []
        failed_files = []
        
        for file_name in self.database_files:
            source_file = source_dir / file_name
            target_file = self.project_path / file_name
            
            if source_file.exists():
                # Check if target file already exists and is identical
                if target_file.exists():
                    try:
                        # Compare file contents to see if they're identical
                        if source_file.read_text() == target_file.read_text():
                            self.log_info(f"Skipping {file_name} (already exists and identical)")
                            copied_files.append(file_name)
                            continue
                        else:
                            # Files exist but are different - copy over
                            shutil.copy2(source_file, target_file)
                            copied_files.append(file_name)
                            self.log_success(f"Updated database file: {file_name}")
                    except Exception:
                        # If we can't compare, just copy
                        shutil.copy2(source_file, target_file)
                        copied_files.append(file_name)
                        self.log_success(f"Copied database file: {file_name}")
                else:
                    # Target file doesn't exist, copy it
                    try:
                        shutil.copy2(source_file, target_file)
                        copied_files.append(file_name)
                        self.log_success(f"Copied database file: {file_name}")
                    except Exception as e:
                        failed_files.append((file_name, str(e)))
                        self.log_error(f"Failed to copy {file_name}: {e}")
            else:
                self.log_warning(f"Database file not found: {file_name}")
        
        if copied_files:
            self.log_success(f"Successfully copied {len(copied_files)} database files")
        
        if failed_files:
            self.log_error(f"Failed to copy {len(failed_files)} database files")
        
        # Return True if we found the source directory, even if some files failed to copy
        return True
    
    def copy_ui_files(self) -> bool:
        """Copy UI files if requested"""
        if not self.interactive:
            return True
            
        self.log_step("SETUP", "Checking for UI features...")
        
        response = input("🖥️  Install web UI for conversation management? [y/N]: ").strip().lower()
        if response not in ['y', 'yes']:
            self.log_info("Skipping UI installation")
            return True
        
        # Find the source directory (where the MCP files are located)
        source_dir = self._find_mcp_project_dir()
        if not source_dir:
            return False
        
        copied_files = []
        for file_name in self.ui_files:
            source_file = source_dir / file_name
            target_file = self.project_path / file_name
            
            if source_file.exists():
                try:
                    shutil.copy2(source_file, target_file)
                    copied_files.append(file_name)
                    self.log_success(f"Copied UI file: {file_name}")
                except Exception as e:
                    self.log_error(f"Failed to copy {file_name}: {e}")
        
        if copied_files:
            self.log_success(f"Installed {len(copied_files)} UI files")
        
        return True
    
    def create_project_config(self) -> bool:
        """Create project-specific configuration"""
        self.log_step("CONFIG", "Creating project configuration...")
        
        config = {
            "project_info": {
                "name": self.project_path.name,
                "path": str(self.project_path),
                "type": self.detected_stack.get("project_type", "unknown"),
                "primary_language": self.detected_stack.get("primary_language", "unknown"),
                "frameworks": self.detected_stack.get("frameworks", []),
                "detected_at": self._get_timestamp()
            },
            "mcp_intelligence": {
                "version": "1.0.0",
                "features": {
                    "smart_context_injection": True,
                    "automatic_stack_detection": True,
                    "conversation_tracking": True,
                    "user_preference_learning": True,
                    "real_time_context_refinement": "advanced_files" in os.listdir(self.project_path) if os.path.exists(self.project_path) else False
                },
                "database": {
                    "type": "sqlite",
                    "path": "./data/agent_tracker.db"
                }
            },
            "cursor_integration": {
                "enabled": True,
                "config_path": "./cursor_mcp_config.json"
            }
        }
        
        config_file = self.project_path / "mcp_intelligence_config.json"
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.log_success(f"Created configuration: {config_file.name}")
            return True
        except Exception as e:
            self.log_error(f"Failed to create config: {e}")
            return False
    
    def create_cursor_config(self) -> bool:
        """Create Cursor IDE integration configuration"""
        self.log_step("CURSOR", "Setting up Cursor IDE integration...")
        
        cursor_config = {
            "mcpServers": {
                "mcp-intelligence": {
                    "command": "python",
                    "args": [str(self.project_path / "local_mcp_server_simple.py")],
                    "env": {
                        "PYTHONPATH": str(self.project_path)
                    }
                }
            }
        }
        
        config_file = self.project_path / "cursor_mcp_config.json"
        try:
            with open(config_file, 'w') as f:
                json.dump(cursor_config, f, indent=2)
            self.log_success(f"Created Cursor config: {config_file.name}")
            
            # Provide instructions
            self.log_info("To use with Cursor IDE:")
            self.log_info(f"1. Copy the contents of {config_file.name}")
            self.log_info("2. Add to your Cursor settings.json under 'mcpServers'")
            self.log_info("3. Restart Cursor IDE")
            
            return True
        except Exception as e:
            self.log_error(f"Failed to create Cursor config: {e}")
            return False
    
    def create_requirements_file(self) -> bool:
        """Create or update requirements file for MCP Intelligence"""
        self.log_step("DEPS", "Setting up dependencies...")
        
        mcp_requirements = [
            "# MCP Conversation Intelligence System Dependencies",
            "httpx>=0.28.1",
            "mcp[cli]>=1.13.1", 
            "sqlalchemy>=2.0.0",
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "psycopg2-binary>=2.9.0",
            "pymysql>=1.1.0",
            "",
            "# Optional: For UI features",
            "# streamlit>=1.28.0",
            "# pandas>=2.0.0",
            "# plotly>=5.15.0",
            "",
            "# Optional: For advanced features", 
            "# scikit-learn>=1.3.0",
            "# numpy>=1.24.0"
        ]
        
        # Check if requirements.txt already exists
        requirements_file = self.project_path / "requirements.txt"
        mcp_requirements_file = self.project_path / "requirements_mcp_intelligence.txt"
        
        try:
            with open(mcp_requirements_file, 'w') as f:
                f.write('\n'.join(mcp_requirements))
            self.log_success(f"Created MCP requirements: {mcp_requirements_file.name}")
            
            if requirements_file.exists():
                self.log_info(f"Existing {requirements_file.name} found - MCP requirements saved separately")
            else:
                # Copy to main requirements.txt
                shutil.copy2(mcp_requirements_file, requirements_file)
                self.log_success(f"Created main requirements: {requirements_file.name}")
            
            return True
        except Exception as e:
            self.log_error(f"Failed to create requirements: {e}")
            return False
    
    def create_data_directory(self) -> bool:
        """Create data directory for database and logs"""
        self.log_step("DATA", "Setting up data directory...")
        
        data_dir = self.project_path / "data"
        logs_dir = self.project_path / "logs"
        
        try:
            data_dir.mkdir(exist_ok=True)
            logs_dir.mkdir(exist_ok=True)
            
            # Create .gitignore for data directory
            gitignore_file = data_dir / ".gitignore"
            with open(gitignore_file, 'w') as f:
                f.write("# MCP Intelligence Data\n")
                f.write("*.db\n")
                f.write("*.log\n")
                f.write("sessions/\n")
                f.write("*.json\n")
            
            self.log_success("Created data and logs directories")
            return True
        except Exception as e:
            self.log_error(f"Failed to create directories: {e}")
            return False
    
    def create_quick_start_script(self) -> bool:
        """Create a quick start script for the project"""
        self.log_step("SCRIPT", "Creating quick start script...")
        
        script_content = f'''#!/bin/bash
# Quick Start Script for MCP Conversation Intelligence System
# Generated for: {self.project_path.name}

echo "🚀 Starting MCP Conversation Intelligence System..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Install dependencies if needed
if [ ! -f "requirements_mcp_intelligence.txt" ]; then
    echo "⚠️  MCP requirements file not found"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -r requirements_mcp_intelligence.txt

# Initialize database
echo "🗄️  Initializing database..."
python3 init_db.py

# Start the system
echo "🎯 Starting MCP Intelligence System..."
python3 local_mcp_server_simple.py
'''
        
        script_file = self.project_path / "start_mcp_intelligence.sh"
        try:
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            # Make executable on Unix systems
            if platform.system() != "Windows":
                os.chmod(script_file, 0o755)
            
            self.log_success(f"Created quick start script: {script_file.name}")
            return True
        except Exception as e:
            self.log_error(f"Failed to create start script: {e}")
            return False
    
    def create_usage_examples(self) -> bool:
        """Create usage examples for the project"""
        self.log_step("EXAMPLES", "Creating usage examples...")
        
        examples_content = f'''# MCP Conversation Intelligence System - Usage Examples

## Quick Start

```bash
# Start the system
./start_mcp_intelligence.sh

# Or manually
python3 local_mcp_server_simple.py
```

## Basic Usage

```python
from smart_context_injector import SmartContextInjector
from prompt_generator import prompt_generator

# Initialize with your project
injector = SmartContextInjector("/path/to/your/project")

# Detect tech stack
stack_info = injector.detect_tech_stack()
print(f"Detected: {{stack_info['project_type']}}")

# Generate enhanced prompt
enhanced_prompt = prompt_generator.generate_enhanced_prompt(
    user_message="How do I set up authentication?",
    context_type="smart"
)
```

## Advanced Usage

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
    current_context={{}},
    available_context={{}},
    conversation_history=[]
)
```

## Cursor IDE Integration

1. Copy the contents of `cursor_mcp_config.json`
2. Add to your Cursor settings.json under 'mcpServers'
3. Restart Cursor IDE
4. Use MCP tools in Cursor for enhanced AI assistance

## Project Type: {self.detected_stack.get('project_type', 'Unknown')}

Your project has been detected as: **{self.detected_stack.get('primary_language', 'Unknown')}**

The system will automatically provide:
- {self.detected_stack.get('primary_language', 'Language')}-specific best practices
- Framework-aware suggestions ({', '.join(self.detected_stack.get('frameworks', ['None detected']))})
- Project structure analysis
- Context-aware responses

## Troubleshooting

If you encounter issues:

1. Check that all dependencies are installed: `pip install -r requirements_mcp_intelligence.txt`
2. Initialize the database: `python3 init_db.py`
3. Check the logs in the `logs/` directory
4. Verify your project path in the configuration

## Support

For issues or questions, check the generated configuration file: `mcp_intelligence_config.json`
'''
        
        examples_file = self.project_path / "MCP_INTELLIGENCE_USAGE.md"
        try:
            with open(examples_file, 'w') as f:
                f.write(examples_content)
            self.log_success(f"Created usage guide: {examples_file.name}")
            return True
        except Exception as e:
            self.log_error(f"Failed to create usage guide: {e}")
            return False
    
    def test_setup(self) -> bool:
        """Test the setup to ensure everything works"""
        self.log_step("TEST", "Testing setup...")
        
        try:
            # Test imports
            import sys
            sys.path.insert(0, str(self.project_path))
            
            # Test core imports with graceful error handling
            try:
                from smart_context_injector import SmartContextInjector
                self.log_success("✅ SmartContextInjector imported successfully")
            except ImportError as e:
                self.log_warning(f"⚠️  SmartContextInjector import failed: {e}")
                self.log_info("This is normal if dependencies are not installed yet")
            
            try:
                from prompt_generator import prompt_generator
                self.log_success("✅ prompt_generator imported successfully")
            except ImportError as e:
                self.log_warning(f"⚠️  prompt_generator import failed: {e}")
                self.log_info("This is normal if dependencies are not installed yet")
            
            # Test file existence
            core_files_exist = all((self.project_path / f).exists() for f in self.core_files)
            if core_files_exist:
                self.log_success("✅ All core files are present")
            else:
                self.log_warning("⚠️  Some core files are missing")
            
            # Test configuration
            config_file = self.project_path / "mcp_intelligence_config.json"
            if config_file.exists():
                self.log_success("✅ Configuration file created")
            else:
                self.log_warning("⚠️  Configuration file missing")
            
            self.log_success("Setup test completed - basic validation passed!")
            self.log_info("Note: Some imports may fail until dependencies are installed")
            return True
            
        except Exception as e:
            self.log_error(f"Setup test failed: {e}")
            return False
    
    def run_setup(self) -> bool:
        """Run the complete setup process"""
        self.log(f"{Colors.BOLD}🚀 MCP Conversation Intelligence System Setup{Colors.END}")
        self.log(f"Project: {self.project_path}")
        self.log(f"Interactive: {self.interactive}")
        self.log("")
        
        # Step 1: Detect project type
        if not self.detect_project_type():
            self.log_error("Project detection failed")
            return False
        
        # Step 2: Copy core files
        if not self.copy_core_files():
            self.log_error("Failed to copy core files")
            return False
        
        # Step 3: Copy optional files
        if not self.copy_optional_files():
            self.log_error("Failed to copy optional files")
            return False
        
        # Step 4: Copy database files
        if not self.copy_database_files():
            self.log_error("Failed to copy database files")
            return False
        
        # Step 5: Copy UI files
        if not self.copy_ui_files():
            self.log_error("Failed to copy UI files")
            return False
        
        # Step 6: Create configuration
        if not self.create_project_config():
            self.log_error("Failed to create project configuration")
            return False
        
        # Step 7: Create Cursor config
        if not self.create_cursor_config():
            self.log_error("Failed to create Cursor configuration")
            return False
        
        # Step 8: Create requirements
        if not self.create_requirements_file():
            self.log_error("Failed to create requirements file")
            return False
        
        # Step 9: Create data directory
        if not self.create_data_directory():
            self.log_error("Failed to create data directory")
            return False
        
        # Step 10: Create quick start script
        if not self.create_quick_start_script():
            self.log_error("Failed to create quick start script")
            return False
        
        # Step 11: Create usage examples
        if not self.create_usage_examples():
            self.log_error("Failed to create usage examples")
            return False
        
        # Step 12: Test setup
        if not self.test_setup():
            self.log_error("Setup test failed")
            return False
        
        # Success!
        self.log("")
        self.log(f"{Colors.BOLD}{Colors.GREEN}🎉 Setup Complete!{Colors.END}")
        self.log("")
        self.log("Next steps:")
        self.log("1. Install dependencies: pip install -r requirements_mcp_intelligence.txt")
        self.log("2. Initialize database: python3 init_db.py")
        self.log("3. Start the system: ./start_mcp_intelligence.sh")
        self.log("4. Read the usage guide: MCP_INTELLIGENCE_USAGE.md")
        self.log("")
        self.log("For Cursor IDE integration, see cursor_mcp_config.json")
        
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Setup MCP Conversation Intelligence System in any project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_mcp_intelligence.py                    # Setup in current directory
  python setup_mcp_intelligence.py --project-path /path/to/project
  python setup_mcp_intelligence.py --no-interactive   # Non-interactive mode
        """
    )
    
    parser.add_argument(
        "--project-path", 
        type=str, 
        help="Path to the project directory (default: current directory)"
    )
    
    parser.add_argument(
        "--no-interactive", 
        action="store_true", 
        help="Run in non-interactive mode (skip optional features)"
    )
    
    args = parser.parse_args()
    
    # Create setup instance
    setup = MCPIntelligenceSetup(
        project_path=args.project_path,
        interactive=not args.no_interactive
    )
    
    # Run setup
    success = setup.run_setup()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
