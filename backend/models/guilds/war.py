from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class WarStatus(str, Enum):
    ACTIVE = "active"
    PEACE_NEGOTIATION = "peace_negotiation"
    ENDED = "ended"


class GuildWar(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # Participants
    attacker_guild_id: str
    defender_guild_id: str

    # War details
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    status: WarStatus = WarStatus.ACTIVE

    # War points
    attacker_points: int = 0
    defender_points: int = 0

    # Objectives
    target_territory: Optional[int] = None

    # Peace terms
    peace_offer: Optional[dict] = None
    peace_offered_by: Optional[str] = None

    # Outcome
    winner_guild_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "attacker_guild_id": "guild_123",
                "defender_guild_id": "guild_456",
                "target_territory": 5,
                "status": "active"
            }
        }
