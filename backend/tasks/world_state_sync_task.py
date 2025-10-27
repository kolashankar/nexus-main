"""Background task for syncing world state"""

import logging
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import get_settings
from ..services.world.state_manager import WorldStateManager

logger = logging.getLogger(__name__)

settings = get_settings()


async def sync_world_state_task():
    """
    Periodically sync world state statistics
    Runs every 10 minutes for full sync
    """
    # Connect to database
    client = AsyncIOMotorClient(settings.MONGO_URL)
    db = client[settings.DB_NAME]

    world_manager = WorldStateManager(db)

    while True:
        try:
            logger.info("Syncing world state...")

            # Perform full sync
            state = await world_manager.sync_world_state()

            logger.info(
                f"World state synced: "
                f"karma={state.collective_karma:.0f}, "
                f"players={state.total_players}, "
                f"online={state.online_players}"
            )

        except Exception as e:
            logger.error(f"Error in world state sync task: {e}", exc_info=True)

        # Wait 10 minutes before next sync
        await asyncio.sleep(600)


def start_world_state_sync_task():
    """
    Start the world state sync background task
    Call this from your FastAPI startup event
    """
    logger.info("Starting world state sync background task")

    # Create task
    task = asyncio.create_task(sync_world_state_task())

    return task
