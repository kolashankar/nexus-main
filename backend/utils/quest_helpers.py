"""Quest helper utilities"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import uuid


def generate_quest_id() -> str:
    """Generate unique quest ID"""
    return str(uuid.uuid4())


def generate_objective_id() -> str:
    """Generate unique objective ID"""
    return str(uuid.uuid4())


def calculate_quest_difficulty(
    objectives: List[Dict[str, Any]],
    rewards: Dict[str, Any],
) -> str:
    """Calculate quest difficulty based on objectives and rewards"""
    # Simple heuristic
    total_required = sum(
        obj.get("required", 1)
        for obj in objectives
    )

    if total_required <= 5:
        return "easy"
    elif total_required <= 15:
        return "medium"
    elif total_required <= 30:
        return "hard"
    else:
        return "very_hard"


def calculate_quest_xp(difficulty: str, player_level: int) -> int:
    """Calculate XP reward for quest"""
    base_xp = {
        "easy": 50,
        "medium": 150,
        "hard": 400,
        "very_hard": 1000,
    }

    xp = base_xp.get(difficulty, 150)

    # Scale with player level
    multiplier = 1 + (player_level * 0.1)
    return int(xp * multiplier)


def calculate_quest_credits(difficulty: str, player_level: int) -> int:
    """Calculate credit reward for quest"""
    base_credits = {
        "easy": 100,
        "medium": 300,
        "hard": 600,
        "very_hard": 1500,
    }

    credits = base_credits.get(difficulty, 300)

    # Scale with player level
    multiplier = 1 + (player_level * 0.1)
    return int(credits * multiplier)


def format_quest_time(seconds: int) -> str:
    """Format quest completion time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def get_quest_expiry(quest_type: str) -> datetime:
    """Get expiry time for quest type"""
    now = datetime.utcnow()

    if quest_type == "daily":
        # Expires at end of day
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return tomorrow
    elif quest_type == "weekly":
        # Expires at end of week (Sunday)
        days_until_sunday = (6 - now.weekday()) % 7
        if days_until_sunday == 0:
            days_until_sunday = 7
        end_of_week = (now + timedelta(days=days_until_sunday)).replace(
            hour=23, minute=59, second=59
        )
        return end_of_week
    elif quest_type == "personal":
        # Expires in 7 days
        return now + timedelta(days=7)
    elif quest_type == "world":
        # Expires in 3 days
        return now + timedelta(days=3)
    else:
        # Default 7 days
        return now + timedelta(days=7)


def is_quest_completable(quest: Dict[str, Any]) -> bool:
    """Check if all quest objectives are completed"""
    objectives = quest.get("objectives", [])
    return all(obj.get("completed", False) for obj in objectives)


def get_quest_progress_percentage(quest: Dict[str, Any]) -> float:
    """Get overall quest progress as percentage"""
    objectives = quest.get("objectives", [])
    if not objectives:
        return 0.0

    total_progress = 0
    for obj in objectives:
        current = obj.get("current", 0)
        required = obj.get("required", 1)
        total_progress += (current / required)

    return (total_progress / len(objectives)) * 100
