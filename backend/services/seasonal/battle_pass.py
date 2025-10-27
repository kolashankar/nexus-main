"""Battle Pass Service."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from backend.core.database import db
import uuid


class BattlePassService:
    """Service for managing battle pass system."""

    def __init__(self):
        self.db = db

    async def create_battle_pass(
        self,
        season: int,
        name: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Create a new battle pass for a season."""
        pass_id = str(uuid.uuid4())

        # Generate tiers
        tiers = self._generate_tiers()

        battle_pass = {
            "pass_id": pass_id,
            "season": season,
            "name": name,
            "description": f"Battle Pass for Season {season}",
            "start_date": start_date,
            "end_date": end_date,
            "is_active": True,
            "total_tiers": 100,
            "free_tiers": 50,
            "premium_tiers": 100,
            "tiers": tiers,
            "premium_price": 1000,
            "total_players": 0,
            "premium_players": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.db.battle_passes.insert_one(battle_pass)
        return battle_pass

    def _generate_tiers(self) -> List[Dict[str, Any]]:
        """Generate 100 tiers with rewards."""
        tiers = []
        cumulative_xp = 0

        for tier in range(1, 101):
            # XP required increases with each tier
            tier_xp = 1000 + (tier * 100)
            cumulative_xp += tier_xp

            # Generate free rewards (every tier)
            free_rewards = self._generate_free_rewards(tier)

            # Generate premium rewards (more valuable)
            premium_rewards = self._generate_premium_rewards(tier)

            tiers.append({
                "tier": tier,
                "xp_required": cumulative_xp,
                "free_rewards": free_rewards,
                "premium_rewards": premium_rewards,
                "is_locked": True
            })

        return tiers

    def _generate_free_rewards(self, tier: int) -> List[Dict[str, Any]]:
        """Generate free rewards for a tier."""
        rewards = []

        # Every tier gets some credits
        rewards.append({
            "reward_type": "credits",
            "reward_id": "credits",
            "amount": 50 * tier,
            "name": f"{50 * tier} Credits",
            "description": "In-game currency",
            "rarity": "common"
        })

        # Every 5 tiers gets XP boost
        if tier % 5 == 0:
            rewards.append({
                "reward_type": "xp",
                "reward_id": "xp_boost",
                "amount": 500,
                "name": "500 XP",
                "description": "Experience points",
                "rarity": "common"
            })

        # Every 10 tiers gets a cosmetic
        if tier % 10 == 0:
            rewards.append({
                "reward_type": "cosmetic",
                "reward_id": f"cosmetic_tier_{tier}",
                "amount": 1,
                "name": f"Tier {tier} Outfit",
                "description": "Exclusive outfit",
                "rarity": "rare"
            })

        return rewards

    def _generate_premium_rewards(self, tier: int) -> List[Dict[str, Any]]:
        """Generate premium rewards for a tier."""
        rewards = []

        # Premium gets more credits
        rewards.append({
            "reward_type": "credits",
            "reward_id": "credits",
            "amount": 100 * tier,
            "name": f"{100 * tier} Credits",
            "description": "In-game currency",
            "rarity": "common",
            "is_premium_only": True
        })

        # Every tier gets karma tokens
        rewards.append({
            "reward_type": "karma_tokens",
            "reward_id": "karma_tokens",
            "amount": 10,
            "name": "10 Karma Tokens",
            "description": "Special currency",
            "rarity": "rare",
            "is_premium_only": True
        })

        # Every 10 tiers gets exclusive item
        if tier % 10 == 0:
            rewards.append({
                "reward_type": "exclusive_item",
                "reward_id": f"exclusive_tier_{tier}",
                "amount": 1,
                "name": f"Tier {tier} Exclusive",
                "description": "Premium exclusive item",
                "rarity": "epic",
                "is_premium_only": True
            })

        # Every 25 tiers gets emote
        if tier % 25 == 0:
            rewards.append({
                "reward_type": "emote",
                "reward_id": f"emote_tier_{tier}",
                "amount": 1,
                "name": f"Tier {tier} Emote",
                "description": "Exclusive emote",
                "rarity": "legendary",
                "is_premium_only": True
            })

        # Tier 50 and 100 get special rewards
        if tier == 50:
            rewards.append({
                "reward_type": "robot",
                "reward_id": "battle_pass_robot_1",
                "amount": 1,
                "name": "Battle Pass Robot",
                "description": "Exclusive robot",
                "rarity": "legendary",
                "is_premium_only": True
            })

        if tier == 100:
            rewards.append({
                "reward_type": "superpower_charge",
                "reward_id": "superpower_unlock",
                "amount": 1,
                "name": "Superpower Unlock",
                "description": "Unlock a random superpower",
                "rarity": "legendary",
                "is_premium_only": True
            })

        return rewards

    async def get_active_battle_pass(self) -> Optional[Dict[str, Any]]:
        """Get currently active battle pass."""
        now = datetime.utcnow()
        battle_pass = await self.db.battle_passes.find_one({
            "is_active": True,
            "start_date": {"$lte": now},
            "end_date": {"$gte": now}
        })
        return battle_pass

    async def get_player_progress(
        self,
        player_id: str,
        pass_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get player's battle pass progress."""
        progress = await self.db.player_battle_pass.find_one({
            "player_id": player_id,
            "pass_id": pass_id
        })

        if not progress:
            # Initialize progress
            progress = await self._initialize_player_progress(player_id, pass_id)

        return progress

    async def _initialize_player_progress(
        self,
        player_id: str,
        pass_id: str
    ) -> Dict[str, Any]:
        """Initialize player's battle pass progress."""
        battle_pass = await self.db.battle_passes.find_one({"pass_id": pass_id})

        progress = {
            "player_id": player_id,
            "pass_id": pass_id,
            "season": battle_pass["season"],
            "has_premium": False,
            "current_tier": 0,
            "current_xp": 0,
            "claimed_free_rewards": [],
            "claimed_premium_rewards": [],
            "total_xp_earned": 0,
            "last_xp_gain": None,
            "premium_purchased_at": None,
            "premium_price_paid": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.db.player_battle_pass.insert_one(progress)
        return progress

    async def add_xp(
        self,
        player_id: str,
        pass_id: str,
        xp_amount: int
    ) -> Dict[str, Any]:
        """Add XP to player's battle pass progress."""
        progress = await self.get_player_progress(player_id, pass_id)
        battle_pass = await self.db.battle_passes.find_one({"pass_id": pass_id})

        # Add XP
        new_xp = progress["current_xp"] + xp_amount
        new_total_xp = progress["total_xp_earned"] + xp_amount

        # Calculate new tier
        new_tier = progress["current_tier"]
        for tier_data in battle_pass["tiers"]:
            if new_xp >= tier_data["xp_required"]:
                new_tier = tier_data["tier"]
            else:
                break

        # Update progress
        await self.db.player_battle_pass.update_one(
            {"player_id": player_id, "pass_id": pass_id},
            {
                "$set": {
                    "current_xp": new_xp,
                    "current_tier": new_tier,
                    "total_xp_earned": new_total_xp,
                    "last_xp_gain": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            }
        )

        # Check if tier increased
        tiers_gained = new_tier - progress["current_tier"]

        return {
            "xp_added": xp_amount,
            "new_xp": new_xp,
            "new_tier": new_tier,
            "tiers_gained": tiers_gained,
            "rewards_available": tiers_gained > 0
        }

    async def claim_rewards(
        self,
        player_id: str,
        pass_id: str,
        tier: int
    ) -> Dict[str, Any]:
        """Claim rewards for a specific tier."""
        progress = await self.get_player_progress(player_id, pass_id)
        battle_pass = await self.db.battle_passes.find_one({"pass_id": pass_id})

        # Validate tier is unlocked
        if tier > progress["current_tier"]:
            raise ValueError("Tier not yet unlocked")

        # Get tier data
        tier_data = next(
            (t for t in battle_pass["tiers"] if t["tier"] == tier),
            None
        )

        if not tier_data:
            raise ValueError("Invalid tier")

        claimed_rewards = []

        # Claim free rewards
        if tier not in progress["claimed_free_rewards"]:
            for reward in tier_data["free_rewards"]:
                await self._grant_reward(player_id, reward)
                claimed_rewards.append(reward)

            await self.db.player_battle_pass.update_one(
                {"player_id": player_id, "pass_id": pass_id},
                {"$push": {"claimed_free_rewards": tier}}
            )

        # Claim premium rewards if has premium
        if progress["has_premium"] and tier not in progress["claimed_premium_rewards"]:
            for reward in tier_data["premium_rewards"]:
                await self._grant_reward(player_id, reward)
                claimed_rewards.append(reward)

            await self.db.player_battle_pass.update_one(
                {"player_id": player_id, "pass_id": pass_id},
                {"$push": {"claimed_premium_rewards": tier}}
            )

        return {
            "tier": tier,
            "rewards_claimed": claimed_rewards
        }

    async def _grant_reward(
        self,
        player_id: str,
        reward: Dict[str, Any]
    ):
        """Grant a reward to a player."""
        reward_type = reward["reward_type"]
        amount = reward["amount"]

        if reward_type == "credits":
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"currencies.credits": amount}}
            )
        elif reward_type == "xp":
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"xp": amount}}
            )
        elif reward_type == "karma_tokens":
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"currencies.karma_tokens": amount}}
            )
        elif reward_type in ["cosmetic", "emote", "exclusive_item"]:
            # Add to player's cosmetics/items
            await self.db.players.update_one(
                {"_id": player_id},
                {"$push": {"cosmetics.owned_items": reward["reward_id"]}}
            )
        # Add more reward type handlers as needed

    async def purchase_premium(
        self,
        player_id: str,
        pass_id: str
    ) -> Dict[str, Any]:
        """Purchase premium battle pass."""
        battle_pass = await self.db.battle_passes.find_one({"pass_id": pass_id})
        player = await self.db.players.find_one({"_id": player_id})

        # Check if player has enough credits
        if player["currencies"]["credits"] < battle_pass["premium_price"]:
            raise ValueError("Insufficient credits")

        # Deduct credits
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"currencies.credits": -battle_pass["premium_price"]}}
        )

        # Unlock premium
        await self.db.player_battle_pass.update_one(
            {"player_id": player_id, "pass_id": pass_id},
            {
                "$set": {
                    "has_premium": True,
                    "premium_purchased_at": datetime.utcnow(),
                    "premium_price_paid": battle_pass["premium_price"]
                }
            }
        )

        # Update battle pass stats
        await self.db.battle_passes.update_one(
            {"pass_id": pass_id},
            {"$inc": {"premium_players": 1}}
        )

        return {
            "success": True,
            "message": "Premium battle pass purchased",
            "price_paid": battle_pass["premium_price"]
        }
