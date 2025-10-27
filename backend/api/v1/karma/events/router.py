from fastapi import APIRouter, Depends, Query
from .....services.karma.events import KarmaEventManager
from .....api.deps import get_current_user

router = APIRouter()

@router.get("/")
async def get_karma_events(
    limit: int = Query(default=50, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Get karma events for the player"""
    manager = KarmaEventManager()
    events = await manager.get_player_karma_history(current_user["_id"], limit)
    return events

@router.get("/recent")
async def get_recent_karma_events(
    limit: int = Query(default=100, le=200),
    current_user: dict = Depends(get_current_user)
):
    """Get recent karma events across all players"""
    manager = KarmaEventManager()
    events = await manager.get_recent_karma_events(limit)
    return events
