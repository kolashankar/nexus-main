"""Combat task generator service."""

import random
from typing import Dict, Any, List
from backend.models.tasks.task_types import CombatOutcome

class CombatTaskGenerator:
    """Generates combat scenario tasks."""
    
    COMBAT_SCENARIOS = [
        {
            "title": "Ambushed by Bandits",
            "description": "While traveling through the wasteland, you're ambushed by a group of bandits. They demand your credits. You're outnumbered 3 to 1.",
            "enemy_type": "bandits",
            "enemy_count": 3,
            "difficulty": "medium"
        },
        {
            "title": "Rogue AI Encounter",
            "description": "A malfunctioning combat AI blocks your path. Its weapons are charging. You have seconds to decide.",
            "enemy_type": "ai",
            "enemy_count": 1,
            "difficulty": "hard"
        },
        {
            "title": "Guild Territory Dispute",
            "description": "You've accidentally entered rival guild territory. Their enforcers approach with weapons drawn.",
            "enemy_type": "guild_enforcers",
            "enemy_count": 4,
            "difficulty": "hard"
        },
        {
            "title": "Wild Creature Attack",
            "description": "A mutated wasteland creature lunges at you from the shadows. It's hungry and aggressive.",
            "enemy_type": "creature",
            "enemy_count": 1,
            "difficulty": "easy"
        },
        {
            "title": "Corporate Security",
            "description": "Corporate security has caught you in a restricted area. They're calling for backup.",
            "enemy_type": "security",
            "enemy_count": 2,
            "difficulty": "medium"
        }
    ]
    
    def generate_combat_task(self, player_level: int, player_traits: Dict[str, float]) -> Dict[str, Any]:
        """Generate a combat task based on player level and traits."""
        scenario = random.choice(self.COMBAT_SCENARIOS)
        
        # Adjust difficulty based on player level
        if player_level < 5:
            difficulty = "easy"
        elif player_level < 10:
            difficulty = "medium"
        else:
            difficulty = scenario["difficulty"]
        
        # Generate choices
        choices = self._generate_combat_choices(
            scenario, 
            player_level,
            player_traits.get("courage", 50),
            player_traits.get("intelligence", 50)
        )
        
        return {
            "task_id": f"combat_{random.randint(10000, 99999)}",
            "title": scenario["title"],
            "description": scenario["description"],
            "type": "combat",
            "difficulty": difficulty,
            "xp_reward": self._calculate_xp(difficulty),
            "credits_reward": self._calculate_credits(difficulty),
            "choices": choices
        }
    
    def _generate_combat_choices(
        self, 
        scenario: Dict[str, Any], 
        player_level: int,
        courage: float,
        intelligence: float
    ) -> List[Dict[str, Any]]:
        """Generate combat choices based on scenario."""
        choices = []
        
        # FIGHT option
        choices.append({
            "text": f"Fight the {scenario['enemy_type']}! (Requires courage)",
            "traits_impact": {
                "courage": 10,
                "aggression": 8,
                "resilience": 5,
                "karma_points": -3
            }
        })
        
        # FLEE option
        choices.append({
            "text": "Run away and escape to safety",
            "traits_impact": {
                "courage": -8,
                "wisdom": 5,
                "adaptability": 7,
                "karma_points": 0
            }
        })
        
        # NEGOTIATE option
        if intelligence >= 40:
            choices.append({
                "text": "Try to negotiate and find a peaceful solution",
                "traits_impact": {
                    "intelligence": 8,
                    "charisma": 10,
                    "compassion": 7,
                    "karma_points": 15
                }
            })
        
        # AMBUSH option for high courage
        if courage >= 60 and player_level >= 5:
            choices.append({
                "text": "Set up a counter-ambush using the environment",
                "traits_impact": {
                    "intelligence": 12,
                    "courage": 8,
                    "cunning": 10,
                    "karma_points": 5
                }
            })
        
        return choices
    
    def _calculate_xp(self, difficulty: str) -> int:
        """Calculate XP reward based on difficulty."""
        xp_map = {
            "easy": 75,
            "medium": 150,
            "hard": 300,
            "expert": 500
        }
        return xp_map.get(difficulty, 100)
    
    def _calculate_credits(self, difficulty: str) -> int:
        """Calculate credits reward based on difficulty."""
        credits_map = {
            "easy": 150,
            "medium": 300,
            "hard": 600,
            "expert": 1000
        }
        return credits_map.get(difficulty, 200)
