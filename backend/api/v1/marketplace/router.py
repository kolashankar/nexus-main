"""Marketplace API Router"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from pydantic import BaseModel

from backend.core.database import get_database
from backend.api.deps import get_current_user
from backend.services.marketplace.marketplace import MarketplaceService

router = APIRouter()

class PurchaseRequest(BaseModel):
    item_type: str  # 'chain' or 'ring'

@router.get('/info')
async def get_marketplace_info(
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get marketplace information for player"""
    try:
        marketplace = MarketplaceService(db)
        info = await marketplace.get_marketplace_info(current_user['_id'])
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/purchase')
async def purchase_ornament(
    request: PurchaseRequest,
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Purchase an ornament (chain or ring)"""
    try:
        marketplace = MarketplaceService(db)
        result = await marketplace.purchase_ornament(current_user['_id'], request.item_type)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
