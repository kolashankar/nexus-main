from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from backend.models.player.prestige import PlayerPrestige
from backend.services.player.prestige import PrestigeService, PRESTIGE_REWARDS
from backend.api.deps import get_current_player

router = APIRouter(prefix="/prestige", tags=["Prestige"])

@router.get("/")
async def get_prestige(current_player: Dict = Depends(get_current_player)):
    """Get prestige information for the current player"""
    prestige_data = current_player.get("prestige")

    if not prestige_data:
        prestige = PrestigeService.initialize_prestige(
            str(current_player["_id"]))
        return prestige.dict()

    return prestige_data

@router.get("/benefits")
async def get_prestige_benefits(current_player: Dict = Depends(get_current_player)):
    """Get current prestige benefits"""
    prestige_data = current_player.get("prestige")

    if not prestige_data:
        prestige = PrestigeService.initialize_prestige(
            str(current_player["_id"]))
    else:
        prestige = PlayerPrestige(**prestige_data)

    benefits = PrestigeService.get_prestige_benefits(prestige)
    return benefits

@router.get("/eligibility")
async def check_prestige_eligibility(current_player: Dict = Depends(get_current_player)):
    """Check if player can prestige"""
    prestige_data = current_player.get("prestige")
    player_level = current_player.get("level", 1)
    karma_points = current_player.get("karma_points", 0)
    total_achievements = len(current_player.get(
        "achievements", {}).get("unlocked_achievements", []))

    if not prestige_data:
        prestige = PrestigeService.initialize_prestige(
            str(current_player["_id"]))
    else:
        prestige = PlayerPrestige(**prestige_data)

    eligible, message = PrestigeService.check_prestige_eligibility(
        prestige,
        player_level,
        karma_points,
        total_achievements
    )

    return {
        "eligible": eligible,
        "message": message,
        "current_level": player_level,
        "current_karma": karma_points,
        "current_achievements": total_achievements,
        "requirements": {
            "level": 100,
            "karma": 1000,
            "achievements": 50 if prestige.current_prestige_level >= 5 else 0
        }
    }

@router.post("/perform")
async def perform_prestige(current_player: Dict = Depends(get_current_player)):
    """Perform prestige reset"""
    prestige_data = current_player.get("prestige")
    player_traits = current_player.get("traits", {})
    player_level = current_player.get("level", 1)
    karma_points = current_player.get("karma_points", 0)
    total_achievements = len(current_player.get(
        "achievements", {}).get("unlocked_achievements", []))

    if not prestige_data:
        prestige = PrestigeService.initialize_prestige(
            str(current_player["_id"]))
    else:
        prestige = PlayerPrestige(**prestige_data)

    # Check eligibility first
    eligible, message = PrestigeService.check_prestige_eligibility(
        prestige,
        player_level,
        karma_points,
        total_achievements
    )

    if not eligible:
        raise HTTPException(status_code=400, detail=message)

    # Perform prestige
    success, rewards, new_traits = PrestigeService.perform_prestige(
        prestige,
        player_traits
    )

    if not success:
        raise HTTPException(status_code=400, detail="Failed to prestige")

    return {
        "success": True,
        "message": f"Prestiged to level {prestige.current_prestige_level}!",
        "prestige_level": prestige.current_prestige_level,
        "rewards": rewards,
        "new_traits": new_traits,
        "permanent_bonuses": prestige.permanent_bonuses
    }

@router.get("/rewards")
async def get_prestige_rewards():
    """Get all prestige rewards"""
    rewards = {}
    for level, reward in PRESTIGE_REWARDS.items():
        rewards[level] = reward.dict()

    return {"rewards": rewards}

@router.get("/rewards/{level}")
async def get_prestige_reward(level: int):
    """Get rewards for a specific prestige level"""
    if level not in PRESTIGE_REWARDS:
        raise HTTPException(status_code=404, detail="Prestige level not found")

    return PRESTIGE_REWARDS[level].dict()

@router.get("/history")
async def get_prestige_history(current_player: Dict = Depends(get_current_player)):
    """Get prestige history"""
    prestige_data = current_player.get("prestige")

    if not prestige_data:
        return {"history": []}

    prestige = PlayerPrestige(**prestige_data)

    return {
        "total_prestiges": prestige.total_prestiges,
        "current_level": prestige.current_prestige_level,
        "history": prestige.prestige_history
    }
