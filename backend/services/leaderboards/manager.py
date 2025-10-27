"""Leaderboard Manager Service."""

from typing import Dict, Optional, Any
from datetime import datetime
from backend.core.database import db


class LeaderboardManager:
    """Service for managing all leaderboards."""

    def __init__(self):
        self.db = db
        self.leaderboard_configs = {
            "karma": {
                "field": "karma_points",
                "collection": "players",
                "season_field": "season_karma_earned"
            },
            "wealth": {
                "field": "currencies.credits",
                "collection": "players",
                "season_field": "season_wealth_earned"
            },
            "combat": {
                "field": "stats.pvp_wins",
                "collection": "players",
                "season_field": "season_combat_wins"
            },
            "achievement": {
                "field": "achievement_points",
                "collection": "players",
                "season_field": "season_achievements"
            },
            "guild": {
                "field": "level",
                "collection": "guilds",
                "season_field": None
            }
        }

    async def get_leaderboard(
        self,
        leaderboard_type: str,
        limit: int = 50,
        season_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get leaderboard rankings."""
        if leaderboard_type not in self.leaderboard_configs:
            raise ValueError(f"Unknown leaderboard type: {leaderboard_type}")

        config = self.leaderboard_configs[leaderboard_type]

        if season_id and config["season_field"]:
            # Get seasonal leaderboard
            return await self._get_seasonal_leaderboard(
                leaderboard_type=leaderboard_type,
                season_id=season_id,
                limit=limit
            )
        else:
            # Get all-time leaderboard
            return await self._get_alltime_leaderboard(
                leaderboard_type=leaderboard_type,
                limit=limit
            )

    async def _get_alltime_leaderboard(
        self,
        leaderboard_type: str,
        limit: int
    ) -> Dict[str, Any]:
        """Get all-time leaderboard."""
        config = self.leaderboard_configs[leaderboard_type]
        collection = getattr(self.db, config["collection"])
        field = config["field"]

        # Get sorted entries
        cursor = collection.find().sort(field, -1).limit(limit)
        entries = await cursor.to_list(length=limit)

        # Format entries
        formatted_entries = []
        for rank, entry in enumerate(entries, 1):
            formatted_entry = await self._format_entry(
                entry=entry,
                rank=rank,
                field=field,
                leaderboard_type=leaderboard_type
            )
            formatted_entries.append(formatted_entry)

        # Get total count
        total_entries = await collection.count_documents({})

        return {
            "leaderboard_type": leaderboard_type,
            "entries": formatted_entries,
            "total_entries": total_entries,
            "last_updated": datetime.utcnow().isoformat(),
            "season_id": None
        }

    async def _get_seasonal_leaderboard(
        self,
        leaderboard_type: str,
        season_id: str,
        limit: int
    ) -> Dict[str, Any]:
        """Get seasonal leaderboard."""
        config = self.leaderboard_configs[leaderboard_type]
        season_field = config["season_field"]

        # Get seasonal progress
        cursor = self.db.player_season_progress.find({
            "season_id": season_id
        }).sort(season_field, -1).limit(limit)

        entries = await cursor.to_list(length=limit)

        # Format entries
        formatted_entries = []
        for rank, entry in enumerate(entries, 1):
            # Get player data
            player = await self.db.players.find_one({"_id": entry["player_id"]})
            if not player:
                continue

            formatted_entry = {
                "rank": rank,
                "player_id": entry["player_id"],
                "username": player.get("username", "Unknown"),
                "value": entry.get(season_field, 0),
                "level": player.get("level"),
                "guild_name": await self._get_guild_name(player.get("guild_id")),
                "title": player.get("active_title"),
                "change_24h": None  # Would need historical data
            }
            formatted_entries.append(formatted_entry)

        # Get total count
        total_entries = await self.db.player_season_progress.count_documents({
            "season_id": season_id
        })

        return {
            "leaderboard_type": leaderboard_type,
            "entries": formatted_entries,
            "total_entries": total_entries,
            "last_updated": datetime.utcnow().isoformat(),
            "season_id": season_id
        }

    async def _format_entry(
        self,
        entry: Dict[str, Any],
        rank: int,
        field: str,
        leaderboard_type: str
    ) -> Dict[str, Any]:
        """Format a leaderboard entry."""
        # Get nested field value
        value = entry
        for part in field.split('.'):
            value = value.get(part, 0)

        formatted = {
            "rank": rank,
            "player_id": str(entry.get("_id", "")),
            "value": value,
            "change_24h": None
        }

        # Add type-specific fields
        if leaderboard_type == "guild":
            formatted["username"] = entry.get("name", "Unknown Guild")
            formatted["level"] = entry.get("level")
            formatted["guild_name"] = None
        else:
            formatted["username"] = entry.get("username", "Unknown")
            formatted["level"] = entry.get("level")
            formatted["guild_name"] = await self._get_guild_name(entry.get("guild_id"))
            formatted["title"] = entry.get("active_title")

        return formatted

    async def _get_guild_name(self, guild_id: Optional[str]) -> Optional[str]:
        """Get guild name from ID."""
        if not guild_id:
            return None

        guild = await self.db.guilds.find_one({"_id": guild_id})
        return guild.get("name") if guild else None

    async def get_player_rank(
        self,
        player_id: str,
        leaderboard_type: str,
        season_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get player's rank in a leaderboard."""
        if leaderboard_type not in self.leaderboard_configs:
            raise ValueError(f"Unknown leaderboard type: {leaderboard_type}")

        config = self.leaderboard_configs[leaderboard_type]

        if season_id and config["season_field"]:
            return await self._get_seasonal_player_rank(
                player_id=player_id,
                leaderboard_type=leaderboard_type,
                season_id=season_id
            )
        else:
            return await self._get_alltime_player_rank(
                player_id=player_id,
                leaderboard_type=leaderboard_type
            )

    async def _get_alltime_player_rank(
        self,
        player_id: str,
        leaderboard_type: str
    ) -> Dict[str, Any]:
        """Get player's all-time rank."""
        config = self.leaderboard_configs[leaderboard_type]
        collection = getattr(self.db, config["collection"])
        field = config["field"]

        # Get player data
        player = await collection.find_one({"_id": player_id})
        if not player:
            raise ValueError("Player not found")

        # Get player's value
        value = player
        for part in field.split('.'):
            value = value.get(part, 0)

        # Count players with higher value
        rank = await collection.count_documents({
            field: {"$gt": value}
        }) + 1

        # Get total players
        total_players = await collection.count_documents({})

        # Calculate percentile
        percentile = ((total_players - rank) / total_players * \
                      100) if total_players > 0 else 0

        return {
            "player_id": player_id,
            "username": player.get("username", player.get("name", "Unknown")),
            "leaderboard_type": leaderboard_type,
            "rank": rank,
            "value": value,
            "percentile": percentile,
            "total_players": total_players,
            "change_24h": None
        }

    async def _get_seasonal_player_rank(
        self,
        player_id: str,
        leaderboard_type: str,
        season_id: str
    ) -> Dict[str, Any]:
        """Get player's seasonal rank."""
        config = self.leaderboard_configs[leaderboard_type]
        season_field = config["season_field"]

        # Get player's season progress
        progress = await self.db.player_season_progress.find_one({
            "player_id": player_id,
            "season_id": season_id
        })

        if not progress:
            raise ValueError("Player season progress not found")

        value = progress.get(season_field, 0)

        # Count players with higher value
        rank = await self.db.player_season_progress.count_documents({
            "season_id": season_id,
            season_field: {"$gt": value}
        }) + 1

        # Get total players
        total_players = await self.db.player_season_progress.count_documents({
            "season_id": season_id
        })

        # Calculate percentile
        percentile = ((total_players - rank) / total_players * \
                      100) if total_players > 0 else 0

        # Get player data
        player = await self.db.players.find_one({"_id": player_id})
        username = player.get("username", "Unknown") if player else "Unknown"

        return {
            "player_id": player_id,
            "username": username,
            "leaderboard_type": leaderboard_type,
            "rank": rank,
            "value": value,
            "percentile": percentile,
            "total_players": total_players,
            "change_24h": None
        }

    async def update_leaderboards(self):
        """Update/refresh all leaderboards (called periodically)."""
        # This would be called by a background task
        # For now, leaderboards are calculated on-demand
        pass
