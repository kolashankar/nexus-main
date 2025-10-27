"""Robot marketplace routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user
from backend.services.robots.marketplace import RobotMarketplace
from .schemas import ListRobotRequest, BuyRobotRequest

router = APIRouter(prefix="/marketplace", tags=["robots", "marketplace"])
marketplace = RobotMarketplace()


@router.get("/")
async def get_marketplace_listings(
    limit: int = 50,
    skip: int = 0
):
    """Get all robot marketplace listings."""
    try:
        listings = await marketplace.get_listings(limit=limit, skip=skip)
        return {"listings": listings, "total": len(listings)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/list")
async def list_robot_for_sale(
    request: ListRobotRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """List a robot for sale on the marketplace."""
    try:
        result = await marketplace.list_robot(
            robot_id=request.robot_id,
            seller_id=current_user["_id"],
            price=request.price
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/buy")
async def buy_robot_from_marketplace(
    request: BuyRobotRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Buy a robot from the marketplace."""
    try:
        result = await marketplace.buy_robot(
            listing_id=request.listing_id,
            buyer_id=current_user["_id"]
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/listing/{listing_id}")
async def cancel_listing(
    listing_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Cancel a marketplace listing."""
    try:
        result = await marketplace.cancel_listing(
            listing_id=listing_id,
            seller_id=current_user["_id"]
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/my-listings")
async def get_my_listings(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current user's active listings."""
    try:
        listings = await marketplace.get_seller_listings(current_user["_id"])
        return {"listings": listings}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
