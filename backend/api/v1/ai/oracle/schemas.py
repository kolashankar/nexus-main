"""Oracle API Schemas"""

from typing import Dict, Optional, Any, List
from pydantic import BaseModel


class QuestGenerationRequestAPI(BaseModel):
    """API request for quest generation"""
    player: Optional[Dict[str, Any]
        ] = None  # Will use current user if not provided
    quest_type: str = "personal"
    difficulty: str = "medium"


class QuestObjectiveAPI(BaseModel):
    """Quest objective"""
    description: str
    type: str
    target: str
    required: int
    current: int = 0
    optional: bool = False


class QuestRewardsAPI(BaseModel):
    """Quest rewards"""
    credits: int = 0
    xp: int = 0
    karma: int = 0
    items: List[str] = []
    trait_boosts: Dict[str, float] = {}
    special: Optional[str] = None


class GeneratedQuestAPI(BaseModel):
    """Generated quest"""
    title: str
    description: str
    lore: str
    objectives: List[QuestObjectiveAPI]
    rewards: QuestRewardsAPI
    difficulty: str
    estimated_time_minutes: int
    quest_type: str


class CampaignChapterAPI(BaseModel):
    """Campaign chapter"""
    chapter_number: int
    title: str
    description: str


class GeneratedCampaignAPI(BaseModel):
    """Generated campaign"""
    campaign_title: str
    campaign_description: str
    theme: str
    total_chapters: int
