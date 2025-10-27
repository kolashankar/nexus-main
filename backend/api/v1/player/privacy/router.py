from fastapi import APIRouter, Depends, HTTPException
from .....services.player.visibility import VisibilityService
from .....api.deps import get_current_user
from .schemas import VisibilitySettingsUpdate, PrivacyTierUpdate

router = APIRouter()

@router.get("/settings")
async def get_privacy_settings(current_user: dict = Depends(get_current_user)):
    """Get current privacy settings"""
    service = VisibilityService()
    return await service.get_privacy_settings(current_user["_id"])

@router.put("/settings")
async def update_privacy_settings(
    settings: VisibilitySettingsUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update privacy settings"""
    service = VisibilityService()
    try:
        result = await service.update_privacy_settings(
            current_user["_id"],
            settings.dict(exclude_unset=True)
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tier")
async def change_privacy_tier(
    tier_update: PrivacyTierUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Change privacy tier"""
    service = VisibilityService()
    try:
        result = await service.change_privacy_tier(
            current_user["_id"],
            tier_update.tier
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
