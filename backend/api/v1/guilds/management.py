from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.guilds.management import GuildManagementService
from backend.api.deps import get_current_user
from backend.models.guilds.guild import GuildRank
from pydantic import BaseModel

router = APIRouter()


class KickMemberRequest(BaseModel):
    player_id: str


class PromoteMemberRequest(BaseModel):
    player_id: str
    new_rank: GuildRank


class ContributeRequest(BaseModel):
    credits: int


@router.post("/kick", response_model=dict)
async def kick_member(
    request: KickMemberRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Kick a member from guild"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    service = GuildManagementService(db)

    try:
        success = await service.kick_member(guild_id, request.player_id, current_user["_id"])
        return {"success": success, "message": "Member kicked successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/promote", response_model=dict)
async def promote_member(
    request: PromoteMemberRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Promote/demote a guild member"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    service = GuildManagementService(db)

    try:
        success = await service.promote_member(guild_id, request.player_id, request.new_rank, current_user["_id"])
        return {"success": success, "message": "Member rank updated"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/contribute", response_model=dict)
async def contribute_to_bank(
    request: ContributeRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Contribute credits to guild bank"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    if request.credits <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    service = GuildManagementService(db)

    try:
        success = await service.contribute_to_bank(guild_id, current_user["_id"], request.credits)
        return {"success": success, "message": f"Contributed {request.credits} credits to guild bank"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bank", response_model=dict)
async def get_guild_bank(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get guild bank status"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    service = GuildManagementService(db)
    guild = await service.get_guild(guild_id)

    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    return guild.get("guild_bank", {"credits": 0, "resources": {}})
