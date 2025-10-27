"""Collective Karma Tracking System"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


class CollectiveKarmaTracker:
    """
    Tracks and analyzes collective karma trends
    Used by The Architect to determine event triggers
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        logger.info("CollectiveKarmaTracker initialized")

    async def get_collective_karma(self) -> float:
        """
        Calculate total karma of all players
        
        Returns:
            Total collective karma
        """
        pipeline = [
            {"$group": {
                "_id": None,
                "total_karma": {"$sum": "$karma_points"}
            }}
        ]

        result = await self.db.players.aggregate(pipeline).to_list(1)

        if result:
            return result[0].get("total_karma", 0.0)
        return 0.0

    async def get_average_karma(self) -> float:
        """
        Calculate average karma per player
        
        Returns:
            Average karma
        """
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_karma": {"$avg": "$karma_points"}
            }}
        ]

        result = await self.db.players.aggregate(pipeline).to_list(1)

        if result:
            return result[0].get("avg_karma", 0.0)
        return 0.0

    async def get_karma_distribution(self) -> Dict[str, int]:
        """
        Get distribution of players across karma ranges
        
        Returns:
            Dictionary with counts per karma range
        """
        pipeline = [
            {"$bucket": {
                "groupBy": "$karma_points",
                "boundaries": [-10000, -5000, -1000, 0, 1000, 5000, 10000, 20000],
                "default": "extreme",
                "output": {
                    "count": {"$sum": 1},
                    "players": {"$push": "$username"}
                }
            }}
        ]

        result = await self.db.players.aggregate(pipeline).to_list(None)

        distribution = {
            "apocalyptic": 0,  # < -10000
            "very_negative": 0,  # -10000 to -5000
            "negative": 0,  # -5000 to -1000
            "slightly_negative": 0,  # -1000 to 0
            "slightly_positive": 0,  # 0 to 1000
            "positive": 0,  # 1000 to 5000
            "very_positive": 0,  # 5000 to 10000
            "enlightened": 0  # > 10000
        }

        # Map bucket results to distribution
        for bucket in result:
            boundary = bucket.get("_id")
            count = bucket.get("count", 0)

            if boundary == -10000:
                distribution["apocalyptic"] = count
            elif boundary == -5000:
                distribution["very_negative"] = count
            elif boundary == -1000:
                distribution["negative"] = count
            elif boundary == 0:
                distribution["slightly_negative"] = count
            elif boundary == 1000:
                distribution["slightly_positive"] = count
            elif boundary == 5000:
                distribution["positive"] = count
            elif boundary == 10000:
                distribution["very_positive"] = count
            elif boundary == 20000:
                distribution["enlightened"] = count

        return distribution

    async def get_karma_trend(self, hours: int = 24) -> str:
        """
        Analyze karma trend over time period
        
        Args:
            hours: Number of hours to analyze
        
        Returns:
            "rising", "falling", or "stable"
        """
        # Get world state karma history
        world_state = await self.db.world_state.find_one({"_id": "global"})

        if not world_state or not world_state.get("karma_history"):
            return "stable"

        history = world_state["karma_history"]

        if len(history) < 2:
            return "stable"

        # Get oldest and newest karma values
        oldest_karma = history[0].get("collective_karma", 0)
        newest_karma = history[-1].get("collective_karma", 0)

        # Calculate percentage change
        if oldest_karma == 0:
            return "stable"

        change_pct = ((newest_karma - oldest_karma) / abs(oldest_karma)) * 100

        # Determine trend
        if change_pct > 10:
            return "rising"
        elif change_pct < -10:
            return "falling"
        else:
            return "stable"

    async def get_top_karma_players(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get players with highest karma
        
        Args:
            limit: Number of players to return
        
        Returns:
            List of player data dictionaries
        """
        cursor = self.db.players.find(
            {},
            {"username": 1, "karma_points": 1, "moral_class": 1}
        ).sort("karma_points", -1).limit(limit)

        return await cursor.to_list(limit)

    async def get_bottom_karma_players(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get players with lowest karma
        
        Args:
            limit: Number of players to return
        
        Returns:
            List of player data dictionaries
        """
        cursor = self.db.players.find(
            {},
            {"username": 1, "karma_points": 1, "moral_class": 1}
        ).sort("karma_points", 1).limit(limit)

        return await cursor.to_list(limit)

    async def get_karma_by_alignment(self) -> Dict[str, float]:
        """
        Get average karma by moral alignment
        
        Returns:
            Dictionary with average karma per alignment
        """
        pipeline = [
            {"$group": {
                "_id": "$moral_class",
                "avg_karma": {"$avg": "$karma_points"},
                "count": {"$sum": 1}
            }}
        ]

        result = await self.db.players.aggregate(pipeline).to_list(None)

        alignment_karma = {
            "good": 0.0,
            "average": 0.0,
            "bad": 0.0
        }

        for group in result:
            alignment = group.get("_id", "average")
            alignment_karma[alignment] = group.get("avg_karma", 0.0)

        return alignment_karma

    async def get_action_ratio_24h(self) -> Dict[str, float]:
        """
        Get ratio of positive to negative actions in last 24h
        
        Returns:
            Dictionary with action counts and ratios
        """
        cutoff = datetime.utcnow() - timedelta(hours=24)

        pipeline = [
            {"$match": {"timestamp": {"$gte": cutoff}}},
            {"$group": {
                "_id": "$action_type",
                "count": {"$sum": 1}
            }}
        ]

        result = await self.db.actions.aggregate(pipeline).to_list(None)

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for action in result:
            action_type = action.get("_id")
            count = action.get("count", 0)

            if action_type in ["help", "donate"]:
                positive_count += count
            elif action_type in ["steal", "hack", "attack"]:
                negative_count += count
            else:
                neutral_count += count

        total = positive_count + negative_count + neutral_count

        return {
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "total_count": total,
            "positive_ratio": positive_count / total if total > 0 else 0.0,
            "negative_ratio": negative_count / total if total > 0 else 0.0,
            "neutral_ratio": neutral_count / total if total > 0 else 0.0
        }

    async def predict_karma_threshold_crossing(self, threshold: float, hours_ahead: int = 24) -> Optional[float]:
        """
        Predict if collective karma will cross a threshold
        
        Args:
            threshold: Karma threshold to check
            hours_ahead: Hours to predict ahead
        
        Returns:
            Estimated hours until threshold crossed, or None if won't cross
        """
        # Get current karma and trend
        current_karma = await self.get_collective_karma()
        trend = await self.get_karma_trend(hours=24)

        if trend == "stable":
            return None

        # Get karma history to calculate rate of change
        world_state = await self.db.world_state.find_one({"_id": "global"})

        if not world_state or not world_state.get("karma_history"):
            return None

        history = world_state["karma_history"]

        if len(history) < 2:
            return None

        # Calculate average karma change per hour
        oldest = history[0]
        newest = history[-1]

        oldest_time = datetime.fromisoformat(oldest["timestamp"])
        newest_time = datetime.fromisoformat(newest["timestamp"])

        time_diff = (newest_time - oldest_time).total_seconds() / 3600.0
        karma_diff = newest["collective_karma"] - oldest["collective_karma"]

        if time_diff == 0:
            return None

        karma_per_hour = karma_diff / time_diff

        # Calculate if and when threshold will be crossed
        karma_needed = threshold - current_karma

        if (karma_per_hour > 0 and karma_needed > 0) or (karma_per_hour < 0 and karma_needed < 0):
            hours_until = abs(karma_needed / karma_per_hour)

            if hours_until <= hours_ahead:
                return hours_until

        return None
