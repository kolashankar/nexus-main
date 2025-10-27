"""AI Response Cache Manager"""

import json
import hashlib
from typing import Any, Dict, Optional
import logging
from datetime import timedelta

try:
    from redis import asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)


class AICacheManager:
    """Manage caching of AI responses for cost optimization"""

    def __init__(self, redis_url: Optional[str] = None, ttl: int = 3600):
        self.redis_client = None
        self.ttl = ttl
        self.memory_cache: Dict[str, Any] = {}  # In-memory fallback

        if REDIS_AVAILABLE and redis_url:
            try:
                self.redis_client = aioredis.from_url(
                    redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                logger.info("Redis cache initialized")
            except Exception as e:
                logger.warning(
                    f"Redis initialization failed: {e}. Using memory cache.")

    def _generate_cache_key(self, service: str, params: Dict[str, Any]) -> str:
        """Generate unique cache key from service name and parameters"""
        params_str = json.dumps(params, sort_keys=True)
        hash_obj = hashlib.md5(params_str.encode())
        return f"ai_cache:{service}:{hash_obj.hexdigest()}"

    async def get(self, service: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached response"""
        cache_key = self._generate_cache_key(service, params)

        # Try Redis first
        if self.redis_client:
            try:
                cached = await self.redis_client.get(cache_key)
                if cached:
                    logger.info(f"Cache hit for {service}")
                    return json.loads(cached)
            except Exception as e:
                logger.error(f"Redis get error: {e}")

        # Fallback to memory cache
        if cache_key in self.memory_cache:
            logger.info(f"Memory cache hit for {service}")
            return self.memory_cache[cache_key]

        return None

    async def set(
        self,
        service: str,
        params: Dict[str, Any],
        response: Dict[str, Any],
        ttl: Optional[int] = None
    ) -> bool:
        """Set cached response"""
        cache_key = self._generate_cache_key(service, params)
        response_str = json.dumps(response)
        ttl = ttl or self.ttl

        # Try Redis first
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    cache_key,
                    timedelta(seconds=ttl),
                    response_str
                )
                logger.info(f"Cached response for {service} in Redis")
                return True
            except Exception as e:
                logger.error(f"Redis set error: {e}")

        # Fallback to memory cache
        self.memory_cache[cache_key] = response
        logger.info(f"Cached response for {service} in memory")
        return True

    async def clear_cache(self, service: Optional[str] = None) -> bool:
        """Clear cache for a service or all caches"""
        if self.redis_client:
            try:
                if service:
                    pattern = f"ai_cache:{service}:*"
                    keys = await self.redis_client.keys(pattern)
                    if keys:
                        await self.redis_client.delete(*keys)
                else:
                    await self.redis_client.flushdb()
                logger.info(f"Cleared cache for {service or 'all'}")
                return True
            except Exception as e:
                logger.error(f"Redis clear error: {e}")

        # Clear memory cache
        if service:
            keys_to_delete = [k for k in self.memory_cache.keys(
            ) if k.startswith(f"ai_cache:{service}:")]
            for key in keys_to_delete:
                del self.memory_cache[key]
        else:
            self.memory_cache.clear()

        return True


# Global cache manager instance
cache_manager = AICacheManager()
