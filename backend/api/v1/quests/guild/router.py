"""Guild quests API routes"""

from fastapi import APIRouter, Depends, HTTPException, status

from .....core.database import get_database
from .....services.quests.guild import GuildQuestService
from ....deps import get_current_player

router = APIRouter(prefix="/guild", tags=["guild-quests"])


@router.get("/available")
async def get_available_guild_quests(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get available guild quests"""
    if not current_player.get("guild_id"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must be in a guild to view guild quests",
        )

    service = GuildQuestService(db)
    quests = await service.get_guild_quests(
        guild_id=current_player["guild_id"],
    )

    return {"quests": quests, "total": len(quests)}


@router.post("/generate")
async def generate_guild_quest(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Generate a new guild quest (requires officer+)"""
    if not current_player.get("guild_id"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must be in a guild",
        )

    service = GuildQuestService(db)

    try:
        quest = await service.generate_guild_quest(
            guild_id=current_player["guild_id"],
        )
        return {"quest": quest, "message": "Guild quest generated!"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/progress/{quest_id}")
async def get_guild_quest_progress(
    quest_id: str,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get guild quest progress"""
    service = GuildQuestService(db)
    progress = await service.get_quest_progress(quest_id)

    return {"progress": progress}
