"""Real estate marketplace routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user

router = APIRouter(prefix="/real-estate", tags=["market", "real-estate"])


@router.get("/")
async def get_properties():
    """Get available properties."""
    # Placeholder for real estate
    return {
        "status": "coming_soon",
        "message": "Real estate system will be available in Phase 8",
        "properties": []
    }


@router.post("/buy")
async def buy_property(
    property_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Buy a property."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Real estate coming in Phase 8"
    )


@router.get("/my-properties")
async def get_my_properties(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get player's owned properties."""
    return {
        "properties": [],
        "total_value": 0
    }
