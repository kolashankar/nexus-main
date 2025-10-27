from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any


class CraftingHistory(BaseModel):
    """Player crafting history entry."""
    player_id: str = Field(..., description="Player ID")
    recipe_id: str = Field(..., description="Recipe ID used")
    recipe_name: str = Field(..., description="Recipe name")

    item_crafted: str = Field(..., description="Name of item crafted")
    quantity: int = Field(default=1, ge=1, description="Quantity crafted")
    success: bool = Field(
        default=True, description="Whether craft was successful")

    materials_used: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Materials consumed"
    )

    xp_gained: int = Field(default=0, ge=0, description="XP gained")
    bonus_received: Optional[str] = Field(
        default=None, description="Bonus effect received")

    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Craft timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player_123",
                "recipe_id": "basic_robot_parts",
                "recipe_name": "Basic Robot Parts",
                "item_crafted": "Basic Robot Parts",
                "quantity": 1,
                "success": True,
                "materials_used": [
                    {"material_id": "scrap_metal", "quantity": 5}
                ],
                "xp_gained": 25,
                "timestamp": "2025-01-01T12:00:00Z"
            }
        }
