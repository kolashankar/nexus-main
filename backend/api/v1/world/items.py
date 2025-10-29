"""API routes for world items."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
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

# === ACQUISITION ENDPOINTS ===

@router.post("/{item_id}/acquire")
async def acquire_item(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Start item acquisition process."""
    discovery_service = ItemDiscoveryService(db)
    
    # Check if player can acquire
    can_acquire, message = await discovery_service.can_player_acquire(
        item_id,
        current_user.id,
        current_user.level,
        current_user.currencies.credits
    )
    
    if not can_acquire:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    # Get item details
    item_details = await discovery_service.get_item_details(item_id, current_user.id)
    if not item_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or no longer available"
        )
    
    # Create acquisition record
    from datetime import datetime, timedelta
    acquisition_time = 300  # 5 minutes in seconds
    
    acquisition = {
        "id": f"acq_{item_id}_{current_user.id}",
        "player_id": current_user.id,
        "item_id": item_id,
        "item_type": item_details["item_type"],
        "item_name": item_details["item_name"],
        "cost_paid": item_details["cost"],
        "status": "in_progress",
        "started_at": datetime.utcnow(),
        "completes_at": datetime.utcnow() + timedelta(seconds=acquisition_time)
    }
    
    # Deduct credits from player
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"currencies.credits": -item_details["cost"]}}
    )
    
    # Store acquisition
    await db.acquisitions.insert_one(acquisition)
    
    # Remove item from world
    await db.world_items.delete_one({"_id": item_id})
    
    return {
        "success": True,
        "message": "Acquisition started",
        "acquisition": acquisition
    }


@router.get("/acquisitions/active")
async def get_active_acquisitions(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Get player's active acquisitions."""
    from datetime import datetime
    
    acquisitions = await db.acquisitions.find({
        "player_id": current_user.id,
        "status": {"$in": ["in_progress", "completed"]}
    }).to_list(length=100)
    
    # Update status for completed acquisitions
    now = datetime.utcnow()
    for acq in acquisitions:
        if acq["status"] == "in_progress" and acq["completes_at"] <= now:
            acq["status"] = "completed"
            await db.acquisitions.update_one(
                {"_id": acq["_id"]},
                {"$set": {"status": "completed"}}
            )
    
    return {
        "acquisitions": [{
            "id": str(acq["_id"]),
            "item_type": acq["item_type"],
            "item_name": acq["item_name"],
            "cost_paid": acq["cost_paid"],
            "status": acq["status"],
            "started_at": acq["started_at"].isoformat(),
            "completes_at": acq["completes_at"].isoformat()
        } for acq in acquisitions]
    }


@router.post("/acquisitions/{acquisition_id}/claim")
async def claim_acquisition(
    acquisition_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Claim a completed acquisition."""
    from datetime import datetime
    
    # Find acquisition
    acquisition = await db.acquisitions.find_one({
        "_id": acquisition_id,
        "player_id": current_user.id,
        "status": "completed"
    })
    
    if not acquisition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Acquisition not found or not ready to claim"
        )
    
    # Add item to player's inventory/traits/skills based on type
    if acquisition["item_type"] == "skill":
        # Add to player skills
        await db.players.update_one(
            {"_id": current_user.id},
            {"$addToSet": {"skills": acquisition["item_name"]}}
        )
    elif acquisition["item_type"] == "superpower_tool":
        # Add to player tools
        await db.players.update_one(
            {"_id": current_user.id},
            {"$addToSet": {"tools": acquisition["item_name"]}}
        )
    elif acquisition["item_type"] == "meta_trait":
        # Add to player meta traits
        await db.players.update_one(
            {"_id": current_user.id},
            {"$addToSet": {"meta_traits": acquisition["item_name"]}}
        )
    
    # Mark acquisition as claimed
    await db.acquisitions.update_one(
        {"_id": acquisition_id},
        {"$set": {"status": "claimed", "claimed_at": datetime.utcnow()}}
    )
    
    return {
        "success": True,
        "message": f"{acquisition['item_name']} has been added to your inventory",
        "item": {
            "type": acquisition["item_type"],
            "name": acquisition["item_name"]
        }
    }


@router.post("/acquisitions/{acquisition_id}/cancel")
async def cancel_acquisition(
    acquisition_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Cancel an active acquisition (50% refund)."""
    # Find acquisition
    acquisition = await db.acquisitions.find_one({
        "_id": acquisition_id,
        "player_id": current_user.id,
        "status": "in_progress"
    })
    
    if not acquisition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Acquisition not found or cannot be canceled"
        )
    
    # Calculate refund (50% of cost)
    refund_amount = int(acquisition["cost_paid"] * 0.5)
    
    # Refund credits
    await db.players.update_one(
        {"_id": current_user.id},
        {"$inc": {"currencies.credits": refund_amount}}
    )
    
    # Mark acquisition as canceled
    from datetime import datetime
    await db.acquisitions.update_one(
        {"_id": acquisition_id},
        {"$set": {"status": "canceled", "canceled_at": datetime.utcnow()}}
    )
    
    return {
        "success": True,
        "message": "Acquisition canceled",
        "refund_amount": refund_amount
    }
