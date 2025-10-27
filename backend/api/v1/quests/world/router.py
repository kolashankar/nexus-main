"""World quests API routes"""

from fastapi import APIRouter, Depends

from .....core.database import get_database
from .....services.quests.world import WorldQuestService
from .....services.quests.manager import QuestManager
from ....deps import get_current_player

router = APIRouter(prefix="/world", tags=["world-quests"])


@router.get("/available")
async def get_available_world_quests(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get available world quests (open to all players)"""
    service = WorldQuestService(db)

    quests = await service.get_active_world_quests()

    return {
        "quests": quests,
        "total": len(quests),
        "message": "World quests are open to all players!",
    }


@router.get("/leaderboard/{quest_id}")
async def get_world_quest_leaderboard(
    quest_id: str,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get leaderboard for a world quest"""
    service = WorldQuestService(db)

    leaderboard = await service.get_quest_leaderboard(quest_id)

    return {
        "leaderboard": leaderboard,
        "total_participants": len(leaderboard),
    }


@router.post("/participate/{quest_id}")
async def participate_in_world_quest(
    quest_id: str,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Participate in a world quest"""
    WorldQuestService(db)
    manager = QuestManager(db)

    # Accept the quest
    quest = await manager.accept_quest(
        quest_id=quest_id,
        player_id=current_player["_id"],
    )

    return {
        "quest": quest,
        "message": "You are now participating in this world quest!",
    }
