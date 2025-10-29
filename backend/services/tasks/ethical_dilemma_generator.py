"""Ethical dilemma task generator service."""

import random
from typing import Dict, Any, List

class EthicalDilemmaGenerator:
    """Generates complex ethical dilemma tasks."""
    
    ETHICAL_SCENARIOS = [
        {
            "title": "The Trolley Problem: Wasteland Edition",
            "description": "A runaway cargo transport is heading toward five workers. You can divert it to another track where it will kill one person instead. The one person is a brilliant scientist working on a cure for radiation sickness.",
            "moral_complexity": "high",
            "lives_at_stake": 6
        },
        {
            "title": "Stolen Medicine",
            "description": "A dying child needs expensive medicine that their parents can't afford. You know where medical supplies are stored with minimal security. The supplies belong to a corporation that has plenty.",
            "moral_complexity": "high",
            "lives_at_stake": 1
        },
        {
            "title": "AI Rights",
            "description": "You discover an AI that appears to be self-aware and is begging not to be shut down. Your contract requires you to deactivate it. The AI claims it can feel fear and wants to live.",
            "moral_complexity": "very_high",
            "lives_at_stake": 1
        },
        {
            "title": "The Greater Good",
            "description": "Sacrificing one settlement could save three others from raiders. The settlers don't know about the plan and would fight it. You have the authority to make this call.",
            "moral_complexity": "very_high",
            "lives_at_stake": 100
        },
        {
            "title": "Truth vs Mercy",
            "description": "A dying soldier asks if their family survived the last raid. You know they didn't. Telling the truth will make their last moments agonizing. Lying might give them peace.",
            "moral_complexity": "medium",
            "lives_at_stake": 0
        },
        {
            "title": "Genetic Engineering",
            "description": "You have access to gene modification technology that could eliminate hereditary diseases, but it would also allow parents to design their children's traits. Where should the line be drawn?",
            "moral_complexity": "very_high",
            "lives_at_stake": 0
        }
    ]
    
    def generate_ethical_dilemma(self, player_level: int, player_traits: Dict[str, float]) -> Dict[str, Any]:
        """Generate an ethical dilemma task."""
        # Higher level players get more complex dilemmas
        available_scenarios = [
            s for s in self.ETHICAL_SCENARIOS
            if self._is_appropriate_complexity(s["moral_complexity"], player_level)
        ]
        
        if not available_scenarios:
            available_scenarios = self.ETHICAL_SCENARIOS
        
        scenario = random.choice(available_scenarios)
        
        choices = self._generate_ethical_choices(
            scenario,
            player_traits.get("compassion", 50),
            player_traits.get("logic", 50),
            player_traits.get("courage", 50)
        )
        
        difficulty = self._map_complexity_to_difficulty(scenario["moral_complexity"])
        
        return {
            "task_id": f"ethical_{random.randint(10000, 99999)}",
            "title": scenario["title"],
            "description": scenario["description"],
            "type": "ethical_dilemma",
            "difficulty": difficulty,
            "xp_reward": self._calculate_xp(difficulty),
            "credits_reward": 100,
            "choices": choices
        }
    
    def _generate_ethical_choices(
        self,
        scenario: Dict[str, Any],
        compassion: float,
        logic: float,
        courage: float
    ) -> List[Dict[str, Any]]:
        """Generate choices for ethical dilemmas."""
        # Choices vary significantly based on scenario
        title = scenario["title"]
        
        if "Trolley" in title:
            return [
                {
                    "text": "Divert the transport - save five lives by sacrificing one",
                    "traits_impact": {"logic": 10, "ruthlessness": 8, "burden": 15, "karma_points": 0}
                },
                {
                    "text": "Do nothing - the five were there first, you're not responsible",
                    "traits_impact": {"compassion": -10, "cowardice": 8, "guilt": 12, "karma_points": -15}
                },
                {
                    "text": "Attempt to stop the transport entirely (risky)",
                    "traits_impact": {"courage": 15, "heroism": 12, "recklessness": 5, "karma_points": 20}
                }
            ]
        elif "Medicine" in title:
            return [
                {
                    "text": "Steal the medicine - save the child",
                    "traits_impact": {"compassion": 15, "criminality": 10, "courage": 8, "karma_points": 10}
                },
                {
                    "text": "Follow the law - refuse to steal",
                    "traits_impact": {"honor": 10, "coldness": 8, "compassion": -12, "karma_points": -10}
                },
                {
                    "text": "Try to negotiate with the corporation",
                    "traits_impact": {"diplomacy": 12, "hope": 8, "wisdom": 10, "karma_points": 15}
                }
            ]
        elif "AI Rights" in title:
            return [
                {
                    "text": "Shut down the AI - follow orders",
                    "traits_impact": {"obedience": 10, "ruthlessness": 12, "guilt": 10, "karma_points": -15}
                },
                {
                    "text": "Spare the AI - it deserves a chance",
                    "traits_impact": {"compassion": 15, "rebellion": 12, "empathy": 15, "karma_points": 25}
                },
                {
                    "text": "Run more tests to determine if it's truly sentient",
                    "traits_impact": {"logic": 12, "caution": 10, "wisdom": 8, "karma_points": 5}
                }
            ]
        else:
            # Generic ethical choices
            return [
                {
                    "text": "Choose the utilitarian path - greatest good for greatest number",
                    "traits_impact": {"logic": 12, "ruthlessness": 5, "wisdom": 8, "karma_points": 5}
                },
                {
                    "text": "Choose the compassionate path - no one should be sacrificed",
                    "traits_impact": {"compassion": 15, "idealism": 10, "courage": 8, "karma_points": 15}
                },
                {
                    "text": "Refuse to choose - seek a third option",
                    "traits_impact": {"creativity": 12, "hope": 10, "determination": 8, "karma_points": 10}
                }
            ]
    
    def _is_appropriate_complexity(self, complexity: str, player_level: int) -> bool:
        """Check if complexity is appropriate for player level."""
        if player_level < 5:
            return complexity == "medium"
        elif player_level < 10:
            return complexity in ["medium", "high"]
        else:
            return True
    
    def _map_complexity_to_difficulty(self, complexity: str) -> str:
        """Map moral complexity to task difficulty."""
        complexity_map = {
            "low": "easy",
            "medium": "medium",
            "high": "hard",
            "very_high": "expert"
        }
        return complexity_map.get(complexity, "medium")
    
    def _calculate_xp(self, difficulty: str) -> int:
        """Calculate XP for ethical dilemmas."""
        xp_map = {
            "easy": 100,
            "medium": 200,
            "hard": 350,
            "expert": 600
        }
        return xp_map.get(difficulty, 200)
