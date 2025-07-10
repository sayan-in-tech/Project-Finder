"""
Core configuration for the Project Finder application
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Project Finder"
    PROJECT_DESCRIPTION: str = "AI-powered project discovery and generation platform"
    VERSION: str = "2.0.0"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database settings (for future use)
    DATABASE_URL: Optional[str] = None
    
    # Cache settings
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
