"""Oracle API Routes"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
import logging

from .schemas import QuestGenerationRequestAPI, GeneratedQuestAPI, GeneratedCampaignAPI
from backend.services.ai.oracle.oracle import oracle
from backend.services.ai.cost_tracker import cost_tracker
from backend.api.v1.deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/oracle", tags=["AI - Oracle"])


@router.post("/generate-quest", response_model=GeneratedQuestAPI)
async def generate_quest(
    request: QuestGenerationRequestAPI,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate a personalized quest using Oracle AI"""

    try:
        # Use current user's data if not provided
        player_data = request.player or current_user

        quest = await oracle.generate_quest_for_player(
            player=player_data,
            quest_type=request.quest_type,
            difficulty=request.difficulty
        )

        return quest

    except Exception as e:
        logger.error(f"Quest generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-daily-quests")
async def generate_daily_quests(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate 3 daily quests for current player"""

    try:
        quests = await oracle.generate_daily_quests(current_user, count=3)
        return {"quests": [q.dict() for q in quests]}

    except Exception as e:
        logger.error(f"Daily quest generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-campaign", response_model=GeneratedCampaignAPI)
async def generate_campaign(
    campaign_type: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Generate a story campaign for current player"""

    try:
        campaign = await oracle.generate_campaign(
            player=current_user,
            campaign_type=campaign_type
        )

        return campaign

    except Exception as e:
        logger.error(f"Campaign generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_oracle_status(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get Oracle status"""
    return {
        "available": oracle.is_available(),
        "model": oracle.model
    }


@router.get("/stats")
async def get_oracle_stats(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get quest generation statistics"""
    stats = {
        "quest_stats": cost_tracker.get_stats("oracle_quest"),
        "campaign_stats": cost_tracker.get_stats("oracle_campaign")
    }
    return stats
