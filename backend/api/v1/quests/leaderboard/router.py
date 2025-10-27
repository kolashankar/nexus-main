"""Quest leaderboard API routes"""

from fastapi import APIRouter, Depends, Query

from .....core.database import get_database
from .....services.quests.leaderboard import QuestLeaderboardService
from ....deps import get_current_player

router = APIRouter(prefix="/leaderboard", tags=["quest-leaderboard"])


@router.get("/completions")
async def get_completion_leaderboard(
    timeframe: str = Query(
        "all_time", regex="^(daily|weekly|monthly|all_time)$"),
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_database),
):
    """Get quest completion leaderboard"""
    service = QuestLeaderboardService(db)
    leaderboard = await service.get_completion_leaderboard(
        timeframe=timeframe,
        limit=limit,
    )
    return {"leaderboard": leaderboard, "timeframe": timeframe}


@router.get("/speedruns")
async def get_speedrun_leaderboard(
    quest_type: str = None,
    limit: int = Query(100, ge=1, le=1000),
    db = Depends(get_database),
):
    """Get fastest quest completions"""
    service = QuestLeaderboardService(db)
    speedruns = await service.get_speedrun_leaderboard(
        quest_type=quest_type,
        limit=limit,
    )
    return {"speedruns": speedruns}


@router.get("/my-rank")
async def get_my_rank(
    timeframe: str = Query(
        "all_time", regex="^(daily|weekly|monthly|all_time)$"),
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get current player's rank"""
    service = QuestLeaderboardService(db)
    rank = await service.get_player_rank(
        player_id=current_player["_id"],
        timeframe=timeframe,
    )
    return rank
