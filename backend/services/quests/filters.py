"""Quest filtering service"""

from typing import Dict, Any, List, Optional


class QuestFilterService:
    """Filters quests based on various criteria"""

    @staticmethod
    def filter_by_difficulty(
        quests: List[Dict[str, Any]],
        difficulty: str,
    ) -> List[Dict[str, Any]]:
        """Filter quests by difficulty"""
        return [
            q for q in quests
            if q.get("difficulty") == difficulty
        ]

    @staticmethod
    def filter_by_type(
        quests: List[Dict[str, Any]],
        quest_type: str,
    ) -> List[Dict[str, Any]]:
        """Filter quests by type"""
        return [
            q for q in quests
            if q.get("quest_type") == quest_type
        ]

    @staticmethod
    def filter_by_rewards(
        quests: List[Dict[str, Any]],
        min_xp: Optional[int] = None,
        min_credits: Optional[int] = None,
        min_karma: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Filter quests by minimum rewards"""
        filtered = quests

        if min_xp is not None:
            filtered = [
                q for q in filtered
                if q.get("rewards", {}).get("xp", 0) >= min_xp
            ]

        if min_credits is not None:
            filtered = [
                q for q in filtered
                if q.get("rewards", {}).get("credits", 0) >= min_credits
            ]

        if min_karma is not None:
            filtered = [
                q for q in filtered
                if q.get("rewards", {}).get("karma", 0) >= min_karma
            ]

        return filtered

    @staticmethod
    def sort_quests(
        quests: List[Dict[str, Any]],
        sort_by: str = "generated_at",
        ascending: bool = False,
    ) -> List[Dict[str, Any]]:
        """Sort quests by various criteria"""
        reverse = not ascending

        if sort_by == "xp":
            return sorted(
                quests,
                key=lambda q: q.get("rewards", {}).get("xp", 0),
                reverse=reverse
            )
        elif sort_by == "credits":
            return sorted(
                quests,
                key=lambda q: q.get("rewards", {}).get("credits", 0),
                reverse=reverse
            )
        elif sort_by == "generated_at":
            return sorted(
                quests,
                key=lambda q: q.get("generated_at"),
                reverse=reverse
            )
        else:
            return quests
