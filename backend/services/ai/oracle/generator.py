"""Quest Generator - Generates quests using AI"""

import json
import logging
from typing import Dict, Any

from .prompts import QUEST_GENERATION_TEMPLATE, CAMPAIGN_GENERATION_TEMPLATE
from .schemas import (
    QuestGenerationRequest,
    GeneratedQuest,
    GeneratedCampaign,
    QuestObjective,
    QuestRewards,
    QuestRequirements
)
from .config import MODEL_CONFIG, QUEST_TYPES
from ..client import ai_client
from ..cache_manager import cache_manager
from ..cost_tracker import cost_tracker

logger = logging.getLogger(__name__)


class QuestGenerator:
    """Generates quests using AI"""

    def __init__(self):
        self.ai_client = ai_client
        self.cache_manager = cache_manager
        self.cost_tracker = cost_tracker

    def _format_traits(self, traits: Dict[str, float], threshold: float, above: bool = True) -> str:
        """Format traits for prompt"""
        if above:
            filtered = {k: v for k, v in traits.items() if v >= threshold}
        else:
            filtered = {k: v for k, v in traits.items() if v < threshold}

        if not filtered:
            return "None"

        return "\n".join([
            f"- {trait}: {value:.1f}%"
            for trait, value in sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:5]
        ])

    async def generate_quest(self, request: QuestGenerationRequest) -> GeneratedQuest:
        """Generate a personalized quest"""

        # Note: We don't cache quest generation to ensure uniqueness
        prompt = self._prepare_quest_prompt(request)

        try:
            response = await self._call_ai(prompt, "quest")
            quest_data = self._parse_quest_response(response)
            quest_data["quest_type"] = request.quest_type

            return GeneratedQuest(**quest_data)

        except Exception as e:
            logger.error(f"Quest generation error: {e}")
            return self._fallback_quest(request)

    def _prepare_quest_prompt(self, request: QuestGenerationRequest) -> str:
        """Prepare quest generation prompt"""
        return QUEST_GENERATION_TEMPLATE.format(
            username=request.username,
            level=request.level,
            karma_points=request.karma_points,
            moral_class=request.moral_class,
            economic_class=request.economic_class,
            top_traits=self._format_traits(request.traits, 70, above=True),
            low_traits=self._format_traits(request.traits, 30, above=False),
            recent_actions=", ".join(
                request.recent_actions[-5:]) if request.recent_actions else "None",
            quest_type=request.quest_type,
            difficulty=request.difficulty
        )

    async def _call_ai(self, prompt: str, context: str = "quest") -> Dict[str, Any]:
        """Call AI for generation"""
        from .prompts import ORACLE_SYSTEM

        messages = [
            {"role": "system", "content": ORACLE_SYSTEM},
            {"role": "user", "content": prompt}
        ]

        response = await self.ai_client.chat_completion(
            messages=messages,
            model=MODEL_CONFIG["default_model"],
            temperature=MODEL_CONFIG["temperature"],
            response_format={"type": "json_object"},
            max_tokens=MODEL_CONFIG["max_tokens"]
        )

        # Track usage
        if "usage" in response:
            self.cost_tracker.track_call(
                f"oracle_{context}",
                MODEL_CONFIG["default_model"],
                response["usage"]["prompt_tokens"],
                response["usage"]["completion_tokens"],
                cached=False
            )

        return response

    def _parse_quest_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI quest response"""
        try:
            content = response.get("content", "{}")
            data = json.loads(content)

            # Ensure all required fields
            return {
                "title": data.get("title", "Mystery Quest"),
                "description": data.get("description", "A quest awaits you."),
                "lore": data.get("lore", "The story unfolds..."),
                "objectives": [
                    QuestObjective(**obj).dict() for obj in data.get("objectives", [])
                ],
                "rewards": QuestRewards(**data.get("rewards", {})).dict(),
                "requirements": QuestRequirements(**data.get("requirements", {})).dict(),
                "difficulty": data.get("difficulty", "medium"),
                "estimated_time_minutes": data.get("estimated_time_minutes", 30),
                "moral_choice": data.get("moral_choice"),
                "branching_paths": data.get("branching_paths", []),
                "failure_consequence": data.get("failure_consequence")
            }
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse quest response: {e}")
            raise

    def _fallback_quest(self, request: QuestGenerationRequest) -> GeneratedQuest:
        """Fallback quest when AI is unavailable"""
        quest_config = QUEST_TYPES.get(
            request.quest_type, QUEST_TYPES["personal"])

        return GeneratedQuest(
            title=f"Standard {request.quest_type.title()} Quest",
            description=f"Complete this {request.quest_type} quest to earn rewards.",
            lore="A standard quest generated by the system.",
            objectives=[
                QuestObjective(
                    description="Complete a basic task",
                    type="collect",
                    target="experience",
                    required=1
                )
            ],
            rewards=QuestRewards(
                credits=int(100 * quest_config["rewards_multiplier"]),
                xp=int(50 * quest_config["rewards_multiplier"]),
                karma=10
            ),
            requirements=QuestRequirements(
                min_level=quest_config["min_level"]
            ),
            difficulty=request.difficulty,
            estimated_time_minutes=quest_config["duration_hours"] * 60,
            quest_type=request.quest_type
        )

    async def generate_campaign(
        self,
        request: QuestGenerationRequest,
        campaign_type: str = "redemption"
    ) -> GeneratedCampaign:
        """Generate a story campaign"""

        prompt = self._prepare_campaign_prompt(request, campaign_type)

        try:
            response = await self._call_ai(prompt, "campaign")
            campaign_data = self._parse_campaign_response(response)

            return GeneratedCampaign(**campaign_data)

        except Exception as e:
            logger.error(f"Campaign generation error: {e}")
            return self._fallback_campaign(request, campaign_type)

    def _prepare_campaign_prompt(self, request: QuestGenerationRequest, campaign_type: str) -> str:
        """Prepare campaign generation prompt"""
        traits_summary = ", ".join([
            f"{k}: {v:.0f}%"
            for k, v in sorted(request.traits.items(), key=lambda x: x[1], reverse=True)[:10]
        ])

        return CAMPAIGN_GENERATION_TEMPLATE.format(
            username=request.username,
            karma_points=request.karma_points,
            moral_class=request.moral_class,
            traits_summary=traits_summary,
            campaign_type=campaign_type
        )

    def _parse_campaign_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI campaign response"""
        try:
            content = response.get("content", "{}")
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse campaign response: {e}")
            raise

    def _fallback_campaign(self, request: QuestGenerationRequest, campaign_type: str) -> GeneratedCampaign:
        """Fallback campaign when AI is unavailable"""
        from .schemas import CampaignChapter, CampaignEnding

        return GeneratedCampaign(
            campaign_title=f"The {campaign_type.title()} Story",
            campaign_description="A standard campaign story.",
            theme=campaign_type,
            total_chapters=5,
            chapters=[
                CampaignChapter(
                    chapter_number=i+1,
                    title=f"Chapter {i+1}",
                    description=f"Chapter {i+1} of your journey.",
                    objectives=[
                        QuestObjective(
                            description="Complete chapter objective",
                            type="collect",
                            target="progress",
                            required=1
                        )
                    ]
                )
                for i in range(5)
            ],
            endings=[
                CampaignEnding(
                    ending_type="good",
                    condition="Complete all chapters positively",
                    description="A heroic ending.",
                    rewards=QuestRewards(credits=5000, xp=2500, karma=100)
                )
            ]
        )
