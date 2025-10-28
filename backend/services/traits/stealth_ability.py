"""Stealth skill ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict
from datetime import datetime, timedelta
import random

class StealthAbility:
    """Implementation of Stealth skill - Shadow Walk ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def shadow_walk(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Enter stealth mode - become invisible to other players.
        
        Args:
            player_id: ID of stealthing player
            trait_level: Stealth trait level (affects duration)
        
        Returns:
            Dict with success, duration, and stealth status
        """
        
        # Calculate duration (20-40 seconds based on level)
        base_duration = 20
        level_bonus = (trait_level - 1) * 0.2  # +0.2 seconds per level
        duration_seconds = int(base_duration + level_bonus)
        duration_seconds = min(40, duration_seconds)
        
        # Set stealth status
        expires_at = datetime.utcnow() + timedelta(seconds=duration_seconds)
        
        await self.db.players.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "status.is_stealthed": True,
                    "status.stealth_expires_at": expires_at,
                    "status.stealth_level": trait_level,
                    "status.movement_speed_modifier": 0.5  # -50% speed
                }
            }
        )
        
        return {
            "success": True,
            "message": "Shadow Walk activated - You are invisible",
            "duration_seconds": duration_seconds,
            "expires_at": expires_at.isoformat(),
            "movement_speed": "50% (reduced)",
            "detection_warning": "Players with Perception 80+ can detect you"
        }
    
    async def break_stealth(self, player_id: str) -> Dict:
        """Break stealth mode (attacking or interacting)."""
        
        result = await self.db.players.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "status.is_stealthed": False,
                    "status.movement_speed_modifier": 1.0
                },
                "$unset": {
                    "status.stealth_expires_at": "",
                    "status.stealth_level": ""
                }
            }
        )
        
        return {
            "success": True,
            "message": "Stealth broken"
        }