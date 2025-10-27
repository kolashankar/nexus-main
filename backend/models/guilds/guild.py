from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class GuildRank(str, Enum):
    LEADER = "leader"
    OFFICER = "officer"
    VETERAN = "veteran"
    MEMBER = "member"
    RECRUIT = "recruit"


class GuildMember(BaseModel):
    player_id: str
    rank: GuildRank = GuildRank.MEMBER
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    contribution: int = 0


class Guild(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    tag: str  # 3-5 character guild tag
    description: str = ""

    # Leadership
    leader_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Members
    members: List[GuildMember] = Field(default_factory=list)
    total_members: int = 1
    max_members: int = 50  # Can be upgraded

    # Progression
    level: int = 1
    xp: int = 0

    # Resources
    guild_bank: dict = Field(default_factory=lambda: {
        "credits": 0,
        "resources": {}
    })

    # Territory
    controlled_territories: List[int] = Field(default_factory=list)

    # Karma
    guild_karma: int = 0

    # Skills
    unlocked_skills: List[str] = Field(default_factory=list)

    # Wars
    active_wars: List[dict] = Field(default_factory=list)

    # Settings
    recruitment_open: bool = True
    emblem: str = ""
    reputation: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Shadow Hackers",
                "tag": "SHDW",
                "description": "Elite hacker guild",
                "leader_id": "player_123",
                "max_members": 50
            }
        }
