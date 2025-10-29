"""Advanced task model with enhanced features."""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.models.base import BaseDBModel
from backend.models.tasks.task_types import TaskType, TaskDifficulty, TaskCategory

class SkillRequirement(BaseModel):
    """Skill requirement for a task."""
    skill_name: str = Field(..., description="Name of required skill")
    min_level: int = Field(..., ge=0, le=100, description="Minimum skill level required")

class LocationRequirement(BaseModel):
    """Location requirement for a task."""
    location_name: str = Field(..., description="Required location name")
    coordinates: Optional[Dict[str, float]] = Field(default=None, description="X, Y, Z coordinates")
    radius: float = Field(default=50.0, description="Required proximity radius")

class TaskReward(BaseModel):
    """Enhanced task rewards."""
    xp: int = Field(default=0, ge=0)
    credits: int = Field(default=0, ge=0)
    karma: int = Field(default=0)
    items: List[str] = Field(default_factory=list, description="Item IDs to grant")
    skills: List[str] = Field(default_factory=list, description="Skill IDs to unlock")
    titles: List[str] = Field(default_factory=list, description="Title IDs to grant")
    reputation: Dict[str, int] = Field(default_factory=dict, description="Faction reputation changes")
    random_bonus: bool = Field(default=False, description="10% chance for bonus rewards")

class TaskChoice(BaseModel):
    """Enhanced task choice with more impact."""
    text: str = Field(..., description="Choice text")
    traits_impact: Dict[str, int] = Field(default_factory=dict, description="Trait changes")
    rewards: TaskReward = Field(default_factory=TaskReward, description="Choice-specific rewards")
    consequences: List[str] = Field(default_factory=list, description="Future consequences")
    required_traits: Optional[Dict[str, int]] = Field(default=None, description="Required trait levels")
    unlocks_tasks: List[str] = Field(default_factory=list, description="Tasks unlocked by this choice")

class AdvancedTask(BaseDBModel):
    """Advanced task with all new features."""
    player_id: str = Field(..., description="Player ID")
    task_id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    
    # Classification
    type: TaskType = Field(default=TaskType.MORAL_CHOICE)
    difficulty: TaskDifficulty = Field(default=TaskDifficulty.EASY)
    category: TaskCategory = Field(default=TaskCategory.PERSONAL)
    
    # Requirements
    min_level: int = Field(default=1, ge=1, description="Minimum player level")
    skill_requirements: List[SkillRequirement] = Field(default_factory=list)
    location_requirement: Optional[LocationRequirement] = Field(default=None)
    previous_tasks: List[str] = Field(default_factory=list, description="Required completed tasks")
    
    # Rewards
    base_rewards: TaskReward = Field(default_factory=TaskReward)
    
    # Choices
    choices: List[TaskChoice] = Field(default_factory=list)
    
    # Multiplayer
    is_multiplayer: bool = Field(default=False)
    required_players: Optional[int] = Field(default=None, ge=2, le=10)
    participating_players: List[str] = Field(default_factory=list)
    
    # Story continuity
    story_arc: Optional[str] = Field(default=None, description="Story arc this task belongs to")
    sequence_number: Optional[int] = Field(default=None, description="Position in story sequence")
    remembers_choices: List[str] = Field(default_factory=list, description="Previous choice IDs this task references")
    
    # Status
    status: str = Field(default="active", description="Task status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    choice_made: Optional[int] = None
    
    # Analytics
    times_completed: int = Field(default=0, description="Global completion count")
    choice_statistics: Dict[int, int] = Field(default_factory=dict, description="Choice selection counts")
    average_completion_time: Optional[float] = Field(default=None, description="Average time to complete in seconds")
