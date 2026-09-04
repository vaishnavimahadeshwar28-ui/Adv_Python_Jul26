# app/decorators.py

"""

Custom decorators for logging, caching, and performance monitoring.

"""

import functools

import time

import json

import hashlib

from typing import Any, Callable, Dict, Optional

from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)

# ===== Simple In-Memory Cache =====

class Cache:

    """Simple in-memory cache with TTL."""

    

    def __init__(self):

        self._cache: Dict[str, tuple[Any, datetime]] = {}

    

    def get(self, key: str) -> Optional[Any]:

        """Get cached value if not expired."""

        if key in self._cache:

            value, expires_at = self._cache[key]

            if datetime.now() < expires_at:

                return value

            else:

                del self._cache[key]

        return None

    

    def set(self, key: str, value: Any, ttl_seconds: int = 300):

        """Store value with TTL."""

        expires_at = datetime.now() + timedelta(seconds=ttl_seconds)

        self._cache[key] = (value, expires_at)

    

    def clear(self):

        """Clear all cache entries."""

        self._cache.clear()

    

    def invalidate(self, pattern: str):

        """Invalidate cache entries matching a pattern."""

        to_delete = [k for k in self._cache.keys() if pattern in k]

        for k in to_delete:

            del self._cache[k]


# Global cache instance

cache = Cache()


# ===== Logging Decorator =====

def log_execution(func: Callable) -> Callable:

    """

    Decorator to log function execution with arguments and return value.

    """

    @functools.wraps(func)

    def wrapper(*args, **kwargs):

        # Prepare log data

        func_name = func.__name__

        args_str = ', '.join([repr(a) for a in args[1:]])  # Skip self

        kwargs_str = ', '.join([f"{k}={repr(v)}" for k, v in kwargs.items()])

        

        logger.debug(f"Starting {func_name}({args_str}{', ' if args_str and kwargs_str else ''}{kwargs_str})")

        

        try:

            start_time = time.time()

            result = func(*args, **kwargs)

            elapsed = time.time() - start_time

            

            logger.info(f"Completed {func_name} in {elapsed:.3f}s")

            return result

            

        except Exception as e:

            logger.error(f"Error in {func_name}: {type(e).__name__}: {str(e)}")

            raise

    

    return wrapper


# ===== Caching Decorator =====

def cached(ttl_seconds: int = 300, key_prefix: str = ""):

    """

    Decorator to cache function results.

    """

    def decorator(func: Callable) -> Callable:

        @functools.wraps(func)

        def wrapper(*args, **kwargs):

            # Generate cache key

            key_parts = [key_prefix, func.__name__]

            

            # Add positional arguments (skip self)

            for arg in args[1:]:

                key_parts.append(str(arg))

            

            # Add keyword arguments

            for k, v in sorted(kwargs.items()):

                key_parts.append(f"{k}:{v}")

            

            cache_key = hashlib.md5('|'.join(key_parts).encode()).hexdigest()

            

            # Check cache

            cached_result = cache.get(cache_key)

            if cached_result is not None:

                logger.debug(f"Cache hit for {func.__name__}")

                return cached_result

            

            # Execute function

            logger.debug(f"Cache miss for {func.__name__}")

            result = func(*args, **kwargs)

            

            # Store in cache

            cache.set(cache_key, result, ttl_seconds)

            

            return result

        

        return wrapper

    return decorator


# ===== Retry Decorator =====

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):

    """

    Decorator to retry a function on failure.

    """

    def decorator(func: Callable) -> Callable:

        @functools.wraps(func)

        def wrapper(*args, **kwargs):

            last_exception = None

            for attempt in range(max_attempts):

                try:

                    return func(*args, **kwargs)

                except exceptions as e:

                    last_exception = e

                    if attempt < max_attempts - 1:

                        wait_time = delay * (2 ** attempt)  # Exponential backoff

                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {wait_time:.2f}s")

                        time.sleep(wait_time)

            

            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")

            raise last_exception

        

        return wrapper

    return decorator


# ===== Performance Monitoring Decorator =====

def monitor_performance(threshold: float = 1.0):

    """

    Decorator to monitor performance and warn if execution exceeds threshold.

    """

    def decorator(func: Callable) -> Callable:

        @functools.wraps(func)

        def wrapper(*args, **kwargs):

            start_time = time.time()

            result = func(*args, **kwargs)

            elapsed = time.time() - start_time

            

            if elapsed > threshold:

                logger.warning(f"Performance warning: {func.__name__} took {elapsed:.3f}s (threshold: {threshold}s)")

            

            return result

        

        return wrapper

    return decorator