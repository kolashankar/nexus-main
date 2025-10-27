"""World State Manager"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...models.world.world_state import WorldStateModel

logger = logging.getLogger(__name__)


class WorldStateManager:
    """
    Manages the global state of the game world
    Singleton pattern - only one world state exists
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.world_state
        self._cache: Optional[WorldStateModel] = None
        self._cache_time: Optional[datetime] = None
        self.CACHE_TTL = 60  # Cache for 60 seconds
        logger.info("WorldStateManager initialized")

    async def get_world_state(self, use_cache: bool = True) -> WorldStateModel:
        """
        Get current world state
        
        Args:
            use_cache: Whether to use cached state (default True)
        
        Returns:
            WorldStateModel with current world state
        """
        # Check cache
        if use_cache and self._cache and self._cache_time:
            age = (datetime.utcnow() - self._cache_time).total_seconds()
            if age < self.CACHE_TTL:
                logger.debug(f"Using cached world state (age: {age:.1f}s)")
                return self._cache

        # Fetch from database
        state_doc = await self.collection.find_one({"_id": "global"})

        if not state_doc:
            # Initialize new world state
            logger.info("No world state found, initializing new state")
            state = WorldStateModel()
            await self._save_world_state(state)
        else:
            # Remove MongoDB _id
            state_doc.pop("_id", None)
            state = WorldStateModel(**state_doc)

        # Update cache
        self._cache = state
        self._cache_time = datetime.utcnow()

        return state

    async def update_world_state(
        self,
        updates: Dict[str, Any],
        increment: Optional[Dict[str, float]] = None
    ) -> WorldStateModel:
        """
        Update world state with new values
        
        Args:
            updates: Dictionary of fields to update
            increment: Dictionary of fields to increment
        
        Returns:
            Updated WorldStateModel
        """
        update_doc = {}

        if updates:
            update_doc["$set"] = {
                **updates,
                "last_updated": datetime.utcnow(),
                "update_count": {"$inc": 1}
            }

        if increment:
            if "$inc" not in update_doc:
                update_doc["$inc"] = {}
            update_doc["$inc"].update(increment)

        # Ensure state exists
        await self.collection.update_one(
            {"_id": "global"},
            update_doc,
            upsert=True
        )

        # Invalidate cache
        self._cache = None

        # Return updated state
        return await self.get_world_state(use_cache=False)

    async def _save_world_state(self, state: WorldStateModel) -> None:
        """Save world state to database"""
        state_dict = state.dict()
        state_dict["_id"] = "global"

        await self.collection.replace_one(
            {"_id": "global"},
            state_dict,
            upsert=True
        )

    async def sync_world_state(self) -> WorldStateModel:
        """
        Perform full sync of world state from all sources
        Expensive operation - use sparingly
        """
        logger.info("Performing full world state sync")

        # Get current state
        state = await self.get_world_state(use_cache=False)

        # Calculate player statistics
        total_players = await self.db.players.count_documents({})

        # Active in last 24h
        active_cutoff = datetime.utcnow() - timedelta(hours=24)
        active_players = await self.db.players.count_documents({
            "last_action": {"$gte": active_cutoff}
        })

        # Currently online
        online_players = await self.db.players.count_documents({
            "online": True
        })

        # Calculate collective karma
        pipeline = [
            {"$group": {
                "_id": None,
                "total_karma": {"$sum": "$karma_points"},
                "avg_karma": {"$avg": "$karma_points"}
            }}
        ]
        karma_result = await self.db.players.aggregate(pipeline).to_list(1)

        if karma_result:
            collective_karma = karma_result[0].get("total_karma", 0.0)
            average_karma = karma_result[0].get("avg_karma", 0.0)
        else:
            collective_karma = 0.0
            average_karma = 0.0

        # Calculate karma trend
        karma_trend = "stable"
        if state.karma_history:
            last_karma = state.karma_history[-1].get("collective_karma", 0)
            if collective_karma > last_karma * 1.1:
                karma_trend = "rising"
            elif collective_karma < last_karma * 0.9:
                karma_trend = "falling"

        # Action statistics (last 24h)
        action_cutoff = datetime.utcnow() - timedelta(hours=24)
        action_pipeline = [
            {"$match": {"timestamp": {"$gte": action_cutoff}}},
            {"$group": {
                "_id": "$action_type",
                "count": {"$sum": 1}
            }}
        ]
        action_stats = await self.db.actions.aggregate(action_pipeline).to_list(None)

        total_actions = sum(stat["count"] for stat in action_stats)
        positive_actions = sum(
            stat["count"] for stat in action_stats
            if stat["_id"] in ["help", "donate"]
        )
        negative_actions = sum(
            stat["count"] for stat in action_stats
            if stat["_id"] in ["steal", "hack", "attack"]
        )

        # Guild statistics
        total_guilds = await self.db.guilds.count_documents({})
        guild_wars_active = await self.db.guilds.count_documents({
            "active_wars.0": {"$exists": True}
        })

        # Territory statistics
        territories_contested = await self.db.territories.count_documents({
            "contested": True
        })

        # Total wealth
        wealth_pipeline = [
            {"$group": {
                "_id": None,
                "total": {"$sum": "$currencies.credits"}
            }}
        ]
        wealth_result = await self.db.players.aggregate(wealth_pipeline).to_list(1)
        total_wealth = wealth_result[0].get("total", 0) if wealth_result else 0

        # Update karma history (keep last 24 hourly snapshots)
        karma_snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "collective_karma": collective_karma,
            "average_karma": average_karma,
            "total_players": total_players
        }

        karma_history = state.karma_history[-23:
            ] if state.karma_history else []
        karma_history.append(karma_snapshot)

        # Build update
        updates = {
            "collective_karma": collective_karma,
            "average_karma": average_karma,
            "karma_trend": karma_trend,
            "karma_history": karma_history,
            "total_players": total_players,
            "active_players_24h": active_players,
            "online_players": online_players,
            "total_actions_24h": total_actions,
            "positive_actions_24h": positive_actions,
            "negative_actions_24h": negative_actions,
            "neutral_actions_24h": total_actions - positive_actions - negative_actions,
            "guild_wars_active": guild_wars_active,
            "territories_contested": territories_contested,
            "total_guilds": total_guilds,
            "total_wealth": total_wealth,
            "last_full_sync": datetime.utcnow(),
            "update_count": 0  # Reset counter after full sync
        }

        logger.info(
            f"World state synced: karma={collective_karma:.0f}, "
            f"players={total_players}, online={online_players}, "
            f"actions_24h={total_actions}"
        )

        return await self.update_world_state(updates)

    async def record_karma_change(self, player_id: str, karma_change: float) -> None:
        """
        Record a karma change and update collective karma
        Called after each action evaluation
        """
        await self.update_world_state(
            {},
            increment={"collective_karma": karma_change}
        )

    async def get_time_since_last_event(self) -> Optional[float]:
        """
        Get hours since last global event ended
        
        Returns:
            Hours since last event ended, or None if no events yet
        """
        state = await self.get_world_state()

        if not state.last_global_event_ended:
            return None

        delta = datetime.utcnow() - state.last_global_event_ended
        return delta.total_seconds() / 3600.0

    async def set_active_event(self, event_data: Dict[str, Any]) -> None:
        """
        Set the currently active global event
        """
        await self.update_world_state({
            "active_global_event": event_data,
            "last_global_event_type": event_data.get("event_type"),
            "last_global_event_time": datetime.utcnow(),
            "ai_pantheon_state.architect_last_event": datetime.utcnow()
        })

    async def end_active_event(self) -> None:
        """
        Mark the active event as ended
        """
        await self.update_world_state({
            "active_global_event": None,
            "last_global_event_ended": datetime.utcnow()
        })

    async def get_market_health(self) -> str:
        """
        Calculate and return market health status
        
        Returns:
            "stable", "boom", "crash", or "volatile"
        """
        # This would be calculated based on market data
        # For now, return current state
        state = await self.get_world_state()
        return state.market_health

    async def invalidate_cache(self) -> None:
        """Force cache invalidation"""
        self._cache = None
        self._cache_time = None
        logger.debug("World state cache invalidated")
