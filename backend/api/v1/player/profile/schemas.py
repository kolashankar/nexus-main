"""Player profile schemas."""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime


class PlayerProfileResponse(BaseModel):
    """Player profile response schema."""
    _id: str = Field(alias='_id')
    username: str
    email: Optional[str] = None
    level: int
    xp: int
    prestige_level: int = 0
    economic_class: str
    moral_class: str
    currencies: Dict[str, int]
    karma_points: Optional[int]
    traits: Dict[str, int]
    meta_traits: Dict[str, int]
    superpowers: List[Dict[str, Any]] = []
    visibility: Dict[str, Any] = {}
    stats: Dict[str, int] = {}
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            'example': {
                '_id': '507f1f77bcf86cd799439011',
                'username': 'NexusWarrior',
                'level': 25,
                'xp': 62500,
                'prestige_level': 0,
                'economic_class': 'middle',
                'moral_class': 'good',
                'currencies': {
                    'credits': 10000,
                    'karma_tokens': 50
                },
                'karma_points': 350,
                'traits': {
                    'empathy': 75,
                    'courage': 80,
                    'hacking': 65
                },
                'meta_traits': {
                    'reputation': 70,
                    'combat_rating': 60
                },
                'created_at': '2025-01-15T10:30:00Z'
            }
        }


class ProfileUpdateRequest(BaseModel):
    """Request to update player profile."""
    bio: Optional[str] = Field(
        None, max_length=500, description='Player biography')
    active_title: Optional[str] = Field(
        None, description='Active display title')
    appearance: Optional[Dict[str, Any]] = Field(
        None, description='Appearance customization')
    cosmetics: Optional[Dict[str, Any]] = Field(
        None, description='Equipped cosmetics')

    class Config:
        json_schema_extra = {
            'example': {
                'bio': 'A skilled hacker seeking redemption...',
                'active_title': 'The Redeemed',
                'appearance': {
                    'hair_color': '#FF5733',
                    'skin_tone': 'medium'
                }
            }
        }


class StatsResponse(BaseModel):
    """Player stats response schema."""
    player_id: str
    username: str
    level: int
    combat_stats: Dict[str, Any]
    derived_traits: Dict[str, Any]
    level_progress: Dict[str, Any]

    class Config:
        json_schema_extra = {
            'example': {
                'player_id': '507f1f77bcf86cd799439011',
                'username': 'NexusWarrior',
                'level': 25,
                'combat_stats': {
                    'hp': 750,
                    'max_hp': 750,
                    'attack': 85,
                    'defense': 75,
                    'evasion': 40,
                    'crit_chance': 18
                },
                'derived_traits': {
                    'reputation': 70,
                    'influence': 65,
                    'trustworthiness': 75
                },
                'level_progress': {
                    'level': 25,
                    'xp': 62500,
                    'xp_needed_for_next': 5100,
                    'level_progress_percentage': 75.5
                }
            }
        }


class OnlinePlayersResponse(BaseModel):
    """Online players response schema."""
    total_online: int
    players: List[Dict[str, Any]]

    class Config:
        json_schema_extra = {
            'example': {
                'total_online': 42,
                'players': [
                    {
                        'player_id': '507f1f77bcf86cd799439011',
                        'username': 'NexusWarrior',
                        'level': 25,
                        'moral_class': 'good',
                        'online_status': 'online'
                    }
                ]
            }
        }
