"""Robot schemas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class PurchaseRobotRequest(BaseModel):
    """Request to purchase a robot."""
    robot_type: str = Field(..., description="Type of robot to purchase")
    custom_name: Optional[str] = Field(
        None, description="Custom name for the robot")


class RobotResponse(BaseModel):
    """Robot information response."""
    id: str
    robot_type: str
    name: str
    owner_id: str
    level: int
    experience: int
    stats: Dict[str, Any]
    status: str
    created_at: datetime
    last_used: Optional[datetime] = None
