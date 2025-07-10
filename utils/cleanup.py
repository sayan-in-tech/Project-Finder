#!/usr/bin/env python3
"""
Cache Cleanup Utility

This module provides functions to clean up Python cache files (__pycache__)
before and after running the application to keep the repository clean.
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def find_pycache_dirs(root_path: str = ".") -> List[str]:
    """
    Find all __pycache__ directories in the given root path.
    
    Args:
        root_path (str): Root directory to search in
        
    Returns:
        List[str]: List of paths to __pycache__ directories
    """
    pycache_dirs = []
    
    for root, dirs, files in os.walk(root_path):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            pycache_dirs.append(pycache_path)
    
    return pycache_dirs


def remove_pycache_dirs(pycache_dirs: List[str]) -> int:
    """
    Remove __pycache__ directories and their contents.
    
    Args:
        pycache_dirs (List[str]): List of __pycache__ directory paths
        
    Returns:
        int: Number of directories removed
    """
    removed_count = 0
    
    for pycache_dir in pycache_dirs:
        try:
            if os.path.exists(pycache_dir):
                shutil.rmtree(pycache_dir)
                logger.info(f"Removed: {pycache_dir}")
                removed_count += 1
        except Exception as e:
            logger.error(f"Failed to remove {pycache_dir}: {e}")
    
    return removed_count


def cleanup_pycache(root_path: str = ".") -> int:
    """
    Clean up all Python cache files in the given directory.
    
    Args:
        root_path (str): Root directory to search for cache files
        
    Returns:
        int: Number of cache directories removed
    """
    logger.info("🔍 Searching for Python cache directories...")
    pycache_dirs = find_pycache_dirs(root_path)
    
    if not pycache_dirs:
        logger.info("✅ No Python cache directories found")
        return 0
    
    logger.info(f"Found {len(pycache_dirs)} cache directory(ies)")
    removed_count = remove_pycache_dirs(pycache_dirs)
    
    if removed_count > 0:
        logger.info(f"✅ Successfully removed {removed_count} cache directory(ies)")
    else:
        logger.warning("⚠️  No cache directories were removed")
    
    return removed_count


def cleanup_before_run():
    """Clean up cache files before running the application."""
    logger.info("🧹 Pre-run cleanup: Removing Python cache files...")
    cleanup_pycache()


def cleanup_after_run():
    """Clean up cache files after running the application."""
    logger.info("🧹 Post-run cleanup: Removing Python cache files...")
    cleanup_pycache()


def main():
    """Main function to run cleanup when script is executed directly."""
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        root_path = "."
    
    logger.info(f"Starting cache cleanup in: {os.path.abspath(root_path)}")
    removed_count = cleanup_pycache(root_path)
    
    if removed_count > 0:
        print(f"✅ Cleanup complete! Removed {removed_count} cache directory(ies)")
    else:
        print("✅ Cleanup complete! No cache directories found")


if __name__ == "__main__":
    main() 