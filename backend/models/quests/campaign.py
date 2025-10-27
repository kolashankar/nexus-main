"""Campaign database model."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class CampaignType(str, Enum):
    """Campaign type enumeration."""
    MAIN = "main"
    SIDE = "side"
    MORAL = "moral"
    ECONOMIC = "economic"
    SEASONAL = "seasonal"
    LEGACY = "legacy"
    REDEMPTION = "redemption"
    FALL_FROM_GRACE = "fall_from_grace"
    NEUTRAL_PATH = "neutral_path"
    POWER_QUEST = "power_quest"
    ORIGIN_STORY = "origin_story"
    MYSTERY = "mystery"

class CampaignChoice(BaseModel):
    """Campaign choice model."""
    id: str
    text: str
    description: Optional[str] = None
    consequences: Dict = Field(default_factory=dict)
    branching: Optional[str] = None  # Changes story path

class CampaignChapter(BaseModel):
    """Campaign chapter model."""
    chapter_number: int
    title: str
    description: str
    story_text: str
    objectives: List[str] = Field(default_factory=list)
    choices: List[CampaignChoice] = Field(default_factory=list)
    rewards: Optional[Dict] = None

class Campaign(BaseModel):
    """Campaign database model."""
    title: str
    description: str
    lore: str

    # Chapters
    chapters: List[CampaignChapter] = Field(default_factory=list)
    total_chapters: int

    # Requirements
    min_level: int = 1
    min_karma: Optional[int] = None
    required_moral_class: Optional[str] = None

    # Metadata
    difficulty: str = "medium"
    estimated_time: int = 0  # minutes
    category: str = "main"

    # Branching paths
    branching_paths: List[str] = Field(default_factory=lambda: ["main"])

    # Stats
    started_count: int = 0
    completed_count: int = 0
    average_completion_time: Optional[int] = None

    # Rewards
    completion_rewards: Dict = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Redemption Arc",
                "description": "A journey from darkness to light",
                "lore": "For those seeking redemption...",
                "total_chapters": 10,
                "difficulty": "hard",
                "category": "moral"
            }
        }

class CampaignProgress(BaseModel):
    """Campaign progress tracking model."""
    player_id: str
    campaign_id: str
    status: str = "active"  # active, completed, abandoned

    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    current_chapter: int = 0
    chapters_completed: int = 0
    total_chapters: int

    choices_made: List[Dict] = Field(default_factory=list)
    branching_path: str = "main"

    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player123",
                "campaign_id": "campaign456",
                "status": "active",
                "current_chapter": 3,
                "chapters_completed": 2,
                "total_chapters": 10
            }
        }
