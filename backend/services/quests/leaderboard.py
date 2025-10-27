"""Quest leaderboard service"""

from typing import List, Dict, Any
from datetime import datetime, timedelta


class QuestLeaderboardService:
    """Manages quest leaderboards"""

    def __init__(self, db):
        self.db = db
        self.quests = db.quests
        self.players = db.players

    async def get_completion_leaderboard(
        self,
        timeframe: str = "all_time",
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get quest completion leaderboard"""
        # Build time filter
        time_filter = {}
        if timeframe == "daily":
            start = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            time_filter = {"completed_at": {"$gte": start}}
        elif timeframe == "weekly":
            start = datetime.utcnow() - timedelta(days=7)
            time_filter = {"completed_at": {"$gte": start}}
        elif timeframe == "monthly":
            start = datetime.utcnow() - timedelta(days=30)
            time_filter = {"completed_at": {"$gte": start}}

        # Aggregate completions by player
        pipeline = [
            {"$match": {"status": "completed", **time_filter}},
            {
                "$group": {
                    "_id": "$player_id",
                    "quests_completed": {"$sum": 1},
                    "total_xp_earned": {"$sum": "$rewards.xp"},
                }
            },
            {"$sort": {"quests_completed": -1}},
            {"$limit": limit}
        ]

        leaderboard = []
        rank = 1
        async for entry in self.quests.aggregate(pipeline):
            # Get player info
            player = await self.players.find_one({"_id": entry["_id"]})

            leaderboard.append({
                "rank": rank,
                "player_id": entry["_id"],
                "username": player.get("username") if player else "Unknown",
                "quests_completed": entry["quests_completed"],
                "total_xp_earned": entry.get("total_xp_earned", 0),
            })
            rank += 1

        return leaderboard

    async def get_speedrun_leaderboard(
        self,
        quest_type: str = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get fastest quest completions"""
        match_filter = {
            "status": "completed",
            "completion_time": {"$exists": True, "$gt": 0}
        }

        if quest_type:
            match_filter["quest_type"] = quest_type

        pipeline = [
            {"$match": match_filter},
            {"$sort": {"completion_time": 1}},
            {"$limit": limit}
        ]

        speedruns = []
        rank = 1
        async for quest in self.quests.aggregate(pipeline):
            player = await self.players.find_one({"_id": quest["player_id"]})

            speedruns.append({
                "rank": rank,
                "player_id": quest["player_id"],
                "username": player.get("username") if player else "Unknown",
                "quest_title": quest.get("title"),
                "completion_time": quest["completion_time"],
                "quest_type": quest.get("quest_type"),
            })
            rank += 1

        return speedruns

    async def get_player_rank(
        self,
        player_id: str,
        timeframe: str = "all_time",
    ) -> Dict[str, Any]:
        """Get player's rank on leaderboard"""
        leaderboard = await self.get_completion_leaderboard(timeframe, limit=10000)

        for entry in leaderboard:
            if entry["player_id"] == player_id:
                return entry

        return {
            "rank": None,
            "player_id": player_id,
            "quests_completed": 0,
            "message": "Not ranked yet",
        }
