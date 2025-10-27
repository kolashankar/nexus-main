"""World & Events API routes."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from backend.api.deps import get_current_player
from backend.models.player.player import Player
from backend.services.world.events import WorldEventsService
from backend.services.world.karma_tracker import GlobalKarmaTracker
from .schemas import (
    WorldStateResponse,
    WorldEventResponse,
    RegionalEventResponse,
    GlobalKarmaResponse,
    TriggerEventRequest,
    EventResponseRequest
)

router = APIRouter(prefix="/world", tags=["world"])


@router.get("/state", response_model=WorldStateResponse)
async def get_world_state(
    current_player: Player = Depends(get_current_player)
):
    """Get current world state."""
    events_service = WorldEventsService()
    return await events_service.get_world_state()


@router.get("/events", response_model=List[WorldEventResponse])
async def get_active_events(
    event_type: Optional[str] = None,
    current_player: Player = Depends(get_current_player)
):
    """Get all active world events."""
    events_service = WorldEventsService()
    return await events_service.get_active_events(event_type=event_type)


@router.get("/events/{event_id}", response_model=WorldEventResponse)
async def get_event_details(
    event_id: str,
    current_player: Player = Depends(get_current_player)
):
    """Get specific event details."""
    events_service = WorldEventsService()
    event = await events_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/events/{event_id}/respond")
async def respond_to_event(
    event_id: str,
    response: EventResponseRequest,
    current_player: Player = Depends(get_current_player)
):
    """Respond to a world event."""
    events_service = WorldEventsService()
    result = await events_service.respond_to_event(
        event_id=event_id,
        player_id=str(current_player.id),
        response=response.response_type
    )
    return result


@router.get("/karma/global", response_model=GlobalKarmaResponse)
async def get_global_karma(
    current_player: Player = Depends(get_current_player)
):
    """Get global karma statistics."""
    karma_tracker = GlobalKarmaTracker()
    return await karma_tracker.get_global_stats()


@router.get("/events/regional/{territory_id}", response_model=List[RegionalEventResponse])
async def get_regional_events(
    territory_id: int,
    current_player: Player = Depends(get_current_player)
):
    """Get regional events for a specific territory."""
    events_service = WorldEventsService()
    return await events_service.get_regional_events(territory_id=territory_id)


@router.post("/events/trigger")
async def trigger_event(
    request: TriggerEventRequest,
    current_player: Player = Depends(get_current_player)
):
    """Trigger a world event (admin/testing)."""
    # This would typically require admin permissions
    events_service = WorldEventsService()
    event = await events_service.trigger_event(
        event_type=request.event_type,
        parameters=request.parameters
    )
    return event


@router.get("/history")
async def get_world_history(
    limit: int = 50,
    current_player: Player = Depends(get_current_player)
):
    """Get world event history."""
    events_service = WorldEventsService()
    return await events_service.get_event_history(limit=limit)
