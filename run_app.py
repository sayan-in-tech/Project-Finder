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

from backend.services.startup.check_api_health import check_api_health
from backend.utils.cache_cleaner import clean_pycache
from backend.services.startup.install_dependencies import install_dependencies
from backend.services.startup.start_backend import start_backend
from backend.services.startup.start_frontend import start_frontend
from backend.services.startup.signal_handler import signal_handler

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
    atexit.register(clean_pycache)
    
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
        clean_pycache()
        print("✅ Both servers stopped")

if __name__ == "__main__":
    main() 