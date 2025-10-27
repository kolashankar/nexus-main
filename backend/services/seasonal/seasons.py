"""Season Management Service."""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from backend.core.database import db
import uuid


class SeasonService:
    """Service for managing seasons."""

    def __init__(self):
        self.db = db

    async def create_season(
        self,
        season_number: int,
        name: str,
        duration_days: int = 90
    ) -> Dict[str, Any]:
        """Create a new season."""
        season_id = str(uuid.uuid4())
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=duration_days)

        season = {
            "season_id": season_id,
            "season_number": season_number,
            "name": name,
            "description": f"Season {season_number}: {name}",
            "theme": "default",
            "start_date": start_date,
            "end_date": end_date,
            "status": "active",
            "duration_days": duration_days,
            "exclusive_quests": [],
            "exclusive_items": [],
            "exclusive_superpowers": [],
            "battle_pass_id": None,
            "special_events": [],
            "season_end_rewards": {},
            "leaderboard_rewards": self._generate_leaderboard_rewards(),
            "total_players": 0,
            "active_players": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.db.seasons.insert_one(season)

        # Create battle pass for this season
        from backend.services.seasonal.battle_pass import BattlePassService
        bp_service = BattlePassService()
        battle_pass = await bp_service.create_battle_pass(
            season=season_number,
            name=f"{name} Battle Pass",
            start_date=start_date,
            end_date=end_date
        )

        # Link battle pass
        await self.db.seasons.update_one(
            {"season_id": season_id},
            {"$set": {"battle_pass_id": battle_pass["pass_id"]}}
        )

        return season

    def _generate_leaderboard_rewards(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate rewards for leaderboard rankings."""
        return {
            "karma": [
                {"rank": 1, "credits": 10000,
                    "karma_tokens": 1000, "title": "Karma Master"},
                {"rank": 2, "credits": 7500, "karma_tokens": 750,
                    "title": "Karma Expert"},
                {"rank": 3, "credits": 5000,
                    "karma_tokens": 500, "title": "Karma Adept"},
                {"ranks": [4, 10], "credits": 2500, "karma_tokens": 250},
                {"ranks": [11, 50], "credits": 1000, "karma_tokens": 100},
            ],
            "wealth": [
                {"rank": 1, "credits": 10000,
                    "exclusive_item": "golden_crown", "title": "Wealth King"},
                {"rank": 2, "credits": 7500, "exclusive_item": "silver_crown",
                    "title": "Wealth Prince"},
                {"rank": 3, "credits": 5000, "exclusive_item": "bronze_crown",
                    "title": "Wealth Noble"},
                {"ranks": [4, 10], "credits": 2500},
                {"ranks": [11, 50], "credits": 1000},
            ],
            "combat": [
                {"rank": 1, "credits": 10000, "exclusive_robot": "champion_bot",
                    "title": "Combat Champion"},
                {"rank": 2, "credits": 7500, "title": "Combat Master"},
                {"rank": 3, "credits": 5000, "title": "Combat Expert"},
                {"ranks": [4, 10], "credits": 2500},
                {"ranks": [11, 50], "credits": 1000},
            ],
            "achievement": [
                {"rank": 1, "credits": 10000, "legacy_points": 500,
                    "title": "Achievement Hunter"},
                {"rank": 2, "credits": 7500, "legacy_points": 300},
                {"rank": 3, "credits": 5000, "legacy_points": 200},
                {"ranks": [4, 10], "credits": 2500, "legacy_points": 100},
                {"ranks": [11, 50], "credits": 1000, "legacy_points": 50},
            ]
        }

    async def get_current_season(self) -> Optional[Dict[str, Any]]:
        """Get the currently active season."""
        now = datetime.utcnow()
        season = await self.db.seasons.find_one({
            "status": "active",
            "start_date": {"$lte": now},
            "end_date": {"$gte": now}
        })
        return season

    async def get_player_season_progress(
        self,
        player_id: str,
        season_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get player's progress in a season."""
        progress = await self.db.player_season_progress.find_one({
            "player_id": player_id,
            "season_id": season_id
        })

        if not progress:
            progress = await self._initialize_season_progress(player_id, season_id)

        return progress

    async def _initialize_season_progress(
        self,
        player_id: str,
        season_id: str
    ) -> Dict[str, Any]:
        """Initialize player's season progress."""
        season = await self.db.seasons.find_one({"season_id": season_id})

        progress = {
            "player_id": player_id,
            "season_id": season_id,
            "season_number": season["season_number"],
            "karma_rank": None,
            "wealth_rank": None,
            "combat_rank": None,
            "achievement_rank": None,
            "season_karma_earned": 0,
            "season_wealth_earned": 0,
            "season_combat_wins": 0,
            "season_achievements": 0,
            "season_quests_completed": 0,
            "exclusive_items_unlocked": [],
            "exclusive_quests_completed": [],
            "rewards_claimed": False,
            "end_of_season_rewards": [],
            "first_login": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "days_active": 1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.db.player_season_progress.insert_one(progress)

        # Increment season player count
        await self.db.seasons.update_one(
            {"season_id": season_id},
            {"$inc": {"total_players": 1, "active_players": 1}}
        )

        return progress

    async def update_season_stats(
        self,
        player_id: str,
        season_id: str,
        stat_type: str,
        value: int
    ):
        """Update player's season statistics."""
        field_map = {
            "karma": "season_karma_earned",
            "wealth": "season_wealth_earned",
            "combat_win": "season_combat_wins",
            "achievement": "season_achievements",
            "quest": "season_quests_completed"
        }

        field = field_map.get(stat_type)
        if not field:
            return

        await self.db.player_season_progress.update_one(
            {"player_id": player_id, "season_id": season_id},
            {
                "$inc": {field: value},
                "$set": {
                    "last_login": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )

    async def end_season(self, season_id: str):
        """End a season and distribute rewards."""
        season = await self.db.seasons.find_one({"season_id": season_id})

        # Update season status
        await self.db.seasons.update_one(
            {"season_id": season_id},
            {"$set": {"status": "ended", "updated_at": datetime.utcnow()}}
        )

        # Calculate final rankings
        await self._calculate_final_rankings(season_id)

        # Distribute rewards
        await self._distribute_season_rewards(season)

        # Prepare for next season
        await self._prepare_season_reset(season)

    async def _calculate_final_rankings(self, season_id: str):
        """Calculate final rankings for all leaderboards."""
        leaderboards = ["karma", "wealth", "combat", "achievement"]

        for lb_type in leaderboards:
            field_map = {
                "karma": "season_karma_earned",
                "wealth": "season_wealth_earned",
                "combat": "season_combat_wins",
                "achievement": "season_achievements"
            }

            field = field_map[lb_type]

            # Get sorted rankings
            players = await self.db.player_season_progress.find({
                "season_id": season_id
            }).sort(field, -1).to_list(length=None)

            # Update ranks
            for rank, player in enumerate(players, 1):
                await self.db.player_season_progress.update_one(
                    {"_id": player["_id"]},
                    {"$set": {f"{lb_type}_rank": rank}}
                )

    async def _distribute_season_rewards(
        self,
        season: Dict[str, Any]
    ):
        """Distribute rewards to top players."""
        # Get all player progress for this season
        players = await self.db.player_season_progress.find({
            "season_id": season["season_id"],
            "rewards_claimed": False
        }).to_list(length=None)

        for player in players:
            rewards = []

            # Calculate rewards based on rankings
            for lb_type, lb_rewards in season["leaderboard_rewards"].items():
                rank_field = f"{lb_type}_rank"
                player_rank = player.get(rank_field)

                if not player_rank:
                    continue

                # Find applicable reward
                for reward_tier in lb_rewards:
                    if "rank" in reward_tier and reward_tier["rank"] == player_rank:
                        rewards.append({"type": lb_type, **reward_tier})
                    elif "ranks" in reward_tier:
                        min_rank, max_rank = reward_tier["ranks"]
                        if min_rank <= player_rank <= max_rank:
                            rewards.append({"type": lb_type, **reward_tier})

            # Grant rewards
            for reward in rewards:
                await self._grant_season_reward(player["player_id"], reward)

            # Mark rewards as claimed
            await self.db.player_season_progress.update_one(
                {"_id": player["_id"]},
                {
                    "$set": {
                        "rewards_claimed": True,
                        "end_of_season_rewards": rewards
                    }
                }
            )

    async def _grant_season_reward(
        self,
        player_id: str,
        reward: Dict[str, Any]
    ):
        """Grant a season reward to a player."""
        # Grant credits
        if "credits" in reward:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"currencies.credits": reward["credits"]}}
            )

        # Grant legacy points
        if "legacy_points" in reward:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"legacy_points": reward["legacy_points"]}}
            )

        # Grant title
        if "title" in reward:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$push": {"titles": reward["title"]}}
            )

        # Grant exclusive items
        if "exclusive_item" in reward:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$push": {"cosmetics.owned_items": reward["exclusive_item"]}}
            )

    async def _prepare_season_reset(self, season: Dict[str, Any]):
        """Prepare for season reset."""
        # This would handle what carries over to next season
        # Implementation depends on reset configuration
        pass
