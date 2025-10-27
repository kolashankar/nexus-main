"""Turn manager for combat system."""

from typing import Dict
from datetime import datetime, timedelta
import asyncio

from backend.models.combat.battle import Battle, Combatant


class TurnManager:
    """Manage combat turns and timing."""

    def __init__(self, turn_time_limit: int = 60):
        """Initialize turn manager.
        
        Args:
            turn_time_limit: Time limit per turn in seconds (default 60)
        """
        self.turn_time_limit = turn_time_limit
        self.turn_timers: Dict[str, datetime] = {}

    def start_turn(self, battle_id: str):
        """Start a new turn timer."""
        self.turn_timers[battle_id] = datetime.utcnow(
        ) + timedelta(seconds=self.turn_time_limit)

    def get_time_remaining(self, battle_id: str) -> int:
        """Get remaining time for current turn in seconds."""
        if battle_id not in self.turn_timers:
            return self.turn_time_limit

        deadline = self.turn_timers[battle_id]
        remaining = (deadline - datetime.utcnow()).total_seconds()
        return max(0, int(remaining))

    def is_turn_expired(self, battle_id: str) -> bool:
        """Check if turn time has expired."""
        return self.get_time_remaining(battle_id) == 0

    def reset_turn_timer(self, battle_id: str):
        """Reset the turn timer."""
        if battle_id in self.turn_timers:
            del self.turn_timers[battle_id]

    def get_next_actor(self, battle: Battle) -> Combatant:
        """Get the next actor in turn order."""
        return battle.combatants[battle.current_actor_index]

    def advance_turn(self, battle: Battle) -> bool:
        """Advance to next turn.
        
        Returns:
            True if turn advanced, False if battle is over
        """
        # Move to next combatant
        battle.current_actor_index = (
            battle.current_actor_index + 1) % len(battle.combatants)

        # If back to first combatant, increment turn counter
        if battle.current_actor_index == 0:
            battle.current_turn += 1

        # Reset action points for current actor
        current_actor = battle.combatants[battle.current_actor_index]
        current_actor.action_points = current_actor.max_action_points

        # Process status effects
        self._process_status_effects(battle)

        return True

    def _process_status_effects(self, battle: Battle):
        """Process status effects at turn start."""
        for combatant in battle.combatants:
            # Decrease duration of effects
            effects_to_remove = []

            for i, effect in enumerate(combatant.status_effects):
                effect["duration"] = effect.get("duration", 0) - 1

                if effect["duration"] <= 0:
                    effects_to_remove.append(i)
                else:
                    # Apply ongoing effects
                    if effect["type"] == "poison":
                        combatant.hp -= effect.get("value", 5)
                    elif effect["type"] == "regen":
                        combatant.hp = min(
                            combatant.max_hp,
                            combatant.hp + effect.get("value", 5)
                        )

            # Remove expired effects
            for i in reversed(effects_to_remove):
                combatant.status_effects.pop(i)

    def check_action_points(self, battle: Battle, action_cost: int) -> bool:
        """Check if current actor has enough action points."""
        current_actor = battle.combatants[battle.current_actor_index]
        return current_actor.action_points >= action_cost

    def consume_action_points(self, battle: Battle, action_cost: int):
        """Consume action points for an action."""
        current_actor = battle.combatants[battle.current_actor_index]
        current_actor.action_points -= action_cost

    def get_action_cost(self, action_type: str) -> int:
        """Get action point cost for an action."""
        costs = {
            "attack": 1,
            "heavy_attack": 2,
            "defend": 1,
            "use_power": 2,
            "use_item": 1,
            "flee": 3
        }
        return costs.get(action_type, 1)

    def can_perform_action(self, battle: Battle, action_type: str) -> bool:
        """Check if current actor can perform an action."""
        action_cost = self.get_action_cost(action_type)
        return self.check_action_points(battle, action_cost)

    async def wait_for_action(self, battle_id: str, timeout: int = None) -> bool:
        """Wait for action with timeout.
        
        Returns:
            True if action received, False if timeout
        """
        timeout = timeout or self.turn_time_limit
        try:
            await asyncio.wait_for(asyncio.sleep(timeout), timeout=timeout)
            return False  # Timeout
        except asyncio.TimeoutError:
            return False
