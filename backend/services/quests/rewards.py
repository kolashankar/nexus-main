"""Quest reward distribution service."""

from datetime import datetime
from typing import Dict
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

class RewardDistributor:
    """Handles quest reward distribution."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.players = db.players
        self.items = db.items
        self.achievements = db.achievements

    async def distribute_rewards(self, player_id: str, rewards: Dict) -> Dict:
        """Distribute quest rewards to player."""
        try:
            distributed = {
                "credits": 0,
                "xp": 0,
                "karma": 0,
                "items": [],
                "trait_boosts": {},
                "special_rewards": []
            }

            # Get player
            player = await self.players.find_one({"_id": player_id})
            if not player:
                raise ValueError("Player not found")

            updates = {}

            # Credits
            if "credits" in rewards:
                credits = rewards["credits"]
                updates["currencies.credits"] = player["currencies"]["credits"] + credits
                distributed["credits"] = credits

            # XP
            if "xp" in rewards:
                xp = rewards["xp"]
                current_xp = player.get("xp", 0)
                new_xp = current_xp + xp

                updates["xp"] = new_xp
                distributed["xp"] = xp

                # Check for level up
                new_level = await self._check_level_up(player, new_xp)
                if new_level > player.get("level", 1):
                    updates["level"] = new_level
                    distributed["level_up"] = new_level

            # Karma
            if "karma" in rewards:
                karma = rewards["karma"]
                updates["karma_points"] = player.get("karma_points", 0) + karma
                distributed["karma"] = karma

            # Items
            if "items" in rewards:
                for item_id in rewards["items"]:
                    await self._add_item(player_id, item_id)
                    distributed["items"].append(item_id)

            # Trait boosts
            if "trait_boosts" in rewards:
                for trait, boost in rewards["trait_boosts"].items():
                    current = player["traits"].get(trait, 0)
                    new_value = min(100, current + boost)
                    updates[f"traits.{trait}"] = new_value
                    distributed["trait_boosts"][trait] = boost

            # Special rewards
            if "special" in rewards:
                special = await self._handle_special_reward(player_id, rewards["special"])
                distributed["special_rewards"].append(special)

            # Apply updates
            if updates:
                await self.players.update_one(
                    {"_id": player_id},
                    {"$set": updates}
                )

            # Log reward distribution
            await self._log_reward_distribution(player_id, distributed)

            return distributed

        except Exception as e:
            logger.error(f"Error distributing rewards: {e}")
            raise

    async def _check_level_up(self, player: Dict, new_xp: int) -> int:
        """Check if player leveled up."""
        current_level = player.get("level", 1)

        # XP required for each level (exponential)
        def xp_for_level(level):
            return int(100 * (1.5 ** (level - 1)))

        # Calculate new level
        level = current_level
        while new_xp >= xp_for_level(level + 1) and level < 100:
            level += 1

        return level

    async def _add_item(self, player_id: str, item_id: str) -> None:
        """Add item to player inventory."""
        try:
            # Check if item exists in inventory
            player = await self.players.find_one({"_id": player_id})
            inventory = player.get("inventory", [])

            # Find existing item
            existing = None
            for item in inventory:
                if item["item_id"] == item_id:
                    existing = item
                    break

            if existing:
                # Increment quantity
                await self.players.update_one(
                    {
                        "_id": player_id,
                        "inventory.item_id": item_id
                    },
                    {
                        "$inc": {"inventory.$.quantity": 1}
                    }
                )
            else:
                # Add new item
                await self.players.update_one(
                    {"_id": player_id},
                    {
                        "$push": {
                            "inventory": {
                                "item_id": item_id,
                                "quantity": 1,
                                "acquired_at": datetime.utcnow()
                            }
                        }
                    }
                )

        except Exception as e:
            logger.error(f"Error adding item: {e}")
            raise

    async def _handle_special_reward(self, player_id: str, special: str) -> Dict:
        """Handle special rewards (superpowers, titles, etc.)."""
        try:
            if special.startswith("unlock_superpower:"):
                power_name = special.split(":")[1]

                # Add superpower to player
                await self.players.update_one(
                    {"_id": player_id},
                    {
                        "$push": {
                            "superpowers": {
                                "name": power_name,
                                "unlocked_at": datetime.utcnow(),
                                "usage_count": 0
                            }
                        }
                    }
                )

                return {
                    "type": "superpower",
                    "name": power_name
                }

            elif special.startswith("title:"):
                title = special.split(":")[1]

                # Add title
                await self.players.update_one(
                    {"_id": player_id},
                    {
                        "$addToSet": {"titles": title}
                    }
                )

                return {
                    "type": "title",
                    "name": title
                }

            return {"type": "unknown", "value": special}

        except Exception as e:
            logger.error(f"Error handling special reward: {e}")
            return {"type": "error", "message": str(e)}

    async def _log_reward_distribution(self, player_id: str, rewards: Dict) -> None:
        """Log reward distribution for tracking."""
        try:
            await self.db.reward_logs.insert_one({
                "player_id": player_id,
                "rewards": rewards,
                "distributed_at": datetime.utcnow(),
                "source": "quest"
            })
        except Exception as e:
            logger.error(f"Error logging rewards: {e}")
