"""World Events Notification System"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()


class WorldEventNotifier:
    """Manages real-time notifications for world events"""

    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Add new WebSocket connection"""
        await websocket.accept()
        self.connections.add(websocket)
        logger.info(
            f"New world events subscriber. Total: {len(self.connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.connections.discard(websocket)
        logger.info(
            f"World events subscriber disconnected. Total: {len(self.connections)}")

    async def broadcast_event(self, event_data: Dict):
        """Broadcast event to all connected clients"""
        message = json.dumps({
            "type": "world_event",
            "data": event_data
        })

        disconnected = set()
        for connection in self.connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.add(connection)

        # Clean up disconnected clients
        for conn in disconnected:
            self.connections.discard(conn)

    async def notify_event_started(self, event):
        """Notify all clients that an event has started"""
        await self.broadcast_event({
            "event_id": event.event_id,
            "event_type": event.event_type,
            "name": event.name,
            "description": event.description,
            "severity": event.severity,
            "status": "started",
            "ends_at": event.ends_at.isoformat() if event.ends_at else None
        })

    async def notify_event_ended(self, event_id: str):
        """Notify all clients that an event has ended"""
        await self.broadcast_event({
            "event_id": event_id,
            "status": "ended"
        })

    async def notify_world_state_update(self, world_state):
        """Notify clients of world state changes"""
        await self.broadcast_event({
            "type": "world_state_update",
            "collective_karma": world_state.collective_karma,
            "karma_trend": world_state.karma_trend,
            "online_players": world_state.online_players
        })


# Global notifier instance
notifier = WorldEventNotifier()


@router.websocket("/ws/events")
async def world_events_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time world event notifications
    """
    await notifier.connect(websocket)

    try:
        while True:
            # Keep connection alive and listen for client messages
            data = await websocket.receive_text()

            # Handle client messages (ping, subscribe, etc.)
            try:
                message = json.loads(data)
                if message.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
            except json.JSONDecodeError:
                pass

    except WebSocketDisconnect:
        notifier.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        notifier.disconnect(websocket)


# Export notifier for use in other modules
def get_notifier() -> WorldEventNotifier:
    """Get the global notifier instance"""
    return notifier
