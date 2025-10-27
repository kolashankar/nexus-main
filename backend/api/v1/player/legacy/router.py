from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from backend.models.player.legacy import PlayerLegacy
from backend.services.player.legacy import LegacyService, LEGACY_PERKS
from backend.api.deps import get_current_player
from pydantic import BaseModel

router = APIRouter(prefix="/legacy", tags=["Legacy"])

class UnlockPerkRequest(BaseModel):
    perk_id: str

class ActivatePerkRequest(BaseModel):
    perk_id: str

class EarnPointsRequest(BaseModel):
    amount: int
    source: str

@router.get("/")
async def get_legacy(current_player: Dict = Depends(get_current_player)):
    """Get legacy information for the current account"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        account_id = str(current_player.get("_id", ""))
        legacy = LegacyService.initialize_legacy(account_id)
        return legacy.dict()

    return legacy_data

@router.get("/summary")
async def get_legacy_summary(current_player: Dict = Depends(get_current_player)):
    """Get legacy system summary"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        return {"message": "No legacy initialized"}

    legacy = PlayerLegacy(**legacy_data)
    summary = LegacyService.get_legacy_summary(legacy)

    return summary

@router.get("/perks")
async def get_available_perks():
    """Get all available legacy perks"""
    return {"perks": [perk.dict() for perk in LEGACY_PERKS]}

@router.get("/perks/unlocked")
async def get_unlocked_perks(current_player: Dict = Depends(get_current_player)):
    """Get unlocked perks"""
    legacy_data = current_player.get("legacy", {})

    if not legacy_data:
        return {"unlocked_perks": []}

    legacy = PlayerLegacy(**legacy_data)
    return {"unlocked_perks": [p.dict() for p in legacy.unlocked_perks]}

@router.get("/perks/active")
async def get_active_perks(current_player: Dict = Depends(get_current_player)):
    """Get active perks"""
    legacy_data = current_player.get("legacy", {})

    if not legacy_data:
        return {"active_perks": []}

    legacy = PlayerLegacy(**legacy_data)
    return {"active_perks": legacy.active_perks}

@router.post("/perks/unlock")
async def unlock_perk(
    request: UnlockPerkRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Unlock a legacy perk"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        account_id = str(current_player.get("_id", ""))
        legacy = LegacyService.initialize_legacy(account_id)
    else:
        legacy = PlayerLegacy(**legacy_data)

    success, message = LegacyService.unlock_perk(legacy, request.perk_id)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "success": True,
        "message": message,
        "remaining_points": legacy.legacy_points
    }

@router.post("/perks/activate")
async def activate_perk(
    request: ActivatePerkRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Activate a legacy perk"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        raise HTTPException(status_code=404, detail="Legacy not initialized")

    legacy = PlayerLegacy(**legacy_data)
    success, message = LegacyService.activate_perk(legacy, request.perk_id)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "success": True,
        "message": message,
        "active_perks": legacy.active_perks
    }

@router.post("/perks/deactivate/{perk_id}")
async def deactivate_perk(
    perk_id: str,
    current_player: Dict = Depends(get_current_player)
):
    """Deactivate a legacy perk"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        raise HTTPException(status_code=404, detail="Legacy not initialized")

    legacy = PlayerLegacy(**legacy_data)

    if perk_id in legacy.active_perks:
        legacy.active_perks.remove(perk_id)

    return {
        "success": True,
        "message": "Perk deactivated",
        "active_perks": legacy.active_perks
    }

@router.post("/points/earn")
async def earn_legacy_points(
    request: EarnPointsRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Earn legacy points (usually called by system)"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        account_id = str(current_player.get("_id", ""))
        legacy = LegacyService.initialize_legacy(account_id)
    else:
        legacy = PlayerLegacy(**legacy_data)

    success, message = LegacyService.earn_legacy_points(
        legacy,
        request.amount,
        request.source
    )

    return {
        "success": True,
        "message": message,
        "legacy_points": legacy.legacy_points,
        "lifetime_points": legacy.lifetime_legacy_points,
        "legacy_level": legacy.legacy_level
    }

@router.get("/titles")
async def get_legacy_titles(current_player: Dict = Depends(get_current_player)):
    """Get legacy titles"""
    legacy_data = current_player.get("legacy", {})

    if not legacy_data:
        return {"titles": []}

    legacy = PlayerLegacy(**legacy_data)
    return {"titles": [t.dict() for t in legacy.earned_titles]}

@router.post("/titles/activate/{title_id}")
async def activate_title(
    title_id: str,
    current_player: Dict = Depends(get_current_player)
):
    """Activate a legacy title"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        raise HTTPException(status_code=404, detail="Legacy not initialized")

    legacy = PlayerLegacy(**legacy_data)

    # Check if title is earned
    if not any(t.title_id == title_id for t in legacy.earned_titles):
        raise HTTPException(status_code=400, detail="Title not earned")

    legacy.active_title = title_id

    return {
        "success": True,
        "message": "Title activated",
        "active_title": title_id
    }

@router.get("/heirlooms")
async def get_heirlooms(current_player: Dict = Depends(get_current_player)):
    """Get heirloom items"""
    legacy_data = current_player.get("legacy", {})

    if not legacy_data:
        return {"heirlooms": []}

    legacy = PlayerLegacy(**legacy_data)
    return {"heirlooms": [h.dict() for h in legacy.heirloom_items]}

@router.get("/mentorship")
async def get_mentorship_stats(current_player: Dict = Depends(get_current_player)):
    """Get mentorship statistics"""
    legacy_data = current_player.get("legacy", {})

    if not legacy_data:
        return {"mentorship": {}}

    legacy = PlayerLegacy(**legacy_data)

    return {
        "mentorship_level": legacy.mentorship_level,
        "apprentices_taught": legacy.apprentices_taught,
        "rewards_earned": legacy.mentorship_rewards_earned
    }

@router.get("/new-character-bonuses")
async def get_new_character_bonuses(current_player: Dict = Depends(get_current_player)):
    """Get bonuses that apply to new characters"""
    legacy_data = current_player.get("legacy")

    if not legacy_data:
        account_id = str(current_player.get("_id", ""))
        legacy = LegacyService.initialize_legacy(account_id)
    else:
        legacy = PlayerLegacy(**legacy_data)

    bonuses = LegacyService.apply_new_character_bonuses(legacy)

    return {"bonuses": bonuses}
