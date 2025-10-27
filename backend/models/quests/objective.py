"""Quest objective models"""

from enum import Enum
from typing import Optional, Any, Dict
from pydantic import BaseModel


class ObjectiveType(str, Enum):
    """Types of quest objectives"""
    KILL = "kill"  # Kill specific enemies
    COLLECT = "collect"  # Collect items
    TALK = "talk"  # Talk to NPCs
    HACK = "hack"  # Hack systems
    TRADE = "trade"  # Trade with players
    VISIT = "visit"  # Visit locations
    WIN_COMBAT = "win_combat"  # Win combats
    EARN_KARMA = "earn_karma"  # Earn karma points
    REACH_TRAIT = "reach_trait"  # Reach trait level
    DONATE = "donate"  # Donate credits
    STEAL = "steal"  # Steal from others
    HELP = "help"  # Help other players
    PURCHASE = "purchase"  # Purchase items
    SELL = "sell"  # Sell items
    TRAIN_ROBOT = "train_robot"  # Train robots
    WIN_DUEL = "win_duel"  # Win duels
    JOIN_GUILD = "join_guild"  # Join a guild
    CAPTURE_TERRITORY = "capture_territory"  # Capture territory


class Objective(BaseModel):
    """Single quest objective"""
    objective_id: str
    description: str
    type: ObjectiveType

    # Target details
    target: str  # What needs to be done
    target_details: Optional[Dict[str, Any]] = None  # Additional details

    # Progress
    current: int = 0
    required: int = 1
    completed: bool = False

    # Display
    display_order: int = 0
    hidden: bool = False  # Hidden objectives

    class Config:
        use_enum_values = True

    def update_progress(self, amount: int = 1) -> bool:
        """Update objective progress"""
        if self.completed:
            return False

        self.current = min(self.current + amount, self.required)

        if self.current >= self.required:
            self.completed = True
            return True

        return False

    def get_progress_percentage(self) -> float:
        """Get progress as percentage"""
        if self.required == 0:
            return 100.0
        return (self.current / self.required) * 100

    def to_display_dict(self) -> dict:
        """Convert to display dictionary (for frontend)"""
        return {
            "id": self.objective_id,
            "description": self.description,
            "type": self.type,
            "current": self.current,
            "required": self.required,
            "completed": self.completed,
            "progress_percentage": self.get_progress_percentage(),
            "hidden": self.hidden,
        }


class ObjectiveTemplate(BaseModel):
    """Template for generating objectives"""
    type: ObjectiveType
    description_template: str  # With placeholders
    target_type: str  # Type of target
    min_required: int = 1
    max_required: int = 10

    class Config:
        use_enum_values = True


# Common objective templates
OBJECTIVE_TEMPLATES = {
    ObjectiveType.KILL: ObjectiveTemplate(
        type=ObjectiveType.KILL,
        description_template="Defeat {count} {enemy_type}",
        target_type="enemy",
        min_required=1,
        max_required=20,
    ),
    ObjectiveType.COLLECT: ObjectiveTemplate(
        type=ObjectiveType.COLLECT,
        description_template="Collect {count} {item_name}",
        target_type="item",
        min_required=1,
        max_required=50,
    ),
    ObjectiveType.HACK: ObjectiveTemplate(
        type=ObjectiveType.HACK,
        description_template="Successfully hack {count} systems",
        target_type="system",
        min_required=1,
        max_required=10,
    ),
    ObjectiveType.EARN_KARMA: ObjectiveTemplate(
        type=ObjectiveType.EARN_KARMA,
        description_template="Earn {count} karma points",
        target_type="karma",
        min_required=50,
        max_required=500,
    ),
    ObjectiveType.WIN_COMBAT: ObjectiveTemplate(
        type=ObjectiveType.WIN_COMBAT,
        description_template="Win {count} combat battles",
        target_type="combat",
        min_required=1,
        max_required=10,
    ),
}
