"""
Database configuration and session management.
"""

import os
import logging
from typing import Generator, Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import SQLAlchemyError, OperationalError, IntegrityError
import structlog

from core.config import settings
from models.project import Base

# Setup logging
logger = structlog.get_logger()

# Create database directory if it doesn't exist
def ensure_database_directory():
    """Ensure database directory exists with error handling."""
    try:
        if settings.DATABASE_URL.startswith("sqlite:///"):
            db_path = settings.DATABASE_URL.replace("sqlite:///", "")
            db_dir = os.path.dirname(db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
                logger.info("Database directory created", path=db_dir)
        return True
    except Exception as e:
        logger.error("Failed to create database directory", 
                    error=str(e), 
                    database_url=settings.DATABASE_URL,
                    file="database.py",
                    function="ensure_database_directory")
        raise RuntimeError(f"Database directory creation failed: {str(e)}")

# Ensure database directory exists
ensure_database_directory()

# Create engine with error handling
def create_database_engine():
    """Create database engine with comprehensive error handling."""
    try:
        if settings.DATABASE_URL.startswith("sqlite"):
            engine = create_engine(
                settings.DATABASE_URL,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=settings.DEBUG
            )
            logger.info("SQLite engine created", database_url=settings.DATABASE_URL)
        else:
            engine = create_engine(
                settings.DATABASE_URL,
                pool_pre_ping=True,
                echo=settings.DEBUG
            )
            logger.info("Database engine created", database_url=settings.DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            logger.info("Database connection test successful")
        
        return engine
    except SQLAlchemyError as e:
        logger.error("Database engine creation failed", 
                    error=str(e), 
                    database_url=settings.DATABASE_URL,
                    file="database.py",
                    function="create_database_engine")
        raise RuntimeError(f"Database engine creation failed: {str(e)}")
    except Exception as e:
        logger.error("Unexpected error creating database engine", 
                    error=str(e), 
                    database_url=settings.DATABASE_URL,
                    file="database.py",
                    function="create_database_engine")
        raise RuntimeError(f"Unexpected database error: {str(e)}")

# Create engine
try:
    engine = create_database_engine()
except Exception as e:
    logger.error("Critical: Failed to create database engine", error=str(e))
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Get database session with error handling."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error("Database session error", 
                    error=str(e), 
                    error_type=type(e).__name__,
                    file="database.py",
                    function="get_db")
        db.rollback()
        raise
    except Exception as e:
        logger.error("Unexpected database error", 
                    error=str(e), 
                    error_type=type(e).__name__,
                    file="database.py",
                    function="get_db")
        db.rollback()
        raise
    finally:
        try:
            db.close()
        except Exception as e:
            logger.error("Failed to close database session", 
                        error=str(e),
                        file="database.py",
                        function="get_db")

async def init_db():
    """Initialize database tables with comprehensive error handling."""
    try:
        logger.info("Starting database initialization")
        
        # Import all models to ensure they are registered
        from models.project import Company, Challenge, Project, CacheEntry, UserSession
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Verify tables exist
        inspector = engine.dialect.inspector(engine)
        tables = inspector.get_table_names()
        logger.info("Database tables verified", tables=tables)
        
    except SQLAlchemyError as e:
        logger.error("Database initialization failed", 
                    error=str(e), 
                    error_type=type(e).__name__,
                    file="database.py",
                    function="init_db")
        raise RuntimeError(f"Database initialization failed: {str(e)}")
    except ImportError as e:
        logger.error("Failed to import database models", 
                    error=str(e),
                    file="database.py",
                    function="init_db")
        raise RuntimeError(f"Model import failed: {str(e)}")
    except Exception as e:
        logger.error("Unexpected error during database initialization", 
                    error=str(e),
                    file="database.py",
                    function="init_db")
        raise RuntimeError(f"Unexpected database initialization error: {str(e)}")

def get_db_session() -> Session:
    """Get a database session for use in non-async contexts with error handling."""
    try:
        session = SessionLocal()
        logger.debug("Database session created")
        return session
    except Exception as e:
        logger.error("Failed to create database session", 
                    error=str(e),
                    file="database.py",
                    function="get_db_session")
        raise RuntimeError(f"Database session creation failed: {str(e)}")

def test_database_connection() -> bool:
    """Test database connection and return status."""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            result.fetchone()
            logger.info("Database connection test successful")
            return True
    except SQLAlchemyError as e:
        logger.error("Database connection test failed", 
                    error=str(e),
                    file="database.py",
                    function="test_database_connection")
        return False
    except Exception as e:
        logger.error("Unexpected error during database connection test", 
                    error=str(e),
                    file="database.py",
                    function="test_database_connection")
        return False 