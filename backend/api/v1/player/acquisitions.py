"""API routes for player item acquisitions."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from backend.api.deps import get_current_user, get_database
from backend.models.player.player import Player
from backend.models.player.item_acquisition import StartAcquisitionRequest, ClaimAcquisitionRequest
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.services.player.item_acquisition_service import ItemAcquisitionService

router = APIRouter(prefix="/player/acquisitions", tags=["acquisitions"])

@router.get("")
async def get_player_acquisitions(
    status_filter: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Get all acquisitions for the current player."""
    acquisition_service = ItemAcquisitionService(db)
    
    acquisitions = await acquisition_service.get_player_acquisitions(
        current_user.id,
        status_filter
    )
    
    return {
        "acquisitions": acquisitions,
        "count": len(acquisitions)
    }

@router.get("/active")
async def get_active_acquisition(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Get player's currently active acquisition."""
    acquisition_service = ItemAcquisitionService(db)
    
    acquisitions = await acquisition_service.get_player_acquisitions(
        current_user.id,
        "investing"
    )
    
    # Also check for completed ones
    completed = await acquisition_service.get_player_acquisitions(
        current_user.id,
        "completed"
    )
    
    active = acquisitions + completed
    
    return {
        "active_acquisition": active[0] if active else None,
        "has_active": len(active) > 0
    }

@router.post("/start")
async def start_acquisition(
    request: StartAcquisitionRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Start acquiring a world item."""
    acquisition_service = ItemAcquisitionService(db)
    
    success, message, acquisition = await acquisition_service.start_acquisition(
        current_user.id,
        request.world_item_id,
        current_user.level,
        current_user.currencies.credits
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return {
        "message": message,
        "acquisition": {
            "id": acquisition.id,
            "item_type": acquisition.item_type,
            "item_name": acquisition.item_name,
            "cost_paid": acquisition.cost_paid,
            "status": acquisition.status,
            "completes_at": acquisition.completes_at,
            "time_remaining": int((acquisition.completes_at - acquisition.started_at).total_seconds())
        }
    }

@router.post("/claim")
async def claim_acquisition(
    request: ClaimAcquisitionRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Claim a completed acquisition."""
    acquisition_service = ItemAcquisitionService(db)
    
    success, message = await acquisition_service.claim_acquisition(
        current_user.id,
        request.acquisition_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return {
        "message": message,
        "success": True
    }

@router.post("/{acquisition_id}/cancel")
async def cancel_acquisition(
    acquisition_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: Player = Depends(get_current_user)
):
    """Cancel an ongoing acquisition."""
    acquisition_service = ItemAcquisitionService(db)
    
    success, message = await acquisition_service.cancel_acquisition(
        current_user.id,
        acquisition_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return {
        "message": message,
        "success": True
    }
