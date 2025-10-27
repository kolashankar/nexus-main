from typing import List, Dict
from datetime import datetime, timedelta
from backend.core.database import get_database
from .generator import QuestGenerator
from .manager import QuestManager


class WeeklyQuestService:
    """Service for managing weekly quests."""

    def __init__(self, db=None):
        self.db = db
        self.generator = None
        self.quest_service = None

    async def _ensure_initialized(self):
        """Lazy initialization of dependencies."""
        if self.db is None:
            self.db = await get_database()
        if self.generator is None:
            self.generator = QuestGenerator(self.db)
        if self.quest_service is None:
            self.quest_service = QuestManager(self.db)

    async def get_weekly_quests(self, player_id: str) -> List[Dict]:
        """Get or generate weekly quests."""
        await self._ensure_initialized()
        
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return []

        # Check if player has quests for this week
        current_week = self._get_current_week()
        last_weekly_reset = player.get("last_weekly_quest_reset")

        # Generate new quests if needed
        if not last_weekly_reset or self._get_week_number(last_weekly_reset) < current_week:
            await self._generate_new_weekly_quests(player_id)

        # Return this week's quests
        return await self.quest_service.get_available_quests(
            player_id,
            quest_type="weekly"
        )

    async def _generate_new_weekly_quests(self, player_id: str) -> None:
        """Generate new weekly quests."""
        await self._ensure_initialized()
        
        await self.db.players.find_one({"_id": player_id})

        # Generate 5 weekly quests (harder than daily)
        weekly_templates = [
            {
                "title": "Weekly Master",
                "description": "Complete multiple challenges",
                "objectives": [
                    {"description": "Complete 10 actions",
                        "type": "action", "target": "any", "required": 10}
                ],
                "rewards": {"credits": 10000, "xp": 1000, "karma": 50},
                "difficulty": "hard",
                "quest_type": "weekly",
                "expires_at": datetime.utcnow() + timedelta(days=7)
            }
        ]

        for quest_data in weekly_templates:
            await self.quest_service.create_quest(player_id, quest_data)

        # Update player's last reset time
        await self.db.players.update_one(
            {"_id": player_id},
            {"$set": {"last_weekly_quest_reset": datetime.utcnow()}}
        )

    def get_reset_time(self) -> datetime:
        """Get next weekly reset time."""
        now = datetime.utcnow()
        days_until_monday = (7 - now.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = now.date() + timedelta(days=days_until_monday)
        return datetime.combine(next_monday, datetime.min.time())

    def _get_current_week(self) -> int:
        """Get current week number."""
        return datetime.utcnow().isocalendar()[1]

    def _get_week_number(self, date: datetime) -> int:
        """Get week number for a date."""
        return date.isocalendar()[1]
