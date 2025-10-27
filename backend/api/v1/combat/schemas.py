"""Combat API schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChallengeRequest(BaseModel):
    """Request to challenge a player."""
    target_id: str = Field(..., description="ID of player to challenge")
    combat_type: str = Field(
        default="duel", description="Type of combat (duel, ambush, arena)")


class ChallengeResponse(BaseModel):
    """Response for challenge creation."""
    challenge_id: str
    status: str
    message: str


class AcceptChallengeRequest(BaseModel):
    """Request to accept a challenge."""
    challenge_id: str = Field(...,
                              description="ID of challenge to accept/decline")


class CombatActionRequest(BaseModel):
    """Request to perform a combat action."""
    battle_id: str = Field(..., description="ID of the battle")
    action_type: str = Field(
        ..., description="Type of action (attack, defend, use_power, use_item, flee)")
    target: Optional[str] = Field(None, description="Target of the action")
    ability_id: Optional[str] = Field(None, description="ID of ability to use")


class FleeRequest(BaseModel):
    """Request to flee from combat."""
    battle_id: str = Field(..., description="ID of the battle")


class CombatantState(BaseModel):
    """State of a combatant."""
    player_id: str
    username: str
    hp: int
    max_hp: int
    action_points: int
    max_action_points: int = 4
    attack: int
    defense: int
    evasion: int
    status_effects: List[Dict[str, Any]] = []
    active_abilities: List[str] = []


class CombatStateResponse(BaseModel):
    """Current state of combat."""
    battle_id: str
    status: str  # active, completed, fled
    combat_type: str
    current_turn: int
    current_actor: str
    combatants: List[CombatantState]
    combat_log: List[Dict[str, Any]]
    winner: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None


class CombatResultSchema(BaseModel):
    """Result of a combat action."""
    success: bool
    action_type: str
    damage: Optional[int] = None
    healing: Optional[int] = None
    effects_applied: List[str] = []
    message: str
    combat_log_entry: Dict[str, Any]
