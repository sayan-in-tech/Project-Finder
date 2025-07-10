#!/usr/bin/env python3
"""
Project Finder - Enhanced Startup Script
Runs both backend and frontend services with comprehensive error handling.
"""

import subprocess
import sys
import time
import os
import signal
import threading
import queue
import json
from pathlib import Path
from datetime import datetime
import traceback

# Log the Python executable and sys.path for debugging
print(f"[DEBUG] sys.executable: {sys.executable}")
print(f"[DEBUG] sys.path: {sys.path}")

# Add backend/utils to path so we can import cleanup
sys.path.append(str(Path(__file__).parent / "backend" / "utils"))

# Global variables for process management
backend_process = None
frontend_process = None
log_queue = queue.Queue()
is_shutting_down = False

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

def log_error(context: str, error: Exception, file_path: str = None, function_name: str = None):
    """Log detailed error information."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_info = {
        "timestamp": timestamp,
        "context": context,
        "error_type": type(error).__name__,
        "error_message": str(error),
        "file_path": file_path,
        "function_name": function_name,
        "traceback": traceback.format_exc()
    }
    
    ColorPrint.print_error(f"[{context}] {type(error).__name__}: {str(error)}")
    if file_path and function_name:
        ColorPrint.print_info(f"Location: {file_path} -> {function_name}")
    
    # Save error to log file
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    with open(log_dir / "startup_errors.log", "a") as f:
        f.write(f"\n{json.dumps(error_info, indent=2)}\n")
        f.write("-" * 80 + "\n")

def check_python_version():
    """Check if Python version is compatible."""
    try:
        if sys.version_info < (3, 8):
            raise RuntimeError(f"Python 3.8+ required, found {sys.version}")
        ColorPrint.print_success(f"Python version: {sys.version.split()[0]}")
        return True
    except Exception as e:
        log_error("Python Version Check", e, "start.py", "check_python_version")
        return False

def check_dependencies():
    """Check if required dependencies are installed with detailed error reporting."""
    dependencies = {
        "streamlit": "Frontend framework",
        "fastapi": "Backend API framework", 
        "uvicorn": "ASGI server",
        "pydantic": "Data validation",
        "pydantic_settings": "Settings management",  # Note: hyphen becomes underscore in import
        "requests": "HTTP client",
        "dotenv": "Environment management"  # Note: python-dotenv imports as dotenv
    }
    
    missing_deps = []
    failed_imports = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            ColorPrint.print_success(f"{dep}: {description}")
        except ImportError as e:
            missing_deps.append(dep)
            failed_imports.append((dep, str(e)))
            ColorPrint.print_error(f"{dep}: {description} - NOT FOUND")
            log_error(f"Dependency Check - {dep}", e, "start.py", "check_dependencies")
        except Exception as e:
            missing_deps.append(dep)
            failed_imports.append((dep, str(e)))
            ColorPrint.print_error(f"{dep}: {description} - ERROR")
            log_error(f"Dependency Check - {dep}", e, "start.py", "check_dependencies")
    
    if missing_deps:
        ColorPrint.print_error(f"Missing dependencies: {', '.join(missing_deps)}")
        ColorPrint.print_info("Run: pip install -r requirements.txt")
        
        # Additional debugging information
        ColorPrint.print_info("Debugging information:")
        ColorPrint.print_info(f"Python executable: {sys.executable}")
        ColorPrint.print_info(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
        
        # Check if virtual environment is activated
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            ColorPrint.print_success("Virtual environment is active")
        else:
            ColorPrint.print_warning("No virtual environment detected")
        
        # Show failed import details
        for dep, error in failed_imports:
            ColorPrint.print_info(f"  {dep}: {error}")
        
        return False
    
    return True

def check_project_structure():
    """Check if all required project files and directories exist."""
    required_paths = [
        ("backend/", "Backend directory"),
        ("frontend/", "Frontend directory"),
        ("backend/main.py", "Backend main file"),
        ("frontend/app.py", "Frontend app file"),
        ("requirements.txt", "Dependencies file")
    ]
    
    missing_paths = []
    
    for path, description in required_paths:
        if not Path(path).exists():
            missing_paths.append(path)
            ColorPrint.print_error(f"{description}: {path} - NOT FOUND")
    
    if missing_paths:
        ColorPrint.print_error(f"Missing project files: {', '.join(missing_paths)}")
        return False
    
    ColorPrint.print_success("Project structure is valid")
    return True

def setup_environment():
    """Set up environment variables and configuration."""
    try:
        # Create .env if it doesn't exist
        if not Path(".env").exists():
            ColorPrint.print_warning(".env file not found. Creating minimal .env file...")
            
            env_content = """# Project Finder Environment Configuration
