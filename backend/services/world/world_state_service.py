"""World state service"""

from datetime import datetime
from typing import Dict, Any, Optional

from ...models.world.world_state import WorldState, GlobalKarma


class WorldStateService:
    """Manages world state"""

    def __init__(self, db):
        self.db = db
        self.world_states = db.world_states
        self.players = db.players
        self.actions = db.actions

    async def get_world_state(self) -> Optional[Dict[str, Any]]:
        """Get current world state"""
        state = await self.world_states.find_one({"_id": "world_state"})
        if not state:
            # Create default world state
            state = await self.initialize_world_state()
        return state

    async def initialize_world_state(self) -> Dict[str, Any]:
        """Initialize world state"""
        world_state = WorldState(
            _id="world_state",
            global_karma=GlobalKarma(),
            current_season=1,
            season_start=datetime.utcnow(),
        )

        state_dict = world_state.to_dict()
        await self.world_states.insert_one(state_dict)
        return state_dict

    async def update_global_karma(
        self,
        karma_change: int,
    ) -> Dict[str, Any]:
        """Update global karma"""
        state = await self.get_world_state()

        # Update collective karma
        new_karma = state["global_karma"]["collective_karma"] + karma_change

        # Update action counters
        if karma_change > 0:
            positive_actions = state["global_karma"].get(
                "positive_actions_today", 0) + 1
            update = {"global_karma.positive_actions_today": positive_actions}
        else:
            negative_actions = state["global_karma"].get(
                "negative_actions_today", 0) + 1
            update = {"global_karma.negative_actions_today": negative_actions}

        update["global_karma.collective_karma"] = new_karma
        update["global_karma.total_actions_today"] = state["global_karma"].get(
            "total_actions_today", 0) + 1
        update["last_updated"] = datetime.utcnow()

        # Determine trend
        trend = self._calculate_karma_trend(state)
        update["global_karma.karma_trend"] = trend

        await self.world_states.update_one(
            {"_id": "world_state"},
            {"$set": update}
        )

        return await self.get_world_state()

    def _calculate_karma_trend(self, state: Dict[str, Any]) -> str:
        """Calculate karma trend"""
        positive = state["global_karma"].get("positive_actions_today", 0)
        negative = state["global_karma"].get("negative_actions_today", 0)

        if positive > negative * 1.5:
            return "rising"
        elif negative > positive * 1.5:
            return "falling"
        else:
            return "stable"

    async def update_online_players(self) -> int:
        """Update count of online players"""
        online_count = await self.players.count_documents({"online": True})

        await self.world_states.update_one(
            {"_id": "world_state"},
            {"$set": {
                "online_players": online_count,
                "last_updated": datetime.utcnow(),
            }}
        )

        return online_count

    async def reset_daily_stats(self):
        """Reset daily statistics"""
        await self.world_states.update_one(
            {"_id": "world_state"},
            {"$set": {
                "global_karma.positive_actions_today": 0,
                "global_karma.negative_actions_today": 0,
                "global_karma.total_actions_today": 0,
                "last_updated": datetime.utcnow(),
            }}
        )

    async def get_global_stats(self) -> Dict[str, Any]:
        """Get global statistics"""
        state = await self.get_world_state()

        # Count total players
        total_players = await self.players.count_documents({})

        # Calculate total wealth
        pipeline = [
            {"$group": {
                "_id": None,
                "total_wealth": {"$sum": "$currencies.credits"}
            }}
        ]

        wealth_result = await self.players.aggregate(pipeline).to_list(1)
        total_wealth = wealth_result[0]["total_wealth"] if wealth_result else 0

        return {
            "total_players": total_players,
            "online_players": state.get("online_players", 0),
            "global_karma": state.get("global_karma", {}),
            "total_wealth": total_wealth,
            "current_season": state.get("current_season", 1),
            "active_event": state.get("active_event"),
        }
