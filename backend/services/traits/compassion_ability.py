"""Compassion virtue ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class CompassionAbility:
    """Implementation of Compassion virtue - Healing Touch ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def healing_touch(
        self,
        healer_id: str,
        target_id: str,
        healer_trait_level: int
    ) -> Dict:
        """Execute healing touch on target player.
        
        Args:
            healer_id: ID of healing player
            target_id: ID of target player (can be self)
            healer_trait_level: Compassion trait level (1-100)
        
        Returns:
            Dict with success, hp_restored, karma_gain, message
        """
        
        # Get target player
        target = await self.db.players.find_one({"_id": target_id})
        if not target:
            return {
                "success": False,
                "hp_restored": 0,
                "karma_gain": 0,
                "message": "Target player not found"
            }
        
        # Get target's current and max HP
        target_stats = target.get("stats", {})
        current_hp = target_stats.get("hp", 100)
        max_hp = target_stats.get("max_hp", 100)
        
        # Check if target needs healing
        if current_hp >= max_hp:
            return {
                "success": False,
                "hp_restored": 0,
                "karma_gain": 0,
                "message": "Target is already at full health"
            }
        
        # Calculate healing amount (20-50% of max HP based on trait level)
        min_percent = 20
        max_percent = 50
        heal_percent = min_percent + (healer_trait_level / 100) * (max_percent - min_percent)
        
        hp_to_restore = int(max_hp * (heal_percent / 100))
        hp_to_restore = min(hp_to_restore, max_hp - current_hp)  # Don't overheal
        
        # Execute the healing
        new_hp = min(max_hp, current_hp + hp_to_restore)
        await self.db.players.update_one(
            {"_id": target_id},
            {"$set": {"stats.hp": new_hp}}
        )
        
        # Calculate karma gain (more for healing others than self)
        is_self_heal = healer_id == target_id
        karma_gain = 3 if is_self_heal else random.randint(8, 15)
        
        # Apply karma bonus to healer
        await self.db.players.update_one(
            {"_id": healer_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        # Create notification for target if not self
        if not is_self_heal:
            healer = await self.db.players.find_one({"_id": healer_id})
            healer_name = healer.get("profile", {}).get("name", "Unknown")
            
            await self.db.notifications.insert_one({
                "player_id": target_id,
                "type": "healed",
                "message": f"{healer_name} healed you for {hp_to_restore} HP!",
                "data": {
                    "healer_id": healer_id,
                    "amount": hp_to_restore,
                    "timestamp": datetime.utcnow()
                },
                "created_at": datetime.utcnow(),
                "read": False
            })
        
        return {
            "success": True,
            "hp_restored": hp_to_restore,
            "karma_gain": karma_gain,
            "new_hp": new_hp,
            "message": f"Successfully healed for {hp_to_restore} HP" + 
                      (" - Your compassion is recognized!" if not is_self_heal else "")
        }
