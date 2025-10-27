"""Quest scheduler - Manages quest generation timing"""

from datetime import datetime, timedelta
from typing import Dict


class QuestScheduler:
    """Schedules automatic quest generation"""

    def __init__(self, db):
        self.db = db
        self.quests = db.quests
        self.players = db.players

    async def check_daily_quests(self, player_id: str) -> bool:
        """Check if player needs daily quests generated"""
        today = datetime.utcnow().date()

        # Check if player has daily quests for today
        existing = await self.quests.find({
            "player_id": player_id,
            "quest_type": "daily",
            "generated_at": {
                "$gte": datetime.combine(today, datetime.min.time())
            }
        }).to_list(length=10)

        # Should have 3 daily quests
        return len(existing) < 3

    async def check_weekly_quests(self, player_id: str) -> bool:
        """Check if player needs weekly quests"""
        now = datetime.utcnow()
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(
            hour=0, minute=0, second=0, microsecond=0)

        existing = await self.quests.find({
            "player_id": player_id,
            "quest_type": "weekly",
            "generated_at": {"$gte": week_start}
        }).to_list(length=10)

        # Should have 5 weekly quests
        return len(existing) < 5

    async def schedule_quest_generation(
        self,
        player_id: str,
    ) -> Dict[str, bool]:
        """Schedule quest generation for player"""
        needs_daily = await self.check_daily_quests(player_id)
        needs_weekly = await self.check_weekly_quests(player_id)

        return {
            "needs_daily": needs_daily,
            "needs_weekly": needs_weekly,
        }

    async def get_refresh_times(self) -> Dict[str, datetime]:
        """Get next refresh times"""
        now = datetime.utcnow()

        # Next daily refresh (midnight UTC)
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        # Next weekly refresh (Monday midnight UTC)
        days_until_monday = (7 - now.weekday()) % 7
        next_monday = (now + timedelta(days=days_until_monday)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        return {
            "daily_refresh": tomorrow,
            "weekly_refresh": next_monday,
        }
