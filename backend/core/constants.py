# Game constants and configuration

# Superpower configurations
SUPERPOWERS_CONFIG = {
    "mind_reading": {
        "tier": 1,
        "description": "Read others' intentions and thoughts",
        "requirements": {"empathy": 80, "perception": 70},
        "cooldown_minutes": 5
    },
    "enhanced_reflexes": {
        "tier": 1,
        "description": "Lightning-fast reactions",
        "requirements": {"speed": 75, "dexterity": 70},
        "cooldown_minutes": 3
    },
    "persuasion_aura": {
        "tier": 1,
        "description": "Influence emotions of others",
        "requirements": {"charisma": 80, "negotiation": 75},
        "cooldown_minutes": 10
    },
    "danger_sense": {
        "tier": 1,
        "description": "Detect incoming threats",
        "requirements": {"perception": 80, "survival_instinct": 70},
        "cooldown_minutes": 5
    },
    "quick_heal": {
        "tier": 1,
        "description": "Rapidly recover from injuries",
        "requirements": {"medicine": 75, "resilience": 70},
        "cooldown_minutes": 15
    },
    # Tier 2
    "telekinesis": {
        "tier": 2,
        "description": "Move objects with your mind",
        "requirements": {"meditation": 80, "intelligence": 75},
        "cooldown_minutes": 20
    },
    "invisibility": {
        "tier": 2,
        "description": "Become completely unseen",
        "requirements": {"stealth": 90, "patience": 70},
        "cooldown_minutes": 30
    },
    # More powers can be added
}

# Skill tree configuration
SKILL_TREE_CONFIG = {
    "nodes_per_trait": 20,
    "max_prestiges": 10
}

# Privacy tier costs
PRIVACY_TIER_COSTS = {
    "public": 0,
    "selective": 100,
    "private": 500,
    "ghost": 2000,
    "phantom": 10000
}

# Trait categories
TRAIT_CATEGORIES = {
    "virtues": [
        "empathy", "integrity", "discipline", "creativity", "resilience",
        "curiosity", "kindness", "courage", "patience", "adaptability",
        "wisdom", "humility", "vision", "honesty", "loyalty",
        "generosity", "self_awareness", "gratitude", "optimism", "loveability"
    ],
    "vices": [
        "greed", "arrogance", "deceit", "cruelty", "selfishness",
        "envy", "wrath", "cowardice", "laziness", "gluttony",
        "paranoia", "impulsiveness", "vengefulness", "manipulation", "prejudice",
        "betrayal", "stubbornness", "pessimism", "recklessness", "vanity"
    ],
    "skills": [
        "hacking", "negotiation", "stealth", "leadership", "technical_knowledge",
        "physical_strength", "speed", "intelligence", "charisma", "perception",
        "endurance", "dexterity", "memory", "focus", "networking",
        "strategy", "trading", "engineering", "medicine", "meditation"
    ]
}

# Meta traits
META_TRAITS = [
    "reputation", "influence", "fame", "infamy", "trustworthiness",
    "combat_rating", "tactical_mastery", "survival_instinct",
    "business_acumen", "market_intuition", "wealth_management",
    "enlightenment", "karmic_balance", "divine_favor",
    "guild_loyalty", "political_power", "diplomatic_skill",
    "legendary_status", "mentorship", "historical_impact"
]
