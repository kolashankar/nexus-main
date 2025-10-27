"""Action effects and consequences"""
from typing import Dict
import random

class ActionEffects:
    """Calculate and apply action effects"""

    @staticmethod
    def calculate_trait_effects(action_type: str, success: bool) -> Dict[str, float]:
        """Calculate trait changes based on action"""
        effects = {}

        if action_type == "hack":
            if success:
                effects["hacking"] = random.uniform(0.5, 2.0)
                effects["technical_knowledge"] = random.uniform(0.3, 1.0)
                effects["deceit"] = random.uniform(0.2, 0.8)
            else:
                effects["hacking"] = random.uniform(-0.5, 0.5)

        elif action_type == "help":
            effects["kindness"] = random.uniform(1.0, 3.0)
            effects["empathy"] = random.uniform(0.5, 2.0)
            effects["generosity"] = random.uniform(0.5, 1.5)

        elif action_type == "steal":
            if success:
                effects["stealth"] = random.uniform(0.5, 2.0)
                effects["greed"] = random.uniform(0.5, 1.5)
                effects["deceit"] = random.uniform(0.3, 1.0)
            else:
                effects["stealth"] = random.uniform(-1.0, 0)
                effects["shame"] = random.uniform(0.5, 1.5)

        elif action_type == "donate":
            effects["generosity"] = random.uniform(1.5, 3.5)
            effects["kindness"] = random.uniform(1.0, 2.5)
            effects["selflessness"] = random.uniform(0.5, 2.0)

        elif action_type == "trade":
            effects["negotiation"] = random.uniform(0.5, 2.0)
            effects["trading"] = random.uniform(0.5, 1.5)
            effects["charisma"] = random.uniform(0.3, 1.0)

        return effects

    @staticmethod
    def calculate_karma_effect(action_type: str, success: bool, amount: int = 0) -> int:
        """Calculate karma change"""
        karma_map = {
            "hack": -15 if success else -5,
            "help": 10,
            "steal": -25 if success else -10,
            "donate": max(15, amount // 10),
            "trade": 3
        }
        return karma_map.get(action_type, 0)
