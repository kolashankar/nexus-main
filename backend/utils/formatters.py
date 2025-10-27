"""Data formatting utilities"""
from datetime import datetime
from typing import Dict, Any

def format_player_response(player: Dict[str, Any]) -> Dict[str, Any]:
    """Format player data for API response"""
    return {
        "id": str(player["_id"]),
        "username": player["username"],
        "level": player.get("level", 1),
        "xp": player.get("xp", 0),
        "karma_points": player.get("karma_points", 0),
        "economic_class": player.get("economic_class", "middle"),
        "moral_class": player.get("moral_class", "average"),
        "currencies": player.get("currencies", {}),
        "traits": player.get("traits", {}),
        "created_at": player.get("created_at").isoformat() if player.get("created_at") else None
    }

def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat() if dt else None

def format_karma_change(karma_change: int) -> str:
    """Format karma change with + or - prefix"""
    if karma_change > 0:
        return f"+{karma_change}"
    return str(karma_change)
