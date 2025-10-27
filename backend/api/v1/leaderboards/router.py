"""Leaderboards API routes."""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from backend.api.deps import get_current_player
from backend.models.player.player import Player
from backend.services.leaderboards.manager import LeaderboardManager
from .schemas import (
    LeaderboardResponse,
    PlayerRankResponse
)

router = APIRouter(prefix="/leaderboards", tags=["leaderboards"])


@router.get("/karma", response_model=LeaderboardResponse)
async def get_karma_leaderboard(
    limit: int = Query(default=50, ge=1, le=100),
    season_id: Optional[str] = None,
    current_player: Player = Depends(get_current_player)
):
    """Get karma leaderboard."""
    manager = LeaderboardManager()
    return await manager.get_leaderboard(
        leaderboard_type="karma",
        limit=limit,
        season_id=season_id
    )


@router.get("/wealth", response_model=LeaderboardResponse)
async def get_wealth_leaderboard(
    limit: int = Query(default=50, ge=1, le=100),
    season_id: Optional[str] = None,
    current_player: Player = Depends(get_current_player)
):
    """Get wealth leaderboard."""
    manager = LeaderboardManager()
    return await manager.get_leaderboard(
        leaderboard_type="wealth",
        limit=limit,
        season_id=season_id
    )


@router.get("/combat", response_model=LeaderboardResponse)
async def get_combat_leaderboard(
    limit: int = Query(default=50, ge=1, le=100),
    season_id: Optional[str] = None,
    current_player: Player = Depends(get_current_player)
):
    """Get combat leaderboard."""
    manager = LeaderboardManager()
    return await manager.get_leaderboard(
        leaderboard_type="combat",
        limit=limit,
        season_id=season_id
    )


@router.get("/guilds", response_model=LeaderboardResponse)
async def get_guild_leaderboard(
    limit: int = Query(default=50, ge=1, le=100),
    season_id: Optional[str] = None,
    current_player: Player = Depends(get_current_player)
):
    """Get guild leaderboard."""
    manager = LeaderboardManager()
    return await manager.get_leaderboard(
        leaderboard_type="guild",
        limit=limit,
        season_id=season_id
    )


@router.get("/achievements", response_model=LeaderboardResponse)
async def get_achievement_leaderboard(
    limit: int = Query(default=50, ge=1, le=100),
    season_id: Optional[str] = None,
    current_player: Player = Depends(get_current_player)
):
    """Get achievement leaderboard."""
    manager = LeaderboardManager()
    return await manager.get_leaderboard(
        leaderboard_type="achievement",
        limit=limit,
        season_id=season_id
    )


@router.get("/seasonal", response_model=LeaderboardResponse)
async def get_seasonal_leaderboard(
    leaderboard_type: str = Query(...,
                                  description="karma, wealth, combat, achievement"),
    limit: int = Query(default=50, ge=1, le=100),
    current_player: Player = Depends(get_current_player)
):
    """Get seasonal leaderboard (current season only)."""
    from backend.services.seasonal.seasons import SeasonService
    season_service = SeasonService()
    current_season = await season_service.get_current_season()

    if not current_season:
        return {"entries": [], "total_entries": 0, "leaderboard_type": leaderboard_type}

    manager = LeaderboardManager()
    return await manager.get_leaderboard(
        leaderboard_type=leaderboard_type,
        limit=limit,
        season_id=current_season["season_id"]
    )


@router.get("/my-rank/{leaderboard_type}", response_model=PlayerRankResponse)
async def get_my_rank(
    leaderboard_type: str,
    season_id: Optional[str] = None,
    current_player: Player = Depends(get_current_player)
):
    """Get current player's rank in a leaderboard."""
    manager = LeaderboardManager()
    return await manager.get_player_rank(
        player_id=str(current_player.id),
        leaderboard_type=leaderboard_type,
        season_id=season_id
    )


@router.get("/all")
async def get_all_leaderboards(
    limit: int = Query(default=10, ge=1, le=50),
    current_player: Player = Depends(get_current_player)
):
    """Get top entries from all leaderboards."""
    manager = LeaderboardManager()

    leaderboards = {}
    for lb_type in ["karma", "wealth", "combat", "guild", "achievement"]:
        leaderboards[lb_type] = await manager.get_leaderboard(
            leaderboard_type=lb_type,
            limit=limit
        )

    return leaderboards
