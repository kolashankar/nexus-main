"""Combat statistics model."""

from datetime import datetime
from typing import Dict
from pydantic import BaseModel, Field


class CombatStats(BaseModel):
    """Player combat statistics."""
    player_id: str

    # Base combat stats (derived from traits)
    hp: int
    max_hp: int
    attack: int
    defense: int
    evasion: int
    crit_chance: float

    # Combat history
    total_battles: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    fled: int = 0

    # PvP specific
    pvp_wins: int = 0
    pvp_losses: int = 0
    pvp_rating: int = 1000  # Elo rating

    # Arena stats
    arena_wins: int = 0
    arena_losses: int = 0
    arena_rank: int = 0
    arena_tier: str = "Bronze"

    # Guild war stats
    guild_war_kills: int = 0
    guild_war_deaths: int = 0
    territories_captured: int = 0

    # Damage stats
    total_damage_dealt: int = 0
    total_damage_taken: int = 0
    highest_damage: int = 0

    # Ability usage
    abilities_used: Dict[str, int] = Field(default_factory=dict)

    # Combat abilities unlocked
    unlocked_abilities: list = Field(default_factory=list)

    # Achievements
    combat_achievements: list = Field(default_factory=list)

    # Streak tracking
    current_win_streak: int = 0
    best_win_streak: int = 0

    last_battle: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player-123",
                "hp": 100,
                "max_hp": 100,
                "attack": 50,
                "defense": 30,
                "evasion": 20,
                "crit_chance": 0.15,
                "total_battles": 50,
                "wins": 30,
                "losses": 15,
                "pvp_rating": 1200
            }
        }

    def calculate_win_rate(self) -> float:
        """Calculate win rate percentage."""
        if self.total_battles == 0:
            return 0.0
        return (self.wins / self.total_battles) * 100

    def update_rating(self, won: bool, opponent_rating: int, k_factor: int = 32):
        """Update Elo rating after a match."""
        expected = 1 / (1 + 10 ** ((opponent_rating - self.pvp_rating) / 400))
        actual = 1.0 if won else 0.0
        self.pvp_rating += int(k_factor * (actual - expected))
