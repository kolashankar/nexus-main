from fastapi import APIRouter, Depends, HTTPException, status
from ....core.security import get_current_user
from ....services.crafting.crafter import CraftingService
from ....services.player.profile import PlayerService
from .schemas import (
    CraftItemRequest,
    CraftItemResponse,
    RecipeListResponse,
    RecipeDetailResponse,
    CraftingMaterialsResponse
)

router = APIRouter(prefix="/crafting", tags=["crafting"])


@router.get("/recipes", response_model=RecipeListResponse)
async def get_all_recipes(
    category: str = None,
    min_level: int = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all available crafting recipes."""
    crafting_service = CraftingService()
    recipes = await crafting_service.get_recipes(
        player_level=current_user.get("level", 1),
        category=category,
        min_level=min_level
    )
    return {"recipes": recipes, "total": len(recipes)}


@router.get("/recipes/{recipe_id}", response_model=RecipeDetailResponse)
async def get_recipe_details(
    recipe_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed information about a specific recipe."""
    crafting_service = CraftingService()
    recipe = await crafting_service.get_recipe_by_id(recipe_id)

    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )

    return recipe


@router.get("/materials", response_model=CraftingMaterialsResponse)
async def get_player_materials(
    current_user: dict = Depends(get_current_user)
):
    """Get player's available crafting materials."""
    player_service = PlayerService()
    materials = await player_service.get_crafting_materials(current_user["_id"])
    return {"materials": materials}


@router.post("/craft", response_model=CraftItemResponse)
async def craft_item(
    request: CraftItemRequest,
    current_user: dict = Depends(get_current_user)
):
    """Craft an item using a recipe."""
    crafting_service = CraftingService()

    # Check if player has required materials
    can_craft = await crafting_service.can_craft(
        current_user["_id"],
        request.recipe_id,
        request.quantity
    )

    if not can_craft:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient materials or level requirement not met"
        )

    # Craft the item
    result = await crafting_service.craft_item(
        current_user["_id"],
        request.recipe_id,
        request.quantity
    )

    return result


@router.post("/dismantle/{item_id}")
async def dismantle_item(
    item_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Dismantle an item to get materials back."""
    crafting_service = CraftingService()

    result = await crafting_service.dismantle_item(
        current_user["_id"],
        item_id
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or cannot be dismantled"
        )

    return result


@router.get("/history")
async def get_crafting_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Get player's crafting history."""
    crafting_service = CraftingService()
    history = await crafting_service.get_crafting_history(
        current_user["_id"],
        limit=limit
    )
    return {"history": history}
