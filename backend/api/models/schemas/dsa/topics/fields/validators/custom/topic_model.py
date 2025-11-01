from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DSATopicBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    icon: Optional[str] = None  # emoji or icon name
    color: Optional[str] = "#3B82F6"  # hex color for UI
    parent_topic: Optional[str] = None  # for sub-topics
    difficulty_distribution: Optional[dict] = None  # {"easy": 10, "medium": 20, "hard": 15}
    is_active: bool = True

class DSATopicCreate(DSATopicBase):
    pass

class DSATopicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    parent_topic: Optional[str] = None
    difficulty_distribution: Optional[dict] = None
    is_active: Optional[bool] = None

class DSATopicResponse(DSATopicBase):
    id: str
    question_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
