from fastapi import APIRouter, Depends, HTTPException
from backend.api.deps import get_current_user
from backend.core.database import get_database as get_db
from ....services.upgrades import RobotUpgrader
from ..upgrades.schemas import RobotUpgradeRequest, UpgradeResponse

router = APIRouter(prefix="/robots", tags=["robot-upgrades"])


@router.post("/upgrade", response_model=UpgradeResponse)
async def upgrade_specific_robot(
    request: RobotUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Dedicated endpoint for robot upgrades
    
    Available robots:
    - scout: Reconnaissance specialist (Unlock: Level 1)
    - combat: Battle companion (Unlock: Level 10)
    - hacker: Digital warfare (Unlock: Level 15)
    - medic: Healing and support (Unlock: Level 20)
    - trader: Resource management (Unlock: Level 25)
    - guardian: Heavy defense (Unlock: Level 35)
    """
    try:
        upgrader = RobotUpgrader(db)
        result = await upgrader.upgrade_robot(current_user['player_id'], request.robot_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.get("/available")
async def get_available_robots(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get list of available robots with unlock status
    """
    player = await db.players.find_one({'player_id': current_user['player_id']})
    player_level = player.get('level', 1) if player else 1
    
    robots = [
        {'id': 'scout', 'name': 'Scout Bot', 'description': 'Reconnaissance and exploration specialist', 'unlock_level': 1, 'unlocked': player_level >= 1},
        {'id': 'combat', 'name': 'Combat Droid', 'description': 'Battle companion with advanced weapons', 'unlock_level': 10, 'unlocked': player_level >= 10},
        {'id': 'hacker', 'name': 'Hacker Bot', 'description': 'Digital warfare and system infiltration', 'unlock_level': 15, 'unlocked': player_level >= 15},
        {'id': 'medic', 'name': 'Medic Bot', 'description': 'Healing and support functions', 'unlock_level': 20, 'unlocked': player_level >= 20},
        {'id': 'trader', 'name': 'Trader Bot', 'description': 'Automated trading and resource management', 'unlock_level': 25, 'unlocked': player_level >= 25},
        {'id': 'guardian', 'name': 'Guardian Mech', 'description': 'Heavy defense and protection systems', 'unlock_level': 35, 'unlocked': player_level >= 35}
    ]
    return {'robots': robots, 'player_level': player_level}
