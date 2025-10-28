from fastapi import APIRouter, Depends, HTTPException
from ....core.deps import get_current_user, get_db
from ....services.upgrades import ChipUpgrader
from ..upgrades.schemas import ChipUpgradeRequest, UpgradeResponse

router = APIRouter(prefix="/chips", tags=["chip-upgrades"])


@router.post("/upgrade", response_model=UpgradeResponse)
async def upgrade_specific_chip(
    request: ChipUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Dedicated endpoint for chip upgrades
    
    Available chips:
    - neural_enhancer: Mental processing boost (Unlock: Level 5)
    - combat_chip: Combat reflexes and damage (Unlock: Level 10)
    - stealth_module: Stealth and evasion (Unlock: Level 15)
    - hacking_chip: Advanced hacking protocols (Unlock: Level 20)
    - resource_optimizer: Resource gathering boost (Unlock: Level 25)
    - quantum_processor: Ultimate computational power (Unlock: Level 40)
    """
    try:
        upgrader = ChipUpgrader(db)
        result = await upgrader.upgrade_chip(current_user['player_id'], request.chip_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.get("/available")
async def get_available_chips(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get list of available chips with unlock status
    """
    player = await db.players.find_one({'player_id': current_user['player_id']})
    player_level = player.get('level', 1) if player else 1
    
    chips = [
        {'id': 'neural_enhancer', 'name': 'Neural Enhancer', 'description': 'Boosts mental processing speed', 'effect': '+5% XP gain per level', 'unlock_level': 5, 'unlocked': player_level >= 5},
        {'id': 'combat_chip', 'name': 'Combat Chip', 'description': 'Enhances combat reflexes and damage', 'effect': '+3% damage per level', 'unlock_level': 10, 'unlocked': player_level >= 10},
        {'id': 'stealth_module', 'name': 'Stealth Module', 'description': 'Improves stealth and evasion', 'effect': '+4% evasion per level', 'unlock_level': 15, 'unlocked': player_level >= 15},
        {'id': 'hacking_chip', 'name': 'Hacking Chip', 'description': 'Advanced hacking protocols', 'effect': '+6% hack success rate per level', 'unlock_level': 20, 'unlocked': player_level >= 20},
        {'id': 'resource_optimizer', 'name': 'Resource Optimizer', 'description': 'Optimizes resource gathering', 'effect': '+2% credits gain per level', 'unlock_level': 25, 'unlocked': player_level >= 25},
        {'id': 'quantum_processor', 'name': 'Quantum Processor', 'description': 'Ultimate computational power', 'effect': '+10% all stats per level', 'unlock_level': 40, 'unlocked': player_level >= 40}
    ]
    return {'chips': chips, 'player_level': player_level}
