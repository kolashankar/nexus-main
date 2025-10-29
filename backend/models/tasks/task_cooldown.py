"""Task cooldown model."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from backend.models.base import BaseDBModel
from backend.models.tasks.task_types import TaskType

class TaskCooldown(BaseDBModel):
    """Tracks cooldown periods for task types."""
    player_id: str = Field(..., description="Player ID")
    task_type: TaskType = Field(..., description="Type of task on cooldown")
    last_completed_at: datetime = Field(..., description="When the task was last completed")
    cooldown_ends_at: datetime = Field(..., description="When the cooldown expires")
    completed_count: int = Field(default=1, description="Number of times completed during cooldown period")
    max_completions: int = Field(default=3, description="Max completions before cooldown")
