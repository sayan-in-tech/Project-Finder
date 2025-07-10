"""
Cache configuration and management.
"""

import json
import hashlib
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
import redis.asyncio as redis
from cachetools import TTLCache
import structlog
import traceback

from core.config import settings

logger = structlog.get_logger()

# In-memory cache as fallback
memory_cache = TTLCache(maxsize=1000, ttl=settings.CACHE_TTL)

# Redis client
redis_client: Optional[redis.Redis] = None


async def init_cache():
    """Initialize cache connection with comprehensive error handling."""
    global redis_client
    
    try:
        if settings.USE_REDIS and settings.REDIS_URL:
            logger.info("Attempting to initialize Redis cache", redis_url=settings.REDIS_URL)
            
            try:
                redis_client = redis.from_url(settings.REDIS_URL)
                await redis_client.ping()
                logger.info("Redis cache initialized successfully")
                
                # Test cache operations
                test_key = "test_connection"
                await redis_client.set(test_key, "test_value", ex=10)
                test_value = await redis_client.get(test_key)
                await redis_client.delete(test_key)
                
                if test_value == b"test_value":
                    logger.info("Redis cache operations verified")
                else:
                    raise RuntimeError("Redis cache test failed")
                    
            except redis.ConnectionError as e:
                logger.error("Redis connection failed", 
                            error=str(e), 
                            redis_url=settings.REDIS_URL,
                            file="cache.py",
                            function="init_cache")
                logger.warning("Falling back to in-memory cache")
                redis_client = None
                
            except redis.RedisError as e:
                logger.error("Redis operation failed", 
                            error=str(e), 
                            redis_url=settings.REDIS_URL,
                            file="cache.py",
                            function="init_cache")
                logger.warning("Falling back to in-memory cache")
                redis_client = None
                
            except Exception as e:
                logger.error("Unexpected Redis error", 
                            error=str(e), 
                            redis_url=settings.REDIS_URL,
                            file="cache.py",
                            function="init_cache")
                logger.warning("Falling back to in-memory cache")
                redis_client = None
        else:
            logger.info("Using in-memory cache", 
                       use_redis=settings.USE_REDIS,
                       has_redis_url=bool(settings.REDIS_URL))
            
    except Exception as e:
        logger.error("Critical cache initialization error", 
                    error=str(e),
                    file="cache.py",
                    function="init_cache")
        raise RuntimeError(f"Cache initialization failed: {str(e)}")


