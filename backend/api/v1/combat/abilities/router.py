"""Combat abilities routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user
from backend.services.combat.abilities import CombatAbilitiesService

router = APIRouter(prefix="/abilities", tags=["combat", "abilities"])
abilities_service = CombatAbilitiesService()


@router.get("/available")
async def get_available_abilities(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all available combat abilities for current player."""
    try:
        abilities = await abilities_service.get_available_abilities(current_user["_id"])
        return {
            "abilities": abilities,
            "total": len(abilities)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/all")
async def get_all_abilities():
    """Get all possible combat abilities with unlock requirements."""
    from backend.services.combat.abilities import CombatAbilitiesService

    abilities_list = []
    for trait_name, ability_data in CombatAbilitiesService.TRAIT_ABILITIES.items():
        abilities_list.append({
            "id": trait_name,
            "trait_required": trait_name,
            "trait_level_required": 80,
            **ability_data
        })

    return {
        "abilities": abilities_list,
        "total": len(abilities_list)
    }


@router.get("/cooldowns")
async def get_ability_cooldowns(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get current ability cooldowns."""
    from backend.core.database import get_database

    db = await get_database()
    cooldowns = await db.ability_cooldowns.find_one({"player_id": current_user["_id"]})

    if not cooldowns:
        return {"cooldowns": {}}

    return {"cooldowns": cooldowns.get("abilities", {})}


@router.get("/{ability_id}")
async def get_ability_details(
    ability_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed information about a specific ability."""
    from backend.services.combat.abilities import CombatAbilitiesService

    if ability_id not in CombatAbilitiesService.TRAIT_ABILITIES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ability not found"
        )

    ability_data = CombatAbilitiesService.TRAIT_ABILITIES[ability_id]

    # Check if player has unlocked it
    from backend.core.database import get_database
    from bson import ObjectId

    db = await get_database()
    player = await db.players.find_one({"_id": ObjectId(current_user["_id"])})

    trait_value = player.get("traits", {}).get(ability_id, 0)
    unlocked = trait_value >= 80

    # Check cooldown
    on_cooldown = not await abilities_service.check_ability_cooldown(
        current_user["_id"],
        ability_id
    )

    return {
        "id": ability_id,
        "trait_required": ability_id,
        "trait_level_required": 80,
        "current_trait_level": trait_value,
        "unlocked": unlocked,
        "on_cooldown": on_cooldown,
        **ability_data
    }
