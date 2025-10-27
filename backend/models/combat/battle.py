"""Battle and combat challenge models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid


class Combatant(BaseModel):
    """Combatant in a battle."""
    player_id: str
    username: str
    hp: int
    max_hp: int
    action_points: int = 4
    max_action_points: int = 4
    attack: int
    defense: int
    evasion: int
    status_effects: List[Dict[str, Any]] = Field(default_factory=list)
    active_abilities: List[str] = Field(default_factory=list)


class CombatLogEntry(BaseModel):
    """Entry in combat log."""
    turn: int
    actor: str
    action: str
    target: Optional[str] = None
    result: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Battle(BaseModel):
    """Battle model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    battle_type: str  # duel, ambush, arena, guild_war
    status: str = "active"  # active, completed, fled

    combatants: List[Combatant]
    current_turn: int = 1
    current_actor_index: int = 0

    combat_log: List[CombatLogEntry] = Field(default_factory=list)

    winner: Optional[str] = None
    loser: Optional[str] = None

    rewards: Dict[str, Any] = Field(default_factory=dict)
    penalties: Dict[str, Any] = Field(default_factory=dict)

    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None

    # Additional metadata
    guild_war_id: Optional[str] = None
    territory_id: Optional[int] = None
    arena_match_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "battle-123",
                "battle_type": "duel",
                "status": "active",
                "combatants": [
                    {
                        "player_id": "player1",
                        "username": "Warrior1",
                        "hp": 100,
                        "max_hp": 100,
                        "action_points": 4,
                        "attack": 50,
                        "defense": 30,
                        "evasion": 20
                    }
                ],
                "current_turn": 1,
                "current_actor_index": 0
            }
        }


class CombatChallenge(BaseModel):
    """Combat challenge model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    challenger_id: str
    challenger_username: str
    target_id: str
    target_username: str
    combat_type: str = "duel"
    status: str = "pending"  # pending, accepted, declined, expired
    message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    battle_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "challenge-123",
                "challenger_id": "player1",
                "target_id": "player2",
                "combat_type": "duel",
                "status": "pending"
            }
        }
