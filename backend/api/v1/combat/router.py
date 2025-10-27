"""Combat API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user
from backend.services.combat.engine import CombatEngine
from backend.services.combat.calculator import CombatCalculator
from .schemas import (
    ChallengeRequest,
    ChallengeResponse,
    CombatActionRequest,
    CombatStateResponse,
    AcceptChallengeRequest,
    FleeRequest
)

router = APIRouter(prefix="/combat", tags=["combat"])
combat_engine = CombatEngine()
combat_calculator = CombatCalculator()


@router.post("/challenge", response_model=ChallengeResponse)
async def challenge_player(
    request: ChallengeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Challenge another player to combat."""
    try:
        challenge = await combat_engine.create_challenge(
            challenger_id=current_user["_id"],
            target_id=request.target_id,
            combat_type=request.combat_type
        )
        return ChallengeResponse(
            challenge_id=str(challenge["_id"]),
            status="pending",
            message=f"Challenge sent to {request.target_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/accept")
async def accept_challenge(
    request: AcceptChallengeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Accept a combat challenge."""
    try:
        battle = await combat_engine.accept_challenge(
            challenge_id=request.challenge_id,
            accepter_id=current_user["_id"]
        )
        return {
            "battle_id": str(battle["_id"]),
            "status": "started",
            "message": "Combat has begun!"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/decline")
async def decline_challenge(
    request: AcceptChallengeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Decline a combat challenge."""
    try:
        await combat_engine.decline_challenge(
            challenge_id=request.challenge_id,
            decliner_id=current_user["_id"]
        )
        return {"status": "declined", "message": "Challenge declined"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/active", response_model=CombatStateResponse)
async def get_active_combat(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current active combat state."""
    try:
        battle = await combat_engine.get_active_battle(current_user["_id"])
        if not battle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active combat"
            )

        return await combat_engine.get_combat_state(str(battle["_id"]))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/action")
async def perform_combat_action(
    request: CombatActionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Perform a combat action."""
    try:
        result = await combat_engine.execute_action(
            battle_id=request.battle_id,
            player_id=current_user["_id"],
            action_type=request.action_type,
            target=request.target,
            ability_id=request.ability_id
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/state/{battle_id}", response_model=CombatStateResponse)
async def get_combat_state(
    battle_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get combat state for a specific battle."""
    try:
        return await combat_engine.get_combat_state(battle_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/flee")
async def flee_combat(
    request: FleeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Attempt to flee from combat."""
    try:
        result = await combat_engine.attempt_flee(
            battle_id=request.battle_id,
            player_id=current_user["_id"]
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/stats")
async def get_combat_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get player's combat statistics."""
    try:
        stats = await combat_calculator.get_player_combat_stats(current_user["_id"])
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/history")
async def get_combat_history(
    current_user: Dict[str, Any] = Depends(get_current_user),
    limit: int = 20,
    skip: int = 0
):
    """Get combat history."""
    try:
        history = await combat_engine.get_combat_history(
            player_id=current_user["_id"],
            limit=limit,
            skip=skip
        )
        return {"history": history, "total": len(history)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
