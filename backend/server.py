"""
Backend server for Project Finder API
"""

import os
import logging
from flask import Flask
from .routes.api_routes import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to run the Flask server"""
    # Create Flask app (API key will be passed from frontend)
    app = create_app("")  # Empty string as placeholder, will be set by frontend
    
    # Run the server
    print("🚀 Starting Project Finder API server...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/health")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )

if __name__ == "__main__":
    main() 