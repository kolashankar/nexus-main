"""Seasonal content API schemas."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class BattlePassTierResponse(BaseModel):
    """Battle pass tier information."""
    tier: int
    xp_required: int
    free_rewards: List[Dict[str, Any]]
    premium_rewards: List[Dict[str, Any]]
    is_locked: bool

    class Config:
        from_attributes = True


class BattlePassResponse(BaseModel):
    """Battle pass information."""
    pass_id: str
    season: int
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    is_active: bool
    total_tiers: int
    free_tiers: int
    premium_tiers: int
    premium_price: int
    tiers: List[Dict[str, Any]]

    class Config:
        from_attributes = True


class PlayerBattlePassProgressResponse(BaseModel):
    """Player's battle pass progress."""
    player_id: str
    pass_id: str
    season: int
    has_premium: bool
    current_tier: int
    current_xp: int
    claimed_free_rewards: List[int]
    claimed_premium_rewards: List[int]
    total_xp_earned: int

    class Config:
        from_attributes = True


class ClaimRewardsRequest(BaseModel):
    """Request to claim rewards for a tier."""
    tier: int = Field(..., ge=1, le=100)


class ClaimRewardsResponse(BaseModel):
    """Response after claiming rewards."""
    tier: int
    rewards_claimed: List[Dict[str, Any]]


class SeasonResponse(BaseModel):
    """Season information."""
    season_id: str
    season_number: int
    name: str
    description: str
    theme: str
    start_date: datetime
    end_date: datetime
    status: str
    duration_days: int
    battle_pass_id: Optional[str]
    total_players: int
    active_players: int

    class Config:
        from_attributes = True


class PlayerSeasonProgressResponse(BaseModel):
    """Player's season progress."""
    player_id: str
    season_id: str
    season_number: int
    karma_rank: Optional[int]
    wealth_rank: Optional[int]
    combat_rank: Optional[int]
    achievement_rank: Optional[int]
    season_karma_earned: int
    season_wealth_earned: int
    season_combat_wins: int
    season_achievements: int
    season_quests_completed: int
    days_active: int

    class Config:
        from_attributes = True
