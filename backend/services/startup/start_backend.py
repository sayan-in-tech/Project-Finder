import subprocess
import sys

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