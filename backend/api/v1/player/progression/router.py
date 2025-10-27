"""Player Progression API Routes."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from backend.api.deps import get_current_user
from backend.models.player.player import Player
from backend.services.player.progression import ProgressionService
from backend.utils.progression_calculator import (
    calculate_level_from_xp
)

router = APIRouter(prefix="/progression", tags=["progression"])
progression_service = ProgressionService()

@router.get("")
async def get_progression_data(
    current_user: Player = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get complete progression data for player."""
    try:
        # Calculate level info
        level, xp_progress, xp_for_next = calculate_level_from_xp(
            current_user.xp)

        # Get skill tree progress
        skill_tree_progress = {}
        for trait_name, tree_data in current_user.skill_trees.items():
            unlocked_count = len(tree_data.get("nodes_unlocked", []))
            skill_tree_progress[trait_name] = (unlocked_count / 20) * 100

        # Count superpowers
        superpowers_unlocked = len(
            [p for p in current_user.superpowers if p.get("unlocked", False)])

        # Get achievements
        achievements_unlocked = len(current_user.achievements)

        return {
            "level": level,
            "xp": current_user.xp,
            "xp_progress": xp_progress,
            "xp_for_next": xp_for_next,
            "prestige_level": current_user.prestige_level,
            "skill_tree_progress": skill_tree_progress,
            "superpowers_unlocked": superpowers_unlocked,
            "achievements_unlocked": achievements_unlocked,
            "total_achievements": 100  # From achievement_definitions.py
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/xp")
async def gain_xp(
    amount: int,
    current_user: Player = Depends(get_current_user)
) -> Dict[str, Any]:
    """Add XP to player and handle level ups."""
    try:
        old_xp = current_user.xp
        old_level = calculate_level_from_xp(old_xp)[0]

        new_xp = old_xp + amount
        new_level = calculate_level_from_xp(new_xp)[0]

        # Update player
        current_user.xp = new_xp
        current_user.level = new_level
        await current_user.save()

        level_up = new_level > old_level

        return {
            "success": True,
            "new_xp": new_xp,
            "new_level": new_level,
            "level_up": level_up,
            "levels_gained": new_level - old_level if level_up else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_progression_summary(
    current_user: Player = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get summarized progression statistics."""
    try:
        level, _, _ = calculate_level_from_xp(current_user.xp)

        return {
            "level": level,
            "prestige_level": current_user.prestige_level,
            "total_skill_nodes": sum(len(tree.get("nodes_unlocked", [])) for tree in current_user.skill_trees.values()),
            "total_superpowers": len([p for p in current_user.superpowers if p.get("unlocked")]),
            "total_achievements": len(current_user.achievements),
            "completion_percentage": progression_service.calculate_completion_percentage(current_user)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
