from pydantic import Field
from datetime import datetime
from typing import Dict, Optional
from backend.models.base import BaseDBModel

class Action(BaseDBModel):
    """Action history model"""
    action_type: str = Field(...,
                             description="Type of action (hack, help, steal, donate, trade)")
    actor_id: str = Field(..., description="Player who performed the action")
    target_id: Optional[str] = Field(
        None, description="Target player (if applicable)")
    amount: Optional[int] = Field(
        None, description="Amount involved (credits, items, etc.)")
    success: bool = Field(default=True)
    karma_change: int = Field(default=0)
    trait_changes: Dict[str, float] = Field(default_factory=dict)
    message: str = Field(default="")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
