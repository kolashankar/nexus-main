"""API endpoints for trait actions and abilities."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from backend.core.deps import get_current_player, get_database
from backend.services.player.trait_ability_service import TraitAbilityService

# Import all trait abilities
from backend.services.traits.hacking_ability import HackingAbility
from backend.services.traits.negotiation_ability import NegotiationAbility
from backend.services.traits.stealth_ability import StealthAbility
from backend.services.traits.leadership_ability import LeadershipAbility
from backend.services.traits.meditation_ability import MeditationAbility
from backend.services.traits.telekinesis_ability import TelekinesisAbility
from backend.services.traits.pyrokinesis_ability import PyrokinesisAbility
from backend.services.traits.cryokinesis_ability import CryokinesisAbility
from backend.services.traits.empathy_ability import EmpathyAbility
from backend.services.traits.integrity_ability import IntegrityAbility
from backend.services.traits.compassion_ability import CompassionAbility
from backend.services.traits.honesty_ability import HonestyAbility
from backend.services.traits.envy_ability import EnvyAbility
from backend.services.traits.wrath_ability import WrathAbility
from backend.services.traits.sloth_ability import SlothAbility
from backend.services.traits.pride_ability import PrideAbility
from backend.services.traits.luck_ability import LuckAbility
from backend.services.traits.resilience_ability import ResilienceAbility
from backend.services.traits.wisdom_ability import WisdomAbility
from backend.services.traits.adaptability_ability import AdaptabilityAbility
from backend.services.traits.greed_ability import GreedAbility
from backend.services.traits.arrogance_ability import ArroganceAbility

router = APIRouter()

# Request/Response Models
class UseTraitAbilityRequest(BaseModel):
    trait_id: str = Field(..., description="Trait ID to use")
    target_id: Optional[str] = Field(None, description="Target player ID if applicable")
    
class EquipTraitRequest(BaseModel):
    trait_id: str = Field(..., description="Trait to equip")
    trait_type: str = Field(..., description="Type: skill, superpower_tool, meta_trait, virtue, vice")
    trait_level: int = Field(default=1, ge=1, le=100)
    slot_number: int = Field(..., ge=1, le=6, description="Slot 1-6")

# ===== TRAIT MANAGEMENT =====

@router.get("/equipped")
async def get_equipped_traits(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Get player's currently equipped traits."""
    
    service = TraitAbilityService(db)
    equipped = await service.get_player_equipped_traits(current_player["_id"])
    
    if not equipped:
        return {
            "equipped_traits": {},
            "message": "No traits equipped"
        }
    
    return {
        "equipped_traits": equipped.model_dump(exclude={"id", "created_at", "updated_at"}),
        "message": "Equipped traits retrieved"
    }

@router.post("/equip")
async def equip_trait(
    request: EquipTraitRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Equip a trait to a specific slot."""
    
    service = TraitAbilityService(db)
    
    # Check if player owns this trait
    player_traits = current_player.get("traits", {})
    trait_value = player_traits.get(request.trait_id, 0)
    
    if trait_value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You don't own this trait"
        )
    
    # Equip the trait
    success = await service.equip_trait(
        player_id=current_player["_id"],
        trait_id=request.trait_id,
        trait_type=request.trait_type,
        trait_level=request.trait_level,
        slot_number=request.slot_number
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to equip trait"
        )
    
    return {
        "success": True,
        "message": f"Trait {request.trait_id} equipped to slot {request.slot_number}"
    }

@router.post("/unequip/{slot_number}")
async def unequip_trait(
    slot_number: int,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Unequip a trait from a slot."""
    
    if not 1 <= slot_number <= 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slot number must be between 1 and 6"
        )
    
    service = TraitAbilityService(db)
    success = await service.unequip_trait(current_player["_id"], slot_number)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No trait in that slot"
        )
    
    return {
        "success": True,
        "message": f"Trait unequipped from slot {slot_number}"
    }

# ===== TRAIT ABILITIES - SKILLS =====

