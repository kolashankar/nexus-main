"""Dialogue Generator for AI Companions"""

import logging
from typing import Dict, Any, Optional

from ..client import ai_client
from ..cost_tracker import cost_tracker
from .personality import PersonalityEngine

logger = logging.getLogger(__name__)


class DialogueGenerator:
    """Generates contextual dialogue for AI companions"""

    def __init__(self):
        self.ai_client = ai_client
        self.cost_tracker = cost_tracker
        self.personality_engine = PersonalityEngine()

    async def generate_response(
        self,
        player: Dict[str, Any],
        message: str,
        personality: str,
        companion_name: str,
        context: Optional[str] = None
    ) -> str:
        """Generate a conversational response"""

        system_prompt = self.personality_engine.get_system_prompt(
            personality, companion_name)

        # Add player context
        player_context = f"""
Player: {player.get('username')}
Karma: {player.get('karma_points', 0)}
Level: {player.get('level', 1)}
Moral Class: {player.get('moral_class', 'average')}
Recent actions: {', '.join(player.get('recent_actions', [])[-3:]) if player.get('recent_actions') else 'None'}
"""

        if context:
            player_context += f"\nCurrent situation: {context}"

        user_prompt = f"{player_context}\n\nPlayer says: \"{message}\"\n\nRespond as {companion_name} in character."

        try:
            response = await self.ai_client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="gpt-4o-mini",  # Use mini for dialogue
                temperature=0.8,  # Higher for personality
                max_tokens=200
            )

            # Track usage
            if "usage" in response:
                self.cost_tracker.track_call(
                    "companion_dialogue",
                    "gpt-4o-mini",
                    response["usage"]["prompt_tokens"],
                    response["usage"]["completion_tokens"],
                    cached=False
                )

            return response.get("content", "I'm here for you.")

        except Exception as e:
            logger.error(f"Dialogue generation error: {e}")
            return self._fallback_response(personality, message)

    def _fallback_response(self, personality: str, message: str) -> str:
        """Fallback response when AI is unavailable"""

        fallbacks = {
            "wise_mentor": "I sense your intentions. Let wisdom guide your path.",
            "neutral_guide": "I'm here to help. What do you need?",
            "dark_tempter": "Interesting. Tell me more about your plans.",
            "rebellious_friend": "Hey, I'm listening. What's on your mind?"
        }

        return fallbacks.get(personality, "I'm here to assist you.")