# Add your Gemini API key below (required):
GEMINI_API_KEY=your_api_key_here

# Optional: Database URL (defaults to SQLite)
# DATABASE_URL=sqlite:///./database/project_finder.db

# Optional: Redis URL for caching (defaults to in-memory)
# REDIS_URL=redis://localhost:6379

# Optional: Debug mode (defaults to False)
# DEBUG=True

# Optional: Log level (defaults to INFO)
# LOG_LEVEL=INFO
"""
            
            with open(".env", "w") as f:
                f.write(env_content)
            
            ColorPrint.print_success("Created .env file")
            ColorPrint.print_info("Please edit .env and add your Gemini API key")
            ColorPrint.print_info("Get your API key from: https://makersuite.google.com/app/apikey")
            return False
        
        # Load and validate environment
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError as e:
            log_error("Environment Setup", e, "start.py", "setup_environment")
            ColorPrint.print_error("python-dotenv not installed")
            ColorPrint.print_info("Run: pip install python-dotenv")
            return False
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            ColorPrint.print_error("GEMINI_API_KEY not set in .env file")
            ColorPrint.print_info("Please edit .env and add your Gemini API key")
            ColorPrint.print_info("Get your API key from: https://makersuite.google.com/app/apikey")
            return False
        
        ColorPrint.print_success("Environment configuration loaded")
        return True
        
    except Exception as e:
        log_error("Environment Setup", e, "start.py", "setup_environment")
        return False

def check_ports_available():
    """Check if required ports are available."""
    import socket
    
    ports_to_check = [
        (8000, "Backend API"),
        (8501, "Frontend UI")
    ]
    
    unavailable_ports = []
    
    for port, service in ports_to_check:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                ColorPrint.print_success(f"Port {port} ({service}) is available")
        except OSError:
            unavailable_ports.append(port)
            ColorPrint.print_error(f"Port {port} ({service}) is already in use")
    
    if unavailable_ports:
        ColorPrint.print_error(f"Ports {unavailable_ports} are already in use")
        ColorPrint.print_info("Please stop other services using these ports")
        return False
    
    return True

def start_backend():
    """Start the FastAPI backend server with comprehensive error handling."""
    global backend_process
    
    try:
        ColorPrint.print_header("🚀 Starting Backend Server...")
        
        backend_dir = Path("backend")
        if not backend_dir.exists():
            raise FileNotFoundError("Backend directory not found")
        
        # Check if main.py exists
        main_file = backend_dir / "main.py"
        if not main_file.exists():
            raise FileNotFoundError("backend/main.py not found")
        
        # Always use sys.executable for subprocess calls
        cmd = [
            sys.executable,  # Use the current Python interpreter
            "main.py"
        ]
        
        ColorPrint.print_info(f"Command: {' '.join(cmd)}")
        ColorPrint.print_info(f"Working directory: {backend_dir.absolute()}")
        
        backend_process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait a moment and check if process started successfully
        time.sleep(3)
        
        if backend_process.poll() is not None:
            # Process exited immediately
            stdout, stderr = backend_process.communicate()
            raise RuntimeError(f"Backend failed to start. Exit code: {backend_process.returncode}\nSTDOUT: {stdout}\nSTDERR: {stderr}")
        
        ColorPrint.print_success("Backend server started on http://localhost:8000")
        ColorPrint.print_info("API Documentation: http://localhost:8000/docs")
        
        return True
        
    except Exception as e:
        log_error("Backend Startup", e, "start.py", "start_backend")
        return False

def start_frontend():
    """Start the Streamlit frontend server with comprehensive error handling."""
    global frontend_process
    
    try:
        ColorPrint.print_header("🎨 Starting Frontend Server...")
        
        frontend_dir = Path("frontend")
        if not frontend_dir.exists():
            raise FileNotFoundError("Frontend directory not found")
        
        # Check if app.py exists
        app_file = frontend_dir / "app.py"
        if not app_file.exists():
            raise FileNotFoundError("frontend/app.py not found")
        
        # Always use sys.executable for subprocess calls
        cmd = [
            sys.executable,  # Use the current Python interpreter
            "-m", "streamlit", 
            "run", 
            "app.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ]
        
        ColorPrint.print_info(f"Command: {' '.join(cmd)}")
        ColorPrint.print_info(f"Working directory: {frontend_dir.absolute()}")
        
        frontend_process = subprocess.Popen(
            cmd,
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait a moment and check if process started successfully
        time.sleep(5)
        
        if frontend_process.poll() is not None:
            # Process exited immediately
            stdout, stderr = frontend_process.communicate()
            raise RuntimeError(f"Frontend failed to start. Exit code: {frontend_process.returncode}\nSTDOUT: {stdout}\nSTDERR: {stderr}")
        
        ColorPrint.print_success("Frontend server started on http://localhost:8501")
        
        return True
        
    except Exception as e:
        log_error("Frontend Startup", e, "start.py", "start_frontend")
        return False

def monitor_processes():
    """Monitor backend and frontend processes for unexpected exits."""
    global backend_process, frontend_process, is_shutting_down
    
    while not is_shutting_down:
        try:
            # Check backend
            if backend_process and backend_process.poll() is not None:
                stdout, stderr = backend_process.communicate()
                ColorPrint.print_error("Backend process stopped unexpectedly!")
                ColorPrint.print_info(f"Exit code: {backend_process.returncode}")
                if stderr:
                    ColorPrint.print_info(f"Error: {stderr}")
                break
            
            # Check frontend
            if frontend_process and frontend_process.poll() is not None:
                stdout, stderr = frontend_process.communicate()
                ColorPrint.print_error("Frontend process stopped unexpectedly!")
                ColorPrint.print_info(f"Exit code: {frontend_process.returncode}")
                if stderr:
                    ColorPrint.print_info(f"Error: {stderr}")
                break
            
            time.sleep(2)
            
        except Exception as e:
            log_error("Process Monitoring", e, "start.py", "monitor_processes")
            break

def cleanup_processes():
    """Clean up running processes."""
    global backend_process, frontend_process, is_shutting_down
    
    is_shutting_down = True
    
    ColorPrint.print_header("🛑 Stopping Services...")
    
    if backend_process:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
            ColorPrint.print_success("Backend stopped")
        except subprocess.TimeoutExpired:
            backend_process.kill()
            ColorPrint.print_warning("Backend force-killed")
        except Exception as e:
            log_error("Backend Cleanup", e, "start.py", "cleanup_processes")
    
    if frontend_process:
        try:
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
            ColorPrint.print_success("Frontend stopped")
        except subprocess.TimeoutExpired:
            frontend_process.kill()
            ColorPrint.print_warning("Frontend force-killed")
        except Exception as e:
            log_error("Frontend Cleanup", e, "start.py", "cleanup_processes")

def signal_handler(signum, frame):
    """Handle interrupt signals."""
    ColorPrint.print_info("Received interrupt signal")
    cleanup_processes()
    sys.exit(0)

def main():
    """Main startup function with comprehensive error handling."""
    global backend_process, frontend_process
    
    try:
        ColorPrint.print_header("🚀 Project Finder - Project Launcher")
        ColorPrint.print_header("=" * 60)
        
        # Check if we're in the right directory
        if not Path("backend").exists() or not Path("frontend").exists():
            ColorPrint.print_error("Please run this script from the project root directory")
            ColorPrint.print_info("Make sure you're in the Project-Finder folder")
            sys.exit(1)
        
        # Pre-cleanup: Remove Python cache files
        try:
            from cleanup import cleanup_before_run
            cleanup_before_run()
        except ImportError as e:
            ColorPrint.print_warning("Could not import cleanup utility")
            log_error("Cleanup Import", e, "start.py", "main")
        except Exception as e:
            ColorPrint.print_warning(f"Pre-cleanup failed: {e}")
            log_error("Pre-cleanup", e, "start.py", "main")
        
        # .env and API key check (from run.py)
        if not Path(".env").exists():
            ColorPrint.print_info("Creating .env file...")
            env_content = """# Project Finder Environment Configuration\n# Add your Gemini API key below (required):\nGEMINI_API_KEY=your_api_key_here\n\n# Optional: Database URL (defaults to SQLite)\n# DATABASE_URL=sqlite:///./database/project_finder.db\n\n# Optional: Redis URL for caching (defaults to in-memory)\n# REDIS_URL=redis://localhost:6379\n\n# Optional: Debug mode (defaults to False)\n# DEBUG=True\n\n# Optional: Log level (defaults to INFO)\n# LOG_LEVEL=INFO\n"""
            with open(".env", "w") as f:
                f.write(env_content)
            ColorPrint.print_success("Created .env file")
            ColorPrint.print_warning("Please edit .env and add your Gemini API key")
            ColorPrint.print_info("Get your API key from: https://makersuite.google.com/app/apikey")
            return
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key or api_key == "your_api_key_here":
                ColorPrint.print_warning("Please set your Gemini API key in the .env file")
                ColorPrint.print_info("Get your API key from: https://makersuite.google.com/app/apikey")
                return
        except ImportError as e:
            ColorPrint.print_warning("python-dotenv not installed. Install with: pip install python-dotenv")
            log_error("Dotenv Import", e, "start.py", "main")
            return
        
        # Step 1: Check Python version
        ColorPrint.print_header("Step 1: Checking Python Version")
        if not check_python_version():
            sys.exit(1)
        
        # Step 2: Check dependencies
        ColorPrint.print_header("Step 2: Checking Dependencies")
        if not check_dependencies():
            sys.exit(1)
        
        # Step 3: Check project structure
        ColorPrint.print_header("Step 3: Checking Project Structure")
        if not check_project_structure():
            sys.exit(1)
        
        # Step 4: Setup environment
        ColorPrint.print_header("Step 4: Setting Up Environment")
        if not setup_environment():
            sys.exit(1)
        
        # Step 5: Check ports
        ColorPrint.print_header("Step 5: Checking Port Availability")
        if not check_ports_available():
            sys.exit(1)
        
        # Step 6: Start backend
        ColorPrint.print_header("Step 6: Starting Backend")
        if not start_backend():
            ColorPrint.print_error("Failed to start backend")
            sys.exit(1)
        
        # Step 7: Start frontend
        ColorPrint.print_header("Step 7: Starting Frontend")
        if not start_frontend():
            ColorPrint.print_error("Failed to start frontend")
            cleanup_processes()
            sys.exit(1)
        
        # Success!
        ColorPrint.print_header("🎉 Project Finder is Running!")
        ColorPrint.print_success("Frontend: http://localhost:8501")
        ColorPrint.print_success("Backend API: http://localhost:8000")
        ColorPrint.print_success("API Documentation: http://localhost:8000/docs")
        ColorPrint.print_info("Press Ctrl+C to stop all services")
        ColorPrint.print_header("=" * 60)
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_processes, daemon=True)
        monitor_thread.start()
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            ColorPrint.print_info("Received keyboard interrupt")
            cleanup_processes()
        
        ColorPrint.print_success("👋 Goodbye!")
        
    except Exception as e:
        log_error("Main Startup", e, "start.py", "main")
        ColorPrint.print_error("Critical startup error occurred")
        cleanup_processes()
        sys.exit(1)
    finally:
        # Post-cleanup: Remove Python cache files
        try:
            from cleanup import cleanup_after_run
            cleanup_after_run()
        except ImportError as e:
            ColorPrint.print_warning("Could not import cleanup utility")
            log_error("Cleanup Import", e, "start.py", "main")
        except Exception as e:
            ColorPrint.print_warning(f"Post-cleanup failed: {e}")
            log_error("Post-cleanup", e, "start.py", "main")

if __name__ == "__main__":
    main() 