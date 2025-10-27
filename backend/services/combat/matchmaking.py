from typing import Dict, List, Optional
import random
from datetime import datetime


class MatchmakingService:
    """
    Handles arena matchmaking logic
    """

    def __init__(self):
        self.queue: List[Dict] = []

    def add_to_queue(self, player: Dict, ranked: bool = False):
        """
        Add player to matchmaking queue
        """
        entry = {
            "player_id": player["player_id"],
            "username": player.get("username"),
            "combat_rating": player.get("combat_stats", {}).get("combat_rating", 1500),
            "ranked": ranked,
            "joined_at": datetime.utcnow(),
            "player_data": player
        }
        self.queue.append(entry)

    def remove_from_queue(self, player_id: str) -> bool:
        """
        Remove player from queue
        
        Returns:
            True if removed, False if not in queue
        """
        for i, entry in enumerate(self.queue):
            if entry["player_id"] == player_id:
                self.queue.pop(i)
                return True
        return False

    def find_match(self, player_id: str) -> Optional[Dict]:
        """
        Find a suitable opponent for a player
        
        Args:
            player_id: Player looking for match
        
        Returns:
            Opponent entry if found, None otherwise
        """
        # Find player in queue
        player_entry = None
        for entry in self.queue:
            if entry["player_id"] == player_id:
                player_entry = entry
                break

        if not player_entry:
            return None

        # Find suitable opponent
        ranked = player_entry["ranked"]
        player_rating = player_entry["combat_rating"]

        if ranked:
            # Ranked: Match within rating range
            rating_range = 200
            candidates = [
                e for e in self.queue
                if e["player_id"] != player_id
                and e["ranked"]
                and abs(e["combat_rating"] - player_rating) <= rating_range
            ]
        else:
            # Casual: Any opponent
            candidates = [
                e for e in self.queue
                if e["player_id"] != player_id
                and not e["ranked"]
            ]

        if not candidates:
            return None

        # Pick closest rating (for ranked) or random (for casual)
        if ranked:
            candidates.sort(key=lambda e: abs(
                e["combat_rating"] - player_rating))
            opponent = candidates[0]
        else:
            opponent = random.choice(candidates)

        # Remove both players from queue
        self.remove_from_queue(player_id)
        self.remove_from_queue(opponent["player_id"])

        return opponent

    def get_queue_position(self, player_id: str) -> int:
        """
        Get player's position in queue
        
        Returns:
            Position (1-indexed), or 0 if not in queue
        """
        for i, entry in enumerate(sorted(self.queue, key=lambda e: e["joined_at"]), 1):
            if entry["player_id"] == player_id:
                return i
        return 0

    def get_queue_size(self, ranked: Optional[bool] = None) -> int:
        """
        Get total players in queue
        
        Args:
            ranked: If specified, count only ranked/casual queue
        
        Returns:
            Number of players in queue
        """
        if ranked is None:
            return len(self.queue)
        return sum(1 for e in self.queue if e["ranked"] == ranked)
