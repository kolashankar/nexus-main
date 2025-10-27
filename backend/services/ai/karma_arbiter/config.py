"""Karma Arbiter Configuration"""


# Karma scales for different action severities
KARMA_SCALES = {
    "minor": {"min": -20, "max": 20, "trait_change": (1, 5)},
    "moderate": {"min": -50, "max": 50, "trait_change": (5, 15)},
    "major": {"min": -100, "max": 100, "trait_change": (15, 30)},
    "critical": {"min": -200, "max": 200, "trait_change": (30, 50)},
}

# Action type to severity mapping
ACTION_SEVERITY = {
    "hack": "moderate",
    "steal": "major",
    "help": "moderate",
    "donate": "moderate",
    "trade": "minor",
    "betray": "critical",
    "save_life": "critical",
}

# Model configuration
MODEL_CONFIG = {
    "default_model": "gpt-4o",
    "fast_model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 1000,
}

# Cache configuration
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 3600,  # 1 hour
    "cache_simple_actions": True,
}
