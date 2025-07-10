#!/usr/bin/env python3
"""
Test script for the cleanup utility.
This script demonstrates how the cleanup utility works.
"""

import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent / "utils"))

def test_cleanup():
    """Test the cleanup utility functions."""
    print("🧪 Testing Cleanup Utility")
    print("=" * 40)
    
    try:
        from cleanup import cleanup_pycache, find_pycache_dirs
        
        # Test finding pycache directories
        print("🔍 Searching for Python cache directories...")
        pycache_dirs = find_pycache_dirs()
        
        if pycache_dirs:
            print(f"Found {len(pycache_dirs)} cache directory(ies):")
            for dir_path in pycache_dirs:
                print(f"  - {dir_path}")
        else:
            print("✅ No cache directories found")
        
        # Test cleanup
        print("\n🧹 Running cleanup...")
        removed_count = cleanup_pycache()
        
        if removed_count > 0:
            print(f"✅ Cleanup complete! Removed {removed_count} cache directory(ies)")
        else:
            print("✅ Cleanup complete! No cache directories to remove")
            
    except ImportError as e:
        print(f"❌ Error importing cleanup utility: {e}")
        print("Make sure utils/cleanup.py exists")
    except Exception as e:
        print(f"❌ Error during cleanup test: {e}")

if __name__ == "__main__":
    test_cleanup() 