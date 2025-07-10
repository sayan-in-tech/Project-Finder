"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from core.config import settings


def setup_logging():
    """Setup structured logging configuration."""
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )
    
    # Set log levels for external libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google.generativeai").setLevel(logging.WARNING)


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


def log_request(request_id: str, method: str, path: str, **kwargs):
    """Log HTTP request details."""
    logger = get_logger("http.request")
    logger.info(
        "HTTP Request",
        request_id=request_id,
        method=method,
        path=path,
        **kwargs
    )


def log_response(request_id: str, status_code: int, duration: float, **kwargs):
    """Log HTTP response details."""
    logger = get_logger("http.response")
    logger.info(
        "HTTP Response",
        request_id=request_id,
        status_code=status_code,
        duration=duration,
        **kwargs
    )


def log_error(error: Exception, context: Dict[str, Any] = None):
    """Log error with context."""
    logger = get_logger("error")
    logger.error(
        "Application Error",
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {},
        exc_info=True
    )


def log_api_call(service: str, method: str, **kwargs):
    """Log API call details."""
    logger = get_logger("api.call")
    logger.info(
        "API Call",
        service=service,
        method=method,
        **kwargs
    ) 