def generate_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments with error handling."""
    try:
        key_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    except Exception as e:
        logger.error("Failed to generate cache key", 
                    error=str(e),
                    args=args,
                    kwargs=kwargs,
                    file="cache.py",
                    function="generate_cache_key")
        # Fallback to simple key
        return hashlib.md5(str(args).encode()).hexdigest()


async def get_cache(key: str) -> Optional[Any]:
    """Get value from cache with comprehensive error handling."""
    try:
        if redis_client:
            try:
                value = await redis_client.get(key)
                if value:
                    return json.loads(value)
            except redis.RedisError as e:
                logger.error("Redis get operation failed", 
                            error=str(e), 
                            key=key,
                            file="cache.py",
                            function="get_cache")
                return None
            except json.JSONDecodeError as e:
                logger.error("Failed to deserialize cached value", 
                            error=str(e), 
                            key=key,
                            file="cache.py",
                            function="get_cache")
                return None
        else:
            return memory_cache.get(key)
            
    except Exception as e:
        logger.error("Unexpected cache get error", 
                    error=str(e), 
                    key=key,
                    file="cache.py",
                    function="get_cache")
        return None


async def set_cache(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """Set value in cache with comprehensive error handling."""
    try:
        ttl = ttl or settings.CACHE_TTL
        
        if redis_client:
            try:
                serialized_value = json.dumps(value)
                await redis_client.setex(key, ttl, serialized_value)
                logger.debug("Value cached in Redis", key=key, ttl=ttl)
                return True
            except redis.RedisError as e:
                logger.error("Redis set operation failed", 
                            error=str(e), 
                            key=key,
                            file="cache.py",
                            function="set_cache")
                return False
            except json.JSONEncodeError as e:
                logger.error("Failed to serialize value for cache", 
                            error=str(e), 
                            key=key,
                            value_type=type(value).__name__,
                            file="cache.py",
                            function="set_cache")
                return False
        else:
            memory_cache[key] = value
            logger.debug("Value cached in memory", key=key, ttl=ttl)
            return True
            
    except Exception as e:
        logger.error("Unexpected cache set error", 
                    error=str(e), 
                    key=key,
                    file="cache.py",
                    function="set_cache")
        return False


async def delete_cache(key: str) -> bool:
    """Delete value from cache with comprehensive error handling."""
    try:
        if redis_client:
            try:
                await redis_client.delete(key)
                logger.debug("Value deleted from Redis cache", key=key)
                return True
            except redis.RedisError as e:
                logger.error("Redis delete operation failed", 
                            error=str(e), 
                            key=key,
                            file="cache.py",
                            function="delete_cache")
                return False
        else:
            memory_cache.pop(key, None)
            logger.debug("Value deleted from memory cache", key=key)
            return True
            
    except Exception as e:
        logger.error("Unexpected cache delete error", 
                    error=str(e), 
                    key=key,
                    file="cache.py",
                    function="delete_cache")
        return False


async def clear_cache() -> bool:
    """Clear all cache entries with comprehensive error handling."""
    try:
        if redis_client:
            try:
                await redis_client.flushdb()
                logger.info("Redis cache cleared successfully")
                return True
            except redis.RedisError as e:
                logger.error("Redis clear operation failed", 
                            error=str(e),
                            file="cache.py",
                            function="clear_cache")
                return False
        else:
            memory_cache.clear()
            logger.info("Memory cache cleared successfully")
            return True
            
    except Exception as e:
        logger.error("Unexpected cache clear error", 
                    error=str(e),
                    file="cache.py",
                    function="clear_cache")
        return False


def cache_decorator(ttl: Optional[int] = None):
    """Decorator for caching function results with error handling."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                # Generate cache key
                cache_key = generate_cache_key(func.__name__, *args, **kwargs)
                
                # Try to get from cache
                cached_result = await get_cache(cache_key)
                if cached_result is not None:
                    logger.debug("Cache hit", function=func.__name__, key=cache_key)
                    return cached_result
                
                # Execute function and cache result
                result = await func(*args, **kwargs)
                await set_cache(cache_key, result, ttl)
                logger.debug("Cache miss, stored result", function=func.__name__, key=cache_key)
                
                return result
                
            except Exception as e:
                logger.error("Cache decorator error", 
                            error=str(e), 
                            function=func.__name__,
                            file="cache.py",
                            function="cache_decorator")
                # Return function result without caching on error
                return await func(*args, **kwargs)
                
        return wrapper
    return decorator


async def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics with error handling."""
    try:
        stats = {
            "cache_type": "redis" if redis_client else "memory",
            "memory_cache_size": len(memory_cache),
            "memory_cache_ttl": settings.CACHE_TTL
        }
        
        if redis_client:
            try:
                info = await redis_client.info()
                stats.update({
                    "redis_connected": True,
                    "redis_keys": info.get("db0", {}).get("keys", 0),
                    "redis_memory": info.get("used_memory_human", "N/A")
                })
            except Exception as e:
                logger.error("Failed to get Redis stats", 
                            error=str(e),
                            file="cache.py",
                            function="get_cache_stats")
                stats["redis_connected"] = False
        else:
            stats["redis_connected"] = False
            
        return stats
        
    except Exception as e:
        logger.error("Failed to get cache stats", 
                    error=str(e),
                    file="cache.py",
                    function="get_cache_stats")
        return {"error": str(e)} 