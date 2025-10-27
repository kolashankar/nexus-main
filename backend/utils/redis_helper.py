"""Redis Helper Utilities"""

import logging
from typing import Optional, Any
import json

logger = logging.getLogger(__name__)


class RedisHelper:
    """Helper class for Redis operations"""

    @staticmethod
    async def safe_get(redis_client: Any, key: str) -> Optional[str]:
        """Safely get value from Redis"""
        try:
            if redis_client:
                return await redis_client.get(key)
        except Exception as e:
            logger.error(f"Redis get error for key {key}: {e}")
        return None

    @staticmethod
    async def safe_set(
        redis_client: Any,
        key: str,
        value: str,
        expire: Optional[int] = None
    ) -> bool:
        """Safely set value in Redis"""
        try:
            if redis_client:
                if expire:
                    await redis_client.setex(key, expire, value)
                else:
                    await redis_client.set(key, value)
                return True
        except Exception as e:
            logger.error(f"Redis set error for key {key}: {e}")
        return False

    @staticmethod
    async def safe_delete(redis_client: Any, key: str) -> bool:
        """Safely delete key from Redis"""
        try:
            if redis_client:
                await redis_client.delete(key)
                return True
        except Exception as e:
            logger.error(f"Redis delete error for key {key}: {e}")
        return False

    @staticmethod
    def serialize(data: Any) -> str:
        """Serialize data for Redis storage"""
        return json.dumps(data)

    @staticmethod
    def deserialize(data: str) -> Any:
        """Deserialize data from Redis"""
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data
