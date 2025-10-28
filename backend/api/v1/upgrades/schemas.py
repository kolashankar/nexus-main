from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

"""
Upgrade API Schemas
Request and response models for upgrade endpoints
"""

class TraitUpgradeRequest(BaseModel):
    """Request to upgrade a trait"""
    trait_id: str = Field(..., description="ID of the trait to upgrade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "trait_id": "strength"
            }
        }


class RobotUpgradeRequest(BaseModel):
    """Request to upgrade a robot"""
    robot_id: str = Field(..., description="ID of the robot to upgrade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "robot_id": "combat"
            }
        }


class OrnamentUpgradeRequest(BaseModel):
    """Request to upgrade an ornament"""
    ornament_id: str = Field(..., description="ID of the ornament to upgrade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ornament_id": "avatar_frame"
            }
        }


class ChipUpgradeRequest(BaseModel):
    """Request to upgrade a chip"""
    chip_id: str = Field(..., description="ID of the chip to upgrade")
    
    class Config:
        json_schema_extra = {
            "example": {
                "chip_id": "neural_enhancer"
            }
        }


class UpgradeResponse(BaseModel):
    """Generic upgrade response"""
    success: bool = True
    message: str
    upgrade_type: str
    item_id: str
    old_level: int
    new_level: int
    cost: Dict[str, int]
    remaining_currencies: Dict[str, int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Strength upgraded successfully",
                "upgrade_type": "trait",
                "item_id": "strength",
                "old_level": 50,
                "new_level": 51,
                "cost": {
                    "credits": 2500,
                    "karma_tokens": 250,
                    "dark_matter": 25
                },
                "remaining_currencies": {
                    "credits": 7500,
                    "karma_tokens": 750,
                    "dark_matter": 75
                },
                "timestamp": "2025-01-15T10:30:00"
            }
        }


class UpgradeHistoryResponse(BaseModel):
    """Upgrade history entry"""
    player_id: str
    upgrade_type: str
    item_id: str
    item_name: str
    old_level: int
    new_level: int
    cost: Dict[str, int]
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
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


class UpgradeStatsResponse(BaseModel):
    """Player upgrade statistics"""
    total_upgrades: int
    upgrades_by_type: Dict[str, int]
    total_spent: Dict[str, int]
    highest_level_items: Dict[str, Dict[str, any]]
    
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
