import subprocess
import sys

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