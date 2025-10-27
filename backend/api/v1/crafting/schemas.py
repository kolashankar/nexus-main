from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class CraftItemRequest(BaseModel):
    recipe_id: str = Field(..., description="Recipe ID")
    quantity: int = Field(default=1, ge=1, le=100,
                          description="Quantity to craft")


class MaterialRequirement(BaseModel):
    material_id: str
    material_name: str
    required: int
    owned: int


class RecipeBase(BaseModel):
    id: str
    name: str
    description: str
    category: str
    level_required: int
    crafting_time: int  # seconds
    xp_reward: int


class RecipeListItem(RecipeBase):
    materials_required: List[Dict[str, Any]]
    result_item: Dict[str, Any]
    unlocked: bool


class RecipeDetailResponse(RecipeBase):
    materials_required: List[MaterialRequirement]
    result_item: Dict[str, Any]
    success_rate: float
    bonus_effects: Optional[List[str]]
    unlocked: bool
    can_craft: bool


class RecipeListResponse(BaseModel):
    recipes: List[RecipeListItem]
    total: int


class CraftItemResponse(BaseModel):
    success: bool
    item_id: Optional[str]
    item_name: str
    quantity_crafted: int
    xp_gained: int
    materials_consumed: List[Dict[str, Any]]
    bonus_received: Optional[str]


class CraftingMaterial(BaseModel):
    material_id: str
    name: str
    quantity: int
    rarity: str
    description: str


class CraftingMaterialsResponse(BaseModel):
    materials: List[CraftingMaterial]


class CraftingHistoryItem(BaseModel):
    timestamp: datetime
    recipe_name: str
    item_crafted: str
    quantity: int
    success: bool
    xp_gained: int
