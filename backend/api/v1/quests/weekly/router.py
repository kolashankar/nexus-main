from fastapi import APIRouter, Depends
from .....core.security import get_current_user
from .....services.quests.weekly import WeeklyQuestService

router = APIRouter(prefix="/weekly", tags=["weekly-quests"])


@router.get("")
async def get_weekly_quests(
    current_user: dict = Depends(get_current_user)
):
    """Get this week's challenges."""
    weekly_service = WeeklyQuestService()
    quests = await weekly_service.get_weekly_quests(current_user["_id"])
    return {"quests": quests, "reset_time": weekly_service.get_reset_time()}
