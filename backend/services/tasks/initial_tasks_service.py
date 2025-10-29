"""Initial tasks service for new players without traits.
Now integrated with Gemini AI task generator.
"""

import random
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.player.player import Player
from backend.models.tasks.initial_task import InitialTask, TaskChoice, TaskCompletion
from backend.services.ai.task_generator import TaskGenerator
import logging

logger = logging.getLogger(__name__)

class InitialTasksService:
    """Service for managing initial tasks for new players."""

    def __init__(self):
        self.task_generator = TaskGenerator()
        logger.info("✅ InitialTasksService initialized with Gemini AI")

    async def get_initial_tasks(self, player_id: str, db: AsyncIOMotorDatabase, count: int = 3) -> List[InitialTask]:
        """Get AI-generated initial tasks for a new player."""
        # Check if player already has active initial tasks
        existing_tasks = await db.initial_tasks.find({
            "player_id": player_id,
            "status": "active"
        }).to_list(length=None)

        if len(existing_tasks) >= count:
            logger.info(f"📋 Player {player_id} already has {len(existing_tasks)} active tasks")
            return [InitialTask(**task) for task in existing_tasks]

        # Get player data
        player_dict = await db.players.find_one({"_id": player_id})
        if not player_dict:
            raise ValueError("Player not found")

        # Generate tasks using Gemini AI
        tasks = []
        tasks_needed = count - len(existing_tasks)
        
        logger.info(f"🤖 Generating {tasks_needed} AI-powered initial tasks for player {player_dict.get('username')}...")
        
        for i in range(tasks_needed):
            try:
                # Generate task with Gemini AI
                task_data = await self.task_generator.generate_initial_task(player_dict)
                
                # Convert to InitialTask model
                task = InitialTask(
                    player_id=player_id,
                    task_id=task_data.get('task_id', f"ai_task_{datetime.utcnow().timestamp()}_{i}"),
                    title=task_data['title'],
                    description=task_data['description'],
                    type=task_data.get('type', 'moral_choice'),
                    difficulty=task_data.get('difficulty', 'easy'),
                    xp_reward=task_data.get('xp_reward', 50),
                    credits_reward=task_data.get('credits_reward', 100),
                    choices=[TaskChoice(**choice) for choice in task_data.get('choices', [])],
                    status="active",
                    created_at=datetime.utcnow(),
                    expires_at=datetime.utcnow() + timedelta(hours=24)
                )
                tasks.append(task)

                # Save to database
                await db.initial_tasks.insert_one(task.model_dump(by_alias=True))
                logger.info(f"✅ Task {i+1}/{tasks_needed} generated: '{task.title}'")
                
            except Exception as e:
                logger.error(f"❌ Failed to generate task {i+1}: {e}")
                continue

        # Combine with existing tasks
        all_tasks = [InitialTask(**t) for t in existing_tasks] + tasks
        logger.info(f"✨ Returning {len(all_tasks)} total initial tasks")
        
        return all_tasks

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
                logger.info(f"  ➡️ {trait_name}: {current_value:.1f} → {new_value:.1f} ({change:+d})")

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

        logger.info(f"✅ Task completed: '{task.title}' | XP: +{task.xp_reward} | Credits: +{task.credits_reward} | Karma: {karma_change:+d}")
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
