"""Player profile service."""

from typing import Optional, Dict, Any
from datetime import datetime
from backend.core.database import get_database
from fastapi import HTTPException

class PlayerProfileService:
    """Service for managing player profiles."""

    def __init__(self):
        self.db = get_database()
        self.collection = self.db.players

    async def get_player_by_id(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get player by ID."""
        try:
            player = await self.collection.find_one({"_id": player_id})
            return player
        except Exception as e:
            print(f"Error getting player: {e}")
            return None

    async def get_player_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get player by username."""
        try:
            player = await self.collection.find_one({"username": username})
            if player:
                player["_id"] = str(player["_id"])
            return player
        except Exception as e:
            print(f"Error getting player: {e}")
            return None

    async def update_player(self, player_id: str, update_data: Dict[str, Any]) -> bool:
        """Update player data."""
        try:
            update_data["last_action"] = datetime.utcnow()
            result = await self.collection.update_one(
                {"_id": player_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating player: {e}")
            return False

    async def update_visibility(self, player_id: str, visibility_settings: Dict[str, Any]) -> bool:
        """Update player visibility settings."""
        return await self.update_player(
            player_id,
            {"visibility": visibility_settings}
        )

    async def get_online_players(self, limit: int = 50) -> list:
        """Get online players."""
        try:
            cursor = self.collection.find({"online": True}).limit(limit)
            players = await cursor.to_list(length=limit)
            for player in players:
                player["_id"] = str(player["_id"])
            return players
        except Exception as e:
            print(f"Error getting online players: {e}")
            return []

    async def set_online_status(self, player_id: str, online: bool) -> bool:
        """Set player online status."""
        try:
            result = await self.collection.update_one(
                {"_id": player_id},
                {
                    "$set": {
                        "online": online,
                        "last_action": datetime.utcnow()
                    }
                }
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error setting online status: {e}")
            return False

    async def get_full_profile(self, player_id: str) -> Dict:
        """Get player's complete profile."""
        player_dict = await self.collection.find_one({"_id": player_id})
        if not player_dict:
            raise HTTPException(status_code=404, detail="Player not found")

        return {
            "id": player_dict["_id"],
            "username": player_dict["username"],
            "email": player_dict["email"],
            "level": player_dict["level"],
            "xp": player_dict["xp"],
            "prestige_level": player_dict["prestige_level"],
            "economic_class": player_dict["economic_class"],
            "moral_class": player_dict["moral_class"],
            "currencies": player_dict["currencies"],
            "karma_points": player_dict["karma_points"],
            "traits": player_dict["traits"],
            "meta_traits": player_dict["meta_traits"],
            "visibility": player_dict["visibility"],
            "stats": player_dict["stats"],
            "online": player_dict["online"],
            "last_login": player_dict.get("last_login")
        }

    async def update_profile(self, player_id: str, update_data: any) -> Dict:
        """Update player profile."""
        update_dict = {}

        if hasattr(update_data, 'economic_class') and update_data.economic_class:
            update_dict["economic_class"] = update_data.economic_class
        if hasattr(update_data, 'moral_class') and update_data.moral_class:
            update_dict["moral_class"] = update_data.moral_class

        if not update_dict:
            raise HTTPException(
                status_code=400, detail="No valid updates provided")

        await self.collection.update_one(
            {"_id": player_id},
            {"$set": update_dict}
        )

        return await self.get_full_profile(player_id)

    async def get_player_stats(self, player_id: str) -> Dict:
        """Get player statistics."""
        player_dict = await self.collection.find_one({"_id": player_id})
        if not player_dict:
            raise HTTPException(status_code=404, detail="Player not found")

        return {
            "id": player_dict["_id"],
            "username": player_dict["username"],
            "level": player_dict["level"],
            "xp": player_dict["xp"],
            "stats": player_dict["stats"],
            "total_karma": player_dict["karma_points"],
            "rank": None  # Will be calculated later
        }


# Backward compatibility alias
PlayerService = PlayerProfileService
