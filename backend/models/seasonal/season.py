"""Season model."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class SeasonStatus(str, Enum):
    """Season status."""
    UPCOMING = "upcoming"
    ACTIVE = "active"
    ENDING = "ending"
    ENDED = "ended"


class Season(BaseModel):
    """Season model."""
    season_id: str = Field(..., description="Unique season ID")
    season_number: int = Field(..., ge=1, description="Season number")
    name: str = Field(..., description="Season name")
    description: str = Field(default="")
    theme: str = Field(default="default", description="Season theme")

    # Timing
    start_date: datetime
    end_date: datetime
    status: SeasonStatus = SeasonStatus.UPCOMING

    # Duration in days
    duration_days: int = Field(
        default=90, description="Season duration in days")

    # Content
    exclusive_quests: List[str] = Field(default_factory=list)
    exclusive_items: List[str] = Field(default_factory=list)
    exclusive_superpowers: List[str] = Field(default_factory=list)

    # Battle Pass
    battle_pass_id: Optional[str] = None

    # Events
    special_events: List[Dict[str, Any]] = Field(default_factory=list)

    # Rewards
    season_end_rewards: Dict[str, Any] = Field(default_factory=dict)

    # Leaderboards
    leaderboard_rewards: Dict[str, List[Dict[str, Any]]] = Field(
        default_factory=dict,
        description="Rewards for top players in each leaderboard"
    )

    # Statistics
    total_players: int = Field(default=0)
    active_players: int = Field(default=0)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class PlayerSeasonProgress(BaseModel):
    """Player's progress in a season."""
    player_id: str
    season_id: str
    season_number: int

    # Rankings
    karma_rank: Optional[int] = None
    wealth_rank: Optional[int] = None
    combat_rank: Optional[int] = None
    achievement_rank: Optional[int] = None

    # Stats
    season_karma_earned: int = Field(default=0)
    season_wealth_earned: int = Field(default=0)
    season_combat_wins: int = Field(default=0)
    season_achievements: int = Field(default=0)
    season_quests_completed: int = Field(default=0)

    # Exclusive unlocks
    exclusive_items_unlocked: List[str] = Field(default_factory=list)
    exclusive_quests_completed: List[str] = Field(default_factory=list)

    # Rewards
    rewards_claimed: bool = Field(default=False)
    end_of_season_rewards: List[Dict[str, Any]] = Field(default_factory=list)

    # Participation
    first_login: Optional[datetime] = None
    last_login: Optional[datetime] = None
    days_active: int = Field(default=0)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class SeasonReset(BaseModel):
    """Season reset configuration."""
    reset_id: str
    season_from: int
    season_to: int
    reset_date: datetime

    # What resets
    reset_karma: bool = Field(default=False)
    reset_traits: bool = Field(default=False)
    reset_wealth: bool = Field(default=False)
    reset_achievements: bool = Field(default=False)

    # What carries over
    carry_over_percentage: Dict[str, float] = Field(
        default_factory=lambda: {
            "karma": 0.0,
            "wealth": 0.1,  # Carry over 10% of wealth
            "traits": 0.0
        }
    )

    # Legacy rewards
    legacy_points_awarded: Dict[str, int] = Field(
        default_factory=dict,
        description="Legacy points awarded to players based on ranks"
    )

    # Statistics
    players_affected: int = Field(default=0)
    reset_completed: bool = Field(default=False)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True
