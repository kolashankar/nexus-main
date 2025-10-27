"""Action cooldown routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import get_database
from backend.api.deps import get_current_user
from backend.services.actions.cooldown_manager import CooldownManager
from backend.models.actions.cooldown import CooldownStatus

router = APIRouter()


@router.get('/{action_type}', response_model=CooldownStatus)
async def check_action_cooldown(
    action_type: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Check cooldown status for an action.
    
    Args:
        action_type: Type of action to check
        
    Returns:
        Cooldown status information
    """
    cooldown_manager = CooldownManager(db)

    cooldown_info = await cooldown_manager.check_cooldown(
        current_user['_id'],
        action_type
    )

    return cooldown_info


@router.get('/', response_model=Dict[str, Dict[str, Any]])
async def get_all_cooldowns(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get all active cooldowns for current player.
    
    Returns:
        Dictionary of action types to cooldown information
    """
    cooldown_manager = CooldownManager(db)

    cooldowns = await cooldown_manager.get_all_cooldowns(current_user['_id'])

    return cooldowns


@router.delete('/{action_type}')
async def clear_cooldown(
    action_type: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Clear a cooldown (admin or special item use).
    
    Args:
        action_type: Type of action cooldown to clear
        
    Returns:
        Success status
    """
    # Note: In production, add admin check or item consumption check
    cooldown_manager = CooldownManager(db)

    cleared = await cooldown_manager.clear_cooldown(
        current_user['_id'],
        action_type
    )

    if not cleared:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No active cooldown found for action: {action_type}'
        )

    return {'success': True, 'message': f'Cooldown cleared for {action_type}'}


@router.post('/{action_type}/reduce')
async def reduce_cooldown(
    action_type: str,
    reduction_seconds: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Reduce cooldown time (power or item effect).
    
    Args:
        action_type: Type of action cooldown to reduce
        reduction_seconds: Seconds to reduce from cooldown
        
    Returns:
        Updated cooldown information
    """
    if reduction_seconds <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Reduction must be positive'
        )

    # Note: In production, verify item/power usage
    cooldown_manager = CooldownManager(db)

    result = await cooldown_manager.reduce_cooldown(
        current_user['_id'],
        action_type,
        reduction_seconds
    )

    return result
