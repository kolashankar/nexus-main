from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import random
import math

class PyrokinesisAbility:
    """Pyrokinesis superpower - Control and generate fire, create explosions, and burn damage over time"""
    
    def __init__(self, db):
        self.db = db
        self.players_collection = db.get_collection("players")
        self.notifications_collection = db.get_collection("notifications")
    
    async def flame_burst(self, player_id: str, target_ids: list, trait_level: int) -> Dict[str, Any]:
        """
        Unleash a burst of flames at targets
        Deals immediate fire damage and applies burning effect
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost scales with number of targets
        energy_cost = 25 + (len(target_ids) * 8)
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate fire damage (30-100 initial + burning DOT)
        initial_damage = 30 + (trait_level * 0.7)
        burn_damage_per_tick = 5 + (trait_level * 0.1)  # 5-15 damage per tick
        burn_duration = 10 + (trait_level * 0.15)  # 10-25 seconds
        
        affected_targets = []
        
        for target_id in target_ids:
            if target_id == player_id:
                continue
            
            target = await self.players_collection.find_one({"id": target_id})
            if target:
                # Apply initial damage
                current_hp = target.get("health", {}).get("current", 100)
                new_hp = max(0, current_hp - initial_damage)
                
                # Apply burning debuff
                await self.players_collection.update_one(
                    {"id": target_id},
                    {
                        "$set": {"health.current": new_hp},
                        "$push": {
                            "debuffs": {
                                "type": "burning",
                                "damage_per_tick": burn_damage_per_tick,
                                "tick_interval": 2,  # Damage every 2 seconds
                                "expires_at": datetime.utcnow() + timedelta(seconds=burn_duration),
                                "applied_by": player_id
                            }
                        }
                    }
                )
                
                total_burn_damage = burn_damage_per_tick * (burn_duration / 2)
                affected_targets.append({
                    "target_id": target_id,
                    "initial_damage": initial_damage,
                    "burn_damage_total": total_burn_damage,
                    "burn_duration": burn_duration
                })
                
                # Notify target
                await self.notifications_collection.insert_one({
                    "player_id": target_id,
                    "type": "combat",
                    "title": "Engulfed in Flames!",
                    "message": f"{player.get('username', 'A pyrokinetic')} hit you with a flame burst! {initial_damage:.0f} damage + burning for {burn_duration:.0f}s.",
                    "data": {
                        "ability": "Pyrokinesis - Flame Burst",
                        "initial_damage": initial_damage,
                        "burn_damage_per_tick": burn_damage_per_tick,
                        "duration": burn_duration
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
            "initial_damage": initial_damage,
            "burn_damage_per_tick": burn_damage_per_tick,
            "burn_duration": burn_duration,
            "energy_cost": energy_cost,
            "details": affected_targets
        }
    
    async def inferno_shield(self, player_id: str, trait_level: int) -> Dict[str, Any]:
        """
        Surround yourself with a shield of flames
        Burns attackers and provides damage resistance
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost
        energy_cost = 35
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate shield benefits
        damage_resistance = 20 + (trait_level * 0.3)  # 20-50% damage reduction
        retaliation_damage = 15 + (trait_level * 0.25)  # 15-40 damage to attackers
        shield_duration = 25 + (trait_level * 0.4)  # 25-65 seconds
        
        # Apply inferno shield buff
        await self.players_collection.update_one(
            {"id": player_id},
            {
                "$inc": {"energy.current": -energy_cost},
                "$push": {
                    "buffs": {
                        "type": "inferno_shield",
                        "damage_resistance": damage_resistance,
                        "retaliation_damage": retaliation_damage,
                        "expires_at": datetime.utcnow() + timedelta(seconds=shield_duration)
                    }
                }
            }
        )
        
        return {
            "success": True,
            "damage_resistance": damage_resistance,
            "retaliation_damage": retaliation_damage,
            "duration": shield_duration,
            "energy_cost": energy_cost
        }
    
    async def pyroclasm(self, player_id: str, position: Dict[str, float], trait_level: int) -> Dict[str, Any]:
        """
        Create a massive explosion at target location
        Deals heavy AOE damage with falloff based on distance
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # High energy cost for ultimate ability
        energy_cost = 60
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy for Pyroclasm"}
        
        # Calculate explosion parameters
        max_damage = 100 + (trait_level * 1.2)  # 100-220 damage at epicenter
        explosion_radius = 15 + (trait_level * 0.15)  # 15-30 meter radius
        aftershock_duration = 8 + (trait_level * 0.1)  # 8-18 seconds of fire patches
        
        # Find all players within explosion radius
        all_players = await self.players_collection.find({}).to_list(length=None)
        affected_targets = []
        
        for target in all_players:
            target_id = target.get("id")
            if target_id == player_id:
                continue
            
            # Calculate distance (assume target has position)
            target_pos = target.get("position", {"x": 0, "y": 0, "z": 0})
            distance = math.sqrt(
                (target_pos.get("x", 0) - position.get("x", 0)) ** 2 +
                (target_pos.get("y", 0) - position.get("y", 0)) ** 2 +
                (target_pos.get("z", 0) - position.get("z", 0)) ** 2
            )
            
            if distance <= explosion_radius:
                # Damage falloff based on distance
                damage_multiplier = max(0.3, 1 - (distance / explosion_radius))
                actual_damage = max_damage * damage_multiplier
                
                # Apply damage
                current_hp = target.get("health", {}).get("current", 100)
                new_hp = max(0, current_hp - actual_damage)
                
                # Apply stunned effect for close targets
                if distance < explosion_radius * 0.5:
                    await self.players_collection.update_one(
                        {"id": target_id},
                        {
                            "$set": {"health.current": new_hp},
                            "$push": {
                                "debuffs": {
                                    "type": "stunned",
                                    "value": 100,
                                    "expires_at": datetime.utcnow() + timedelta(seconds=3),
                                    "applied_by": player_id
                                }
                            }
                        }
                    )
                else:
                    await self.players_collection.update_one(
                        {"id": target_id},
                        {"$set": {"health.current": new_hp}}
                    )
                
                affected_targets.append({
                    "target_id": target_id,
                    "damage": actual_damage,
                    "distance": distance
                })
                
                # Notify target
                await self.notifications_collection.insert_one({
                    "player_id": target_id,
                    "type": "combat",
                    "title": "Pyroclasm!",
                    "message": f"{player.get('username', 'A pyrokinetic')} unleashed Pyroclasm! {actual_damage:.0f} damage.",
                    "data": {
                        "ability": "Pyrokinesis - Pyroclasm",
                        "damage": actual_damage,
                        "distance": distance
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
            "max_damage": max_damage,
            "explosion_radius": explosion_radius,
            "aftershock_duration": aftershock_duration,
            "energy_cost": energy_cost,
            "details": affected_targets
        }
    
    async def heat_generation(self, player_id: str, trait_level: int) -> Dict[str, Any]:
        """
        Generate intense heat to warm allies or melt obstacles
        Provides environmental control and support abilities
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Low energy cost for utility ability
        energy_cost = 15
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate heat benefits
        warmth_radius = 10 + (trait_level * 0.2)  # 10-30 meter radius
        healing_rate = 2 + (trait_level * 0.05)  # 2-7 HP per tick for cold allies
        melting_power = 50 + (trait_level * 0.5)  # 50-100 environmental interaction
        heat_duration = 30 + (trait_level * 0.5)  # 30-80 seconds
        
        # Apply heat aura buff
        await self.players_collection.update_one(
            {"id": player_id},
            {
                "$inc": {"energy.current": -energy_cost},
                "$push": {
                    "buffs": {
                        "type": "heat_aura",
                        "radius": warmth_radius,
                        "healing_rate": healing_rate,
                        "melting_power": melting_power,
                        "expires_at": datetime.utcnow() + timedelta(seconds=heat_duration)
                    }
                }
            }
        )
        
        # Small karma gain for providing warmth
        karma_gain = 2 + random.randint(0, 3)
        await self.players_collection.update_one(
            {"id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        return {
            "success": True,
            "warmth_radius": warmth_radius,
            "healing_rate": healing_rate,
            "melting_power": melting_power,
            "duration": heat_duration,
            "energy_cost": energy_cost,
            "karma_gain": karma_gain
        }
