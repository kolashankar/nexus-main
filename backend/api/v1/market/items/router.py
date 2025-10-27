"""Item marketplace routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user

router = APIRouter(prefix="/items", tags=["market", "items"])


@router.get("/")
async def get_item_marketplace():
    """Get item marketplace listings."""
    # Placeholder for item marketplace
    return {
        "status": "coming_soon",
        "message": "Item marketplace will be available in Phase 8",
        "available_items": []
    }


@router.post("/buy")
async def buy_item(
    item_id: str,
    quantity: int = 1,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Buy an item from the marketplace."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Item marketplace coming in Phase 8"
    )


@router.post("/sell")
async def sell_item(
    item_id: str,
    quantity: int,
    price: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List an item for sale."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Item marketplace coming in Phase 8"
    )
