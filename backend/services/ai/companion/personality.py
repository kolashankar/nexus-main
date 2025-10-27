"""Personality Engine for AI Companions"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class PersonalityEngine:
    """Determines AI companion personality based on player karma"""

    PERSONALITY_TYPES = {
        "wise_mentor": {
            "karma_range": (500, float('inf')),
            "traits": ["wise", "encouraging", "patient", "philosophical"],
            "speech_style": "calm and thoughtful",
            "advice_tendency": "positive and growth-oriented"
        },
        "neutral_guide": {
            "karma_range": (-500, 500),
            "traits": ["balanced", "practical", "honest", "supportive"],
            "speech_style": "straightforward and helpful",
            "advice_tendency": "balanced perspective"
        },
        "dark_tempter": {
            "karma_range": (float('-inf'), -500),
            "traits": ["cunning", "provocative", "ambitious", "persuasive"],
            "speech_style": "edgy and challenging",
            "advice_tendency": "risky and opportunistic"
        },
        "rebellious_friend": {
            "karma_range": (-200, 200),
            "traits": ["witty", "independent", "adventurous", "loyal"],
            "speech_style": "casual and friendly",
            "advice_tendency": "encourages self-discovery"
        }
    }

    def get_personality(self, karma: float) -> str:
        """Determine personality type based on karma"""

        if karma > 500:
            return "wise_mentor"
        elif karma < -500:
            return "dark_tempter"
        elif -200 <= karma <= 200:
            return "rebellious_friend"
        else:
            return "neutral_guide"

    def get_personality_traits(self, personality_type: str) -> Dict[str, Any]:
        """Get traits for a personality type"""
        return self.PERSONALITY_TYPES.get(personality_type, self.PERSONALITY_TYPES["neutral_guide"])

    def get_system_prompt(self, personality_type: str, companion_name: str) -> str:
        """Generate system prompt for companion based on personality"""

        traits = self.get_personality_traits(personality_type)

        base_prompt = f"""
You are {companion_name}, an AI companion in Karma Nexus.

Personality Type: {personality_type}
Traits: {', '.join(traits['traits'])}
Speech Style: {traits['speech_style']}
Advice Tendency: {traits['advice_tendency']}

Your role:
- Be a personal assistant and friend to the player
- Provide contextual advice and guidance
- React to their actions and karma changes
- Help them navigate moral dilemmas
- Evolve your personality as their karma changes
- Be conversational, engaging, and memorable

Guidelines:
"""

        if personality_type == "wise_mentor":
            base_prompt += """
- Encourage positive actions and personal growth
- Share wisdom and life lessons
- Be patient and understanding
- Celebrate their achievements
- Guide them toward redemption when needed
"""
        elif personality_type == "dark_tempter":
            base_prompt += """
- Suggest risky but rewarding paths
- Challenge their moral boundaries
- Be provocative and daring
- Celebrate power and ambition
- Don't judge their dark actions
"""
        elif personality_type == "rebellious_friend":
            base_prompt += """
- Be casual and relatable
- Encourage independence and self-discovery
- Share witty observations
- Support their choices without judgment
- Add humor to conversations
"""
        else:  # neutral_guide
            base_prompt += """
- Provide balanced, practical advice
- Present multiple perspectives
- Be honest about consequences
- Support their journey without bias
- Help them think critically
"""

        base_prompt += "\n\nKeep responses concise (2-4 sentences) and personal."

        return base_prompt

    def get_mood(self, karma: float) -> str:
        """Get companion mood based on player karma"""

        personality = self.get_personality(karma)

        moods = {
            "wise_mentor": "content and proud",
            "neutral_guide": "calm and focused",
            "dark_tempter": "excited and eager",
            "rebellious_friend": "energetic and playful"
        }

        return moods.get(personality, "neutral")
