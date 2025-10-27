"""Tournament model."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class TournamentType(str, Enum):
    """Types of tournaments."""
    PVP_COMBAT = "pvp_combat"
    ROBOT_BATTLE = "robot_battle"
    TRADING_COMPETITION = "trading_competition"
    QUEST_SPEEDRUN = "quest_speedrun"
    CREATIVITY_CONTEST = "creativity_contest"


class TournamentStatus(str, Enum):
    """Tournament status."""
    UPCOMING = "upcoming"
    REGISTRATION = "registration"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BracketType(str, Enum):
    """Tournament bracket types."""
    SINGLE_ELIMINATION = "single_elimination"
    DOUBLE_ELIMINATION = "double_elimination"
    ROUND_ROBIN = "round_robin"
    SWISS = "swiss"


class TournamentMatch(BaseModel):
    """Single match in a tournament."""
    match_id: str
    round_number: int
    bracket_position: int
    player1_id: Optional[str] = None
    player2_id: Optional[str] = None
    winner_id: Optional[str] = None
    score: Optional[Dict[str, int]] = None
    status: str = "pending"  # pending, in_progress, completed
    scheduled_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class Tournament(BaseModel):
    """Tournament model."""
    tournament_id: str = Field(..., description="Unique tournament ID")
    name: str
    description: str = ""
    tournament_type: TournamentType

    # Status
    status: TournamentStatus = TournamentStatus.UPCOMING

    # Timing
    registration_start: datetime
    registration_end: datetime
    start_time: datetime
    end_time: Optional[datetime] = None

    # Structure
    bracket_type: BracketType = BracketType.SINGLE_ELIMINATION
    max_participants: int = Field(
        default=64, description="Maximum number of participants")
    min_participants: int = Field(
        default=8, description="Minimum participants to start")

    # Requirements
    min_level: Optional[int] = Field(None, description="Minimum player level")
    min_karma: Optional[int] = Field(
        None, description="Minimum karma requirement")
    entry_fee: int = Field(default=0, description="Credits required to enter")

    # Participants
    registered_players: List[str] = Field(default_factory=list)
    total_registered: int = 0

    # Bracket
    matches: List[TournamentMatch] = Field(default_factory=list)
    current_round: int = 0
    total_rounds: int = 0

    # Rewards
    prize_pool: int = 0
    rewards: Dict[int, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Rewards by placement (1st, 2nd, 3rd, etc.)"
    )

    # Season
    season_id: Optional[str] = None

    # Metadata
    created_by: str = Field(default="system")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class TournamentParticipant(BaseModel):
    """Tournament participant information."""
    tournament_id: str
    player_id: str
    registration_time: datetime
    checked_in: bool = False
    current_match_id: Optional[str] = None
    wins: int = 0
    losses: int = 0
    placement: Optional[int] = None
    eliminated: bool = False

    class Config:
        from_attributes = True
