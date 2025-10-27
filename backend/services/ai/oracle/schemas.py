"""Oracle Pydantic Schemas"""

from typing import Dict, Optional, List, Any
from pydantic import BaseModel, Field
from datetime import datetime


class QuestObjective(BaseModel):
    """Quest objective"""
    description: str
    type: str = Field(..., pattern="^(collect|defeat|talk|hack|trade|visit|craft|donate|protect|discover)$")
    target: str
    required: int = Field(..., gt=0)
    current: int = 0
    optional: bool = False


class QuestRewards(BaseModel):
    """Quest rewards"""
    credits: int = 0
    xp: int = 0
    karma: int = 0
    items: List[str] = Field(default_factory=list)
    trait_boosts: Dict[str, float] = Field(default_factory=dict)
    special: Optional[str] = None


class QuestRequirements(BaseModel):
    """Quest requirements"""
    min_level: int = 1
    min_karma: Optional[float] = None
    required_traits: Dict[str, float] = Field(default_factory=dict)
    required_items: List[str] = Field(default_factory=list)


class QuestGenerationRequest(BaseModel):
    """Request to generate a quest"""
    player_id: str
    username: str
    level: int
    karma_points: float
    moral_class: str
    economic_class: str
    traits: Dict[str, float]
    recent_actions: List[str] = Field(default_factory=list)
    quest_type: str = "personal"
    difficulty: str = "medium"


class GeneratedQuest(BaseModel):
    """Generated quest data"""
    title: str
    description: str
    lore: str
    objectives: List[QuestObjective]
    rewards: QuestRewards
    requirements: QuestRequirements = Field(default_factory=QuestRequirements)
    difficulty: str = Field(..., pattern="^(easy|medium|hard|epic)$")
    estimated_time_minutes: int = Field(..., gt=0)
    moral_choice: Optional[str] = None
    branching_paths: List[str] = Field(default_factory=list)
    failure_consequence: Optional[str] = None
    quest_type: str = "personal"
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class CampaignChapter(BaseModel):
    """Campaign chapter"""
    chapter_number: int
    title: str
    description: str
    objectives: List[QuestObjective]
    choices: List[Dict[str, Any]] = Field(default_factory=list)


class CampaignEnding(BaseModel):
    """Campaign ending"""
    ending_type: str
    condition: str
    description: str
    rewards: QuestRewards


class GeneratedCampaign(BaseModel):
    """Generated campaign"""
    campaign_title: str
    campaign_description: str
    theme: str
    total_chapters: int
    chapters: List[CampaignChapter]
    endings: List[CampaignEnding]
