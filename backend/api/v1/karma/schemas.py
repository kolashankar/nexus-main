from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class KarmaScoreResponse(BaseModel):
    """Player's karma score response."""
    player_id: str
    username: str
    karma_points: int
    moral_class: str
    karma_level: str
    next_milestone: Optional[int] = None

class KarmaHistoryResponse(BaseModel):
    """Karma change history entry."""
    action_type: str
    karma_change: int
    timestamp: datetime
    message: str

class KarmaEventResponse(BaseModel):
    """Karma-triggered event."""
    event_type: str
    event_name: str
    description: str
    triggered_at: datetime
    effects: dict

class CollectiveKarmaResponse(BaseModel):
    """World collective karma state."""
    collective_karma: int
    karma_trend: str  # rising, falling, stable
    total_players: int
    online_players: int