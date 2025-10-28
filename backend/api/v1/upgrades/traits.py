from fastapi import APIRouter, Depends, HTTPException
from backend.api.deps import get_current_user
from backend.core.database import get_database as get_db
from ....services.upgrades import TraitUpgrader
from ..upgrades.schemas import TraitUpgradeRequest, UpgradeResponse

router = APIRouter(prefix="/traits", tags=["trait-upgrades"])


@router.post("/upgrade", response_model=UpgradeResponse)
async def upgrade_specific_trait(
    request: TraitUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Dedicated endpoint for trait upgrades
    
    Available traits:
    - strength: Physical power
    - hacking: Digital skills
    - charisma: Social influence
    - stealth: Covert operations
    - intelligence: Problem solving
    - luck: Random outcomes
    """
    try:
        upgrader = TraitUpgrader(db)
        result = await upgrader.upgrade_trait(current_user['player_id'], request.trait_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.get("/available")
async def get_available_traits(
    current_user: dict = Depends(get_current_user)
):
    """
    Get list of available traits and their descriptions
    """
    traits = [
        {'id': 'strength', 'name': 'Strength', 'description': 'Physical power and combat effectiveness'},
        {'id': 'hacking', 'name': 'Hacking', 'description': 'Digital infiltration and system manipulation'},
        {'id': 'charisma', 'name': 'Charisma', 'description': 'Social influence and persuasion'},
        {'id': 'stealth', 'name': 'Stealth', 'description': 'Covert operations and evasion'},
        {'id': 'intelligence', 'name': 'Intelligence', 'description': 'Problem solving and strategy'},
        {'id': 'luck', 'name': 'Luck', 'description': 'Random event outcomes and critical chances'}
    ]
    return {'traits': traits}
