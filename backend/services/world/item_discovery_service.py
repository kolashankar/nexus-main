"""Service for handling item discovery and interactions."""

from typing import Optional, List, Dict
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.world.world_item import WorldItem, WorldItemPosition
from datetime import datetime
import math

class ItemDiscoveryService:
    """Handles player discovery and interaction with world items."""
    
    PROXIMITY_DISTANCE = 50.0  # Units in game world
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
    
    async def get_nearby_items(
        self, 
        player_position: WorldItemPosition,
        player_id: str,
        radius: float = PROXIMITY_DISTANCE
    ) -> List[Dict]:
        """Get all active items within radius of player."""
        
        # Get all active items
        cursor = self.db.world_items.find({"status": "active"})
        all_items = await cursor.to_list(length=None)
        
        nearby_items = []
        for item_data in all_items:
            item = WorldItem(**item_data)
            distance = self._calculate_distance(player_position, item.position)
            
            if distance <= radius:
                # Mark as discovered by this player
                if player_id not in item.discovered_by:
                    await self.db.world_items.update_one(
                        {"_id": item.id},
                        {"$addToSet": {"discovered_by": player_id}}
                    )
                
                # Calculate time remaining
                time_remaining = int((item.expires_at - datetime.utcnow()).total_seconds())
                
                nearby_items.append({
                    "id": item.id,
                    "item_type": item.item_type,
                    "item_name": item.item_name,
                    "position": item.position.model_dump(),
                    "distance": round(distance, 2),
                    "cost": item.cost,
                    "required_level": item.required_level,
                    "rarity": item.rarity,
                    "icon": item.icon,
                    "time_remaining": max(0, time_remaining)
                })
        
        return nearby_items
    
    async def get_item_details(self, item_id: str, player_id: str) -> Optional[Dict]:
        """Get detailed information about a specific item."""
        
        item_data = await self.db.world_items.find_one({"_id": item_id})
        if not item_data:
            return None
        
        item = WorldItem(**item_data)
        
        # Check if item is still active
        if item.status != "active":
            return None
        
        # Calculate time remaining
        time_remaining = int((item.expires_at - datetime.utcnow()).total_seconds())
        if time_remaining <= 0:
            # Item expired, update status
            await self.db.world_items.update_one(
                {"_id": item_id},
                {"$set": {"status": "expired"}}
            )
            return None
        
        return {
            "id": item.id,
            "item_type": item.item_type,
            "item_name": item.item_name,
            "item_id": item.item_id,
            "position": item.position.model_dump(),
            "region": item.region,
            "cost": item.cost,
            "required_level": item.required_level,
            "status": item.status,
            "rarity": item.rarity,
            "icon": item.icon,
            "time_remaining": time_remaining,
            "discovered_by_count": len(item.discovered_by)
        }
    
    async def can_player_acquire(
        self,
        item_id: str,
        player_id: str,
        player_level: int,
        player_credits: int
    ) -> tuple[bool, str]:
        """Check if player can acquire this item."""
        
        # Get item
        item_data = await self.db.world_items.find_one({"_id": item_id})
        if not item_data:
            return False, "Item not found"
        
        item = WorldItem(**item_data)
        
        # Check if active
        if item.status != "active":
            return False, "Item is no longer available"
        
        # Check if already claimed
        if item.claimed_by:
            return False, "Item already claimed by another player"
        
        # Check level requirement
        if player_level < item.required_level:
            return False, f"Level {item.required_level} required"
        
        # Check if player has enough credits
        if player_credits < item.cost:
            return False, f"Not enough credits (need {item.cost})"
        
        # Check if player already has an active acquisition
        active_acquisition = await self.db.item_acquisitions.find_one({
            "player_id": player_id,
            "status": {"$in": ["investing", "completed"]}
        })
        
        if active_acquisition:
            return False, "You already have an active acquisition"
        
        return True, "OK"
    
    def _calculate_distance(
        self,
        pos1: WorldItemPosition,
        pos2: WorldItemPosition
    ) -> float:
        """Calculate Euclidean distance between two positions."""
        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        dz = pos1.z - pos2.z
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    async def mark_item_claimed(self, item_id: str, player_id: str) -> bool:
        """Mark item as claimed by player."""
        result = await self.db.world_items.update_one(
            {"_id": item_id, "status": "active"},
            {"$set": {"status": "claimed", "claimed_by": player_id}}
        )
        return result.modified_count > 0
