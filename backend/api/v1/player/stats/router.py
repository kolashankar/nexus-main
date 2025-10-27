"""Player stats routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from backend.core.database import get_database
from backend.api.deps import get_current_user
from backend.services.player.stats_calculator import StatsCalculator
from backend.utils.trait_calculator import TraitCalculator
from backend.api.v1.player.profile.schemas import StatsResponse

router = APIRouter()


@router.get('/me', response_model=StatsResponse)
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


@router.get('/me/traits/analysis')
async def get_trait_analysis(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get detailed trait analysis."""
    player = await db.players.find_one({'_id': ObjectId(current_user['_id'])})

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Player not found'
        )

    traits = player.get('traits', {})

    # Calculate analysis
    moral_alignment, alignment_score = TraitCalculator.calculate_moral_alignment(
        traits)
    trait_balance = TraitCalculator.calculate_trait_balance(traits)
    dominant_traits = TraitCalculator.get_dominant_traits(traits, 5)
    weakest_traits = TraitCalculator.get_weakest_traits(traits, 5)
    suggestions = TraitCalculator.suggest_trait_improvements(traits)
    synergies = TraitCalculator.calculate_synergies(traits)

    return {
        'moral_alignment': {
            'class': moral_alignment,
            'score': alignment_score
        },
        'balance': trait_balance,
        'dominant_traits': [
            {'trait': t[0], 'value': t[1]} for t in dominant_traits
        ],
        'weakest_traits': [
            {'trait': t[0], 'value': t[1]} for t in weakest_traits
        ],
        'improvement_suggestions': suggestions,
        'active_synergies': synergies
    }


@router.get('/me/traits/category/{category}')
async def get_traits_by_category(
    category: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get traits by category (virtues, vices, skills).
    
    Args:
        category: Category name ('virtues', 'vices', 'skills')
    """
    player = await db.players.find_one({'_id': ObjectId(current_user['_id'])})

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Player not found'
        )

    traits = player.get('traits', {})

    # Get traits by category
    if category == 'virtues':
        trait_list = TraitCalculator.VIRTUES
    elif category == 'vices':
        trait_list = TraitCalculator.VICES
    elif category == 'skills':
        trait_list = TraitCalculator.SKILLS
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid category. Use: virtues, vices, or skills'
        )

    category_traits = {
        trait: traits.get(trait, 50)
        for trait in trait_list
    }

    avg_value = sum(category_traits.values()) / len(category_traits)

    return {
        'category': category,
        'traits': category_traits,
        'average': round(avg_value, 2),
        'count': len(category_traits)
    }
