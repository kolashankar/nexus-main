"""Quest API routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from datetime import datetime

from ....core.database import get_database
from ....services.quests.manager import QuestManager
from ....services.quests.generator import QuestGenerator
from ....models.quests.quest import QuestType, QuestStatus
from .schemas import (
    QuestResponse,
    QuestListResponse,
    QuestAcceptRequest,
    QuestAbandonRequest,
    QuestCompleteRequest,
    ObjectiveProgressRequest,
    QuestGenerateRequest,
)
from ...deps import get_current_player

router = APIRouter(prefix="/quests", tags=["quests"])


@router.get("/available", response_model=QuestListResponse)
async def get_available_quests(
    quest_type: Optional[QuestType] = None,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get available quests for player"""
    manager = QuestManager(db)

    # Get player's current traits and items
    player_level = current_player.get("level", 1)
    player_karma = current_player.get("karma_points", 0)
    player_traits = current_player.get("traits", {})
    player_items = [item["item_id"]
        for item in current_player.get("items", [])]

    quests = await manager.get_available_quests(
        player_id=current_player["_id"],
        quest_type=quest_type,
        player_level=player_level,
        player_karma=player_karma,
        player_traits=player_traits,
        player_items=player_items,
    )

    return {"quests": quests, "total": len(quests)}


@router.get("/active", response_model=QuestListResponse)
async def get_active_quests(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get player's active quests"""
    manager = QuestManager(db)
    quests = await manager.get_player_quests(
        player_id=current_player["_id"],
        status=QuestStatus.ACTIVE,
    )
    return {"quests": quests, "total": len(quests)}


@router.get("/completed", response_model=QuestListResponse)
async def get_completed_quests(
    limit: int = Query(50, ge=1, le=100),
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get player's completed quests"""
    manager = QuestManager(db)
    quests = await manager.get_player_quests(
        player_id=current_player["_id"],
        status=QuestStatus.COMPLETED,
        limit=limit,
    )
    return {"quests": quests, "total": len(quests)}


@router.get("/{quest_id}", response_model=QuestResponse)
async def get_quest(
    quest_id: str,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get quest details"""
    manager = QuestManager(db)
    quest = await manager.get_quest(quest_id)

    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )

    # Check if player can view this quest
    if quest.get("player_id") and quest["player_id"] != current_player["_id"]:
        if quest.get("quest_type") not in ["world", "guild"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot view this quest"
            )

    return {"quest": quest}


@router.post("/accept", response_model=QuestResponse)
async def accept_quest(
    request: QuestAcceptRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Accept a quest"""
    manager = QuestManager(db)

    # Check if quest exists
    quest = await manager.get_quest(request.quest_id)
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quest not found"
        )

    # Accept quest
    try:
        updated_quest = await manager.accept_quest(
            quest_id=request.quest_id,
            player_id=current_player["_id"],
        )
        return {"quest": updated_quest}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/abandon", response_model=dict)
async def abandon_quest(
    request: QuestAbandonRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Abandon a quest"""
    manager = QuestManager(db)

    try:
        success = await manager.abandon_quest(
            quest_id=request.quest_id,
            player_id=current_player["_id"],
        )
        return {"success": success, "message": "Quest abandoned"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/progress", response_model=QuestResponse)
async def update_quest_progress(
    request: ObjectiveProgressRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Update quest objective progress"""
    manager = QuestManager(db)

    try:
        updated_quest = await manager.update_objective_progress(
            quest_id=request.quest_id,
            objective_id=request.objective_id,
            progress=request.progress,
            player_id=current_player["_id"],
        )
        return {"quest": updated_quest}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/complete", response_model=dict)
async def complete_quest(
    request: QuestCompleteRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Complete a quest and claim rewards"""
    manager = QuestManager(db)

    try:
        result = await manager.complete_quest(
            quest_id=request.quest_id,
            player_id=current_player["_id"],
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/daily", response_model=QuestListResponse)
async def get_daily_quests(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get daily quests"""
    manager = QuestManager(db)
    generator = QuestGenerator(db)

    # Check if daily quests exist for today
    daily_quests = await manager.get_player_quests(
        player_id=current_player["_id"],
        quest_type=QuestType.DAILY,
        status=None,  # Any status
    )

    # Filter to today's quests
    today = datetime.utcnow().date()
    today_quests = [
        q for q in daily_quests
        if datetime.fromisoformat(q["generated_at"].replace("Z", "+00:00")).date() == today
    ]

    # Generate new daily quests if needed (should be 3)
    if len(today_quests) < 3:
        new_quests = await generator.generate_daily_quests(
            player_id=current_player["_id"],
            player=current_player,
            count=3 - len(today_quests),
        )
        today_quests.extend(new_quests)

    return {"quests": today_quests, "total": len(today_quests)}


@router.get("/weekly", response_model=QuestListResponse)
async def get_weekly_quests(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Get weekly quests"""
    manager = QuestManager(db)
    generator = QuestGenerator(db)

    # Check if weekly quests exist
    weekly_quests = await manager.get_player_quests(
        player_id=current_player["_id"],
        quest_type=QuestType.WEEKLY,
        status=None,
    )

    # Generate if needed (should be 5)
    if len(weekly_quests) < 5:
        new_quests = await generator.generate_weekly_quests(
            player_id=current_player["_id"],
            player=current_player,
            count=5 - len(weekly_quests),
        )
        weekly_quests.extend(new_quests)

    return {"quests": weekly_quests, "total": len(weekly_quests)}


@router.post("/generate", response_model=QuestResponse)
async def generate_quest(
    request: QuestGenerateRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database),
):
    """Generate a new quest using AI (Oracle)"""
    generator = QuestGenerator(db)

    try:
        quest = await generator.generate_personal_quest(
            player_id=current_player["_id"],
            player=current_player,
            quest_type=request.quest_type or "personal",
        )
        return {"quest": quest}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate quest: {str(e)}"
        )
