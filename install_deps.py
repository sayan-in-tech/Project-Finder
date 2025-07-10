#!/usr/bin/env python3
"""
Dependency Installer for Project Finder
This script helps install dependencies with better error handling.
"""

import sys
import subprocess
import os
from pathlib import Path

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

def check_virtual_environment():
    """Check if virtual environment is active."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        ColorPrint.print_success("Virtual environment is active")
        ColorPrint.print_info(f"Environment: {sys.prefix}")
        return True
    else:
        ColorPrint.print_warning("No virtual environment detected")
        ColorPrint.print_info("Consider using a virtual environment for better dependency management")
        return False

def upgrade_pip():
    """Upgrade pip to latest version."""
    ColorPrint.print_header("Upgrading pip...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            ColorPrint.print_success("pip upgraded successfully")
            return True
        else:
            ColorPrint.print_error("Failed to upgrade pip")
            ColorPrint.print_info(f"Error: {result.stderr}")
            return False
    except Exception as e:
        ColorPrint.print_error(f"Failed to upgrade pip: {e}")
        return False

def install_requirements():
    """Install dependencies from requirements.txt."""
    req_file = Path("requirements.txt")
    if not req_file.exists():
        ColorPrint.print_error("requirements.txt not found")
        return False
    
    ColorPrint.print_header("Installing dependencies from requirements.txt...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode == 0:
            ColorPrint.print_success("Dependencies installed successfully")
            return True
        else:
            ColorPrint.print_error("Failed to install dependencies")
            ColorPrint.print_info(f"Error: {result.stderr}")
            return False
    except Exception as e:
        ColorPrint.print_error(f"Failed to install dependencies: {e}")
        return False

def install_individual_packages():
    """Install individual packages that might be missing."""
    critical_packages = [
        "python-dotenv",
        "pydantic-settings",
        "streamlit",
        "fastapi",
        "uvicorn",
        "requests"
    ]
    
    ColorPrint.print_header("Installing critical packages individually...")
    
    for package in critical_packages:
        ColorPrint.print_info(f"Installing {package}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True,
                text=True,
                timeout=300
            )
            if result.returncode == 0:
                ColorPrint.print_success(f"{package} installed successfully")
            else:
                ColorPrint.print_error(f"Failed to install {package}")
                ColorPrint.print_info(f"Error: {result.stderr}")
        except Exception as e:
            ColorPrint.print_error(f"Failed to install {package}: {e}")

def verify_installation():
    """Verify that key packages are installed."""
    key_packages = ["streamlit", "fastapi", "uvicorn", "pydantic", "dotenv"]
    
    ColorPrint.print_header("Verifying installation...")
    
    for package in key_packages:
        try:
            __import__(package)
            ColorPrint.print_success(f"{package} is available")
        except ImportError:
            ColorPrint.print_error(f"{package} is not available")

def main():
    """Main function."""
    ColorPrint.print_header("🔧 Project Finder - Dependency Installer")
    ColorPrint.print_header("=" * 50)
    
    # Check virtual environment
    ColorPrint.print_header("Step 1: Environment Check")
    check_virtual_environment()
    
    # Upgrade pip
    ColorPrint.print_header("Step 2: Upgrade pip")
    upgrade_pip()
    
    # Install requirements
    ColorPrint.print_header("Step 3: Install Dependencies")
    if not install_requirements():
        ColorPrint.print_warning("Failed to install from requirements.txt")
        ColorPrint.print_info("Trying individual package installation...")
        install_individual_packages()
    
    # Verify installation
    ColorPrint.print_header("Step 4: Verify Installation")
    verify_installation()
    
    ColorPrint.print_header("=" * 50)
    ColorPrint.print_success("Installation process completed!")
    ColorPrint.print_info("Run 'python check_deps.py' to verify all dependencies")
    ColorPrint.print_info("Run 'python start.py' to start the application")

if __name__ == "__main__":
    main() 