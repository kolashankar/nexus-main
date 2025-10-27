"""Background task for checking and triggering world events"""

import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import get_settings
from ..services.world.event_manager import EventManager

logger = logging.getLogger(__name__)

settings = get_settings()


async def check_events_task():
    """
    Periodically check if world events should be triggered
    Runs every 5 minutes
    """
    # Connect to database
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.DB_NAME]

    event_manager = EventManager(db)

    while True:
        try:
            logger.info("Checking for world event triggers...")

            # Check if event should be triggered
            event = await event_manager.check_and_trigger_event(force=False)

            if event:
                logger.info(
                    f"World event triggered: {event.name} ({event.event_type})")
            else:
                logger.info("No event triggered this check")

            # Clean up expired events
            cleaned = await event_manager.cleanup_expired_events()
            if cleaned > 0:
                logger.info(f"Cleaned up {cleaned} expired events")

        except Exception as e:
            logger.error(f"Error in events check task: {e}", exc_info=True)

        # Wait 5 minutes before next check
        await asyncio.sleep(300)


def start_world_events_task():
    """
    Start the world events background task
    Call this from your FastAPI startup event
    """
    logger.info("Starting world events background task")

    # Create task
    task = asyncio.create_task(check_events_task())

    return task
