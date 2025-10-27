"""Territories API Routes"""

from fastapi import APIRouter, Depends, HTTPException, status

from ....core.database import get_database
from ....services.world.territory_manager import TerritoryManager
from .schemas import TerritoryResponse, TerritoryListResponse

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/all", response_model=TerritoryListResponse)
async def get_all_territories(
    db = Depends(get_database)
):
    """
    Get all territories in the game world
    
    Returns information about all 20 territories including control status,
    population, karma levels, and active events.
    """
    territory_manager = TerritoryManager(db)
    territories = await territory_manager.get_all_territories()

    return TerritoryListResponse(
        territories=[TerritoryResponse.from_model(t) for t in territories],
        total=len(territories)
    )


@router.get("/contested", response_model=TerritoryListResponse)
async def get_contested_territories(
    db = Depends(get_database)
):
    """
    Get all contested territories
    
    Returns territories that are currently being fought over by guilds.
    """
    territory_manager = TerritoryManager(db)
    territories = await territory_manager.get_contested_territories()

    return TerritoryListResponse(
        territories=[TerritoryResponse.from_model(t) for t in territories],
        total=len(territories)
    )


@router.get("/guild/{guild_id}", response_model=TerritoryListResponse)
async def get_guild_territories(
    guild_id: str,
    db = Depends(get_database)
):
    """
    Get territories controlled by a specific guild
    
    Returns all territories currently under control of the specified guild.
    """
    territory_manager = TerritoryManager(db)
    territories = await territory_manager.get_guild_territories(guild_id)

    return TerritoryListResponse(
        territories=[TerritoryResponse.from_model(t) for t in territories],
        total=len(territories)
    )


@router.get("/{territory_id}", response_model=TerritoryResponse)
async def get_territory(
    territory_id: int,
    db = Depends(get_database)
):
    """
    Get detailed information about a specific territory
    """
    if territory_id < 1 or territory_id > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Territory ID must be between 1 and 20"
        )

    territory_manager = TerritoryManager(db)
    territory = await territory_manager.get_territory(territory_id)

    if not territory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Territory {territory_id} not found"
        )

    return TerritoryResponse.from_model(territory)


@router.post("/initialize")
async def initialize_territories(
    db = Depends(get_database)
):
    """
    Initialize all 20 territories if they don't exist
    
    This endpoint creates all territories in the database if they haven't been
    created yet. Usually called once during initial setup.
    """
    territory_manager = TerritoryManager(db)

    try:
        created = await territory_manager.initialize_territories()

        return {
            "success": True,
            "message": f"Initialized {created} new territories",
            "total_territories": 20
        }
    except Exception as e:
        logger.error(f"Error initializing territories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize territories: {str(e)}"
        )


@router.post("/{territory_id}/sync-population")
async def sync_territory_population(
    territory_id: int,
    db = Depends(get_database)
):
    """
    Synchronize territory population from player data
    
    Recalculates the number of players in the territory from the database.
    """
    if territory_id < 1 or territory_id > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Territory ID must be between 1 and 20"
        )

    territory_manager = TerritoryManager(db)

    try:
        population = await territory_manager.sync_territory_population(territory_id)
        karma = await territory_manager.calculate_local_karma(territory_id)

        return {
            "success": True,
            "territory_id": territory_id,
            "population": population,
            "local_karma": karma
        }
    except Exception as e:
        logger.error(f"Error syncing territory {territory_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync territory: {str(e)}"
        )
