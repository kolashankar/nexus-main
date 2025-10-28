"""Honesty virtue ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class HonestyAbility:
    """Implementation of Honesty virtue - Truth Reveal ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def truth_reveal(
        self,
        revealer_id: str,
        target_id: str,
        revealer_trait_level: int
    ) -> Dict:
        """Reveal hidden information about target player.
        
        Args:
            revealer_id: ID of player using ability
            target_id: ID of target player to analyze
            revealer_trait_level: Honesty trait level (1-100)
        
        Returns:
            Dict with success, revealed_info, karma_alignment, message
        """
        
        # Get target player
        target = await self.db.players.find_one({"_id": target_id})
        if not target:
            return {
                "success": False,
                "revealed_info": {},
                "message": "Target player not found"
            }
        
        # Get revealer
        revealer = await self.db.players.find_one({"_id": revealer_id})
        if not revealer:
            return {
                "success": False,
                "revealed_info": {},
                "message": "Revealer not found"
            }
        
        # Calculate what information is revealed based on trait level
        revealed_info = {}
        
        # Basic info (available at level 1+)
        if revealer_trait_level >= 1:
            revealed_info["karma"] = target.get("karma", {}).get("current", 50)
            revealed_info["level"] = target.get("level", 1)
        
        # Intermediate info (available at level 25+)
        if revealer_trait_level >= 25:
            revealed_info["credits"] = target.get("economy", {}).get("credits", 0)
            revealed_info["alignment"] = self._get_alignment(target.get("karma", {}).get("current", 50))
        
        # Advanced info (available at level 50+)
        if revealer_trait_level >= 50:
            recent_actions = await self.db.action_logs.find(
                {"player_id": target_id}
            ).sort("timestamp", -1).limit(5).to_list(5)
            
            revealed_info["recent_actions"] = [
                {
                    "action": action.get("action_type", "unknown"),
                    "karma_change": action.get("karma_change", 0)
                }
                for action in recent_actions
            ]
        
        # Expert info (available at level 75+)
        if revealer_trait_level >= 75:
            equipped_traits = target.get("traits", {}).get("equipped", [])
            revealed_info["equipped_traits"] = equipped_traits
            revealed_info["weaknesses"] = self._analyze_weaknesses(target)
        
        # Determine karma alignment
        target_karma = target.get("karma", {}).get("current", 50)
        revealer_karma = revealer.get("karma", {}).get("current", 50)
        
        # Karma gain for honest players revealing dishonest ones
        karma_gain = 0
        if revealer_karma >= 60 and target_karma < 40:
            karma_gain = random.randint(5, 10)
            await self.db.players.update_one(
                {"_id": revealer_id},
                {"$inc": {"karma.current": karma_gain}}
            )
        
        # Notify target that they were analyzed
        revealer_name = revealer.get("profile", {}).get("name", "Unknown")
        await self.db.notifications.insert_one({
            "player_id": target_id,
            "type": "truth_revealed",
            "message": f"{revealer_name} used Truth Reveal on you",
            "data": {
                "revealer_id": revealer_id,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "revealed_info": revealed_info,
            "karma_gain": karma_gain,
            "message": "Truth revealed successfully"
        }
    
    def _get_alignment(self, karma: int) -> str:
        """Get alignment string based on karma value."""
        if karma >= 80:
            return "Saint"
        elif karma >= 60:
            return "Good"
        elif karma >= 40:
            return "Neutral"
        elif karma >= 20:
            return "Evil"
        else:
            return "Corrupted"
    
    def _analyze_weaknesses(self, target: Dict) -> list:
        """Analyze target's weaknesses based on their stats and traits."""
        weaknesses = []
        stats = target.get("stats", {})
        
        # Check for low stats
        if stats.get("defense", 50) < 30:
            weaknesses.append("Low physical defense")
        if stats.get("speed", 50) < 30:
            weaknesses.append("Slow movement")
        if stats.get("perception", 50) < 30:
            weaknesses.append("Poor awareness")
        
        # Check for negative traits
        traits = target.get("traits", {}).get("acquired", {})
        if "greed" in traits and traits["greed"] > 50:
            weaknesses.append("Vulnerable to money traps")
        if "wrath" in traits and traits["wrath"] > 50:
            weaknesses.append("Easily provoked")
        
        return weaknesses if weaknesses else ["No obvious weaknesses detected"]
