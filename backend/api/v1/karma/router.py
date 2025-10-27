from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from .schemas import KarmaScoreResponse, KarmaHistoryResponse
from backend.core.database import get_database
from backend.api.v1.auth.router import get_current_user_dep
from backend.models.player.player import Player
from backend.services.karma.calculator import KarmaCalculator

router = APIRouter(prefix="/karma", tags=["karma"])

@router.get("/score", response_model=KarmaScoreResponse)
async def get_karma_score(
    current_user: Player = Depends(get_current_user_dep)
):
    """Get current player's karma score."""
    calculator = KarmaCalculator()
    moral_class = calculator.determine_moral_class(current_user.karma_points)

    return KarmaScoreResponse(
        player_id=current_user.id,
        username=current_user.username,
        karma_points=current_user.karma_points,
        moral_class=moral_class,
        karma_level=calculator.get_karma_level(current_user.karma_points),
        next_milestone=calculator.get_next_milestone(current_user.karma_points)
    )

@router.get("/history", response_model=List[KarmaHistoryResponse])
async def get_karma_history(
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = 20
):
    """Get karma change history."""
    # Get actions that affected karma
    actions = await db.actions.find(
        {"actor_id": current_user.id, "karma_change": {"$ne": 0}}
    ).sort("timestamp", -1).limit(limit).to_list(limit)

    history = [
        KarmaHistoryResponse(
            action_type=action["action_type"],
            karma_change=action["karma_change"],
            timestamp=action["timestamp"],
            message=action.get("message", "")
        )
        for action in actions
    ]

    return history

@router.get("/world-state")
async def get_world_karma_state(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get global karma state."""
    # Get world state
    world_state = await db.world_state.find_one()

    if not world_state:
        # Initialize world state if not exists
        world_state = {
            "collective_karma": 0,
            "karma_trend": "stable",
            "total_players": 0,
            "online_players": 0
        }
        await db.world_state.insert_one(world_state)

    return {
        "collective_karma": world_state.get("collective_karma", 0),
        "karma_trend": world_state.get("karma_trend", "stable"),
        "total_players": world_state.get("total_players", 0),
        "online_players": world_state.get("online_players", 0)
    }

@router.get("/leaderboard")
async def get_karma_leaderboard(
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = 10,
    order: str = "highest"  # highest or lowest
):
    """Get karma leaderboard."""
    sort_order = -1 if order == "highest" else 1

    players = await db.players.find(
        {}
    ).sort("karma_points", sort_order).limit(limit).to_list(limit)

    leaderboard = [
        {
            "rank": idx + 1,
            "username": player["username"],
            "karma_points": player["karma_points"],
            "moral_class": player["moral_class"],
            "level": player["level"]
        }
        for idx, player in enumerate(players)
    ]

    return {
        "leaderboard": leaderboard,
        "order": order
    }