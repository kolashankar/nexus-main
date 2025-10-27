"""Arena schemas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class JoinQueueRequest(BaseModel):
    """Request to join arena queue."""
    rating: Optional[int] = Field(
        None, description="Player's current rating (auto-fetched if not provided)")


class ArenaMatchResponse(BaseModel):
    """Response when arena match is found."""
    status: str
    message: str
    battle_id: Optional[str] = None
    opponent: Optional[Dict[str, Any]] = None
    queue_position: Optional[int] = None
