"""Quest templates - Predefined quest structures"""

from typing import Dict, Any
import random


class QuestTemplates:
    """Provides quest templates for quick generation"""

    COMBAT_TEMPLATES = [
        {
            "title": "Warrior's Challenge",
            "description": "Prove your combat prowess",
            "objectives": [
                {
                    "type": "win_combat",
                    "description": "Win {count} combat battles",
                    "required": 5,
                }
            ],
        },
        {
            "title": "Arena Champion",
            "description": "Dominate the arena",
            "objectives": [
                {
                    "type": "win_duel",
                    "description": "Win {count} duels",
                    "required": 3,
                }
            ],
        },
    ]

    HACKING_TEMPLATES = [
        {
            "title": "Digital Infiltrator",
            "description": "Breach secure systems",
            "objectives": [
                {
                    "type": "hack",
                    "description": "Successfully hack {count} systems",
                    "required": 5,
                }
            ],
        },
    ]

    KARMA_TEMPLATES = [
        {
            "title": "Path to Enlightenment",
            "description": "Earn positive karma",
            "objectives": [
                {
                    "type": "earn_karma",
                    "description": "Earn {count} karma points",
                    "required": 100,
                }
            ],
        },
        {
            "title": "Good Samaritan",
            "description": "Help others",
            "objectives": [
                {
                    "type": "help",
                    "description": "Help {count} players",
                    "required": 5,
                }
            ],
        },
    ]

    ECONOMIC_TEMPLATES = [
        {
            "title": "Master Trader",
            "description": "Engage in commerce",
            "objectives": [
                {
                    "type": "trade",
                    "description": "Complete {count} trades",
                    "required": 10,
                }
            ],
        },
    ]

    @classmethod
    def get_random_template(
        cls,
        category: str = None,
    ) -> Dict[str, Any]:
        """Get a random quest template"""
        if category == "combat":
            templates = cls.COMBAT_TEMPLATES
        elif category == "hacking":
            templates = cls.HACKING_TEMPLATES
        elif category == "karma":
            templates = cls.KARMA_TEMPLATES
        elif category == "economic":
            templates = cls.ECONOMIC_TEMPLATES
        else:
            # Random category
            all_templates = (
                cls.COMBAT_TEMPLATES +
                cls.HACKING_TEMPLATES +
                cls.KARMA_TEMPLATES +
                cls.ECONOMIC_TEMPLATES
            )
            return random.choice(all_templates).copy()

        return random.choice(templates).copy()

    @classmethod
    def get_template_by_traits(
        cls,
        player_traits: Dict[str, int],
    ) -> Dict[str, Any]:
        """Get template based on player's strongest traits"""
        # Find strongest trait
        if not player_traits:
            return cls.get_random_template()

        strongest = max(player_traits.items(), key=lambda x: x[1])
        trait_name, trait_value = strongest

        # Map traits to categories
        if trait_name in ["strength", "dexterity", "courage"]:
            return cls.get_random_template("combat")
        elif trait_name in ["hacking", "technical_knowledge"]:
            return cls.get_random_template("hacking")
        elif trait_name in ["kindness", "empathy", "generosity"]:
            return cls.get_random_template("karma")
        elif trait_name in ["trading", "negotiation"]:
            return cls.get_random_template("economic")
        else:
            return cls.get_random_template()
