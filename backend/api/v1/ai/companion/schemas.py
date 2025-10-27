"""AI Companion API Schemas"""

from typing import Optional
from pydantic import BaseModel


class CompanionMessageAPI(BaseModel):
    """Message to companion"""
    message: str
    context: Optional[str] = None


class CompanionResponseAPI(BaseModel):
    """Response from companion"""
    companion_name: str
    personality: str
    response: str
    timestamp: str


class AdviceRequestAPI(BaseModel):
    """Request for advice"""
    situation: str


class CompanionStatusAPI(BaseModel):
    """Companion status"""
    name: str
    personality_type: str
    relationship_level: int
    conversations: int
    mood: str
