"""Background tasks for seasonal content."""

import asyncio
from datetime import datetime
from backend.core.database import db
from backend.services.seasonal.battle_pass import BattlePassService
from backend.services.seasonal.seasons import SeasonService
from backend.services.world.events import WorldEventsService
import logging

logger = logging.getLogger(__name__)


class SeasonalTasksManager:
    """Manager for seasonal background tasks."""

    def __init__(self):
        self.db = db
        self.bp_service = BattlePassService()
        self.season_service = SeasonService()
        self.events_service = WorldEventsService()

    async def check_season_end(self):
        """Check if current season has ended and handle transition."""
        try:
            current_season = await self.season_service.get_current_season()
            if not current_season:
                logger.info("No active season found")
                return

            now = datetime.utcnow()
            end_date = current_season["end_date"]

            # Check if season should end
            if now >= end_date:
                logger.info(
                    f"Season {current_season['season_number']} has ended. Processing...")
                await self.season_service.end_season(current_season["season_id"])

                # Create new season
                new_season_number = current_season["season_number"] + 1
                await self.season_service.create_season(
                    season_number=new_season_number,
                    name=f"Season {new_season_number}",
                    duration_days=90
                )
                logger.info(f"Created new season {new_season_number}")

            # Warn if season is ending soon (7 days)
            elif (end_date - now).days <= 7:
                logger.info(
                    f"Season {current_season['season_number']} ending in {(end_date - now).days} days")

        except Exception as e:
            logger.error(f"Error checking season end: {e}")

    async def check_battle_pass_end(self):
        """Check if battle pass has ended."""
        try:
            battle_pass = await self.bp_service.get_active_battle_pass()
            if not battle_pass:
                logger.info("No active battle pass found")
                return

            now = datetime.utcnow()
            end_date = battle_pass["end_date"]

            if now >= end_date:
                logger.info(
                    f"Battle Pass for Season {battle_pass['season']} has ended")
                await self.db.battle_passes.update_one(
                    {"pass_id": battle_pass["pass_id"]},
                    {"$set": {"is_active": False}}
                )

        except Exception as e:
            logger.error(f"Error checking battle pass end: {e}")

    async def check_world_events(self):
        """Check and update world events."""
        try:
            # End expired events
            expired_count = await self.events_service.end_expired_events()
            if expired_count > 0:
                logger.info(f"Ended {expired_count} expired world events")

            # Check if collective karma triggers new events
            world_state = await self.events_service.get_world_state()
            if world_state:
                collective_karma = world_state.get("collective_karma", 0)
                await self.events_service.check_and_trigger_karma_events(collective_karma)

        except Exception as e:
            logger.error(f"Error checking world events: {e}")

    async def update_leaderboards(self):
        """Update leaderboard caches."""
        try:
            from backend.services.leaderboards.manager import LeaderboardManager
            manager = LeaderboardManager()
            await manager.update_leaderboards()
            logger.info("Leaderboards updated")
        except Exception as e:
            logger.error(f"Error updating leaderboards: {e}")

    async def run_periodic_tasks(self):
        """Run all periodic tasks."""
        logger.info("Running seasonal periodic tasks...")

        await asyncio.gather(
            self.check_season_end(),
            self.check_battle_pass_end(),
            self.check_world_events(),
            self.update_leaderboards(),
            return_exceptions=True
        )

        logger.info("Seasonal periodic tasks completed")


async def run_seasonal_tasks_loop():
    """Run seasonal tasks in a loop (every hour)."""
    manager = SeasonalTasksManager()

    while True:
        try:
            await manager.run_periodic_tasks()
        except Exception as e:
            logger.error(f"Error in seasonal tasks loop: {e}")

        # Wait 1 hour before next run
        await asyncio.sleep(3600)


if __name__ == "__main__":
    # For testing
    asyncio.run(run_seasonal_tasks_loop())
