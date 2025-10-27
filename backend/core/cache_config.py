"""Cache Configuration"""


# Cache TTL configurations (in seconds)
CACHE_TTL = {
    "karma_evaluation": 3600,  # 1 hour
    "quest_generation": 7200,  # 2 hours (though we don't cache quests much)
    "player_profile": 300,  # 5 minutes
    "leaderboards": 600,  # 10 minutes
    "market_prices": 60,  # 1 minute
    "world_state": 120,  # 2 minutes
}

# Cache key prefixes
CACHE_PREFIXES = {
    "ai_karma": "ai_cache:karma_arbiter:",
    "ai_oracle": "ai_cache:oracle:",
    "ai_companion": "ai_cache:companion:",
    "player": "player:",
    "session": "session:",
    "leaderboard": "leaderboard:",
}

# Cache strategies
CACHE_STRATEGIES = {
    "write_through": True,  # Update cache and database simultaneously
    "lazy_loading": True,  # Load data into cache on first access
    "ttl_refresh": True,  # Refresh TTL on access
}
