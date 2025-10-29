"""Update task types enum with new multiplayer task types."""

from enum import Enum

class TaskType(str, Enum):
    """Types of tasks available in the game."""
    # Original task types
    MORAL_CHOICE = "moral_choice"
    EXPLORATION = "exploration"
    SKILL_BASED = "skill_based"
    SOCIAL = "social"
    
    # Enhanced task types from Batch 1
    COMBAT = "combat"
    ECONOMIC = "economic"
    RELATIONSHIP = "relationship"
    GUILD = "guild"
    ETHICAL_DILEMMA = "ethical_dilemma"
    
    # Multiplayer task types (Batch 4)
    COOP = "coop"  # Co-op tasks requiring multiple players
    COMPETITIVE = "competitive"  # PvP competitive challenges
    PVP_MORAL = "pvp_moral"  # Moral choices affecting other players
    GUILD_BENEFIT = "guild_benefit"  # Tasks that benefit entire guild
    
class TaskDifficulty(str, Enum):
    """Difficulty levels for tasks."""
    TUTORIAL = "tutorial"  # Level 1-3
    EASY = "easy"  # Level 1-10
    MEDIUM = "medium"  # Level 10-20
    HARD = "hard"  # Level 20-35
    EXPERT = "expert"  # Level 35-50
    LEGENDARY = "legendary"  # Level 50+

class TaskStatus(str, Enum):
    """Status of a task."""
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"
    LOCKED = "locked"
    
    # Multiplayer-specific statuses
    LOOKING_FOR_PARTNERS = "looking_for_partners"
    LOOKING_FOR_OPPONENT = "looking_for_opponent"
    READY_TO_START = "ready_to_start"
    PENDING_CHOICE = "pending_choice"
    MATCHED = "matched"

class TaskCategory(str, Enum):
    """Categories for organizing tasks."""
    MAIN_QUEST = "main_quest"
    SIDE_QUEST = "side_quest"
    DAILY = "daily"
    WEEKLY = "weekly"
    EVENT = "event"
    GUILD = "guild"
    PERSONAL = "personal"
    MULTIPLAYER = "multiplayer"
    PVP = "pvp"
    SEASONAL = "seasonal"
