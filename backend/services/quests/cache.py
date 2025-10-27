"""Quest caching service"""

from typing import Dict, Any, Optional


class QuestCacheService:
    """Caches quest data for performance"""

    def __init__(self):
        # Simple in-memory cache
        # In production, use Redis
        self.cache = {}
        self.ttl = 300  # 5 minutes

    def _generate_key(self, prefix: str, identifier: str) -> str:
        """Generate cache key"""
        return f"quest:{prefix}:{identifier}"

    def get_quest(self, quest_id: str) -> Optional[Dict[str, Any]]:
        """Get cached quest"""
        key = self._generate_key("quest", quest_id)
        return self.cache.get(key)

    def set_quest(self, quest_id: str, quest_data: Dict[str, Any]):
        """Cache quest data"""
        key = self._generate_key("quest", quest_id)
        self.cache[key] = quest_data

    def invalidate_quest(self, quest_id: str):
        """Invalidate cached quest"""
        key = self._generate_key("quest", quest_id)
        if key in self.cache:
            del self.cache[key]

    def get_player_quests(self, player_id: str) -> Optional[list]:
        """Get cached player quests"""
        key = self._generate_key("player_quests", player_id)
        return self.cache.get(key)

    def set_player_quests(self, player_id: str, quests: list):
        """Cache player quests"""
        key = self._generate_key("player_quests", player_id)
        self.cache[key] = quests

    def invalidate_player_quests(self, player_id: str):
        """Invalidate cached player quests"""
        key = self._generate_key("player_quests", player_id)
        if key in self.cache:
            del self.cache[key]

    def clear_all(self):
        """Clear entire cache"""
        self.cache.clear()
