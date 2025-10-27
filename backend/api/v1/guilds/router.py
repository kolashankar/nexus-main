from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.guilds.management import GuildManagementService
from backend.api.deps import get_current_user
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()


class CreateGuildRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    tag: str = Field(..., min_length=2, max_length=5)
    description: str = Field(default="", max_length=500)


class GuildResponse(BaseModel):
    id: str
    name: str
    tag: str
    description: str
    leader_id: str
    total_members: int
    level: int
    reputation: int


@router.post("", response_model=dict)
async def create_guild(
    request: CreateGuildRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new guild"""
    service = GuildManagementService(db)

    try:
        guild = await service.create_guild(
            name=request.name,
            tag=request.tag,
            description=request.description,
            leader_id=current_user["_id"]
        )
        return {"success": True, "guild": guild.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[dict])
async def list_guilds(
    skip: int = 0,
    limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List all guilds"""
    service = GuildManagementService(db)
    guilds = await service.list_guilds(skip=skip, limit=limit)
    return guilds


@router.get("/{guild_id}", response_model=dict)
async def get_guild(
    guild_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get guild by ID"""
    service = GuildManagementService(db)
    guild = await service.get_guild(guild_id)

    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    return guild


@router.post("/{guild_id}/join", response_model=dict)
async def join_guild(
    guild_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Join a guild"""
    service = GuildManagementService(db)

    try:
        success = await service.join_guild(guild_id, current_user["_id"])
        return {"success": success, "message": "Successfully joined guild"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/leave", response_model=dict)
async def leave_guild(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Leave current guild"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    service = GuildManagementService(db)

    try:
        success = await service.leave_guild(guild_id, current_user["_id"])
        return {"success": success, "message": "Successfully left guild"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{guild_id}/members", response_model=List[dict])
async def get_guild_members(
    guild_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all guild members"""
    service = GuildManagementService(db)
    members = await service.get_guild_members(guild_id)
    return members
