from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from backend.models.player.superpowers import PlayerSuperpowers
from backend.services.player.superpowers import SuperpowerService, SUPERPOWER_DEFINITIONS
from backend.api.deps import get_current_player
from pydantic import BaseModel

router = APIRouter(prefix="/superpowers", tags=["Superpowers"])

class UnlockPowerRequest(BaseModel):
    power_id: str

class EquipPowerRequest(BaseModel):
    power_id: str

class UsePowerRequest(BaseModel):
    power_id: str

@router.get("/")
async def get_superpowers(current_player: Dict = Depends(get_current_player)):
    """Get all superpowers for the current player"""
    superpowers_data = current_player.get("superpowers")

    if not superpowers_data:
        superpowers = SuperpowerService.initialize_superpowers(
            str(current_player["_id"]))
        return superpowers.dict()

    return superpowers_data

@router.get("/available")
async def get_available_powers(current_player: Dict = Depends(get_current_player)):
    """Get list of powers player can unlock"""
    player_traits = current_player.get("traits", {})
    available = SuperpowerService.get_available_powers(player_traits)

    return {"available_powers": available}

@router.get("/definitions")
async def get_power_definitions():
    """Get all superpower definitions"""
    definitions = []
    for power_id, power_def in SUPERPOWER_DEFINITIONS.items():
        definitions.append({
            "power_id": power_id,
            "name": power_def.name,
            "description": power_def.description,
            "tier": power_def.tier,
            "requirements": power_def.requirements,
            "cooldown_seconds": power_def.cooldown_seconds,
            "energy_cost": power_def.energy_cost
        })

    return {"powers": definitions}

@router.get("/definitions/{power_id}")
async def get_power_definition(power_id: str):
    """Get a specific superpower definition"""
    if power_id not in SUPERPOWER_DEFINITIONS:
        raise HTTPException(status_code=404, detail="Power not found")

    power_def = SUPERPOWER_DEFINITIONS[power_id]
    return power_def.dict()

@router.post("/unlock")
async def unlock_power(
    request: UnlockPowerRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Unlock a superpower"""
    superpowers_data = current_player.get("superpowers")
    player_traits = current_player.get("traits", {})

    if not superpowers_data:
        superpowers = SuperpowerService.initialize_superpowers(
            str(current_player["_id"]))
    else:
        superpowers = PlayerSuperpowers(**superpowers_data)

    success, message = SuperpowerService.unlock_power(
        superpowers,
        player_traits,
        request.power_id
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "success": True,
        "message": message,
        "power_id": request.power_id,
        "total_unlocked": superpowers.total_powers_unlocked
    }

@router.post("/equip")
async def equip_power(
    request: EquipPowerRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Equip a superpower"""
    superpowers_data = current_player.get("superpowers")

    if not superpowers_data:
        raise HTTPException(
            status_code=404, detail="Superpowers not initialized")

    superpowers = PlayerSuperpowers(**superpowers_data)

    success = superpowers.equip_power(request.power_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to equip power")

    return {
        "success": True,
        "message": "Power equipped",
        "equipped_powers": superpowers.equipped_powers
    }

@router.post("/unequip/{power_id}")
async def unequip_power(
    power_id: str,
    current_player: Dict = Depends(get_current_player)
):
    """Unequip a superpower"""
    superpowers_data = current_player.get("superpowers")

    if not superpowers_data:
        raise HTTPException(
            status_code=404, detail="Superpowers not initialized")

    superpowers = PlayerSuperpowers(**superpowers_data)

    if power_id in superpowers.equipped_powers:
        superpowers.equipped_powers.remove(power_id)

    return {
        "success": True,
        "message": "Power unequipped",
        "equipped_powers": superpowers.equipped_powers
    }

@router.post("/use")
async def use_power(
    request: UsePowerRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Use a superpower"""
    superpowers_data = current_player.get("superpowers")

    if not superpowers_data:
        raise HTTPException(
            status_code=404, detail="Superpowers not initialized")

    superpowers = PlayerSuperpowers(**superpowers_data)

    success, message, effects = SuperpowerService.use_power(
        superpowers,
        request.power_id
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "success": True,
        "message": message,
        "effects": effects,
        "power_id": request.power_id
    }
