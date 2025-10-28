"""Integrity virtue ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict
from datetime import datetime, timedelta

class IntegrityAbility:
    """Implementation of Integrity virtue - Unbreakable Will ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def unbreakable_will(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Become immune to all control effects.
        
        Args:
            player_id: Player activating ability
            trait_level: Integrity trait level
        
        Returns:
            Dict with success and immunity details
        """
        
        duration_seconds = 30
        expires_at = datetime.utcnow() + timedelta(seconds=duration_seconds)
        
        # Clear any existing control effects
        await self.db.players.update_one(
            {"_id": player_id},
            {
                "$unset": {
                    "debuffs.mind_control": "",
                    "debuffs.charm": "",
                    "debuffs.fear": "",
                    "debuffs.confusion": "",
                    "debuffs.intimidation": ""
                },
                "$set": {
                    "buffs.unbreakable_will": {
                        "active": True,
                        "expires_at": expires_at,
                        "immunity": ["mind_control", "charm", "fear", "confusion", "intimidation"],
                        "damage_bonus_corrupted": 25
                    }
                }
            }
        )
        
        # Grant karma bonus
        karma_gain = 8
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        return {
            "success": True,
            "message": "Unbreakable Will activated - You are incorruptible",
            "duration_seconds": duration_seconds,
            "immunities": ["Mind Control", "Charm", "Fear", "Confusion", "Intimidation"],
            "bonus": "+25% damage to corrupted enemies",
            "karma_gain": karma_gain
        }