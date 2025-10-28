"""World item model for discoverable items in the game world."""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from backend.models.base import BaseDBModel

class WorldItemPosition(BaseModel):
    """3D position in game world."""
    x: float
    y: float
    z: float

class WorldItem(BaseDBModel):
    """Discoverable item in the game world."""
    
    # Item details
    item_type: Literal["skill", "superpower_tool", "meta_trait"] = Field(...)
    item_name: str = Field(..., description="Name of the skill/tool/trait")
    item_id: str = Field(..., description="ID from traits/superpowers config")
    
    # World placement
    position: WorldItemPosition
    region: str = Field(default="central_hub")
    
    # Cost and level
    cost: int = Field(..., ge=0)
    required_level: int = Field(default=1, ge=1, le=100)
    
    # Status
    status: Literal["active", "claimed", "expired"] = Field(default="active")
    claimed_by: Optional[str] = None  # player_id
    
    # Timing
    spawned_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    
    # Discovery tracking
    discovered_by: list[str] = Field(default_factory=list)  # player_ids who've seen it
    
    # Icon/Visual
    icon: str = Field(default="default_icon.png")
    rarity: Literal["common", "uncommon", "rare", "epic", "legendary"] = Field(default="common")
    
    class Config:
        json_schema_extra = {
            "example": {
                "item_type": "skill",
                "item_name": "hacking",
                "item_id": "skill_hacking",
                "position": {"x": 100.5, "y": 0.0, "z": 50.3},
                "region": "central_hub",
                "cost": 500,
                "required_level": 5,
                "status": "active",
                "rarity": "uncommon"
            }
        }

class WorldItemResponse(BaseModel):
    """Response model for world items."""
    id: str
    item_type: str
    item_name: str
    position: WorldItemPosition
    cost: int
    required_level: int
    status: str
    rarity: str
    icon: str
    time_remaining: int  # seconds until expiration
