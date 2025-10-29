"""Task location model."""

from pydantic import BaseModel, Field
from typing import Optional, Dict

class TaskLocation(BaseModel):
    """Location data for tasks."""
    name: str = Field(..., description="Location name")
    zone: str = Field(default="wasteland", description="Zone identifier")
    coordinates: Dict[str, float] = Field(
        default_factory=lambda: {"x": 0.0, "y": 0.0, "z": 0.0},
        description="3D coordinates"
    )
    radius: float = Field(default=50.0, description="Proximity radius required")
    description: Optional[str] = Field(default=None, description="Location description")
    is_dangerous: bool = Field(default=False, description="Whether location is dangerous")
    required_level: int = Field(default=1, description="Minimum level to access")
