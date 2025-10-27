from typing import Dict, List, Optional, Tuple
from backend.models.achievements import (
    PlayerAchievements, AchievementDefinition, AchievementCategory,
    AchievementRarity, AchievementProgress
)
import logging

logger = logging.getLogger(__name__)

# Achievement definitions (100+ achievements)
ACHIEVEMENT_DEFINITIONS = {
    # Trait Mastery (20 achievements)
    "trait_master_empathy": AchievementDefinition(
        achievement_id="trait_master_empathy",
        name="Master of Empathy",
        description="Reach 100% Empathy",
        category=AchievementCategory.TRAIT_MASTERY,
        rarity=AchievementRarity.RARE,
        icon="empathy_icon",
        points=50,
        requirements={"trait": "empathy", "value": 100}
    ),
    "trait_master_hacking": AchievementDefinition(
        achievement_id="trait_master_hacking",
        name="Elite Hacker",
        description="Reach 100% Hacking",
        category=AchievementCategory.TRAIT_MASTERY,
        rarity=AchievementRarity.RARE,
        icon="hacking_icon",
        points=50,
        requirements={"trait": "hacking", "value": 100}
    ),
    "trait_master_wisdom": AchievementDefinition(
        achievement_id="trait_master_wisdom",
        name="Ancient Wisdom",
        description="Reach 100% Wisdom",
        category=AchievementCategory.TRAIT_MASTERY,
        rarity=AchievementRarity.RARE,
        icon="wisdom_icon",
        points=50,
        requirements={"trait": "wisdom", "value": 100}
    ),
    "multi_trait_master": AchievementDefinition(
        achievement_id="multi_trait_master",
        name="Polymath",
        description="Master 5 different traits",
        category=AchievementCategory.TRAIT_MASTERY,
        rarity=AchievementRarity.EPIC,
        icon="polymath_icon",
        points=200,
        requirements={"mastered_traits": 5}
    ),

    # Power Collector (10 achievements)
    "first_power": AchievementDefinition(
        achievement_id="first_power",
        name="Awakening",
        description="Unlock your first superpower",
        category=AchievementCategory.POWER_COLLECTOR,
        rarity=AchievementRarity.COMMON,
        icon="first_power_icon",
        points=25
    ),
    "tier_1_complete": AchievementDefinition(
        achievement_id="tier_1_complete",
        name="Basic Training",
        description="Unlock all Tier 1 powers",
        category=AchievementCategory.POWER_COLLECTOR,
        rarity=AchievementRarity.UNCOMMON,
        icon="tier1_icon",
        points=75
    ),
    "all_powers_unlocked": AchievementDefinition(
        achievement_id="all_powers_unlocked",
        name="God Among Men",
        description="Unlock all 25 superpowers",
        category=AchievementCategory.POWER_COLLECTOR,
        rarity=AchievementRarity.LEGENDARY,
        icon="godlike_icon",
        points=500
    ),

    # Karma Achievements (15 achievements)
    "karma_saint": AchievementDefinition(
        achievement_id="karma_saint",
        name="Saint",
        description="Reach 5000 karma",
        category=AchievementCategory.KARMA,
        rarity=AchievementRarity.EPIC,
        icon="saint_icon",
        points=150
    ),
    "karma_demon": AchievementDefinition(
        achievement_id="karma_demon",
        name="Demon",
        description="Reach -5000 karma",
        category=AchievementCategory.KARMA,
        rarity=AchievementRarity.EPIC,
        icon="demon_icon",
        points=150
    ),
    "karma_balanced": AchievementDefinition(
        achievement_id="karma_balanced",
        name="Perfect Balance",
        description="Maintain karma between -50 and +50 for 7 days",
        category=AchievementCategory.KARMA,
        rarity=AchievementRarity.RARE,
        icon="balance_icon",
        points=100
    ),
    "karma_redemption": AchievementDefinition(
        achievement_id="karma_redemption",
        name="Redemption Arc",
        description="Go from -1000 karma to +1000 karma",
        category=AchievementCategory.KARMA,
        rarity=AchievementRarity.EPIC,
        icon="redemption_icon",
        points=200
    ),

    # Social Achievements (15 achievements)
    "first_friend": AchievementDefinition(
        achievement_id="first_friend",
        name="Socialite",
        description="Form your first alliance",
        category=AchievementCategory.SOCIAL,
        rarity=AchievementRarity.COMMON,
        icon="friend_icon",
        points=15
    ),
    "guild_founder": AchievementDefinition(
        achievement_id="guild_founder",
        name="Guild Founder",
        description="Create a guild",
        category=AchievementCategory.SOCIAL,
        rarity=AchievementRarity.UNCOMMON,
        icon="guild_icon",
        points=50
    ),
    "married": AchievementDefinition(
        achievement_id="married",
        name="Til Death Do Us Part",
        description="Get married to another player",
        category=AchievementCategory.SOCIAL,
        rarity=AchievementRarity.RARE,
        icon="marriage_icon",
        points=100
    ),
    "mentor": AchievementDefinition(
        achievement_id="mentor",
        name="Wise Mentor",
        description="Guide 5 apprentices to level 50",
        category=AchievementCategory.SOCIAL,
        rarity=AchievementRarity.EPIC,
        icon="mentor_icon",
        points=200
    ),

    # Economic Achievements (15 achievements)
    "first_million": AchievementDefinition(
        achievement_id="first_million",
        name="Millionaire",
        description="Accumulate 1,000,000 credits",
        category=AchievementCategory.ECONOMIC,
        rarity=AchievementRarity.UNCOMMON,
        icon="millionaire_icon",
        points=50
    ),
    "billionaire": AchievementDefinition(
        achievement_id="billionaire",
        name="Billionaire",
        description="Accumulate 1,000,000,000 credits",
        category=AchievementCategory.ECONOMIC,
        rarity=AchievementRarity.LEGENDARY,
        icon="billionaire_icon",
        points=500
    ),
    "stock_tycoon": AchievementDefinition(
        achievement_id="stock_tycoon",
        name="Stock Market Tycoon",
        description="Earn 100,000 credits from stock trading",
        category=AchievementCategory.ECONOMIC,
        rarity=AchievementRarity.RARE,
        icon="stocks_icon",
        points=75
    ),
    "robot_collector": AchievementDefinition(
        achievement_id="robot_collector",
        name="Robot Collector",
        description="Own all 15 robot types",
        category=AchievementCategory.ECONOMIC,
        rarity=AchievementRarity.EPIC,
        icon="robots_icon",
        points=150
    ),

    # Combat Achievements (15 achievements)
    "first_victory": AchievementDefinition(
        achievement_id="first_victory",
        name="First Blood",
        description="Win your first PvP battle",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.COMMON,
        icon="victory_icon",
        points=20
    ),
    "undefeated": AchievementDefinition(
        achievement_id="undefeated",
        name="Undefeated Champion",
        description="Win 50 PvP battles in a row",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.LEGENDARY,
        icon="champion_icon",
        points=500
    ),
    "arena_master": AchievementDefinition(
        achievement_id="arena_master",
        name="Arena Master",
        description="Reach rank 1 in Arena",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.EPIC,
        icon="arena_icon",
        points=200
    ),
    "guild_warrior": AchievementDefinition(
        achievement_id="guild_warrior",
        name="Guild Warrior",
        description="Participate in 10 guild wars",
        category=AchievementCategory.COMBAT,
        rarity=AchievementRarity.UNCOMMON,
        icon="war_icon",
        points=75
    ),

    # Story Achievements (10 achievements)
    "quest_beginner": AchievementDefinition(
        achievement_id="quest_beginner",
        name="Quest Beginner",
        description="Complete your first quest",
        category=AchievementCategory.STORY,
        rarity=AchievementRarity.COMMON,
        icon="quest_icon",
        points=10
    ),
    "campaign_hero": AchievementDefinition(
        achievement_id="campaign_hero",
        name="Campaign Hero",
        description="Complete a full story campaign",
        category=AchievementCategory.STORY,
        rarity=AchievementRarity.RARE,
        icon="hero_icon",
        points=100
    ),
    "daily_dedication": AchievementDefinition(
        achievement_id="daily_dedication",
        name="Daily Dedication",
        description="Complete daily quests for 30 days straight",
        category=AchievementCategory.STORY,
        rarity=AchievementRarity.EPIC,
        icon="dedication_icon",
        points=150
    ),

    # Hidden Achievements (10 achievements)
    "secret_explorer": AchievementDefinition(
        achievement_id="secret_explorer",
        name="???",
        description="Discover a hidden location",
        category=AchievementCategory.HIDDEN,
        rarity=AchievementRarity.RARE,
        icon="mystery_icon",
        points=100,
        hidden=True
    ),
    "easter_egg_hunter": AchievementDefinition(
        achievement_id="easter_egg_hunter",
        name="???",
        description="Find all easter eggs",
        category=AchievementCategory.HIDDEN,
        rarity=AchievementRarity.LEGENDARY,
        icon="egg_icon",
        points=500,
        hidden=True
    ),
}

