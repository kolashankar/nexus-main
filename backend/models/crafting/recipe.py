from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class MaterialRequirement(BaseModel):
    """Material requirement for a recipe."""
    material_id: str
    name: str
    quantity: int
    rarity: Optional[str] = "common"


class ResultItem(BaseModel):
    """Item produced by crafting."""
    name: str
    type: str
    rarity: str = "common"
    stats: Optional[Dict] = None


class Recipe(BaseModel):
    """Crafting recipe model."""
    id: str = Field(..., description="Unique recipe ID")
    name: str = Field(..., description="Recipe name")
    description: str = Field(..., description="Recipe description")
    category: str = Field(..., description="Recipe category")

    level_required: int = Field(
        default=1, ge=1, description="Level required to craft")
    crafting_time: int = Field(
        default=60, ge=1, description="Crafting time in seconds")
    xp_reward: int = Field(
        default=10, ge=0, description="XP reward for crafting")
    success_rate: float = Field(
        default=0.95, ge=0.0, le=1.0, description="Base success rate")

    materials_required: List[MaterialRequirement] = Field(
        default_factory=list,
        description="Materials required for crafting"
    )
    result_item: ResultItem = Field(..., description="Item produced")

    bonus_effects: Optional[List[str]] = Field(
        default=None,
        description="Possible bonus effects on successful craft"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "basic_robot_parts",
                "name": "Basic Robot Parts",
                "description": "Essential components for robot construction",
                "category": "robot_parts",
                "level_required": 1,
                "crafting_time": 60,
                "xp_reward": 25,
                "success_rate": 0.95,
                "materials_required": [
                    {
                        "material_id": "scrap_metal",
                        "name": "Scrap Metal",
                        "quantity": 5,
                        "rarity": "common"
                    }
                ],
                "result_item": {
                    "name": "Basic Robot Parts",
                    "type": "robot_component",
                    "rarity": "common"
                }
            }
        }
