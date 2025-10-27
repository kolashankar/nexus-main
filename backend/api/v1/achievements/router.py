from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Optional
from backend.models.achievements import (
    PlayerAchievements, AchievementCategory, AchievementRarity
)
from backend.services.achievements.achievement_service import (
    AchievementService, ACHIEVEMENT_DEFINITIONS
)
from backend.api.deps import get_current_player
from pydantic import BaseModel

router = APIRouter(prefix="/achievements", tags=["Achievements"])

class UpdateProgressRequest(BaseModel):
    achievement_id: str
    progress_amount: int

@router.get("/")
async def get_achievements(current_player: Dict = Depends(get_current_player)):
    """Get all achievements for the current player"""
    achievements_data = current_player.get("achievements")

    if not achievements_data:
        achievements = AchievementService.initialize_achievements(
            str(current_player["_id"]))
        return achievements.dict()

    return achievements_data

@router.get("/summary")
async def get_achievement_summary(current_player: Dict = Depends(get_current_player)):
    """Get achievement summary"""
    achievements_data = current_player.get("achievements")

    if not achievements_data:
        return {"message": "No achievements initialized"}

    achievements = PlayerAchievements(**achievements_data)
    summary = AchievementService.get_achievement_summary(achievements)

    return summary

@router.get("/unlocked")
async def get_unlocked_achievements(current_player: Dict = Depends(get_current_player)):
    """Get unlocked achievements"""
    achievements_data = current_player.get("achievements", {})

    if not achievements_data:
        return {"unlocked": []}

    achievements = PlayerAchievements(**achievements_data)
    return {"unlocked": achievements.unlocked_achievements}

@router.get("/progress")
async def get_achievement_progress(current_player: Dict = Depends(get_current_player)):
    """Get achievement progress"""
    achievements_data = current_player.get("achievements", {})

    if not achievements_data:
        return {"progress": {}}

    achievements = PlayerAchievements(**achievements_data)
    return {"progress": achievements.achievement_progress}

@router.get("/definitions")
async def get_achievement_definitions(
    category: Optional[AchievementCategory] = None,
    rarity: Optional[AchievementRarity] = None
):
    """Get achievement definitions with optional filters"""
    definitions = list(ACHIEVEMENT_DEFINITIONS.values())

    if category:
        definitions = [d for d in definitions if d.category == category]

    if rarity:
        definitions = [d for d in definitions if d.rarity == rarity]

    # Don't show hidden achievements
    visible_definitions = [d for d in definitions if not d.hidden]

    return {
        "total": len(visible_definitions),
        "achievements": [d.dict() for d in visible_definitions]
    }

@router.get("/definitions/{achievement_id}")
async def get_achievement_definition(achievement_id: str):
    """Get a specific achievement definition"""
    if achievement_id not in ACHIEVEMENT_DEFINITIONS:
        raise HTTPException(status_code=404, detail="Achievement not found")

    definition = ACHIEVEMENT_DEFINITIONS[achievement_id]

    # Don't reveal hidden achievement details
    if definition.hidden:
        return {
            "achievement_id": achievement_id,
            "name": "???",
            "description": "Hidden achievement",
            "category": definition.category,
            "rarity": definition.rarity,
            "hidden": True
        }

    return definition.dict()

@router.get("/category/{category}")
async def get_achievements_by_category(
    category: AchievementCategory,
    current_player: Dict = Depends(get_current_player)
):
    """Get achievements by category"""
    category_achievements = AchievementService.get_category_achievements(
        category)

    # Get player's unlocked achievements
    achievements_data = current_player.get("achievements", {})
    unlocked_ids = []
    if achievements_data:
        achievements = PlayerAchievements(**achievements_data)
        unlocked_ids = [
            a.achievement_id for a in achievements.unlocked_achievements]

    result = []
    for achievement in category_achievements:
        result.append({
            "definition": achievement.dict(),
            "unlocked": achievement.achievement_id in unlocked_ids
        })

    return {
        "category": category,
        "total": len(result),
        "achievements": result
    }

@router.post("/unlock/{achievement_id}")
async def unlock_achievement(
    achievement_id: str,
    current_player: Dict = Depends(get_current_player)
):
    """Unlock an achievement (usually called by system)"""
    achievements_data = current_player.get("achievements")

    if not achievements_data:
        achievements = AchievementService.initialize_achievements(
            str(current_player["_id"]))
    else:
        achievements = PlayerAchievements(**achievements_data)

    success, message = AchievementService.unlock_achievement(
        achievements,
        achievement_id
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "success": True,
        "message": message,
        "achievement_id": achievement_id,
        "total_points": achievements.total_points
    }

@router.post("/progress/update")
async def update_achievement_progress(
    request: UpdateProgressRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Update progress towards an achievement"""
    achievements_data = current_player.get("achievements")

    if not achievements_data:
        achievements = AchievementService.initialize_achievements(
            str(current_player["_id"]))
    else:
        achievements = PlayerAchievements(**achievements_data)

    AchievementService.update_progress(
        achievements,
        request.achievement_id,
        request.progress_amount
    )

    progress = achievements.achievement_progress.get(request.achievement_id)

    return {
        "success": True,
        "achievement_id": request.achievement_id,
        "progress": progress.dict() if progress else None
    }

@router.get("/recent")
async def get_recent_unlocks(current_player: Dict = Depends(get_current_player)):
    """Get recently unlocked achievements"""
    achievements_data = current_player.get("achievements", {})

    if not achievements_data:
        return {"recent": []}

    achievements = PlayerAchievements(**achievements_data)
    recent_ids = achievements.recent_unlocks[:10]

    recent_achievements = []
    for achievement_id in recent_ids:
        if achievement_id in ACHIEVEMENT_DEFINITIONS:
            definition = ACHIEVEMENT_DEFINITIONS[achievement_id]
            unlocked = next(
                (a for a in achievements.unlocked_achievements if a.achievement_id == achievement_id),
                None
            )
            recent_achievements.append({
                "definition": definition.dict(),
                "unlocked_at": unlocked.unlocked_at if unlocked else None
            })

    return {"recent": recent_achievements}
