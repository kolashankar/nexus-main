"""Service for spawning world items randomly in the game world."""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.world.world_item import WorldItem, WorldItemPosition
from backend.services.player.traits import TraitsService
import uuid

class ItemSpawnService:
    """Handles random spawning of items in the game world."""
    
    # Spawn frequencies (in seconds)
    SPAWN_INTERVALS = {
        "skill": {"min": 120, "max": 300},  # 2-5 minutes
        "superpower_tool": {"min": 600, "max": 900},  # 10-15 minutes
        "meta_trait": {"min": 1800, "max": 3600}  # 30-60 minutes
    }
    
    # Acquisition times (in seconds)
    ACQUISITION_TIMES = {
        "skill": {"min": 30, "max": 60},  # 30-60 seconds
        "superpower_tool": {"min": 120, "max": 300},  # 2-5 minutes
        "meta_trait": {"min": 300, "max": 600}  # 5-10 minutes
    }
    
    # Item lifetime (in seconds)
    ITEM_LIFETIMES = {
        "skill": 600,  # 10 minutes
        "superpower_tool": 900,  # 15 minutes
        "meta_trait": 1200  # 20 minutes
    }
    
    # Base costs by level
    BASE_COSTS = {
        "skill": {"min": 100, "max": 500},
        "superpower_tool": {"min": 1000, "max": 3000},
        "meta_trait": {"min": 5000, "max": 10000}
    }
    
    # Rarity mapping
    RARITIES = {
        "skill": "common",
        "superpower_tool": "rare",
        "meta_trait": "legendary"
    }
    
    # Spawn regions
    REGIONS = [
        "central_hub", "northern_district", "southern_bazaar",
        "eastern_tech_quarter", "western_industrial", "underground_network"
    ]
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.traits_service = TraitsService()
    
    async def spawn_random_item(self, item_type: str) -> Optional[WorldItem]:
        """Spawn a random item of the given type."""
        
        # Get available items for this type
        available_items = self._get_available_items(item_type)
        if not available_items:
            return None
        
        # Select random item
        item_data = random.choice(available_items)
        
        # Generate random position
        position = self._generate_random_position()
        
        # Calculate cost (random within range)
        cost_range = self.BASE_COSTS[item_type]
        base_cost = random.randint(cost_range["min"], cost_range["max"])
        
        # Random level requirement (1-100)
        required_level = random.randint(1, 100)
        
        # Calculate expiration
        lifetime = self.ITEM_LIFETIMES[item_type]
        expires_at = datetime.utcnow() + timedelta(seconds=lifetime)
        
        # Create world item
        world_item = WorldItem(
            id=str(uuid.uuid4()),
            item_type=item_type,
            item_name=item_data["name"],
            item_id=item_data["id"],
            position=position,
            region=random.choice(self.REGIONS),
            cost=base_cost,
            required_level=required_level,
            status="active",
            spawned_at=datetime.utcnow(),
            expires_at=expires_at,
            icon=item_data.get("icon", "default_icon.png"),
            rarity=self.RARITIES[item_type]
        )
        
        # Save to database
        await self.db.world_items.insert_one(world_item.model_dump(by_alias=True))
        
        return world_item
    
    def _get_available_items(self, item_type: str) -> List[Dict]:
        """Get list of available items for spawning."""
        
        if item_type == "skill":
            return [{"id": f"skill_{skill}", "name": skill, "icon": f"{skill}_icon.png"} 
                    for skill in self.traits_service.SKILLS]
        
        elif item_type == "superpower_tool":
            # For now, create placeholders for 25 superpowers
            return [{"id": f"power_{i}", "name": f"Power {i}", "icon": f"power_{i}_icon.png"} 
                    for i in range(1, 26)]
        
        elif item_type == "meta_trait":
            return [{"id": f"meta_{trait}", "name": trait, "icon": f"{trait}_icon.png"} 
                    for trait in self.traits_service.META_TRAITS]
        
        return []
    
    def _generate_random_position(self) -> WorldItemPosition:
        """Generate random 3D position in game world."""
        return WorldItemPosition(
            x=random.uniform(-500, 500),
            y=0.0,  # Ground level
            z=random.uniform(-500, 500)
        )
    
    async def cleanup_expired_items(self) -> int:
        """Remove expired items from the world."""
        result = await self.db.world_items.delete_many({
            "expires_at": {"$lt": datetime.utcnow()},
            "status": "active"
        })
        return result.deleted_count
    
    async def get_active_items(self, region: Optional[str] = None) -> List[WorldItem]:
        """Get all active items in the world or specific region."""
        query = {"status": "active"}
        if region:
            query["region"] = region
        
        cursor = self.db.world_items.find(query)
        items = await cursor.to_list(length=None)
        return [WorldItem(**item) for item in items]
    
    def get_acquisition_time(self, item_type: str) -> int:
        """Get random acquisition time for item type (in seconds)."""
        time_range = self.ACQUISITION_TIMES[item_type]
        return random.randint(time_range["min"], time_range["max"])
