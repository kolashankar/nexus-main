"""Quest objectives manager"""

from typing import Dict, Any
import uuid


class QuestObjectivesManager:
    """Manages quest objectives"""

    @staticmethod
    def create_objective(
        objective_type: str,
        description: str,
        required: int = 1,
        target: str = "",
    ) -> Dict[str, Any]:
        """Create a new objective"""
        return {
            "objective_id": str(uuid.uuid4()),
            "description": description,
            "type": objective_type,
            "target": target,
            "current": 0,
            "required": required,
            "completed": False,
        }

    @staticmethod
    def update_objective_progress(
        objective: Dict[str, Any],
        progress: int,
    ) -> Dict[str, Any]:
        """Update objective progress"""
        if not objective.get("completed"):
            objective["current"] = min(
                objective["current"] + progress,
                objective["required"]
            )

            if objective["current"] >= objective["required"]:
                objective["completed"] = True

        return objective

    @staticmethod
    def reset_objective(objective: Dict[str, Any]) -> Dict[str, Any]:
        """Reset objective progress"""
        objective["current"] = 0
        objective["completed"] = False
        return objective

    @staticmethod
    def get_objective_progress_text(objective: Dict[str, Any]) -> str:
        """Get human-readable progress text"""
        current = objective.get("current", 0)
        required = objective.get("required", 1)
        completed = objective.get("completed", False)

        if completed:
            return "✓ Completed"
        else:
            return f"{current}/{required}"

    @staticmethod
    def calculate_objective_progress_percentage(
        objective: Dict[str, Any]
    ) -> float:
        """Calculate objective progress as percentage"""
        current = objective.get("current", 0)
        required = objective.get("required", 1)

        if required == 0:
            return 100.0

        return (current / required) * 100
