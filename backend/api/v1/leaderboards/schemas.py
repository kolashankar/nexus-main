"""Leaderboards API schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional


class LeaderboardEntryResponse(BaseModel):
    """Single leaderboard entry."""
    rank: int
    player_id: str
    username: str
    value: float = Field(...,
                         description="The value being ranked (karma, wealth, etc.)")
    level: Optional[int] = None
    guild_name: Optional[str] = None
    title: Optional[str] = None
    change_24h: Optional[int] = Field(
        None, description="Change in rank over last 24h")

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Leaderboard response."""
    leaderboard_type: str
    entries: List[LeaderboardEntryResponse]
    total_entries: int
    last_updated: Optional[str] = None
    season_id: Optional[str] = None

    class Config:
        from_attributes = True


class PlayerRankResponse(BaseModel):
    """Player's rank information."""
    player_id: str
    username: str
    leaderboard_type: str
    rank: int
    value: float
    percentile: float = Field(..., description="Percentile ranking (0-100)")
    total_players: int
    change_24h: Optional[int] = None

    class Config:
        from_attributes = True
