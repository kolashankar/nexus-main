import logging
from typing import Dict, Any
from backend.api.websocket.manager import manager

logger = logging.getLogger(__name__)

async def handle_player_event(event_name: str, data: Dict[str, Any], player_id: str) -> Dict[str, Any]:
    """Handle player-related WebSocket events."""

    if event_name == "location_update":
        # Player moved in the game world
        location = data.get("location", {})

        # Broadcast to nearby players (for now, broadcast to all)
        await manager.broadcast({
            "type": "player",
            "event": "player_moved",
            "data": {
                "player_id": player_id,
                "location": location
            }
        }, exclude=[player_id])

        return {
            "type": "player",
            "event": "location_updated",
            "data": {"success": True}
        }

    elif event_name == "action_performed":
        # Player performed an action (hack, help, etc.)
        action_type = data.get("action_type")
        target_id = data.get("target_id")

        # Notify the target player
        if target_id:
            await manager.send_personal_message({
                "type": "player",
                "event": "action_received",
                "data": {
                    "from_player_id": player_id,
                    "action_type": action_type,
                    "details": data
                }
            }, target_id)

        return {
            "type": "player",
            "event": "action_acknowledged",
            "data": {"success": True}
        }

    elif event_name == "join_room":
        # Player joins a game room (territory, guild hall, etc.)
        room_id = data.get("room_id")
        if room_id:
            manager.join_room(player_id, room_id)

            # Notify others in the room
            await manager.broadcast_to_room(room_id, {
                "type": "player",
                "event": "player_joined_room",
                "data": {
                    "player_id": player_id,
                    "room_id": room_id
                }
            }, exclude=[player_id])

            return {
                "type": "player",
                "event": "room_joined",
                "data": {
                    "room_id": room_id,
                    "players": manager.get_room_players(room_id)
                }
            }

    elif event_name == "leave_room":
        # Player leaves a game room
        room_id = data.get("room_id")
        if room_id:
            manager.leave_room(player_id, room_id)

            # Notify others in the room
            await manager.broadcast_to_room(room_id, {
                "type": "player",
                "event": "player_left_room",
                "data": {
                    "player_id": player_id,
                    "room_id": room_id
                }
            })

            return {
                "type": "player",
                "event": "room_left",
                "data": {"room_id": room_id}
            }

    else:
        logger.warning(f"Unknown player event: {event_name}")
        return {
            "type": "error",
            "message": f"Unknown player event: {event_name}"
        }
