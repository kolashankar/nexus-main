"""Background tasks for quest system"""

from datetime import datetime, timedelta
import asyncio


class QuestBackgroundTasks:
    """Background tasks for quest management"""

    def __init__(self, db):
        self.db = db
        self.quests = db.quests
        self.players = db.players
        self.running = False

    async def start(self):
        """Start background tasks"""
        self.running = True

        # Start multiple tasks
        await asyncio.gather(
            self.expire_quests_task(),
            self.generate_daily_quests_task(),
            self.cleanup_old_quests_task(),
        )

    async def stop(self):
        """Stop background tasks"""
        self.running = False

    async def expire_quests_task(self):
        """Periodically expire old quests"""
        while self.running:
            try:
                # Mark expired quests
                result = await self.quests.update_many(
                    {
                        "status": {"$in": ["available", "active"]},
                        "expires_at": {"$lt": datetime.utcnow()}
                    },
                    {
                        "$set": {
                            "status": "expired",
                            "updated_at": datetime.utcnow(),
                        }
                    }
                )

                if result.modified_count > 0:
                    print(f"Expired {result.modified_count} quests")

            except Exception as e:
                print(f"Error expiring quests: {e}")

            # Run every 5 minutes
            await asyncio.sleep(300)

    async def generate_daily_quests_task(self):
        """Generate daily quests for all players"""
        while self.running:
            try:
                # Check if it's a new day
                now = datetime.utcnow()
                if now.hour == 0 and now.minute < 10:
                    # Generate daily quests for all active players
                    players = await self.players.find(
                        {"online": True}
                    ).to_list(length=1000)

                    print(
                        f"Generating daily quests for {len(players)} players")

                    # This would call the quest generator for each player
                    # Skipped for now to avoid heavy processing

            except Exception as e:
                print(f"Error generating daily quests: {e}")

            # Check every 10 minutes
            await asyncio.sleep(600)

    async def cleanup_old_quests_task(self):
        """Clean up very old completed/failed quests"""
        while self.running:
            try:
                # Delete quests older than 30 days
                cutoff = datetime.utcnow() - timedelta(days=30)

                result = await self.quests.delete_many({
                    "status": {"$in": ["completed", "failed", "expired"]},
                    "updated_at": {"$lt": cutoff}
                })

                if result.deleted_count > 0:
                    print(f"Cleaned up {result.deleted_count} old quests")

            except Exception as e:
                print(f"Error cleaning up quests: {e}")

            # Run once per day
            await asyncio.sleep(86400)
