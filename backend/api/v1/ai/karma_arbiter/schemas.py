"""Karma Arbiter API Schemas"""

from typing import Dict, Optional, Any
from pydantic import BaseModel


class EvaluationRequestAPI(BaseModel):
    """API request for karma evaluation"""
    action_type: str
    action_details: Dict[str, Any]
    actor: Dict[str, Any]
    target: Optional[Dict[str, Any]] = None
    additional_context: Optional[str] = None


class EvaluationResponseAPI(BaseModel):
    """API response from karma evaluation"""
    karma_change: float
    trait_changes: Dict[str, float]
    event_triggered: Optional[str] = None
    message: str
    reasoning: str
    severity: str
    cached: bool = False
