"""Initial tasks service for new players without traits."""

import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.player.player import Player
from backend.models.tasks.initial_task import InitialTask, TaskChoice, TaskCompletion

class InitialTasksService:
    """Service for managing initial tasks for new players."""

    def __init__(self):
        self.task_templates = self._load_task_templates()

    def _load_task_templates(self) -> List[Dict[str, Any]]:
        """Load pre-defined initial task templates."""
        return [
            {
                "id": "find_lost_item",
                "title": "Find the Lost Item",
                "description": "A citizen has lost their important data chip. You found it nearby. What do you do?",
                "type": "moral_choice",
                "difficulty": "easy",
                "xp_reward": 50,
                "credits_reward": 100,
                "choices": [
                    {
                        "text": "Return it immediately to the owner",
                        "traits_impact": {"honesty": 5, "kindness": 3, "karma_points": 10}
                    },
                    {
                        "text": "Sell it for quick credits",
                        "traits_impact": {"greed": 4, "deceit": 3, "karma_points": -10}
                    },
                    {
                        "text": "Keep it and use it yourself",
                        "traits_impact": {"selfishness": 3, "karma_points": -5}
                    }
                ]
            },
            {
                "id": "help_stranger",
                "title": "Help a Stranger",
                "description": "You see someone struggling with heavy cargo containers. They look exhausted.",
                "type": "moral_choice",
                "difficulty": "easy",
                "xp_reward": 40,
                "credits_reward": 75,
                "choices": [
                    {
                        "text": "Offer to help them carry the containers",
                        "traits_impact": {"kindness": 4, "physical_strength": 2, "karma_points": 8}
                    },
                    {
                        "text": "Walk past, it's not your problem",
                        "traits_impact": {"selfishness": 2, "karma_points": -3}
                    },
                    {
                        "text": "Ask them to pay you for help",
                        "traits_impact": {"greed": 3, "negotiation": 1, "karma_points": 0}
                    }
                ]
            },
            {
                "id": "witness_theft",
                "title": "Witness a Theft",
                "description": "You witness someone stealing food from a vendor. The thief looks desperate and hungry.",
                "type": "moral_choice",
                "difficulty": "medium",
                "xp_reward": 60,
                "credits_reward": 120,
                "choices": [
                    {
                        "text": "Report them to authorities",
                        "traits_impact": {"honesty": 3, "courage": 2, "karma_points": 5}
                    },
                    {
                        "text": "Pretend you didn't see anything",
                        "traits_impact": {"cowardice": 2, "karma_points": -2}
                    },
                    {
                        "text": "Pay for the food and give it to them",
                        "traits_impact": {"generosity": 5, "empathy": 4, "karma_points": 15}
                    },
                    {
                        "text": "Demand a share of the stolen goods",
                        "traits_impact": {"greed": 4, "deceit": 3, "karma_points": -8}
                    }
                ]
            },
            {
                "id": "explore_area",
                "title": "Explore Unknown Territory",
                "description": "You discover an unexplored area in the city. It could be dangerous or rewarding.",
                "type": "exploration",
                "difficulty": "medium",
                "xp_reward": 70,
                "credits_reward": 150,
                "choices": [
                    {
                        "text": "Carefully explore and map the area",
                        "traits_impact": {"curiosity": 5, "patience": 3, "perception": 2, "karma_points": 5}
                    },
                    {
                        "text": "Rush in without thinking",
                        "traits_impact": {"recklessness": 4, "courage": 2, "karma_points": 0}
                    },
                    {
                        "text": "Avoid it, too risky",
                        "traits_impact": {"cowardice": 3, "karma_points": -3}
                    }
                ]
            },
            {
                "id": "fix_broken_robot",
                "title": "Repair Broken Robot",
                "description": "You find a damaged robot that was helping maintain the city. You have some technical knowledge.",
                "type": "skill_based",
                "difficulty": "medium",
                "xp_reward": 80,
                "credits_reward": 200,
                "choices": [
                    {
                        "text": "Try to repair it with available parts",
                        "traits_impact": {"technical_knowledge": 5, "patience": 2, "engineering": 3, "karma_points": 10}
                    },
                    {
                        "text": "Salvage it for valuable parts",
                        "traits_impact": {"greed": 3, "technical_knowledge": 1, "karma_points": -5}
                    },
                    {
                        "text": "Ignore it and move on",
                        "traits_impact": {"selfishness": 2, "karma_points": -3}
                    }
                ]
            },
            {
                "id": "conflict_resolution",
                "title": "Resolve a Dispute",
                "description": "Two citizens are arguing loudly over territory. The situation might escalate to violence.",
                "type": "social",
                "difficulty": "hard",
                "xp_reward": 90,
                "credits_reward": 180,
                "choices": [
                    {
                        "text": "Mediate peacefully between them",
                        "traits_impact": {"negotiation": 5, "charisma": 3, "wisdom": 2, "karma_points": 12}
                    },
                    {
                        "text": "Side with the stronger person",
                        "traits_impact": {"cowardice": 2, "manipulation": 2, "karma_points": -5}
                    },
                    {
                        "text": "Walk away, not your business",
                        "traits_impact": {"selfishness": 3, "cowardice": 2, "karma_points": -4}
                    },
                    {
                        "text": "Threaten both to stop fighting",
                        "traits_impact": {"courage": 3, "wrath": 2, "leadership": 1, "karma_points": 2}
                    }
                ]
            },
            {
                "id": "share_resources",
                "title": "Share Resources",
                "description": "You have extra food supplies. A family nearby is struggling to make ends meet.",
                "type": "moral_choice",
                "difficulty": "easy",
                "xp_reward": 50,
                "credits_reward": 100,
                "choices": [
                    {
                        "text": "Share your supplies with them",
                        "traits_impact": {"generosity": 5, "empathy": 3, "karma_points": 12}
                    },
                    {
                        "text": "Keep everything for yourself",
                        "traits_impact": {"selfishness": 4, "greed": 2, "karma_points": -8}
                    },
                    {
                        "text": "Sell them at a discounted price",
                        "traits_impact": {"generosity": 2, "trading": 2, "karma_points": 3}
                    }
                ]
            },
            {
                "id": "learn_new_skill",
                "title": "Learn Something New",
                "description": "You find an old data terminal with training programs. You have time to learn one skill.",
                "type": "skill_based",
                "difficulty": "medium",
                "xp_reward": 100,
                "credits_reward": 150,
                "choices": [
                    {
                        "text": "Study hacking techniques",
                        "traits_impact": {"hacking": 6, "intelligence": 3, "focus": 2, "karma_points": 5}
                    },
                    {
                        "text": "Practice combat training",
                        "traits_impact": {"physical_strength": 4, "endurance": 3, "discipline": 2, "karma_points": 5}
                    },
                    {
                        "text": "Learn negotiation tactics",
                        "traits_impact": {"negotiation": 5, "charisma": 3, "intelligence": 2, "karma_points": 5}
                    },
                    {
                        "text": "Skip the training",
                        "traits_impact": {"laziness": 3, "karma_points": -2}
                    }
                ]
            }
        ]

    async def get_initial_tasks(self, player_id: str, db: AsyncIOMotorDatabase, count: int = 3) -> List[InitialTask]:
        """Get random initial tasks for a new player."""
        # Check if player already has active initial tasks
        existing_tasks = await db.initial_tasks.find({
            "player_id": player_id,
            "status": "active"
        }).to_list(length=None)

        if len(existing_tasks) >= count:
            return [InitialTask(**task) for task in existing_tasks]

        # Select random tasks
        selected_templates = random.sample(self.task_templates, min(count, len(self.task_templates)))

        tasks = []
        for template in selected_templates:
            task = InitialTask(
                player_id=player_id,
                task_id=template["id"],
                title=template["title"],
                description=template["description"],
                type=template["type"],
                difficulty=template["difficulty"],
                xp_reward=template["xp_reward"],
                credits_reward=template["credits_reward"],
                choices=[TaskChoice(**choice) for choice in template["choices"]],
                status="active",
                created_at=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(hours=24)
            )
            tasks.append(task)

            # Save to database
            await db.initial_tasks.insert_one(task.model_dump(by_alias=True))

        return tasks

    async def complete_task(self, player_id: str, task_id: str, choice_index: int, db: AsyncIOMotorDatabase) -> TaskCompletion:
        """Complete an initial task and apply trait changes."""
        # Get task
        task_dict = await db.initial_tasks.find_one({
            "player_id": player_id,
            "task_id": task_id,
            "status": "active"
        })

        if not task_dict:
            raise ValueError("Task not found or already completed")

        task = InitialTask(**task_dict)

        # Validate choice
        if choice_index < 0 or choice_index >= len(task.choices):
            raise ValueError("Invalid choice index")

        selected_choice = task.choices[choice_index]

        # Get player
        player_dict = await db.players.find_one({"_id": player_id})
        if not player_dict:
            raise ValueError("Player not found")

        player = Player(**player_dict)

        # Apply trait changes
        traits_dict = player.traits.model_dump()
        karma_change = 0

        for trait_name, change in selected_choice.traits_impact.items():
            if trait_name == "karma_points":
                karma_change = change
            elif trait_name in traits_dict:
                # Update trait value (clamped between 0-100)
                current_value = traits_dict[trait_name]
                new_value = max(0, min(100, current_value + change))
                traits_dict[trait_name] = new_value

        # Update player in database
        await db.players.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "traits": traits_dict,
                    "karma_points": player.karma_points + karma_change,
                    "xp": player.xp + task.xp_reward,
                    "currencies.credits": player.currencies.credits + task.credits_reward
                },
                "$inc": {
                    "stats.quests_completed": 1,
                    "stats.total_actions": 1
                }
            }
        )

        # Mark task as completed
        await db.initial_tasks.update_one(
            {"_id": task_dict["_id"]},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow(),
                    "choice_made": choice_index
                }
            }
        )

        # Create completion result
        completion = TaskCompletion(
            task_id=task_id,
            title=task.title,
            choice_text=selected_choice.text,
            traits_changed=selected_choice.traits_impact,
            xp_gained=task.xp_reward,
            credits_gained=task.credits_reward,
            karma_change=karma_change
        )

        return completion

    async def get_player_progress(self, player_id: str, db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """Get player's initial tasks progress."""
        total_tasks = await db.initial_tasks.count_documents({"player_id": player_id})
        completed_tasks = await db.initial_tasks.count_documents({
            "player_id": player_id,
            "status": "completed"
        })
        active_tasks = await db.initial_tasks.count_documents({
            "player_id": player_id,
            "status": "active"
        })

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "active_tasks": active_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
