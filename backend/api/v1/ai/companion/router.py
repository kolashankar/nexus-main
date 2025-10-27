"""AI Companion API Routes"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import logging

from .schemas import CompanionMessageAPI, CompanionResponseAPI, AdviceRequestAPI
from backend.services.ai.companion.companion import ai_companion
from backend.services.ai.cost_tracker import cost_tracker
from backend.api.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/companion", tags=["AI - Companion"])


@router.post("/talk", response_model=CompanionResponseAPI)
async def talk_to_companion(
    message: CompanionMessageAPI,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Have a conversation with your AI companion"""

    try:
        response = await ai_companion.talk(
            player=current_user,
            message=message.message,
            context=message.context
        )

        return CompanionResponseAPI(**response)

    except Exception as e:
        logger.error(f"Companion conversation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advice")
async def get_advice(
    request: AdviceRequestAPI,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get advice from your AI companion"""

    try:
        response = await ai_companion.give_advice(
            player=current_user,
            situation=request.situation
        )

        return response

    except Exception as e:
        logger.error(f"Companion advice error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_companion_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get your AI companion status"""

    try:
        status = await ai_companion.get_companion_status(current_user)
        return status

    except Exception as e:
        logger.error(f"Companion status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_companion_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get companion interaction statistics"""
    stats = {
        "dialogue_stats": cost_tracker.get_stats("companion_dialogue"),
        "advice_stats": cost_tracker.get_stats("companion_advice")
    }
    return stats
