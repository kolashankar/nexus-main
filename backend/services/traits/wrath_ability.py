"""Wrath vice ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class WrathAbility:
    """Implementation of Wrath vice - Berserker Rage ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def berserker_rage(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Enter berserker rage state with massive damage boost but reduced defense.
        
        Args:
            player_id: ID of player activating rage
            trait_level: Wrath trait level (1-100)
        
        Returns:
            Dict with success, damage_boost, defense_penalty, duration, message
        """
        
        # Get player
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "damage_boost": 0,
                "message": "Player not found"
            }
        
        # Calculate damage boost (50-150% based on trait level)
        min_boost = 50
        max_boost = 150
        damage_boost = min_boost + (trait_level / 100) * (max_boost - min_boost)
        
        # Defense penalty (30-50% reduction)
        defense_penalty = 30 + (trait_level / 100) * 20
        
        # Duration based on trait level (15-45 seconds)
        duration = 15 + int((trait_level / 100) * 30)
        
        # Check current HP - more damage bonus when low HP
        current_hp = player.get("stats", {}).get("hp", 100)
        max_hp = player.get("stats", {}).get("max_hp", 100)
        hp_percent = (current_hp / max_hp) * 100
        
        # Bonus damage when injured (enraged by pain)
        if hp_percent < 50:
            rage_bonus = int(damage_boost * 0.3)  # +30% more damage
            damage_boost += rage_bonus
        
        # Apply buff
        buff_data = {
            "type": "berserker_rage",
            "damage_boost_percent": int(damage_boost),
            "defense_penalty_percent": int(defense_penalty),
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "wrath",
            "visual_effect": "red_aura"
        }
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$push": {"buffs": buff_data}}
        )
        
        # Apply moderate karma penalty (violence-based)
        karma_loss = random.randint(5, 12)
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"karma.current": -karma_loss}}
        )
        
        # Create self-notification with warning
        await self.db.notifications.insert_one({
            "player_id": player_id,
            "type": "berserker_rage_active",
            "message": f"BERSERKER RAGE ACTIVATED! +{int(damage_boost)}% damage, -{int(defense_penalty)}% defense",
            "data": {
                "damage_boost": int(damage_boost),
                "defense_penalty": int(defense_penalty),
                "duration": duration,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        # Notify nearby players (intimidation effect)
        nearby_players = await self.db.players.find({
            "_id": {"$ne": player_id},
            "location.map": player.get("location", {}).get("map"),
            # In production, would add distance calculation here
        }).limit(10).to_list(10)
        
        player_name = player.get("profile", {}).get("name", "Unknown")
        for nearby in nearby_players:
            await self.db.notifications.insert_one({
                "player_id": nearby["_id"],
                "type": "berserker_nearby",
                "message": f"⚠️ {player_name} has entered BERSERKER RAGE nearby!",
                "data": {
                    "raging_player_id": player_id,
                    "timestamp": datetime.utcnow()
                },
                "created_at": datetime.utcnow(),
                "read": False
            })
        
        return {
            "success": True,
            "damage_boost": int(damage_boost),
            "defense_penalty": int(defense_penalty),
            "duration": duration,
            "karma_loss": karma_loss,
            "message": f"RAGE ACTIVATED! +{int(damage_boost)}% damage for {duration}s - BEWARE: -{int(defense_penalty)}% defense!"
        }
