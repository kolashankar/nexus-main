"""Empathy virtue ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict
from datetime import datetime

class EmpathyAbility:
    """Implementation of Empathy virtue - Emotional Shield ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def emotional_shield(
        self,
        caster_id: str,
        target_id: str,
        trait_level: int
    ) -> Dict:
        """Absorb emotional damage from ally.
        
        Takes mental status effects from target and applies to caster with resistance.
        
        Args:
            caster_id: Player using Empathy
            target_id: Ally to protect
            trait_level: Empathy trait level
        
        Returns:
            Dict with success and transfer details
        """
        
        # Get target's mental afflictions
        target = await self.db.players.find_one({"_id": target_id})
        if not target:
            return {
                "success": False,
                "message": "Target not found"
            }
        
        # Get current mental debuffs
        debuffs = target.get("debuffs", {})
        mental_debuffs = []
        
        mental_types = ["fear", "charm", "confusion", "intimidation"]
        for debuff_type in mental_types:
            if debuffs.get(debuff_type, {}).get("active", False):
                mental_debuffs.append(debuff_type)
        
        if not mental_debuffs:
            return {
                "success": False,
                "message": "Target has no mental afflictions to cleanse"
            }
        
        # Clear target's debuffs
        unset_fields = {f"debuffs.{d}": "" for d in mental_debuffs}
        await self.db.players.update_one(
            {"_id": target_id},
            {"$unset": unset_fields}
        )
        
        # Apply to caster with 50% resistance chance
        import random
        resist_chance = 50 + (trait_level * 0.3)  # +0.3% per level
        resist_chance = min(95, resist_chance)
        
        transferred_debuffs = []
        resisted_debuffs = []
        
        for debuff in mental_debuffs:
            if random.randint(1, 100) > resist_chance:
                # Failed to resist, take the debuff
                await self.db.players.update_one(
                    {"_id": caster_id},
                    {
                        "$set": {
                            f"debuffs.{debuff}": {
                                "active": True,
                                "duration_seconds": 30,
                                "applied_at": datetime.utcnow()
                            }
                        }
                    }
                )
                transferred_debuffs.append(debuff)
            else:
                # Successfully resisted
                resisted_debuffs.append(debuff)
        
        # Grant karma bonus
        karma_gain = 10
        await self.db.players.update_one(
            {"_id": caster_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        return {
            "success": True,
            "message": "Emotional Shield activated - Ally cleansed",
            "debuffs_cleansed": mental_debuffs,
            "debuffs_transferred": transferred_debuffs,
            "debuffs_resisted": resisted_debuffs,
            "karma_gain": karma_gain,
            "target_username": target.get("username", "Unknown")
        }