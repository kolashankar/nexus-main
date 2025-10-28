"""Pride vice ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class PrideAbility:
    """Implementation of Pride vice - Superior Presence ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def superior_presence(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Assert dominance over weaker players, gaining buffs against lower-level opponents.
        
        Args:
            player_id: ID of prideful player
            trait_level: Pride trait level (1-100)
        
        Returns:
            Dict with success, buff_applied, affected_players, message
        """
        
        # Get player
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "buff_applied": False,
                "message": "Player not found"
            }
        
        player_level = player.get("level", 1)
        player_karma = player.get("karma", {}).get("current", 50)
        
        # Find nearby players with lower level
        nearby_players = await self.db.players.find({
            "_id": {"$ne": player_id},
            "location.map": player.get("location", {}).get("map"),
            "level": {"$lt": player_level}
        }).limit(20).to_list(20)
        
        if not nearby_players:
            return {
                "success": False,
                "buff_applied": False,
                "message": "No weaker players nearby to assert dominance over"
            }
        
        # Calculate buff strength based on level difference
        level_differences = [player_level - p.get("level", 1) for p in nearby_players]
        avg_level_diff = sum(level_differences) / len(level_differences)
        
        # Buff percentage (10-40% based on trait level and level differences)
        base_buff = 10 + (trait_level / 100) * 30
        level_bonus = min(20, avg_level_diff * 2)  # +2% per level difference, max +20%
        total_buff = int(base_buff + level_bonus)
        
        # Duration based on trait level (45-120 seconds)
        duration = 45 + int((trait_level / 100) * 75)
        
        # Apply buff to prideful player
        buff_data = {
            "type": "superior_presence",
            "damage_boost_percent": total_buff,
            "defense_boost_percent": int(total_buff * 0.5),
            "intimidation_aura": True,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "pride",
            "affected_players_count": len(nearby_players)
        }
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$push": {"buffs": buff_data}}
        )
        
        # Apply intimidation debuff to nearby weaker players
        player_name = player.get("profile", {}).get("name", "Unknown")
        
        for nearby in nearby_players:
            # Weaker players get intimidated
            debuff_data = {
                "type": "intimidated",
                "accuracy_penalty_percent": 15,
                "damage_penalty_percent": 10,
                "expires_at": datetime.utcnow().timestamp() + duration,
                "source_player_id": player_id
            }
            
            await self.db.players.update_one(
                {"_id": nearby["_id"]},
                {"$push": {"debuffs": debuff_data}}
            )
            
            # Notify intimidated player
            await self.db.notifications.insert_one({
                "player_id": nearby["_id"],
                "type": "intimidated",
                "message": f"{player_name}'s superior presence intimidates you!",
                "data": {
                    "intimidator_id": player_id,
                    "duration": duration,
                    "timestamp": datetime.utcnow()
                },
                "created_at": datetime.utcnow(),
                "read": False
            })
        
        # Karma penalty (pride is a vice, especially when used to oppress weaker players)
        karma_loss = random.randint(10, 18)
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"karma.current": -karma_loss}}
        )
        
        # Self notification
        await self.db.notifications.insert_one({
            "player_id": player_id,
            "type": "superior_presence_active",
            "message": f"Your pride empowers you! +{total_buff}% damage against {len(nearby_players)} weaker opponents",
            "data": {
                "buff_percent": total_buff,
                "affected_count": len(nearby_players),
                "duration": duration,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "buff_applied": True,
            "damage_buff_percent": total_buff,
            "defense_buff_percent": int(total_buff * 0.5),
            "affected_players": len(nearby_players),
            "duration": duration,
            "karma_loss": karma_loss,
            "message": f"Superior Presence activated! +{total_buff}% combat effectiveness vs {len(nearby_players)} weaker players"
        }
