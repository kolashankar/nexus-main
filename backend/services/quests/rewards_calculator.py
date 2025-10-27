"""Quest rewards calculator"""

from typing import Dict, Any
import random


class QuestRewardsCalculator:
    """Calculates quest rewards based on various factors"""

    @staticmethod
    def calculate_base_rewards(
        difficulty: str,
        player_level: int,
        quest_type: str,
    ) -> Dict[str, Any]:
        """Calculate base rewards"""
        # Base values by difficulty
        base = {
            "easy": {"credits": 100, "xp": 50, "karma": 10},
            "medium": {"credits": 300, "xp": 150, "karma": 25},
            "hard": {"credits": 600, "xp": 400, "karma": 50},
            "very_hard": {"credits": 1200, "xp": 800, "karma": 100},
        }

        rewards = base.get(difficulty, base["medium"]).copy()

        # Scale by player level
        level_multiplier = 1 + (player_level * 0.1)
        rewards["credits"] = int(rewards["credits"] * level_multiplier)
        rewards["xp"] = int(rewards["xp"] * level_multiplier)

        # Quest type bonuses
        if quest_type == "guild":
            rewards["credits"] = int(rewards["credits"] * 1.5)
            rewards["guild_coins"] = 50
        elif quest_type == "world":
            rewards["credits"] = int(rewards["credits"] * 1.3)
        elif quest_type == "campaign":
            rewards["xp"] = int(rewards["xp"] * 2)

        return rewards

    @staticmethod
    def add_bonus_rewards(
        rewards: Dict[str, Any],
        performance_score: float,  # 0.0 to 1.0
    ) -> Dict[str, Any]:
        """Add bonus rewards based on performance"""
        # Bonus for perfect/fast completion
        if performance_score >= 0.9:
            rewards["credits"] = int(rewards.get("credits", 0) * 1.5)
            rewards["xp"] = int(rewards.get("xp", 0) * 1.5)
            rewards["bonus"] = "Perfect completion!"
        elif performance_score >= 0.75:
            rewards["credits"] = int(rewards.get("credits", 0) * 1.2)
            rewards["xp"] = int(rewards.get("xp", 0) * 1.2)
            rewards["bonus"] = "Great job!"

        return rewards

    @staticmethod
    def add_random_reward(
        rewards: Dict[str, Any],
        luck_factor: float = 0.1,
    ) -> Dict[str, Any]:
        """Add random bonus reward"""
        if random.random() < luck_factor:
            bonus_types = [
                "karma_tokens",
                "special_item",
                "trait_boost",
            ]

            bonus_type = random.choice(bonus_types)

            if bonus_type == "karma_tokens":
                rewards["karma_tokens"] = rewards.get(
                    "karma_tokens", 0) + random.randint(1, 5)
                rewards["lucky_bonus"] = "Bonus karma tokens!"
            elif bonus_type == "special_item":
                rewards["special_item"] = f"item_{random.randint(1, 100)}"
                rewards["lucky_bonus"] = "Found a special item!"
            elif bonus_type == "trait_boost":
                rewards["trait_boosts"] = {"random_trait": 5}
                rewards["lucky_bonus"] = "Random trait boost!"

        return rewards
