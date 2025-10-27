from pydantic import Field
from datetime import datetime
from typing import Dict, Optional
from backend.models.base import BaseDBModel

class ActionHistory(BaseDBModel):
    """Extended action history with more details."""
    # Action details
    action_type: str = Field(...)
    actor_id: str = Field(...)
    target_id: Optional[str] = None

    # Outcome
    success: bool = Field(...)
    amount: int = Field(default=0)

    # Effects
    karma_change: int = Field(default=0)
    trait_changes: Dict[str, int] = Field(default_factory=dict)
    xp_gained: int = Field(default=0)

    # Context
    message: str = Field(default="")
    location: Optional[Dict] = None
    witnesses: list = Field(default_factory=list)

    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None