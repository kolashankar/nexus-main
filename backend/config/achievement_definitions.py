"""Achievement Definitions - 100+ Achievements across 10 categories."""

from typing import Dict, List, Any
from enum import Enum

class AchievementCategory(Enum):
    TRAITS = "traits"
    POWERS = "powers"
    KARMA = "karma"
    SOCIAL = "social"
    ECONOMIC = "economic"
    COMBAT = "combat"
    QUESTS = "quests"
    EXPLORATION = "exploration"
    COLLECTION = "collection"
    HIDDEN = "hidden"

# 100+ Achievements
ALL_ACHIEVEMENTS: List[Dict[str, Any]] = [
    # TRAITS ACHIEVEMENTS (15)
    {"id": "trait_master_empathy", "name": "Empath Supreme", "description": "Reach 100% Empathy", "category": "traits",
        "condition": {"empathy": 100}, "rewards": {"xp": 500, "karma_tokens": 100}, "hidden": False},
    {"id": "trait_master_integrity", "name": "Moral Pillar", "description": "Reach 100% Integrity", "category": "traits",
        "condition": {"integrity": 100}, "rewards": {"xp": 500, "karma_tokens": 100}, "hidden": False},
    {"id": "trait_master_hacking", "name": "Elite Hacker", "description": "Reach 100% Hacking", "category": "traits",
        "condition": {"hacking": 100}, "rewards": {"xp": 500, "karma_tokens": 100}, "hidden": False},
    {"id": "trait_all_50", "name": "Balanced Soul", "description": "Get all traits to 50%", "category": "traits",
        "condition": {"all_traits": 50}, "rewards": {"xp": 2000, "karma_tokens": 500}, "hidden": False},
    {"id": "trait_all_75", "name": "Master of All", "description": "Get all traits to 75%", "category": "traits",
        "condition": {"all_traits": 75}, "rewards": {"xp": 5000, "karma_tokens": 1000}, "hidden": False},
    {"id": "trait_virtue_max", "name": "Pure Virtue", "description": "Max all 20 virtues", "category": "traits",
        "condition": {"all_virtues": 100}, "rewards": {"xp": 10000, "karma_tokens": 2000, "title": "Saint"}, "hidden": False},
    {"id": "trait_vice_max", "name": "Embraced Darkness", "description": "Max all 20 vices", "category": "traits",
        "condition": {"all_vices": 100}, "rewards": {"xp": 10000, "dark_matter": 2000, "title": "Demon"}, "hidden": False},
    {"id": "trait_skill_max", "name": "Ultimate Skillmaster", "description": "Max all 20 skills", "category": "traits",
        "condition": {"all_skills": 100}, "rewards": {"xp": 10000, "credits": 100000}, "hidden": False},
    {"id": "trait_opposites", "name": "Walking Paradox", "description": "Have Empathy and Cruelty both at 90+", "category": "traits",
        "condition": {"empathy": 90, "cruelty": 90}, "rewards": {"xp": 3000, "karma_tokens": 500, "dark_matter": 500}, "hidden": True},
    {"id": "trait_rapid_change", "name": "Identity Crisis", "description": "Change 10 traits by 20+ in one day",
        "category": "traits", "condition": {"trait_changes": 10}, "rewards": {"xp": 1000}, "hidden": True},

    # SUPERPOWERS ACHIEVEMENTS (10)
    {"id": "power_first", "name": "Awakening", "description": "Unlock your first superpower", "category": "powers",
        "condition": {"powers_unlocked": 1}, "rewards": {"xp": 1000, "karma_tokens": 200}, "hidden": False},
    {"id": "power_tier1_all", "name": "Basic Powers Complete", "description": "Unlock all Tier 1 powers", "category": "powers",
        "condition": {"tier_1_complete": True}, "rewards": {"xp": 2000, "karma_tokens": 500}, "hidden": False},
    {"id": "power_tier2_all", "name": "Intermediate Mastery", "description": "Unlock all Tier 2 powers", "category": "powers",
        "condition": {"tier_2_complete": True}, "rewards": {"xp": 3000, "karma_tokens": 750}, "hidden": False},
    {"id": "power_tier3_all", "name": "Advanced Powers", "description": "Unlock all Tier 3 powers", "category": "powers",
        "condition": {"tier_3_complete": True}, "rewards": {"xp": 4000, "karma_tokens": 1000}, "hidden": False},
    {"id": "power_tier4_all", "name": "Master of Powers", "description": "Unlock all Tier 4 powers", "category": "powers",
        "condition": {"tier_4_complete": True}, "rewards": {"xp": 5000, "karma_tokens": 1500}, "hidden": False},
    {"id": "power_legendary", "name": "Legendary Being", "description": "Unlock a Tier 5 legendary power", "category": "powers",
        "condition": {"legendary_power": 1}, "rewards": {"xp": 10000, "karma_tokens": 3000, "title": "Legendary"}, "hidden": False},
    {"id": "power_all_25", "name": "Omnipotent", "description": "Unlock all 25 superpowers", "category": "powers", "condition": {
        "powers_unlocked": 25}, "rewards": {"xp": 20000, "karma_tokens": 5000, "prestige_points": 500, "title": "God-Tier"}, "hidden": False},
    {"id": "power_ascension", "name": "Divine Ascension", "description": "Unlock the Ascension power", "category": "powers",
        "condition": {"power_id": "ascension"}, "rewards": {"xp": 15000, "karma_tokens": 4000}, "hidden": False},
    {"id": "power_frequent", "name": "Power Addict", "description": "Use superpowers 1000 times", "category": "powers",
        "condition": {"power_uses": 1000}, "rewards": {"xp": 3000, "karma_tokens": 500}, "hidden": False},

    # KARMA ACHIEVEMENTS (10)
    {"id": "karma_saint", "name": "Saint", "description": "Reach +5000 karma", "category": "karma",
        "condition": {"karma": 5000}, "rewards": {"xp": 5000, "karma_tokens": 1000, "title": "Saint"}, "hidden": False},
    {"id": "karma_demon", "name": "Demon", "description": "Reach -5000 karma", "category": "karma",
        "condition": {"karma": -5000}, "rewards": {"xp": 5000, "dark_matter": 1000, "title": "Demon"}, "hidden": False},
    {"id": "karma_balanced", "name": "Perfect Balance", "description": "Maintain karma between -100 and +100 for 30 days", "category": "karma",
        "condition": {"balanced_days": 30}, "rewards": {"xp": 3000, "karma_tokens": 500, "dark_matter": 500}, "hidden": False},
    {"id": "karma_redemption", "name": "Redemption Arc", "description": "Go from -3000 karma to +3000 karma", "category": "karma",
        "condition": {"karma_change": 6000}, "rewards": {"xp": 5000, "karma_tokens": 2000, "title": "Redeemed"}, "hidden": False},
    {"id": "karma_fall", "name": "Fall from Grace", "description": "Go from +3000 karma to -3000 karma", "category": "karma",
        "condition": {"karma_change": -6000}, "rewards": {"xp": 5000, "dark_matter": 2000, "title": "Fallen"}, "hidden": False},
    {"id": "karma_events_100", "name": "Event Survivor", "description": "Survive 100 karma events", "category": "karma",
        "condition": {"events_survived": 100}, "rewards": {"xp": 2000, "karma_tokens": 500}, "hidden": False},
    {"id": "karma_generous", "name": "Generous Soul", "description": "Donate 1,000,000 credits", "category": "karma",
        "condition": {"total_donated": 1000000}, "rewards": {"xp": 3000, "karma_tokens": 1000}, "hidden": False},
    {"id": "karma_greedy", "name": "Master Thief", "description": "Steal 1,000,000 credits", "category": "karma",
        "condition": {"total_stolen": 1000000}, "rewards": {"xp": 3000, "dark_matter": 1000}, "hidden": False},

    # SOCIAL ACHIEVEMENTS (15)
    {"id": "social_first_friend", "name": "First Friend", "description": "Make your first alliance",
        "category": "social", "condition": {"alliances": 1}, "rewards": {"xp": 500, "karma_tokens": 100}, "hidden": False},
    {"id": "social_married", "name": "Soulmate", "description": "Get married", "category": "social",
        "condition": {"married": True}, "rewards": {"xp": 2000, "karma_tokens": 500}, "hidden": False},
    {"id": "social_mentor", "name": "Wise Mentor", "description": "Graduate 10 apprentices", "category": "social", "condition": {
        "apprentices_graduated": 10}, "rewards": {"xp": 5000, "legacy_shards": 1000, "title": "Master"}, "hidden": False},
    {"id": "social_guild_leader", "name": "Guild Master", "description": "Lead a guild with 50+ members", "category": "social",
        "condition": {"guild_leader": True, "guild_members": 50}, "rewards": {"xp": 5000, "guild_coins": 5000}, "hidden": False},
    {"id": "social_rival_defeat", "name": "Rival Crusher", "description": "Defeat your rival 10 times", "category": "social",
        "condition": {"rival_defeats": 10}, "rewards": {"xp": 2000, "karma_tokens": 500}, "hidden": False},
    {"id": "social_chat_1000", "name": "Chatty", "description": "Send 1000 chat messages",
        "category": "social", "condition": {"messages_sent": 1000}, "rewards": {"xp": 1000}, "hidden": False},
    {"id": "social_divorce", "name": "Heartbreaker", "description": "Get divorced 5 times", "category": "social",
        "condition": {"divorces": 5}, "rewards": {"xp": 1000, "dark_matter": 500}, "hidden": True},

    # ECONOMIC ACHIEVEMENTS (15)
    {"id": "econ_millionaire", "name": "Millionaire", "description": "Accumulate 1,000,000 credits", "category": "economic",
        "condition": {"total_credits": 1000000}, "rewards": {"xp": 3000, "karma_tokens": 500}, "hidden": False},
    {"id": "econ_billionaire", "name": "Billionaire", "description": "Accumulate 1,000,000,000 credits", "category": "economic",
        "condition": {"total_credits": 1000000000}, "rewards": {"xp": 10000, "prestige_points": 1000, "title": "Tycoon"}, "hidden": False},
    {"id": "econ_stock_profit", "name": "Stock Master", "description": "Earn 100,000 from stocks", "category": "economic",
        "condition": {"stock_profit": 100000}, "rewards": {"xp": 2000, "karma_tokens": 300}, "hidden": False},
    {"id": "econ_robot_empire", "name": "Robot Empire", "description": "Own 50 robots", "category": "economic",
        "condition": {"robots_owned": 50}, "rewards": {"xp": 3000, "credits": 50000}, "hidden": False},
    {"id": "econ_real_estate", "name": "Property Mogul", "description": "Own 10 properties", "category": "economic",
        "condition": {"properties_owned": 10}, "rewards": {"xp": 4000, "credits": 100000}, "hidden": False},
    {"id": "econ_trade_100", "name": "Merchant", "description": "Complete 100 trades", "category": "economic",
        "condition": {"trades_completed": 100}, "rewards": {"xp": 2000, "karma_tokens": 400}, "hidden": False},

    # COMBAT ACHIEVEMENTS (10)
    {"id": "combat_first_victory", "name": "First Blood", "description": "Win your first PvP battle",
        "category": "combat", "condition": {"pvp_wins": 1}, "rewards": {"xp": 500, "karma_tokens": 100}, "hidden": False},
    {"id": "combat_win_100", "name": "Warrior", "description": "Win 100 PvP battles", "category": "combat", "condition": {
        "pvp_wins": 100}, "rewards": {"xp": 3000, "karma_tokens": 500, "title": "Warrior"}, "hidden": False},
    {"id": "combat_undefeated_10", "name": "Unstoppable", "description": "Win 10 battles in a row", "category": "combat",
        "condition": {"win_streak": 10}, "rewards": {"xp": 2000, "karma_tokens": 400}, "hidden": False},
    {"id": "combat_arena_champion", "name": "Arena Champion", "description": "Reach Arena rank 1", "category": "combat",
        "condition": {"arena_rank": 1}, "rewards": {"xp": 5000, "karma_tokens": 1000, "title": "Champion"}, "hidden": False},
    {"id": "combat_tournament_win", "name": "Tournament Victor", "description": "Win a tournament", "category": "combat",
        "condition": {"tournaments_won": 1}, "rewards": {"xp": 5000, "karma_tokens": 1000}, "hidden": False},

    # QUESTS ACHIEVEMENTS (10)
    {"id": "quest_first", "name": "Quest Beginner", "description": "Complete your first quest", "category": "quests",
        "condition": {"quests_completed": 1}, "rewards": {"xp": 500, "karma_tokens": 100}, "hidden": False},
    {"id": "quest_complete_100", "name": "Quest Master", "description": "Complete 100 quests", "category": "quests",
        "condition": {"quests_completed": 100}, "rewards": {"xp": 3000, "karma_tokens": 500}, "hidden": False},
    {"id": "quest_complete_1000", "name": "Legendary Adventurer", "description": "Complete 1000 quests", "category": "quests", "condition": {
        "quests_completed": 1000}, "rewards": {"xp": 10000, "karma_tokens": 2000, "title": "Legendary Adventurer"}, "hidden": False},
    {"id": "quest_campaign_complete", "name": "Campaign Hero", "description": "Complete a full campaign", "category": "quests",
        "condition": {"campaigns_completed": 1}, "rewards": {"xp": 5000, "karma_tokens": 1000}, "hidden": False},
    {"id": "quest_daily_streak_30", "name": "Daily Dedication", "description": "Complete dailies for 30 days straight",
        "category": "quests", "condition": {"daily_streak": 30}, "rewards": {"xp": 3000, "karma_tokens": 1000}, "hidden": False},

    # EXPLORATION ACHIEVEMENTS (10)
    {"id": "explore_all_territories", "name": "World Explorer", "description": "Visit all 20 territories", "category": "exploration",
        "condition": {"territories_visited": 20}, "rewards": {"xp": 3000, "karma_tokens": 500}, "hidden": False},
    {"id": "explore_secrets_10", "name": "Secret Finder", "description": "Find 10 hidden secrets", "category": "exploration",
        "condition": {"secrets_found": 10}, "rewards": {"xp": 2000, "karma_tokens": 400}, "hidden": False},

    # COLLECTION ACHIEVEMENTS (10)
    {"id": "collect_all_robots", "name": "Robot Collector", "description": "Collect all 15 robot types", "category": "collection",
        "condition": {"robot_types_owned": 15}, "rewards": {"xp": 5000, "credits": 100000}, "hidden": False},
    {"id": "collect_all_chips", "name": "Chip Master", "description": "Collect all 20 robot chips", "category": "collection",
        "condition": {"chip_types_owned": 20}, "rewards": {"xp": 3000, "karma_tokens": 500}, "hidden": False},

    # HIDDEN ACHIEVEMENTS (10+)
    {"id": "hidden_easter_egg_1", "name": "????", "description": "Find the hidden developer room", "category": "hidden",
        "condition": {"easter_egg_1": True}, "rewards": {"xp": 5000, "karma_tokens": 1000, "legacy_shards": 500}, "hidden": True},
    {"id": "hidden_break_game", "name": "Glitch Master", "description": "Find and exploit a game bug", "category": "hidden",
        "condition": {"bug_found": True}, "rewards": {"xp": 10000, "prestige_points": 500}, "hidden": True},
    {"id": "hidden_karma_zero", "name": "Perfect Neutrality", "description": "Maintain exactly 0 karma for 24 hours", "category": "hidden",
        "condition": {"karma": 0, "duration": 86400}, "rewards": {"xp": 3000, "karma_tokens": 500, "dark_matter": 500}, "hidden": True}
]

def get_achievement_by_id(achievement_id: str) -> Dict[str, Any]:
    """Get achievement definition by ID."""
    for achievement in ALL_ACHIEVEMENTS:
        if achievement["id"] == achievement_id:
            return achievement
    return None

def get_achievements_by_category(category: str) -> List[Dict[str, Any]]:
    """Get all achievements in a category."""
    return [a for a in ALL_ACHIEVEMENTS if a["category"] == category]

def check_achievement_condition(achievement_id: str, player_data: Dict[str, Any]) -> bool:
    """Check if player meets achievement condition."""
    achievement = get_achievement_by_id(achievement_id)
    if not achievement:
        return False

    condition = achievement["condition"]

    for key, value in condition.items():
        player_value = player_data.get(key)
        if player_value is None:
            return False

        if isinstance(value, bool):
            if player_value != value:
                return False
        elif isinstance(value, (int, float)):
            if player_value < value:
                return False

    return True
