"""Player profile routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import get_database
from backend.api.deps import get_current_user
from backend.api.v1.player.profile.schemas import (
    PlayerProfileResponse,
    ProfileUpdateRequest,
    StatsResponse
)
from backend.services.player.stats_calculator import StatsCalculator
from bson import ObjectId

router = APIRouter()


@router.get('/me', response_model=PlayerProfileResponse)
async def get_my_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current player's profile."""
    player = await db.players.find_one({'_id': ObjectId(current_user['_id'])})

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Player profile not found'
        )

    player['_id'] = str(player['_id'])
    return player


@router.get('/{player_id}', response_model=PlayerProfileResponse)
async def get_player_profile(
    player_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get another player's profile (respects visibility settings)."""
    player = await db.players.find_one({'_id': ObjectId(player_id)})

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Player not found'
        )

    # Apply visibility filters (if not viewing own profile)
    if str(player['_id']) != current_user['_id']:
        visibility = player.get('visibility', {})
        privacy_tier = visibility.get('privacy_tier', 'public')

        if privacy_tier != 'public':
            # Filter sensitive information based on privacy tier
            if not visibility.get('cash', True):
                player['currencies'] = {'credits': 'hidden'}

            if not visibility.get('karma_score', True):
                player['karma_points'] = None

            if not visibility.get('traits_public', []):
                player['traits'] = {}
            else:
                public_traits = visibility.get('traits_public', [])
                player['traits'] = {
                    k: v for k, v in player.get('traits', {}).items()
                    if k in public_traits
                }

    player['_id'] = str(player['_id'])
    return player


@router.put('/me', response_model=PlayerProfileResponse)
async def update_my_profile(
    profile_update: ProfileUpdateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Update current player's profile."""
    update_data = profile_update.dict(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No fields to update'
        )

    # Prevent updating sensitive fields
    forbidden_fields = {'_id', 'username', 'email',
        'password_hash', 'level', 'xp', 'karma_points'}
    if any(field in update_data for field in forbidden_fields):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot update protected fields'
        )

    result = await db.players.update_one(
        {'_id': ObjectId(current_user['_id'])},
        {'$set': update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail='No changes made'
        )

    # Return updated profile
    updated_player = await db.players.find_one({'_id': ObjectId(current_user['_id'])})
    updated_player['_id'] = str(updated_player['_id'])

    return updated_player


@router.get('/me/stats', response_model=StatsResponse)
async def get_my_stats(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current player's calculated stats."""
    player = await db.players.find_one({'_id': ObjectId(current_user['_id'])})

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Player not found'
        )

    # Calculate all stats
    combat_stats = StatsCalculator.calculate_combat_stats(player)
    derived_traits = StatsCalculator.calculate_derived_traits(player)
    level_progress = StatsCalculator.calculate_level_progress(
        player.get('xp', 0),
        player.get('level', 1)
    )

    return {
        'player_id': str(player['_id']),
        'username': player['username'],
        'level': player['level'],
        'combat_stats': combat_stats,
        'derived_traits': derived_traits,
        'level_progress': level_progress
    }
