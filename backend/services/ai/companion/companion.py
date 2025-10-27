"""AI Companion - Main Service"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..base import BaseAIService
from .personality import PersonalityEngine
from .dialogue import DialogueGenerator
from .advice import AdviceEngine

logger = logging.getLogger(__name__)


class AICompanion(BaseAIService):
    """Personal AI Companion for each player"""

    def __init__(self):
        super().__init__("AICompanion", model="gpt-4o-mini")  # Use mini for cost efficiency
        self.personality_engine = PersonalityEngine()
        self.dialogue_generator = DialogueGenerator()
        self.advice_engine = AdviceEngine()
        logger.info("AI Companion initialized")

    async def talk(
        self,
        player: Dict[str, Any],
        message: str,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Have a conversation with the companion"""

        # Determine companion personality based on player karma
        personality = self.personality_engine.get_personality(
            player.get("karma_points", 0))
        companion_name = player.get("ai_companion", {}).get("name", "Aria")

        # Generate response
        response = await self.dialogue_generator.generate_response(
            player=player,
            message=message,
            personality=personality,
            companion_name=companion_name,
            context=context
        )

        logger.info(
            f"Companion {companion_name} responded to {player.get('username')}")

        return {
            "companion_name": companion_name,
            "personality": personality,
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def give_advice(
        self,
        player: Dict[str, Any],
        situation: str
    ) -> Dict[str, Any]:
        """Give advice for a specific situation"""

        personality = self.personality_engine.get_personality(
            player.get("karma_points", 0))
        companion_name = player.get("ai_companion", {}).get("name", "Aria")

        advice = await self.advice_engine.generate_advice(
            player=player,
            situation=situation,
            personality=personality,
            companion_name=companion_name
        )

        logger.info(
            f"Companion {companion_name} gave advice to {player.get('username')}")

        return {
            "companion_name": companion_name,
            "advice": advice,
            "personality": personality,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def get_companion_status(
        self,
        player: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get companion status and relationship"""

        companion_data = player.get("ai_companion", {})
        personality = self.personality_engine.get_personality(
            player.get("karma_points", 0))

        return {
            "name": companion_data.get("name", "Aria"),
            "personality_type": personality,
            "relationship_level": companion_data.get("relationship_level", 0),
            "conversations": companion_data.get("conversations", 0),
            "last_interaction": companion_data.get("last_advice"),
            "mood": self.personality_engine.get_mood(player.get("karma_points", 0))
        }

    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        """Process companion interaction (base class requirement)"""
        return await self.talk(*args, **kwargs)


# Global AI companion instance
ai_companion = AICompanion()
