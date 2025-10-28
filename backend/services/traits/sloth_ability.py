"""Sloth vice ability implementation."""

from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, Optional
import random
from datetime import datetime

class SlothAbility:
    """Implementation of Sloth vice - Energy Siphon ability."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def energy_siphon(
        self,
        sloth_player_id: str,
        target_id: str,
        trait_level: int
    ) -> Dict:
        """Drain energy from target to restore own energy (lazy way to recover).
        
        Args:
            sloth_player_id: ID of slothful player
            target_id: ID of target player
            trait_level: Sloth trait level (1-100)
        
        Returns:
            Dict with success, energy_drained, karma_loss, message
        """
        
        # Get target player
        target = await self.db.players.find_one({"_id": target_id})
        if not target:
            return {
                "success": False,
                "energy_drained": 0,
                "message": "Target player not found"
            }
        
        # Get sloth player
        sloth_player = await self.db.players.find_one({"_id": sloth_player_id})
        if not sloth_player:
            return {
                "success": False,
                "energy_drained": 0,
                "message": "Player not found"
            }
        
        # Can't siphon yourself
        if sloth_player_id == target_id:
            return {
                "success": False,
                "energy_drained": 0,
                "message": "Cannot siphon energy from yourself"
            }
        
        # Get target's energy
        target_stats = target.get("stats", {})
        target_energy = target_stats.get("energy", 100)
        target_max_energy = target_stats.get("max_energy", 100)
        
        # Check if target has energy to drain
        if target_energy < 20:
            return {
                "success": False,
                "energy_drained": 0,
                "message": "Target has insufficient energy to siphon"
            }
        
        # Calculate siphon amount (20-50% of target's current energy)
        min_percent = 20
        max_percent = 50
        siphon_percent = min_percent + (trait_level / 100) * (max_percent - min_percent)
        
        energy_to_drain = int(target_energy * (siphon_percent / 100))
        energy_to_drain = max(20, energy_to_drain)  # Minimum 20 energy
        energy_to_drain = min(energy_to_drain, target_energy - 10)  # Leave target with at least 10
        
        # Apply slow debuff to target (slowed by exhaustion)
        debuff_duration = 30 + int((trait_level / 100) * 30)  # 30-60 seconds
        
        debuff_data = {
            "type": "energy_drained_slow",
            "speed_penalty_percent": 25,
            "attack_speed_penalty_percent": 20,
            "expires_at": datetime.utcnow().timestamp() + debuff_duration,
            "source_player_id": sloth_player_id
        }
        
        # Deduct energy from target
        await self.db.players.update_one(
            {"_id": target_id},
            {
                "$inc": {"stats.energy": -energy_to_drain},
                "$push": {"debuffs": debuff_data}
            }
        )
        
        # Restore energy to sloth player
        sloth_stats = sloth_player.get("stats", {})
        sloth_energy = sloth_stats.get("energy", 100)
        sloth_max_energy = sloth_stats.get("max_energy", 100)
        
        energy_to_restore = min(energy_to_drain, sloth_max_energy - sloth_energy)
        
        await self.db.players.update_one(
            {"_id": sloth_player_id},
            {"$inc": {"stats.energy": energy_to_restore}}
        )
        
        # Apply karma penalty (stealing energy is lazy and malicious)
        karma_loss = random.randint(8, 15)
        await self.db.players.update_one(
            {"_id": sloth_player_id},
            {"$inc": {"karma.current": -karma_loss}}
        )
        
        # Notify target
        sloth_name = sloth_player.get("profile", {}).get("name", "Unknown")
        
        await self.db.notifications.insert_one({
            "player_id": target_id,
            "type": "energy_siphoned",
            "message": f"{sloth_name} siphoned {energy_to_drain} energy from you!",
            "data": {
                "siphoner_id": sloth_player_id,
                "energy_lost": energy_to_drain,
                "slow_duration": debuff_duration,
                "timestamp": datetime.utcnow()
            },
            "created_at": datetime.utcnow(),
            "read": False
        })
        
        return {
            "success": True,
            "energy_drained": energy_to_drain,
            "energy_restored": energy_to_restore,
            "karma_loss": karma_loss,
            "slow_duration": debuff_duration,
            "message": f"Siphoned {energy_to_drain} energy from target (restored {energy_to_restore} to you)"
        }
    
    async def lazy_dodge(
        self,
        player_id: str,
        trait_level: int
    ) -> Dict:
        """Passive ability: Occasionally avoid damage by being too slow/lazy to be where attacker expected.
        
        Args:
            player_id: ID of player
            trait_level: Sloth trait level (1-100)
        
        Returns:
            Dict with success and dodge chance
        """
        
        # Calculate dodge chance (5-20% based on trait level)
        dodge_chance = 5 + (trait_level / 100) * 15
        
        # Roll for dodge
        roll = random.randint(1, 100)
        dodged = roll <= dodge_chance
        
        return {
            "success": True,
            "dodged": dodged,
            "dodge_chance": dodge_chance,
            "message": "Lazily avoided the attack" if dodged else "Too slow to dodge"
        }
