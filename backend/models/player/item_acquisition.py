"""Item acquisition model for tracking player's item acquisition progress."""

from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from backend.models.base import BaseDBModel

class ItemAcquisition(BaseDBModel):
    """Player's active item acquisition."""
    
    # Player and item references
    player_id: str = Field(...)
    world_item_id: str = Field(..., description="Reference to WorldItem")
    
    # Item details (cached for easy access)
    item_type: Literal["skill", "superpower_tool", "meta_trait"] = Field(...)
    item_name: str
    item_id: str
    
    # Investment
    cost_paid: int = Field(..., ge=0)
    
    # Status
    status: Literal["investing", "completed", "claimed", "cancelled"] = Field(default="investing")
    
    # Timing
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completes_at: datetime = Field(...)
    claimed_at: Optional[datetime] = None
    
    # Progress
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player_123",
                "world_item_id": "item_456",
                "item_type": "skill",
                "item_name": "hacking",
                "item_id": "skill_hacking",
                "cost_paid": 500,
                "status": "investing",
                "progress_percentage": 45.5
            }
        }

class ItemAcquisitionResponse(BaseModel):
    """Response model for item acquisition."""
    id: str
    item_type: str
    item_name: str
    cost_paid: int
    status: str
    started_at: datetime
    completes_at: datetime
    time_remaining: int  # seconds
    progress_percentage: float

class StartAcquisitionRequest(BaseModel):
    """Request to start acquiring an item."""
    world_item_id: str

class ClaimAcquisitionRequest(BaseModel):
    """Request to claim a completed acquisition."""
    acquisition_id: str
