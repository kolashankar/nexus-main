"""Leadership skill ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, List
from datetime import datetime, timedelta

class LeadershipAbility:
    """Implementation of Leadership skill - Rally Cry ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def rally_cry(
        self,
        leader_id: str,
        leader_position: dict,
        trait_level: int
    ) -> Dict:
        """Buff all party/guild members within range.
        
        Args:
            leader_id: ID of leader using ability
            leader_position: Leader's current position
            trait_level: Leadership trait level
        
        Returns:
            Dict with success, allies_buffed, and buff details
        """
        
        # Get leader's party/guild
        leader = await self.db.players.find_one({"_id": leader_id})
        if not leader:
            return {
                "success": False,
                "message": "Leader not found"
            }
        
        # Get allies (party members or guild members)
        party_members = leader.get("party", {}).get("members", [])
        guild_id = leader.get("guild", {}).get("guild_id")
        
        # Find nearby allies
        range_meters = 200
        allies_query = {
            "_id": {"$ne": leader_id},
            "status.is_online": True,
            "$or": [
                {"_id": {"$in": party_members}},
                {"guild.guild_id": guild_id} if guild_id else {"_id": {"$in": []}}
            ]
        }
        
        cursor = self.db.players.find(allies_query)
        all_allies = await cursor.to_list(length=None)
        
        # Filter by range
        buffed_allies = []
        buff_duration = timedelta(minutes=10)
        buff_expires = datetime.utcnow() + buff_duration
        
        for ally in all_allies:
            if "position" in ally:
                distance = self._calculate_distance(
                    leader_position,
                    ally["position"]
                )
                
                if distance <= range_meters:
                    # Apply buff
                    await self.db.players.update_one(
                        {"_id": ally["_id"]},
                        {
                            "$set": {
                                "buffs.rally_cry": {
                                    "active": True,
                                    "stat_bonus": 15,  # +15% all stats
                                    "expires_at": buff_expires,
                                    "from_leader": leader_id
                                }
                            }
                        }
                    )
                    
                    buffed_allies.append({
                        "player_id": ally["_id"],
                        "username": ally.get("username", "Unknown"),
                        "distance": round(distance, 1)
                    })
        
        if len(buffed_allies) == 0:
            return {
                "success": False,
                "message": "No allies nearby to buff (need at least 2 allies within 200m)"
            }
        
        # Apply karma bonus
        await self.db.players.update_one(
            {"_id": leader_id},
            {"$inc": {"karma.current": 5}}
        )
        
        return {
            "success": True,
            "message": f"Rally Cry activated! {len(buffed_allies)} allies buffed",
            "allies_buffed": buffed_allies,
            "buff_bonus": "+15% to all stats",
            "duration_minutes": 10,
            "karma_gain": 5
        }
    
    def _calculate_distance(self, pos1: dict, pos2: dict) -> float:
        """Calculate distance between positions."""
        import math
        dx = pos1.get("x", 0) - pos2.get("x", 0)
        dy = pos1.get("y", 0) - pos2.get("y", 0)
        dz = pos1.get("z", 0) - pos2.get("z", 0)
        return math.sqrt(dx*dx + dy*dy + dz*dz)