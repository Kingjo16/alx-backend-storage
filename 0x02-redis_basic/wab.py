#!/usr/bin/env python3
"""A module with tools for request caching and tracking."""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize the module-level Redis instance.
redis_store = redis.Redis()

def cache_requests(method: Callable) -> Callable:
    """Decorator to cache the output of fetched data."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function for caching the output and tracking request count."""
        # Increment the request count for the URL
        redis_store.incr(f'count:{url}')
        
        # Check if the result is already cached
        cached_result = redis_store.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        
        # Call the original method and cache the result
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper

@cache_requests
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response
    and tracking the request count.
    """
    response = requests.get(url)
    return response.text
