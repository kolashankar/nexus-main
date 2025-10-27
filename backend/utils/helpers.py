"""Helper utility functions."""

from datetime import datetime
import random
import string

def generate_id(length: int = 16) -> str:
    """Generate a random ID."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def calculate_level_from_xp(xp: int) -> int:
    """Calculate player level from XP.
    
    Formula: Level = floor(sqrt(XP / 100))
    """
    return int((xp / 100) ** 0.5)

def calculate_xp_for_level(level: int) -> int:
    """Calculate XP required for a level."""
    return level * level * 100

def calculate_karma_class(karma: float) -> str:
    """Calculate moral class based on karma."""
    if karma >= 500:
        return "good"
    elif karma <= -500:
        return "bad"
    else:
        return "average"

def calculate_economic_class(credits: float) -> str:
    """Calculate economic class based on credits."""
    if credits >= 100000:
        return "rich"
    elif credits >= 10000:
        return "middle"
    else:
        return "poor"

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))

def format_timestamp(dt: datetime) -> str:
    """Format datetime for JSON."""
    return dt.isoformat()

def calculate_trait_change(base_value: float, change: float) -> float:
    """Calculate new trait value with bounds checking."""
    new_value = base_value + change
    return clamp(new_value, 0.0, 100.0)
