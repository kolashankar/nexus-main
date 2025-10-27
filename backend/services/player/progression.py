from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict
from fastapi import HTTPException
import math

class ProgressionService:
    """Service for managing player progression (XP, levels)."""

    @staticmethod
    def calculate_xp_for_level(level: int) -> int:
        """Calculate total XP needed for a specific level."""
        # Formula: XP = 100 * level^2
        return 100 * (level ** 2)

    @staticmethod
    def calculate_level_from_xp(xp: int) -> int:
        """Calculate level from XP amount."""
        # Inverse formula: level = sqrt(XP / 100)
        level = int(math.sqrt(xp / 100))
        return max(1, min(100, level))  # Clamp between 1 and 100

    async def add_xp(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        xp_amount: int
    ) -> Dict:
        """Add XP to player and handle level ups."""
        # Get current player
        player_dict = await db.players.find_one({"_id": player_id})
        if not player_dict:
            raise HTTPException(status_code=404, detail="Player not found")

        current_xp = player_dict["xp"]
        current_level = player_dict["level"]

        # Add XP
        new_xp = current_xp + xp_amount
        new_level = self.calculate_level_from_xp(new_xp)

        # Check for level up
        leveled_up = new_level > current_level
        levels_gained = new_level - current_level if leveled_up else 0

        # Update player
        await db.players.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "xp": new_xp,
                    "level": new_level
                }
            }
        )

        return {
            "xp_gained": xp_amount,
            "total_xp": new_xp,
            "current_level": new_level,
            "leveled_up": leveled_up,
            "levels_gained": levels_gained,
            "message": f"Gained {xp_amount} XP!" + (f" Level up! Now level {new_level}!" if leveled_up else "")
        }

    async def get_progression_info(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str
    ) -> Dict:
        """Get player's progression information."""
        player_dict = await db.players.find_one({"_id": player_id})
        if not player_dict:
            raise HTTPException(status_code=404, detail="Player not found")

        current_xp = player_dict["xp"]
        current_level = player_dict["level"]

        # Calculate XP for current and next level
        xp_for_current = self.calculate_xp_for_level(current_level)
        xp_for_next = self.calculate_xp_for_level(current_level + 1)

        # XP progress in current level
        xp_in_level = current_xp - xp_for_current
        xp_needed = xp_for_next - xp_for_current
        progress_percentage = (xp_in_level / xp_needed * \
                               100) if xp_needed > 0 else 0

        return {
            "level": current_level,
            "total_xp": current_xp,
            "xp_for_current_level": xp_for_current,
            "xp_for_next_level": xp_for_next,
            "xp_in_current_level": xp_in_level,
            "xp_needed_for_next": xp_needed,
            "progress_percentage": round(progress_percentage, 2)
        }