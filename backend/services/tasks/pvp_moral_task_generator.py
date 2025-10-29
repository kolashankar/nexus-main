"""PvP moral choice task generator - choices affect other players."""

from typing import Dict, List, Optional
import random
from datetime import datetime, timedelta
from backend.models.tasks.task_types import TaskType, TaskDifficulty

class PvPMoralTaskGenerator:
    """Generate PvP moral choice tasks where your choice affects another player."""
    
    def __init__(self):
        self.moral_scenarios = [
            {
                "title": "Intercepted Data Package",
                "description": "You've intercepted a data package meant for {target_player}. It contains valuable trade secrets. Do you deliver it, sell it, or keep it for yourself?",
                "difficulty": TaskDifficulty.MEDIUM,
                "choices": [
                    {
                        "id": 0,
                        "text": "Deliver it to {target_player} honestly",
                        "player_effects": {
                            "xp": 200,
                            "credits": 500,
                            "karma": 20,
                            "traits": {"honesty": 10, "loyalty": 8}
                        },
                        "target_effects": {
                            "credits": 2000,
                            "karma": 10,
                            "reputation": {"traders": 30},
                            "relationship_change": 25,
                            "message": "{player_name} honestly delivered your intercepted data package."
                        }
                    },
                    {
                        "id": 1,
                        "text": "Sell it to a competitor",
                        "player_effects": {
                            "xp": 150,
                            "credits": 3000,
                            "karma": -15,
                            "traits": {"greed": 10, "cunning": 8, "honesty": -5}
                        },
                        "target_effects": {
                            "credits": -1500,
                            "karma": -5,
                            "reputation": {"traders": -20},
                            "relationship_change": -30,
                            "message": "{player_name} sold your intercepted data to a competitor. You suffered losses."
                        }
                    },
                    {
                        "id": 2,
                        "text": "Keep it for yourself and use the information",
                        "player_effects": {
                            "xp": 180,
                            "credits": 1500,
                            "karma": -10,
                            "items": ["trade_secrets"],
                            "traits": {"cunning": 10, "selfishness": 5}
                        },
                        "target_effects": {
                            "credits": -800,
                            "reputation": {"traders": -15},
                            "relationship_change": -20,
                            "message": "{player_name} kept your intercepted data and used it against you."
                        }
                    }
                ]
            },
            {
                "title": "Guild Member in Trouble",
                "description": "{target_player} from a rival guild is trapped and needs help. Saving them would cost you resources, but leaving them might weaken their guild.",
                "difficulty": TaskDifficulty.HARD,
                "choices": [
                    {
                        "id": 0,
                        "text": "Save them despite the cost",
                        "player_effects": {
                            "xp": 400,
                            "credits": -1000,
                            "karma": 30,
                            "traits": {"compassion": 15, "heroism": 10, "honor": 10}
                        },
                        "target_effects": {
                            "health": "restored",
                            "karma": 15,
                            "relationship_change": 40,
                            "guild_reputation": 20,
                            "message": "{player_name} saved you despite you being in a rival guild. True heroism!"
                        }
                    },
                    {
                        "id": 1,
                        "text": "Leave them - it's not your problem",
                        "player_effects": {
                            "xp": 50,
                            "credits": 0,
                            "karma": -15,
                            "traits": {"callousness": 8, "pragmatism": 5}
                        },
                        "target_effects": {
                            "health": -30,
                            "karma": -10,
                            "relationship_change": -35,
                            "guild_reputation": -15,
                            "message": "{player_name} left you to suffer because of guild rivalry."
                        }
                    },
                    {
                        "id": 2,
                        "text": "Demand payment for the rescue",
                        "player_effects": {
                            "xp": 250,
                            "credits": 2000,
                            "karma": -5,
                            "traits": {"pragmatism": 10, "greed": 5, "compassion": -5}
                        },
                        "target_effects": {
                            "health": "restored",
                            "credits": -2000,
                            "karma": 0,
                            "relationship_change": -10,
                            "message": "{player_name} saved you, but demanded a hefty payment."
                        }
                    }
                ]
            },
            {
                "title": "Resource Claim Dispute",
                "description": "You and {target_player} discovered a rare resource deposit at the same time. You can share it, fight for it, or negotiate.",
                "difficulty": TaskDifficulty.MEDIUM,
                "choices": [
                    {
                        "id": 0,
                        "text": "Share the resources fairly",
                        "player_effects": {
                            "xp": 300,
                            "credits": 1500,
                            "karma": 20,
                            "items": ["rare_ore_share"],
                            "traits": {"cooperation": 12, "fairness": 10}
                        },
                        "target_effects": {
                            "credits": 1500,
                            "karma": 20,
                            "items": ["rare_ore_share"],
                            "relationship_change": 30,
                            "message": "{player_name} agreed to share the rare resource deposit fairly with you."
                        }
                    },
                    {
                        "id": 1,
                        "text": "Challenge them to combat for it",
                        "player_effects": {
                            "xp": 400,
                            "credits": 0,  # Depends on combat outcome
                            "karma": -10,
                            "traits": {"aggression": 10, "competitive_spirit": 8}
                        },
                        "target_effects": {
                            "forced_into_combat": True,
                            "karma": -5,
                            "relationship_change": -25,
                            "message": "{player_name} challenged you to combat for the resource deposit!"
                        }
                    },
                    {
                        "id": 2,
                        "text": "Offer to buy them out",
                        "player_effects": {
                            "xp": 250,
                            "credits": -1000,
                            "karma": 5,
                            "items": ["rare_ore_full"],
                            "traits": {"negotiation": 10, "wealth_management": 5}
                        },
                        "target_effects": {
                            "credits": 1000,
                            "karma": 5,
                            "relationship_change": 10,
                            "message": "{player_name} offered to buy your claim on the resource deposit."
                        }
                    }
                ]
            },
            {
                "title": "Reputation at Stake",
                "description": "You've discovered {target_player} engaged in questionable activities. You can expose them, blackmail them, or stay silent.",
                "difficulty": TaskDifficulty.HARD,
                "choices": [
                    {
                        "id": 0,
                        "text": "Stay silent and mind your business",
                        "player_effects": {
                            "xp": 100,
                            "credits": 0,
                            "karma": 5,
                            "traits": {"discretion": 10, "privacy_respect": 8}
                        },
                        "target_effects": {
                            "karma": 0,
                            "relationship_change": 15,
                            "message": "{player_name} discovered your secret but chose to stay silent."
                        }
                    },
                    {
                        "id": 1,
                        "text": "Expose them publicly",
                        "player_effects": {
                            "xp": 300,
                            "credits": 500,
                            "karma": 10,
                            "reputation": {"citizens": 30},
                            "traits": {"justice": 12, "courage": 8}
                        },
                        "target_effects": {
                            "credits": -2000,
                            "karma": -25,
                            "reputation": {"all": -40},
                            "relationship_change": -50,
                            "message": "{player_name} exposed your questionable activities publicly. Your reputation has taken a major hit!"
                        }
                    },
                    {
                        "id": 2,
                        "text": "Blackmail them for credits",
                        "player_effects": {
                            "xp": 200,
                            "credits": 3000,
                            "karma": -20,
                            "traits": {"manipulation": 12, "greed": 10, "honor": -10}
                        },
                        "target_effects": {
                            "credits": -3000,
                            "karma": -10,
                            "relationship_change": -40,
                            "blackmailed_by": "player_id",
                            "message": "{player_name} is blackmailing you with information about your activities."
                        }
                    }
                ]
            },
            {
                "title": "Job Opportunity",
                "description": "You've been offered a high-paying job that {target_player} was counting on. Do you take it, decline it for them, or negotiate a partnership?",
                "difficulty": TaskDifficulty.EASY,
                "choices": [
                    {
                        "id": 0,
                        "text": "Take the job - business is business",
                        "player_effects": {
                            "xp": 250,
                            "credits": 2000,
                            "karma": -5,
                            "traits": {"ambition": 8, "competitive_spirit": 5}
                        },
                        "target_effects": {
                            "credits": 0,
                            "karma": -5,
                            "relationship_change": -15,
                            "message": "{player_name} took the job you were counting on."
                        }
                    },
                    {
                        "id": 1,
                        "text": "Decline and let them have it",
                        "player_effects": {
                            "xp": 150,
                            "credits": 0,
                            "karma": 15,
                            "traits": {"generosity": 10, "empathy": 8}
                        },
                        "target_effects": {
                            "credits": 2000,
                            "karma": 10,
                            "relationship_change": 30,
                            "message": "{player_name} declined a job opportunity so you could have it!"
                        }
                    },
                    {
                        "id": 2,
                        "text": "Propose working together on it",
                        "player_effects": {
                            "xp": 300,
                            "credits": 1200,
                            "karma": 10,
                            "traits": {"cooperation": 12, "leadership": 8}
                        },
                        "target_effects": {
                            "credits": 1200,
                            "karma": 10,
                            "relationship_change": 25,
                            "message": "{player_name} proposed working together on the job opportunity. Partnership formed!"
                        }
                    }
                ]
            }
        ]
    
    def generate_pvp_moral_task(
        self,
        player_level: int,
        player_traits: Dict,
        target_player: Dict
    ) -> Dict:
        """Generate a PvP moral choice task.
        
        Args:
            player_level: Player's current level
            player_traits: Player's trait values
            target_player: The other player affected by choice
        
        Returns:
            Dict with task data
        """
        # Filter by difficulty
        suitable_scenarios = self._filter_by_difficulty(player_level)
        
        # Select scenario
        scenario = random.choice(suitable_scenarios)
        
        # Personalize description
        description = scenario["description"].replace("{target_player}", target_player["name"])
        
        # Personalize choices
        personalized_choices = []
        for choice in scenario["choices"]:
            personalized_choice = choice.copy()
            personalized_choice["text"] = choice["text"].replace("{target_player}", target_player["name"])
            personalized_choices.append(personalized_choice)
        
        # Generate task ID
        task_id = f"pvp_moral_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return {
            "_id": task_id,
            "task_id": task_id,
            "type": TaskType.PVP_MORAL.value,
            "title": scenario["title"],
            "description": description,
            "difficulty": scenario["difficulty"].value,
            "target_player": {
                "player_id": target_player["_id"],
                "player_name": target_player["name"],
                "player_level": target_player.get("level", 1)
            },
            "choices": personalized_choices,
            "status": "pending_choice",
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }
    
    def _filter_by_difficulty(self, player_level: int) -> List[Dict]:
        """Filter scenarios by appropriate difficulty."""
        if player_level < 10:
            allowed = [TaskDifficulty.EASY]
        elif player_level < 20:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM]
        else:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM, TaskDifficulty.HARD]
        
        return [s for s in self.moral_scenarios if s["difficulty"] in allowed]
    
    def complete_pvp_moral_task(
        self,
        task: Dict,
        choice_index: int,
        player_id: str,
        player_name: str
    ) -> Dict:
        """Complete a PvP moral task and apply effects to both players.
        
        Args:
            task: The PvP moral task
            choice_index: Index of chosen option
            player_id: ID of player making choice
            player_name: Name of player making choice
        
        Returns:
            Completion result with effects for both players
        """
        if choice_index < 0 or choice_index >= len(task["choices"]):
            raise ValueError(f"Invalid choice index: {choice_index}")
        
        choice = task["choices"][choice_index]
        
        # Personalize target effects message
        target_effects = choice["target_effects"].copy()
        if "message" in target_effects:
            target_effects["message"] = target_effects["message"].replace("{player_name}", player_name)
        
        result = {
            "task_id": task["task_id"],
            "completed_at": datetime.now(),
            "choice_index": choice_index,
            "choice_text": choice["text"],
            "player_effects": {
                "player_id": player_id,
                "effects": choice["player_effects"]
            },
            "target_player_effects": {
                "player_id": task["target_player"]["player_id"],
                "player_name": task["target_player"]["player_name"],
                "effects": target_effects,
                "notification_sent": True
            }
        }
        
        return result