class AchievementService:
    """Service for managing player achievements"""

    @staticmethod
    def initialize_achievements(player_id: str) -> PlayerAchievements:
        """Initialize achievements for a new player"""
        return PlayerAchievements(player_id=player_id)

    @staticmethod
    def check_achievement(
        player_achievements: PlayerAchievements,
        achievement_id: str,
        player_data: Dict
    ) -> Tuple[bool, Optional[AchievementDefinition]]:
        """Check if achievement should be unlocked"""
        if achievement_id not in ACHIEVEMENT_DEFINITIONS:
            return False, None

        definition = ACHIEVEMENT_DEFINITIONS[achievement_id]

        # Check if already unlocked (and not repeatable)
        if any(a.achievement_id == achievement_id for a in player_achievements.unlocked_achievements):
            if not definition.repeatable:
                return False, None

        # Check requirements based on category
        requirements_met = AchievementService._check_requirements(
            definition, player_data
        )

        if requirements_met:
            return True, definition

        return False, None

    @staticmethod
    def _check_requirements(definition: AchievementDefinition, player_data: Dict) -> bool:
        """Check if requirements are met"""
        requirements = definition.requirements

        if "trait" in requirements:
            trait_name = requirements["trait"]
            trait_value = requirements["value"]
            if player_data.get("traits", {}).get(trait_name, 0) >= trait_value:
                return True

        if "mastered_traits" in requirements:
            count = requirements["mastered_traits"]
            mastered = sum(1 for v in player_data.get(
                "traits", {}).values() if v >= 100)
            if mastered >= count:
                return True

        if "karma" in requirements:
            if player_data.get("karma_points", 0) >= requirements["karma"]:
                return True

        if "level" in requirements:
            if player_data.get("level", 0) >= requirements["level"]:
                return True

        return False

    @staticmethod
    def unlock_achievement(
        player_achievements: PlayerAchievements,
        achievement_id: str
    ) -> Tuple[bool, str]:
        """Unlock an achievement"""
        if achievement_id not in ACHIEVEMENT_DEFINITIONS:
            return False, "Achievement not found"

        definition = ACHIEVEMENT_DEFINITIONS[achievement_id]
        success = player_achievements.unlock_achievement(
            achievement_id, definition)

        if success:
            return True, f"Achievement unlocked: {definition.name}!"
        return False, "Achievement already unlocked"

    @staticmethod
    def update_progress(
        player_achievements: PlayerAchievements,
        achievement_id: str,
        progress_amount: int
    ):
        """Update progress towards an achievement"""
        if achievement_id not in player_achievements.achievement_progress:
            definition = ACHIEVEMENT_DEFINITIONS.get(achievement_id)
            if definition:
                player_achievements.achievement_progress[achievement_id] = AchievementProgress(
                    achievement_id=achievement_id,
                    required_progress=definition.requirements.get("count", 1)
                )

        if achievement_id in player_achievements.achievement_progress:
            player_achievements.achievement_progress[achievement_id].update_progress(
                progress_amount)

    @staticmethod
    def get_category_achievements(category: AchievementCategory) -> List[AchievementDefinition]:
        """Get all achievements in a category"""
        return [a for a in ACHIEVEMENT_DEFINITIONS.values() if a.category == category]

    @staticmethod
    def get_achievement_summary(player_achievements: PlayerAchievements) -> Dict:
        """Get achievement summary"""
        total_achievements = len(ACHIEVEMENT_DEFINITIONS)
        unlocked_count = len(player_achievements.unlocked_achievements)

        # Count by rarity
        rarity_counts = {}
        for achievement in player_achievements.unlocked_achievements:
            rarity = achievement.rarity
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1

        return {
            "total_achievements": total_achievements,
            "unlocked": unlocked_count,
            "completion_percentage": (unlocked_count / total_achievements) * 100,
            "total_points": player_achievements.total_points,
            "by_rarity": rarity_counts,
            "recent_unlocks": player_achievements.recent_unlocks[:5]
        }
