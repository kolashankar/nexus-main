"""Tournament Manager Service."""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from backend.core.database import db
from backend.models.tournaments.tournament import (
    TournamentType
)
import uuid
import math


class TournamentManager:
    """Service for managing tournaments."""

    def __init__(self):
        self.db = db

    async def create_tournament(
        self,
        name: str,
        tournament_type: TournamentType,
        start_time: datetime,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new tournament."""
        tournament_id = str(uuid.uuid4())

        # Calculate registration times
        registration_start = kwargs.get(
            'registration_start', datetime.utcnow())
        registration_end = kwargs.get(
            'registration_end', start_time - timedelta(hours=1))

        tournament = {
            "tournament_id": tournament_id,
            "name": name,
            "description": kwargs.get('description', ''),
            "tournament_type": tournament_type,
            "status": "registration",
            "registration_start": registration_start,
            "registration_end": registration_end,
            "start_time": start_time,
            "end_time": None,
            "bracket_type": kwargs.get('bracket_type', 'single_elimination'),
            "max_participants": kwargs.get('max_participants', 64),
            "min_participants": kwargs.get('min_participants', 8),
            "min_level": kwargs.get('min_level'),
            "min_karma": kwargs.get('min_karma'),
            "entry_fee": kwargs.get('entry_fee', 0),
            "registered_players": [],
            "total_registered": 0,
            "matches": [],
            "current_round": 0,
            "total_rounds": 0,
            "prize_pool": kwargs.get('prize_pool', 0),
            "rewards": self._generate_default_rewards(kwargs.get('prize_pool', 0)),
            "season_id": kwargs.get('season_id'),
            "created_by": kwargs.get('created_by', 'system'),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        await self.db.tournaments.insert_one(tournament)
        return tournament

    def _generate_default_rewards(self, prize_pool: int) -> Dict[int, Dict[str, Any]]:
        """Generate default reward distribution."""
        if prize_pool == 0:
            return {}

        return {
            1: {  # 1st place - 50%
                "credits": int(prize_pool * 0.5),
                "title": "Tournament Champion",
                "exclusive_item": "champion_trophy"
            },
            2: {  # 2nd place - 30%
                "credits": int(prize_pool * 0.3),
                "title": "Tournament Runner-up"
            },
            3: {  # 3rd place - 20%
                "credits": int(prize_pool * 0.2),
                "title": "Tournament Semi-finalist"
            }
        }

    async def register_player(
        self,
        tournament_id: str,
        player_id: str
    ) -> Dict[str, Any]:
        """Register a player for a tournament."""
        tournament = await self.db.tournaments.find_one({"tournament_id": tournament_id})

        if not tournament:
            raise ValueError("Tournament not found")

        # Check if registration is open
        now = datetime.utcnow()
        if now < tournament["registration_start"] or now > tournament["registration_end"]:
            raise ValueError("Registration is not open")

        # Check if tournament is full
        if tournament["total_registered"] >= tournament["max_participants"]:
            raise ValueError("Tournament is full")

        # Check if already registered
        if player_id in tournament["registered_players"]:
            raise ValueError("Already registered")

        # Check player requirements
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            raise ValueError("Player not found")

        if tournament["min_level"] and player.get("level", 0) < tournament["min_level"]:
            raise ValueError(
                f"Minimum level {tournament['min_level']} required")

        if tournament["min_karma"] and player.get("karma_points", 0) < tournament["min_karma"]:
            raise ValueError(
                f"Minimum karma {tournament['min_karma']} required")

        # Check entry fee
        if tournament["entry_fee"] > 0:
            if player["currencies"]["credits"] < tournament["entry_fee"]:
                raise ValueError("Insufficient credits for entry fee")

            # Deduct entry fee
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"currencies.credits": -tournament["entry_fee"]}}
            )

            # Add to prize pool
            await self.db.tournaments.update_one(
                {"tournament_id": tournament_id},
                {"$inc": {"prize_pool": tournament["entry_fee"]}}
            )

        # Register player
        await self.db.tournaments.update_one(
            {"tournament_id": tournament_id},
            {
                "$push": {"registered_players": player_id},
                "$inc": {"total_registered": 1},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

        # Create participant record
        participant = {
            "tournament_id": tournament_id,
            "player_id": player_id,
            "registration_time": datetime.utcnow(),
            "checked_in": False,
            "current_match_id": None,
            "wins": 0,
            "losses": 0,
            "placement": None,
            "eliminated": False
        }
        await self.db.tournament_participants.insert_one(participant)

        return {"success": True, "message": "Registered successfully"}

    async def start_tournament(self, tournament_id: str):
        """Start a tournament and generate brackets."""
        tournament = await self.db.tournaments.find_one({"tournament_id": tournament_id})

        if not tournament:
            raise ValueError("Tournament not found")

        if tournament["total_registered"] < tournament["min_participants"]:
            raise ValueError(
                f"Minimum {tournament['min_participants']} participants required")

        # Generate bracket
        matches = await self._generate_bracket(
            tournament_id=tournament_id,
            players=tournament["registered_players"],
            bracket_type=tournament["bracket_type"]
        )

        # Calculate total rounds
        total_rounds = math.ceil(
            math.log2(len(tournament["registered_players"])))

        # Update tournament
        await self.db.tournaments.update_one(
            {"tournament_id": tournament_id},
            {
                "$set": {
                    "status": "active",
                    "matches": matches,
                    "current_round": 1,
                    "total_rounds": total_rounds,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        return {"success": True, "total_matches": len(matches)}

    async def _generate_bracket(
        self,
        tournament_id: str,
        players: List[str],
        bracket_type: str
    ) -> List[Dict[str, Any]]:
        """Generate tournament bracket."""
        if bracket_type == "single_elimination":
            return await self._generate_single_elimination_bracket(tournament_id, players)
        # Add other bracket types as needed
        return []

    async def _generate_single_elimination_bracket(
        self,
        tournament_id: str,
        players: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate single elimination bracket."""
        import random
        random.shuffle(players)  # Shuffle for fairness

        # Round to next power of 2
        2 ** math.ceil(math.log2(len(players)))

        matches = []
        match_position = 0

        # First round
        for i in range(0, len(players), 2):
            player1 = players[i] if i < len(players) else None
            player2 = players[i + 1] if i + 1 < len(players) else None

            match = {
                "match_id": str(uuid.uuid4()),
                "round_number": 1,
                "bracket_position": match_position,
                "player1_id": player1,
                "player2_id": player2,
                "winner_id": player2 if not player1 else None,  # Bye if only one player
                "score": None,
                "status": "bye" if not player1 or not player2 else "pending",
                "scheduled_time": None,
                "completed_time": None
            }
            matches.append(match)
            match_position += 1

        return matches

    async def get_active_tournaments(self) -> List[Dict[str, Any]]:
        """Get all active tournaments."""
        tournaments = await self.db.tournaments.find({
            "status": {"$in": ["registration", "active"]}
        }).sort("start_time", 1).to_list(length=100)
        return tournaments

    async def get_tournament(self, tournament_id: str) -> Optional[Dict[str, Any]]:
        """Get tournament details."""
        tournament = await self.db.tournaments.find_one({"tournament_id": tournament_id})
        return tournament

    async def get_player_tournaments(
        self,
        player_id: str,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get tournaments for a specific player."""
        query = {"registered_players": player_id}
        if status:
            query["status"] = status

        tournaments = await self.db.tournaments.find(query).to_list(length=100)
        return tournaments
