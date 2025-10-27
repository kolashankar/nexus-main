from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.social.alliances import AllianceService
from backend.api.deps import get_current_user
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class CreateAllianceRequest(BaseModel):
    alliance_name: Optional[str] = None


class AddMemberRequest(BaseModel):
    player_id: str


@router.post("", response_model=dict)
async def create_alliance(
    request: CreateAllianceRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new alliance"""
    service = AllianceService(db)

    try:
        alliance = await service.create_alliance(
            creator_id=current_user["_id"],
            alliance_name=request.alliance_name
        )
        return {"success": True, "alliance": alliance.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-alliance", response_model=dict)
async def get_my_alliance(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get my current alliance"""
    service = AllianceService(db)
    alliance = await service.get_player_alliance(current_user["_id"])

    if not alliance:
        raise HTTPException(status_code=404, detail="Not in an alliance")

    return alliance


@router.post("/add-member", response_model=dict)
async def add_alliance_member(
    request: AddMemberRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Add a member to alliance"""
    service = AllianceService(db)

    # Get current alliance
    alliance = await service.get_player_alliance(current_user["_id"])
    if not alliance:
        raise HTTPException(status_code=400, detail="Not in an alliance")

    try:
        success = await service.add_member(alliance.get("id"), request.player_id)
        return {"success": success, "message": "Member added to alliance"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/leave", response_model=dict)
async def leave_alliance(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Leave current alliance"""
    service = AllianceService(db)

    alliance = await service.get_player_alliance(current_user["_id"])
    if not alliance:
        raise HTTPException(status_code=400, detail="Not in an alliance")

    try:
        success = await service.remove_member(alliance.get("id"), current_user["_id"])
        return {"success": success, "message": "Left alliance"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/disband", response_model=dict)
async def disband_alliance(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Disband alliance (creator only)"""
    service = AllianceService(db)

    alliance = await service.get_player_alliance(current_user["_id"])
    if not alliance:
        raise HTTPException(status_code=400, detail="Not in an alliance")

    # Check if creator
    if alliance.get("members", [])[0] != current_user["_id"]:
        raise HTTPException(
            status_code=403, detail="Only alliance creator can disband")

    try:
        success = await service.disband_alliance(alliance.get("id"))
        return {"success": success, "message": "Alliance disbanded"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
