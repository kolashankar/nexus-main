from typing import Dict, Tuple
from backend.models.player.prestige import PlayerPrestige, PrestigeReward
import logging

logger = logging.getLogger(__name__)

# Prestige rewards for each level (1-10)
PRESTIGE_REWARDS = {
    1: PrestigeReward(
        prestige_level=1,
        prestige_points=100,
        exclusive_powers=[],
        permanent_bonuses={"xp_gain": 1.05},  # 5% XP boost
        cosmetic_rewards=["prestige_1_title", "prestige_1_badge"]
    ),
    2: PrestigeReward(
        prestige_level=2,
        prestige_points=150,
        exclusive_powers=[],
        permanent_bonuses={"xp_gain": 1.10, "karma_gain": 1.05},
        cosmetic_rewards=["prestige_2_title", "prestige_2_aura"]
    ),
    3: PrestigeReward(
        prestige_level=3,
        prestige_points=200,
        exclusive_powers=["prestige_sight"],
        permanent_bonuses={"xp_gain": 1.15,
            "karma_gain": 1.10, "credits_gain": 1.05},
        cosmetic_rewards=["prestige_3_title", "prestige_3_outfit"]
    ),
    5: PrestigeReward(
        prestige_level=5,
        prestige_points=300,
        exclusive_powers=["prestige_mastery"],
        permanent_bonuses={"xp_gain": 1.25,
            "karma_gain": 1.15, "credits_gain": 1.10},
        cosmetic_rewards=["prestige_5_title", "prestige_5_crown"]
    ),
    10: PrestigeReward(
        prestige_level=10,
        prestige_points=500,
        exclusive_powers=["divine_transcendence"],
        permanent_bonuses={"xp_gain": 1.50, "karma_gain": 1.25,
            "credits_gain": 1.20, "all_traits": 1.10},
        cosmetic_rewards=["prestige_10_title", "prestige_10_legendary_skin"]
    ),
}

class PrestigeService:
    """Service for managing player prestige"""

    @staticmethod
    def initialize_prestige(player_id: str) -> PlayerPrestige:
        """Initialize prestige for a new player"""
        return PlayerPrestige(player_id=player_id)

    @staticmethod
    def check_prestige_eligibility(
        player_prestige: PlayerPrestige,
        player_level: int,
        karma_points: int,
        total_achievements: int
    ) -> Tuple[bool, str]:
        """Check if player can prestige"""
        # Max prestige level check
        if player_prestige.current_prestige_level >= 10:
            return False, "Maximum prestige level reached"

        # Level requirement
        if player_level < 100:
            return False, f"Must be level 100 (current: {player_level})"

        # Karma requirement
        if karma_points < 1000:
            return False, f"Must have 1000+ karma (current: {karma_points})"

        # Achievement requirement (at higher prestige levels)
        if player_prestige.current_prestige_level >= 5 and total_achievements < 50:
            return False, "Must have 50+ achievements unlocked"

        player_prestige.check_prestige_eligibility(player_level, karma_points)
        return True, "Eligible for prestige!"

    @staticmethod
    def perform_prestige(
        player_prestige: PlayerPrestige,
        player_traits: Dict[str, float]
    ) -> Tuple[bool, Dict, Dict[str, float]]:
        """Perform prestige reset"""
        if not player_prestige.can_prestige:
            return False, {}, player_traits

        # Perform prestige
        success = player_prestige.perform_prestige()
        if not success:
            return False, {}, player_traits

        # Calculate trait retention (10% kept)
        new_traits = {}
        kept_percentage = 0.10 + \
            (player_prestige.current_prestige_level * 0.02)  # +2% per prestige
        kept_percentage = min(kept_percentage, 0.50)  # Max 50% retention

        for trait, value in player_traits.items():
            new_traits[trait] = value * kept_percentage

        # Get prestige rewards
        rewards = PRESTIGE_REWARDS.get(
            player_prestige.current_prestige_level, {})

        # Apply permanent bonuses
        if isinstance(rewards, PrestigeReward):
            for bonus_type, bonus_value in rewards.permanent_bonuses.items():
                if bonus_type not in player_prestige.permanent_bonuses:
                    player_prestige.permanent_bonuses[bonus_type] = 1.0
                player_prestige.permanent_bonuses[bonus_type] *= bonus_value

            reward_data = {
                "prestige_points": rewards.prestige_points,
                "exclusive_powers": rewards.exclusive_powers,
                "permanent_bonuses": rewards.permanent_bonuses,
                "cosmetic_rewards": rewards.cosmetic_rewards,
                "traits_kept_percentage": kept_percentage * 100
            }
        else:
            reward_data = {
                "prestige_points": 100,
                "traits_kept_percentage": kept_percentage * 100
            }

        logger.info(
            f"Player prestiged to level {player_prestige.current_prestige_level}")
        return True, reward_data, new_traits

    @staticmethod
    def get_prestige_benefits(player_prestige: PlayerPrestige) -> Dict:
        """Get current prestige benefits"""
        return {
            "current_level": player_prestige.current_prestige_level,
            "total_prestiges": player_prestige.total_prestiges,
            "prestige_points": player_prestige.prestige_points,
            "permanent_bonuses": player_prestige.permanent_bonuses,
            "can_prestige": player_prestige.can_prestige,
            "next_level_rewards": PRESTIGE_REWARDS.get(player_prestige.current_prestige_level + 1)
        }
