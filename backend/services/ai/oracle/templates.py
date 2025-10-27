"""Quest Templates for common quest patterns"""


# Quest templates for quick generation
QUEST_TEMPLATES = {
    "help_npc": {
        "title_template": "Help {npc_name} with {task}",
        "description_template": "A local {npc_type} needs your assistance with {problem}.",
        "objective_types": ["talk", "collect", "deliver"],
        "karma_impact": "positive"
    },
    "defeat_enemy": {
        "title_template": "Defeat {enemy_count} {enemy_type}",
        "description_template": "{location} is under threat from {enemy_type}. Clear them out.",
        "objective_types": ["defeat"],
        "karma_impact": "varies"
    },
    "collect_items": {
        "title_template": "Gather {item_count} {item_name}",
        "description_template": "Collect {item_count} {item_name} from {location}.",
        "objective_types": ["collect"],
        "karma_impact": "neutral"
    },
    "moral_dilemma": {
        "title_template": "The {dilemma_type} Dilemma",
        "description_template": "You face a choice that will define your character.",
        "objective_types": ["talk", "choose"],
        "karma_impact": "major"
    },
    "investigation": {
        "title_template": "Investigate {mystery}",
        "description_template": "Something suspicious is happening. Uncover the truth.",
        "objective_types": ["discover", "talk", "hack"],
        "karma_impact": "varies"
    },
    "trade_mission": {
        "title_template": "Trading {item_name}",
        "description_template": "Transport and trade {item_name} for profit.",
        "objective_types": ["trade", "visit"],
        "karma_impact": "neutral"
    },
    "protection": {
        "title_template": "Protect {target}",
        "description_template": "Keep {target} safe from {threat} for {duration}.",
        "objective_types": ["protect"],
        "karma_impact": "positive"
    },
    "hacking": {
        "title_template": "Hack {target_system}",
        "description_template": "Break into {target_system} and {objective}.",
        "objective_types": ["hack"],
        "karma_impact": "negative"
    },
    "donation": {
        "title_template": "Support {cause}",
        "description_template": "Help {cause} by donating {resource}.",
        "objective_types": ["donate"],
        "karma_impact": "positive"
    },
    "discovery": {
        "title_template": "Discover {location}",
        "description_template": "Explore and discover the secrets of {location}.",
        "objective_types": ["discover", "visit"],
        "karma_impact": "neutral"
    }
}

# Campaign templates
CAMPAIGN_TEMPLATES = {
    "redemption": {
        "theme": "redemption",
        "chapter_count": 10,
        "description": "A journey from darkness to light",
        "karma_progression": "negative_to_positive"
    },
    "corruption": {
        "theme": "corruption",
        "chapter_count": 8,
        "description": "The descent into darkness",
        "karma_progression": "positive_to_negative"
    },
    "discovery": {
        "theme": "discovery",
        "chapter_count": 12,
        "description": "Uncovering ancient secrets",
        "karma_progression": "neutral"
    },
    "revenge": {
        "theme": "revenge",
        "chapter_count": 7,
        "description": "Seeking justice or vengeance",
        "karma_progression": "varies"
    },
    "love": {
        "theme": "love",
        "chapter_count": 6,
        "description": "A tale of romance and sacrifice",
        "karma_progression": "positive"
    },
    "power": {
        "theme": "power",
        "chapter_count": 9,
        "description": "The pursuit of ultimate power",
        "karma_progression": "varies"
    }
}

# NPC types for quest generation
NPC_TYPES = [
    "merchant", "scientist", "hacker", "doctor", "engineer",
    "artist", "criminal", "detective", "politician", "rebel",
    "AI entity", "companion", "rival", "mentor", "stranger"
]

# Location types
LOCATION_TYPES = [
    "cyberpunk district", "corporate tower", "underground market",
    "research facility", "slums", "luxury district", "industrial zone",
    "data center", "virtual reality hub", "abandoned sector"
]

# Moral dilemma types
DILEMMA_TYPES = [
    "trolley problem", "sacrifice", "betrayal", "truth vs lie",
    "justice vs mercy", "freedom vs security", "individual vs collective",
    "ends vs means", "loyalty vs morality", "life vs principle"
]
