"""World & Events API schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class EventType(str, Enum):
    """World event types."""
    GOLDEN_AGE = "golden_age"
    DIVINE_BLESSING = "divine_blessing"
    FESTIVAL_OF_LIGHT = "festival_of_light"
    THE_CONVERGENCE = "the_convergence"
    THE_PURGE = "the_purge"
    ECONOMIC_COLLAPSE = "economic_collapse"
    DARK_ECLIPSE = "dark_eclipse"
    JUDGMENT_DAY = "judgment_day"
    METEOR_SHOWER = "meteor_shower"
    GLITCH_IN_MATRIX = "glitch_in_matrix"
    ROBOT_UPRISING = "robot_uprising"
    TIME_ANOMALY = "time_anomaly"


class KarmaTrend(str, Enum):
    """Global karma trend."""
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"


class WorldStateResponse(BaseModel):
    """World state information."""
    collective_karma: float
    karma_trend: KarmaTrend
    active_event: Optional[Dict[str, Any]] = None
    current_season: int
    season_start: datetime
    season_end: datetime
    total_players: int
    online_players: int
    total_karma_generated: float
    territories: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class WorldEventResponse(BaseModel):
    """World event details."""
    event_id: str
    event_type: EventType
    name: str
    description: str
    started_at: datetime
    ends_at: datetime
    effects: Dict[str, Any]
    trigger_reason: Optional[str] = None
    affected_territories: List[int] = Field(default_factory=list)
    participants: int = 0
    is_active: bool = True

    class Config:
        from_attributes = True


class RegionalEventResponse(BaseModel):
    """Regional event details."""
    event_id: str
    territory_id: int
    territory_name: str
    event_type: str
    name: str
    description: str
    started_at: datetime
    ends_at: Optional[datetime] = None
    effects: Dict[str, Any]
    is_active: bool = True

    class Config:
        from_attributes = True


class GlobalKarmaResponse(BaseModel):
    """Global karma statistics."""
    collective_karma: float
    karma_trend: KarmaTrend
    positive_actions_24h: int
    negative_actions_24h: int
    neutral_actions_24h: int
    top_contributors: List[Dict[str, Any]]
    karma_distribution: Dict[str, int]
    next_event_threshold: Optional[float] = None
    next_event_type: Optional[str] = None

    class Config:
        from_attributes = True


class TriggerEventRequest(BaseModel):
    """Request to trigger a world event."""
    event_type: EventType
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict)


class EventResponseRequest(BaseModel):
    """Player response to an event."""
    response_type: str = Field(...,
                               description="How the player responds to the event")
    action_data: Optional[Dict[str, Any]] = Field(default_factory=dict)
