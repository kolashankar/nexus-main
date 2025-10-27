from pydantic import BaseModel, Field
from typing import List


class CampaignChapterInfo(BaseModel):
    chapter_number: int
    title: str
    description: str
    completed: bool
    unlocked: bool


class CampaignInfo(BaseModel):
    id: str
    campaign_type: str
    title: str
    description: str
    total_chapters: int
    estimated_duration: str  # e.g., "10-20 hours"


class CampaignListResponse(BaseModel):
    campaigns: List[CampaignInfo]


class StartCampaignRequest(BaseModel):
    campaign_type: str = Field(..., description="Type of campaign to start")


class CampaignProgressResponse(BaseModel):
    campaign_id: str
    title: str
    current_chapter: int
    total_chapters: int
    completion_percentage: float
    chapters: List[CampaignChapterInfo]


class MakeCampaignChoiceRequest(BaseModel):
    chapter_number: int = Field(..., description="Chapter number")
    choice: str = Field(..., description="Choice made")
