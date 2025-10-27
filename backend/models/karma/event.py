from pydantic import Field
from datetime import datetime
from typing import Dict, Optional
from backend.models.base import BaseDBModel

class KarmaEvent(BaseDBModel):
    """Karma-triggered event model."""
    event_type: str = Field(..., description="Type of karma event")
    event_name: str = Field(..., description="Name of the event")
    description: str = Field(..., description="Event description")

    # Trigger conditions
    triggered_by: str = Field(..., description="What triggered this event")
    karma_threshold: Optional[int] = None

    # Event details
    effects: Dict = Field(default_factory=dict, description="Event effects")
    duration: Optional[int] = Field(None, description="Duration in seconds")

    # Affected entities
    affected_players: list = Field(default_factory=list)
    affected_guilds: list = Field(default_factory=list)

    # Status
    status: str = Field(default="active")  # active, completed, cancelled
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ends_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "event_type": "positive_karma",
                "event_name": "Divine Blessing",
                "description": "Your exceptional karma has attracted divine favor",
                "triggered_by": "karma_milestone",
                "karma_threshold": 1000,
                "effects": {
                    "karma_bonus": 0.1,
                    "xp_bonus": 0.2
                },
                "duration": 3600
            }
        }