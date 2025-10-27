"""Redis Configuration and Connection"""

import os
import logging
from typing import Optional

try:
    from redis import asyncio as aioredis
    from redis.asyncio import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    Redis = None

logger = logging.getLogger(__name__)


class RedisManager:
    """Manages Redis connection for caching"""

    def __init__(self):
        self.redis: Optional[Redis] = None
        self.connected = False

    async def connect(self) -> bool:
        """Connect to Redis"""

        if not REDIS_AVAILABLE:
            logger.warning(
                "Redis library not available. Caching will use memory fallback.")
            return False

        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

        try:
            self.redis = await aioredis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )

            # Test connection
            await self.redis.ping()

            self.connected = True
            logger.info(f"Connected to Redis at {redis_url}")
            return True

        except Exception as e:
            logger.warning(
                f"Failed to connect to Redis: {e}. Using memory cache fallback.")
            self.redis = None
            self.connected = False
            return False

    async def disconnect(self) -> None:
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
            self.connected = False
            logger.info("Disconnected from Redis")

    def is_connected(self) -> bool:
        """Check if connected to Redis"""
        return self.connected

    def get_client(self) -> Optional[Redis]:
        """Get Redis client"""
        return self.redis if self.connected else None


# Global Redis manager instance
redis_manager = RedisManager()
