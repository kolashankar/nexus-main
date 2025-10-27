"""Robot training schemas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class StartTrainingRequest(BaseModel):
    """Request to start robot training."""
    robot_id: str = Field(..., description="ID of robot to train")
    training_type: str = Field(
        ..., description="Type of training (combat, efficiency, intelligence)")
    duration_hours: int = Field(
        default=1, ge=1, le=24, description="Training duration in hours")


class TrainingStatusResponse(BaseModel):
    """Training status response."""
    robot_id: str
    is_training: bool
    training_type: Optional[str] = None
    started_at: Optional[datetime] = None
    completes_at: Optional[datetime] = None
    time_remaining_seconds: Optional[int] = None
    rewards: Optional[Dict[str, Any]] = None
