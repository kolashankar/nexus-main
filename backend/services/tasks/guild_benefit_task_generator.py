"""Guild benefit task generator - tasks that benefit entire guild."""

from typing import Dict, List, Optional
import random
from datetime import datetime, timedelta
from backend.models.tasks.task_types import TaskType, TaskDifficulty

class GuildBenefitTaskGenerator:
    """Generate tasks that provide benefits to entire guild when completed."""
    
    def __init__(self):
        self.guild_tasks = [
            {
                "title": "Guild Vault Security Upgrade",
                "description": "Complete a series of security challenges to upgrade your guild's vault protection.",
                "difficulty": TaskDifficulty.HARD,
                "duration_minutes": 45,
                "required_contributions": 3,  # Number of members who must contribute
                "contribution_types": ["complete_challenge", "donate_credits", "provide_materials"],
                "rewards_per_contributor": {
                    "xp": 400,
                    "credits": 1000,
                    "karma": 15,
                    "guild_reputation": 50
                },
                "guild_benefits": {
                    "vault_capacity": "+20%",
                    "vault_protection": "+15%",
                    "description": "Guild vault can hold 20% more items and has 15% better protection"
                },
                "trait_impacts": {
                    "loyalty": 12,
                    "cooperation": 10,
                    "dedication": 8
                }
            },
            {
                "title": "Territory Expansion Campaign",
                "description": "Help your guild secure a new territory through strategic missions.",
                "difficulty": TaskDifficulty.LEGENDARY,
                "duration_minutes": 90,
                "required_contributions": 5,
                "contribution_types": ["combat_mission", "diplomatic_mission", "resource_gathering"],
                "rewards_per_contributor": {
                    "xp": 800,
                    "credits": 2500,
                    "karma": 25,
                    "guild_reputation": 100,
                    "items": ["territory_founder_badge"]
                },
                "guild_benefits": {
                    "territory_count": "+1",
                    "resource_income": "+10%",
                    "description": "Guild gains a new territory, increasing resource income by 10%"
                },
                "trait_impacts": {
                    "loyalty": 20,
                    "leadership": 15,
                    "strategic_thinking": 12,
                    "cooperation": 15
                }
            },
            {
                "title": "Guild Training Facility",
                "description": "Pool resources to build a training facility that benefits all guild members.",
                "difficulty": TaskDifficulty.MEDIUM,
                "duration_minutes": 60,
                "required_contributions": 4,
                "contribution_types": ["donate_credits", "provide_materials", "construction_work"],
                "rewards_per_contributor": {
                    "xp": 300,
                    "credits": 500,
                    "karma": 20,
                    "guild_reputation": 40
                },
                "guild_benefits": {
                    "training_speed": "+15%",
                    "skill_gains": "+10%",
                    "description": "All guild members gain 15% faster training and 10% bonus skill improvements"
                },
                "trait_impacts": {
                    "generosity": 10,
                    "cooperation": 12,
                    "foresight": 8
                }
            },
            {
                "title": "Guild Alliance Formation",
                "description": "Help negotiate an alliance with another guild for mutual benefits.",
                "difficulty": TaskDifficulty.HARD,
                "duration_minutes": 50,
                "required_contributions": 3,
                "contribution_types": ["diplomatic_mission", "gift_contribution", "reputation_building"],
                "rewards_per_contributor": {
                    "xp": 450,
                    "credits": 1500,
                    "karma": 30,
                    "guild_reputation": 60
                },
                "guild_benefits": {
                    "alliance_count": "+1",
                    "trade_bonus": "+12%",
                    "war_support": "Ally support in wars",
                    "description": "Guild forms alliance, gaining 12% trade bonus and ally support"
                },
                "trait_impacts": {
                    "diplomacy": 15,
                    "charisma": 10,
                    "cooperation": 12
                }
            },
            {
                "title": "Guild Research Project",
                "description": "Contribute to guild research that unlocks new technologies for everyone.",
                "difficulty": TaskDifficulty.MEDIUM,
                "duration_minutes": 40,
                "required_contributions": 4,
                "contribution_types": ["research_points", "rare_materials", "credits"],
                "rewards_per_contributor": {
                    "xp": 350,
                    "credits": 800,
                    "karma": 15,
                    "guild_reputation": 45
                },
                "guild_benefits": {
                    "technology_unlock": "Advanced Tech",
                    "crafting_bonus": "+15%",
                    "description": "Guild unlocks advanced technology, improving crafting by 15%"
                },
                "trait_impacts": {
                    "intelligence": 12,
                    "innovation": 10,
                    "cooperation": 8
                }
            },
            {
                "title": "Guild Defense System",
                "description": "Build automated defenses to protect guild territory and members.",
                "difficulty": TaskDifficulty.HARD,
                "duration_minutes": 55,
                "required_contributions": 5,
                "contribution_types": ["provide_materials", "combat_training", "credits"],
                "rewards_per_contributor": {
                    "xp": 500,
                    "credits": 1200,
                    "karma": 20,
                    "guild_reputation": 70
                },
                "guild_benefits": {
                    "defense_rating": "+25%",
                    "raid_protection": "Enhanced protection",
                    "description": "Guild territories gain 25% defense boost and enhanced raid protection"
                },
                "trait_impacts": {
                    "strategic_thinking": 12,
                    "cooperation": 15,
                    "loyalty": 10
                }
            }
        ]
    
    def generate_guild_benefit_task(
        self,
        guild_id: str,
        guild_level: int,
        guild_member_count: int
    ) -> Dict:
        """Generate a guild benefit task.
        
        Args:
            guild_id: The guild's ID
            guild_level: Guild's current level
            guild_member_count: Number of active guild members
        
        Returns:
            Dict with task data
        """
        # Filter by appropriate difficulty
        suitable_tasks = self._filter_by_guild_level(guild_level)
        
        # Select random task
        task_template = random.choice(suitable_tasks)
        
        # Adjust required contributions based on guild size
        adjusted_contributions = self._adjust_requirements(task_template, guild_member_count)
        
        # Generate task ID
        task_id = f"guild_benefit_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return {
            "_id": task_id,
            "task_id": task_id,
            "type": TaskType.GUILD_BENEFIT.value,
            "guild_id": guild_id,
            "title": task_template["title"],
            "description": task_template["description"],
            "difficulty": task_template["difficulty"].value,
            "duration_minutes": task_template["duration_minutes"],
            "required_contributions": adjusted_contributions,
            "contribution_types": task_template["contribution_types"],
            "current_contributions": 0,
            "contributors": [],
            "rewards_per_contributor": task_template["rewards_per_contributor"],
            "guild_benefits": task_template["guild_benefits"],
            "trait_impacts": task_template["trait_impacts"],
            "status": "active",
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=48),  # 48 hours to complete
            "progress_percentage": 0
        }
    
    def _filter_by_guild_level(self, guild_level: int) -> List[Dict]:
        """Filter tasks by guild level."""
        if guild_level < 5:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM]
        elif guild_level < 10:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM, TaskDifficulty.HARD]
        else:
            allowed = [TaskDifficulty.EASY, TaskDifficulty.MEDIUM, TaskDifficulty.HARD, TaskDifficulty.LEGENDARY]
        
        return [t for t in self.guild_tasks if t["difficulty"] in allowed]
    
    def _adjust_requirements(self, task_template: Dict, guild_member_count: int) -> int:
        """Adjust contribution requirements based on guild size."""
        base_requirement = task_template["required_contributions"]
        
        # Scale with guild size
        if guild_member_count < 10:
            return max(2, base_requirement - 1)
        elif guild_member_count < 30:
            return base_requirement
        else:
            return base_requirement + 2
    
    def contribute_to_guild_task(
        self,
        task: Dict,
        player_id: str,
        player_name: str,
        contribution_type: str,
        contribution_value: Optional[float] = 1.0
    ) -> Dict:
        """Player contributes to a guild task.
        
        Args:
            task: The guild benefit task
            player_id: ID of contributing player
            player_name: Name of contributing player
            contribution_type: Type of contribution
            contribution_value: Value/amount of contribution (default 1.0)
        
        Returns:
            Updated task with contribution added
        """
        # Check if player already contributed
        if any(c["player_id"] == player_id for c in task["contributors"]):
            raise ValueError("Already contributed to this task")
        
        # Validate contribution type
        if contribution_type not in task["contribution_types"]:
            raise ValueError(f"Invalid contribution type. Must be one of: {task['contribution_types']}")
        
        # Add contribution
        task["contributors"].append({
            "player_id": player_id,
            "player_name": player_name,
            "contribution_type": contribution_type,
            "contribution_value": contribution_value,
            "contributed_at": datetime.now()
        })
        
        # Update progress
        task["current_contributions"] = len(task["contributors"])
        task["progress_percentage"] = int((task["current_contributions"] / task["required_contributions"]) * 100)
        
        # Check if task is completed
        if task["current_contributions"] >= task["required_contributions"]:
            task["status"] = "completed"
            task["completed_at"] = datetime.now()
        
        return task
    
    def complete_guild_task(self, task: Dict, guild_data: Dict) -> Dict:
        """Complete a guild benefit task and apply rewards.
        
        Args:
            task: The completed guild benefit task
            guild_data: Current guild data
        
        Returns:
            Completion result with rewards for all contributors and guild benefits
        """
        if task["status"] != "completed":
            raise ValueError("Task not completed yet")
        
        result = {
            "task_id": task["task_id"],
            "completed_at": datetime.now(),
            "contributors": [],
            "guild_benefits_applied": task["guild_benefits"]
        }
        
        # Calculate rewards for each contributor
        for contributor in task["contributors"]:
            contributor_result = {
                "player_id": contributor["player_id"],
                "player_name": contributor["player_name"],
                "contribution_type": contributor["contribution_type"],
                "rewards": task["rewards_per_contributor"],
                "trait_impacts": task["trait_impacts"]
            }
            result["contributors"].append(contributor_result)
        
        # Guild-wide benefits description
        result["guild_announcement"] = (
            f"Guild Task Completed: {task['title']}! "
            f"Thanks to {len(task['contributors'])} contributors, the guild has gained: "
            f"{task['guild_benefits']['description']}"
        )
        
        return result
