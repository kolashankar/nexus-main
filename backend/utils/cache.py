"""Caching utilities"""
import hashlib
import json
from typing import Any, Optional
from datetime import datetime, timedelta

class SimpleCache:
    """Simple in-memory cache"""

    def __init__(self):
        self._cache: dict = {}
        self._expiry: dict = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            if key in self._expiry and datetime.utcnow() > self._expiry[key]:
                # Expired
                del self._cache[key]
                del self._expiry[key]
                return None
            return self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value in cache with TTL"""
        self._cache[key] = value
        self._expiry[key] = datetime.utcnow() + timedelta(seconds=ttl_seconds)

    def delete(self, key: str):
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]
        if key in self._expiry:
            del self._expiry[key]

    def clear(self):
        """Clear all cache"""
        self._cache.clear()
        self._expiry.clear()

def generate_cache_key(*args, **kwargs) -> str:
    """Generate cache key from arguments"""
    data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()

# Global cache instance
cache = SimpleCache()
