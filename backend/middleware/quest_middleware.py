"""Quest middleware - Automatic quest progress tracking"""

from fastapi import Request
from typing import Callable
from ..services.quests.tracking import QuestTrackingService


async def quest_tracking_middleware(
    request: Request,
    call_next: Callable,
):
    """Middleware to track quest progress on actions"""
    response = await call_next(request)

    # Check if this was an action endpoint
    if request.url.path.startswith("/api/actions/"):
        # Extract player and action info from request/response
        player_id = getattr(request.state, "player_id", None)

        if player_id:
            # Get database
            db = request.app.state.db

            # Track action
            tracking_service = QuestTrackingService(db)

            # Determine action type from path
            action_type = request.url.path.split("/")[-1]

            # Track the action
            await tracking_service.track_action(
                player_id=player_id,
                action_type=action_type,
                action_data={},
            )

    return response
