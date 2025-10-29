"""Models for multiplayer tasks (co-op, competitive, PvP moral)."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class TaskParticipantStatus(str, Enum):
    """Status of task participant."""
    INVITED = "invited"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class CoopTaskParticipant(BaseModel):
    """Participant in a co-op task."""
    player_id: str
    player_name: str
    role: str
    status: TaskParticipantStatus = TaskParticipantStatus.INVITED
    joined_at: Optional[datetime] = None
    contribution_score: float = 0.0

class CoopTask(BaseModel):
    """Co-op multiplayer task model."""
    _id: str = Field(alias="_id")
    task_id: str
    type: str = "coop"
    title: str
    description: str
    difficulty: str
    min_players: int = 2
    max_players: int = 4
    duration_minutes: int
    roles: List[Dict[str, Any]]
    creator_id: str
    participants: List[CoopTaskParticipant] = []
    rewards: Dict[str, Any]
    trait_impacts: Dict[str, int]
    status: str = "looking_for_partners"
    created_at: datetime
    expires_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True

class CompetitiveTaskParticipant(BaseModel):
    """Participant in competitive task."""
    player_id: str
    player_name: str
    player_level: int
    skill_level: float
    score: float = 0.0
    rank: Optional[int] = None

class CompetitiveTask(BaseModel):
    """Competitive PvP task model."""
    _id: str = Field(alias="_id")
    task_id: str
    type: str = "competitive"
    category: str  # speed_challenge, combat, economic, social
    title: str
    description: str
    difficulty: str
    duration_minutes: int
    required_skill: str
    min_skill_level: int
    creator: CompetitiveTaskParticipant
    opponent: Optional[CompetitiveTaskParticipant] = None
    winner_rewards: Dict[str, Any]
    loser_rewards: Dict[str, Any]
    trait_impacts_winner: Dict[str, int]
    trait_impacts_loser: Dict[str, int]
    status: str = "looking_for_opponent"
    created_at: datetime
    expires_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    winner: Optional[str] = None
    
    class Config:
        populate_by_name = True

class PvPMoralChoice(BaseModel):
    """Choice in a PvP moral task."""
    id: int
    text: str
    player_effects: Dict[str, Any]
    target_effects: Dict[str, Any]

class PvPMoralTask(BaseModel):
    """PvP moral choice task - affects another player."""
    _id: str = Field(alias="_id")
    task_id: str
    type: str = "pvp_moral"
    title: str
    description: str
    difficulty: str
    player_id: str  # Player making the choice
    player_name: str
    target_player_id: str  # Player affected by choice
    target_player_name: str
    choices: List[PvPMoralChoice]
    status: str = "pending_choice"
    created_at: datetime
    expires_at: datetime
    choice_made_at: Optional[datetime] = None
    chosen_index: Optional[int] = None
    
    class Config:
        populate_by_name = True

class MultiplayerTaskInvitation(BaseModel):
    """Invitation to join a multiplayer task."""
    invitation_id: str
    task_id: str
    task_type: str  # coop, competitive, pvp_moral
    task_title: str
    from_player_id: str
    from_player_name: str
    to_player_id: str
    to_player_name: str
    role: Optional[str] = None  # For co-op tasks
    status: str = "pending"  # pending, accepted, declined, expired
    created_at: datetime
    expires_at: datetime
    responded_at: Optional[datetime] = None

class MultiplayerTaskResult(BaseModel):
    """Result of completed multiplayer task."""
    task_id: str
    task_type: str
    completed_at: datetime
    success: bool
    participants: List[Dict[str, Any]]
    rewards_distributed: Dict[str, Dict[str, Any]]  # player_id -> rewards
    trait_changes: Dict[str, Dict[str, int]]  # player_id -> trait changes
    special_outcomes: Optional[List[str]] = None
