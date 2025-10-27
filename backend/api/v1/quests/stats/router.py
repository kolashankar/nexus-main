"""Quest statistics API routes"""

from fastapi import APIRouter, Depends

from .....core.database import get_database
from .....services.quests.analytics import QuestAnalyticsService
from ....deps import get_current_player

router = APIRouter(prefix="/stats", tags=["quest-stats"])


@router.get("/player")
async def get_player_quest_stats(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get quest statistics for current player"""
    analytics = QuestAnalyticsService(db)
    stats = await analytics.get_player_quest_stats(
        player_id=current_player["_id"]
    )
    return stats


@router.get("/global")
async def get_global_quest_stats(
    db = Depends(get_database),
):
    """Get global quest statistics"""
    analytics = QuestAnalyticsService(db)
    stats = await analytics.get_global_quest_stats()
    return stats


@router.get("/popular")
async def get_popular_quests(
    limit: int = 10,
    db = Depends(get_database),
):
    """Get most popular quests"""
    analytics = QuestAnalyticsService(db)
    popular = await analytics.get_popular_quests(limit=limit)
    return {"popular_quests": popular}
