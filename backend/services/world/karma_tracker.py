"""Global Karma Tracker - Tracks collective karma across all players."""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from backend.core.database import db


class GlobalKarmaTracker:
    """Service for tracking global karma statistics."""

    def __init__(self):
        self.db = db

    async def get_global_stats(self) -> Dict[str, Any]:
        """Get global karma statistics."""
        # Get world state
        world_state = await self.db.world_state.find_one()
        if not world_state:
            return self._empty_stats()

        # Calculate 24h action stats
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

        # Count actions by type in last 24h
        actions_pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": twenty_four_hours_ago}
                }
            },
            {
                "$group": {
                    "_id": "$karma_change",
                    "count": {"$sum": 1}
                }
            }
        ]

        actions_stats = await self.db.actions.aggregate(actions_pipeline).to_list(length=None)

        positive_actions = 0
        negative_actions = 0
        neutral_actions = 0

        for stat in actions_stats:
            karma_change = stat["_id"]
            count = stat["count"]
            if karma_change > 0:
                positive_actions += count
            elif karma_change < 0:
                negative_actions += count
            else:
                neutral_actions += count

        # Get top contributors
        top_contributors = await self._get_top_karma_contributors(limit=10)

        # Get karma distribution
        karma_distribution = await self._get_karma_distribution()

        # Determine karma trend
        karma_trend = await self._calculate_karma_trend()

        # Predict next event
        next_event_info = await self._predict_next_event(
            world_state.get("collective_karma", 0)
        )

        return {
            "collective_karma": world_state.get("collective_karma", 0.0),
            "karma_trend": karma_trend,
            "positive_actions_24h": positive_actions,
            "negative_actions_24h": negative_actions,
            "neutral_actions_24h": neutral_actions,
            "top_contributors": top_contributors,
            "karma_distribution": karma_distribution,
            "next_event_threshold": next_event_info.get("threshold"),
            "next_event_type": next_event_info.get("event_type")
        }

    async def update_collective_karma(self, karma_change: float):
        """Update collective karma when a player performs an action."""
        await self.db.world_state.update_one(
            {},
            {
                "$inc": {
                    "collective_karma": karma_change,
                    "total_karma_generated": abs(karma_change)
                },
                "$set": {"last_updated": datetime.utcnow()}
            },
            upsert=True
        )

        # Get updated collective karma
        world_state = await self.db.world_state.find_one()
        collective_karma = world_state.get("collective_karma", 0)

        # Check if this triggers any world events
        from backend.services.world.events import WorldEventsService
        events_service = WorldEventsService()
        await events_service.check_and_trigger_karma_events(collective_karma)

        return collective_karma

    async def _get_top_karma_contributors(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top karma contributors in the last 7 days."""
        seven_days_ago = datetime.utcnow() - timedelta(days=7)

        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": seven_days_ago}
                }
            },
            {
                "$group": {
                    "_id": "$player_id",
                    "total_karma_generated": {"$sum": "$karma_change"},
                    "action_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"total_karma_generated": -1}
            },
            {
                "$limit": limit
            }
        ]

        contributors = await self.db.actions.aggregate(pipeline).to_list(length=limit)

        # Enrich with player data
        result = []
        for contributor in contributors:
            player = await self.db.players.find_one({"_id": contributor["_id"]})
            if player:
                result.append({
                    "player_id": str(contributor["_id"]),
                    "username": player.get("username", "Unknown"),
                    "karma_generated": contributor["total_karma_generated"],
                    "action_count": contributor["action_count"]
                })

        return result

    async def _get_karma_distribution(self) -> Dict[str, int]:
        """Get distribution of players across karma ranges."""
        pipeline = [
            {
                "$bucket": {
                    "groupBy": "$karma_points",
                    "boundaries": [-10000, -5000, -1000, 0, 1000, 5000, 10000],
                    "default": "other",
                    "output": {
                        "count": {"$sum": 1}
                    }
                }
            }
        ]

        distribution = await self.db.players.aggregate(pipeline).to_list(length=None)

        # Format results
        labels = {
            -10000: "very_evil",
            -5000: "evil",
            -1000: "slightly_evil",
            0: "neutral",
            1000: "slightly_good",
            5000: "good",
            10000: "very_good"
        }

        result = {}
        for bucket in distribution:
            key = labels.get(bucket["_id"], "other")
            result[key] = bucket["count"]

        return result

    async def _calculate_karma_trend(self) -> str:
        """Calculate karma trend (rising, falling, stable)."""
        # Get karma changes in last 24 hours vs previous 24 hours
        now = datetime.utcnow()
        last_24h_start = now - timedelta(hours=24)
        previous_24h_start = now - timedelta(hours=48)

        # Last 24 hours
        last_24h_pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": last_24h_start}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$karma_change"}
                }
            }
        ]

        last_24h_result = await self.db.actions.aggregate(last_24h_pipeline).to_list(length=1)
        last_24h_karma = last_24h_result[0]["total"] if last_24h_result else 0

        # Previous 24 hours
        previous_24h_pipeline = [
            {
                "$match": {
                    "timestamp": {
                        "$gte": previous_24h_start,
                        "$lt": last_24h_start
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$karma_change"}
                }
            }
        ]

        previous_24h_result = await self.db.actions.aggregate(previous_24h_pipeline).to_list(length=1)
        previous_24h_karma = previous_24h_result[0]["total"] if previous_24h_result else 0

        # Calculate trend
        if abs(last_24h_karma - previous_24h_karma) < 100:
            return "stable"
        elif last_24h_karma > previous_24h_karma:
            return "rising"
        else:
            return "falling"

    async def _predict_next_event(self, current_karma: float) -> Dict[str, Any]:
        """Predict the next event based on current karma."""
        from backend.services.world.events import WorldEventsService
        events_service = WorldEventsService()

        # Find closest threshold
        closest_threshold = None
        closest_event = None
        min_distance = float('inf')

        for event_type, config in events_service.event_types.items():
            threshold = config.get("karma_threshold")
            if threshold is None:
                continue

            distance = abs(current_karma - threshold)
            if distance < min_distance and (
                (threshold > current_karma and current_karma >= 0) or
                (threshold < current_karma and current_karma < 0)
            ):
                min_distance = distance
                closest_threshold = threshold
                closest_event = event_type

        return {
            "threshold": closest_threshold,
            "event_type": closest_event
        }

    def _empty_stats(self) -> Dict[str, Any]:
        """Return empty stats when no data is available."""
        return {
            "collective_karma": 0.0,
            "karma_trend": "stable",
            "positive_actions_24h": 0,
            "negative_actions_24h": 0,
            "neutral_actions_24h": 0,
            "top_contributors": [],
            "karma_distribution": {},
            "next_event_threshold": None,
            "next_event_type": None
        }
