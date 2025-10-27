"""Oracle Configuration"""


# Quest types and their characteristics
QUEST_TYPES = {
    "personal": {
        "min_level": 1,
        "duration_hours": 24,
        "complexity": "medium",
        "rewards_multiplier": 1.0
    },
    "daily": {
        "min_level": 1,
        "duration_hours": 24,
        "complexity": "low",
        "rewards_multiplier": 0.5
    },
    "weekly": {
        "min_level": 5,
        "duration_hours": 168,  # 7 days
        "complexity": "high",
        "rewards_multiplier": 2.0
    },
    "campaign": {
        "min_level": 10,
        "duration_hours": 720,  # 30 days
        "complexity": "epic",
        "rewards_multiplier": 5.0
    },
    "guild": {
        "min_level": 15,
        "duration_hours": 72,  # 3 days
        "complexity": "high",
        "rewards_multiplier": 3.0
    },
    "world": {
        "min_level": 20,
        "duration_hours": 48,
        "complexity": "medium",
        "rewards_multiplier": 2.5
    },
    "hidden": {
        "min_level": 25,
        "duration_hours": 168,
        "complexity": "very_high",
        "rewards_multiplier": 10.0
    }
}

# Objective types
OBJECTIVE_TYPES = [
    "collect",
    "defeat",
    "talk",
    "hack",
    "trade",
    "visit",
    "craft",
    "donate",
    "protect",
    "discover"
]

# Reward types
REWARD_TYPES = {
    "credits": {"min": 100, "max": 10000},
    "xp": {"min": 50, "max": 5000},
    "karma": {"min": -100, "max": 100},
    "items": [],
    "trait_boosts": {},
    "special": []
}

# Model configuration
MODEL_CONFIG = {
    "default_model": "gpt-4o",
    "fast_model": "gpt-4o-mini",
    "temperature": 0.9,  # Higher for creativity
    "max_tokens": 1500,
}

# Cache configuration
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 7200,  # 2 hours
    "cache_similar_quests": False,  # Each quest should be unique
}
