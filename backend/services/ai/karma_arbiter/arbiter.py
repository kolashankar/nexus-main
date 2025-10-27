"""Karma Arbiter - Main Service"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..base import BaseAIService
from .evaluator import ActionEvaluator
from .schemas import EvaluationRequest, EvaluationResponse, ActionContext, PlayerProfile

logger = logging.getLogger(__name__)


class KarmaArbiter(BaseAIService):
    """The Karma Arbiter - Supreme Judge of Actions"""

    def __init__(self):
        super().__init__("KarmaArbiter", model="gpt-4o")
        self.evaluator = ActionEvaluator()
        logger.info("Karma Arbiter initialized")

    async def evaluate_action(
        self,
        action_type: str,
        action_details: Dict[str, Any],
        actor: Dict[str, Any],
        target: Optional[Dict[str, Any]] = None,
        additional_context: Optional[str] = None
    ) -> EvaluationResponse:
        """Evaluate a player action and return consequences"""

        # Create evaluation request
        request = EvaluationRequest(
            context=ActionContext(
                action_type=action_type,
                action_details=action_details,
                actor_id=actor.get("_id", ""),
                target_id=target.get("_id") if target else None,
                amount=action_details.get("amount"),
                timestamp=datetime.utcnow().isoformat()
            ),
            actor=PlayerProfile(
                username=actor.get("username", "Unknown"),
                karma_points=actor.get("karma_points", 0),
                moral_class=actor.get("moral_class", "average"),
                economic_class=actor.get("economic_class", "middle"),
                traits=actor.get("traits", {}),
                recent_actions=actor.get("recent_actions", [])
            ),
            target=PlayerProfile(
                username=target.get("username", "Unknown"),
                karma_points=target.get("karma_points", 0),
                moral_class=target.get("moral_class", "average"),
                economic_class=target.get("economic_class", "middle"),
                traits=target.get("traits", {}),
                recent_actions=target.get("recent_actions", [])
            ) if target else None,
            additional_context=additional_context
        )

        # Evaluate
        result = await self.evaluator.evaluate(request, use_cache=True)

        logger.info(
            f"Karma Arbiter evaluated {action_type}: "
            f"karma_change={result.karma_change}, "
            f"traits={len(result.trait_changes)}, "
            f"cached={result.cached}"
        )

        return result

    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        """Process action evaluation (base class requirement)"""
        result = await self.evaluate_action(*args, **kwargs)
        return result.dict()

    async def batch_evaluate(
        self,
        actions: list[Dict[str, Any]]
    ) -> list[EvaluationResponse]:
        """Evaluate multiple actions efficiently"""
        results = []
        for action_data in actions:
            try:
                result = await self.evaluate_action(
                    action_type=action_data["action_type"],
                    action_details=action_data["action_details"],
                    actor=action_data["actor"],
                    target=action_data.get("target"),
                    additional_context=action_data.get("context")
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Batch evaluation error: {e}")
                results.append(self.evaluator._fallback_evaluation(
                    EvaluationRequest(
                        context=ActionContext(
                            action_type=action_data["action_type"],
                            action_details=action_data["action_details"],
                            actor_id="",
                            timestamp=datetime.utcnow().isoformat()
                        ),
                        actor=PlayerProfile(**action_data["actor"]),
                        target=PlayerProfile(
                            **action_data["target"]) if action_data.get("target") else None
                    )
                ))

        return results


# Global karma arbiter instance
karma_arbiter = KarmaArbiter()
