"""AI Companion Pydantic Schemas"""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CompanionMessage(BaseModel):
    """Message to/from companion"""
    player_id: str
    message: str
    context: Optional[str] = None


class CompanionResponse(BaseModel):
    """Response from companion"""
    companion_name: str
    personality: str
    response: str
    timestamp: datetime = datetime.utcnow()


class AdviceRequest(BaseModel):
    """Request for advice"""
    player_id: str
    situation: str


class AdviceResponse(BaseModel):
    """Advice from companion"""
    companion_name: str
    advice: str
    personality: str
    timestamp: datetime = datetime.utcnow()


class CompanionStatus(BaseModel):
    """Companion status"""
    name: str
    personality_type: str
    relationship_level: int
    conversations: int
    last_interaction: Optional[datetime] = None
    mood: str
