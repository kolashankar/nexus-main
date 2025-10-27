"""Action Evaluator - Processes individual actions"""

import json
import logging
from typing import Dict, Any

from .prompts import ACTION_EVALUATION_TEMPLATE
from .schemas import EvaluationRequest, EvaluationResponse
from .config import MODEL_CONFIG
from ..client import ai_client
from ..cache_manager import cache_manager
from ..cost_tracker import cost_tracker

logger = logging.getLogger(__name__)


class ActionEvaluator:
    """Evaluates individual actions using AI"""

    def __init__(self):
        self.ai_client = ai_client
        self.cache_manager = cache_manager
        self.cost_tracker = cost_tracker

    def _format_traits(self, traits: Dict[str, float], threshold: float, above: bool = True) -> str:
        """Format traits for prompt"""
        if above:
            filtered = {k: v for k, v in traits.items() if v >= threshold}
        else:
            filtered = {k: v for k, v in traits.items() if v < threshold}

        if not filtered:
            return "None"

        return "\n".join([f"- {trait}: {value:.1f}%" for trait, value in sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:5]])

    def _generate_cache_key(self, request: EvaluationRequest) -> Dict[str, Any]:
        """Generate cache key parameters"""
        return {
            "action_type": request.context.action_type,
            "actor_karma_range": int(request.actor.karma_points / 100) * 100,
            "actor_moral": request.actor.moral_class,
            "target_moral": request.target.moral_class if request.target else None,
            "amount_range": int(request.context.amount / 1000) * 1000 if request.context.amount else None,
        }

    async def evaluate(self, request: EvaluationRequest, use_cache: bool = True) -> EvaluationResponse:
        """Evaluate an action and return karma/trait changes"""

        # Try cache first
        if use_cache:
            cache_params = self._generate_cache_key(request)
            cached_result = await self.cache_manager.get("karma_arbiter", cache_params)
            if cached_result:
                logger.info(
                    f"Using cached evaluation for {request.context.action_type}")
                self.cost_tracker.track_call(
                    "karma_arbiter", MODEL_CONFIG["default_model"], 0, 0, cached=True)
                cached_result["cached"] = True
                return EvaluationResponse(**cached_result)

        # Prepare prompt
        prompt = self._prepare_prompt(request)

        # Call AI
        try:
            response = await self._call_ai(prompt)
            result = self._parse_response(response)

            # Cache the result
            if use_cache:
                await self.cache_manager.set("karma_arbiter", cache_params, result)

            return EvaluationResponse(**result)

        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            return self._fallback_evaluation(request)

    def _prepare_prompt(self, request: EvaluationRequest) -> str:
        """Prepare the evaluation prompt"""
        actor = request.actor
        target = request.target
        context = request.context

        return ACTION_EVALUATION_TEMPLATE.format(
            action_type=context.action_type,
            action_details=json.dumps(context.action_details),
            actor_username=actor.username,
            actor_karma=actor.karma_points,
            actor_moral_class=actor.moral_class,
            actor_economic_class=actor.economic_class,
            actor_recent_actions=", ".join(
                actor.recent_actions[-5:]) if actor.recent_actions else "None",
            actor_top_traits=self._format_traits(actor.traits, 60, above=True),
            actor_low_traits=self._format_traits(
                actor.traits, 40, above=False),
            target_username=target.username if target else "N/A",
            target_karma=target.karma_points if target else "N/A",
            target_moral_class=target.moral_class if target else "N/A",
            target_economic_class=target.economic_class if target else "N/A",
            target_top_traits=self._format_traits(
                target.traits, 60, above=True) if target else "N/A",
            context=request.additional_context or "Standard action"
        )

    async def _call_ai(self, prompt: str) -> Dict[str, Any]:
        """Call AI for evaluation"""
        from .prompts import KARMA_ARBITER_SYSTEM

        messages = [
            {"role": "system", "content": KARMA_ARBITER_SYSTEM},
            {"role": "user", "content": prompt}
        ]

        response = await self.ai_client.chat_completion(
            messages=messages,
            model=MODEL_CONFIG["default_model"],
            temperature=MODEL_CONFIG["temperature"],
            response_format={"type": "json_object"},
            max_tokens=MODEL_CONFIG["max_tokens"]
        )

        # Track usage
        if "usage" in response:
            self.cost_tracker.track_call(
                "karma_arbiter",
                MODEL_CONFIG["default_model"],
                response["usage"]["prompt_tokens"],
                response["usage"]["completion_tokens"],
                cached=False
            )

        return response

    def _parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response"""
        try:
            content = response.get("content", "{}")
            result = json.loads(content)

            # Validate and normalize
            return {
                "karma_change": float(result.get("karma_change", 0)),
                "trait_changes": result.get("trait_changes", {}),
                "event_triggered": result.get("event_triggered"),
                "message": result.get("message", "The Arbiter has judged your action."),
                "reasoning": result.get("reasoning", "Judgment rendered."),
                "severity": result.get("severity", "moderate"),
                "cached": False
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            raise

    def _fallback_evaluation(self, request: EvaluationRequest) -> EvaluationResponse:
        """Fallback evaluation when AI is unavailable"""
        action_type = request.context.action_type
        severity = "moderate"  # Default severity for fallback

        # Simple rule-based evaluation
        karma_change = 0
        trait_changes = {}

        if action_type == "help":
            karma_change = 20
            trait_changes = {"kindness": 2, "empathy": 2}
            severity = "minor"
        elif action_type == "steal":
            karma_change = -30
            trait_changes = {"greed": 3, "deceit": 2}
            severity = "major"
        elif action_type == "hack":
            karma_change = -15
            trait_changes = {"hacking": 1, "deceit": 1}
            severity = "moderate"
        elif action_type == "donate":
            karma_change = 25
            trait_changes = {"generosity": 3, "kindness": 2}
            severity = "minor"

        return EvaluationResponse(
            karma_change=karma_change,
            trait_changes=trait_changes,
            event_triggered=None,
            message="Action processed using default rules (AI unavailable)",
            reasoning="Fallback rule-based evaluation",
            severity=severity,
            cached=False
        )
