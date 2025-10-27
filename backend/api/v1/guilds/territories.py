from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.guilds.territories import TerritoryService
from backend.api.deps import get_current_user
from typing import List

router = APIRouter()


@router.get("", response_model=List[dict])
async def get_all_territories(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all territories"""
    service = TerritoryService(db)
    territories = await service.get_all_territories()
    return territories


@router.get("/{territory_id}", response_model=dict)
async def get_territory(
    territory_id: int,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get territory by ID"""
    service = TerritoryService(db)
    territory = await service.get_territory(territory_id)

    if not territory:
        raise HTTPException(status_code=404, detail="Territory not found")

    return territory


@router.get("/guild/my-territories", response_model=List[dict])
async def get_my_guild_territories(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get territories controlled by my guild"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    service = TerritoryService(db)
    territories = await service.get_guild_territories(guild_id)
    return territories


@router.post("/{territory_id}/attack", response_model=dict)
async def attack_territory(
    territory_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Attack a territory"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    # Check if user has permission (officer or leader)
    guild_rank = current_user.get("guild_rank")
    if guild_rank not in ["leader", "officer"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    service = TerritoryService(db)

    try:
        result = await service.attack_territory(territory_id, guild_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{territory_id}/defend", response_model=dict)
async def defend_territory(
    territory_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Upgrade territory defense"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    guild_rank = current_user.get("guild_rank")
    if guild_rank not in ["leader", "officer"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    service = TerritoryService(db)

    try:
        success = await service.defend_territory(territory_id, guild_id)
        return {"success": success, "message": "Defense level upgraded"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
