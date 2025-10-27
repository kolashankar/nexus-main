from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict
from fastapi import HTTPException

class VisibilityService:
    """Service for managing player visibility/privacy settings."""

    PRIVACY_TIERS = {
        "public": {
            "description": "Everything visible",
            "cost": 0,
            "defaults": {
                "cash": True,
                "economic_class": True,
                "moral_class": True,
                "karma_score": True,
                "guild": True,
                "location": True
            }
        },
        "selective": {
            "description": "Choose what to show",
            "cost": 10,  # credits per day
            "defaults": {
                "cash": False,
                "economic_class": True,
                "moral_class": True,
                "karma_score": False,
                "guild": True,
                "location": True
            }
        },
        "private": {
            "description": "Most things hidden",
            "cost": 50,
            "defaults": {
                "cash": False,
                "economic_class": False,
                "moral_class": False,
                "karma_score": False,
                "guild": True,
                "location": False
            }
        },
        "ghost": {
            "description": "Nearly invisible",
            "cost": 200,
            "defaults": {
                "cash": False,
                "economic_class": False,
                "moral_class": False,
                "karma_score": False,
                "guild": False,
                "location": False
            }
        },
        "phantom": {
            "description": "Untraceable",
            "cost": 1000,
            "defaults": {
                "cash": False,
                "economic_class": False,
                "moral_class": False,
                "karma_score": False,
                "guild": False,
                "location": False
            }
        }
    }

    async def update_visibility(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        updates: Dict
    ) -> Dict:
        """Update player's visibility settings."""
        # Get current player
        player_dict = await db.players.find_one({"_id": player_id})
        if not player_dict:
            raise HTTPException(status_code=404, detail="Player not found")

        update_dict = {}

        # Handle privacy tier change
        if "privacy_tier" in updates and updates["privacy_tier"]:
            tier = updates["privacy_tier"]
            if tier not in self.PRIVACY_TIERS:
                raise HTTPException(
                    status_code=400, detail="Invalid privacy tier")

            # Check if player can afford this tier
            tier_cost = self.PRIVACY_TIERS[tier]["cost"]
            player_credits = player_dict.get(
                "currencies", {}).get("credits", 0)

            if player_credits < tier_cost:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient credits. Need {tier_cost}, have {player_credits}"
                )

            # Apply tier defaults
            defaults = self.PRIVACY_TIERS[tier]["defaults"]
            update_dict["visibility.privacy_tier"] = tier
            for key, value in defaults.items():
                update_dict[f"visibility.{key}"] = value

        # Apply individual setting updates
        for key, value in updates.items():
            if key != "privacy_tier" and value is not None:
                update_dict[f"visibility.{key}"] = value

        if not update_dict:
            return {"message": "No changes made"}

        # Update database
        await db.players.update_one(
            {"_id": player_id},
            {"$set": update_dict}
        )

        # Get updated visibility
        updated_player = await db.players.find_one({"_id": player_id})

        return {
            "message": "Visibility settings updated",
            "visibility": updated_player.get("visibility", {})
        }

    async def get_visibility(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str
    ) -> Dict:
        """Get player's current visibility settings."""
        player_dict = await db.players.find_one({"_id": player_id})
        if not player_dict:
            raise HTTPException(status_code=404, detail="Player not found")

        visibility = player_dict.get("visibility", {})
        current_tier = visibility.get("privacy_tier", "public")

        return {
            "current_settings": visibility,
            "current_tier": current_tier,
            "tier_info": self.PRIVACY_TIERS.get(current_tier, {}),
            "available_tiers": self.PRIVACY_TIERS
        }

    def can_see_data(
        self,
        viewer_id: str,
        target_player_dict: Dict,
        data_type: str
    ) -> bool:
        """Check if viewer can see specific data about target player."""
        # Players can always see their own data
        if viewer_id == target_player_dict.get("_id"):
            return True

        visibility = target_player_dict.get("visibility", {})

        # Check specific visibility setting
        return visibility.get(data_type, False)