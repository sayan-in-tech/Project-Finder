#!/usr/bin/env python3
"""
Unified launcher for Project Finder - starts both backend and frontend
"""

import os
import sys
import time
import subprocess
import threading
import requests
import signal
import atexit
from pathlib import Path

# Import cache cleaner
sys.path.append(str(Path(__file__).parent / "backend" / "utils"))
from cache_cleaner import clean_pycache

def check_api_health(base_url: str, max_retries: int = 30) -> bool:
    """Check if the API is healthy and ready"""
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Backend API is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            print(f"⏳ Waiting for backend API... ({i+1}/{max_retries})")
            time.sleep(2)
    
    return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Checking dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed/updated")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True

def start_backend():
    """Start the backend server in a separate thread"""
    try:
        # Start backend server (API key will be passed from frontend)
        subprocess.run([
            sys.executable, "-m", "backend.server"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend server error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def start_frontend():
    """Start the frontend server"""
    try:
        # Start frontend
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "frontend/streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped")

def cleanup_on_exit():
    """Clean up cache and other resources on exit"""
    print("\n🧹 Cleaning up cache...")
    try:
        clean_pycache()
        print("✅ Cache cleanup completed")
    except Exception as e:
        print(f"⚠️  Cache cleanup warning: {e}")

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    cleanup_on_exit()
    sys.exit(0)

def main():
    """Main launcher function"""
    
    print("🚀 Project Finder - Unified Launcher")
    print("=" * 50)
    
    # Clean cache at startup
    print("🧹 Cleaning cache at startup...")
    try:
        clean_pycache()
        print("✅ Startup cache cleanup completed")
    except Exception as e:
        print(f"⚠️  Startup cache cleanup warning: {e}")
    
    # Register cleanup function to run on exit
    atexit.register(cleanup_on_exit)
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check if required files exist
    backend_server_path = Path("backend/server.py")
    frontend_app_path = Path("frontend/streamlit_app.py")
    
    if not backend_server_path.exists():
        print("❌ Backend server not found at backend/server.py")
        sys.exit(1)
    
    if not frontend_app_path.exists():
        print("❌ Frontend app not found at frontend/streamlit_app.py")
        sys.exit(1)
    
    print("✅ All required files found")
    
    # Install/update dependencies
    if not install_dependencies():
        sys.exit(1)
    
    print("🔧 Starting Project Finder...")
    print("💡 API key will be requested in the Streamlit UI")
    print("-" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(
        target=start_backend, 
        daemon=True
    )
    backend_thread.start()
    
    # Wait for backend to be ready
    print("⏳ Starting backend server...")
    if not check_api_health("http://localhost:5000"):
        print("❌ Backend failed to start within expected time")
        print("💡 Make sure you have Flask installed: pip install flask")
        sys.exit(1)
    
    # Start frontend
    print("🌐 Starting frontend...")
    print("📱 Opening browser to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop both servers")
    print("-" * 50)
    
    try:
        start_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Project Finder...")
        cleanup_on_exit()
        print("✅ Both servers stopped")

if __name__ == "__main__":
    main() 