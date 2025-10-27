"""Duel schemas."""

from pydantic import BaseModel, Field
from typing import Optional


class DuelChallengeRequest(BaseModel):
    """Request to challenge to a duel."""
    target_id: str = Field(..., description="ID of player to challenge")
    target_username: str = Field(..., description="Username of target")
    message: Optional[str] = Field(
        None, description="Optional challenge message")
