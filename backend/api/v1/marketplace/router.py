"""Marketplace API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from pydantic import BaseModel

from backend.core.database import get_database
from backend.core.security import get_current_user
from backend.services.marketplace.ornament_shop import OrnamentShop
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])


class PurchaseRequest(BaseModel):
    """Request model for ornament purchase"""
    item_type: str  # "chain" or "ring"


@router.get("/inventory")
async def get_inventory(
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get player's ornament inventory.
    
    Returns:
        Inventory with chains, rings, and bonus percentage
    """
    try:
        player_id = current_user.get('player_id')
        shop = OrnamentShop(db)
        inventory = await shop.get_inventory(player_id)
        
        return {
            "success": True,
            "inventory": inventory
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve inventory: {str(e)}")


@router.get("/prices")
async def get_prices(
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get current prices for ornaments based on player's ownership.
    
    Returns:
        Current prices for chain and ring
    """
    try:
        player_id = current_user.get('player_id')
        shop = OrnamentShop(db)
        
        chain_price = await shop.get_current_price(player_id, "chain")
        ring_price = await shop.get_current_price(player_id, "ring")
        
        return {
            "success": True,
            "prices": {
                "chain": chain_price,
                "ring": ring_price
            },
            "bonuses": {
                "chain": "3% per chain",
                "ring": "7% per ring"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve prices: {str(e)}")


@router.post("/purchase")
async def purchase_ornament(
    request: PurchaseRequest,
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Purchase an ornament (chain or ring).
    
    Args:
        request: Purchase request with item_type
        
    Returns:
        Purchase result with new balance and next price
    """
    try:
        player_id = current_user.get('player_id')
        shop = OrnamentShop(db)
        
        result = await shop.purchase_ornament(player_id, request.item_type)
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Purchase failed'))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Purchase failed: {str(e)}")


@router.get("/history")
async def get_purchase_history(
    limit: int = 20,
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get purchase history for the player.
    
    Args:
        limit: Maximum number of records
        
    Returns:
        List of purchases
    """
    try:
        player_id = current_user.get('player_id')
        shop = OrnamentShop(db)
        history = await shop.get_purchase_history(player_id, limit)
        
        return {
            "success": True,
            "history": history
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")
