"""Arrogance vice ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict
from datetime import datetime, timedelta

class ArroganceAbility:
    """Implementation of Arrogance vice - Crushing Ego ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def crushing_ego(
        self,
        caster_id: str,
        target_id: str,
        trait_level: int
    ) -> Dict:
        """Declare superiority and debuff enemy.
        
        Args:
            caster_id: Arrogant player
            target_id: Target to debuff
            trait_level: Arrogance trait level
        
        Returns:
            Dict with success and debuff details
        """
        
        # Get both players
        caster = await self.db.players.find_one({"_id": caster_id})
        target = await self.db.players.find_one({"_id": target_id})
        
        if not target:
            return {
                "success": False,
                "message": "Target not found"
            }
        
        # Check if caster is actually higher level
        caster_level = caster.get("level", 1)
        target_level = target.get("level", 1)
        
        # Apply debuff
        debuff_duration = 60  # 1 minute
        expires_at = datetime.utcnow() + timedelta(seconds=debuff_duration)
        
        await self.db.players.update_one(
            {"_id": target_id},
            {
                "$set": {
                    "debuffs.crushing_ego": {
                        "active": True,
                        "stat_penalty": 20,  # -20% all stats
                        "expires_at": expires_at,
                        "from_player": caster_id
                    },
                    "psychological_state.tilted": True
                }
            }
        )
        
        # If target is PvP enabled, force taunt
        target_pvp = target.get("pvp", {}).get("enabled", False)
        taunted = False
        
        if target_pvp:
            await self.db.players.update_one(
                {"_id": target_id},
                {"$set": {"combat.forced_target": caster_id}}
            )
            taunted = True
        
        # Apply karma penalty
        karma_loss = 10
        await self.db.players.update_one(
            {"_id": caster_id},
            {"$inc": {"karma.current": -karma_loss}}
        )
        
        # Send notification to target
        await self.db.notifications.insert_one({
            "player_id": target_id,
            "type": "crushing_ego",
            "message": f"{caster.get('username', 'Someone')} mocks your inferiority!",
            "created_at": datetime.utcnow()
        })
        
        return {
            "success": True,
            "message": f"Crushing Ego activated on {target.get('username', 'target')}",
            "debuff": "-20% to all stats for 1 minute",
            "psychological_effect": "Target may become tilted",
            "taunted": taunted,
            "karma_loss": karma_loss,
            "warning": "You've made an enemy"
        }