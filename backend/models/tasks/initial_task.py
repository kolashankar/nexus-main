"""Initial task models for new players."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.models.base import BaseDBModel

class TaskChoice(BaseModel):
    """A choice the player can make in a task."""
    text: str = Field(..., description="Choice text")
    traits_impact: Dict[str, int] = Field(
        default_factory=dict,
        description="Traits affected by this choice (trait_name: change_amount)"
    )

class InitialTask(BaseDBModel):
    """Initial task for new players without established traits."""
    player_id: str = Field(..., description="Player ID")
    task_id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    type: str = Field(..., description="Task type (moral_choice, exploration, skill_based, social)")
    difficulty: str = Field(default="easy", description="Task difficulty")
    
    # Rewards
    xp_reward: int = Field(default=50, ge=0)
    credits_reward: int = Field(default=100, ge=0)
    
    # Choices
    choices: List[TaskChoice] = Field(default_factory=list, description="Available choices")
    
    # Status
    status: str = Field(default="active", description="Task status (active, completed, expired)")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    choice_made: Optional[int] = None

class TaskCompletion(BaseModel):
    """Result of completing a task."""
    task_id: str
    title: str
    choice_text: str
    traits_changed: Dict[str, int]
    xp_gained: int
    credits_gained: int
    karma_change: int
