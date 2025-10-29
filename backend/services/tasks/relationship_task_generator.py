"""Relationship task generator service."""

import random
from typing import Dict, Any, List

class RelationshipTaskGenerator:
    """Generates relationship-focused tasks."""
    
    RELATIONSHIP_SCENARIOS = [
        {
            "title": "Betrayed Ally",
            "description": "Your former ally has joined a rival guild and is now working against you. They reach out asking to meet.",
            "npc_type": "former_ally",
            "trust_level": "low"
        },
        {
            "title": "New Guild Member",
            "description": "A skilled fighter wants to join your guild, but they have a dark reputation from their past.",
            "npc_type": "recruit",
            "trust_level": "unknown"
        },
        {
            "title": "Wounded Stranger",
            "description": "You find a wounded traveler outside the city. They claim they were robbed, but something seems off about their story.",
            "npc_type": "stranger",
            "trust_level": "unknown"
        },
        {
            "title": "Childhood Friend Returns",
            "description": "A friend from before the wasteland reaches out. They need help, but associating with them could damage your reputation.",
            "npc_type": "old_friend",
            "trust_level": "high"
        },
        {
            "title": "Rival's Offer",
            "description": "Your biggest rival offers a temporary alliance against a common enemy. Can you trust them?",
            "npc_type": "rival",
            "trust_level": "very_low"
        }
    ]
    
    def generate_relationship_task(self, player_level: int, player_traits: Dict[str, float]) -> Dict[str, Any]:
        """Generate a relationship task."""
        scenario = random.choice(self.RELATIONSHIP_SCENARIOS)
        
        choices = self._generate_relationship_choices(
            scenario,
            player_traits.get("trust", 50),
            player_traits.get("compassion", 50),
            player_traits.get("cunning", 50)
        )
        
        return {
            "task_id": f"relationship_{random.randint(10000, 99999)}",
            "title": scenario["title"],
            "description": scenario["description"],
            "type": "relationship",
            "difficulty": "medium",
            "xp_reward": 100,
            "credits_reward": 150,
            "choices": choices
        }
    
    def _generate_relationship_choices(
        self,
        scenario: Dict[str, Any],
        trust: float,
        compassion: float,
        cunning: float
    ) -> List[Dict[str, Any]]:
        """Generate relationship choices."""
        choices = []
        
        # BEFRIEND option
        choices.append({
            "text": "Give them a chance and try to build trust",
            "traits_impact": {
                "trust": 10,
                "compassion": 8,
                "loyalty": 7,
                "karma_points": 15
            }
        })
        
        # BETRAY option
        if cunning >= 50:
            choices.append({
                "text": "Use this situation to your advantage",
                "traits_impact": {
                    "cunning": 12,
                    "ruthlessness": 10,
                    "trust": -15,
                    "karma_points": -20
                }
            })
        
        # IGNORE option
        choices.append({
            "text": "Avoid getting involved and walk away",
            "traits_impact": {
                "independence": 8,
                "compassion": -5,
                "trust": -3,
                "karma_points": -5
            }
        })
        
        # HELP option
        if compassion >= 60:
            choices.append({
                "text": "Help them unconditionally, regardless of consequences",
                "traits_impact": {
                    "compassion": 15,
                    "generosity": 12,
                    "loyalty": 10,
                    "karma_points": 25
                }
            })
        
        # FORGIVE option (for betrayal scenarios)
        if "betray" in scenario["title"].lower():
            choices.append({
                "text": "Forgive their betrayal and offer reconciliation",
                "traits_impact": {
                    "compassion": 15,
                    "wisdom": 10,
                    "trust": 8,
                    "karma_points": 30
                }
            })
        
        return choices
