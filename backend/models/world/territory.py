"""Territory Model"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class TerritoryStatus(str, Enum):
    """Status of territory"""
    NEUTRAL = "neutral"
    CONTROLLED = "controlled"
    CONTESTED = "contested"
    SIEGE = "siege"


class ResourceType(str, Enum):
    """Types of territory resources"""
    CREDITS = "credits"
    TECH_PARTS = "tech_parts"
    RARE_MATERIALS = "rare_materials"
    ENERGY = "energy"
    DATA = "data"


class TerritoryEvent(BaseModel):
    """Regional event affecting territory"""
    event_id: str
    event_type: str
    name: str
    started_at: datetime
    ends_at: datetime
    is_active: bool = True


class TerritoryBattle(BaseModel):
    """Record of a territory battle"""
    battle_id: str
    attacker_guild_id: str
    attacker_guild_name: str
    defender_guild_id: Optional[str] = None
    defender_guild_name: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    winner: Optional[str] = None
    attacker_contribution: Dict[str, int] = Field(
        default_factory=dict)  # player_id: points
    defender_contribution: Dict[str, int] = Field(default_factory=dict)


class TerritoryModel(BaseModel):
    """
    Represents a territory in the game world
    Stored in MongoDB territories collection
    """

    # Identity
    territory_id: int = Field(..., description="Unique territory ID (1-20)")
    name: str = Field(..., description="Territory name")
    description: str = Field(..., description="Territory description")
    region: str = Field(...,
                        description="World region (north, south, east, west, central)")

    # Control
    status: TerritoryStatus = Field(
        default=TerritoryStatus.NEUTRAL, description="Current status")
    controlling_guild_id: Optional[str] = Field(
        default=None, description="Guild that controls territory")
    controlling_guild_name: Optional[str] = Field(
        default=None, description="Guild name for display")
    controlled_since: Optional[datetime] = Field(
        default=None, description="When control was established")
    control_duration_hours: float = Field(
        default=0.0, description="Total hours under current control")

    # Contest State
    contested: bool = Field(
        default=False, description="Is territory being contested")
    challenger_guild_id: Optional[str] = Field(
        default=None, description="Guild challenging for control")
    challenger_guild_name: Optional[str] = Field(
        default=None, description="Challenger name")
    contest_started: Optional[datetime] = Field(
        default=None, description="When contest began")

    # Population
    total_residents: int = Field(
        default=0, description="Players who set this as home")
    active_players: int = Field(
        default=0, description="Currently active players in territory")
    online_players: int = Field(
        default=0, description="Currently online in territory")

    # Karma & Alignment
    local_karma: float = Field(
        default=0.0, description="Combined karma of residents")
    average_karma: float = Field(
        default=0.0, description="Average karma of residents")
    karma_trend: str = Field(
        default="stable", description="rising, falling, stable")
    dominant_alignment: str = Field(
        default="neutral", description="good, neutral, evil")

    # Prosperity & Development
    prosperity_level: float = Field(
        default=50.0, description="0-100 prosperity score")
    development_level: int = Field(
        default=1, description="1-10 development tier")
    infrastructure: Dict[str, int] = Field(
        default_factory=lambda: {
            "barracks": 0,
            "markets": 0,
            "temples": 0,
            "workshops": 0,
            "walls": 0
        },
        description="Built infrastructure"
    )

    # Conflict
    conflict_level: float = Field(
        default=0.0, description="0-100 conflict intensity")
    total_battles: int = Field(
        default=0, description="Total battles fought here")
    recent_battles: List[TerritoryBattle] = Field(
        default_factory=list, description="Recent battle history")
    under_siege: bool = Field(
        default=False, description="Currently under siege")

    # Resources
    resources: Dict[str, int] = Field(
        default_factory=lambda: {
            "credits": 0,
            "tech_parts": 0,
            "rare_materials": 0,
            "energy": 0,
            "data": 0
        },
        description="Available resources"
    )
    resource_generation_rate: Dict[str, float] = Field(
        default_factory=lambda: {
            "credits": 10.0,
            "tech_parts": 5.0,
            "rare_materials": 2.0,
            "energy": 15.0,
            "data": 8.0
        },
        description="Hourly resource generation"
    )

    # Economy
    tax_rate: float = Field(
        default=0.1, description="Tax rate (0-1) on transactions")
    treasury: float = Field(
        default=0.0, description="Territory treasury (credits)")
    daily_income: float = Field(
        default=0.0, description="Daily income from taxes and resources")

    # Events
    active_events: List[TerritoryEvent] = Field(
        default_factory=list, description="Active regional events")
    last_event_type: Optional[str] = Field(
        default=None, description="Last event that occurred")
    last_event_time: Optional[datetime] = Field(
        default=None, description="When last event started")

    # Bonuses (from control/events)
    active_bonuses: Dict[str, float] = Field(
        default_factory=dict,
        description="Active bonuses (xp_boost, resource_mult, etc.)"
    )

    # Geographic
    coordinates: Dict[str, float] = Field(
        default_factory=lambda: {"x": 0.0, "y": 0.0},
        description="Territory center coordinates"
    )
    borders: List[int] = Field(
        default_factory=list, description="Adjacent territory IDs")
    area_size: float = Field(
        default=100.0, description="Territory size in game units")

    # Strategic Value
    strategic_value: int = Field(
        default=50, description="1-100 strategic importance")
    defensibility: int = Field(
        default=50, description="1-100 how easy to defend")
    resource_richness: int = Field(
        default=50, description="1-100 resource abundance")

    # History
    control_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of guild control changes"
    )
    total_control_changes: int = Field(
        default=0, description="How many times control changed")

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="When territory was created")
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Last update time")
    last_battle: Optional[datetime] = Field(
        default=None, description="Last battle time")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
