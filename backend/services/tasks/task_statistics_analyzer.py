"""Task statistics analyzer - analyzes choice patterns and player statistics."""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

class TaskStatisticsAnalyzer:
    """Analyzes task completion statistics across all players."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.history_collection = db.task_history
        self.stats_cache_collection = db.task_statistics_cache
    
    async def get_global_choice_statistics(
        self,
        task_type: Optional[str] = None,
        days: int = 30
    ) -> Dict:
        """Get global statistics on player choices.
        
        Args:
            task_type: Filter by task type
            days: Number of days to analyze
        
        Returns:
            Choice statistics
        """
        start_date = datetime.now() - timedelta(days=days)
        
        query = {
            "completed_at": {"$gte": start_date},
            "choice_made": {"$ne": None}
        }
        
        if task_type:
            query["task_type"] = task_type
        
        # Get all completions with choices
        cursor = self.history_collection.find(query)
        history = await cursor.to_list(length=10000)
        
        if not history:
            return {
                "total_choices_made": 0,
                "choice_breakdown": {},
                "popular_choices": [],
                "task_types_analyzed": [],
                "period_days": days
            }
        
        # Analyze choices
        choice_counts = {}
        task_choices = {}  # Group by task title
        
        for record in history:
            choice = record.get("choice_made", {})
            choice_text = choice.get("text", "Unknown")
            task_title = record.get("task_title", "Unknown Task")
            
            # Global count
            choice_counts[choice_text] = choice_counts.get(choice_text, 0) + 1
            
            # Per-task breakdown
            if task_title not in task_choices:
                task_choices[task_title] = {}
            
            task_choices[task_title][choice_text] = task_choices[task_title].get(choice_text, 0) + 1
        
        # Calculate percentages per task
        task_statistics = {}
        for task_title, choices in task_choices.items():
            total = sum(choices.values())
            task_statistics[task_title] = {
                "total_completions": total,
                "choices": [
                    {
                        "choice": choice,
                        "count": count,
                        "percentage": round(count / total * 100, 1)
                    }
                    for choice, count in sorted(choices.items(), key=lambda x: x[1], reverse=True)
                ]
            }
        
        # Most popular choices overall
        popular_choices = sorted(choice_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_choices_made": len(history),
            "choice_breakdown": task_statistics,
            "popular_choices": [
                {
                    "choice": choice,
                    "count": count,
                    "percentage": round(count / len(history) * 100, 1)
                }
                for choice, count in popular_choices
            ],
            "task_types_analyzed": list(set(r.get("task_type") for r in history)),
            "period_days": days
        }
    
    async def get_task_popularity(
        self,
        days: int = 30
    ) -> List[Dict]:
        """Get most popular tasks by completion count.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            List of tasks sorted by popularity
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # Aggregate by task title
        pipeline = [
            {
                "$match": {
                    "completed_at": {"$gte": start_date}
                }
            },
            {
                "$group": {
                    "_id": "$task_title",
                    "count": {"$sum": 1},
                    "task_type": {"$first": "$task_type"},
                    "difficulty": {"$first": "$difficulty"},
                    "avg_success_rate": {"$avg": {"$cond": [{"$eq": ["$success", True]}, 1, 0]}}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 20
            }
        ]
        
        cursor = self.history_collection.aggregate(pipeline)
        results = await cursor.to_list(length=20)
        
        return [
            {
                "task_title": r["_id"],
                "completions": r["count"],
                "task_type": r.get("task_type", "unknown"),
                "difficulty": r.get("difficulty", "unknown"),
                "success_rate": round(r.get("avg_success_rate", 0) * 100, 1)
            }
            for r in results
        ]
    
    async def get_player_comparison(
        self,
        player_id: str,
        days: int = 30
    ) -> Dict:
        """Compare player's statistics to global averages.
        
        Args:
            player_id: Player's ID
            days: Number of days to analyze
        
        Returns:
            Comparison statistics
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # Get player stats
        player_history = await self.history_collection.find({
            "player_id": player_id,
            "completed_at": {"$gte": start_date}
        }).to_list(length=1000)
        
        # Get global stats
        global_history = await self.history_collection.find({
            "completed_at": {"$gte": start_date}
        }).to_list(length=10000)
        
        if not player_history or not global_history:
            return {
                "player_tasks_completed": len(player_history),
                "global_average_tasks": 0,
                "percentile": 0,
                "comparison": "Not enough data"
            }
        
        # Calculate player stats
        player_task_count = len(player_history)
        player_xp = sum(r.get("xp_gained", 0) for r in player_history)
        player_karma = sum(r.get("karma_change", 0) for r in player_history)
        
        # Calculate global averages
        players_task_counts = {}
        for record in global_history:
            pid = record["player_id"]
            players_task_counts[pid] = players_task_counts.get(pid, 0) + 1
        
        task_counts = list(players_task_counts.values())
        global_avg = sum(task_counts) / len(task_counts) if task_counts else 0
        
        # Calculate percentile
        below_player = sum(1 for count in task_counts if count < player_task_count)
        percentile = (below_player / len(task_counts) * 100) if task_counts else 0
        
        # Comparison message
        if percentile >= 90:
            comparison = "Exceptional! Top 10% of players"
        elif percentile >= 75:
            comparison = "Great! Above average player"
        elif percentile >= 50:
            comparison = "Good! Average player"
        elif percentile >= 25:
            comparison = "Below average"
        else:
            comparison = "Room for improvement"
        
        return {
            "player_tasks_completed": player_task_count,
            "player_total_xp": player_xp,
            "player_total_karma": player_karma,
            "global_average_tasks": round(global_avg, 1),
            "percentile": round(percentile, 1),
            "comparison": comparison,
            "rank_among_players": len(task_counts) - below_player,
            "total_active_players": len(task_counts)
        }
    
    async def get_choice_trends(
        self,
        task_title: str,
        days: int = 90
    ) -> Dict:
        """Get trends in choice selection over time for a specific task.
        
        Args:
            task_title: Title of the task
            days: Number of days to analyze
        
        Returns:
            Trend data
        """
        start_date = datetime.now() - timedelta(days=days)
        
        # Get all completions of this task
        history = await self.history_collection.find({
            "task_title": task_title,
            "completed_at": {"$gte": start_date},
            "choice_made": {"$ne": None}
        }).sort("completed_at", 1).to_list(length=5000)
        
        if not history:
            return {
                "task_title": task_title,
                "total_completions": 0,
                "trends": []
            }
        
        # Group by week
        weekly_choices = {}
        for record in history:
            week_key = record["completed_at"].strftime("%Y-W%W")
            choice = record.get("choice_made", {}).get("text", "Unknown")
            
            if week_key not in weekly_choices:
                weekly_choices[week_key] = {}
            
            weekly_choices[week_key][choice] = weekly_choices[week_key].get(choice, 0) + 1
        
        # Convert to trend format
        trends = []
        for week, choices in sorted(weekly_choices.items()):
            total = sum(choices.values())
            trends.append({
                "week": week,
                "total_completions": total,
                "choices": [
                    {
                        "choice": choice,
                        "count": count,
                        "percentage": round(count / total * 100, 1)
                    }
                    for choice, count in choices.items()
                ]
            })
        
        return {
            "task_title": task_title,
            "total_completions": len(history),
            "trends": trends
        }
    
    async def cache_statistics(
        self,
        cache_duration_hours: int = 1
    ) -> None:
        """Cache frequently accessed statistics for performance.
        
        Args:
            cache_duration_hours: How long to cache data
        """
        # Get global statistics
        global_stats = await self.get_global_choice_statistics(days=30)
        popular_tasks = await self.get_task_popularity(days=30)
        
        cache_data = {
            "_id": "global_stats_cache",
            "global_statistics": global_stats,
            "popular_tasks": popular_tasks,
            "cached_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=cache_duration_hours)
        }
        
        # Upsert cache
        await self.stats_cache_collection.update_one(
            {"_id": "global_stats_cache"},
            {"$set": cache_data},
            upsert=True
        )
    
    async def get_cached_statistics(self) -> Optional[Dict]:
        """Get cached statistics if available and not expired.
        
        Returns:
            Cached statistics or None if expired
        """
        cache = await self.stats_cache_collection.find_one({"_id": "global_stats_cache"})
        
        if not cache:
            return None
        
        # Check if expired
        if cache.get("expires_at", datetime.min) < datetime.now():
            return None
        
        return {
            "global_statistics": cache.get("global_statistics"),
            "popular_tasks": cache.get("popular_tasks"),
            "cached_at": cache.get("cached_at")
        }
