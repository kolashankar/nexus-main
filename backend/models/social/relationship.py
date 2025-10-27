from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class RelationshipType(str, Enum):
    ALLIANCE = "alliance"
    RIVAL = "rival"
    MARRIAGE = "marriage"
    MENTORSHIP = "mentorship"
    FRIEND = "friend"
    ENEMY = "enemy"


class Relationship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: RelationshipType
    player1_id: str
    player2_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    active: bool = True

    # Relationship-specific data
    metadata: dict = Field(default_factory=dict)


class Alliance(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    members: list[str] = Field(default_factory=list)  # Max 3 players
    created_at: datetime = Field(default_factory=datetime.utcnow)
    alliance_name: Optional[str] = None

    # Benefits
    shared_xp: bool = True
    shared_karma: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "members": ["player_123", "player_456", "player_789"],
                "alliance_name": "The Trinity"
            }
        }


class Marriage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    player1_id: str
    player2_id: str
    married_at: datetime = Field(default_factory=datetime.utcnow)
    divorced_at: Optional[datetime] = None
    active: bool = True

    # Marriage benefits
    shared_resources: bool = True
    shared_xp_bonus: float = 1.1  # 10% bonus
    joint_karma: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "player1_id": "player_123",
                "player2_id": "player_456",
                "shared_resources": True
            }
        }


class Mentorship(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    mentor_id: str
    apprentice_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    graduated_at: Optional[datetime] = None
    active: bool = True

    # Progress
    apprentice_level: int = 1
    lessons_completed: int = 0

    # Rewards
    mentor_legacy_points: int = 0
    apprentice_xp_bonus: float = 1.25  # 25% faster learning

    class Config:
        json_schema_extra = {
            "example": {
                "mentor_id": "player_123",
                "apprentice_id": "player_456",
                "lessons_completed": 5
            }
        }
