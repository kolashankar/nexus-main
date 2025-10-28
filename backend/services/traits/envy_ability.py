"""Envy vice ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class EnvyAbility:
    """Implementation of Envy vice - Stat Drain ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def stat_drain(
        self,
        envier_id: str,
        target_id: str,
        envier_trait_level: int
    ) -> Dict:
        """Drain stats from target and temporarily boost own stats.
        
        Args:
            envier_id: ID of envious player
            target_id: ID of target player
            envier_trait_level: Envy trait level (1-100)
        
        Returns:
            Dict with success, stats_drained, duration, karma_loss, message
        """
        
        # Get target player
        target = await self.db.players.find_one({"_id": target_id})
        if not target:
            return {
                "success": False,
                "stats_drained": {},
                "message": "Target player not found"
            }
        
        # Can't drain yourself
        if envier_id == target_id:
            return {
                "success": False,
                "stats_drained": {},
                "message": "Cannot use Envy on yourself"
            }
        
        # Get both players' stats
        target_stats = target.get("stats", {})
        
        # Calculate drain amount (10-30% based on trait level)
        min_percent = 10
        max_percent = 30
        drain_percent = min_percent + (envier_trait_level / 100) * (max_percent - min_percent)
        
        # Randomly select 2-4 stats to drain
        num_stats_to_drain = 2 if envier_trait_level < 50 else 4
        stat_names = ["strength", "speed", "intelligence", "defense"]
        stats_to_drain = random.sample(stat_names, num_stats_to_drain)
        
        stats_drained = {}
        for stat in stats_to_drain:
            current_value = target_stats.get(stat, 50)
            drain_amount = int(current_value * (drain_percent / 100))
            drain_amount = max(5, drain_amount)  # Minimum 5 points
            stats_drained[stat] = drain_amount
        
        # Duration based on trait level (30-90 seconds)
        duration = 30 + int((envier_trait_level / 100) * 60)
        
        # Apply stat reduction to target (temporary debuff)
        debuff_data = {
            "type": "stat_drain",
            "stats": stats_drained,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_player_id": envier_id
        }
        
        await self.db.players.update_one(
            {"_id": target_id},
            {"$push": {"debuffs": debuff_data}}
        )
        
        # Apply stat boost to envier (temporary buff)
        buff_data = {
            "type": "stat_boost_envy",
            "stats": stats_drained,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "envy"
        }
        
        await self.db.players.update_one(
            {"_id": envier_id},
            {"$push": {"buffs": buff_data}}
        )
        
        # Apply karma penalty (envy is a vice)
        karma_loss = random.randint(10, 20)
        await self.db.players.update_one(
            {"_id": envier_id},
            {"$inc": {"karma.current": -karma_loss}}
        )
        
        # Notify target
        envier = await self.db.players.find_one({"_id": envier_id})
        envier_name = envier.get("profile", {}).get("name", "Unknown")
        
        await self.db.notifications.insert_one({
            "player_id": target_id,
            "type": "stat_drained",
            "message": f"{envier_name}'s envy has drained your stats temporarily!",
            "data": {
                "envier_id": envier_id,
                "stats_drained": stats_drained,
                "duration": duration,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "stats_drained": stats_drained,
            "duration": duration,
            "karma_loss": karma_loss,
            "message": f"Drained {', '.join(stats_to_drain)} from target for {duration} seconds"
        }
