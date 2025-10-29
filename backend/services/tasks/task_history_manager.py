"""Task history manager - tracks and retrieves player's task completion history."""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

class TaskHistoryManager:
    """Manages player task completion history."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.history_collection = db.task_history
    
    async def record_task_completion(
        self,
        player_id: str,
        task_data: Dict,
        choice_made: Optional[Dict] = None,
        completion_result: Dict = None
    ) -> Dict:
        """Record a task completion in history.
        
        Args:
            player_id: Player's ID
            task_data: The task that was completed
            choice_made: The choice the player made (if applicable)
            completion_result: Results of task completion
        
        Returns:
            History record
        """
        history_record = {
            "_id": f"history_{datetime.now().strftime('%Y%m%d%H%M%S')}_{player_id[:8]}",
            "player_id": player_id,
            "task_id": task_data.get("task_id"),
            "task_type": task_data.get("type"),
            "task_title": task_data.get("title"),
            "task_description": task_data.get("description"),
            "difficulty": task_data.get("difficulty"),
            "completed_at": datetime.now(),
            "time_taken_minutes": completion_result.get("time_taken_minutes") if completion_result else None,
            "success": completion_result.get("success", True) if completion_result else True,
            "choice_made": choice_made,
            "rewards_received": completion_result.get("rewards") if completion_result else task_data.get("rewards"),
            "trait_changes": completion_result.get("trait_changes") if completion_result else {},
            "xp_gained": completion_result.get("xp_gained") if completion_result else 0,
            "karma_change": completion_result.get("karma_change") if completion_result else 0,
        }
        
        await self.history_collection.insert_one(history_record)
        return history_record
    
    async def get_player_history(
        self,
        player_id: str,
        limit: int = 50,
        skip: int = 0,
        task_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """Get player's task history with optional filters.
        
        Args:
            player_id: Player's ID
            limit: Maximum number of records to return
            skip: Number of records to skip (pagination)
            task_type: Filter by task type
            start_date: Filter by start date
            end_date: Filter by end date
        
        Returns:
            List of history records
        """
        query = {"player_id": player_id}
        
        # Add filters
        if task_type:
            query["task_type"] = task_type
        
        if start_date or end_date:
            query["completed_at"] = {}
            if start_date:
                query["completed_at"]["$gte"] = start_date
            if end_date:
                query["completed_at"]["$lte"] = end_date
        
        # Get history records
        cursor = self.history_collection.find(query).sort("completed_at", -1).skip(skip).limit(limit)
        history = await cursor.to_list(length=limit)
        
        return history
    
    async def get_history_stats(
        self,
        player_id: str,
        period_days: int = 30
    ) -> Dict:
        """Get statistical summary of player's task history.
        
        Args:
            player_id: Player's ID
            period_days: Number of days to analyze
        
        Returns:
            Dictionary with statistics
        """
        start_date = datetime.now() - timedelta(days=period_days)
        
        # Get all history in period
        history = await self.get_player_history(
            player_id=player_id,
            start_date=start_date,
            limit=1000
        )
        
        if not history:
            return {
                "total_tasks_completed": 0,
                "success_rate": 0,
                "tasks_by_type": {},
                "tasks_by_difficulty": {},
                "total_xp_gained": 0,
                "total_karma_change": 0,
                "average_completion_time": 0,
                "most_common_choices": [],
                "period_days": period_days
            }
        
        # Calculate statistics
        total_tasks = len(history)
        successful_tasks = sum(1 for h in history if h.get("success", True))
        
        # Tasks by type
        tasks_by_type = {}
        for record in history:
            task_type = record.get("task_type", "unknown")
            tasks_by_type[task_type] = tasks_by_type.get(task_type, 0) + 1
        
        # Tasks by difficulty
        tasks_by_difficulty = {}
        for record in history:
            difficulty = record.get("difficulty", "unknown")
            tasks_by_difficulty[difficulty] = tasks_by_difficulty.get(difficulty, 0) + 1
        
        # Total rewards
        total_xp = sum(record.get("xp_gained", 0) for record in history)
        total_karma = sum(record.get("karma_change", 0) for record in history)
        
        # Average completion time
        completion_times = [r.get("time_taken_minutes", 0) for r in history if r.get("time_taken_minutes")]
        avg_time = sum(completion_times) / len(completion_times) if completion_times else 0
        
        # Most common choices
        choice_counts = {}
        for record in history:
            if record.get("choice_made"):
                choice_text = record["choice_made"].get("text", "Unknown")
                choice_counts[choice_text] = choice_counts.get(choice_text, 0) + 1
        
        most_common = sorted(choice_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_tasks_completed": total_tasks,
            "success_rate": (successful_tasks / total_tasks * 100) if total_tasks > 0 else 0,
            "tasks_by_type": tasks_by_type,
            "tasks_by_difficulty": tasks_by_difficulty,
            "total_xp_gained": total_xp,
            "total_karma_change": total_karma,
            "average_completion_time": round(avg_time, 1),
            "most_common_choices": [{
                "choice": choice,
                "count": count,
                "percentage": round(count / total_tasks * 100, 1)
            } for choice, count in most_common],
            "period_days": period_days
        }
    
    async def get_task_streak(
        self,
        player_id: str
    ) -> Dict:
        """Get player's task completion streak.
        
        Args:
            player_id: Player's ID
        
        Returns:
            Streak information
        """
        # Get recent history
        history = await self.get_player_history(
            player_id=player_id,
            limit=100
        )
        
        if not history:
            return {
                "current_streak": 0,
                "longest_streak": 0,
                "last_completion": None
            }
        
        # Calculate current streak (consecutive days with completions)
        current_streak = 0
        check_date = datetime.now().date()
        
        for record in history:
            completion_date = record["completed_at"].date()
            
            if completion_date == check_date:
                current_streak += 1
                check_date = check_date - timedelta(days=1)
            elif completion_date < check_date:
                break
        
        # Calculate longest streak
        longest_streak = 0
        temp_streak = 1
        
        for i in range(1, len(history)):
            prev_date = history[i-1]["completed_at"].date()
            curr_date = history[i]["completed_at"].date()
            
            if (prev_date - curr_date).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
        
        return {
            "current_streak": current_streak,
            "longest_streak": max(longest_streak, current_streak),
            "last_completion": history[0]["completed_at"] if history else None
        }
    
    async def get_recent_completions(
        self,
        player_id: str,
        days: int = 7
    ) -> List[Dict]:
        """Get player's recent task completions grouped by day.
        
        Args:
            player_id: Player's ID
            days: Number of recent days to retrieve
        
        Returns:
            List of daily completion counts
        """
        start_date = datetime.now() - timedelta(days=days)
        
        history = await self.get_player_history(
            player_id=player_id,
            start_date=start_date,
            limit=500
        )
        
        # Group by day
        daily_completions = {}
        for record in history:
            date_key = record["completed_at"].date().isoformat()
            if date_key not in daily_completions:
                daily_completions[date_key] = {
                    "date": date_key,
                    "count": 0,
                    "xp_gained": 0,
                    "karma_change": 0
                }
            
            daily_completions[date_key]["count"] += 1
            daily_completions[date_key]["xp_gained"] += record.get("xp_gained", 0)
            daily_completions[date_key]["karma_change"] += record.get("karma_change", 0)
        
        # Fill in missing days with zero counts
        result = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).date().isoformat()
            if date in daily_completions:
                result.append(daily_completions[date])
            else:
                result.append({
                    "date": date,
                    "count": 0,
                    "xp_gained": 0,
                    "karma_change": 0
                })
        
        return sorted(result, key=lambda x: x["date"])
    
    async def delete_old_history(
        self,
        days_to_keep: int = 90
    ) -> int:
        """Delete task history older than specified days.
        
        Args:
            days_to_keep: Number of days of history to keep
        
        Returns:
            Number of records deleted
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        result = await self.history_collection.delete_many({
            "completed_at": {"$lt": cutoff_date}
        })
        
        return result.deleted_count
