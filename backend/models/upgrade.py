from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid

"""
Upgrade Models
Handles all upgrade-related data structures
"""

class UpgradeBase(BaseModel):
    """Base upgrade model"""
    upgrade_type: str = Field(..., description="Type of upgrade: trait, robot, ornament, chip")
    item_id: str = Field(..., description="ID of the item being upgraded")
    

class UpgradeCreate(UpgradeBase):
    """Model for creating a new upgrade"""
    player_id: str = Field(..., description="UUID of the player")


class UpgradeResponse(BaseModel):
    """Response model after successful upgrade"""
    success: bool = True
    message: str
    upgrade_type: str
    item_id: str
    old_level: int
    new_level: int
    cost: Dict[str, int]
    remaining_currencies: Dict[str, int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class UpgradeHistory(BaseModel):
    """Upgrade history entry"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    player_id: str
    upgrade_type: str
    item_id: str
    item_name: str
    old_level: int
    new_level: int
    cost: Dict[str, int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "player_id": "123e4567-e89b-12d3-a456-426614174000",
                "upgrade_type": "trait",
                "item_id": "strength",
                "item_name": "Strength",
                "old_level": 50,
                "new_level": 51,
                "cost": {
                    "credits": 2500,
                    "karma_tokens": 250,
                    "dark_matter": 25
                },
                "timestamp": "2025-01-15T10:30:00"
            }
        }


class UpgradeStats(BaseModel):
    """Player upgrade statistics"""
    total_upgrades: int = 0
    upgrades_by_type: Dict[str, int] = Field(default_factory=dict)
    total_spent: Dict[str, int] = Field(default_factory=lambda: {
        "credits": 0,
        "karma_tokens": 0,
        "dark_matter": 0
    })
    highest_level_items: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    recent_upgrades: list = Field(default_factory=list)
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_upgrades": 145,
                "upgrades_by_type": {
                    "trait": 60,
                    "robot": 35,
                    "ornament": 25,
                    "chip": 25
                },
                "total_spent": {
                    "credits": 125000,
                    "karma_tokens": 12500,
                    "dark_matter": 1250
                },
                "highest_level_items": {
                    "strength": {"level": 75, "type": "trait"},
                    "combat_bot": {"level": 60, "type": "robot"}
                }
            }
        }


class PlayerUpgrades(BaseModel):
    """Complete player upgrade data"""
    player_id: str
    traits: Dict[str, int] = Field(default_factory=dict)
    robots: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    ornaments: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    chips: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    upgrade_history: list = Field(default_factory=list)
    stats: UpgradeStats = Field(default_factory=UpgradeStats)
    
    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "123e4567-e89b-12d3-a456-426614174000",
                "traits": {
                    "strength": 50,
                    "hacking": 45,
                    "charisma": 30
                },
                "robots": {
                    "scout": {"level": 25, "unlocked": True},
                    "combat": {"level": 40, "unlocked": True}
                },
                "ornaments": {
                    "avatar_frame": {"level": 15, "unlocked": True}
                },
                "chips": {
                    "neural_enhancer": {"level": 35, "unlocked": True}
                }
            }
        }
