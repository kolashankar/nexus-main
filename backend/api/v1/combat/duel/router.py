"""Duel-specific combat routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user
from backend.services.combat.engine import CombatEngine
from .schemas import DuelChallengeRequest

router = APIRouter(prefix="/duel", tags=["combat", "duel"])
combat_engine = CombatEngine()


@router.post("/challenge")
async def challenge_to_duel(
    request: DuelChallengeRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Challenge another player to an honorable duel."""
    try:
        challenge = await combat_engine.create_challenge(
            challenger_id=current_user["_id"],
            target_id=request.target_id,
            combat_type="duel"
        )
        return {
            "challenge_id": str(challenge["_id"]),
            "status": "pending",
            "message": f"Duel challenge sent to {request.target_username}",
            "expires_in": 300  # 5 minutes
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/pending")
async def get_pending_duels(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all pending duel challenges."""
    from backend.core.database import get_database

    db = await get_database()

    # Challenges sent by user
    sent = await db.combat_challenges.find({
        "challenger_id": current_user["_id"],
        "combat_type": "duel",
        "status": "pending"
    }).to_list(length=50)

    # Challenges received by user
    received = await db.combat_challenges.find({
        "target_id": current_user["_id"],
        "combat_type": "duel",
        "status": "pending"
    }).to_list(length=50)

    return {
        "sent": sent,
        "received": received
    }


@router.get("/rules")
async def get_duel_rules():
    """Get duel combat rules."""
    return {
        "rules": [
            "Honorable 1v1 combat",
            "Both parties must agree",
            "Winner gains karma (+5)",
            "Loser loses karma (-5)",
            "No ambush mechanics",
            "Turn-based with 60s per turn",
            "4 action points per turn",
            "Can flee (costs 3 AP, 80% chance)"
        ],
        "rewards": {
            "winner": {
                "karma": 5,
                "xp": 100,
                "reputation": 10
            },
            "loser": {
                "karma": -5,
                "xp": 30,
                "reputation": -5
            }
        }
    }
