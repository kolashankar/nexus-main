"""Action cooldown model."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ActionCooldown(BaseModel):
    """Action cooldown model."""

    player_id: str = Field(..., description='Player ID')
    action_type: str = Field(..., description='Type of action on cooldown')
    set_at: datetime = Field(
        default_factory=datetime.utcnow, description='When cooldown was set')
    expires_at: datetime = Field(..., description='When cooldown expires')
    duration_seconds: int = Field(...,
                                  description='Cooldown duration in seconds')

    class Config:
        json_schema_extra = {
            'example': {
                'player_id': '507f1f77bcf86cd799439011',
                'action_type': 'hack',
                'set_at': '2025-01-15T10:30:00Z',
                'expires_at': '2025-01-15T10:35:00Z',
                'duration_seconds': 300
            }
        }


class CooldownStatus(BaseModel):
    """Cooldown status response."""

    on_cooldown: bool = Field(..., description='Whether action is on cooldown')
    can_perform: bool = Field(...,
                              description='Whether action can be performed')
    expires_at: Optional[datetime] = Field(
        None, description='When cooldown expires')
    remaining_seconds: int = Field(0, description='Seconds remaining')
    remaining_minutes: float = Field(0.0, description='Minutes remaining')

    class Config:
        json_schema_extra = {
            'example': {
                'on_cooldown': True,
                'can_perform': False,
                'expires_at': '2025-01-15T10:35:00Z',
                'remaining_seconds': 180,
                'remaining_minutes': 3.0
            }
        }
