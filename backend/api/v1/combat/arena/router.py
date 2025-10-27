"""Arena-specific combat routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime
import random

from backend.api.deps import get_current_user
from backend.core.database import get_database
from backend.services.combat.engine import CombatEngine
from .schemas import JoinQueueRequest

router = APIRouter(prefix="/arena", tags=["combat", "arena"])
combat_engine = CombatEngine()


@router.post("/join")
async def join_arena_queue(
    request: JoinQueueRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Join the arena matchmaking queue."""
    db = await get_database()

    try:
        # Check if already in queue
        existing = await db.arena_queue.find_one({"player_id": current_user["_id"]})
        if existing:
            return {"status": "already_in_queue", "message": "You are already in the queue"}

        # Add to queue
        queue_entry = {
            "player_id": current_user["_id"],
            "username": current_user.get("username"),
            "rating": request.rating or 1000,
            "joined_at": datetime.utcnow()
        }

        await db.arena_queue.insert_one(queue_entry)

        # Try to find a match
        match = await _find_arena_match(current_user["_id"])

        if match:
            return {
                "status": "match_found",
                "message": "Match found!",
                "battle_id": match["battle_id"],
                "opponent": match["opponent"]
            }
        else:
            return {
                "status": "queued",
                "message": "Searching for opponent...",
                "queue_position": await _get_queue_position(current_user["_id"])
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/leave")
async def leave_arena_queue(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Leave the arena queue."""
    db = await get_database()

    result = await db.arena_queue.delete_one({"player_id": current_user["_id"]})

    if result.deleted_count > 0:
        return {"status": "left_queue", "message": "Left the arena queue"}
    else:
        return {"status": "not_in_queue", "message": "You were not in the queue"}


@router.get("/queue")
async def get_queue_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current arena queue status."""
    db = await get_database()

    # Total players in queue
    total = await db.arena_queue.count_documents({})

    # User's position
    user_entry = await db.arena_queue.find_one({"player_id": current_user["_id"]})

    in_queue = user_entry is not None
    position = await _get_queue_position(current_user["_id"]) if in_queue else None

    return {
        "in_queue": in_queue,
        "queue_position": position,
        "total_in_queue": total,
        "estimated_wait_time": min(total * 30, 300)  # Rough estimate
    }


@router.get("/rankings")
async def get_arena_rankings(
    limit: int = 50,
    skip: int = 0
):
    """Get arena rankings."""
    db = await get_database()

    # Get top players by arena rating
    rankings = await db.combat_stats.find().sort(
        "pvp_rating", -1
    ).skip(skip).limit(limit).to_list(length=limit)

    # Get player names
    for i, rank in enumerate(rankings):
        player = await db.players.find_one({"_id": rank["player_id"]})
        if player:
            rank["username"] = player.get("username")
            rank["rank"] = skip + i + 1

    return {"rankings": rankings}


@router.get("/rules")
async def get_arena_rules():
    """Get arena combat rules."""
    return {
        "rules": [
            "Ranked competitive combat",
            "Matchmaking based on Elo rating",
            "Winner gains rating and karma (+10)",
            "Loser loses rating, no karma penalty",
            "Cannot flee from arena matches",
            "Turn-based with 45s per turn",
            "4 action points per turn"
        ],
        "tiers": [
            {"name": "Bronze", "min_rating": 0, "max_rating": 1199},
            {"name": "Silver", "min_rating": 1200, "max_rating": 1499},
            {"name": "Gold", "min_rating": 1500, "max_rating": 1799},
            {"name": "Platinum", "min_rating": 1800, "max_rating": 2099},
            {"name": "Diamond", "min_rating": 2100, "max_rating": 2499},
            {"name": "Master", "min_rating": 2500, "max_rating": 9999}
        ],
        "rewards": {
            "win": {
                "karma": 10,
                "xp": 150,
                "rating_gain": "15-35 (based on opponent)"
            },
            "loss": {
                "karma": 0,
                "xp": 50,
                "rating_loss": "10-30 (based on opponent)"
            }
        }
    }


async def _find_arena_match(player_id: str) -> Dict[str, Any] | None:
    """Try to find an arena match for a player."""
    db = await get_database()

    # Get player's queue entry
    player_entry = await db.arena_queue.find_one({"player_id": player_id})
    if not player_entry:
        return None

    player_rating = player_entry.get("rating", 1000)

    # Find suitable opponents (within 200 rating points)
    opponents = await db.arena_queue.find({
        "player_id": {"$ne": player_id},
        "rating": {
            "$gte": player_rating - 200,
            "$lte": player_rating + 200
        }
    }).to_list(length=10)

    if not opponents:
        return None

    # Pick a random opponent
    opponent = random.choice(opponents)

    # Create arena match
    battle = await combat_engine._create_battle(
        player1_id=player_id,
        player2_id=opponent["player_id"],
        battle_type="arena"
    )

    # Remove both from queue
    await db.arena_queue.delete_many({
        "player_id": {"$in": [player_id, opponent["player_id"]]}
    })

    return {
        "battle_id": battle["id"],
        "opponent": {
            "id": opponent["player_id"],
            "username": opponent.get("username"),
            "rating": opponent.get("rating")
        }
    }


async def _get_queue_position(player_id: str) -> int:
    """Get player's position in queue."""
    db = await get_database()

    player_entry = await db.arena_queue.find_one({"player_id": player_id})
    if not player_entry:
        return 0

    # Count how many joined before this player
    position = await db.arena_queue.count_documents({
        "joined_at": {"$lt": player_entry["joined_at"]}
    })

    return position + 1
