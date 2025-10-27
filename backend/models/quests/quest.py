"""Quest database model."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class QuestType(str, Enum):
    """Quest type enumeration."""
    PERSONAL = "personal"
    DAILY = "daily"
    WEEKLY = "weekly"
    GUILD = "guild"
    WORLD = "world"
    HIDDEN = "hidden"
    CAMPAIGN = "campaign"

class QuestStatus(str, Enum):
    """Quest status enumeration."""
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"

class QuestDifficulty(str, Enum):
    """Quest difficulty enumeration."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    LEGENDARY = "legendary"

class QuestObjective(BaseModel):
    """Quest objective model."""
    description: str
    type: str  # kill, collect, talk, hack, trade, visit
    target: Optional[str] = None
    current: int = 0
    required: int = 1
    completed: bool = False

class QuestRewards(BaseModel):
    """Quest rewards model."""
    credits: int = 0
    xp: int = 0
    karma: int = 0
    items: List[str] = Field(default_factory=list)
    trait_boosts: Dict[str, int] = Field(default_factory=dict)
    special: Optional[str] = None

class QuestRequirements(BaseModel):
    """Quest requirements model."""
    min_level: Optional[int] = None
    min_karma: Optional[int] = None
    required_traits: Dict[str, int] = Field(default_factory=dict)
    required_items: List[str] = Field(default_factory=list)
    required_quests: List[str] = Field(default_factory=list)

class Quest(BaseModel):
    """Quest database model."""
    quest_type: str  # personal, daily, weekly, guild, world, hidden, campaign
    title: str
    description: str
    lore: Optional[str] = None

    # Assignment
    player_id: Optional[str] = None
    guild_id: Optional[str] = None

    # Generation
    generated_by: str = "system"  # oracle, system
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    seed: Optional[str] = None

    # Progress
    status: str = "available"  # available, active, completed, failed, expired
    objectives: List[QuestObjective] = Field(default_factory=list)

    # Rewards
    rewards: QuestRewards = Field(default_factory=QuestRewards)

    # Requirements
    requirements: QuestRequirements = Field(default_factory=QuestRequirements)

    # Story
    story_data: Optional[Dict] = None

    # Expiry
    expires_at: Optional[datetime] = None

    # Completion
    completed_at: Optional[datetime] = None
    completion_time: Optional[int] = None  # seconds

    # Hidden quest specific
    is_hidden: bool = False
    discovery_conditions: Optional[Dict] = None
    hint: Optional[str] = None
    discovery_count: int = 0

    # Metadata
    difficulty: str = "medium"  # easy, medium, hard, legendary
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "quest_type": "personal",
                "title": "Test Your Hacking Skills",
                "description": "Successfully hack 5 corporate systems",
                "objectives": [
                    {
                        "description": "Hack corporate systems",
                        "type": "hack",
                        "target": "corporate",
                        "required": 5
                    }
                ],
                "rewards": {
                    "credits": 500,
                    "xp": 100,
                    "karma": -10
                },
                "difficulty": "medium"
            }
        }
