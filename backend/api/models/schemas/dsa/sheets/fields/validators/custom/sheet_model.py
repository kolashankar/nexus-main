from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DSASheetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    author: str = Field(..., min_length=1)
    
    # Sheet organization
    questions: List[dict] = Field(default_factory=list)  # [{"question_id": "...", "order": 1, "is_completed": false}]
    topics_covered: List[str] = Field(default_factory=list)  # Topic IDs
    
    # Difficulty breakdown
    difficulty_breakdown: dict = Field(default_factory=dict)  # {"easy": 10, "medium": 20, "hard": 15}
    estimated_time: Optional[str] = None  # "30 days", "2 months"
    
    # Sheet metadata
    level: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced|expert)$")
    tags: List[str] = Field(default_factory=list)  # ["interview-prep", "competitive", "company-specific"]
    cover_image: Optional[str] = None
    
    # Stats
    total_questions: int = 0
    followers_count: int = 0
    completion_count: int = 0
    
    # Settings
    is_published: bool = True
    is_featured: bool = False
    is_premium: bool = False

class DSASheetCreate(DSASheetBase):
    pass

class DSASheetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    author: Optional[str] = None
    questions: Optional[List[dict]] = None
    topics_covered: Optional[List[str]] = None
    difficulty_breakdown: Optional[dict] = None
    estimated_time: Optional[str] = None
    level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced|expert)$")
    tags: Optional[List[str]] = None
    cover_image: Optional[str] = None
    total_questions: Optional[int] = None
    followers_count: Optional[int] = None
    completion_count: Optional[int] = None
    is_published: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_premium: Optional[bool] = None

class DSASheetResponse(DSASheetBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
