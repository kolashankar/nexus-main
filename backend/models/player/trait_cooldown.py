"""Model for trait ability cooldowns."""

from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
from backend.models.base import BaseDBModel

class TraitCooldown(BaseDBModel):
    """Cooldown tracking for trait abilities."""
    player_id: str = Field(..., description="Player ID")
    trait_id: str = Field(..., description="Trait identifier")
    trait_type: Literal["skill", "superpower_tool", "meta_trait", "virtue", "vice"] = Field(...)
    
    # Timing
    used_at: datetime = Field(default_factory=datetime.utcnow)
    available_at: datetime = Field(..., description="When ability is available again")
    cooldown_seconds: int = Field(..., description="Total cooldown duration")
    
    # Status
    is_active: bool = Field(default=True, description="If cooldown is still active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player123",
                "trait_id": "hacking",
                "trait_type": "skill",
                "used_at": "2025-07-10T10:00:00",
                "available_at": "2025-07-10T10:30:00",
                "cooldown_seconds": 1800,
                "is_active": True
            }
        }

class TraitUsageHistory(BaseDBModel):
    """History of trait ability usage."""
    player_id: str = Field(...)
    trait_id: str = Field(...)
    trait_type: str = Field(...)
    
    # Action details
    action_type: str = Field(..., description="What ability was used")
    target_id: Optional[str] = Field(None, description="Target player ID if applicable")
    success: bool = Field(default=True)
    
    # Results
    karma_change: int = Field(default=0)
    credits_affected: int = Field(default=0)
    damage_dealt: int = Field(default=0)
    
    # Metadata
    used_at: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[dict] = Field(None, description="Where ability was used")
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player123",
                "trait_id": "hacking",
                "action_type": "credit_hack",
                "target_id": "player456",
                "success": True,
                "karma_change": -10,
                "credits_affected": 500
            }
        }