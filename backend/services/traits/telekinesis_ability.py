from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random
import math

class TelekinesisAbility:
    """Telekinesis superpower - Move objects with the mind, create force fields, and manipulate the environment"""
    
    def __init__(self, db):
        self.db = db
        self.players_collection = db.get_collection("players")
        self.notifications_collection = db.get_collection("notifications")
    
    async def force_push(self, player_id: str, target_ids: list, trait_level: int) -> Dict[str, Any]:
        """
        Push targets away with telekinetic force
        Deals damage and knockback based on trait level
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost increases with number of targets
        energy_cost = 20 + (len(target_ids) * 5)
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate force damage (20-80 based on trait level)
        force_damage = 20 + (trait_level * 0.6)
        knockback_distance = 5 + (trait_level * 0.1)  # 5-15 meters
        stun_duration = 2 + (trait_level * 0.03)  # 2-5 seconds
        
        affected_targets = []
        
        for target_id in target_ids:
            if target_id == player_id:
                continue
            
            target = await self.players_collection.find_one({"id": target_id})
            if target:
                # Apply damage
                new_hp = max(0, target.get("health", {}).get("current", 100) - force_damage)
                
                # Apply stun debuff
                await self.players_collection.update_one(
                    {"id": target_id},
                    {
                        "$set": {"health.current": new_hp},
                        "$push": {
                            "debuffs": {
                                "type": "stunned",
                                "value": 100,  # 100% movement reduction
                                "expires_at": datetime.utcnow() + timedelta(seconds=stun_duration),
                                "applied_by": player_id
                            }
                        }
                    }
                )
                
                affected_targets.append({
                    "target_id": target_id,
                    "damage": force_damage,
                    "knockback": knockback_distance,
                    "stunned": stun_duration
                })
                
                # Notify target
                await self.notifications_collection.insert_one({
                    "player_id": target_id,
                    "type": "combat",
                    "title": "Force Pushed!",
                    "message": f"{player.get('username', 'Someone')} used Telekinesis to push you away! {force_damage:.0f} damage, {stun_duration:.1f}s stun.",
                    "data": {
                        "ability": "Telekinesis - Force Push",
                        "damage": force_damage,
                        "knockback": knockback_distance
                    },
                    "created_at": datetime.utcnow(),
                    "read": False
                })
        
        # Deduct energy
        await self.players_collection.update_one(
            {"id": player_id},
            {"$inc": {"energy.current": -energy_cost}}
        )
        
        return {
            "success": True,
            "targets_affected": len(affected_targets),
            "force_damage": force_damage,
            "knockback_distance": knockback_distance,
            "energy_cost": energy_cost,
            "details": affected_targets
        }
    
    async def force_field(self, player_id: str, trait_level: int) -> Dict[str, Any]:
        """
        Create a protective telekinetic force field
        Absorbs damage and reflects projectiles
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost for force field
        energy_cost = 30
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate force field strength (100-500 HP absorption)
        field_strength = 100 + (trait_level * 4)
        field_duration = 30 + (trait_level * 0.5)  # 30-80 seconds
        reflection_chance = 20 + (trait_level * 0.3)  # 20-50% chance to reflect
        
        # Apply force field buff
        await self.players_collection.update_one(
            {"id": player_id},
            {
                "$inc": {"energy.current": -energy_cost},
                "$push": {
                    "buffs": {
                        "type": "force_field",
                        "value": field_strength,
                        "reflection_chance": reflection_chance,
                        "expires_at": datetime.utcnow() + timedelta(seconds=field_duration)
                    }
                }
            }
        )
        
        return {
            "success": True,
            "field_strength": field_strength,
            "duration": field_duration,
            "reflection_chance": reflection_chance,
            "energy_cost": energy_cost
        }
    
    async def object_manipulation(self, player_id: str, object_type: str, trait_level: int) -> Dict[str, Any]:
        """
        Manipulate objects in the environment telekinetically
        Can create barriers, throw objects, or solve puzzles
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost varies by object type
        energy_costs = {
            "small": 10,
            "medium": 20,
            "large": 35,
            "massive": 50
        }
        
        energy_cost = energy_costs.get(object_type, 20)
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate manipulation effectiveness (50-100% success rate)
        effectiveness = 50 + (trait_level * 0.5)
        success = random.random() * 100 < effectiveness
        
        if success:
            # Different effects based on object type
            effects = {
                "small": {"damage": 15 + (trait_level * 0.2), "range": 30},
                "medium": {"damage": 30 + (trait_level * 0.4), "range": 20},
                "large": {"damage": 50 + (trait_level * 0.6), "range": 15},
                "massive": {"damage": 80 + (trait_level * 0.8), "range": 10}
            }
            
            effect = effects.get(object_type, effects["medium"])
            
            # Deduct energy
            await self.players_collection.update_one(
                {"id": player_id},
                {"$inc": {"energy.current": -energy_cost}}
            )
            
            # Grant temporary manipulation buff
            manipulation_duration = 15 + (trait_level * 0.2)  # 15-35 seconds
            await self.players_collection.update_one(
                {"id": player_id},
                {
                    "$push": {
                        "buffs": {
                            "type": "object_control",
                            "object_type": object_type,
                            "value": effect["damage"],
                            "expires_at": datetime.utcnow() + timedelta(seconds=manipulation_duration)
                        }
                    }
                }
            )
            
            return {
                "success": True,
                "object_type": object_type,
                "damage": effect["damage"],
                "range": effect["range"],
                "duration": manipulation_duration,
                "energy_cost": energy_cost
            }
        else:
            # Failed manipulation still costs half energy
            await self.players_collection.update_one(
                {"id": player_id},
                {"$inc": {"energy.current": -(energy_cost // 2)}}
            )
            
            return {
                "success": False,
                "message": "Failed to manipulate object",
                "energy_cost": energy_cost // 2
            }
    
    async def levitate(self, player_id: str, trait_level: int) -> Dict[str, Any]:
        """
        Levitate self or objects to bypass obstacles
        Provides movement and defensive bonuses
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost for levitation
        energy_cost = 25
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate levitation benefits
        speed_boost = 30 + (trait_level * 0.4)  # 30-70% speed increase
        dodge_bonus = 15 + (trait_level * 0.25)  # 15-40% dodge chance
        levitation_duration = 20 + (trait_level * 0.3)  # 20-50 seconds
        
        # Apply levitation buff
        await self.players_collection.update_one(
            {"id": player_id},
            {
                "$inc": {"energy.current": -energy_cost},
                "$push": {
                    "buffs": {
                        "type": "levitating",
                        "speed_boost": speed_boost,
                        "dodge_bonus": dodge_bonus,
                        "expires_at": datetime.utcnow() + timedelta(seconds=levitation_duration)
                    }
                }
            }
        )
        
        return {
            "success": True,
            "speed_boost": speed_boost,
            "dodge_bonus": dodge_bonus,
            "duration": levitation_duration,
            "energy_cost": energy_cost
        }
