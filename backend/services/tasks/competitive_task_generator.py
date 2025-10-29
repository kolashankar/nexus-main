"""Competitive task generator for PvP tasks."""

from typing import Dict, List, Optional
import random
from datetime import datetime, timedelta
from backend.models.tasks.task_types import TaskType, TaskDifficulty

class CompetitiveTaskGenerator:
    """Generate competitive tasks where players race against each other."""
    
    def __init__(self):
        self.competitive_scenarios = [
            {
                "title": "Hacking Race",
                "description": "Two hackers compete to breach the same corporation's security first. Fastest hacker wins the contract and reputation.",
                "category": "speed_challenge",
                "difficulty": TaskDifficulty.MEDIUM,
                "duration_minutes": 10,
                "winner_rewards": {
                    "xp": 400,
                    "credits": 2000,
                    "karma": -5,
                    "reputation": {"hackers_guild": 50}
                },
                "loser_rewards": {
                    "xp": 100,
                    "credits": 200,
                    "karma": -2,
                    "reputation": {"hackers_guild": 10}
                },
                "required_skill": "hacking",
                "min_skill_level": 20,
                "trait_impacts_winner": {
                    "cunning": 10,
                    "confidence": 8,
                    "competitive_spirit": 10
                },
                "trait_impacts_loser": {
                    "humility": 5,
                    "determination": 5
                }
            },
            {
                "title": "Arena Duel",
                "description": "Face off against another player in the combat arena. Winner takes glory and substantial rewards.",
                "category": "combat",
                "difficulty": TaskDifficulty.HARD,
                "duration_minutes": 15,
                "winner_rewards": {
                    "xp": 600,
                    "credits": 3000,
                    "karma": 0,
                    "items": ["champion_trophy"],
                    "reputation": {"arena": 100}
                },
                "loser_rewards": {
                    "xp": 200,
                    "credits": 500,
                    "karma": 0,
                    "reputation": {"arena": 20}
                },
                "required_skill": "strength",
                "min_skill_level": 25,
                "trait_impacts_winner": {
                    "strength": 10,
                    "confidence": 15,
                    "dominance": 12
                },
                "trait_impacts_loser": {
                    "humility": 8,
                    "resilience": 10,
                    "determination": 8
                }
            },
            {
                "title": "Trading Competition",
                "description": "Two traders compete to make the most profit in the market within a time limit.",
                "category": "economic",
                "difficulty": TaskDifficulty.MEDIUM,
                "duration_minutes": 20,
                "winner_rewards": {
                    "xp": 350,
                    "credits": 2500,
                    "karma": 0,
                    "reputation": {"traders_guild": 60}
                },
                "loser_rewards": {
                    "xp": 150,
                    "credits": 500,
                    "karma": 0,
                    "reputation": {"traders_guild": 15}
                },
                "required_skill": "trading",
                "min_skill_level": 15,
                "trait_impacts_winner": {
                    "cunning": 8,
                    "greed": 5,
                    "intelligence": 10
                },
                "trait_impacts_loser": {
                    "humility": 5,
                    "patience": 5
                }
            },
            {
                "title": "Resource Gathering Sprint",
                "description": "Race against another player to collect the most rare resources from the Wasteland.",
                "category": "speed_challenge",
                "difficulty": TaskDifficulty.EASY,
                "duration_minutes": 15,
                "winner_rewards": {
                    "xp": 250,
                    "credits": 1000,
                    "karma": 5,
                    "items": ["rare_crystal"],
                    "reputation": {"scavengers": 40}
                },
                "loser_rewards": {
                    "xp": 100,
                    "credits": 300,
                    "karma": 2,
                    "reputation": {"scavengers": 10}
                },
                "required_skill": "perception",
                "min_skill_level": 10,
                "trait_impacts_winner": {
                    "speed": 8,
                    "resourcefulness": 10,
                    "competitive_spirit": 8
                },
                "trait_impacts_loser": {
                    "patience": 5,
                    "determination": 5
                }
            },
            {
                "title": "Influence Campaign",
                "description": "Compete to gain the most followers and influence in the city's social network.",
                "category": "social",
                "difficulty": TaskDifficulty.HARD,
                "duration_minutes": 30,
                "winner_rewards": {
                    "xp": 500,
                    "credits": 2000,
                    "karma": 10,
                    "items": ["influencer_badge"],
                    "reputation": {"citizens": 80, "social_elite": 60}
                },
                "loser_rewards": {
                    "xp": 150,
                    "credits": 400,
                    "karma": 5,
                    "reputation": {"citizens": 20}
                },
                "required_skill": "charisma",
                "min_skill_level": 20,
                "trait_impacts_winner": {
                    "charisma": 15,
                    "confidence": 10,
                    "manipulation": 5
                },
                "trait_impacts_loser": {
                    "humility": 8,
                    "authenticity": 5
                }
            }
        ]
    
    def generate_competitive_task(
        self,
        player_level: int,
        player_traits: Dict,
        opponent_data: Optional[Dict] = None
    ) -> Dict:
        """Generate a competitive task.
        
        Args:
            player_level: Player's current level
            player_traits: Player's trait values
            opponent_data: Data about potential opponent (optional)
        
        Returns:
            Dict with task data
        """
        # Filter by difficulty
        suitable_scenarios = self._filter_by_difficulty(player_level)
        
        # Select scenario
        scenario = random.choice(suitable_scenarios)
        
        # Check if player qualifies
        qualifies = self._check_qualification(scenario, player_traits)
        
        # Generate task ID
        task_id = f"competitive_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return {
            "_id": task_id,
            "task_id": task_id,
            "type": TaskType.COMPETITIVE.value,
            "category": scenario["category"],
            "title": scenario["title"],
            "description": scenario["description"],
            "difficulty": scenario["difficulty"].value,
            "duration_minutes": scenario["duration_minutes"],
            "required_skill": scenario["required_skill"],
            "min_skill_level": scenario["min_skill_level"],
            "player_qualifies": qualifies,
            "winner_rewards": scenario["winner_rewards"],
            "loser_rewards": scenario["loser_rewards"],
            "trait_impacts_winner": scenario["trait_impacts_winner"],
            "trait_impacts_loser": scenario["trait_impacts_loser"],
            "status": "looking_for_opponent",
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=12),
            "opponent": opponent_data,
            "match_result": None
        }
    
    def _filter_by_difficulty(self, player_level: int) -> List[Dict]:
        """Filter scenarios by appropriate difficulty."""
        if player_level < 10:
            allowed = [TaskDifficulty.EASY]
        elif player_level < 25:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM]
        else:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM, TaskDifficulty.HARD]
        
        return [s for s in self.competitive_scenarios if s["difficulty"] in allowed]
    
    def _check_qualification(self, scenario: Dict, player_traits: Dict) -> bool:
        """Check if player meets minimum requirements."""
        skill = scenario["required_skill"]
        min_level = scenario["min_skill_level"]
        player_skill_value = player_traits.get(skill, 0)
        
        return player_skill_value >= min_level
    
    def match_opponent(
        self,
        task: Dict,
        opponent_id: str,
        opponent_name: str,
        opponent_level: int,
        opponent_traits: Dict
    ) -> Dict:
        """Match player with an opponent.
        
        Args:
            task: The competitive task
            opponent_id: ID of opponent
            opponent_name: Name of opponent
            opponent_level: Opponent's level
            opponent_traits: Opponent's traits
        
        Returns:
            Updated task with opponent matched
        """
        # Check if opponent qualifies
        qualifies = self._check_qualification(task, opponent_traits)
        
        if not qualifies:
            raise ValueError(f"Opponent does not meet skill requirement: {task['required_skill']} >= {task['min_skill_level']}")
        
        task["opponent"] = {
            "player_id": opponent_id,
            "player_name": opponent_name,
            "player_level": opponent_level,
            "skill_level": opponent_traits.get(task["required_skill"], 0)
        }
        task["status"] = "matched"
        task["matched_at"] = datetime.now()
        
        return task
    
    def start_competitive_task(self, task: Dict) -> Dict:
        """Start the competitive task.
        
        Args:
            task: The competitive task
        
        Returns:
            Updated task with started status
        """
        if task["status"] != "matched":
            raise ValueError("Task not ready - need opponent")
        
        task["status"] = "in_progress"
        task["started_at"] = datetime.now()
        task["must_complete_by"] = datetime.now() + timedelta(minutes=task["duration_minutes"])
        
        return task
    
    def complete_competitive_task(
        self,
        task: Dict,
        player_id: str,
        player_score: float,
        opponent_score: float
    ) -> Dict:
        """Complete competitive task and determine winner.
        
        Args:
            task: The competitive task
            player_id: ID of the player
            player_score: Player's performance score
            opponent_score: Opponent's performance score
        
        Returns:
            Completion result with rewards
        """
        winner = player_id if player_score > opponent_score else task["opponent"]["player_id"]
        player_won = (winner == player_id)
        
        result = {
            "task_id": task["task_id"],
            "completed_at": datetime.now(),
            "winner": winner,
            "player_score": player_score,
            "opponent_score": opponent_score,
            "margin": abs(player_score - opponent_score),
            "player_result": {
                "won": player_won,
                "rewards": task["winner_rewards"] if player_won else task["loser_rewards"],
                "trait_impacts": task["trait_impacts_winner"] if player_won else task["trait_impacts_loser"]
            },
            "opponent_result": {
                "player_id": task["opponent"]["player_id"],
                "won": not player_won,
                "rewards": task["loser_rewards"] if player_won else task["winner_rewards"],
                "trait_impacts": task["trait_impacts_loser"] if player_won else task["trait_impacts_winner"]
            }
        }
        
        return result
