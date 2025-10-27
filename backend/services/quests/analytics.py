"""Quest analytics service"""

from typing import Dict, Any, List
from datetime import datetime


class QuestAnalyticsService:
    """Provides analytics for quest system"""

    def __init__(self, db):
        self.db = db
        self.quests = db.quests
        self.players = db.players

    async def get_player_quest_stats(
        self,
        player_id: str,
    ) -> Dict[str, Any]:
        """Get quest statistics for a player"""
        # Count quests by status
        pipeline = [
            {"$match": {"player_id": player_id}},
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }}
        ]

        status_counts = {}
        async for doc in self.quests.aggregate(pipeline):
            status_counts[doc["_id"]] = doc["count"]

        # Count by quest type
        type_pipeline = [
            {"$match": {"player_id": player_id}},
            {"$group": {
                "_id": "$quest_type",
                "count": {"$sum": 1}
            }}
        ]

        type_counts = {}
        async for doc in self.quests.aggregate(type_pipeline):
            type_counts[doc["_id"]] = doc["count"]

        # Average completion time
        completed = await self.quests.find({
            "player_id": player_id,
            "status": "completed",
            "completion_time": {"$exists": True}
        }).to_list(length=1000)

        avg_time = 0
        if completed:
            total_time = sum(q.get("completion_time", 0) for q in completed)
            avg_time = total_time / len(completed)

        return {
            "total_quests": sum(status_counts.values()),
            "by_status": status_counts,
            "by_type": type_counts,
            "average_completion_time_seconds": avg_time,
            "completion_rate": (
                status_counts.get("completed", 0) /
                max(sum(status_counts.values()), 1)
            ) * 100,
        }

    async def get_global_quest_stats(self) -> Dict[str, Any]:
        """Get global quest statistics"""
        # Total quests
        total = await self.quests.count_documents({})

        # Active quests
        active = await self.quests.count_documents({"status": "active"})

        # Completed today
        today_start = datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        completed_today = await self.quests.count_documents({
            "status": "completed",
            "completed_at": {"$gte": today_start}
        })

        return {
            "total_quests": total,
            "active_quests": active,
            "completed_today": completed_today,
        }

    async def get_popular_quests(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular quest types"""
        pipeline = [
            {"$match": {"status": "completed"}},
            {"$group": {
                "_id": "$title",
                "count": {"$sum": 1},
                "avg_time": {"$avg": "$completion_time"}
            }},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]

        popular = []
        async for doc in self.quests.aggregate(pipeline):
            popular.append({
                "title": doc["_id"],
                "completions": doc["count"],
                "avg_completion_time": doc.get("avg_time", 0),
            })

        return popular
