from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.guilds.wars import GuildWarService
from backend.api.deps import get_current_user
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()


class DeclareWarRequest(BaseModel):
    defender_guild_id: str
    target_territory: Optional[int] = None


class OfferPeaceRequest(BaseModel):
    war_id: str
    terms: dict


@router.post("/declare", response_model=dict)
async def declare_war(
    request: DeclareWarRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Declare war on another guild"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    # Only leaders can declare war
    guild_rank = current_user.get("guild_rank")
    if guild_rank != "leader":
        raise HTTPException(
            status_code=403, detail="Only guild leaders can declare war")

    service = GuildWarService(db)

    try:
        war = await service.declare_war(
            attacker_guild_id=guild_id,
            defender_guild_id=request.defender_guild_id,
            target_territory=request.target_territory
        )
        return {"success": True, "war": war.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-wars", response_model=List[dict])
async def get_my_guild_wars(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get wars involving my guild"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    service = GuildWarService(db)
    wars = await service.get_guild_wars(guild_id)
    return wars


@router.get("/{war_id}", response_model=dict)
async def get_war(
    war_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get war details"""
    service = GuildWarService(db)
    war = await service.get_war(war_id)

    if not war:
        raise HTTPException(status_code=404, detail="War not found")

    return war


@router.post("/peace/offer", response_model=dict)
async def offer_peace(
    request: OfferPeaceRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Offer peace treaty"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    guild_rank = current_user.get("guild_rank")
    if guild_rank != "leader":
        raise HTTPException(
            status_code=403, detail="Only guild leaders can offer peace")

    service = GuildWarService(db)

    try:
        success = await service.offer_peace(request.war_id, guild_id, request.terms)
        return {"success": success, "message": "Peace offer sent"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/peace/{war_id}/accept", response_model=dict)
async def accept_peace(
    war_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Accept peace treaty"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    guild_rank = current_user.get("guild_rank")
    if guild_rank != "leader":
        raise HTTPException(
            status_code=403, detail="Only guild leaders can accept peace")

    service = GuildWarService(db)

    try:
        success = await service.accept_peace(war_id, guild_id)
        return {"success": success, "message": "Peace treaty accepted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/peace/{war_id}/reject", response_model=dict)
async def reject_peace(
    war_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Reject peace treaty"""
    guild_id = current_user.get("guild_id")
    if not guild_id:
        raise HTTPException(status_code=400, detail="Not in a guild")

    guild_rank = current_user.get("guild_rank")
    if guild_rank != "leader":
        raise HTTPException(
            status_code=403, detail="Only guild leaders can reject peace")

    service = GuildWarService(db)

    try:
        success = await service.reject_peace(war_id)
        return {"success": success, "message": "Peace offer rejected"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
