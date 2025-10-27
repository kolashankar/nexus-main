"""Schemas for The Architect AI"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of world events"""
    # Positive karma events
    GOLDEN_AGE = "golden_age"
    DIVINE_BLESSING = "divine_blessing"
    FESTIVAL_OF_LIGHT = "festival_of_light"
    THE_CONVERGENCE = "the_convergence"

    # Negative karma events
    THE_PURGE = "the_purge"
    ECONOMIC_COLLAPSE = "economic_collapse"
    DARK_ECLIPSE = "dark_eclipse"
    JUDGMENT_DAY = "judgment_day"

    # Neutral events
    METEOR_SHOWER = "meteor_shower"
    GLITCH_IN_MATRIX = "glitch_in_matrix"
    ROBOT_UPRISING = "robot_uprising"
    TIME_ANOMALY = "time_anomaly"

    # Regional events
    REGIONAL_PROSPERITY = "regional_prosperity"
    REGIONAL_CONFLICT = "regional_conflict"
    RESOURCE_DISCOVERY = "resource_discovery"
    TERRITORY_SHIFT = "territory_shift"


class EventSeverity(str, Enum):
    """Event impact severity"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WorldState(BaseModel):
    """Current state of the world"""
    collective_karma: float = Field(
        default=0.0, description="Total karma of all players")
    average_karma: float = Field(
        default=0.0, description="Average karma per player")
    karma_trend: str = Field(
        default="stable", description="Trend: rising, falling, stable")
    total_players: int = Field(default=0, description="Total active players")
    online_players: int = Field(
        default=0, description="Currently online players")
    total_actions_24h: int = Field(
        default=0, description="Actions in last 24h")
    positive_actions_24h: int = Field(
        default=0, description="Positive actions")
    negative_actions_24h: int = Field(
        default=0, description="Negative actions")
    guild_wars_active: int = Field(default=0, description="Active guild wars")
    territories_contested: int = Field(
        default=0, description="Contested territories")
    market_health: str = Field(default="stable", description="Economy health")
    last_global_event: Optional[str] = Field(
        default=None, description="Last global event type")
    time_since_last_event: Optional[float] = Field(
        default=None, description="Hours since last event")


class TerritoryState(BaseModel):
    """State of a specific territory"""
    territory_id: int
    name: str
    controlling_guild_id: Optional[str] = None
    guild_name: Optional[str] = None
    contested: bool = False
    population: int = 0
    local_karma: float = 0.0
    prosperity_level: float = 50.0  # 0-100
    conflict_level: float = 0.0  # 0-100
    resources: Dict[str, int] = Field(default_factory=dict)


class WorldEventRequest(BaseModel):
    """Request to generate a world event"""
    world_state: WorldState
    territories: List[TerritoryState] = Field(default_factory=list)
    force_event_type: Optional[EventType] = None
    target_territory: Optional[int] = None
    triggered_by: str = "automatic"  # "automatic", "admin", "karma_threshold"
    context: Optional[str] = None


class EventEffect(BaseModel):
    """Effects of an event"""
    effect_type: str  # "karma_multiplier", "xp_boost", "resource_spawn", etc.
    value: float
    affected_players: str = "all"  # "all", "territory", "guild", "alignment"
    duration_hours: float = 24.0
    description: str


class WorldEventResponse(BaseModel):
    """Generated world event"""
    event_id: str
    event_type: EventType
    severity: EventSeverity
    name: str
    description: str
    lore: str  # Rich narrative description
    effects: List[EventEffect]
    duration_hours: float

    # Targeting
    is_global: bool = True
    affected_territories: List[int] = Field(default_factory=list)

    # Participation
    requires_participation: bool = False
    participation_mechanics: Optional[str] = None
    participation_rewards: Optional[Dict[str, Any]] = None

    # Metadata
    trigger_reason: str
    karma_threshold: Optional[float] = None
    collective_karma: float
    estimated_impact: str  # "low", "medium", "high", "world_changing"

    # AI reasoning
    architect_reasoning: str
    alternative_events_considered: List[str] = Field(default_factory=list)

    # Generation metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    cached: bool = False


class EventTriggerCondition(BaseModel):
    """Conditions for triggering an event"""
    condition_type: str  # "karma_threshold", "time_since_last", "player_action_ratio"
    threshold: float
    comparison: str = "greater_than"  # "greater_than", "less_than", "equals"
    met: bool = False
    current_value: Optional[float] = None


class TriggerEvaluation(BaseModel):
    """Evaluation of whether to trigger an event"""
    should_trigger: bool
    confidence: float  # 0-1
    event_type_suggestion: Optional[EventType] = None
    severity_suggestion: EventSeverity = EventSeverity.MEDIUM
    conditions_met: List[EventTriggerCondition]
    reasoning: str
    urgency: str = "normal"  # "low", "normal", "high", "critical"
