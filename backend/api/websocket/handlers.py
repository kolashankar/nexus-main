from fastapi import WebSocket, WebSocketDisconnect, Query, status
from jose import JWTError, jwt
import logging
from .manager import manager
from .events.player import handle_player_event

logger = logging.getLogger(__name__)

class WebSocketHandler:
    """Handles WebSocket events and routes them to appropriate handlers."""

    def __init__(self):
        self.event_handlers = {
            "player": handle_player_event,
            # More handlers will be added in later phases
            # "combat": handle_combat_event,
            # "chat": handle_chat_event,
            # "world": handle_world_event,
        }

    async def handle_event(self, event_data: dict, player_id: str):
        """Route an event to the appropriate handler."""
        try:
            event_type = event_data.get("type")
            event_name = event_data.get("event")
            data = event_data.get("data", {})

            if event_type in self.event_handlers:
                handler = self.event_handlers[event_type]
                response = await handler(event_name, data, player_id)
                return response
            else:
                logger.warning(f"Unknown event type: {event_type}")
                return {
                    "type": "error",
                    "message": f"Unknown event type: {event_type}"
                }
        except Exception as e:
            logger.error(f"Error handling event: {e}")
            return {
                "type": "error",
                "message": str(e)
            }

handler = WebSocketHandler()


async def verify_websocket_token(token: str, secret_key: str) -> dict:
    """
    Verify JWT token and extract user information.
    
    Args:
        token: JWT token string
        secret_key: Secret key for JWT verification
        
    Returns:
        dict with user_id and username
        
    Raises:
        JWTError: If token is invalid
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
        username = payload.get("username")
        
        if not user_id:
            raise JWTError("Token payload missing 'sub' field")
            
        return {
            "user_id": user_id,
            "username": username or user_id  # Fallback to user_id if username not in token
        }
    except JWTError as e:
        logger.error(f"JWT verification failed: {e}")
        raise


async def websocket_endpoint(
    websocket: WebSocket, 
    token: str = Query(...),
    secret_key: str = None  # This should be injected via dependency
):
    """
    Main WebSocket endpoint for handling connections.
    
    Args:
        websocket: WebSocket connection
        token: JWT token from query parameter
        secret_key: JWT secret key (injected via dependency)
    """
    
    # If secret_key not provided via dependency, get from settings
    if secret_key is None:
        from backend.core.config import settings
        secret_key = settings.SECRET_KEY
    
    try:
        # Verify token and extract user info
        user_info = await verify_websocket_token(token, secret_key)
        player_id = user_info["user_id"]
        username = user_info["username"]
        
    except JWTError as e:
        logger.warning(f"WebSocket connection rejected - Invalid token: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    except Exception as e:
        logger.error(f"WebSocket authentication error: {e}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return
    
    # Accept the WebSocket connection
    await manager.connect(websocket, player_id, username)
    
    try:
        # Send initial connection success message
        await manager.send_personal_message({
            "type": "connection",
            "event": "connected",
            "data": {
                "message": "Connected to Karma Nexus",
                "player_id": player_id,
                "username": username,
                "online_players": manager.get_online_players()
            }
        }, player_id)
        
        logger.info(f"Player {username} ({player_id}) connected via WebSocket")

        # Listen for messages
        while True:
            data = await websocket.receive_json()
            
            logger.debug(f"Received event from {player_id}: {data}")

            # Handle the event
            response = await handler.handle_event(data, player_id)

            # Send response back to client
            if response:
                await manager.send_personal_message(response, player_id)

    except WebSocketDisconnect:
        logger.info(f"Player {username} ({player_id}) disconnected")
        manager.disconnect(player_id)
        
        # Broadcast player left
        await manager.broadcast({
            "type": "player",
            "event": "player_left",
            "data": {
                "player_id": player_id,
                "username": username
            }
        })
        
    except Exception as e:
        logger.error(f"WebSocket error for player {player_id}: {e}", exc_info=True)
        manager.disconnect(player_id)
        try:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        except:
            pass