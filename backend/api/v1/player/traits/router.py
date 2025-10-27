from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict

from .schemas import TraitAllocateRequest, TraitsResponse, TraitDetailsResponse
from backend.core.database import get_database
from backend.api.v1.auth.router import get_current_user_dep
from backend.models.player.player import Player
from backend.services.player.traits import TraitsService

router = APIRouter(prefix="/traits", tags=["traits"])

@router.get("/", response_model=TraitsResponse)
async def get_all_traits(
    current_user: Player = Depends(get_current_user_dep)
):
    """Get all player traits (60 base + 20 meta)."""
    return TraitsResponse(
        traits=current_user.traits.model_dump(),
        meta_traits=current_user.meta_traits.model_dump(),
        total_traits=80
    )

@router.get("/base", response_model=Dict[str, float])
async def get_base_traits(
    current_user: Player = Depends(get_current_user_dep)
):
    """Get only 60 base traits."""
    return current_user.traits.model_dump()

@router.get("/meta", response_model=Dict[str, float])
async def get_meta_traits(
    current_user: Player = Depends(get_current_user_dep)
):
    """Get only 20 meta traits."""
    return current_user.meta_traits.model_dump()

@router.get("/top")
async def get_top_traits(
    current_user: Player = Depends(get_current_user_dep),
    limit: int = 10
):
    """Get player's top traits."""
    traits_service = TraitsService()
    return traits_service.get_top_traits(current_user, limit)

@router.get("/bottom")
async def get_bottom_traits(
    current_user: Player = Depends(get_current_user_dep),
    limit: int = 10
):
    """Get player's bottom traits."""
    traits_service = TraitsService()
    return traits_service.get_bottom_traits(current_user, limit)

@router.get("/{trait_name}", response_model=TraitDetailsResponse)
async def get_trait_details(
    trait_name: str,
    current_user: Player = Depends(get_current_user_dep)
):
    """Get details about a specific trait."""
    traits_service = TraitsService()
    return traits_service.get_trait_details(current_user, trait_name)

@router.put("/allocate")
async def allocate_trait_points(
    request: TraitAllocateRequest,
    current_user: Player = Depends(get_current_user_dep),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Allocate trait points (for future skill tree system)."""
    traits_service = TraitsService()
    return await traits_service.allocate_points(
        db, current_user.id, request.trait_name, request.points
    )