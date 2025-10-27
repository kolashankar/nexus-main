from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from .schemas import PlayerUpdateRequest, PlayerProfileResponse, PlayerStatsResponse
from backend.core.database import get_database
from backend.api.v1.auth.router import get_current_user_dep
from backend.models.player.player import Player, PlayerResponse
from backend.services.player.profile import PlayerProfileService

router = APIRouter(prefix="/player", tags=["player"])

@router.get("/profile", response_model=PlayerProfileResponse)
async def get_my_profile(
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current player's full profile."""
    profile_service = PlayerProfileService()
    return await profile_service.get_full_profile(current_user.id)

@router.put("/profile", response_model=PlayerProfileResponse)
async def update_profile(
    update_data: PlayerUpdateRequest,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update current player's profile."""
    profile_service = PlayerProfileService()
    return await profile_service.update_profile(current_user.id, update_data)

@router.get("/profile/{player_id}", response_model=PlayerResponse)
async def get_player_profile(
    player_id: str,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get another player's profile (respects visibility settings)."""
    player_dict = await db.players.find_one({"_id": player_id})
    if not player_dict:
        raise HTTPException(status_code=404, detail="Player not found")

    player = Player(**player_dict)
    return PlayerResponse.from_player(player, requester_id=current_user.id)

@router.get("/stats", response_model=PlayerStatsResponse)
async def get_player_stats(
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current player's statistics."""
    profile_service = PlayerProfileService()
    return await profile_service.get_player_stats(current_user.id)

@router.get("/currencies")
async def get_currencies(
    current_user: Player = Depends(get_current_user_dep)
):
    """Get current player's currencies."""
    return {
        "currencies": current_user.currencies.model_dump(),
        "karma_points": current_user.karma_points
    }

@router.get("/nearby")
async def get_nearby_players(
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = 10
):
    """Get nearby online players."""
    players = await db.players.find(
        {"online": True, "_id": {"$ne": current_user.id}}
    ).limit(limit).to_list(limit)

    return {
        "players": [
            PlayerResponse.from_player(
                Player(**p), requester_id=current_user.id).model_dump()
            for p in players
        ],
        "count": len(players)
    }