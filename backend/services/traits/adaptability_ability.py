"""Adaptability meta trait ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class AdaptabilityAbility:
    """Implementation of Adaptability meta trait - Quick Adaptation ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def quick_adaptation(
        self,
        player_id: str,
        situation: str,
        trait_level: int
    ) -> Dict:
        """Quickly adapt to new situations with dynamic stat adjustments.
        
        Args:
            player_id: ID of adaptive player
            situation: Current situation (combat, exploration, social, survival)
            trait_level: Adaptability trait level (1-100)
        
        Returns:
            Dict with success, adaptations, duration, message
        """
        
        # Get player
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "adaptations": {},
                "message": "Player not found"
            }
        
        # Calculate adaptation strength (20-60% based on trait level)
        min_adaptation = 20
        max_adaptation = 60
        adaptation_strength = min_adaptation + (trait_level / 100) * (max_adaptation - min_adaptation)
        
        # Duration based on trait level (60-240 seconds)
        duration = 60 + int((trait_level / 100) * 180)
        
        # Generate situation-specific adaptations
        adaptations = self._get_adaptations_for_situation(situation, adaptation_strength)
        
        # Apply adaptation buff
        buff_data = {
            "type": "quick_adaptation",
            "situation": situation,
            "adaptations": adaptations,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "adaptability",
            "visual_effect": "adaptive_shimmer"
        }
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$push": {"buffs": buff_data}}
        )
        
        # Small karma boost (adaptability is seen as wise)
        karma_gain = random.randint(2, 6)
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        # Create notification
        await self.db.notifications.insert_one({
            "player_id": player_id,
            "type": "quick_adaptation_active",
            "message": f"🔄 Adapted to {situation} situation! Gained situational buffs for {duration}s",
            "data": {
                "situation": situation,
                "adaptations": adaptations,
                "duration": duration,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "adaptations": adaptations,
            "duration": duration,
            "karma_gain": karma_gain,
            "message": f"Quick Adaptation: Optimized for {situation} situation!"
        }
    
    def _get_adaptations_for_situation(self, situation: str, strength: float) -> Dict:
        """Generate situation-specific stat adaptations."""
        base_buff = int(strength)
        
        adaptations = {}
        
        if situation == "combat":
            adaptations = {
                "damage_boost_percent": base_buff,
                "defense_boost_percent": int(base_buff * 0.7),
                "attack_speed_boost_percent": int(base_buff * 0.5),
                "critical_chance_bonus": 10
            }
        elif situation == "exploration":
            adaptations = {
                "movement_speed_boost_percent": base_buff,
                "stamina_regen_boost_percent": int(base_buff * 1.2),
                "perception_boost_percent": int(base_buff * 0.8),
                "trap_detection_bonus": 25
            }
        elif situation == "social":
            adaptations = {
                "charisma_boost_percent": base_buff,
                "negotiation_success_bonus": int(base_buff * 0.6),
                "persuasion_effectiveness": int(base_buff * 0.7),
                "reputation_gain_multiplier": 1.5
            }
        elif situation == "survival":
            adaptations = {
                "hp_regen_boost_percent": base_buff,
                "energy_regen_boost_percent": base_buff,
                "damage_reduction_percent": int(base_buff * 0.8),
                "resource_efficiency": int(base_buff * 0.5)
            }
        else:
            # Generic adaptation
            adaptations = {
                "all_stats_boost_percent": int(base_buff * 0.5),
                "versatility_bonus": True
            }
        
        return adaptations
    
    async def environment_mastery(
        self,
        player_id: str,
        environment_type: str,
        trait_level: int
    ) -> Dict:
        """Passive ability: Gain bonuses in different environments over time.
        
        Args:
            player_id: ID of player
            environment_type: Type of environment (desert, forest, urban, etc.)
            trait_level: Adaptability trait level (1-100)
        
        Returns:
            Dict with success, mastery_level, bonuses, message
        """
        
        # Check player's environment history
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {
                "success": False,
                "mastery_level": 0,
                "message": "Player not found"
            }
        
        # Get or initialize environment mastery
        environment_mastery = player.get("traits", {}).get("environment_mastery", {})
        current_mastery = environment_mastery.get(environment_type, 0)
        
        # Calculate new mastery level (increases with time spent)
        # In production, this would track actual time spent in environment
        mastery_increase = 1 + int(trait_level / 50)
        new_mastery = min(100, current_mastery + mastery_increase)
        
        # Update mastery
        await self.db.players.update_one(
            {"_id": player_id},
            {"$set": {f"traits.environment_mastery.{environment_type}": new_mastery}}
        )
        
        # Calculate bonuses based on mastery level
        bonuses = {
            "movement_bonus_percent": int(new_mastery * 0.3),
            "resource_finding_bonus_percent": int(new_mastery * 0.25),
            "environmental_damage_resistance": int(new_mastery * 0.4),
            "navigation_accuracy": int(new_mastery * 0.5)
        }
        
        return {
            "success": True,
            "environment_type": environment_type,
            "mastery_level": new_mastery,
            "mastery_gained": mastery_increase,
            "bonuses": bonuses,
            "message": f"Environment mastery in {environment_type}: {new_mastery}/100"
        }
    
    async def copy_ability(
        self,
        player_id: str,
        target_id: str,
        ability_name: str,
        trait_level: int
    ) -> Dict:
        """Copy an ability from another player temporarily.
        
        Args:
            player_id: ID of adaptive player
            target_id: ID of target player to copy from
            ability_name: Name of ability to copy
            trait_level: Adaptability trait level (1-100)
        
        Returns:
            Dict with success, copied_ability, duration, effectiveness, message
        """
        
        # Get target player
        target = await self.db.players.find_one({"_id": target_id})
        if not target:
            return {
                "success": False,
                "copied_ability": None,
                "message": "Target player not found"
            }
        
        # Check if target has the ability
        target_traits = target.get("traits", {}).get("acquired", {})
        if ability_name not in target_traits:
            return {
                "success": False,
                "copied_ability": None,
                "message": f"Target doesn't have {ability_name} ability"
            }
        
        # Calculate copy effectiveness (40-90% of original power)
        min_effectiveness = 40
        max_effectiveness = 90
        effectiveness = min_effectiveness + (trait_level / 100) * (max_effectiveness - min_effectiveness)
        
        # Duration based on trait level (2-10 minutes)
        duration = 120 + int((trait_level / 100) * 480)
        
        # Apply copied ability as temporary trait
        copied_ability_data = {
            "type": "copied_ability",
            "ability_name": ability_name,
            "effectiveness_percent": int(effectiveness),
            "source_player_id": target_id,
            "expires_at": datetime.utcnow().timestamp() + duration,
            "source_trait": "adaptability"
        }
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$push": {"temporary_abilities": copied_ability_data}}
        )
        
        # Notify both players
        player = await self.db.players.find_one({"_id": player_id})
        player_name = player.get("profile", {}).get("name", "Unknown")
        target_name = target.get("profile", {}).get("name", "Unknown")
        
        await self.db.notifications.insert_one({
            "player_id": target_id,
            "type": "ability_copied",
            "message": f"{player_name} copied your {ability_name} ability!",
            "data": {
                "copier_id": player_id,
                "ability": ability_name,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "copied_ability": ability_name,
            "effectiveness": int(effectiveness),
            "duration": duration,
            "source_player": target_name,
            "message": f"Copied {ability_name} from {target_name} at {int(effectiveness)}% effectiveness for {duration//60} minutes"
        }
