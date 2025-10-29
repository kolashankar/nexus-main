"""Enhanced task type definitions."""

from enum import Enum

class TaskType(str, Enum):
    """Available task types in the game."""
    
    # Original types
    MORAL_CHOICE = "moral_choice"
    EXPLORATION = "exploration"
    SKILL_BASED = "skill_based"
    SOCIAL = "social"
    
    # New types
    COMBAT = "combat"
    ECONOMIC = "economic"
    RELATIONSHIP = "relationship"
    GUILD = "guild"
    ETHICAL_DILEMMA = "ethical_dilemma"
    
    # Multiplayer types
    COOP = "coop"
    COMPETITIVE = "competitive"
    GUILD_MISSION = "guild_mission"
    PVP_MORAL = "pvp_moral"

class TaskDifficulty(str, Enum):
    """Task difficulty levels."""
    TUTORIAL = "tutorial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    LEGENDARY = "legendary"

class TaskCategory(str, Enum):
    """Task categories for organization."""
    STORY = "story"
    DAILY = "daily"
    WEEKLY = "weekly"
    SEASONAL = "seasonal"
    EVENT = "event"
    HIDDEN = "hidden"
    PERSONAL = "personal"

class CombatOutcome(str, Enum):
    """Possible combat task outcomes."""
    FIGHT = "fight"
    FLEE = "flee"
    NEGOTIATE = "negotiate"
    SURRENDER = "surrender"
    AMBUSH = "ambush"

class EconomicAction(str, Enum):
    """Economic task actions."""
    INVEST = "invest"
    SAVE = "save"
    GAMBLE = "gamble"
    TRADE = "trade"
    DONATE = "donate"
    HOARD = "hoard"

class RelationshipAction(str, Enum):
    """Relationship task actions."""
    BEFRIEND = "befriend"
    BETRAY = "betray"
    IGNORE = "ignore"
    HELP = "help"
    EXPLOIT = "exploit"
    FORGIVE = "forgive"

class GuildAction(str, Enum):
    """Guild-related actions."""
    JOIN = "join"
    LEAD = "lead"
    OPPOSE = "oppose"
    SUPPORT = "support"
    LEAVE = "leave"
    RECRUIT = "recruit"
