"""Hidden quests API routes"""

from fastapi import APIRouter, Depends

from .....core.database import get_database
from .....services.quests.hidden import HiddenQuestService
from ....deps import get_current_player

router = APIRouter(prefix="/hidden", tags=["hidden-quests"])


@router.post("/discover")
async def discover_hidden_quest(
    location: str,
    action: str,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Try to discover a hidden quest"""
    service = HiddenQuestService(db)

    result = await service.check_discovery(
        player_id=current_player["_id"],
        location=location,
        action=action,
        player=current_player,
    )

    return result


@router.get("/discovered")
async def get_discovered_hidden_quests(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get all discovered hidden quests"""
    service = HiddenQuestService(db)
    quests = await service.get_player_hidden_quests(
        player_id=current_player["_id"],
    )

    return {"quests": quests, "total": len(quests)}
