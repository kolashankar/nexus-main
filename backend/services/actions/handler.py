from typing import Dict, Any
from datetime import datetime
from ..player.traits import TraitsService
from ..karma.calculator import KarmaCalculator
from .validator import ActionValidator
from .processor import ActionProcessor
from backend.core.database import get_database
import uuid

class ActionHandler:
    """Main handler for all game actions"""

    def __init__(self):
        self.validator = ActionValidator()
        self.processor = ActionProcessor()
        self.traits_service = TraitsService()
        self.karma_calculator = KarmaCalculator()
        self.db = get_database()

    async def execute_action(
        self,
        action_type: str,
        actor_id: str,
        target_id: str = None,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Execute any game action"""

        # Get actor and target
        actor = await self.db.players.find_one({"_id": actor_id})
        target = None
        if target_id:
            target = await self.db.players.find_one({"_id": target_id})

        if not actor:
            raise ValueError("Actor not found")

        # Validate action
        validation = await self.validator.validate_action(
            action_type, actor, target, params
        )
        if not validation["valid"]:
            raise ValueError(validation["reason"])

        # Process action
        result = await self.processor.process_action(
            action_type, actor, target, params
        )

        # Calculate karma changes
        karma_changes = await self.karma_calculator.calculate_simple(
            action_type, actor, target, result
        )

        # Update actor karma and traits
        await self.db.players.update_one(
            {"_id": actor_id},
            {
                "$inc": {
                    "karma_points": karma_changes["actor_karma"],
                    **{f"traits.{k}": v for k, v in karma_changes["actor_traits"].items()}
                },
                "$set": {"last_action": datetime.utcnow()}
            }
        )

        # Update target if exists
        if target_id and karma_changes.get("target_karma"):
            await self.db.players.update_one(
                {"_id": target_id},
                {
                    "$inc": {
                        "karma_points": karma_changes["target_karma"],
                        **{f"traits.{k}": v for k, v in karma_changes.get("target_traits", {}).items()}
                    }
                }
            )

        # Log action history
        action_log = {
            "_id": str(uuid.uuid4()),
            "action_type": action_type,
            "actor_id": actor_id,
            "target_id": target_id,
            "params": params,
            "result": result,
            "karma_changes": karma_changes,
            "timestamp": datetime.utcnow()
        }
        await self.db.action_history.insert_one(action_log)

        return {
            "success": True,
            "result": result,
            "karma_changes": karma_changes,
            "message": result.get("message", "Action completed successfully")
        }
