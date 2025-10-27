"""Quest API schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class QuestObjectiveSchema(BaseModel):
    """Quest objective schema"""
    objective_id: str
    description: str
    type: str
    target: str
    current: int
    required: int
    completed: bool


class QuestRewardSchema(BaseModel):
    """Quest reward schema"""
    credits: int = 0
    xp: int = 0
    karma: int = 0
    karma_tokens: int = 0
    items: List[str] = Field(default_factory=list)
    trait_boosts: Dict[str, int] = Field(default_factory=dict)
    special: Optional[str] = None


class QuestSchema(BaseModel):
    """Quest schema"""
    id: str = Field(alias="_id")
    quest_type: str
    title: str
    description: str
    lore: Optional[str] = None
    status: str
    objectives: List[QuestObjectiveSchema]
    rewards: QuestRewardSchema
    expires_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    generated_at: datetime

    class Config:
        populate_by_name = True


class QuestResponse(BaseModel):
    """Quest response"""
    quest: Dict[str, Any]


class QuestListResponse(BaseModel):
    """Quest list response"""
    quests: List[Dict[str, Any]]
    total: int


class QuestAcceptRequest(BaseModel):
    """Request to accept quest"""
    quest_id: str


class QuestAbandonRequest(BaseModel):
    """Request to abandon quest"""
    quest_id: str


class QuestCompleteRequest(BaseModel):
    """Request to complete quest"""
    quest_id: str


class ObjectiveProgressRequest(BaseModel):
    """Request to update objective progress"""
    quest_id: str
    objective_id: str
    progress: int = 1


class CampaignStartRequest(BaseModel):
    """Request to start campaign"""
    campaign_id: Optional[str] = None
    campaign_type: Optional[str] = None


class CampaignChoiceRequest(BaseModel):
    """Request to make campaign choice"""
    campaign_id: str
    choice_id: str
    option_id: str


class QuestGenerateRequest(BaseModel):
    """Request to generate quest"""
    quest_type: Optional[str] = "personal"
    preferences: Optional[Dict[str, Any]] = None
