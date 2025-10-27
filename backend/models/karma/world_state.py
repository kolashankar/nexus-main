"""World state model for tracking global karma and events."""

from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from enum import Enum

class KarmaTrend(str, Enum):
    """Trend of collective karma."""
    RISING = "rising"
    FALLING = "falling"
    STABLE = "stable"

class ActiveEvent(BaseModel):
    """Active world event model."""
    event_type: str
    name: str
    description: str
    started_at: datetime
    ends_at: datetime
    effects: Dict = Field(default_factory=dict)

class Territory(BaseModel):
    """Territory model."""
    territory_id: int
    name: str
    controlling_guild_id: Optional[str] = None
    contested: bool = False
    resources: Dict = Field(default_factory=dict)

class AIPantheonState(BaseModel):
    """State of AI Pantheon activities."""
    last_karma_arbiter_action: Optional[datetime] = None
    last_oracle_quest: Optional[datetime] = None
    last_economist_update: Optional[datetime] = None
    last_warlord_event: Optional[datetime] = None
    last_architect_event: Optional[datetime] = None

class WorldState(BaseModel):
    """World state model for global game state."""

    # Global Karma
    collective_karma: float = Field(default=0.0)
    karma_trend: KarmaTrend = KarmaTrend.STABLE

    # Active Global Event
    active_event: Optional[ActiveEvent] = None

    # Season Info
    current_season: int = 1
    season_start: datetime = Field(default_factory=datetime.utcnow)
    season_end: datetime = Field(default_factory=lambda: datetime.utcnow())

    # Territories
    territories: List[Territory] = Field(default_factory=list)

    # World Stats
    total_players: int = 0
    online_players: int = 0
    total_karma_generated: float = 0.0
    total_wealth: float = 0.0

    # AI State
    ai_pantheon_state: AIPantheonState = Field(default_factory=AIPantheonState)

    # Last update
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
