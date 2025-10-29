"""Trait progress API router."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Dict, Any
from pydantic import BaseModel

from backend.core.database import get_database
from backend.core.security import decode_access_token
from backend.services.traits.milestone_tracker import MilestoneTracker
from backend.services.traits.unlock_manager import UnlockManager

router = APIRouter(prefix="/traits/progress", tags=["trait-progress"])
security = HTTPBearer()

class AcknowledgeMilestoneRequest(BaseModel):
    """Request to acknowledge a milestone."""
    milestone_id: str

class AcknowledgeUnlockRequest(BaseModel):
    """Request to acknowledge an unlock."""
    unlock_id: str

@router.get("/milestones")
async def get_player_milestones(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    unacknowledged_only: bool = False
):
    """Get player's trait milestones."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    tracker = MilestoneTracker()
    milestones = await tracker.get_player_milestones(db, player_id, unacknowledged_only)
    
    return {"milestones": milestones}

@router.post("/milestones/acknowledge")
async def acknowledge_milestone(
    request: AcknowledgeMilestoneRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark a milestone as acknowledged."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    tracker = MilestoneTracker()
    await tracker.acknowledge_milestone(db, request.milestone_id)
    
    return {"success": True}

@router.get("/milestones/stats")
async def get_milestone_stats(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get milestone statistics."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    tracker = MilestoneTracker()
    stats = await tracker.get_milestone_stats(db, player_id)
    
    return stats

@router.get("/unlocks")
async def get_player_unlocks(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    unacknowledged_only: bool = False
):
    """Get player's trait unlocks."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    manager = UnlockManager()
    unlocks = await manager.get_player_unlocks(db, player_id, unacknowledged_only)
    
    return {"unlocks": unlocks}

@router.post("/unlocks/acknowledge")
async def acknowledge_unlock(
    request: AcknowledgeUnlockRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Mark an unlock as acknowledged."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    manager = UnlockManager()
    await manager.acknowledge_unlock(db, request.unlock_id)
    
    return {"success": True}

@router.get("/unlocks/available")
async def get_available_unlocks(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all available unlocks with progress."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    manager = UnlockManager()
    available = await manager.get_available_unlocks(db, player_id)
    
    return {"available_unlocks": available}

@router.get("/summary")
async def get_trait_progress_summary(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get comprehensive trait progress summary."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    # Get player data
    player = await db.players.find_one({"_id": player_id})
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    # Get milestones and unlocks
    tracker = MilestoneTracker()
    manager = UnlockManager()
    
    milestone_stats = await tracker.get_milestone_stats(db, player_id)
    available_unlocks = await manager.get_available_unlocks(db, player_id)
    
    # Calculate trait progress
    traits = player.get("traits", {})
    trait_progress = {}
    
    for trait, value in traits.items():
        next_milestone = None
        for threshold in [25, 50, 75, 100]:
            if value < threshold:
                next_milestone = threshold
                break
        
        trait_progress[trait] = {
            "current_value": value,
            "next_milestone": next_milestone,
            "progress_to_next": ((value % 25) / 25) * 100 if next_milestone else 100,
            "level": "Master" if value >= 100 else "Expert" if value >= 75 else "Proficient" if value >= 50 else "Apprentice" if value >= 25 else "Novice"
        }
    
    return {
        "traits": trait_progress,
        "milestone_stats": milestone_stats,
        "available_unlocks": available_unlocks,
        "total_unlocked_abilities": len(player.get("unlocked_abilities", []))
    }
