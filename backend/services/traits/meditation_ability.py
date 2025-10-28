"""Meditation superpower ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import math

class MeditationAbility:
    """Implementation of Meditation superpower - Karmic Trace ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def karmic_trace(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Detect who performed negative actions against player.
        
        Tracks hackers, thieves, saboteurs who targeted this player.
        
        Args:
            player_id: ID of meditating player
            trait_level: Meditation trait level (affects range and accuracy)
        
        Returns:
            Dict with perpetrators list and tracking information
        """
        
        # Get player data
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "message": "Player not found",
                "perpetrators": []
            }
        
        # Look for recent violations (last hour)
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        
        # Find all trait actions against this player
        cursor = self.db.trait_usage_history.find({
            "target_id": player_id,
            "success": True,
            "used_at": {"$gte": cutoff_time},
            "karma_change": {"$lt": 0}  # Negative karma actions
        }).sort("used_at", -1).limit(10)
        
        violations = await cursor.to_list(length=10)
        
        if not violations:
            return {
                "success": True,
                "message": "No recent violations detected",
                "perpetrators": []
            }
        
        # Get perpetrator details with locations
        perpetrators = []
        player_position = player.get("position", {"x": 0, "y": 0, "z": 0})
        
        for violation in violations:
            perp_id = violation["player_id"]
            perp = await self.db.players.find_one({"_id": perp_id})
            
            if perp:
                perp_position = perp.get("position", {"x": 0, "y": 0, "z": 0})
                
                # Calculate distance and direction
                distance = self._calculate_distance(player_position, perp_position)
                direction = self._calculate_direction(player_position, perp_position)
                
                perpetrators.append({
                    "player_id": perp_id,
                    "username": perp.get("username", "Unknown"),
                    "action": violation["action_type"],
                    "trait_used": violation["trait_id"],
                    "karma_taken": abs(violation.get("karma_change", 0)),
                    "credits_stolen": violation.get("credits_affected", 0),
                    "damage_dealt": violation.get("damage_dealt", 0),
                    "time_ago_minutes": int((datetime.utcnow() - violation["used_at"]).total_seconds() / 60),
                    "current_distance": round(distance, 1),
                    "direction": direction,
                    "location": perp_position,
                    "karma_level": perp.get("karma", {}).get("current", 50),
                    "is_online": perp.get("status", {}).get("is_online", False)
                })
        
        return {
            "success": True,
            "message": f"Detected {len(perpetrators)} recent violations",
            "perpetrators": perpetrators,
            "tracking_duration_minutes": 30  # Can track for 30 minutes
        }
    
    def _calculate_distance(self, pos1: dict, pos2: dict) -> float:
        """Calculate 3D distance between positions."""
        dx = pos1.get("x", 0) - pos2.get("x", 0)
        dy = pos1.get("y", 0) - pos2.get("y", 0)
        dz = pos1.get("z", 0) - pos2.get("z", 0)
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def _calculate_direction(self, from_pos: dict, to_pos: dict) -> str:
        """Calculate cardinal direction to target."""
        dx = to_pos.get("x", 0) - from_pos.get("x", 0)
        dz = to_pos.get("z", 0) - from_pos.get("z", 0)
        
        # Calculate angle
        angle = math.degrees(math.atan2(dx, dz))
        
        # Normalize to 0-360
        if angle < 0:
            angle += 360
        
        # Convert to cardinal direction
        if 22.5 <= angle < 67.5:
            return "Northeast"
        elif 67.5 <= angle < 112.5:
            return "East"
        elif 112.5 <= angle < 157.5:
            return "Southeast"
        elif 157.5 <= angle < 202.5:
            return "South"
        elif 202.5 <= angle < 247.5:
            return "Southwest"
        elif 247.5 <= angle < 292.5:
            return "West"
        elif 292.5 <= angle < 337.5:
            return "Northwest"
        else:
            return "North"