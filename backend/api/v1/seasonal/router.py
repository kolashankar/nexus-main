"""Seasonal content API routes."""

from fastapi import APIRouter, Depends, HTTPException
from backend.api.deps import get_current_player
from backend.models.player.player import Player
from backend.services.seasonal.battle_pass import BattlePassService
from backend.services.seasonal.seasons import SeasonService
from backend.core.database import db
from .schemas import (
    BattlePassResponse,
    PlayerBattlePassProgressResponse,
    SeasonResponse,
    PlayerSeasonProgressResponse,
    ClaimRewardsRequest,
    ClaimRewardsResponse
)

router = APIRouter(prefix="/seasonal", tags=["seasonal"])


# Battle Pass Routes
@router.get("/battle-pass/active", response_model=BattlePassResponse)
async def get_active_battle_pass(
    current_player: Player = Depends(get_current_player)
):
    """Get currently active battle pass."""
    bp_service = BattlePassService()
    battle_pass = await bp_service.get_active_battle_pass()

    if not battle_pass:
        raise HTTPException(status_code=404, detail="No active battle pass")

    return battle_pass


@router.get("/battle-pass/progress", response_model=PlayerBattlePassProgressResponse)
async def get_my_battle_pass_progress(
    current_player: Player = Depends(get_current_player)
):
    """Get current player's battle pass progress."""
    bp_service = BattlePassService()
    battle_pass = await bp_service.get_active_battle_pass()

    if not battle_pass:
        raise HTTPException(status_code=404, detail="No active battle pass")

    progress = await bp_service.get_player_progress(
        player_id=str(current_player.id),
        pass_id=battle_pass["pass_id"]
    )

    return progress


@router.post("/battle-pass/purchase-premium")
async def purchase_premium_battle_pass(
    current_player: Player = Depends(get_current_player)
):
    """Purchase premium battle pass."""
    bp_service = BattlePassService()
    battle_pass = await bp_service.get_active_battle_pass()

    if not battle_pass:
        raise HTTPException(status_code=404, detail="No active battle pass")

    try:
        result = await bp_service.purchase_premium(
            player_id=str(current_player.id),
            pass_id=battle_pass["pass_id"]
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/battle-pass/claim-rewards", response_model=ClaimRewardsResponse)
async def claim_battle_pass_rewards(
    request: ClaimRewardsRequest,
    current_player: Player = Depends(get_current_player)
):
    """Claim battle pass rewards for a specific tier."""
    bp_service = BattlePassService()
    battle_pass = await bp_service.get_active_battle_pass()

    if not battle_pass:
        raise HTTPException(status_code=404, detail="No active battle pass")

    try:
        result = await bp_service.claim_rewards(
            player_id=str(current_player.id),
            pass_id=battle_pass["pass_id"],
            tier=request.tier
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Season Routes
@router.get("/season/current", response_model=SeasonResponse)
async def get_current_season(
    current_player: Player = Depends(get_current_player)
):
    """Get current season information."""
    season_service = SeasonService()
    season = await season_service.get_current_season()

    if not season:
        raise HTTPException(status_code=404, detail="No active season")

    return season


@router.get("/season/progress", response_model=PlayerSeasonProgressResponse)
async def get_my_season_progress(
    current_player: Player = Depends(get_current_player)
):
    """Get current player's season progress."""
    season_service = SeasonService()
    season = await season_service.get_current_season()

    if not season:
        raise HTTPException(status_code=404, detail="No active season")

    progress = await season_service.get_player_season_progress(
        player_id=str(current_player.id),
        season_id=season["season_id"]
    )

    return progress


@router.get("/season/{season_id}", response_model=SeasonResponse)
async def get_season(
    season_id: str,
    current_player: Player = Depends(get_current_player)
):
    """Get specific season information."""
    season = await db.seasons.find_one({"season_id": season_id})

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    return season
