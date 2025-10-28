"""Resilience meta trait ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class ResilienceAbility:
    """Implementation of Resilience meta trait - Unbreakable Will ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def unbreakable_will(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Activate unbreakable will to resist debuffs and recover faster.
        
        Args:
            player_id: ID of resilient player
            trait_level: Resilience trait level (1-100)
        
        Returns:
            Dict with success, resistance_boost, debuffs_removed, message
        """
        
        # Get player
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "resistance_boost": 0,
                "message": "Player not found"
            }
        
        # Calculate resistance boost (30-80% based on trait level)
        min_resistance = 30
        max_resistance = 80
        resistance_boost = min_resistance + (trait_level / 100) * (max_resistance - min_resistance)
        
        # Remove existing debuffs based on trait level
        current_debuffs = player.get("debuffs", [])
        debuffs_to_remove = int(len(current_debuffs) * (trait_level / 100))
        debuffs_removed = min(debuffs_to_remove, len(current_debuffs))
        
        # Remove debuffs
        if debuffs_removed > 0:
            remaining_debuffs = current_debuffs[debuffs_removed:]
            await self.db.players.update_one(
                {"_id": player_id},
                {"$set": {"debuffs": remaining_debuffs}}
            )
        
        # Duration based on trait level (60-180 seconds)
        duration = 60 + int((trait_level / 100) * 120)
        
        # Apply resilience buff
        buff_data = {
            "type": "unbreakable_will",
            "debuff_resistance_percent": int(resistance_boost),
            "damage_reduction_percent": 20,
            "hp_regen_boost_percent": 50,
            "immunity_to_fear": True,
            "immunity_to_charm": True,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "resilience",
            "visual_effect": "iron_aura"
        }
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$push": {"buffs": buff_data}}
        )
        
        # Small karma boost (resilience is admirable)
        karma_gain = random.randint(3, 8)
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        # Create notification
        await self.db.notifications.insert_one({
            "player_id": player_id,
            "type": "unbreakable_will_active",
            "message": f"💪 Unbreakable Will! {debuffs_removed} debuffs removed, +{int(resistance_boost)}% resistance for {duration}s",
            "data": {
                "resistance_boost": int(resistance_boost),
                "debuffs_removed": debuffs_removed,
                "duration": duration,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "resistance_boost": int(resistance_boost),
            "debuffs_removed": debuffs_removed,
            "duration": duration,
            "karma_gain": karma_gain,
            "message": f"Unbreakable Will activated! {debuffs_removed} debuffs removed, +{int(resistance_boost)}% resistance"
        }
    
    async def damage_threshold(
        self,
        player_id: str,
        incoming_damage: int,
        trait_level: int
    ) -> Dict:
        """Passive ability: Reduce large damage spikes.
        
        Args:
            player_id: ID of player
            incoming_damage: Amount of damage before reduction
            trait_level: Resilience trait level (1-100)
        
        Returns:
            Dict with success, final_damage, damage_reduced, message
        """
        
        # Get player stats
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "final_damage": incoming_damage,
                "message": "Player not found"
            }
        
        max_hp = player.get("stats", {}).get("max_hp", 100)
        
        # Calculate damage threshold (30-60% of max HP based on trait level)
        threshold_percent = 30 + (trait_level / 100) * 30
        damage_threshold = int(max_hp * (threshold_percent / 100))
        
        # If damage exceeds threshold, reduce it
        if incoming_damage > damage_threshold:
            # Reduce damage by 20-50% based on trait level
            reduction_percent = 20 + (trait_level / 100) * 30
            damage_reduced = int(incoming_damage * (reduction_percent / 100))
            final_damage = incoming_damage - damage_reduced
            
            # Notify player
            await self.db.notifications.insert_one({
                "player_id": player_id,
                "type": "resilience_activated",
                "message": f"🛡️ Resilience reduced incoming damage by {damage_reduced}!",
                "data": {
                    "original_damage": incoming_damage,
                    "reduced_damage": damage_reduced,
                    "final_damage": final_damage,
                    "timestamp": datetime.utcnow()
                },
                "created_at": datetime.utcnow(),
                "read": False
            })
            
            return {
                "success": True,
                "final_damage": final_damage,
                "damage_reduced": damage_reduced,
                "threshold_triggered": True,
                "message": f"Resilience activated! Reduced {damage_reduced} damage"
            }
        else:
            return {
                "success": True,
                "final_damage": incoming_damage,
                "damage_reduced": 0,
                "threshold_triggered": False,
                "message": "Damage below threshold, no reduction"
            }
