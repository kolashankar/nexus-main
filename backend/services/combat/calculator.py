"""Combat calculator - damage and stat calculations."""

from typing import Dict, Any
import random
from bson import ObjectId

from backend.core.database import get_database
from backend.models.combat.battle import Combatant
from backend.models.combat.stats import CombatStats


class CombatCalculator:
    """Calculate combat stats, damage, and outcomes."""

    async def calculate_combat_stats(self, player: Dict[str, Any]) -> Dict[str, int]:
        """Calculate combat stats from player traits."""
        traits = player.get("traits", {})

        # HP = Endurance × 10
        endurance = traits.get("endurance", 50)
        hp = endurance * 10

        # Attack = (Strength + Dexterity) / 2
        strength = traits.get("physical_strength", 50)
        dexterity = traits.get("dexterity", 50)
        attack = int((strength + dexterity) / 2)

        # Defense = (Resilience + Perception) / 2
        resilience = traits.get("resilience", 50)
        perception = traits.get("perception", 50)
        defense = int((resilience + perception) / 2)

        # Evasion = Speed / 2
        speed = traits.get("speed", 50)
        evasion = int(speed / 2)

        # Crit chance (hidden luck stat simulation)
        crit_chance = 0.1 + (traits.get("focus", 50) / 1000)

        return {
            "hp": hp,
            "max_hp": hp,
            "attack": attack,
            "defense": defense,
            "evasion": evasion,
            "crit_chance": crit_chance
        }

    async def calculate_damage(
        self,
        attacker: Combatant,
        defender: Combatant
    ) -> int:
        """Calculate damage for an attack."""
        # Base damage
        base_damage = attacker.attack

        # Check for evasion
        evasion_roll = random.randint(1, 100)
        if evasion_roll <= defender.evasion:
            return 0  # Attack evaded

        # Apply defense reduction
        damage_reduction = defender.defense * 0.5
        damage = max(1, base_damage - damage_reduction)

        # Check for critical hit (15% base chance)
        crit_roll = random.random()
        if crit_roll < 0.15:
            damage *= 2

        # Add randomness (±10%)
        variance = random.uniform(0.9, 1.1)
        damage = int(damage * variance)

        return max(1, damage)

    async def get_player_combat_stats(self, player_id: str) -> Dict[str, Any]:
        """Get comprehensive combat statistics for a player."""
        db = await get_database()

        # Try to get existing stats
        stats_doc = await db.combat_stats.find_one({"player_id": player_id})

        if stats_doc:
            return stats_doc

        # Create initial stats
        player = await db.players.find_one({"_id": ObjectId(player_id)})
        if not player:
            raise ValueError("Player not found")

        combat_stats = await self.calculate_combat_stats(player)

        stats = CombatStats(
            player_id=player_id,
            **combat_stats
        )

        await db.combat_stats.insert_one(stats.model_dump())

        return stats.model_dump()

    async def update_combat_stats_after_battle(
        self,
        player_id: str,
        won: bool,
        damage_dealt: int,
        damage_taken: int,
        fled: bool = False
    ):
        """Update player's combat statistics after a battle."""
        db = await get_database()

        stats = await db.combat_stats.find_one({"player_id": player_id})
        if not stats:
            stats = (await self.get_player_combat_stats(player_id))

        # Update stats
        update_data = {
            "total_battles": stats.get("total_battles", 0) + 1,
            "total_damage_dealt": stats.get("total_damage_dealt", 0) + damage_dealt,
            "total_damage_taken": stats.get("total_damage_taken", 0) + damage_taken,
        }

        if won:
            update_data["wins"] = stats.get("wins", 0) + 1
            update_data["pvp_wins"] = stats.get("pvp_wins", 0) + 1
            update_data["current_win_streak"] = stats.get(
                "current_win_streak", 0) + 1

            if update_data["current_win_streak"] > stats.get("best_win_streak", 0):
                update_data["best_win_streak"] = update_data["current_win_streak"]
        elif fled:
            update_data["fled"] = stats.get("fled", 0) + 1
            update_data["current_win_streak"] = 0
        else:
            update_data["losses"] = stats.get("losses", 0) + 1
            update_data["pvp_losses"] = stats.get("pvp_losses", 0) + 1
            update_data["current_win_streak"] = 0

        if damage_dealt > stats.get("highest_damage", 0):
            update_data["highest_damage"] = damage_dealt

        await db.combat_stats.update_one(
            {"player_id": player_id},
            {"$set": update_data}
        )

    def calculate_xp_reward(self, won: bool, opponent_level: int, player_level: int) -> int:
        """Calculate XP reward from combat."""
        base_xp = 100
        level_diff_multiplier = 1 + ((opponent_level - player_level) * 0.1)
        level_diff_multiplier = max(0.5, min(2.0, level_diff_multiplier))

        if won:
            return int(base_xp * level_diff_multiplier)
        else:
            return int(base_xp * level_diff_multiplier * 0.3)  # Consolation XP

    def calculate_karma_change(self, combat_type: str, won: bool, fled: bool) -> int:
        """Calculate karma change from combat."""
        if fled:
            return -10  # Penalty for fleeing

        if combat_type == "duel":
            return 5 if won else -5  # Honorable combat
        elif combat_type == "ambush":
            return -10 if won else 0  # Dishonorable
        elif combat_type == "arena":
            return 10 if won else 0  # Sporting

        return 0
