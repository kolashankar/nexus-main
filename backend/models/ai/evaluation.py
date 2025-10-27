"""Evaluation Model"""

from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ActionEvaluation(BaseModel):
    """Stored action evaluation"""

    evaluation_id: str = Field(
        default_factory=lambda: str(datetime.utcnow().timestamp()))
    action_type: str
    actor_id: str
    target_id: Optional[str] = None
    karma_change: float
    trait_changes: Dict[str, float]
    event_triggered: Optional[str] = None
    message: str
    reasoning: str
    severity: str
    cached: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "help",
                "actor_id": "player_123",
                "target_id": "player_456",
                "karma_change": 25.0,
                "trait_changes": {"kindness": 2, "empathy": 1},
                "message": "Your compassion shines through your actions.",
                "reasoning": "Helping others in need aligns with virtuous behavior.",
                "severity": "moderate"
            }
        }
