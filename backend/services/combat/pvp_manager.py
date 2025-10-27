from typing import Dict
from .engine import CombatEngine


class PvPManager:
    """
    Manages PvP-specific logic and matchmaking
    """

    def __init__(self):
        self.combat_engine = CombatEngine()

    def calculate_matchmaking_score(self, player1: Dict, player2: Dict) -> float:
        """
        Calculate how good of a match two players are
        Lower score = better match
        
        Args:
            player1: First player
            player2: Second player
        
        Returns:
            Match score (0-100)
        """
        # Get combat ratings
        rating1 = player1.get("combat_stats", {}).get("combat_rating", 1500)
        rating2 = player2.get("combat_stats", {}).get("combat_rating", 1500)

        # Calculate rating difference
        rating_diff = abs(rating1 - rating2)

        # Normalize to 0-100 scale (200 rating diff = 100% mismatch)
        score = min(100, (rating_diff / 200) * 100)

        return score

    def is_valid_duel(self, attacker: Dict, defender: Dict) -> tuple[bool, str]:
        """
        Check if a duel challenge is valid
        
        Returns:
            Tuple of (is_valid, reason_if_invalid)
        """
        # Check if defender is online
        if not defender.get("online", False):
            return False, "Defender is offline"

        # Check if players are in same location (optional)
        # attacker_loc = attacker.get("location", {})
        # defender_loc = defender.get("location", {})

        # Check if defender has duels disabled (optional)
        # if defender.get("settings", {}).get("disable_duels", False):
        #     return False, "Defender has disabled duel challenges"

        return True, ""

    def calculate_ambush_success_chance(self, attacker: Dict, defender: Dict) -> int:
        """
        Calculate chance of successful ambush (0-100%)
        
        Args:
            attacker: Attacking player
            defender: Target player
        
        Returns:
            Success percentage (0-100)
        """
        attacker_stealth = attacker.get("traits", {}).get("stealth", 50)
        defender_perception = defender.get("traits", {}).get("perception", 50)

        # Base chance is 50%
        base_chance = 50

        # Stealth increases chance, perception decreases it
        modifier = (attacker_stealth - defender_perception) // 2

        success_chance = base_chance + modifier

        # Clamp between 10% and 90%
        return max(10, min(90, success_chance))
