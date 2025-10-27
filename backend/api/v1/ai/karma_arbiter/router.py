"""Karma Arbiter API Routes"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import logging

from .schemas import EvaluationRequestAPI, EvaluationResponseAPI
from backend.services.ai.karma_arbiter.arbiter import karma_arbiter
from backend.services.ai.cost_tracker import cost_tracker
from backend.api.v1.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/karma-arbiter", tags=["AI - Karma Arbiter"])


@router.post("/evaluate", response_model=EvaluationResponseAPI)
async def evaluate_action(
    request: EvaluationRequestAPI,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Evaluate an action using Karma Arbiter AI"""

    try:
        result = await karma_arbiter.evaluate_action(
            action_type=request.action_type,
            action_details=request.action_details,
            actor=request.actor,
            target=request.target,
            additional_context=request.additional_context
        )

        return EvaluationResponseAPI(
            karma_change=result.karma_change,
            trait_changes=result.trait_changes,
            event_triggered=result.event_triggered,
            message=result.message,
            reasoning=result.reasoning,
            severity=result.severity,
            cached=result.cached
        )

    except Exception as e:
        logger.error(f"Karma evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_arbiter_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get Karma Arbiter status"""
    return {
        "available": karma_arbiter.is_available(),
        "model": karma_arbiter.model
    }


@router.get("/stats")
async def get_karma_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get karma evaluation statistics"""
    return cost_tracker.get_stats("karma_arbiter")
