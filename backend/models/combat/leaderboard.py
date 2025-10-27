from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class LeaderboardEntry(BaseModel):
    """Entry in a combat leaderboard"""
    rank: int
    player_id: str
    username: str
    combat_rating: int = 1500
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    current_streak: int = 0
    highest_rating: int = 1500


class Leaderboard(BaseModel):
    """Combat leaderboard"""
    leaderboard_type: str  # arena, duel, tournament
    season: int
    entries: List[LeaderboardEntry] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "leaderboard_type": "arena",
                "season": 1,
                "entries": [
                    {
                        "rank": 1,
                        "player_id": "player-123",
                        "username": "ChampionPlayer",
                        "combat_rating": 2100,
                        "wins": 50,
                        "losses": 10,
                        "win_rate": 83.3,
                        "current_streak": 8
                    }
                ]
            }
        }
