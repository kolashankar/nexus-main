"""API routes for world items."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Optional
from backend.api.deps import get_current_user, get_database
from backend.models.player.player import Player
from backend.models.world.world_item import WorldItemPosition
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.services.world.item_spawn_service import ItemSpawnService
from backend.services.world.item_discovery_service import ItemDiscoveryService
from pydantic import BaseModel

router = APIRouter(prefix="/world/items", tags=["world-items"])

class PlayerPositionRequest(BaseModel):
    """Request with player position."""
    x: float
    y: float
    z: float
    radius: Optional[float] = 50.0

@router.get("/active")
async def get_active_world_items(
    region: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Get all active world items."""
    spawn_service = ItemSpawnService(db)
    items = await spawn_service.get_active_items(region)
    
    return {
        "items": [
            {
                "id": item.id,
                "item_type": item.item_type,
                "item_name": item.item_name,
                "position": item.position.model_dump(),
                "region": item.region,
                "cost": item.cost,
                "required_level": item.required_level,
                "rarity": item.rarity,
                "icon": item.icon,
                "time_remaining": int((item.expires_at - item.spawned_at).total_seconds())
            }
            for item in items
        ],
        "count": len(items)
    }

@router.post("/nearby")
async def get_nearby_items(
    position: PlayerPositionRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Get items near player's position."""
    discovery_service = ItemDiscoveryService(db)
    
    player_pos = WorldItemPosition(x=position.x, y=position.y, z=position.z)
    
    nearby_items = await discovery_service.get_nearby_items(
        player_pos,
        current_user.id,
        position.radius
    )
    
    return {
        "items": nearby_items,
        "count": len(nearby_items),
        "position": {"x": position.x, "y": position.y, "z": position.z},
        "radius": position.radius
    }

@router.get("/{item_id}")
async def get_item_details(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Get detailed information about a specific item."""
    discovery_service = ItemDiscoveryService(db)
    
    item_details = await discovery_service.get_item_details(item_id, current_user.id)
    
    if not item_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or no longer available"
        )
    
    return item_details

@router.post("/{item_id}/can-acquire")
async def check_can_acquire(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Check if player can acquire this item."""
    discovery_service = ItemDiscoveryService(db)
    
    can_acquire, message = await discovery_service.can_player_acquire(
        item_id,
        current_user.id,
        current_user.level,
        current_user.currencies.credits
    )
    
    return {
        "can_acquire": can_acquire,
        "message": message,
        "player_level": current_user.level,
        "player_credits": current_user.currencies.credits
    }

# Admin endpoint for manual spawning (for testing)
@router.post("/admin/spawn/{item_type}")
async def admin_spawn_item(
    item_type: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Admin: Manually spawn an item (for testing)."""
    
    # In production, add admin role check here
    
    if item_type not in ["skill", "superpower_tool", "meta_trait"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid item type"
        )
    
    spawn_service = ItemSpawnService(db)
    item = await spawn_service.spawn_random_item(item_type)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to spawn item"
        )
    
    return {
        "message": f"Spawned {item_type}",
        "item": {
            "id": item.id,
            "item_name": item.item_name,
            "position": item.position.model_dump(),
            "cost": item.cost,
            "rarity": item.rarity
        }
    }
