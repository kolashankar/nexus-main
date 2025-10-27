from fastapi import WebSocket
from typing import Dict, Set, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time multiplayer."""

    def __init__(self):
        # Active connections: {player_id: WebSocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Room memberships: {room_id: Set[player_id]}
        self.rooms: Dict[str, Set[str]] = {}
        # Player metadata: {player_id: {username, online_since, etc}}
        self.player_metadata: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket, player_id: str, username: str):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[player_id] = websocket
        self.player_metadata[player_id] = {
            "username": username,
            "online_since": datetime.utcnow().isoformat(),
            "current_room": None
        }
        logger.info(
            f"Player {username} ({player_id}) connected. Total online: {len(self.active_connections)}")

        # Broadcast player joined to all
        await self.broadcast({
            "event": "player_joined",
            "data": {
                "player_id": player_id,
                "username": username,
                "timestamp": datetime.utcnow().isoformat()
            }
        })

    def disconnect(self, player_id: str):
        """Remove a player connection."""
        if player_id in self.active_connections:
            username = self.player_metadata.get(
                player_id, {}).get("username", "Unknown")
            del self.active_connections[player_id]

            # Remove from all rooms
            for room_id in list(self.rooms.keys()):
                if player_id in self.rooms[room_id]:
                    self.rooms[room_id].discard(player_id)
                    if not self.rooms[room_id]:  # Remove empty rooms
                        del self.rooms[room_id]

            if player_id in self.player_metadata:
                del self.player_metadata[player_id]

            logger.info(
                f"Player {username} ({player_id}) disconnected. Total online: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, player_id: str):
        """Send a message to a specific player."""
        if player_id in self.active_connections:
            try:
                await self.active_connections[player_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {player_id}: {e}")
                self.disconnect(player_id)

    async def broadcast(self, message: dict, exclude: List[str] = None):
        """Broadcast a message to all connected players."""
        exclude = exclude or []
        disconnected = []

        for player_id, connection in self.active_connections.items():
            if player_id not in exclude:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to {player_id}: {e}")
                    disconnected.append(player_id)

        # Clean up disconnected players
        for player_id in disconnected:
            self.disconnect(player_id)

    async def broadcast_to_room(self, room_id: str, message: dict, exclude: List[str] = None):
        """Broadcast a message to all players in a specific room."""
        if room_id not in self.rooms:
            return

        exclude = exclude or []
        for player_id in self.rooms[room_id]:
            if player_id not in exclude:
                await self.send_personal_message(message, player_id)

    def join_room(self, player_id: str, room_id: str):
        """Add a player to a room."""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        self.rooms[room_id].add(player_id)

        if player_id in self.player_metadata:
            self.player_metadata[player_id]["current_room"] = room_id

        logger.info(f"Player {player_id} joined room {room_id}")

    def leave_room(self, player_id: str, room_id: str):
        """Remove a player from a room."""
        if room_id in self.rooms and player_id in self.rooms[room_id]:
            self.rooms[room_id].discard(player_id)
            if not self.rooms[room_id]:  # Remove empty rooms
                del self.rooms[room_id]

            if player_id in self.player_metadata:
                self.player_metadata[player_id]["current_room"] = None

            logger.info(f"Player {player_id} left room {room_id}")

    def get_online_players(self) -> List[dict]:
        """Get list of all online players."""
        return [
            {
                "player_id": player_id,
                "username": metadata.get("username"),
                "online_since": metadata.get("online_since"),
                "current_room": metadata.get("current_room")
            }
            for player_id, metadata in self.player_metadata.items()
        ]

    def get_room_players(self, room_id: str) -> List[str]:
        """Get list of player IDs in a specific room."""
        return list(self.rooms.get(room_id, set()))

# Global connection manager instance
manager = ConnectionManager()
