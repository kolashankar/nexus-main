"""World event model"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class EventType(str, Enum):
    """Types of world events"""
    # Positive events
    GOLDEN_AGE = "golden_age"
    DIVINE_BLESSING = "divine_blessing"
    FESTIVAL_OF_LIGHT = "festival_of_light"
    THE_CONVERGENCE = "the_convergence"

    # Negative events
    THE_PURGE = "the_purge"
    ECONOMIC_COLLAPSE = "economic_collapse"
    DARK_ECLIPSE = "dark_eclipse"
    JUDGMENT_DAY = "judgment_day"

    # Neutral events
    METEOR_SHOWER = "meteor_shower"
    GLITCH_IN_MATRIX = "glitch_in_matrix"
    ROBOT_UPRISING = "robot_uprising"
    TIME_ANOMALY = "time_anomaly"

    # Regional events
    TERRITORY_CONTEST = "territory_contest"
    RESOURCE_BOOM = "resource_boom"
    NATURAL_DISASTER = "natural_disaster"


class EventSeverity(str, Enum):
    """Event severity levels"""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"
    CATASTROPHIC = "catastrophic"


class EventScope(str, Enum):
    """Event scope"""
    GLOBAL = "global"  # Affects all players
    REGIONAL = "regional"  # Affects specific territory
    LOCAL = "local"  # Affects specific location


class WorldEvent(BaseModel):
    """World event model"""
    id: str = Field(alias="_id")
    event_type: EventType

    # Event info
    name: str
    description: str
    lore: Optional[str] = None

    # Properties
    severity: EventSeverity = EventSeverity.MODERATE
    scope: EventScope = EventScope.GLOBAL

    # Effects
    effects: Dict[str, Any] = Field(default_factory=dict)

    # Trigger conditions
    triggered_by: str = "architect"  # "architect", "karma", "player_action"
    trigger_reason: Optional[str] = None
    karma_threshold: Optional[int] = None

    # Duration
    started_at: datetime
    ends_at: datetime
    duration_hours: int

    # Status
    status: str = "active"  # active, ended, cancelled

    # Participation
    affected_players: List[str] = Field(default_factory=list)
    affected_territories: List[int] = Field(default_factory=list)

    # Statistics
    participation_count: int = 0

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def is_active(self) -> bool:
        """Check if event is currently active"""
        now = datetime.utcnow()
        return self.status == "active" and self.started_at <= now <= self.ends_at

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return self.model_dump(by_alias=True)
