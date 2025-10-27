"""Tournaments API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from backend.api.deps import get_current_player
from backend.models.player.player import Player
from backend.services.tournaments.manager import TournamentManager
from .schemas import (
    TournamentResponse,
    RegisterTournamentRequest
)

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


@router.get("/active", response_model=List[TournamentResponse])
async def get_active_tournaments(
    current_player: Player = Depends(get_current_player)
):
    """Get all active tournaments."""
    manager = TournamentManager()
    tournaments = await manager.get_active_tournaments()
    return tournaments


@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(
    tournament_id: str,
    current_player: Player = Depends(get_current_player)
):
    """Get tournament details."""
    manager = TournamentManager()
    tournament = await manager.get_tournament(tournament_id)

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return tournament


@router.post("/register")
async def register_for_tournament(
    request: RegisterTournamentRequest,
    current_player: Player = Depends(get_current_player)
):
    """Register for a tournament."""
    manager = TournamentManager()

    try:
        result = await manager.register_player(
            tournament_id=request.tournament_id,
            player_id=str(current_player.id)
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{tournament_id}/bracket")
async def get_tournament_bracket(
    tournament_id: str,
    current_player: Player = Depends(get_current_player)
):
    """Get tournament bracket."""
    manager = TournamentManager()
    tournament = await manager.get_tournament(tournament_id)

    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    return {
        "tournament_id": tournament_id,
        "matches": tournament.get("matches", []),
        "current_round": tournament.get("current_round", 0),
        "total_rounds": tournament.get("total_rounds", 0)
    }


@router.get("/my/tournaments", response_model=List[TournamentResponse])
async def get_my_tournaments(
    status: Optional[str] = Query(None, description="Filter by status"),
    current_player: Player = Depends(get_current_player)
):
    """Get tournaments player is registered in."""
    manager = TournamentManager()
    tournaments = await manager.get_player_tournaments(
        player_id=str(current_player.id),
        status=status
    )
    return tournaments


@router.get("/history")
async def get_tournament_history(
    limit: int = Query(default=50, ge=1, le=100),
    current_player: Player = Depends(get_current_player)
):
    """Get tournament history."""
    manager = TournamentManager()
    # Get completed tournaments player participated in
    tournaments = await manager.get_player_tournaments(
        player_id=str(current_player.id),
        status="completed"
    )
    return tournaments[:limit]
