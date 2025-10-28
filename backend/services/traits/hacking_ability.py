"""Hacking skill ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class HackingAbility:
    """Implementation of Hacking skill - Credit Hack ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def credit_hack(
        self,
        hacker_id: str,
        target_id: str,
        hacker_level: int,
        hacker_trait_level: int
    ) -> Dict:
        """Execute credit hack on target player.
        
        Args:
            hacker_id: ID of hacking player
            target_id: ID of target player
            hacker_level: Player level of hacker
            hacker_trait_level: Hacking trait level (1-100)
        
        Returns:
            Dict with success, amount_stolen, detected, message
        """
        
        # Get target player
        target = await self.db.players.find_one({"_id": target_id})
        if not target:
            return {
                "success": False,
                "amount_stolen": 0,
                "detected": False,
                "message": "Target player not found"
            }
        
        # Calculate success rate (60-90% based on trait level)
        base_success_rate = 60
        level_bonus = (hacker_trait_level - 1) * 0.3  # +0.3% per level
        success_rate = min(90, base_success_rate + level_bonus)
        
        # Check if hack succeeds
        roll = random.randint(1, 100)
        success = roll <= success_rate
        
        if not success:
            return {
                "success": False,
                "amount_stolen": 0,
                "detected": True,
                "message": "Hack failed - security systems detected intrusion"
            }
        
        # Calculate steal amount (5-15% of public credits)
        target_public_credits = target.get("economy", {}).get("credits", 0)
        
        if target_public_credits < 10:
            return {
                "success": False,
                "amount_stolen": 0,
                "detected": False,
                "message": "Target has insufficient credits to hack"
            }
        
        # Steal percentage based on trait level
        min_percent = 5
        max_percent = 15
        steal_percent = min_percent + (hacker_trait_level / 100) * (max_percent - min_percent)
        
        amount_to_steal = int(target_public_credits * (steal_percent / 100))
        amount_to_steal = max(10, amount_to_steal)  # Minimum 10 credits
        
        # Detection chance (40% base, reduced by trait level)
        base_detection = 40
        detection_reduction = (hacker_trait_level - 1) * 0.15  # -0.15% per level above 1
        detection_chance = max(10, base_detection - detection_reduction)
        
        detected = random.randint(1, 100) <= detection_chance
        
        # Execute the theft
        # Deduct from target
        await self.db.players.update_one(
            {"_id": target_id},
            {"$inc": {"economy.credits": -amount_to_steal}}
        )
        
        # Add to hacker
        await self.db.players.update_one(
            {"_id": hacker_id},
            {"$inc": {"economy.credits": amount_to_steal}}
        )
        
        # Apply karma penalty to hacker
        karma_loss = random.randint(5, 15)
        await self.db.players.update_one(
            {"_id": hacker_id},
            {"$inc": {"karma.current": -karma_loss}}
        )
        
        # If detected, create notification for target
        if detected:
            await self.db.notifications.insert_one({
                "player_id": target_id,
                "type": "hack_detected",
                "message": f"You've been hacked! {amount_to_steal} credits stolen.",
                "data": {
                    "hacker_id": hacker_id,
                    "amount": amount_to_steal,
                    "timestamp": datetime.utcnow()
                },
                "created_at": datetime.utcnow(),
                "read": False
            })
        
        return {
            "success": True,
            "amount_stolen": amount_to_steal,
            "detected": detected,
            "karma_loss": karma_loss,
            "message": f"Successfully hacked {amount_to_steal} credits" + 
                      (" - You were detected!" if detected else " - Clean getaway!")
        }