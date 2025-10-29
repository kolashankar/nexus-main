"""Trait unlock management service."""

from datetime import datetime
from typing import Dict, Any, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)

class UnlockManager:
    """Manages trait-based unlocks and abilities."""
    
    # Define all trait unlocks
    TRAIT_UNLOCKS = {
        "courage": {
            50: {
                "name": "Brave Heart",
                "type": "ability",
                "description": "Increases combat effectiveness by 20% and unlocks brave dialogue options",
                "effects": ["+20% combat damage", "Unlock brave task choices", "Intimidation resistance"]
            },
            75: {
                "name": "Fearless Warrior",
                "type": "ability",
                "description": "Master courage ability: immune to fear effects and +30% combat effectiveness",
                "effects": ["+30% combat damage", "Fear immunity", "Counter-attack chance"]
            },
            100: {
                "name": "Legend of Valor",
                "type": "title",
                "description": "Master of courage: Maximum combat bonuses and legendary status",
                "effects": ["+50% combat effectiveness", "Inspire allies", "Legendary reputation"]
            }
        },
        "wisdom": {
            50: {
                "name": "Sage Insight",
                "type": "ability",
                "description": "Gain 15% more XP and unlock strategic task options",
                "effects": ["+15% XP gain", "Better decision insights", "Predict outcomes"]
            },
            75: {
                "name": "Master Strategist",
                "type": "ability",
                "description": "Advanced wisdom: 25% XP bonus and foresight abilities",
                "effects": ["+25% XP gain", "Advanced insights", "Optimal path guidance"]
            },
            100: {
                "name": "Ancient Sage",
                "type": "title",
                "description": "Master of wisdom: Maximum learning bonuses and sage reputation",
                "effects": ["+40% XP gain", "Perfect foresight", "Mentor others"]
            }
        },
        "compassion": {
            50: {
                "name": "Healing Touch",
                "type": "ability",
                "description": "Can heal others and receive karma bonuses for helping",
                "effects": ["Heal 40 HP to others", "+20% karma gains", "Empathy sensing"]
            },
            75: {
                "name": "Divine Healer",
                "type": "ability",
                "description": "Advanced healing and massive karma bonuses",
                "effects": ["Heal 80 HP", "+40% karma gains", "Group healing"]
            },
            100: {
                "name": "Saint",
                "type": "title",
                "description": "Master of compassion: Ultimate healing and saintly reputation",
                "effects": ["Revive fallen allies", "+100% karma gains", "Divine protection"]
            }
        },
        "strength": {
            50: {
                "name": "Iron Fist",
                "type": "ability",
                "description": "Increased physical damage and intimidation options",
                "effects": ["+25% physical damage", "Break obstacles", "Intimidate enemies"]
            },
            75: {
                "name": "Titan's Power",
                "type": "ability",
                "description": "Massive strength bonuses and devastating attacks",
                "effects": ["+40% physical damage", "Stun enemies", "Lift heavy objects"]
            },
            100: {
                "name": "Colossus",
                "type": "title",
                "description": "Master of strength: Unmatched physical power",
                "effects": ["+75% physical damage", "Earthquake strike", "Unstoppable force"]
            }
        },
        "intelligence": {
            50: {
                "name": "Quick Learner",
                "type": "ability",
                "description": "Learn skills faster and unlock hacking abilities",
                "effects": ["+20% skill learning", "Basic hacking", "Puzzle solving"]
            },
            75: {
                "name": "Genius Mind",
                "type": "ability",
                "description": "Advanced learning and superior hacking",
                "effects": ["+35% skill learning", "Advanced hacking", "AI manipulation"]
            },
            100: {
                "name": "Mastermind",
                "type": "title",
                "description": "Master of intelligence: Supreme mental abilities",
                "effects": ["+60% skill learning", "Master hacking", "Control systems"]
            }
        }
    }
    
    async def check_unlocks(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        trait: str,
        new_value: float,
        old_value: float
    ) -> List[Dict[str, Any]]:
        """Check if any unlocks were triggered."""
        unlocks = []
        
        if trait not in self.TRAIT_UNLOCKS:
            return unlocks
        
        trait_unlocks = self.TRAIT_UNLOCKS[trait]
        
        for threshold, unlock_data in trait_unlocks.items():
            if old_value < threshold <= new_value:
                unlock = await self._create_unlock(
                    db, player_id, trait, threshold, unlock_data
                )
                unlocks.append(unlock)
        
        return unlocks
    
    async def _create_unlock(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        trait: str,
        threshold: int,
        unlock_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create an unlock record."""
        unlock = {
            "player_id": player_id,
            "trait": trait,
            "threshold": threshold,
            "name": unlock_data["name"],
            "type": unlock_data["type"],
            "description": unlock_data["description"],
            "effects": unlock_data["effects"],
            "unlocked_at": datetime.utcnow(),
            "is_active": True,
            "acknowledged": False
        }
        
        # Save unlock
        await db.trait_unlocks.insert_one(unlock)
        
        # Add to player's unlocked abilities
        await db.players.update_one(
            {"_id": player_id},
            {
                "$addToSet": {
                    "unlocked_abilities": f"{trait}_{threshold}"
                }
            }
        )
        
        logger.info(f"🔓 Unlock: {player_id} - {unlock_data['name']} ({trait} {threshold})")
        
        return unlock
    
    async def get_player_unlocks(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        unacknowledged_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get all unlocks for a player."""
        query = {"player_id": player_id}
        if unacknowledged_only:
            query["acknowledged"] = False
        
        unlocks = await db.trait_unlocks.find(query).sort(
            "unlocked_at", -1
        ).to_list(length=None)
        
        return unlocks
    
    async def acknowledge_unlock(
        self,
        db: AsyncIOMotorDatabase,
        unlock_id: str
    ):
        """Mark an unlock as acknowledged."""
        await db.trait_unlocks.update_one(
            {"_id": unlock_id},
            {"$set": {"acknowledged": True}}
        )
    
    async def is_ability_unlocked(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        trait: str,
        threshold: int
    ) -> bool:
        """Check if a specific ability is unlocked."""
        unlock = await db.trait_unlocks.find_one({
            "player_id": player_id,
            "trait": trait,
            "threshold": threshold
        })
        
        return unlock is not None
    
    async def get_available_unlocks(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get all available unlocks based on current traits."""
        player = await db.players.find_one({"_id": player_id})
        if not player:
            return {}
        
        traits = player.get("traits", {})
        available = {}
        
        for trait, unlocks in self.TRAIT_UNLOCKS.items():
            trait_value = traits.get(trait, 0)
            trait_unlocks = []
            
            for threshold, unlock_data in unlocks.items():
                is_unlocked = await self.is_ability_unlocked(db, player_id, trait, threshold)
                
                trait_unlocks.append({
                    "threshold": threshold,
                    "name": unlock_data["name"],
                    "type": unlock_data["type"],
                    "description": unlock_data["description"],
                    "effects": unlock_data["effects"],
                    "is_unlocked": is_unlocked,
                    "current_value": trait_value,
                    "can_unlock": trait_value >= threshold,
                    "progress": min(100, (trait_value / threshold) * 100)
                })
            
            available[trait] = trait_unlocks
        
        return available
