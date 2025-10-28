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


# ===== NEW TRAIT ABILITIES ROUTES =====

# Negotiation (Skill)
@router.post("/skills/negotiation/use")
async def use_negotiation_ability(
    ability_name: str,
    targets: Optional[List[str]] = None,
    target_id: Optional[str] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Negotiation skill abilities."""
    negotiation = NegotiationAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "persuade":
            if not target_id:
                raise HTTPException(400, "Target ID required for persuade")
            result = await negotiation.persuade(player_id, target_id, trait_level)
        elif ability_name == "broker_deal":
            if not targets:
                raise HTTPException(400, "Targets required for broker_deal")
            result = await negotiation.broker_deal(player_id, targets, trait_level)
        elif ability_name == "resolve_conflict":
            if not targets:
                raise HTTPException(400, "Targets required for resolve_conflict")
            result = await negotiation.resolve_conflict(player_id, targets, trait_level)
        else:
            raise HTTPException(400, f"Unknown negotiation ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Telekinesis (Superpower Tool)
@router.post("/superpowers/telekinesis/use")
async def use_telekinesis_ability(
    ability_name: str,
    targets: Optional[List[str]] = None,
    params: Optional[Dict] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Telekinesis superpower abilities."""
    telekinesis = TelekinesisAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "force_push":
            if not targets:
                raise HTTPException(400, "Targets required for force_push")
            result = await telekinesis.force_push(player_id, targets, trait_level)
        elif ability_name == "force_field":
            result = await telekinesis.force_field(player_id, trait_level)
        elif ability_name == "object_manipulation":
            object_type = params.get("object_type", "medium") if params else "medium"
            result = await telekinesis.object_manipulation(player_id, object_type, trait_level)
        elif ability_name == "levitate":
            result = await telekinesis.levitate(player_id, trait_level)
        else:
            raise HTTPException(400, f"Unknown telekinesis ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Pyrokinesis (Superpower Tool)
@router.post("/superpowers/pyrokinesis/use")
async def use_pyrokinesis_ability(
    ability_name: str,
    targets: Optional[List[str]] = None,
    params: Optional[Dict] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Pyrokinesis superpower abilities."""
    pyrokinesis = PyrokinesisAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "flame_burst":
            if not targets:
                raise HTTPException(400, "Targets required for flame_burst")
            result = await pyrokinesis.flame_burst(player_id, targets, trait_level)
        elif ability_name == "inferno_shield":
            result = await pyrokinesis.inferno_shield(player_id, trait_level)
        elif ability_name == "pyroclasm":
            position = params.get("position", {"x": 0, "y": 0, "z": 0}) if params else {"x": 0, "y": 0, "z": 0}
            result = await pyrokinesis.pyroclasm(player_id, position, trait_level)
        elif ability_name == "heat_generation":
            result = await pyrokinesis.heat_generation(player_id, trait_level)
        else:
            raise HTTPException(400, f"Unknown pyrokinesis ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Cryokinesis (Superpower Tool)
@router.post("/superpowers/cryokinesis/use")
async def use_cryokinesis_ability(
    ability_name: str,
    targets: Optional[List[str]] = None,
    target_id: Optional[str] = None,
    params: Optional[Dict] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Cryokinesis superpower abilities."""
    cryokinesis = CryokinesisAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "ice_blast":
            if not targets:
                raise HTTPException(400, "Targets required for ice_blast")
            result = await cryokinesis.ice_blast(player_id, targets, trait_level)
        elif ability_name == "frozen_armor":
            result = await cryokinesis.frozen_armor(player_id, trait_level)
        elif ability_name == "deep_freeze":
            if not target_id:
                raise HTTPException(400, "Target ID required for deep_freeze")
            result = await cryokinesis.deep_freeze(player_id, target_id, trait_level)
        elif ability_name == "ice_construct":
            construct_type = params.get("construct_type", "wall") if params else "wall"
            result = await cryokinesis.ice_construct(player_id, construct_type, trait_level)
        elif ability_name == "blizzard":
            position = params.get("position", {"x": 0, "y": 0, "z": 0}) if params else {"x": 0, "y": 0, "z": 0}
            result = await cryokinesis.blizzard(player_id, position, trait_level)
        else:
            raise HTTPException(400, f"Unknown cryokinesis ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Compassion (Good Trait)
@router.post("/good/compassion/use")
async def use_compassion_ability(
    target_id: str,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Compassion healing_touch ability."""
    compassion = CompassionAbility(db)
    player_id = str(current_player["id"])
    
    try:
        result = await compassion.healing_touch(player_id, target_id, trait_level)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Honesty (Good Trait)
@router.post("/good/honesty/use")
async def use_honesty_ability(
    target_id: str,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Honesty truth_reveal ability."""
    honesty = HonestyAbility(db)
    player_id = str(current_player["id"])
    
    try:
        result = await honesty.truth_reveal(player_id, target_id, trait_level)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Envy (Bad Trait)
@router.post("/bad/envy/use")
async def use_envy_ability(
    target_id: str,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Envy stat_drain ability."""
    envy = EnvyAbility(db)
    player_id = str(current_player["id"])
    
    try:
        result = await envy.stat_drain(player_id, target_id, trait_level)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Wrath (Bad Trait)
@router.post("/bad/wrath/use")
async def use_wrath_ability(
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Wrath berserker_rage ability."""
    wrath = WrathAbility(db)
    player_id = str(current_player["id"])
    
    try:
        result = await wrath.berserker_rage(player_id, trait_level)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Sloth (Bad Trait)
@router.post("/bad/sloth/use")
async def use_sloth_ability(
    ability_name: str,
    target_id: Optional[str] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Sloth abilities."""
    sloth = SlothAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "energy_siphon":
            if not target_id:
                raise HTTPException(400, "Target ID required for energy_siphon")
            result = await sloth.energy_siphon(player_id, target_id, trait_level)
        elif ability_name == "lazy_dodge":
            result = await sloth.lazy_dodge(player_id, trait_level)
        else:
            raise HTTPException(400, f"Unknown sloth ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Pride (Bad Trait)
@router.post("/bad/pride/use")
async def use_pride_ability(
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Pride superior_presence ability."""
    pride = PrideAbility(db)
    player_id = str(current_player["id"])
    
    try:
        result = await pride.superior_presence(player_id, trait_level)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Luck (Meta Trait)
@router.post("/meta/luck/use")
async def use_luck_ability(
    ability_name: str,
    params: Optional[Dict] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Luck abilities."""
    luck = LuckAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "fortunes_favor":
            result = await luck.fortunes_favor(player_id, trait_level)
        elif ability_name == "lucky_escape":
            damage = params.get("damage", 100) if params else 100
            result = await luck.lucky_escape(player_id, damage, trait_level)
        elif ability_name == "treasure_sense":
            result = await luck.treasure_sense(player_id, trait_level)
        else:
            raise HTTPException(400, f"Unknown luck ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Resilience (Meta Trait)
@router.post("/meta/resilience/use")
async def use_resilience_ability(
    ability_name: str,
    params: Optional[Dict] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Resilience abilities."""
    resilience = ResilienceAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "unbreakable_will":
            result = await resilience.unbreakable_will(player_id, trait_level)
        elif ability_name == "damage_threshold":
            incoming_damage = params.get("damage", 100) if params else 100
            result = await resilience.damage_threshold(player_id, incoming_damage, trait_level)
        else:
            raise HTTPException(400, f"Unknown resilience ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Wisdom (Meta Trait)
@router.post("/meta/wisdom/use")
async def use_wisdom_ability(
    ability_name: str,
    params: Optional[Dict] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Wisdom abilities."""
    wisdom = WisdomAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "sage_insight":
            situation = params.get("situation", "combat") if params else "combat"
            result = await wisdom.sage_insight(player_id, situation, trait_level)
        elif ability_name == "learning_acceleration":
            skill_type = params.get("skill_type", "general") if params else "general"
            result = await wisdom.learning_acceleration(player_id, skill_type, trait_level)
        else:
            raise HTTPException(400, f"Unknown wisdom ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

# Adaptability (Meta Trait)
@router.post("/meta/adaptability/use")
async def use_adaptability_ability(
    ability_name: str,
    params: Optional[Dict] = None,
    target_id: Optional[str] = None,
    trait_level: int = 1,
    current_player: dict = Depends(get_current_player),
    db = Depends(get_database)
):
    """Use Adaptability abilities."""
    adaptability = AdaptabilityAbility(db)
    player_id = str(current_player["id"])
    
    try:
        if ability_name == "quick_adaptation":
            situation = params.get("situation", "combat") if params else "combat"
            result = await adaptability.quick_adaptation(player_id, situation, trait_level)
        elif ability_name == "environment_mastery":
            environment = params.get("environment", "normal") if params else "normal"
            result = await adaptability.environment_mastery(player_id, environment, trait_level)
        elif ability_name == "copy_ability":
            if not target_id:
                raise HTTPException(400, "Target ID required for copy_ability")
            ability_to_copy = params.get("ability_name", "strength") if params else "strength"
            result = await adaptability.copy_ability(player_id, target_id, ability_to_copy, trait_level)
        else:
            raise HTTPException(400, f"Unknown adaptability ability: {ability_name}")
        
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

