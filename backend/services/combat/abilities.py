"""Combat abilities system - trait-based special moves."""

from typing import Dict, Any, List
from bson import ObjectId

from backend.core.database import get_database
from backend.models.combat.battle import Combatant


class CombatAbilitiesService:
    """Manage combat abilities based on player traits."""

    # Trait-based abilities (unlocked at 80% trait level)
    TRAIT_ABILITIES = {
        "hacking": {
            "name": "EMP Blast",
            "description": "Disable opponent's robots and tech",
            "damage": 0,
            "effect": "disable_robots",
            "cost": 3,
            "cooldown": 3
        },
        "kindness": {
            "name": "Mercy",
            "description": "Spare enemy, gain karma",
            "damage": 0,
            "effect": "end_combat_peaceful",
            "cost": 2,
            "cooldown": 0
        },
        "wrath": {
            "name": "Berserker Rage",
            "description": "2x damage, lose defense",
            "damage_multiplier": 2.0,
            "defense_multiplier": 0.5,
            "cost": 2,
            "cooldown": 5
        },
        "strategy": {
            "name": "Tactical Advantage",
            "description": "Gain extra action points",
            "bonus_ap": 2,
            "cost": 2,
            "cooldown": 4
        },
        "meditation": {
            "name": "Inner Peace",
            "description": "Restore HP",
            "healing": 30,
            "cost": 2,
            "cooldown": 3
        },
        "stealth": {
            "name": "Shadow Strike",
            "description": "Guaranteed hit with bonus damage",
            "damage_bonus": 50,
            "guaranteed_hit": True,
            "cost": 3,
            "cooldown": 4
        },
        "physical_strength": {
            "name": "Power Slam",
            "description": "Heavy damage attack",
            "damage_multiplier": 1.5,
            "stun_chance": 0.3,
            "cost": 2,
            "cooldown": 2
        },
        "resilience": {
            "name": "Iron Will",
            "description": "Reduce damage taken next turn",
            "damage_reduction": 0.5,
            "duration": 2,
            "cost": 2,
            "cooldown": 3
        },
        "speed": {
            "name": "Blitz Attack",
            "description": "Multiple quick strikes",
            "hits": 3,
            "damage_per_hit": 0.4,
            "cost": 3,
            "cooldown": 4
        },
        "courage": {
            "name": "Heroic Stand",
            "description": "Cannot be reduced below 1 HP this turn",
            "effect": "last_stand",
            "cost": 3,
            "cooldown": 5
        },
        "intelligence": {
            "name": "Tactical Analysis",
            "description": "Reveal opponent's next move",
            "effect": "reveal_action",
            "cost": 1,
            "cooldown": 3
        },
        "charisma": {
            "name": "Intimidate",
            "description": "Reduce opponent's attack",
            "attack_reduction": 20,
            "duration": 2,
            "cost": 2,
            "cooldown": 3
        }
    }

    async def get_available_abilities(self, player_id: str) -> List[Dict[str, Any]]:
        """Get all available combat abilities for a player."""
        db = await get_database()
        player = await db.players.find_one({"_id": ObjectId(player_id)})

        if not player:
            raise ValueError("Player not found")

        traits = player.get("traits", {})
        available_abilities = []

        # Check each trait for ability unlock (80% threshold)
        for trait_name, ability_data in self.TRAIT_ABILITIES.items():
            trait_value = traits.get(trait_name, 0)
            if trait_value >= 80:
                ability = {
                    "id": trait_name,
                    "trait": trait_name,
                    "trait_value": trait_value,
                    "unlocked": True,
                    **ability_data
                }
                available_abilities.append(ability)

        return available_abilities

    async def use_ability(
        self,
        ability_id: str,
        attacker: Combatant,
        defender: Combatant,
        player_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a combat ability."""
        # Check if ability exists
        if ability_id not in self.TRAIT_ABILITIES:
            raise ValueError(f"Unknown ability: {ability_id}")

        ability = self.TRAIT_ABILITIES[ability_id]

        # Check if player has high enough trait
        trait_value = player_data.get("traits", {}).get(ability_id, 0)
        if trait_value < 80:
            raise ValueError(
                f"Trait {ability_id} not high enough to use this ability")

        # Check action points
        if attacker.action_points < ability.get("cost", 2):
            raise ValueError("Not enough action points")

        # Execute ability effect
        result = await self._execute_ability_effect(ability, attacker, defender)

        return result

    async def _execute_ability_effect(
        self,
        ability: Dict[str, Any],
        attacker: Combatant,
        defender: Combatant
    ) -> Dict[str, Any]:
        """Execute the specific effect of an ability."""
        result = {
            "success": True,
            "ability_name": ability["name"],
            "effects": []
        }

        # Damage abilities
        if "damage_multiplier" in ability:
            base_damage = attacker.attack
            damage = int(base_damage * ability["damage_multiplier"])
            defender.hp = max(0, defender.hp - damage)
            result["damage"] = damage
            result["effects"].append(f"Dealt {damage} damage")

        # Healing abilities
        if "healing" in ability:
            healing = ability["healing"]
            old_hp = attacker.hp
            attacker.hp = min(attacker.max_hp, attacker.hp + healing)
            actual_healing = attacker.hp - old_hp
            result["healing"] = actual_healing
            result["effects"].append(f"Healed {actual_healing} HP")

        # Status effect abilities
        if "effect" in ability:
            effect_type = ability["effect"]

            if effect_type == "disable_robots":
                defender.status_effects.append({
                    "type": "disabled",
                    "duration": 2
                })
                result["effects"].append("Robots disabled")

            elif effect_type == "last_stand":
                attacker.status_effects.append({
                    "type": "last_stand",
                    "duration": 1
                })
                result["effects"].append("Protected from death")

        # Damage reduction
        if "damage_reduction" in ability:
            attacker.status_effects.append({
                "type": "damage_reduction",
                "value": ability["damage_reduction"],
                "duration": ability.get("duration", 1)
            })
            result["effects"].append("Damage reduction active")

        # Attack reduction
        if "attack_reduction" in ability:
            defender.status_effects.append({
                "type": "attack_debuff",
                "value": ability["attack_reduction"],
                "duration": ability.get("duration", 1)
            })
            result["effects"].append(
                f"Opponent attack reduced by {ability['attack_reduction']}")

        # Bonus action points
        if "bonus_ap" in ability:
            attacker.action_points += ability["bonus_ap"]
            result["effects"].append(
                f"Gained {ability['bonus_ap']} action points")

        # Multiple hits
        if "hits" in ability:
            total_damage = 0
            for _ in range(ability["hits"]):
                damage = int(attacker.attack * ability["damage_per_hit"])
                total_damage += damage
            defender.hp = max(0, defender.hp - total_damage)
            result["damage"] = total_damage
            result["effects"].append(
                f"{ability['hits']} hits for {total_damage} total damage")

        # Stun effect
        if "stun_chance" in ability:
            import random
            if random.random() < ability["stun_chance"]:
                defender.status_effects.append({
                    "type": "stunned",
                    "duration": 1
                })
                result["effects"].append("Target stunned!")

        return result

    async def check_ability_cooldown(
        self,
        player_id: str,
        ability_id: str
    ) -> bool:
        """Check if ability is on cooldown."""
        db = await get_database()

        cooldowns = await db.ability_cooldowns.find_one({"player_id": player_id})

        if not cooldowns:
            return True  # Not on cooldown

        ability_cooldowns = cooldowns.get("abilities", {})

        if ability_id not in ability_cooldowns:
            return True

        # Check if cooldown expired
        from datetime import datetime
        cooldown_until = ability_cooldowns[ability_id]

        if isinstance(cooldown_until, str):
            cooldown_until = datetime.fromisoformat(cooldown_until)

        return datetime.utcnow() > cooldown_until

    async def set_ability_cooldown(
        self,
        player_id: str,
        ability_id: str
    ):
        """Set cooldown for an ability."""
        db = await get_database()

        if ability_id not in self.TRAIT_ABILITIES:
            return

        ability = self.TRAIT_ABILITIES[ability_id]
        cooldown_turns = ability.get("cooldown", 0)

        if cooldown_turns == 0:
            return

        from datetime import datetime, timedelta
        cooldown_until = datetime.utcnow() + timedelta(minutes=cooldown_turns)

        await db.ability_cooldowns.update_one(
            {"player_id": player_id},
            {
                "$set": {
                    f"abilities.{ability_id}": cooldown_until
                }
            },
            upsert=True
        )
