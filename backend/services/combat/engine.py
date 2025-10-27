"""Combat engine - main battle logic."""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import random
from bson import ObjectId

from backend.core.database import get_database
from backend.models.combat.battle import Battle, CombatChallenge, Combatant, CombatLogEntry
from backend.services.combat.calculator import CombatCalculator
from backend.services.player.profile import PlayerProfileService


class CombatEngine:
    """Main combat engine for turn-based battles."""

    def __init__(self):
        self.calculator = CombatCalculator()
        self.player_service = PlayerProfileService()

    async def create_challenge(
        self,
        challenger_id: str,
        target_id: str,
        combat_type: str = "duel"
    ) -> Dict[str, Any]:
        """Create a combat challenge."""
        db = await get_database()

        # Get player data
        challenger = await db.players.find_one({"_id": ObjectId(challenger_id)})
        target = await db.players.find_one({"_id": ObjectId(target_id)})

        if not challenger or not target:
            raise ValueError("Player not found")

        if challenger_id == target_id:
            raise ValueError("Cannot challenge yourself")

        # Check if already in combat
        active_battle = await self.get_active_battle(challenger_id)
        if active_battle:
            raise ValueError("Already in active combat")

        # Create challenge
        challenge = CombatChallenge(
            challenger_id=challenger_id,
            challenger_username=challenger.get("username"),
            target_id=target_id,
            target_username=target.get("username"),
            combat_type=combat_type,
            expires_at=datetime.utcnow() + timedelta(minutes=5)
        )

        result = await db.combat_challenges.insert_one(challenge.model_dump())
        challenge_dict = challenge.model_dump()
        challenge_dict["_id"] = result.inserted_id

        return challenge_dict

    async def accept_challenge(
        self,
        challenge_id: str,
        accepter_id: str
    ) -> Dict[str, Any]:
        """Accept a combat challenge and start battle."""
        db = await get_database()

        # Get challenge
        challenge = await db.combat_challenges.find_one({"_id": ObjectId(challenge_id)})
        if not challenge:
            raise ValueError("Challenge not found")

        if challenge["target_id"] != accepter_id:
            raise ValueError("Not your challenge to accept")

        if challenge["status"] != "pending":
            raise ValueError("Challenge no longer available")

        # Create battle
        battle = await self._create_battle(
            player1_id=challenge["challenger_id"],
            player2_id=challenge["target_id"],
            battle_type=challenge["combat_type"]
        )

        # Update challenge
        await db.combat_challenges.update_one(
            {"_id": ObjectId(challenge_id)},
            {"$set": {
                "status": "accepted",
                "battle_id": battle["id"]
            }}
        )

        return battle

    async def decline_challenge(self, challenge_id: str, decliner_id: str):
        """Decline a combat challenge."""
        db = await get_database()

        challenge = await db.combat_challenges.find_one({"_id": ObjectId(challenge_id)})
        if not challenge:
            raise ValueError("Challenge not found")

        if challenge["target_id"] != decliner_id:
            raise ValueError("Not your challenge to decline")

        await db.combat_challenges.update_one(
            {"_id": ObjectId(challenge_id)},
            {"$set": {"status": "declined"}}
        )

    async def _create_battle(
        self,
        player1_id: str,
        player2_id: str,
        battle_type: str = "duel"
    ) -> Dict[str, Any]:
        """Create a new battle instance."""
        db = await get_database()

        # Get players
        player1 = await db.players.find_one({"_id": ObjectId(player1_id)})
        player2 = await db.players.find_one({"_id": ObjectId(player2_id)})

        # Calculate combat stats
        stats1 = await self.calculator.calculate_combat_stats(player1)
        stats2 = await self.calculator.calculate_combat_stats(player2)

        # Create combatants
        combatant1 = Combatant(
            player_id=player1_id,
            username=player1.get("username"),
            hp=stats1["hp"],
            max_hp=stats1["max_hp"],
            attack=stats1["attack"],
            defense=stats1["defense"],
            evasion=stats1["evasion"]
        )

        combatant2 = Combatant(
            player_id=player2_id,
            username=player2.get("username"),
            hp=stats2["hp"],
            max_hp=stats2["max_hp"],
            attack=stats2["attack"],
            defense=stats2["defense"],
            evasion=stats2["evasion"]
        )

        # Determine turn order (based on speed/perception)
        turn_order = self._determine_turn_order(
            [combatant1, combatant2], [player1, player2])

        # Create battle
        battle = Battle(
            battle_type=battle_type,
            combatants=turn_order
        )

        # Store in database
        await db.battles.insert_one(battle.model_dump())

        return battle.model_dump()

    def _determine_turn_order(
        self,
        combatants: List[Combatant],
        players: List[Dict[str, Any]]
    ) -> List[Combatant]:
        """Determine initiative order."""
        # Calculate initiative (Speed + Perception + random)
        initiatives = []
        for combatant, player in zip(combatants, players):
            speed = player.get("traits", {}).get("speed", 50)
            perception = player.get("traits", {}).get("perception", 50)
            initiative = speed + perception + random.randint(1, 20)
            initiatives.append((initiative, combatant))

        # Sort by initiative (highest first)
        initiatives.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in initiatives]

    async def execute_action(
        self,
        battle_id: str,
        player_id: str,
        action_type: str,
        target: Optional[str] = None,
        ability_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute a combat action."""
        db = await get_database()

        # Get battle
        battle_doc = await db.battles.find_one({"id": battle_id})
        if not battle_doc:
            raise ValueError("Battle not found")

        battle = Battle(**battle_doc)

        # Verify it's player's turn
        current_combatant = battle.combatants[battle.current_actor_index]
        if current_combatant.player_id != player_id:
            raise ValueError("Not your turn")

        # Process action
        if action_type == "attack":
            result = await self._process_attack(battle, target)
        elif action_type == "defend":
            result = await self._process_defend(battle)
        elif action_type == "use_power":
            result = await self._process_power(battle, ability_id, target)
        else:
            raise ValueError(f"Unknown action type: {action_type}")

        # Add to combat log
        log_entry = CombatLogEntry(
            turn=battle.current_turn,
            actor=player_id,
            action=action_type,
            target=target,
            result=result
        )
        battle.combat_log.append(log_entry)

        # Check for battle end
        if await self._check_battle_end(battle):
            battle.status = "completed"
            battle.ended_at = datetime.utcnow()
        else:
            # Next turn
            battle.current_actor_index = (
                battle.current_actor_index + 1) % len(battle.combatants)
            if battle.current_actor_index == 0:
                battle.current_turn += 1

        # Update battle
        await db.battles.update_one(
            {"id": battle_id},
            {"$set": battle.model_dump()}
        )

        return result

    async def _process_attack(
        self,
        battle: Battle,
        target_id: Optional[str]
    ) -> Dict[str, Any]:
        """Process an attack action."""
        attacker = battle.combatants[battle.current_actor_index]

        # Find target (opponent)
        target = next(
            (c for c in battle.combatants if c.player_id == target_id), None)
        if not target:
            target = next(
                (c for c in battle.combatants if c.player_id != attacker.player_id), None)

        # Calculate damage
        damage = await self.calculator.calculate_damage(attacker, target)

        # Apply damage
        target.hp = max(0, target.hp - damage)

        return {
            "success": True,
            "damage": damage,
            "message": f"{attacker.username} deals {damage} damage to {target.username}!",
            "target_hp": target.hp
        }

    async def _process_defend(self, battle: Battle) -> Dict[str, Any]:
        """Process a defend action."""
        defender = battle.combatants[battle.current_actor_index]

        # Add temporary defense buff
        defender.status_effects.append({
            "type": "defense_boost",
            "value": 20,
            "duration": 1
        })

        return {
            "success": True,
            "message": f"{defender.username} takes a defensive stance!"
        }

    async def _process_power(
        self,
        battle: Battle,
        ability_id: Optional[str],
        target_id: Optional[str]
    ) -> Dict[str, Any]:
        """Process superpower usage."""
        # Placeholder for superpower system
        return {
            "success": True,
            "message": "Superpower activated!"
        }

    async def _check_battle_end(self, battle: Battle) -> bool:
        """Check if battle has ended."""
        for combatant in battle.combatants:
            if combatant.hp <= 0:
                # Find winner
                winner = next((c for c in battle.combatants if c.hp > 0), None)
                if winner:
                    battle.winner = winner.player_id
                    loser = next(
                        (c for c in battle.combatants if c.hp <= 0), None)
                    if loser:
                        battle.loser = loser.player_id
                return True
        return False

    async def get_active_battle(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get active battle for a player."""
        db = await get_database()
        battle = await db.battles.find_one({
            "status": "active",
            "combatants.player_id": player_id
        })
        return battle

    async def get_combat_state(self, battle_id: str) -> Dict[str, Any]:
        """Get current combat state."""
        db = await get_database()
        battle = await db.battles.find_one({"id": battle_id})
        if not battle:
            raise ValueError("Battle not found")
        return battle

    async def attempt_flee(self, battle_id: str, player_id: str) -> Dict[str, Any]:
        """Attempt to flee from combat."""
        db = await get_database()
        battle_doc = await db.battles.find_one({"id": battle_id})
        if not battle_doc:
            raise ValueError("Battle not found")

        battle = Battle(**battle_doc)

        # Find player
        combatant = next(
            (c for c in battle.combatants if c.player_id == player_id), None)
        if not combatant:
            raise ValueError("Not in this battle")

        # Calculate flee chance (based on evasion/speed)
        flee_chance = min(0.8, combatant.evasion / 100)

        if random.random() < flee_chance:
            battle.status = "fled"
            battle.loser = player_id
            battle.ended_at = datetime.utcnow()

            await db.battles.update_one(
                {"id": battle_id},
                {"$set": battle.model_dump()}
            )

            return {"success": True, "message": "Successfully fled from battle!"}
        else:
            return {"success": False, "message": "Failed to flee! You remain in combat."}

    async def get_combat_history(
        self,
        player_id: str,
        limit: int = 20,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get combat history for a player."""
        db = await get_database()
        history = await db.battles.find(
            {
                "combatants.player_id": player_id,
                "status": {"$in": ["completed", "fled"]}
            }
        ).sort("started_at", -1).skip(skip).limit(limit).to_list(length=limit)

        return history
