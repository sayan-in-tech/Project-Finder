from backend.utils.cache_cleaner import clean_pycache
import sys

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
    clean_pycache()
    sys.exit(0)