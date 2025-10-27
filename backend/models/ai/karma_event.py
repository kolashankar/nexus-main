"""Karma Event Model"""

from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class KarmaEvent(BaseModel):
    """Karma event triggered by actions"""

    event_id: str = Field(default_factory=lambda: str(
        datetime.utcnow().timestamp()))
    event_type: str
    triggered_by: str  # player_id
    description: str
    effects: Dict[str, float]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True
    duration_hours: Optional[int] = None
    affected_players: list[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "divine_blessing",
                "triggered_by": "player_123",
                "description": "A wave of positive energy spreads across the realm",
                "effects": {"xp_multiplier": 1.5, "karma_boost": 10},
                "duration_hours": 24
            }
        }
