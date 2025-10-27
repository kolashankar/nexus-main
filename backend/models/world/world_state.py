"""World State Model"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class WorldStateModel(BaseModel):
    """
    Represents the current global state of the game world
    Stored in MongoDB world_state collection (singleton document)
    """

    # Global Karma
    collective_karma: float = Field(
        default=0.0, description="Total karma of all players")
    average_karma: float = Field(
        default=0.0, description="Average karma per player")
    karma_trend: str = Field(
        default="stable", description="rising, falling, or stable")
    karma_history: list[Dict[str, Any]] = Field(
        default_factory=list, description="24h karma snapshots")


class GlobalKarma(BaseModel):
    """Global karma statistics."""
    collective_karma: float = Field(default=0.0, description="Total karma of all players")
    average_karma: float = Field(default=0.0, description="Average karma per player")
    karma_trend: str = Field(default="stable", description="rising, falling, or stable")
    positive_actions_24h: int = Field(default=0, description="Positive actions in 24h")
    negative_actions_24h: int = Field(default=0, description="Negative actions in 24h")


class WorldState(WorldStateModel):
    """Alias for WorldStateModel for backward compatibility."""
    pass

    # Player Statistics
    total_players: int = Field(
        default=0, description="Total registered players")
    active_players_24h: int = Field(
        default=0, description="Players active in last 24h")
    online_players: int = Field(
        default=0, description="Currently online players")

    # Action Statistics
    total_actions_24h: int = Field(
        default=0, description="Total actions in last 24h")
    positive_actions_24h: int = Field(
        default=0, description="Positive actions (help, donate)")
    negative_actions_24h: int = Field(
        default=0, description="Negative actions (steal, hack)")
    neutral_actions_24h: int = Field(
        default=0, description="Neutral actions (trade)")

    # World Conflicts
    guild_wars_active: int = Field(default=0, description="Active guild wars")
    territories_contested: int = Field(
        default=0, description="Territories being fought over")
    total_guilds: int = Field(default=0, description="Total active guilds")

    # Economy
    total_wealth: float = Field(
        default=0.0, description="Total credits in circulation")
    market_health: str = Field(
        default="stable", description="stable, boom, crash, volatile")
    inflation_rate: float = Field(
        default=0.0, description="Daily inflation rate")

    # Active Events
    active_global_event: Optional[Dict[str, Any]] = Field(
        default=None, description="Current global event")
    last_global_event_type: Optional[str] = Field(
        default=None, description="Last event type")
    last_global_event_time: Optional[datetime] = Field(
        default=None, description="When last event started")
    last_global_event_ended: Optional[datetime] = Field(
        default=None, description="When last event ended")

    # Regional Events
    active_regional_events: list[str] = Field(
        default_factory=list, description="List of active regional event IDs")

    # Season Information
    current_season: int = Field(default=1, description="Current season number")
    season_start: datetime = Field(
        default_factory=datetime.utcnow, description="Season start date")
    season_end: Optional[datetime] = Field(
        default=None, description="Season end date")

    # AI Pantheon Activity
    ai_pantheon_state: Dict[str, Any] = Field(
        default_factory=lambda: {
            "karma_arbiter_last_active": None,
            "oracle_last_quest": None,
            "economist_last_update": None,
            "warlord_last_action": None,
            "architect_last_event": None,
            "architect_next_check": None
        },
        description="Tracking AI agent activity"
    )

    # System Metrics
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description="Last state update")
    last_full_sync: datetime = Field(
        default_factory=datetime.utcnow, description="Last complete data sync")
    update_count: int = Field(
        default=0, description="Number of updates since last sync")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }
