"""Karma Arbiter specific caching strategies"""

import logging

logger = logging.getLogger(__name__)


class KarmaCache:
    """Caching strategies specific to Karma Arbiter"""

    @staticmethod
    def should_cache(action_type: str, karma_value: float) -> bool:
        """Determine if action should be cached"""
        # Don't cache extreme karma values (need fresh evaluation)
        if abs(karma_value) > 500:
            return False

        # Cache common actions
        common_actions = ["help", "trade", "donate"]
        if action_type in common_actions:
            return True

        return True

    @staticmethod
    def get_cache_ttl(action_type: str) -> int:
        """Get cache TTL based on action type"""
        # Shorter TTL for critical actions
        critical_actions = ["betray", "save_life", "murder"]
        if action_type in critical_actions:
            return 600  # 10 minutes

        # Standard TTL for most actions
        return 3600  # 1 hour

    @staticmethod
    def normalize_for_cache(value: float, bucket_size: float = 100) -> float:
        """Normalize values into buckets for better cache hits"""
        return int(value / bucket_size) * bucket_size
