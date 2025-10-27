"""Oracle - Main Service"""

import logging
from typing import Dict, Any, Optional, List

from ..base import BaseAIService
from .generator import QuestGenerator
from .schemas import QuestGenerationRequest, GeneratedQuest, GeneratedCampaign

logger = logging.getLogger(__name__)


class Oracle(BaseAIService):
    """The Oracle - Quest Generator AI"""

    def __init__(self):
        super().__init__("Oracle", model="gpt-4o")
        self.generator = QuestGenerator()
        logger.info("Oracle initialized")

    async def generate_quest_for_player(
        self,
        player: Dict[str, Any],
        quest_type: str = "personal",
        difficulty: str = "medium"
    ) -> GeneratedQuest:
        """Generate a personalized quest for a player"""

        request = QuestGenerationRequest(
            player_id=str(player.get("_id", "")),
            username=player.get("username", "Unknown"),
            level=player.get("level", 1),
            karma_points=player.get("karma_points", 0),
            moral_class=player.get("moral_class", "average"),
            economic_class=player.get("economic_class", "middle"),
            traits=player.get("traits", {}),
            recent_actions=player.get("recent_actions", []),
            quest_type=quest_type,
            difficulty=difficulty
        )

        quest = await self.generator.generate_quest(request)

        logger.info(
            f"Oracle generated {quest_type} quest for {request.username}: "
            f"{quest.title} ({quest.difficulty})"
        )

        return quest

    async def generate_daily_quests(
        self,
        player: Dict[str, Any],
        count: int = 3
    ) -> List[GeneratedQuest]:
        """Generate daily quests for a player"""
        quests = []

        for i in range(count):
            difficulty = ["easy", "medium", "hard"][i % 3]
            quest = await self.generate_quest_for_player(
                player,
                quest_type="daily",
                difficulty=difficulty
            )
            quests.append(quest)

        return quests

    async def generate_weekly_challenges(
        self,
        player: Dict[str, Any],
        count: int = 5
    ) -> List[GeneratedQuest]:
        """Generate weekly challenges for a player"""
        quests = []

        for i in range(count):
            difficulty = "hard" if i < 3 else "epic"
            quest = await self.generate_quest_for_player(
                player,
                quest_type="weekly",
                difficulty=difficulty
            )
            quests.append(quest)

        return quests

    async def generate_campaign(
        self,
        player: Dict[str, Any],
        campaign_type: Optional[str] = None
    ) -> GeneratedCampaign:
        """Generate a story campaign for a player"""

        # Determine campaign type based on player karma if not specified
        if not campaign_type:
            karma = player.get("karma_points", 0)
            if karma < -500:
                campaign_type = "redemption"
            elif karma > 500:
                campaign_type = "corruption"
            else:
                campaign_type = "discovery"

        request = QuestGenerationRequest(
            player_id=str(player.get("_id", "")),
            username=player.get("username", "Unknown"),
            level=player.get("level", 1),
            karma_points=player.get("karma_points", 0),
            moral_class=player.get("moral_class", "average"),
            economic_class=player.get("economic_class", "middle"),
            traits=player.get("traits", {}),
            recent_actions=player.get("recent_actions", []),
            quest_type="campaign",
            difficulty="epic"
        )

        campaign = await self.generator.generate_campaign(request, campaign_type)

        logger.info(
            f"Oracle generated campaign for {request.username}: "
            f"{campaign.campaign_title} ({campaign_type})"
        )

        return campaign

    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        """Process quest generation (base class requirement)"""
        quest = await self.generate_quest_for_player(*args, **kwargs)
        return quest.dict()


# Global oracle instance
oracle = Oracle()
