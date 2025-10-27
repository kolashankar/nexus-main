"""Robot model."""

from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import uuid


class Robot(BaseModel):
    """Robot model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    robot_type: str  # harvester, trader, guardian, etc.
    name: str
    owner_id: str

    # Progression
    level: int = 1
    experience: int = 0

    # Stats (vary by type)
    stats: Dict[str, int] = Field(default_factory=dict)
    abilities: List[str] = Field(default_factory=list)

    # Status
    status: str = "idle"  # idle, working, training, combat, maintenance
    loyalty: int = 100  # 0-100, can decrease if mistreated

    # Usage tracking
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: Optional[datetime] = None
    total_tasks: int = 0

    # Personality (develops over time)
    personality_traits: Dict[str, int] = Field(default_factory=dict)

    # Equipment/Upgrades
    installed_chips: List[str] = Field(default_factory=list)
    upgrades: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "robot-123",
                "robot_type": "guardian",
                "name": "Defender-01",
                "owner_id": "player-123",
                "level": 5,
                "experience": 250,
                "stats": {
                    "attack": 60,
                    "defense": 90,
                    "speed": 40,
                    "intelligence": 50
                },
                "abilities": ["shield", "guard"],
                "status": "idle",
                "loyalty": 95
            }
        }


class RobotChip(BaseModel):
    """Robot upgrade chip."""
    chip_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    chip_type: str  # combat, utility, economic
    rarity: str  # common, rare, epic, legendary

    # Effects
    stat_bonuses: Dict[str, int] = Field(default_factory=dict)
    ability_unlocks: List[str] = Field(default_factory=list)

    price: int

    class Config:
        json_schema_extra = {
            "example": {
                "chip_id": "chip-123",
                "name": "Combat Optimizer",
                "description": "Increases attack by 20%",
                "chip_type": "combat",
                "rarity": "rare",
                "stat_bonuses": {"attack": 20},
                "price": 5000
            }
        }
