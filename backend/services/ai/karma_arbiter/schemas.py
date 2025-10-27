"""Karma Arbiter Pydantic Schemas"""

from typing import Dict, Optional, List
from pydantic import BaseModel, Field


class ActionContext(BaseModel):
    """Context for action evaluation"""
    action_type: str
    action_details: Dict
    actor_id: str
    target_id: Optional[str] = None
    amount: Optional[float] = None
    timestamp: str


class PlayerProfile(BaseModel):
    """Player profile for evaluation"""
    username: str
    karma_points: float
    moral_class: str
    economic_class: str
    traits: Dict[str, float]
    recent_actions: List[str] = Field(default_factory=list)


class EvaluationRequest(BaseModel):
    """Request for karma evaluation"""
    context: ActionContext
    actor: PlayerProfile
    target: Optional[PlayerProfile] = None
    additional_context: Optional[str] = None


class EvaluationResponse(BaseModel):
    """Response from karma evaluation"""
    karma_change: float = Field(..., ge=-200, le=200)
    trait_changes: Dict[str, float] = Field(default_factory=dict)
    event_triggered: Optional[str] = None
    message: str
    reasoning: str
    severity: str = Field(..., pattern="^(minor|moderate|major|critical)$")
    cached: bool = False


class KarmaEvent(BaseModel):
    """Karma event triggered by actions"""
    event_type: str
    triggered_by: str
    description: str
    effects: Dict[str, float]
    timestamp: str
