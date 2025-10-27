"""Validation utility functions."""

import re
from typing import Optional

def validate_username(username: str) -> tuple[bool, Optional[str]]:
    """Validate username format."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 20:
        return False, "Username must be at most 20 characters long"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, None

def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None

def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if len(password) > 100:
        return False, "Password is too long"
    return True, None

def validate_trait_value(value: float) -> bool:
    """Validate trait value is within bounds."""
    return 0 <= value <= 100

def validate_karma_value(value: float) -> bool:
    """Validate karma value is reasonable."""
    return -10000 <= value <= 10000
