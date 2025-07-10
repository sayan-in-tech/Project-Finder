"""
Dependencies for the FastAPI application
"""

from fastapi import HTTPException, status
from ..core.config import settings


def get_current_user():
    """
    Get current user (placeholder for future authentication)
    """
    # This is a placeholder for future authentication implementation
    return {"user_id": "demo_user", "username": "demo"}


# Note: API key validation is now handled directly in the request models
# Users provide their API keys in the request body
