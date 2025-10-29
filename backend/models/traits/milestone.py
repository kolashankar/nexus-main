"""Milestone model."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List
from backend.models.base import BaseDBModel

class TraitMilestone(BaseDBModel):
    """Represents a trait milestone achievement."""
    player_id: str = Field(..., description="Player ID")
    trait: str = Field(..., description="Trait name")
    threshold: int = Field(..., description="Milestone threshold (25, 50, 75, 100)")
    value_at_milestone: float = Field(..., description="Trait value when milestone was reached")
    reached_at: datetime = Field(default_factory=datetime.utcnow)
    rewards: Dict[str, Any] = Field(default_factory=dict, description="Rewards granted")
    acknowledged: bool = Field(default=False, description="Whether player has seen this milestone")
