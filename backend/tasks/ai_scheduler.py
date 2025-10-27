"""AI Task Scheduler"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)


class AIScheduler:
    """Schedules AI-related background tasks"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.started = False

    def setup_tasks(self) -> None:
        """Setup all scheduled AI tasks"""

        if self.started:
            logger.warning("AI Scheduler already started")
            return

        # Daily quest generation at midnight
        self.scheduler.add_job(
            self._generate_daily_quests,
            CronTrigger(hour=0, minute=0),
            id="daily_quest_generation",
            name="Generate Daily Quests",
            replace_existing=True
        )

        # Weekly challenge generation on Sunday at midnight
        self.scheduler.add_job(
            self._generate_weekly_challenges,
            CronTrigger(day_of_week="sun", hour=0, minute=0),
            id="weekly_challenge_generation",
            name="Generate Weekly Challenges",
            replace_existing=True
        )

        # Process karma queue every 5 minutes
        self.scheduler.add_job(
            self._process_karma_queue,
            IntervalTrigger(minutes=5),
            id="karma_queue_processing",
            name="Process Karma Queue",
            replace_existing=True
        )

        # Clear old cache entries every hour
        self.scheduler.add_job(
            self._cleanup_cache,
            IntervalTrigger(hours=1),
            id="cache_cleanup",
            name="Cleanup Cache",
            replace_existing=True
        )

        logger.info("AI tasks scheduled")

    def start(self) -> None:
        """Start the scheduler"""
        if not self.started:
            self.scheduler.start()
            self.started = True
            logger.info("AI Scheduler started")

    def shutdown(self) -> None:
        """Shutdown the scheduler"""
        if self.started:
            self.scheduler.shutdown()
            self.started = False
            logger.info("AI Scheduler stopped")

    async def _generate_daily_quests(self) -> None:
        """Generate daily quests"""
        from .quest_generator import generate_daily_quests
        logger.info("Running scheduled daily quest generation")
        await generate_daily_quests()

    async def _generate_weekly_challenges(self) -> None:
        """Generate weekly challenges"""
        from .quest_generator import generate_weekly_challenges
        logger.info("Running scheduled weekly challenge generation")
        await generate_weekly_challenges()

    async def _process_karma_queue(self) -> None:
        """Process karma evaluation queue"""
        from .karma_processor import process_karma_queue
        logger.info("Running scheduled karma queue processing")
        await process_karma_queue()

    async def _cleanup_cache(self) -> None:
        """Cleanup old cache entries"""
        logger.info("Running scheduled cache cleanup")
        # Cache cleanup logic here


# Global scheduler instance
ai_scheduler = AIScheduler()


def setup_ai_tasks() -> None:
    """Setup and start AI background tasks"""
    ai_scheduler.setup_tasks()
    ai_scheduler.start()
