"""Advice Engine for AI Companions"""

import logging
from typing import Dict, Any

from ..client import ai_client
from ..cost_tracker import cost_tracker
from .personality import PersonalityEngine

logger = logging.getLogger(__name__)


class AdviceEngine:
    """Generates contextual advice for players"""

    def __init__(self):
        self.ai_client = ai_client
        self.cost_tracker = cost_tracker
        self.personality_engine = PersonalityEngine()

    async def generate_advice(
        self,
        player: Dict[str, Any],
        situation: str,
        personality: str,
        companion_name: str
    ) -> str:
        """Generate advice for a specific situation"""

        system_prompt = self.personality_engine.get_system_prompt(
            personality, companion_name)

        # Prepare advice request
        user_prompt = f"""
Player Profile:
- Username: {player.get('username')}
- Karma: {player.get('karma_points', 0)}
- Level: {player.get('level', 1)}
- Moral Class: {player.get('moral_class', 'average')}

Top Traits:
{self._format_top_traits(player.get('traits', {}))}

Situation: {situation}

Provide advice as {companion_name} in character. Be specific and actionable (2-4 sentences).
"""

        try:
            response = await self.ai_client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="gpt-4o-mini",
                temperature=0.7,
                max_tokens=250
            )

            # Track usage
            if "usage" in response:
                self.cost_tracker.track_call(
                    "companion_advice",
                    "gpt-4o-mini",
                    response["usage"]["prompt_tokens"],
                    response["usage"]["completion_tokens"],
                    cached=False
                )

            return response.get("content", "Consider your options carefully.")

        except Exception as e:
            logger.error(f"Advice generation error: {e}")
            return self._fallback_advice(personality, situation)

    def _format_top_traits(self, traits: Dict[str, float]) -> str:
        """Format top traits for prompt"""
        sorted_traits = sorted(
            traits.items(), key=lambda x: x[1], reverse=True)[:5]
        if not sorted_traits:
            return "No significant traits"
        return "\n".join([f"- {trait}: {value:.0f}%" for trait, value in sorted_traits])

    def _fallback_advice(self, personality: str, situation: str) -> str:
        """Fallback advice when AI is unavailable"""

        fallbacks = {
            "wise_mentor": "Reflect on your values and choose the path that brings growth.",
            "neutral_guide": "Weigh the consequences and make a thoughtful decision.",
            "dark_tempter": "Take the bold path. Fortune favors the daring.",
            "rebellious_friend": "Trust your instincts and do what feels right to you."
        }

        return fallbacks.get(personality, "Consider all angles before deciding.")
