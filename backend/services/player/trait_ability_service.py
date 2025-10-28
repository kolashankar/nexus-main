"""Service for managing trait abilities and their usage."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import math
import random
from backend.models.player.equipped_traits import PlayerEquippedTraits, EquippedTrait
from backend.models.player.trait_cooldown import TraitCooldown, TraitUsageHistory

# Trait ability configurations
TRAIT_ABILITIES = {
    # SKILLS
    "hacking": {
        "name": "Hacking",
        "type": "skill",
        "cooldown_seconds": 1800,  # 30 minutes
        "energy_cost": 25,
        "range_meters": 100,
        "ability_name": "Credit Hack"
    },
    "negotiation": {
        "name": "Negotiation",
        "type": "skill",
        "cooldown_seconds": 900,  # 15 minutes
        "energy_cost": 15,
        "range_meters": 10,
        "ability_name": "Better Deal"
    },
    "stealth": {
        "name": "Stealth",
        "type": "skill",
        "cooldown_seconds": 45,
        "energy_cost": 30,
        "range_meters": 0,
        "ability_name": "Shadow Walk"
    },
    "leadership": {
        "name": "Leadership",
        "type": "skill",
        "cooldown_seconds": 7200,  # 2 hours
        "energy_cost": 50,
        "range_meters": 200,
        "ability_name": "Rally Cry"
    },
    # SUPERPOWER TOOLS
    "meditation_sp": {
        "name": "Meditation (Superpower)",
        "type": "superpower_tool",
        "cooldown_seconds": 3600,  # 1 hour
        "energy_cost": 80,
        "range_meters": 500,
        "ability_name": "Karmic Trace"
    },
    "telekinesis": {
        "name": "Telekinesis",
        "type": "superpower_tool",
        "cooldown_seconds": 45,
        "energy_cost": 70,
        "range_meters": 50,
        "ability_name": "Mind Grip"
    },
    "pyrokinesis": {
        "name": "Pyrokinesis",
        "type": "superpower_tool",
        "cooldown_seconds": 30,
        "energy_cost": 60,
        "range_meters": 40,
        "ability_name": "Flame Burst"
    },
    "cryokinesis": {
        "name": "Cryokinesis",
        "type": "superpower_tool",
        "cooldown_seconds": 35,
        "energy_cost": 65,
        "range_meters": 15,
        "ability_name": "Frost Nova"
    },
    # GOOD TRAITS (VIRTUES)
    "empathy": {
        "name": "Empathy",
        "type": "virtue",
        "cooldown_seconds": 1800,  # 30 minutes
        "energy_cost": 45,
        "range_meters": 20,
        "ability_name": "Emotional Shield"
    },
    "integrity": {
        "name": "Integrity",
        "type": "virtue",
        "cooldown_seconds": 3600,  # 1 hour
        "energy_cost": 50,
        "range_meters": 0,
        "ability_name": "Unbreakable Will"
    },
    # BAD TRAITS (VICES)
    "greed": {
        "name": "Greed",
        "type": "vice",
        "cooldown_seconds": 1200,  # 20 minutes
        "energy_cost": 50,
        "range_meters": 5,
        "ability_name": "Plunder"
    },
    "arrogance": {
        "name": "Arrogance",
        "type": "vice",
        "cooldown_seconds": 1800,  # 30 minutes
        "energy_cost": 45,
        "range_meters": 30,
        "ability_name": "Crushing Ego"
    },
    "deceit": {
        "name": "Deceit",
        "type": "vice",
        "cooldown_seconds": 2700,  # 45 minutes
        "energy_cost": 60,
        "range_meters": 10,
        "ability_name": "Perfect Lie"
    },
    "cruelty": {
        "name": "Cruelty",
        "type": "vice",
        "cooldown_seconds": 3600,  # 1 hour
        "energy_cost": 70,
        "range_meters": 5,
        "ability_name": "Sadistic Strike"
    },
}

class TraitAbilityService:
    """Service for trait ability management."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def get_player_equipped_traits(self, player_id: str) -> Optional[PlayerEquippedTraits]:
        """Get player's equipped traits."""
        data = await self.db.player_equipped_traits.find_one({"player_id": player_id})
        if data:
            return PlayerEquippedTraits(**data)
        return None
    
    async def equip_trait(
        self,
        player_id: str,
        trait_id: str,
        trait_type: str,
        trait_level: int,
        slot_number: int
    ) -> bool:
        """Equip a trait to a slot."""
        
        # Check if player has the trait in their collection
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return False
        
        # Create equipped trait
        equipped_trait = EquippedTrait(
            trait_id=trait_id,
            trait_type=trait_type,
            trait_level=trait_level,
            slot_number=slot_number
        )
        
        # Update or create equipped traits document
        slot_field = f"slot_{slot_number}"
        result = await self.db.player_equipped_traits.update_one(
            {"player_id": player_id},
            {
                "$set": {
                    slot_field: equipped_trait.model_dump(),
                    "last_swap_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        
        return result.modified_count > 0 or result.upserted_id is not None
    
    async def unequip_trait(self, player_id: str, slot_number: int) -> bool:
        """Unequip a trait from a slot."""
        slot_field = f"slot_{slot_number}"
        result = await self.db.player_equipped_traits.update_one(
            {"player_id": player_id},
            {
                "$set": {
                    slot_field: None,
                    "last_swap_at": datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    async def can_use_ability(
        self,
        player_id: str,
        trait_id: str
    ) -> tuple[bool, str, Optional[int]]:
        """Check if player can use this trait ability.
        
        Returns:
            (can_use, message, seconds_remaining)
        """
        
        # Check if trait is equipped
        equipped = await self.get_player_equipped_traits(player_id)
        if not equipped:
            return False, "No traits equipped", None
        
        # Check if trait is in any slot
        trait_equipped = False
        for slot_num in range(1, 7):
            slot = getattr(equipped, f"slot_{slot_num}")
            if slot and slot.trait_id == trait_id:
                trait_equipped = True
                break
        
        if not trait_equipped:
            return False, "Trait not equipped", None
        
        # Check cooldown
        active_cooldown = await self.db.trait_cooldowns.find_one({
            "player_id": player_id,
            "trait_id": trait_id,
            "is_active": True
        })
        
        if active_cooldown:
            cooldown = TraitCooldown(**active_cooldown)
            if datetime.utcnow() < cooldown.available_at:
                seconds_remaining = int((cooldown.available_at - datetime.utcnow()).total_seconds())
                return False, f"Ability on cooldown", seconds_remaining
            else:
                # Cooldown expired, mark as inactive
                await self.db.trait_cooldowns.update_one(
                    {"_id": active_cooldown["_id"]},
                    {"$set": {"is_active": False}}
                )
        
        # Check energy
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return False, "Player not found", None
        
        trait_config = TRAIT_ABILITIES.get(trait_id)
        if not trait_config:
            return False, "Trait configuration not found", None
        
        current_energy = player.get("status", {}).get("energy", 0)
        required_energy = trait_config["energy_cost"]
        
        if current_energy < required_energy:
            return False, f"Not enough energy (need {required_energy})", None
        
        return True, "OK", 0
    
    async def start_cooldown(
        self,
        player_id: str,
        trait_id: str,
        trait_type: str
    ) -> bool:
        """Start cooldown for a trait ability."""
        
        trait_config = TRAIT_ABILITIES.get(trait_id)
        if not trait_config:
            return False
        
        cooldown_seconds = trait_config["cooldown_seconds"]
        now = datetime.utcnow()
        available_at = now + timedelta(seconds=cooldown_seconds)
        
        cooldown = TraitCooldown(
            player_id=player_id,
            trait_id=trait_id,
            trait_type=trait_type,
            used_at=now,
            available_at=available_at,
            cooldown_seconds=cooldown_seconds,
            is_active=True
        )
        
        await self.db.trait_cooldowns.insert_one(cooldown.model_dump())
        return True
    
    async def consume_energy(
        self,
        player_id: str,
        trait_id: str
    ) -> bool:
        """Consume energy for trait ability."""
        
        trait_config = TRAIT_ABILITIES.get(trait_id)
        if not trait_config:
            return False
        
        energy_cost = trait_config["energy_cost"]
        
        result = await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"status.energy": -energy_cost}}
        )
        
        return result.modified_count > 0
    
    async def log_trait_usage(
        self,
        player_id: str,
        trait_id: str,
        trait_type: str,
        action_type: str,
        target_id: Optional[str] = None,
        success: bool = True,
        karma_change: int = 0,
        credits_affected: int = 0,
        damage_dealt: int = 0,
        location: Optional[dict] = None
    ) -> bool:
        """Log trait ability usage to history."""
        
        history = TraitUsageHistory(
            player_id=player_id,
            trait_id=trait_id,
            trait_type=trait_type,
            action_type=action_type,
            target_id=target_id,
            success=success,
            karma_change=karma_change,
            credits_affected=credits_affected,
            damage_dealt=damage_dealt,
            location=location
        )
        
        await self.db.trait_usage_history.insert_one(history.model_dump())
        return True
    
    async def get_trait_usage_history(
        self,
        player_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """Get player's trait usage history."""
        
        cursor = self.db.trait_usage_history.find(
            {"player_id": player_id}
        ).sort("used_at", -1).limit(limit)
        
        history = await cursor.to_list(length=limit)
        return history
    
    async def get_victims_of_trait(
        self,
        target_player_id: str,
        trait_id: str,
        hours: int = 1
    ) -> List[Dict]:
        """Get players who used a specific trait against this player recently.
        
        Used by Meditation superpower to track hackers.
        """
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        cursor = self.db.trait_usage_history.find({
            "target_id": target_player_id,
            "trait_id": trait_id,
            "success": True,
            "used_at": {"$gte": cutoff_time}
        }).sort("used_at", -1)
        
        perpetrators = await cursor.to_list(length=None)
        return perpetrators
    
    def calculate_distance(self, pos1: dict, pos2: dict) -> float:
        """Calculate distance between two positions."""
        dx = pos1["x"] - pos2["x"]
        dy = pos1["y"] - pos2["y"]
        dz = pos1["z"] - pos2["z"]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    async def get_players_in_range(
        self,
        center_position: dict,
        range_meters: float,
        exclude_player_id: Optional[str] = None
    ) -> List[Dict]:
        """Get all players within range of a position."""
        
        # Get all online players with positions
        cursor = self.db.players.find({
            "status.is_online": True,
            "position": {"$exists": True}
        })
        
        all_players = await cursor.to_list(length=None)
        nearby_players = []
        
        for player in all_players:
            if exclude_player_id and player["_id"] == exclude_player_id:
                continue
            
            if "position" in player:
                distance = self.calculate_distance(center_position, player["position"])
                if distance <= range_meters:
                    nearby_players.append({
                        "player_id": player["_id"],
                        "username": player.get("username", "Unknown"),
                        "position": player["position"],
                        "distance": round(distance, 2),
                        "level": player.get("level", 1)
                    })
        
        # Sort by distance
        nearby_players.sort(key=lambda x: x["distance"])
        return nearby_players