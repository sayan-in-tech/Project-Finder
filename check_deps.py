#!/usr/bin/env python3
"""
Comprehensive Dependency Checker for Project Finder
This script helps diagnose and fix dependency issues.
"""

import sys
import subprocess
import os
from pathlib import Path
import importlib
import pkg_resources

class ColorPrint:
    """Utility class for colored console output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print_header(msg):
        print(f"{ColorPrint.HEADER}{ColorPrint.BOLD}{msg}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_success(msg):
        print(f"{ColorPrint.OKGREEN}✅ {msg}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_error(msg):
        print(f"{ColorPrint.FAIL}❌ {msg}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_warning(msg):
        print(f"{ColorPrint.WARNING}⚠️  {msg}{ColorPrint.ENDC}")
    
    @staticmethod
    def print_info(msg):
        print(f"{ColorPrint.OKBLUE}ℹ️  {msg}{ColorPrint.ENDC}")

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    ColorPrint.print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        ColorPrint.print_error("Python 3.8+ required")
        return False
    else:
        ColorPrint.print_success("Python version is compatible")
        return True

def check_virtual_environment():
    """Check if virtual environment is active."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        ColorPrint.print_success("Virtual environment is active")
        ColorPrint.print_info(f"Environment: {sys.prefix}")
        return True
    else:
        ColorPrint.print_warning("No virtual environment detected")
        ColorPrint.print_info("Consider using a virtual environment: python -m venv .venv")
        return False

def check_pip():
    """Check pip installation."""
    try:
        import pip
        ColorPrint.print_success("pip is available")
        return True
    except ImportError:
        ColorPrint.print_error("pip is not available")
        return False

def get_installed_packages():
    """Get list of installed packages."""
    try:
        return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    except Exception as e:
        ColorPrint.print_error(f"Failed to get installed packages: {e}")
        return {}

def check_requirements_file():
    """Check if requirements.txt exists and is readable."""
    req_file = Path("requirements.txt")
    if not req_file.exists():
        ColorPrint.print_error("requirements.txt not found")
        return False
    
    try:
        with open(req_file, 'r') as f:
            requirements = f.read()
        ColorPrint.print_success("requirements.txt found and readable")
        return True
    except Exception as e:
        ColorPrint.print_error(f"Failed to read requirements.txt: {e}")
        return False

def check_dependencies():
    """Check all dependencies with detailed information."""
    dependencies = {
        "streamlit": "Frontend framework",
        "fastapi": "Backend API framework", 
        "uvicorn": "ASGI server",
        "pydantic": "Data validation",
        "pydantic_settings": "Settings management",
        "requests": "HTTP client",
        "dotenv": "Environment management",
        "google-generativeai": "Google AI API",
        "sqlalchemy": "Database ORM",
        "redis": "Caching",
        "pandas": "Data processing",
        "numpy": "Numerical computing"
    }
    
    installed_packages = get_installed_packages()
    missing_deps = []
    version_mismatches = []
    
    ColorPrint.print_header("Checking Dependencies:")
    
    for dep, description in dependencies.items():
        try:
            # Try to import the module
            module = importlib.import_module(dep)
            ColorPrint.print_success(f"{dep}: {description}")
            
            # Check if it's in installed packages
            if dep in installed_packages:
                ColorPrint.print_info(f"  Version: {installed_packages[dep]}")
            else:
                ColorPrint.print_warning(f"  Not in pip list (may be built-in)")
                
        except ImportError as e:
            missing_deps.append(dep)
            ColorPrint.print_error(f"{dep}: {description} - NOT FOUND")
            ColorPrint.print_info(f"  Error: {e}")
        except Exception as e:
            missing_deps.append(dep)
            ColorPrint.print_error(f"{dep}: {description} - ERROR")
            ColorPrint.print_info(f"  Error: {e}")
    
    return missing_deps

def check_pip_install():
    """Check if pip install works."""
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            ColorPrint.print_success("pip is working correctly")
            ColorPrint.print_info(f"pip version: {result.stdout.strip()}")
            return True
        else:
            ColorPrint.print_error("pip is not working correctly")
            ColorPrint.print_info(f"Error: {result.stderr}")
            return False
    except Exception as e:
        ColorPrint.print_error(f"Failed to check pip: {e}")
        return False

def suggest_fixes(missing_deps):
    """Suggest fixes for missing dependencies."""
    if not missing_deps:
        ColorPrint.print_success("All dependencies are installed!")
        return
    
    ColorPrint.print_header("Suggested Fixes:")
    
    # Check if we're in a virtual environment
    if not check_virtual_environment():
        ColorPrint.print_info("1. Create and activate a virtual environment:")
        ColorPrint.print_info("   python -m venv .venv")
        ColorPrint.print_info("   .venv\\Scripts\\activate  # Windows")
        ColorPrint.print_info("   source .venv/bin/activate  # Linux/Mac")
    
    # Check if requirements.txt exists
    if check_requirements_file():
        ColorPrint.print_info("2. Install dependencies from requirements.txt:")
        ColorPrint.print_info("   pip install -r requirements.txt")
    
    # Check if pip is working
    if check_pip_install():
        ColorPrint.print_info("3. Install missing packages individually:")
        for dep in missing_deps:
            ColorPrint.print_info(f"   pip install {dep}")
    
    ColorPrint.print_info("4. If issues persist, try:")
    ColorPrint.print_info("   pip install --upgrade pip")
    ColorPrint.print_info("   pip install --force-reinstall -r requirements.txt")

def main():
    """Main function."""
    ColorPrint.print_header("🔍 Project Finder - Dependency Checker")
    ColorPrint.print_header("=" * 50)
    
    # Check Python version
    ColorPrint.print_header("Step 1: Python Version")
    check_python_version()
    
    # Check virtual environment
    ColorPrint.print_header("Step 2: Virtual Environment")
    check_virtual_environment()
    
    # Check pip
    ColorPrint.print_header("Step 3: Package Manager")
    check_pip_install()
    
    # Check requirements file
    ColorPrint.print_header("Step 4: Requirements File")
    check_requirements_file()
    
    # Check dependencies
    ColorPrint.print_header("Step 5: Dependencies")
    missing_deps = check_dependencies()
    
    # Suggest fixes
    ColorPrint.print_header("Step 6: Recommendations")
    suggest_fixes(missing_deps)
    
    ColorPrint.print_header("=" * 50)
    if missing_deps:
        ColorPrint.print_error(f"Found {len(missing_deps)} missing dependencies")
        ColorPrint.print_info("Run the suggested commands above to fix the issues")
    else:
        ColorPrint.print_success("All checks passed! Your environment is ready.")

if __name__ == "__main__":
    main() 