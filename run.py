#!/usr/bin/env python3
"""
Project Finder - One Command Runner
Simple script to run the entire project with one command.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add utils to path so we can import cleanup
sys.path.append(str(Path(__file__).parent / "utils"))

def main():
    """Main runner function."""
    print("🚀 Project Finder - One Command Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Error: Please run this script from the project root directory")
        print("   Make sure you're in the Project-Finder folder")
        sys.exit(1)
    
    # Import and run pre-cleanup
    try:
        from cleanup import cleanup_before_run
        cleanup_before_run()
    except ImportError:
        print("⚠️  Warning: Could not import cleanup utility")
    except Exception as e:
        print(f"⚠️  Warning: Pre-cleanup failed: {e}")
    
    # Check if .env exists, create if not
    if not Path(".env").exists():
        print("📝 Creating .env file...")
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
        print("✅ Created .env file")
        print("⚠️  Please edit .env and add your Gemini API key")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
        return
    
    # Check if API key is set
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            print("⚠️  Please set your Gemini API key in the .env file")
            print("   Get your API key from: https://makersuite.google.com/app/apikey")
            return
    except ImportError:
        print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
        return
    
    # Run the enhanced startup script
    print("🎯 Starting Project Finder...")
    print("📱 Frontend will be available at: http://localhost:8501")
    print("🔧 Backend API will be available at: http://localhost:8000")
    print("📚 API Documentation will be available at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services")
    print("=" * 50)
    
    try:
        # Run the enhanced startup script
        subprocess.run([sys.executable, "start.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running the application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Run post-cleanup
        try:
            from cleanup import cleanup_after_run
            cleanup_after_run()
        except ImportError:
            print("⚠️  Warning: Could not import cleanup utility")
        except Exception as e:
            print(f"⚠️  Warning: Post-cleanup failed: {e}")

if __name__ == "__main__":
    main() 