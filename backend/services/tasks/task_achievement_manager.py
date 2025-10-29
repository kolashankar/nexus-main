"""Task achievement manager - manages achievements for task completions."""

from typing import Dict, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

class TaskAchievementManager:
    """Manages task-related achievements and milestones."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.achievements_collection = db.player_achievements
        self.history_collection = db.task_history
        
        # Define task achievements
        self.achievements = [
            {
                "id": "first_task",
                "name": "First Steps",
                "description": "Complete your first task",
                "icon": "🎯",
                "requirement": {"type": "total_tasks", "value": 1},
                "rewards": {"xp": 100, "credits": 500}
            },
            {
                "id": "task_10",
                "name": "Getting Started",
                "description": "Complete 10 tasks",
                "icon": "⭐",
                "requirement": {"type": "total_tasks", "value": 10},
                "rewards": {"xp": 500, "credits": 2000}
            },
            {
                "id": "task_50",
                "name": "Experienced",
                "description": "Complete 50 tasks",
                "icon": "🏆",
                "requirement": {"type": "total_tasks", "value": 50},
                "rewards": {"xp": 2000, "credits": 10000, "items": ["veteran_badge"]}
            },
            {
                "id": "task_100",
                "name": "Task Master",
                "description": "Complete 100 tasks",
                "icon": "👑",
                "requirement": {"type": "total_tasks", "value": 100},
                "rewards": {"xp": 5000, "credits": 25000, "items": ["task_master_crown"]}
            },
            {
                "id": "good_deeds_10",
                "name": "Good Samaritan",
                "description": "Complete 10 tasks with positive karma",
                "icon": "😇",
                "requirement": {"type": "karma_tasks", "karma_type": "positive", "value": 10},
                "rewards": {"xp": 1000, "karma": 50, "credits": 5000}
            },
            {
                "id": "dark_path_10",
                "name": "Dark Path",
                "description": "Complete 10 tasks with negative karma",
                "icon": "😈",
                "requirement": {"type": "karma_tasks", "karma_type": "negative", "value": 10},
                "rewards": {"xp": 1000, "karma": -50, "credits": 5000}
            },
            {
                "id": "perfect_week",
                "name": "Perfect Week",
                "description": "Complete at least 1 task every day for 7 days",
                "icon": "📅",
                "requirement": {"type": "streak", "value": 7},
                "rewards": {"xp": 1500, "credits": 7500}
            },
            {
                "id": "legendary_complete",
                "name": "Legend",
                "description": "Complete 5 legendary difficulty tasks",
                "icon": "💎",
                "requirement": {"type": "difficulty", "difficulty": "legendary", "value": 5},
                "rewards": {"xp": 3000, "credits": 15000, "items": ["legendary_gem"]}
            },
            {
                "id": "versatile",
                "name": "Versatile",
                "description": "Complete at least 5 tasks of each type",
                "icon": "🎭",
                "requirement": {"type": "variety", "value": 5},
                "rewards": {"xp": 2500, "credits": 12000}
            },
            {
                "id": "speed_runner",
                "name": "Speed Runner",
                "description": "Complete 10 tasks in under 70% of the time limit",
                "icon": "⚡",
                "requirement": {"type": "fast_completion", "value": 10},
                "rewards": {"xp": 2000, "credits": 10000}
            },
            {
                "id": "team_player",
                "name": "Team Player",
                "description": "Complete 20 co-op tasks",
                "icon": "🤝",
                "requirement": {"type": "task_type", "task_type": "coop", "value": 20},
                "rewards": {"xp": 2500, "credits": 12500}
            },
            {
                "id": "champion",
                "name": "Champion",
                "description": "Win 15 competitive challenges",
                "icon": "🥇",
                "requirement": {"type": "competitive_wins", "value": 15},
                "rewards": {"xp": 3000, "credits": 15000, "items": ["champion_trophy"]}
            },
            {
                "id": "moral_compass",
                "name": "Moral Compass",
                "description": "Complete 25 moral choice tasks",
                "icon": "⚖️",
                "requirement": {"type": "task_type", "task_type": "moral_choice", "value": 25},
                "rewards": {"xp": 2000, "credits": 10000}
            },
            {
                "id": "guild_hero",
                "name": "Guild Hero",
                "description": "Complete 10 guild benefit tasks",
                "icon": "🛡️",
                "requirement": {"type": "task_type", "task_type": "guild_benefit", "value": 10},
                "rewards": {"xp": 2000, "guild_reputation": 100, "credits": 10000}
            },
            {
                "id": "karma_neutral",
                "name": "Balanced",
                "description": "Maintain karma between -10 and +10 for 30 days",
                "icon": "☯️",
                "requirement": {"type": "karma_balance", "days": 30},
                "rewards": {"xp": 1500, "credits": 7500}
            }
        ]
    
    async def check_and_award_achievements(
        self,
        player_id: str
    ) -> List[Dict]:
        """Check if player has earned any new achievements.
        
        Args:
            player_id: Player's ID
        
        Returns:
            List of newly earned achievements
        """
        # Get player's current achievements
        player_achievements = await self.achievements_collection.find_one(
            {"player_id": player_id}
        ) or {"player_id": player_id, "earned": []}
        
        earned_ids = set(a["achievement_id"] for a in player_achievements.get("earned", []))
        
        # Check each achievement
        newly_earned = []
        
        for achievement in self.achievements:
            if achievement["id"] in earned_ids:
                continue  # Already earned
            
            # Check if requirement is met
            if await self._check_requirement(player_id, achievement["requirement"]):
                # Award achievement
                earned_achievement = {
                    "achievement_id": achievement["id"],
                    "name": achievement["name"],
                    "description": achievement["description"],
                    "icon": achievement["icon"],
                    "earned_at": datetime.now(),
                    "rewards": achievement["rewards"]
                }
                
                newly_earned.append(earned_achievement)
        
        # Update player achievements
        if newly_earned:
            await self.achievements_collection.update_one(
                {"player_id": player_id},
                {
                    "$push": {"earned": {"$each": newly_earned}},
                    "$set": {"last_updated": datetime.now()}
                },
                upsert=True
            )
            
            # Apply rewards to player
            for achievement in newly_earned:
                await self._apply_achievement_rewards(player_id, achievement["rewards"])
        
        return newly_earned
    
    async def _check_requirement(
        self,
        player_id: str,
        requirement: Dict
    ) -> bool:
        """Check if player meets achievement requirement.
        
        Args:
            player_id: Player's ID
            requirement: Requirement specification
        
        Returns:
            True if requirement is met
        """
        req_type = requirement["type"]
        
        if req_type == "total_tasks":
            count = await self.history_collection.count_documents({"player_id": player_id})
            return count >= requirement["value"]
        
        elif req_type == "karma_tasks":
            karma_type = requirement["karma_type"]
            if karma_type == "positive":
                query = {"player_id": player_id, "karma_change": {"$gt": 0}}
            else:
                query = {"player_id": player_id, "karma_change": {"$lt": 0}}
            count = await self.history_collection.count_documents(query)
            return count >= requirement["value"]
        
        elif req_type == "streak":
            # Check streak from task history
            history = await self.history_collection.find(
                {"player_id": player_id}
            ).sort("completed_at", -1).limit(100).to_list(length=100)
            
            if not history:
                return False
            
            # Count consecutive days with completions
            streak = 0
            check_date = datetime.now().date()
            
            for record in history:
                if record["completed_at"].date() == check_date:
                    streak += 1
                    check_date = check_date - timedelta(days=1)
                elif record["completed_at"].date() < check_date:
                    break
            
            return streak >= requirement["value"]
        
        elif req_type == "difficulty":
            count = await self.history_collection.count_documents({
                "player_id": player_id,
                "difficulty": requirement["difficulty"]
            })
            return count >= requirement["value"]
        
        elif req_type == "variety":
            # Check if player has completed required count of each task type
            pipeline = [
                {"$match": {"player_id": player_id}},
                {"$group": {"_id": "$task_type", "count": {"$sum": 1}}}
            ]
            cursor = self.history_collection.aggregate(pipeline)
            type_counts = await cursor.to_list(length=100)
            
            # Check if all types have at least the required count
            min_count = min((tc["count"] for tc in type_counts), default=0)
            return min_count >= requirement["value"]
        
        elif req_type == "fast_completion":
            # Count tasks completed under 70% time
            fast_count = 0
            history = await self.history_collection.find(
                {"player_id": player_id, "time_taken_minutes": {"$ne": None}}
            ).to_list(length=1000)
            
            for record in history:
                if record.get("time_taken_minutes") and record.get("duration_minutes"):
                    if record["time_taken_minutes"] < record["duration_minutes"] * 0.7:
                        fast_count += 1
            
            return fast_count >= requirement["value"]
        
        elif req_type == "task_type":
            count = await self.history_collection.count_documents({
                "player_id": player_id,
                "task_type": requirement["task_type"]
            })
            return count >= requirement["value"]
        
        elif req_type == "competitive_wins":
            # Check competitive task wins
            count = await self.history_collection.count_documents({
                "player_id": player_id,
                "task_type": "competitive",
                "success": True,
                "result": "won"  # Assuming this field exists
            })
            return count >= requirement["value"]
        
        return False
    
    async def _apply_achievement_rewards(
        self,
        player_id: str,
        rewards: Dict
    ) -> None:
        """Apply achievement rewards to player.
        
        Args:
            player_id: Player's ID
            rewards: Rewards to apply
        """
        updates = {}
        
        if "xp" in rewards:
            updates["xp"] = rewards["xp"]
        
        if "credits" in rewards:
            updates["currencies.credits"] = rewards["credits"]
        
        if "karma" in rewards:
            updates["karma"] = rewards["karma"]
        
        if "guild_reputation" in rewards:
            updates["guild_reputation"] = rewards["guild_reputation"]
        
        if updates:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": updates}
            )
        
        # Add items to inventory
        if "items" in rewards:
            for item in rewards["items"]:
                await self.db.player_inventory.update_one(
                    {"player_id": player_id},
                    {"$push": {"items": {"item_id": item, "acquired_at": datetime.now()}}},
                    upsert=True
                )
    
    async def get_player_achievements(
        self,
        player_id: str
    ) -> Dict:
        """Get player's earned and available achievements.
        
        Args:
            player_id: Player's ID
        
        Returns:
            Achievement data
        """
        player_achievements = await self.achievements_collection.find_one(
            {"player_id": player_id}
        ) or {"earned": []}
        
        earned_ids = set(a["achievement_id"] for a in player_achievements.get("earned", []))
        
        earned = [
            ach for ach in self.achievements
            if ach["id"] in earned_ids
        ]
        
        locked = [
            ach for ach in self.achievements
            if ach["id"] not in earned_ids
        ]
        
        return {
            "earned": earned,
            "locked": locked,
            "total_earned": len(earned),
            "total_available": len(self.achievements),
            "completion_percentage": round(len(earned) / len(self.achievements) * 100, 1) if self.achievements else 0
        }
    
    async def get_achievement_progress(
        self,
        player_id: str,
        achievement_id: str
    ) -> Dict:
        """Get progress towards a specific achievement.
        
        Args:
            player_id: Player's ID
            achievement_id: Achievement ID
        
        Returns:
            Progress data
        """
        achievement = next((a for a in self.achievements if a["id"] == achievement_id), None)
        
        if not achievement:
            return {"error": "Achievement not found"}
        
        requirement = achievement["requirement"]
        req_type = requirement["type"]
        target = requirement["value"]
        
        # Calculate current progress based on type
        if req_type == "total_tasks":
            current = await self.history_collection.count_documents({"player_id": player_id})
        elif req_type == "karma_tasks":
            karma_type = requirement["karma_type"]
            query = {"player_id": player_id, "karma_change": {"$gt" if karma_type == "positive" else "$lt": 0}}
            current = await self.history_collection.count_documents(query)
        elif req_type == "task_type":
            current = await self.history_collection.count_documents({
                "player_id": player_id,
                "task_type": requirement["task_type"]
            })
        else:
            current = 0  # Default for complex requirements
        
        return {
            "achievement_id": achievement_id,
            "name": achievement["name"],
            "description": achievement["description"],
            "current": current,
            "target": target,
            "percentage": round(min(current / target * 100, 100), 1) if target > 0 else 0,
            "completed": current >= target
        }
