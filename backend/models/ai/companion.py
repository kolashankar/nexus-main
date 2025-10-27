"""AI Companion Model"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AICompanionModel(BaseModel):
    """AI Companion data for a player"""

    player_id: str
    name: str = "Aria"
    personality_type: str = "neutral_guide"
    relationship_level: int = Field(default=0, ge=0, le=100)
    conversations: int = 0
    last_advice: Optional[datetime] = None
    mood: str = "neutral"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player_123",
                "name": "Aria",
                "personality_type": "wise_mentor",
                "relationship_level": 42,
                "conversations": 156,
                "mood": "content and proud"
            }
        }
