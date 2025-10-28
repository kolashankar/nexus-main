"""Model for player's equipped traits and active abilities."""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from backend.models.base import BaseDBModel

class EquippedTrait(BaseModel):
    """Individual equipped trait slot."""
    trait_id: str = Field(..., description="ID of the trait (e.g., 'hacking', 'meditation_sp')")
    trait_type: Literal["skill", "superpower_tool", "meta_trait", "virtue", "vice"] = Field(...)
    trait_level: int = Field(default=1, ge=1, le=100)
    slot_number: int = Field(..., ge=1, le=6, description="Slot 1-6")
    equipped_at: datetime = Field(default_factory=datetime.utcnow)

class PlayerEquippedTraits(BaseDBModel):
    """Player's equipped traits configuration."""
    player_id: str = Field(..., description="Player ID")
    
    # 6 equipped slots
    slot_1: Optional[EquippedTrait] = None
    slot_2: Optional[EquippedTrait] = None
    slot_3: Optional[EquippedTrait] = None
    slot_4: Optional[EquippedTrait] = None
    slot_5: Optional[EquippedTrait] = None
    slot_6: Optional[EquippedTrait] = None
    
    last_swap_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player123",
                "slot_1": {
                    "trait_id": "hacking",
                    "trait_type": "skill",
                    "trait_level": 25,
                    "slot_number": 1
                }
            }
        }