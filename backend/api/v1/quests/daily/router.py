from fastapi import APIRouter, Depends
from .....core.security import get_current_user
from .....services.quests.daily import DailyQuestService

router = APIRouter(prefix="/daily", tags=["daily-quests"])


@router.get("")
async def get_daily_quests(
    current_user: dict = Depends(get_current_user)
):
    """Get today's daily quests."""
    daily_service = DailyQuestService()
    quests = await daily_service.get_daily_quests(current_user["_id"])
    return {"quests": quests, "reset_time": daily_service.get_reset_time()}


@router.post("/refresh")
async def refresh_daily_quests(
    current_user: dict = Depends(get_current_user)
):
    """Manually refresh daily quests (once per day)."""
    daily_service = DailyQuestService()
    result = await daily_service.refresh_daily_quests(current_user["_id"])
    return result
