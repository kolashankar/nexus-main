from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import random
import math

class CryokinesisAbility:
    """Cryokinesis superpower - Control ice and cold, freeze enemies, create ice constructs"""
    
    def __init__(self, db):
        self.db = db
        self.players_collection = db.get_collection("players")
        self.notifications_collection = db.get_collection("notifications")
    
    async def ice_blast(self, player_id: str, target_ids: list, trait_level: int) -> Dict[str, Any]:
        """
        Blast targets with shards of ice
        Deals cold damage and slows movement
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost scales with targets
        energy_cost = 22 + (len(target_ids) * 7)
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate ice damage and slow effect
        ice_damage = 25 + (trait_level * 0.6)  # 25-85 damage
        slow_percentage = 30 + (trait_level * 0.4)  # 30-70% movement slow
        slow_duration = 8 + (trait_level * 0.12)  # 8-20 seconds
        
        affected_targets = []
        
        for target_id in target_ids:
            if target_id == player_id:
                continue
            
            target = await self.players_collection.find_one({"id": target_id})
            if target:
                # Apply damage
                current_hp = target.get("health", {}).get("current", 100)
                new_hp = max(0, current_hp - ice_damage)
                
                # Apply slow debuff
                await self.players_collection.update_one(
                    {"id": target_id},
                    {
                        "$set": {"health.current": new_hp},
                        "$push": {
                            "debuffs": {
                                "type": "slowed",
                                "value": slow_percentage,
                                "expires_at": datetime.utcnow() + timedelta(seconds=slow_duration),
                                "applied_by": player_id
                            }
                        }
                    }
                )
                
                affected_targets.append({
                    "target_id": target_id,
                    "damage": ice_damage,
                    "slow_percentage": slow_percentage,
                    "duration": slow_duration
                })
                
                # Notify target
                await self.notifications_collection.insert_one({
                    "player_id": target_id,
                    "type": "combat",
                    "title": "Frozen!",
                    "message": f"{player.get('username', 'A cryokinetic')} hit you with ice blast! {ice_damage:.0f} damage, {slow_percentage:.0f}% slowed.",
                    "data": {
                        "ability": "Cryokinesis - Ice Blast",
                        "damage": ice_damage,
                        "slow": slow_percentage,
                        "duration": slow_duration
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
            "ice_damage": ice_damage,
            "slow_percentage": slow_percentage,
            "slow_duration": slow_duration,
            "energy_cost": energy_cost,
            "details": affected_targets
        }
    
    async def frozen_armor(self, player_id: str, trait_level: int) -> Dict[str, Any]:
        """
        Encase yourself in ice armor
        Provides damage resistance and chills nearby attackers
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost
        energy_cost = 30
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate armor benefits
        damage_resistance = 25 + (trait_level * 0.35)  # 25-60% damage reduction
        chill_damage = 10 + (trait_level * 0.2)  # 10-30 damage to attackers
        armor_hp = 80 + (trait_level * 1.2)  # 80-200 HP of ice armor
        armor_duration = 30 + (trait_level * 0.5)  # 30-80 seconds
        
        # Apply frozen armor buff
        await self.players_collection.update_one(
            {"id": player_id},
            {
                "$inc": {"energy.current": -energy_cost},
                "$push": {
                    "buffs": {
                        "type": "frozen_armor",
                        "damage_resistance": damage_resistance,
                        "armor_hp": armor_hp,
                        "chill_damage": chill_damage,
                        "expires_at": datetime.utcnow() + timedelta(seconds=armor_duration)
                    }
                }
            }
        )
        
        return {
            "success": True,
            "damage_resistance": damage_resistance,
            "armor_hp": armor_hp,
            "chill_damage": chill_damage,
            "duration": armor_duration,
            "energy_cost": energy_cost
        }
    
    async def deep_freeze(self, player_id: str, target_id: str, trait_level: int) -> Dict[str, Any]:
        """
        Completely freeze a single target
        Immobilizes target and deals damage over time
        """
        player = await self.players_collection.find_one({"id": player_id})
        target = await self.players_collection.find_one({"id": target_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        if not target:
            return {"success": False, "message": "Target not found"}
        
        if player_id == target_id:
            return {"success": False, "message": "Cannot freeze yourself"}
        
        # High energy cost for powerful single-target ability
        energy_cost = 45
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate freeze effects
        freeze_damage = 40 + (trait_level * 0.5)  # 40-90 initial damage
        freeze_duration = 5 + (trait_level * 0.08)  # 5-13 seconds of complete immobilization
        dot_damage = 8 + (trait_level * 0.15)  # 8-23 damage per tick
        
        # Apply initial damage
        current_hp = target.get("health", {}).get("current", 100)
        new_hp = max(0, current_hp - freeze_damage)
        
        # Apply frozen debuff (100% immobilization)
        await self.players_collection.update_one(
            {"id": target_id},
            {
                "$set": {"health.current": new_hp},
                "$push": {
                    "debuffs": [
                        {
                            "type": "frozen",
                            "value": 100,  # 100% immobilization
                            "expires_at": datetime.utcnow() + timedelta(seconds=freeze_duration),
                            "applied_by": player_id
                        },
                        {
                            "type": "frostbite",
                            "damage_per_tick": dot_damage,
                            "tick_interval": 1.5,  # Damage every 1.5 seconds
                            "expires_at": datetime.utcnow() + timedelta(seconds=freeze_duration),
                            "applied_by": player_id
                        }
                    ]
                }
            }
        )
        
        # Deduct energy
        await self.players_collection.update_one(
            {"id": player_id},
            {"$inc": {"energy.current": -energy_cost}}
        )
        
        total_dot_damage = dot_damage * (freeze_duration / 1.5)
        
        # Notify target
        await self.notifications_collection.insert_one({
            "player_id": target_id,
            "type": "combat",
            "title": "Deep Freeze!",
            "message": f"{player.get('username', 'A cryokinetic')} completely froze you! {freeze_damage:.0f} damage + frostbite for {freeze_duration:.1f}s.",
            "data": {
                "ability": "Cryokinesis - Deep Freeze",
                "initial_damage": freeze_damage,
                "dot_damage": dot_damage,
                "duration": freeze_duration
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "initial_damage": freeze_damage,
            "freeze_duration": freeze_duration,
            "dot_damage_per_tick": dot_damage,
            "total_dot_damage": total_dot_damage,
            "energy_cost": energy_cost
        }
    
    async def ice_construct(self, player_id: str, construct_type: str, trait_level: int) -> Dict[str, Any]:
        """
        Create constructs made of ice (walls, bridges, platforms)
        Provides tactical advantages and environmental control
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Energy cost varies by construct type
        energy_costs = {
            "wall": 20,
            "bridge": 30,
            "platform": 25,
            "cage": 40,
            "spike": 15
        }
        
        energy_cost = energy_costs.get(construct_type, 25)
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy"}
        
        # Calculate construct properties
        construct_hp = 100 + (trait_level * 2)  # 100-300 HP
        construct_duration = 60 + (trait_level * 1)  # 60-160 seconds
        
        # Construct-specific effects
        construct_effects = {
            "wall": {"height": 5 + (trait_level * 0.05), "width": 10 + (trait_level * 0.1), "blocks_vision": False},
            "bridge": {"length": 10 + (trait_level * 0.15), "width": 3, "supports_weight": True},
            "platform": {"size": 5 + (trait_level * 0.08), "elevation": 3 + (trait_level * 0.03)},
            "cage": {"radius": 3 + (trait_level * 0.05), "trap_duration": 10 + (trait_level * 0.1)},
            "spike": {"damage": 30 + (trait_level * 0.4), "count": 5 + (trait_level // 20)}
        }
        
        effect = construct_effects.get(construct_type, construct_effects["wall"])
        
        # Deduct energy
        await self.players_collection.update_one(
            {"id": player_id},
            {"$inc": {"energy.current": -energy_cost}}
        )
        
        # Track active construct (could be stored in player's active_constructs array)
        await self.players_collection.update_one(
            {"id": player_id},
            {
                "$push": {
                    "active_constructs": {
                        "type": construct_type,
                        "hp": construct_hp,
                        "properties": effect,
                        "created_at": datetime.utcnow(),
                        "expires_at": datetime.utcnow() + timedelta(seconds=construct_duration)
                    }
                }
            }
        )
        
        # Small karma gain for creative use
        karma_gain = 1 + random.randint(0, 2)
        await self.players_collection.update_one(
            {"id": player_id},
            {"$inc": {"karma.current": karma_gain}}
        )
        
        return {
            "success": True,
            "construct_type": construct_type,
            "construct_hp": construct_hp,
            "duration": construct_duration,
            "properties": effect,
            "energy_cost": energy_cost,
            "karma_gain": karma_gain
        }
    
    async def blizzard(self, player_id: str, position: Dict[str, float], trait_level: int) -> Dict[str, Any]:
        """
        Create a massive blizzard in an area
        Deals AOE damage and drastically reduces visibility and movement
        """
        player = await self.players_collection.find_one({"id": player_id})
        
        if not player:
            return {"success": False, "message": "Player not found"}
        
        # Ultimate ability - high energy cost
        energy_cost = 55
        current_energy = player.get("energy", {}).get("current", 0)
        
        if current_energy < energy_cost:
            return {"success": False, "message": "Insufficient energy for Blizzard"}
        
        # Calculate blizzard parameters
        damage_per_tick = 8 + (trait_level * 0.12)  # 8-20 damage per tick
        blizzard_radius = 20 + (trait_level * 0.25)  # 20-45 meter radius
        blizzard_duration = 15 + (trait_level * 0.2)  # 15-35 seconds
        movement_reduction = 60 + (trait_level * 0.3)  # 60-90% movement slow
        
        # Find all players in radius
        all_players = await self.players_collection.find({}).to_list(length=None)
        affected_targets = []
        
        for target in all_players:
            target_id = target.get("id")
            if target_id == player_id:
                continue
            
            # Calculate distance
            target_pos = target.get("position", {"x": 0, "y": 0, "z": 0})
            distance = math.sqrt(
                (target_pos.get("x", 0) - position.get("x", 0)) ** 2 +
                (target_pos.get("y", 0) - position.get("y", 0)) ** 2 +
                (target_pos.get("z", 0) - position.get("z", 0)) ** 2
            )
            
            if distance <= blizzard_radius:
                # Apply blizzard debuffs
                await self.players_collection.update_one(
                    {"id": target_id},
                    {
                        "$push": {
                            "debuffs": [
                                {
                                    "type": "blizzard_damage",
                                    "damage_per_tick": damage_per_tick,
                                    "tick_interval": 2,
                                    "expires_at": datetime.utcnow() + timedelta(seconds=blizzard_duration),
                                    "applied_by": player_id
                                },
                                {
                                    "type": "blizzard_slow",
                                    "value": movement_reduction,
                                    "expires_at": datetime.utcnow() + timedelta(seconds=blizzard_duration),
                                    "applied_by": player_id
                                }
                            ]
                        }
                    }
                )
                
                total_damage = damage_per_tick * (blizzard_duration / 2)
                affected_targets.append({
                    "target_id": target_id,
                    "distance": distance,
                    "damage_per_tick": damage_per_tick,
                    "total_damage": total_damage
                })
                
                # Notify target
                await self.notifications_collection.insert_one({
                    "player_id": target_id,
                    "type": "combat",
                    "title": "Blizzard!",
                    "message": f"{player.get('username', 'A cryokinetic')} summoned a blizzard! {damage_per_tick:.1f} damage per tick, {movement_reduction:.0f}% slowed.",
                    "data": {
                        "ability": "Cryokinesis - Blizzard",
                        "damage_per_tick": damage_per_tick,
                        "duration": blizzard_duration,
                        "slow": movement_reduction
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
            "damage_per_tick": damage_per_tick,
            "blizzard_radius": blizzard_radius,
            "duration": blizzard_duration,
            "movement_reduction": movement_reduction,
            "energy_cost": energy_cost,
            "details": affected_targets
        }
