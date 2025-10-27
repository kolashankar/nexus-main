"""World Events API Routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from ....core.database import get_database
from ....services.world.event_manager import EventManager
from .schemas import (
    EventResponse,
    EventListResponse,
    TriggerEventRequest,
    TriggerEventResponse,
    ParticipationRequest,
    ParticipationResponse
)
from ..auth.utils import get_current_user

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/active", response_model=Optional[EventResponse])
async def get_active_event(
    db = Depends(get_database)
):
    """
    Get currently active global event
    """
    event_manager = EventManager(db)
    event = await event_manager.get_active_global_event()

    if not event:
        return None

    return EventResponse.from_model(event)


@router.get("/recent", response_model=EventListResponse)
async def get_recent_events(
    limit: int = Query(default=10, ge=1, le=50,
                       description="Number of events to return"),
    db = Depends(get_database)
):
    """
    Get recent world events (active and ended)
    """
    event_manager = EventManager(db)
    events = await event_manager.get_recent_events(limit=limit)

    return EventListResponse(
        events=[EventResponse.from_model(e) for e in events],
        total=len(events)
    )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str,
    db = Depends(get_database)
):
    """
    Get event by ID
    """
    event_manager = EventManager(db)
    event = await event_manager.get_event_by_id(event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return EventResponse.from_model(event)


@router.post("/trigger", response_model=TriggerEventResponse)
async def trigger_event(
    request: TriggerEventRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Manually trigger an event (admin only)
    
    This endpoint allows administrators to manually trigger world events.
    If no event_type is specified, The Architect will choose based on current world state.
    """
    # Check if user is admin (you'll need to add admin role to your user model)
    # For now, we'll allow any authenticated user (change in production)

    event_manager = EventManager(db)

    try:
        # Check and trigger event
        event = await event_manager.check_and_trigger_event(force=request.force)

        if not event:
            # Try with force if conditions not met
            if not request.force:
                event = await event_manager.check_and_trigger_event(force=True)

        if not event:
            return TriggerEventResponse(
                success=False,
                message="No event was triggered. Conditions not met.",
                event=None
            )

        return TriggerEventResponse(
            success=True,
            message=f"Event '{event.name}' triggered successfully!",
            event=EventResponse.from_model(event)
        )

    except Exception as e:
        logger.error(f"Error triggering event: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger event: {str(e)}"
        )


@router.post("/participate", response_model=ParticipationResponse)
async def participate_in_event(
    request: ParticipationRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Record participation in an active event
    
    Some events require player participation to earn rewards.
    This endpoint records your participation.
    """
    event_manager = EventManager(db)

    # Check if event exists and is active
    event = await event_manager.get_event_by_id(request.event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    if event.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is not currently active"
        )

    if not event.requires_participation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This event does not require participation"
        )

    # Record participation
    success = await event_manager.record_participation(
        event_id=request.event_id,
        player_id=str(current_user["_id"]),
        username=current_user["username"]
    )

    if not success:
        return ParticipationResponse(
            success=False,
            message="Participation not recorded",
            event_id=request.event_id
        )

    return ParticipationResponse(
        success=True,
        message="Participation recorded! Rewards will be distributed when the event ends.",
        event_id=request.event_id
    )


@router.get("/territory/{territory_id}", response_model=EventListResponse)
async def get_territory_events(
    territory_id: int,
    db = Depends(get_database)
):
    """
    Get active regional events for a territory
    """
    if territory_id < 1 or territory_id > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Territory ID must be between 1 and 20"
        )

    event_manager = EventManager(db)
    events = await event_manager.get_active_regional_events(territory_id)

    return EventListResponse(
        events=[EventResponse.from_model(e) for e in events],
        total=len(events)
    )
