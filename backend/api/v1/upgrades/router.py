from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from backend.api.deps import get_current_user
from backend.core.database import get_database as get_db
from ....services.upgrades import (
    TraitUpgrader, RobotUpgrader, OrnamentUpgrader, ChipUpgrader
)
from .schemas import (
    TraitUpgradeRequest, RobotUpgradeRequest, OrnamentUpgradeRequest,
    ChipUpgradeRequest, UpgradeResponse, UpgradeHistoryResponse, UpgradeStatsResponse
)

router = APIRouter(prefix="/upgrades", tags=["upgrades"])


@router.post("/traits", response_model=UpgradeResponse)
async def upgrade_trait(
    request: TraitUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Upgrade a player trait
    
    - **trait_id**: ID of the trait (strength, hacking, charisma, stealth, intelligence, luck)
    """
    try:
        upgrader = TraitUpgrader(db)
        result = await upgrader.upgrade_trait(current_user['player_id'], request.trait_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.post("/robots", response_model=UpgradeResponse)
async def upgrade_robot(
    request: RobotUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Upgrade a robot companion
    
    - **robot_id**: ID of the robot (scout, combat, hacker, medic, trader, guardian)
    """
    try:
        upgrader = RobotUpgrader(db)
        result = await upgrader.upgrade_robot(current_user['player_id'], request.robot_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.post("/ornaments", response_model=UpgradeResponse)
async def upgrade_ornament(
    request: OrnamentUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Upgrade an ornament/cosmetic item
    
    - **ornament_id**: ID of the ornament (avatar_frame, title_banner, emote_pack, victory_effect, nameplate, aura)
    """
    try:
        upgrader = OrnamentUpgrader(db)
        result = await upgrader.upgrade_ornament(current_user['player_id'], request.ornament_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.post("/chips", response_model=UpgradeResponse)
async def upgrade_chip(
    request: ChipUpgradeRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Upgrade a cyber chip/neural augmentation
    
    - **chip_id**: ID of the chip (neural_enhancer, combat_chip, stealth_module, hacking_chip, resource_optimizer, quantum_processor)
    """
    try:
        upgrader = ChipUpgrader(db)
        result = await upgrader.upgrade_chip(current_user['player_id'], request.chip_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")


@router.get("/history", response_model=List[UpgradeHistoryResponse])
async def get_upgrade_history(
    upgrade_type: Optional[str] = Query(None, description="Filter by upgrade type"),
    limit: int = Query(10, ge=1, le=100, description="Number of records to return"),
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get player's upgrade history
    
    - **upgrade_type**: Optional filter (trait, robot, ornament, chip)
    - **limit**: Maximum number of records to return (1-100)
    """
    try:
        query = {'player_id': current_user['player_id']}
        if upgrade_type:
            query['upgrade_type'] = upgrade_type
        
        history = await db.upgrade_history.find(query).sort('timestamp', -1).limit(limit).to_list(length=limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


@router.get("/stats", response_model=UpgradeStatsResponse)
async def get_upgrade_stats(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get player's upgrade statistics
    
    Returns comprehensive statistics about player's upgrades
    """
    try:
        player_id = current_user['player_id']
        
        # Get total upgrades
        total_upgrades = await db.upgrade_history.count_documents({'player_id': player_id})
        
        # Get upgrades by type
        pipeline = [
            {'$match': {'player_id': player_id}},
            {'$group': {
                '_id': '$upgrade_type',
                'count': {'$sum': 1}
            }}
        ]
        upgrades_by_type_cursor = db.upgrade_history.aggregate(pipeline)
        upgrades_by_type = {doc['_id']: doc['count'] async for doc in upgrades_by_type_cursor}
        
        # Calculate total spent
        spent_pipeline = [
            {'$match': {'player_id': player_id}},
            {'$group': {
                '_id': None,
                'total_credits': {'$sum': '$cost.credits'},
                'total_karma_tokens': {'$sum': '$cost.karma_tokens'},
                'total_dark_matter': {'$sum': '$cost.dark_matter'}
            }}
        ]
        spent_cursor = db.upgrade_history.aggregate(spent_pipeline)
        spent_doc = await spent_cursor.to_list(length=1)
        total_spent = {
            'credits': spent_doc[0]['total_credits'] if spent_doc else 0,
            'karma_tokens': spent_doc[0]['total_karma_tokens'] if spent_doc else 0,
            'dark_matter': spent_doc[0]['total_dark_matter'] if spent_doc else 0
        }
        
        # Get highest level items
        player = await db.players.find_one({'player_id': player_id})
        highest_level_items = {}
        
        if player:
            # Check traits
            for trait, level in player.get('traits', {}).items():
                if level > 50:  # Only show high-level items
                    highest_level_items[trait] = {'level': level, 'type': 'trait'}
            
            # Check robots
            for robot_id, robot_data in player.get('robots', {}).items():
                level = robot_data.get('level', 0)
                if level > 50:
                    highest_level_items[robot_id] = {'level': level, 'type': 'robot'}
        
        return {
            'total_upgrades': total_upgrades,
            'upgrades_by_type': upgrades_by_type,
            'total_spent': total_spent,
            'highest_level_items': highest_level_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")
