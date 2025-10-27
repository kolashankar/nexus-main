"""World State API Routes"""

from fastapi import APIRouter, Depends, HTTPException, status

from ....core.database import get_database
from ....services.world.state_manager import WorldStateManager
from ....services.world.collective_karma import CollectiveKarmaTracker
from .schemas import (
    WorldStateResponse,
    KarmaStatsResponse,
    TopPlayersResponse
)

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/current", response_model=WorldStateResponse)
async def get_world_state(
    db = Depends(get_database)
):
    """
    Get current world state
    
    Returns comprehensive information about the current state of the game world,
    including karma levels, player activity, conflicts, and economy.
    """
    world_manager = WorldStateManager(db)
    state = await world_manager.get_world_state()

    return WorldStateResponse.from_model(state)


@router.post("/sync")
async def sync_world_state(
    db = Depends(get_database)
):
    """
    Trigger full world state synchronization
    
    This performs an expensive full sync of all world statistics.
    Use sparingly - typically called by background tasks.
    """
    world_manager = WorldStateManager(db)

    try:
        state = await world_manager.sync_world_state()
        logger.info("World state synchronized successfully")

        return {
            "success": True,
            "message": "World state synchronized",
            "state": WorldStateResponse.from_model(state)
        }
    except Exception as e:
        logger.error(f"Error syncing world state: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync world state: {str(e)}"
        )


@router.get("/karma", response_model=KarmaStatsResponse)
async def get_karma_statistics(
    db = Depends(get_database)
):
    """
    Get collective karma statistics
    
    Returns detailed karma statistics including distribution, trends, and top players.
    """
    karma_tracker = CollectiveKarmaTracker(db)

    try:
        collective = await karma_tracker.get_collective_karma()
        average = await karma_tracker.get_average_karma()
        trend = await karma_tracker.get_karma_trend(hours=24)
        distribution = await karma_tracker.get_karma_distribution()
        action_ratio = await karma_tracker.get_action_ratio_24h()

        return KarmaStatsResponse(
            collective_karma=collective,
            average_karma=average,
            karma_trend=trend,
            distribution=distribution,
            action_ratio=action_ratio
        )
    except Exception as e:
        logger.error(f"Error getting karma stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get karma statistics: {str(e)}"
        )


@router.get("/karma/top", response_model=TopPlayersResponse)
async def get_top_karma_players(
    limit: int = 10,
    db = Depends(get_database)
):
    """
    Get players with highest karma
    """
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )

    karma_tracker = CollectiveKarmaTracker(db)
    players = await karma_tracker.get_top_karma_players(limit=limit)

    return TopPlayersResponse(
        players=players,
        total=len(players)
    )


@router.get("/karma/bottom", response_model=TopPlayersResponse)
async def get_bottom_karma_players(
    limit: int = 10,
    db = Depends(get_database)
):
    """
    Get players with lowest karma
    """
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )

    karma_tracker = CollectiveKarmaTracker(db)
    players = await karma_tracker.get_bottom_karma_players(limit=limit)

    return TopPlayersResponse(
        players=players,
        total=len(players)
    )
