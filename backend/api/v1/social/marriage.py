from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.social.marriage import MarriageService
from backend.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()


class ProposeRequest(BaseModel):
    player_id: str


@router.post("/propose", response_model=dict)
async def propose_marriage(
    request: ProposeRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Propose marriage to another player"""
    service = MarriageService(db)

    try:
        proposal = await service.propose_marriage(
            proposer_id=current_user["_id"],
            proposed_to_id=request.player_id
        )
        return {"success": True, "proposal": proposal}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/proposals", response_model=list)
async def get_pending_proposals(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get pending marriage proposals"""
    service = MarriageService(db)
    proposals = await service.get_pending_proposals(current_user["_id"])
    return proposals


@router.post("/proposals/{proposal_id}/accept", response_model=dict)
async def accept_proposal(
    proposal_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Accept marriage proposal"""
    service = MarriageService(db)

    try:
        marriage = await service.accept_proposal(proposal_id)
        return {"success": True, "marriage": marriage.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/proposals/{proposal_id}/reject", response_model=dict)
async def reject_proposal(
    proposal_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Reject marriage proposal"""
    service = MarriageService(db)

    try:
        success = await service.reject_proposal(proposal_id)
        return {"success": success, "message": "Proposal rejected"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-marriage", response_model=dict)
async def get_my_marriage(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get my current marriage"""
    service = MarriageService(db)
    marriage = await service.get_player_marriage(current_user["_id"])

    if not marriage:
        raise HTTPException(status_code=404, detail="Not married")

    return marriage


@router.post("/divorce", response_model=dict)
async def divorce(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Divorce (end marriage)"""
    service = MarriageService(db)

    marriage = await service.get_player_marriage(current_user["_id"])
    if not marriage:
        raise HTTPException(status_code=400, detail="Not married")

    try:
        success = await service.divorce(marriage.get("id"), current_user["_id"])
        return {"success": success, "message": "Divorced (karma penalty applied)"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
