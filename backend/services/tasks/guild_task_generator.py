"""Guild task generator service."""

import random
from typing import Dict, Any, List

class GuildTaskGenerator:
    """Generates guild-related tasks."""
    
    GUILD_SCENARIOS = [
        {
            "title": "Guild Recruitment Drive",
            "description": "Your guild needs more members to compete in the upcoming territory wars. How will you approach recruitment?",
            "guild_status": "growing"
        },
        {
            "title": "Leadership Challenge",
            "description": "A powerful member is challenging the current guild leader. They're asking for your support.",
            "guild_status": "conflict"
        },
        {
            "title": "Alliance Proposal",
            "description": "A neighboring guild proposes an alliance. It could provide protection, but you'd lose some independence.",
            "guild_status": "diplomatic"
        },
        {
            "title": "Guild Traitor",
            "description": "Evidence suggests someone in your guild is leaking information to rivals. You need to act.",
            "guild_status": "crisis"
        },
        {
            "title": "Territory Expansion",
            "description": "Your guild has the opportunity to claim new territory, but it will put you in conflict with another guild.",
            "guild_status": "aggressive"
        },
        {
            "title": "Guild Treasury Crisis",
            "description": "The guild treasury is nearly empty. Someone needs to find a solution before members start leaving.",
            "guild_status": "economic"
        }
    ]
    
    def generate_guild_task(self, player_level: int, player_traits: Dict[str, float], is_guild_member: bool = True) -> Dict[str, Any]:
        """Generate a guild task."""
        scenario = random.choice(self.GUILD_SCENARIOS)
        
        choices = self._generate_guild_choices(
            scenario,
            player_traits.get("leadership", 50),
            player_traits.get("loyalty", 50),
            player_traits.get("ambition", 50),
            is_guild_member
        )
        
        return {
            "task_id": f"guild_{random.randint(10000, 99999)}",
            "title": scenario["title"],
            "description": scenario["description"],
            "type": "guild",
            "difficulty": "medium",
            "xp_reward": 150,
            "credits_reward": 200,
            "choices": choices
        }
    
    def _generate_guild_choices(
        self,
        scenario: Dict[str, Any],
        leadership: float,
        loyalty: float,
        ambition: float,
        is_guild_member: bool
    ) -> List[Dict[str, Any]]:
        """Generate guild-related choices."""
        choices = []
        
        if is_guild_member:
            # LEAD option
            if leadership >= 60:
                choices.append({
                    "text": "Take charge and lead the guild through this challenge",
                    "traits_impact": {
                        "leadership": 15,
                        "courage": 10,
                        "loyalty": 8,
                        "karma_points": 15
                    }
                })
            
            # SUPPORT option
            choices.append({
                "text": "Support the current leadership and follow their direction",
                "traits_impact": {
                    "loyalty": 12,
                    "teamwork": 10,
                    "humility": 8,
                    "karma_points": 10
                }
            })
            
            # OPPOSE option
            if ambition >= 70:
                choices.append({
                    "text": "Oppose the current approach and push for change",
                    "traits_impact": {
                        "ambition": 12,
                        "courage": 8,
                        "loyalty": -10,
                        "karma_points": -5
                    }
                })
            
            # LEAVE option
            choices.append({
                "text": "This guild is no longer serving your interests. Leave.",
                "traits_impact": {
                    "independence": 15,
                    "loyalty": -20,
                    "ambition": 8,
                    "karma_points": -15
                }
            })
        else:
            # JOIN option
            choices.append({
                "text": "Join the guild and help them with their challenges",
                "traits_impact": {
                    "teamwork": 12,
                    "loyalty": 10,
                    "social": 8,
                    "karma_points": 10
                }
            })
            
            # RECRUIT option
            choices.append({
                "text": "Recruit others to join and strengthen the guild",
                "traits_impact": {
                    "leadership": 10,
                    "charisma": 12,
                    "social": 8,
                    "karma_points": 12
                }
            })
            
            # OPPOSE option
            choices.append({
                "text": "Form a rival guild to compete with them",
                "traits_impact": {
                    "ambition": 15,
                    "independence": 12,
                    "rivalry": 10,
                    "karma_points": -10
                }
            })
        
        return choices
