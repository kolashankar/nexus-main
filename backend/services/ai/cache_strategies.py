"""Cache Strategies for AI Services"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class CacheStrategy:
    """Base cache strategy"""

    def should_cache(self, data: Dict[str, Any]) -> bool:
        """Determine if data should be cached"""
        return True

    def get_ttl(self, data: Dict[str, Any]) -> int:
        """Get TTL for cached data"""
        return 3600  # 1 hour default


class KarmaEvaluationCacheStrategy(CacheStrategy):
    """Cache strategy for karma evaluations"""

    def should_cache(self, data: Dict[str, Any]) -> bool:
        """Don't cache extreme karma values"""
        karma_change = abs(data.get("karma_change", 0))
        if karma_change > 100:
            return False
        return True

    def get_ttl(self, data: Dict[str, Any]) -> int:
        """Variable TTL based on severity"""
        severity = data.get("severity", "moderate")
        ttl_map = {
            "minor": 7200,  # 2 hours
            "moderate": 3600,  # 1 hour
            "major": 1800,  # 30 minutes
            "critical": 600  # 10 minutes
        }
        return ttl_map.get(severity, 3600)


class QuestGenerationCacheStrategy(CacheStrategy):
    """Cache strategy for quest generation"""

    def should_cache(self, data: Dict[str, Any]) -> bool:
        """Generally don't cache quests to ensure uniqueness"""
        quest_type = data.get("quest_type", "personal")
        # Only cache templates for very common types
        return quest_type in ["daily"]

    def get_ttl(self, data: Dict[str, Any]) -> int:
        """Short TTL for quest caching"""
        return 1800  # 30 minutes


class CompanionDialogueCacheStrategy(CacheStrategy):
    """Cache strategy for companion dialogue"""

    def should_cache(self, data: Dict[str, Any]) -> bool:
        """Cache common greeting patterns only"""
        message = data.get("message", "").lower()
        common_greetings = ["hi", "hello", "hey", "status", "help"]
        return any(greeting in message for greeting in common_greetings)

    def get_ttl(self, data: Dict[str, Any]) -> int:
        """Short TTL for dialogue"""
        return 600  # 10 minutes


# Strategy factory
CACHE_STRATEGIES = {
    "karma_evaluation": KarmaEvaluationCacheStrategy(),
    "quest_generation": QuestGenerationCacheStrategy(),
    "companion_dialogue": CompanionDialogueCacheStrategy(),
}


def get_cache_strategy(service: str) -> CacheStrategy:
    """Get cache strategy for a service"""
    return CACHE_STRATEGIES.get(service, CacheStrategy())
