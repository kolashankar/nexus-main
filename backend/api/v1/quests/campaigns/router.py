from fastapi import APIRouter, Depends, HTTPException, status
from .....core.security import get_current_user
from .....services.quests.campaigns import CampaignService
from .schemas import (
    CampaignListResponse,
    StartCampaignRequest,
    CampaignProgressResponse,
    MakeCampaignChoiceRequest
)

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("/available", response_model=CampaignListResponse)
async def get_available_campaigns(
    current_user: dict = Depends(get_current_user)
):
    """Get available story campaigns."""
    campaign_service = CampaignService()
    campaigns = await campaign_service.get_available_campaigns(current_user["_id"])
    return {"campaigns": campaigns}


@router.get("/active")
async def get_active_campaign(
    current_user: dict = Depends(get_current_user)
):
    """Get player's active campaign."""
    campaign_service = CampaignService()
    campaign = await campaign_service.get_active_campaign(current_user["_id"])
    return campaign


@router.post("/start")
async def start_campaign(
    request: StartCampaignRequest,
    current_user: dict = Depends(get_current_user)
):
    """Start a new campaign."""
    campaign_service = CampaignService()

    result = await campaign_service.start_campaign(
        current_user["_id"],
        request.campaign_type
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to start campaign")
        )

    return result


@router.get("/progress", response_model=CampaignProgressResponse)
async def get_campaign_progress(
    current_user: dict = Depends(get_current_user)
):
    """Get progress on active campaign."""
    campaign_service = CampaignService()
    progress = await campaign_service.get_campaign_progress(current_user["_id"])

    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active campaign"
        )

    return progress


@router.post("/choice")
async def make_campaign_choice(
    request: MakeCampaignChoiceRequest,
    current_user: dict = Depends(get_current_user)
):
    """Make a choice in campaign storyline."""
    campaign_service = CampaignService()

    result = await campaign_service.make_choice(
        current_user["_id"],
        request.chapter_number,
        request.choice
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to make choice")
        )

    return result
