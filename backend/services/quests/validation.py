"""Quest validation service"""

from typing import Dict, Any


class QuestValidationService:
    """Validates quest data and requirements"""

    def __init__(self, db):
        self.db = db

    def validate_quest_data(self, quest_data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate quest data structure"""
        required_fields = [
            "title",
            "description",
            "quest_type",
            "objectives",
            "rewards",
        ]

        for field in required_fields:
            if field not in quest_data:
                return False, f"Missing required field: {field}"

        # Validate objectives
        if not isinstance(quest_data["objectives"], list):
            return False, "Objectives must be a list"

        if len(quest_data["objectives"]) == 0:
            return False, "Quest must have at least one objective"

        # Validate each objective
        for obj in quest_data["objectives"]:
            if "description" not in obj or "type" not in obj:
                return False, "Invalid objective structure"

        return True, "Valid"

    def validate_requirements(
        self,
        player: Dict[str, Any],
        requirements: Dict[str, Any],
    ) -> tuple[bool, str]:
        """Check if player meets quest requirements"""
        # Level check
        min_level = requirements.get("min_level", 1)
        if player.get("level", 1) < min_level:
            return False, f"Requires level {min_level}"

        # Karma checks
        player_karma = player.get("karma_points", 0)
        min_karma = requirements.get("min_karma")
        max_karma = requirements.get("max_karma")

        if min_karma is not None and player_karma < min_karma:
            return False, f"Requires minimum {min_karma} karma"

        if max_karma is not None and player_karma > max_karma:
            return False, f"Requires maximum {max_karma} karma"

        # Trait checks
        required_traits = requirements.get("required_traits", {})
        player_traits = player.get("traits", {})

        for trait, value in required_traits.items():
            if player_traits.get(trait, 0) < value:
                return False, f"Requires {trait} level {value}"

        return True, "Requirements met"

    def validate_objective_progress(
        self,
        objective: Dict[str, Any],
        progress: int,
    ) -> tuple[bool, str]:
        """Validate objective progress update"""
        if objective.get("completed"):
            return False, "Objective already completed"

        if progress < 0:
            return False, "Progress cannot be negative"

        return True, "Valid progress"
