"""Luck meta trait ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class LuckAbility:
    """Implementation of Luck meta trait - Fortune's Favor ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def fortunes_favor(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Activate fortune's favor for increased luck in all activities.
        
        Args:
            player_id: ID of lucky player
            trait_level: Luck trait level (1-100)
        
        Returns:
            Dict with success, luck_boost, duration, message
        """
        
        # Get player
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "luck_boost": 0,
                "message": "Player not found"
            }
        
        # Calculate luck boost (20-80% based on trait level)
        min_boost = 20
        max_boost = 80
        luck_boost = min_boost + (trait_level / 100) * (max_boost - min_boost)
        
        # Duration based on trait level (2-10 minutes)
        duration = 120 + int((trait_level / 100) * 480)
        
        # Apply fortune buff
        buff_data = {
            "type": "fortunes_favor",
            "luck_boost_percent": int(luck_boost),
            "critical_chance_bonus": 15,
            "loot_quality_bonus": 25,
            "success_rate_bonus": 20,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "luck",
            "visual_effect": "golden_sparkles"
        }
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$push": {"buffs": buff_data}}
        )
        
        # Small karma boost (being lucky is seen as blessed)
        karma_gain = random.randint(2, 5)
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        # Create notification
        await self.db.notifications.insert_one({
            "player_id": player_id,
            "type": "fortunes_favor_active",
            "message": f"✨ Fortune smiles upon you! +{int(luck_boost)}% luck for {duration//60} minutes",
            "data": {
                "luck_boost": int(luck_boost),
                "duration": duration,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "luck_boost": int(luck_boost),
            "duration": duration,
            "karma_gain": karma_gain,
            "message": f"Fortune's Favor activated! +{int(luck_boost)}% luck for {duration//60} minutes"
        }
    
    async def lucky_escape(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Passive ability: Chance to survive lethal damage with 1 HP.
        
        Args:
            player_id: ID of player
            trait_level: Luck trait level (1-100)
        
        Returns:
            Dict with success, escaped, message
        """
        
        # Calculate escape chance (10-35% based on trait level)
        escape_chance = 10 + (trait_level / 100) * 25
        
        # Roll for escape
        roll = random.randint(1, 100)
        escaped = roll <= escape_chance
        
        if escaped:
            # Set HP to 1 instead of 0
            await self.db.players.update_one(
                {"_id": player_id},
                {"$set": {"stats.hp": 1}}
            )
            
            # Notify player
            await self.db.notifications.insert_one({
                "player_id": player_id,
                "type": "lucky_escape",
                "message": "🍀 Incredible luck! You survived with 1 HP!",
                "data": {
                    "timestamp": datetime.utcnow()
                },
                "created_at": datetime.utcnow(),
                "read": False
            })
        
        return {
            "success": True,
            "escaped": escaped,
            "escape_chance": escape_chance,
            "message": "Lucky escape triggered!" if escaped else "Luck failed this time"
        }
    
    async def treasure_sense(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Sense nearby treasure or valuable items.
        
        Args:
            player_id: ID of player
            trait_level: Luck trait level (1-100)
        
        Returns:
            Dict with success, treasures_found, message
        """
        
        # Get player location
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "treasures_found": [],
                "message": "Player not found"
            }
        
        # Calculate detection range (50-200m based on trait level)
        detection_range = 50 + int((trait_level / 100) * 150)
        
        # Find nearby treasures/items
        # In production, would have actual treasure spawns
        treasures_found = []
        
        # Simulate finding treasures
        num_treasures = random.randint(0, 3 + int(trait_level / 33))
        for i in range(num_treasures):
            treasure = {
                "type": random.choice(["chest", "rare_item", "hidden_cache", "credits_pile"]),
                "distance": random.randint(20, detection_range),
                "direction": random.choice(["North", "South", "East", "West", "Northeast", "Northwest", "Southeast", "Southwest"]),
                "rarity": random.choice(["common", "uncommon", "rare", "epic"])
            }
            treasures_found.append(treasure)
        
        return {
            "success": True,
            "treasures_found": treasures_found,
            "detection_range": detection_range,
            "message": f"Detected {len(treasures_found)} treasures within {detection_range}m"
        }
