"""Greed vice ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict
import random
from datetime import datetime

class GreedAbility:
    """Implementation of Greed vice - Plunder ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def plunder(
        self,
        plunderer_id: str,
        target_id: str,
        trait_level: int
    ) -> Dict:
        """Attempt to get double loot from defeated enemy.
        
        Args:
            plunderer_id: Player using Plunder
            target_id: Recently defeated enemy
            trait_level: Greed trait level
        
        Returns:
            Dict with success and loot details
        """
        
        # Check if target was recently defeated by this player
        recent_kill = await self.db.combat_logs.find_one({
            "killer_id": plunderer_id,
            "victim_id": target_id,
            "timestamp": {"$gte": datetime.utcnow() - timedelta(seconds=30)},
            "plundered": {"$ne": True}
        })
        
        if not recent_kill:
            return {
                "success": False,
                "message": "Target not recently defeated or already plundered"
            }
        
        # 50% base chance for double loot
        success_chance = 50 + (trait_level * 0.2)  # +0.2% per level
        success_chance = min(85, success_chance)
        
        success = random.randint(1, 100) <= success_chance
        
        if not success:
            # Failed - target respawns and remembers
            await self.db.combat_logs.update_one(
                {"_id": recent_kill["_id"]},
                {"$set": {"plundered": True, "plunder_failed": True}}
            )
            
            # Create notification for victim
            await self.db.notifications.insert_one({
                "player_id": target_id,
                "type": "plunder_attempt",
                "message": f"Someone tried to plunder your corpse!",
                "data": {"plunderer_id": plunderer_id},
                "created_at": datetime.utcnow()
            })
            
            return {
                "success": False,
                "message": "Plunder failed - Enemy will respawn aware of your greed"
            }
        
        # Success - calculate extra loot
        base_credits = recent_kill.get("credits_dropped", 0)
        extra_credits = int(base_credits * 1.25)  # +125% more
        
        # Grant extra credits
        await self.db.players.update_one(
            {"_id": plunderer_id},
            {"$inc": {"economy.credits": extra_credits}}
        )
        
        # Apply karma penalty
        karma_loss = 15
        await self.db.players.update_one(
            {"_id": plunderer_id},
            {"$inc": {"karma.current": -karma_loss}}
        )
        
        # Mark as plundered
        await self.db.combat_logs.update_one(
            {"_id": recent_kill["_id"]},
            {"$set": {"plundered": True, "plunder_success": True}}
        )
        
        return {
            "success": True,
            "message": f"Plunder successful! Extra {extra_credits} credits obtained",
            "extra_credits": extra_credits,
            "karma_loss": karma_loss,
            "total_from_kill": base_credits + extra_credits
        }

from datetime import timedelta