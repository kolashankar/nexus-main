"""Co-op task generator for multiplayer tasks."""

from typing import Dict, List, Optional
import random
from datetime import datetime, timedelta
from backend.models.tasks.task_types import TaskType, TaskDifficulty

class CoopTaskGenerator:
    """Generate co-op tasks that require multiple players."""
    
    def __init__(self):
        self.coop_scenarios = [
            {
                "title": "Ancient Vault Heist",
                "description": "A legendary vault filled with quantum credits has been discovered. It requires two people to access - one to hack the mainframe, the other to disable physical security.",
                "min_players": 2,
                "max_players": 2,
                "difficulty": TaskDifficulty.HARD,
                "duration_minutes": 30,
                "roles": [
                    {"name": "Hacker", "required_skill": "hacking", "min_level": 25},
                    {"name": "Security Expert", "required_skill": "stealth", "min_level": 20}
                ],
                "rewards": {
                    "xp": 500,
                    "credits": 2000,
                    "karma": 0,
                    "reputation": {"guild": 50}
                },
                "trait_impacts": {
                    "cooperation": 10,
                    "cunning": 5,
                    "courage": 5
                }
            },
            {
                "title": "Rescue the Stranded Citizen",
                "description": "A citizen is trapped in a collapsed building. One player must provide medical support while the other clears debris and ensures structural safety.",
                "min_players": 2,
                "max_players": 2,
                "difficulty": TaskDifficulty.MEDIUM,
                "duration_minutes": 20,
                "roles": [
                    {"name": "Medic", "required_skill": "compassion", "min_level": 15},
                    {"name": "Rescuer", "required_skill": "strength", "min_level": 15}
                ],
                "rewards": {
                    "xp": 300,
                    "credits": 1000,
                    "karma": 30,
                    "reputation": {"citizens": 40}
                },
                "trait_impacts": {
                    "compassion": 15,
                    "cooperation": 10,
                    "heroism": 8
                }
            },
            {
                "title": "Team Combat Training",
                "description": "The Combat Arena needs demonstration fighters. Team up with another player to showcase advanced combat tactics for new recruits.",
                "min_players": 2,
                "max_players": 4,
                "difficulty": TaskDifficulty.EASY,
                "duration_minutes": 15,
                "roles": [
                    {"name": "Attacker", "required_skill": "strength", "min_level": 10},
                    {"name": "Defender", "required_skill": "resilience", "min_level": 10}
                ],
                "rewards": {
                    "xp": 200,
                    "credits": 500,
                    "karma": 10,
                    "reputation": {"arena": 20}
                },
                "trait_impacts": {
                    "cooperation": 8,
                    "strength": 5,
                    "tactical_thinking": 5
                }
            },
            {
                "title": "Guild Resource Expedition",
                "description": "Your guild needs rare materials from the Wasteland. Form a team of 3-4 players to venture out, gather resources, and return safely.",
                "min_players": 3,
                "max_players": 4,
                "difficulty": TaskDifficulty.HARD,
                "duration_minutes": 45,
                "roles": [
                    {"name": "Scout", "required_skill": "perception", "min_level": 20},
                    {"name": "Gatherer", "required_skill": "crafting", "min_level": 15},
                    {"name": "Protector", "required_skill": "strength", "min_level": 20}
                ],
                "rewards": {
                    "xp": 600,
                    "credits": 1500,
                    "karma": 20,
                    "items": ["rare_crystal", "quantum_ore"],
                    "reputation": {"guild": 80}
                },
                "trait_impacts": {
                    "cooperation": 15,
                    "loyalty": 10,
                    "resourcefulness": 8
                }
            },
            {
                "title": "Defend the Settlement",
                "description": "A nearby settlement is under attack by rogue robots. Team up with 2-3 players to defend the citizens and secure the area.",
                "min_players": 2,
                "max_players": 3,
                "difficulty": TaskDifficulty.LEGENDARY,
                "duration_minutes": 60,
                "roles": [
                    {"name": "Front Line", "required_skill": "strength", "min_level": 30},
                    {"name": "Support", "required_skill": "compassion", "min_level": 25},
                    {"name": "Tactician", "required_skill": "tactical_thinking", "min_level": 30}
                ],
                "rewards": {
                    "xp": 1000,
                    "credits": 3000,
                    "karma": 50,
                    "items": ["hero_medal", "settlement_key"],
                    "reputation": {"settlement": 100, "citizens": 80}
                },
                "trait_impacts": {
                    "heroism": 20,
                    "cooperation": 15,
                    "courage": 15,
                    "strength": 10
                }
            }
        ]
    
    def generate_coop_task(
        self,
        player_level: int,
        player_traits: Dict,
        available_partners: List[Dict] = None
    ) -> Dict:
        """Generate a co-op task suitable for the player's level.
        
        Args:
            player_level: Player's current level
            player_traits: Player's trait values
            available_partners: List of potential partner players (optional)
        
        Returns:
            Dict with task data
        """
        # Filter scenarios by appropriate difficulty
        suitable_scenarios = self._filter_by_difficulty(player_level)
        
        # Select random scenario
        scenario = random.choice(suitable_scenarios)
        
        # Determine which role player can take
        available_roles = self._get_available_roles(scenario, player_traits)
        
        # Create task
        task_id = f"coop_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return {
            "_id": task_id,
            "task_id": task_id,
            "type": TaskType.COOP.value,
            "title": scenario["title"],
            "description": scenario["description"],
            "difficulty": scenario["difficulty"].value,
            "min_players": scenario["min_players"],
            "max_players": scenario["max_players"],
            "duration_minutes": scenario["duration_minutes"],
            "roles": scenario["roles"],
            "available_roles_for_player": available_roles,
            "rewards": scenario["rewards"],
            "trait_impacts": scenario["trait_impacts"],
            "status": "looking_for_partners",
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24),
            "partners_joined": [],
            "required_partners": scenario["min_players"] - 1
        }
    
    def _filter_by_difficulty(self, player_level: int) -> List[Dict]:
        """Filter scenarios by appropriate difficulty for player level."""
        if player_level < 10:
            allowed = [TaskDifficulty.EASY]
        elif player_level < 20:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM]
        elif player_level < 30:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM, TaskDifficulty.HARD]
        else:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM, TaskDifficulty.HARD, TaskDifficulty.LEGENDARY]
        
        return [s for s in self.coop_scenarios if s["difficulty"] in allowed]
    
    def _get_available_roles(self, scenario: Dict, player_traits: Dict) -> List[str]:
        """Determine which roles the player qualifies for."""
        available = []
        
        for role in scenario["roles"]:
            skill = role["required_skill"]
            min_level = role["min_level"]
            
            # Check if player has sufficient skill level
            player_skill_value = player_traits.get(skill, 0)
            
            if player_skill_value >= min_level:
                available.append(role["name"])
        
        return available if available else ["Any"]  # Allow any role if player doesn't meet requirements
    
    def join_coop_task(
        self,
        task: Dict,
        player_id: str,
        player_name: str,
        selected_role: str
    ) -> Dict:
        """Player joins an existing co-op task.
        
        Args:
            task: The co-op task data
            player_id: ID of joining player
            player_name: Name of joining player
            selected_role: Role player wants to take
        
        Returns:
            Updated task with player added
        """
        # Check if task is still accepting players
        if len(task["partners_joined"]) >= task["max_players"] - 1:
            raise ValueError("Task is full")
        
        # Check if player already joined
        if any(p["player_id"] == player_id for p in task["partners_joined"]):
            raise ValueError("Already joined this task")
        
        # Add player to partners
        task["partners_joined"].append({
            "player_id": player_id,
            "player_name": player_name,
            "role": selected_role,
            "joined_at": datetime.now()
        })
        
        # Update status if enough players
        if len(task["partners_joined"]) >= task["min_players"] - 1:
            task["status"] = "ready_to_start"
        
        return task
    
    def start_coop_task(self, task: Dict) -> Dict:
        """Start a co-op task once all players are ready.
        
        Args:
            task: The co-op task data
        
        Returns:
            Updated task with started status
        """
        if task["status"] != "ready_to_start":
            raise ValueError("Task not ready to start - need more players")
        
        task["status"] = "in_progress"
        task["started_at"] = datetime.now()
        task["must_complete_by"] = datetime.now() + timedelta(minutes=task["duration_minutes"])
        
        return task
    
    def complete_coop_task(
        self,
        task: Dict,
        success: bool,
        completion_data: Optional[Dict] = None
    ) -> Dict:
        """Complete a co-op task and calculate rewards.
        
        Args:
            task: The co-op task data
            success: Whether task was completed successfully
            completion_data: Optional data about how task was completed
        
        Returns:
            Completion result with rewards for each player
        """
        result = {
            "task_id": task["task_id"],
            "success": success,
            "completed_at": datetime.now(),
            "participants": []
        }
        
        if success:
            # Full rewards for all participants
            reward_multiplier = 1.0
            
            # Bonus for completing under time
            if completion_data and "time_taken_minutes" in completion_data:
                time_taken = completion_data["time_taken_minutes"]
                if time_taken < task["duration_minutes"] * 0.7:
                    reward_multiplier = 1.2  # 20% bonus for fast completion
            
            # Calculate rewards for each participant
            for partner in task["partners_joined"]:
                participant_result = {
                    "player_id": partner["player_id"],
                    "player_name": partner["player_name"],
                    "role": partner["role"],
                    "rewards": {
                        "xp": int(task["rewards"]["xp"] * reward_multiplier),
                        "credits": int(task["rewards"]["credits"] * reward_multiplier),
                        "karma": task["rewards"]["karma"],
                    },
                    "trait_impacts": task["trait_impacts"],
                    "items_received": task["rewards"].get("items", []),
                    "reputation_changes": task["rewards"].get("reputation", {})
                }
                result["participants"].append(participant_result)
        else:
            # Partial rewards for failed attempt
            for partner in task["partners_joined"]:
                participant_result = {
                    "player_id": partner["player_id"],
                    "player_name": partner["player_name"],
                    "role": partner["role"],
                    "rewards": {
                        "xp": int(task["rewards"]["xp"] * 0.2),  # 20% XP for trying
                        "credits": 0,
                        "karma": 0
                    },
                    "trait_impacts": {k: v // 2 for k, v in task["trait_impacts"].items()},
                    "items_received": [],
                    "reputation_changes": {}
                }
                result["participants"].append(participant_result)
        
        return result