@router.post("/actions/hacking/credit-hack")
async def use_credit_hack(
    request: UseTraitAbilityRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Hacking skill to steal credits from target player."""
    
    if not request.target_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target player ID required"
        )
    
    service = TraitAbilityService(db)
    
    # Check if can use ability
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "hacking"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    # Check range
    if "position" not in current_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position not available"
        )
    
    nearby_players = await service.get_players_in_range(
        current_player["position"],
        100,  # 100m range
        current_player["_id"]
    )
    
    target_in_range = any(p["player_id"] == request.target_id for p in nearby_players)
    if not target_in_range:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target not in range (need within 100m)"
        )
    
    # Execute hack
    hacking_service = HackingAbility(db)
    hacker_level = current_player.get("level", 1)
    hacking_trait_level = int(current_player.get("traits", {}).get("hacking", 1))
    
    result = await hacking_service.credit_hack(
        hacker_id=current_player["_id"],
        target_id=request.target_id,
        hacker_level=hacker_level,
        hacker_trait_level=hacking_trait_level
    )
    
    # If successful, consume energy and start cooldown
    if result["success"]:
        await service.consume_energy(current_player["_id"], "hacking")
        await service.start_cooldown(current_player["_id"], "hacking", "skill")
        
        # Log usage
        await service.log_trait_usage(
            player_id=current_player["_id"],
            trait_id="hacking",
            trait_type="skill",
            action_type="credit_hack",
            target_id=request.target_id,
            success=True,
            karma_change=-result.get("karma_loss", 0),
            credits_affected=result.get("amount_stolen", 0),
            location=current_player.get("position")
        )
    
    return result

@router.post("/actions/stealth/shadow-walk")
async def use_shadow_walk(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Activate Stealth - Shadow Walk ability."""
    
    service = TraitAbilityService(db)
    
    # Check if can use
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "stealth"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    # Execute stealth
    stealth_service = StealthAbility(db)
    stealth_trait_level = int(current_player.get("traits", {}).get("stealth", 1))
    
    result = await stealth_service.shadow_walk(
        player_id=current_player["_id"],
        trait_level=stealth_trait_level
    )
    
    # Consume energy and start cooldown
    await service.consume_energy(current_player["_id"], "stealth")
    await service.start_cooldown(current_player["_id"], "stealth", "skill")
    
    # Log usage
    await service.log_trait_usage(
        player_id=current_player["_id"],
        trait_id="stealth",
        trait_type="skill",
        action_type="shadow_walk",
        success=True,
        location=current_player.get("position")
    )
    
    return result

@router.post("/actions/leadership/rally-cry")
async def use_rally_cry(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Activate Leadership - Rally Cry to buff nearby allies."""
    
    service = TraitAbilityService(db)
    
    # Check if can use
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "leadership"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    if "position" not in current_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Position not available"
        )
    
    # Execute rally cry
    leadership_service = LeadershipAbility(db)
    leadership_trait_level = int(current_player.get("traits", {}).get("leadership", 1))
    
    result = await leadership_service.rally_cry(
        leader_id=current_player["_id"],
        leader_position=current_player["position"],
        trait_level=leadership_trait_level
    )
    
    if result["success"]:
        # Consume energy and start cooldown
        await service.consume_energy(current_player["_id"], "leadership")
        await service.start_cooldown(current_player["_id"], "leadership", "skill")
        
        # Log usage
        await service.log_trait_usage(
            player_id=current_player["_id"],
            trait_id="leadership",
            trait_type="skill",
            action_type="rally_cry",
            success=True,
            karma_change=5,
            location=current_player.get("position")
        )
    
    return result

# ===== TRAIT ABILITIES - SUPERPOWER TOOLS =====

@router.post("/actions/meditation/karmic-trace")
async def use_karmic_trace(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Meditation superpower to track those who wronged you."""
    
    service = TraitAbilityService(db)
    
    # Check if can use
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "meditation_sp"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    # Execute karmic trace
    meditation_service = MeditationAbility(db)
    meditation_trait_level = int(current_player.get("traits", {}).get("meditation", 1))
    
    result = await meditation_service.karmic_trace(
        player_id=current_player["_id"],
        trait_level=meditation_trait_level
    )
    
    if result["success"]:
        # Consume energy and start cooldown
        await service.consume_energy(current_player["_id"], "meditation_sp")
        await service.start_cooldown(current_player["_id"], "meditation_sp", "superpower_tool")
        
        # Log usage
        await service.log_trait_usage(
            player_id=current_player["_id"],
            trait_id="meditation_sp",
            trait_type="superpower_tool",
            action_type="karmic_trace",
            success=True,
            karma_change=10,
            location=current_player.get("position")
        )
    
    return result

# ===== TRAIT ABILITIES - VIRTUES =====

@router.post("/actions/empathy/emotional-shield")
async def use_emotional_shield(
    request: UseTraitAbilityRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Empathy to absorb ally's mental afflictions."""
    
    if not request.target_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target ally ID required"
        )
    
    service = TraitAbilityService(db)
    
    # Check if can use
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "empathy"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    # Execute emotional shield
    empathy_service = EmpathyAbility(db)
    empathy_trait_level = int(current_player.get("traits", {}).get("empathy", 1))
    
    result = await empathy_service.emotional_shield(
        caster_id=current_player["_id"],
        target_id=request.target_id,
        trait_level=empathy_trait_level
    )
    
    if result["success"]:
        # Consume energy and start cooldown
        await service.consume_energy(current_player["_id"], "empathy")
        await service.start_cooldown(current_player["_id"], "empathy", "virtue")
        
        # Log usage
        await service.log_trait_usage(
            player_id=current_player["_id"],
            trait_id="empathy",
            trait_type="virtue",
            action_type="emotional_shield",
            target_id=request.target_id,
            success=True,
            karma_change=10,
            location=current_player.get("position")
        )
    
    return result

@router.post("/actions/integrity/unbreakable-will")
async def use_unbreakable_will(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Integrity to become immune to control effects."""
    
    service = TraitAbilityService(db)
    
    # Check if can use
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "integrity"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    # Execute unbreakable will
    integrity_service = IntegrityAbility(db)
    integrity_trait_level = int(current_player.get("traits", {}).get("integrity", 1))
    
    result = await integrity_service.unbreakable_will(
        player_id=current_player["_id"],
        trait_level=integrity_trait_level
    )
    
    # Consume energy and start cooldown
    await service.consume_energy(current_player["_id"], "integrity")
    await service.start_cooldown(current_player["_id"], "integrity", "virtue")
    
    # Log usage
    await service.log_trait_usage(
        player_id=current_player["_id"],
        trait_id="integrity",
        trait_type="virtue",
        action_type="unbreakable_will",
        success=True,
        karma_change=8,
        location=current_player.get("position")
    )
    
    return result

# ===== TRAIT ABILITIES - VICES =====

@router.post("/actions/greed/plunder")
async def use_plunder(
    request: UseTraitAbilityRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Greed to plunder extra loot from defeated enemy."""
    
    if not request.target_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target enemy ID required"
        )
    
    service = TraitAbilityService(db)
    
    # Check if can use
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "greed"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    # Execute plunder
    greed_service = GreedAbility(db)
    greed_trait_level = int(current_player.get("traits", {}).get("greed", 1))
    
    result = await greed_service.plunder(
        plunderer_id=current_player["_id"],
        target_id=request.target_id,
        trait_level=greed_trait_level
    )
    
    if result["success"]:
        # Consume energy and start cooldown
        await service.consume_energy(current_player["_id"], "greed")
        await service.start_cooldown(current_player["_id"], "greed", "vice")
        
        # Log usage
        await service.log_trait_usage(
            player_id=current_player["_id"],
            trait_id="greed",
            trait_type="vice",
            action_type="plunder",
            target_id=request.target_id,
            success=True,
            karma_change=-15,
            credits_affected=result.get("extra_credits", 0),
            location=current_player.get("position")
        )
    
    return result

@router.post("/actions/arrogance/crushing-ego")
async def use_crushing_ego(
    request: UseTraitAbilityRequest,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Arrogance to debuff and taunt enemy."""
    
    if not request.target_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target player ID required"
        )
    
    service = TraitAbilityService(db)
    
    # Check if can use
    can_use, message, cooldown = await service.can_use_ability(
        current_player["_id"],
        "arrogance"
    )
    
    if not can_use:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{message}" + (f" ({cooldown}s remaining)" if cooldown else "")
        )
    
    # Execute crushing ego
    arrogance_service = ArroganceAbility(db)
    arrogance_trait_level = int(current_player.get("traits", {}).get("arrogance", 1))
    
    result = await arrogance_service.crushing_ego(
        caster_id=current_player["_id"],
        target_id=request.target_id,
        trait_level=arrogance_trait_level
    )
    
    if result["success"]:
        # Consume energy and start cooldown
        await service.consume_energy(current_player["_id"], "arrogance")
        await service.start_cooldown(current_player["_id"], "arrogance", "vice")
        
        # Log usage
        await service.log_trait_usage(
            player_id=current_player["_id"],
            trait_id="arrogance",
            trait_type="vice",
            action_type="crushing_ego",
            target_id=request.target_id,
            success=True,
            karma_change=-10,
            location=current_player.get("position")
        )
    
    return result

# ===== UTILITY ENDPOINTS =====

@router.get("/history")
async def get_trait_usage_history(
    limit: int = 50,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Get player's trait usage history."""
    
    service = TraitAbilityService(db)
    history = await service.get_trait_usage_history(current_player["_id"], limit)
    
    return {
        "history": history,
        "total": len(history)
    }

@router.get("/cooldowns")
async def get_active_cooldowns(
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Get all active cooldowns for player."""
    
    from datetime import datetime
    
    cursor = db.trait_cooldowns.find({
        "player_id": current_player["_id"],
        "is_active": True
    })
    
    cooldowns = await cursor.to_list(length=None)
    
    # Calculate remaining time
    for cd in cooldowns:
        if cd["available_at"] > datetime.utcnow():
            cd["seconds_remaining"] = int((cd["available_at"] - datetime.utcnow()).total_seconds())
        else:
            cd["seconds_remaining"] = 0
            # Mark as inactive
            await db.trait_cooldowns.update_one(
                {"_id": cd["_id"]},
                {"$set": {"is_active": False}}
            )
    
    return {
        "cooldowns": cooldowns,
        "total": len(cooldowns)
    }
