"""Event Effects Application System"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...models.world.karma_event import EventEffect

logger = logging.getLogger(__name__)


class EventEffectsManager:
    """
    Manages application and tracking of event effects on players
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        logger.info("EventEffectsManager initialized")

    async def apply_event_effects(self, event_id: str, effects: List[EventEffect]) -> int:
        """
        Apply event effects to affected players
        
        Args:
            event_id: Event ID
            effects: List of effects to apply
        
        Returns:
            Number of players affected
        """
        total_affected = 0

        for effect in effects:
            affected = await self._apply_single_effect(event_id, effect)
            total_affected += affected

        logger.info(
            f"Applied {len(effects)} effects from event {event_id} to {total_affected} players")
        return total_affected

    async def _apply_single_effect(self, event_id: str, effect: EventEffect) -> int:
        """
        Apply a single effect to affected players
        
        Args:
            event_id: Event ID
            effect: Effect to apply
        
        Returns:
            Number of players affected
        """
        # Determine which players are affected
        query = self._build_player_query(effect.affected_players)

        # Build effect document
        effect_doc = {
            "event_id": event_id,
            "effect_type": effect.effect_type,
            "value": effect.value,
            "applied_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=effect.duration_hours),
            "description": effect.description
        }

        # Add to player's active_effects array
        result = await self.db.players.update_many(
            query,
            {"$push": {"active_effects": effect_doc}}
        )

        return result.modified_count

    def _build_player_query(self, affected_players: str) -> Dict:
        """
        Build MongoDB query for affected players
        
        Args:
            affected_players: "all", "territory", "guild", or "alignment"
        
        Returns:
            MongoDB query dict
        """
        if affected_players == "all":
            return {}  # All players

        # Other targeting options would need additional context
        # For now, return all players
        return {}

    async def remove_expired_effects(self) -> int:
        """
        Remove expired effects from all players
        
        Returns:
            Number of effects removed
        """
        now = datetime.utcnow()

        result = await self.db.players.update_many(
            {"active_effects.expires_at": {"$lte": now}},
            {"$pull": {"active_effects": {"expires_at": {"$lte": now}}}}
        )

        if result.modified_count > 0:
            logger.info(
                f"Removed expired effects from {result.modified_count} players")

        return result.modified_count

    async def get_player_active_effects(self, player_id: str) -> List[Dict[str, Any]]:
        """
        Get active effects for a player
        
        Args:
            player_id: Player ID
        
        Returns:
            List of active effects
        """
        player = await self.db.players.find_one(
            {"_id": player_id},
            {"active_effects": 1}
        )

        if not player:
            return []

        # Filter out expired effects
        now = datetime.utcnow()
        active_effects = [
            effect for effect in player.get("active_effects", [])
            if effect.get("expires_at", now) > now
        ]

        return active_effects

    async def calculate_effect_multiplier(self, player_id: str, effect_type: str) -> float:
        """
        Calculate total multiplier for an effect type
        
        Args:
            player_id: Player ID
            effect_type: Type of effect (e.g., "xp_boost")
        
        Returns:
            Total multiplier (1.0 = no boost)
        """
        effects = await self.get_player_active_effects(player_id)

        multiplier = 1.0
        for effect in effects:
            if effect["effect_type"] == effect_type:
                # Add multiplier effects
                if "boost" in effect_type or "multiplier" in effect_type:
                    multiplier += (effect["value"] - 1.0)
                else:
                    multiplier += effect["value"]

        return multiplier
