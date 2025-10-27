"""Tournaments API schemas."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class TournamentMatchResponse(BaseModel):
    """Tournament match information."""
    match_id: str
    round_number: int
    bracket_position: int
    player1_id: Optional[str]
    player2_id: Optional[str]
    winner_id: Optional[str]
    score: Optional[Dict[str, int]]
    status: str

    class Config:
        from_attributes = True


class TournamentResponse(BaseModel):
    """Tournament information."""
    tournament_id: str
    name: str
    description: str
    tournament_type: str
    status: str
    registration_start: datetime
    registration_end: datetime
    start_time: datetime
    end_time: Optional[datetime]
    bracket_type: str
    max_participants: int
    min_participants: int
    min_level: Optional[int]
    min_karma: Optional[int]
    entry_fee: int
    total_registered: int
    prize_pool: int
    current_round: int
    total_rounds: int

    class Config:
        from_attributes = True


class TournamentListResponse(BaseModel):
    """List of tournaments."""
    tournaments: List[TournamentResponse]
    total: int


class RegisterTournamentRequest(BaseModel):
    """Request to register for tournament."""
    tournament_id: str = Field(..., description="Tournament to register for")


class CreateTournamentRequest(BaseModel):
    """Request to create a tournament."""
    name: str
    description: str = ""
    tournament_type: str
    start_time: datetime
    max_participants: int = 64
    min_participants: int = 8
    entry_fee: int = 0
    prize_pool: int = 0
