from fastapi import APIRouter, Depends, HTTPException
from backend.api.deps import get_current_user
from backend.core.database import get_database as get_db
from ....services.upgrades import OrnamentUpgrader
from ..upgrades.schemas import OrnamentUpgradeRequest, UpgradeResponse

router = APIRouter(prefix="/ornaments", tags=["ornament-upgrades"])


@router.post("/upgrade", response_model=UpgradeResponse)
async def upgrade_specific_ornament(
    request: OrnamentUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Dedicated endpoint for ornament upgrades
    
    Available ornaments:
    - avatar_frame: Decorative profile border (Unlock: Level 5)
    - title_banner: Custom title display (Unlock: Level 10)
    - emote_pack: Exclusive animations (Unlock: Level 15)
    - victory_effect: Special victory effects (Unlock: Level 20)
    - nameplate: Personalized nameplate (Unlock: Level 25)
    - aura: Character glow effect (Unlock: Level 30)
    """
    try:
        upgrader = OrnamentUpgrader(db)
        result = await upgrader.upgrade_ornament(current_user['player_id'], request.ornament_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.get("/available")
async def get_available_ornaments(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get list of available ornaments with unlock status
    """
    player = await db.players.find_one({'player_id': current_user['player_id']})
    player_level = player.get('level', 1) if player else 1
    
    ornaments = [
        {'id': 'avatar_frame', 'name': 'Avatar Frame', 'description': 'Decorative border for profile picture', 'bonus': 'Prestige +10', 'unlock_level': 5, 'unlocked': player_level >= 5},
        {'id': 'title_banner', 'name': 'Title Banner', 'description': 'Custom title display banner', 'bonus': 'Reputation +5', 'unlock_level': 10, 'unlocked': player_level >= 10},
        {'id': 'emote_pack', 'name': 'Emote Pack', 'description': 'Exclusive emote animations', 'bonus': 'Social +15', 'unlock_level': 15, 'unlocked': player_level >= 15},
        {'id': 'victory_effect', 'name': 'Victory Effect', 'description': 'Special effects for victories', 'bonus': 'Morale +20', 'unlock_level': 20, 'unlocked': player_level >= 20},
        {'id': 'nameplate', 'name': 'Custom Nameplate', 'description': 'Personalized name display', 'bonus': 'Recognition +12', 'unlock_level': 25, 'unlocked': player_level >= 25},
        {'id': 'aura', 'name': 'Character Aura', 'description': 'Glowing aura effect around character', 'bonus': 'Intimidation +25', 'unlock_level': 30, 'unlocked': player_level >= 30}
    ]
    return {'ornaments': ornaments, 'player_level': player_level}
