from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.social.mentorship import MentorshipService
from backend.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()


class RequestMentorshipRequest(BaseModel):
    mentor_id: str


@router.post("/request", response_model=dict)
async def request_mentorship(
    request: RequestMentorshipRequest,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Request mentorship from a player"""
    service = MentorshipService(db)

    try:
        mentorship_request = await service.request_mentorship(
            apprentice_id=current_user["_id"],
            mentor_id=request.mentor_id
        )
        return {"success": True, "request": mentorship_request}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/requests", response_model=list)
async def get_pending_requests(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get pending mentorship requests (as mentor)"""
    service = MentorshipService(db)
    requests = await service.get_pending_requests(current_user["_id"])
    return requests


@router.post("/requests/{request_id}/accept", response_model=dict)
async def accept_mentorship(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Accept mentorship request"""
    service = MentorshipService(db)

    try:
        mentorship = await service.accept_mentorship(request_id)
        return {"success": True, "mentorship": mentorship.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/requests/{request_id}/reject", response_model=dict)
async def reject_mentorship(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Reject mentorship request"""
    service = MentorshipService(db)

    try:
        success = await service.reject_mentorship(request_id)
        return {"success": success, "message": "Mentorship request rejected"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/my-mentorship", response_model=dict)
async def get_my_mentorship(
    as_mentor: bool = False,
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get my current mentorship"""
    service = MentorshipService(db)
    mentorship = await service.get_player_mentorship(current_user["_id"], as_mentor=as_mentor)

    if not mentorship:
        role = "mentor" if as_mentor else "apprentice"
        raise HTTPException(status_code=404, detail=f"Not a {role}")

    return mentorship


@router.post("/graduate", response_model=dict)
async def graduate_apprentice(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Graduate apprentice (they reached level 50)"""
    service = MentorshipService(db)

    # Get mentorship where current user is apprentice
    mentorship = await service.get_player_mentorship(current_user["_id"], as_mentor=False)
    if not mentorship:
        raise HTTPException(status_code=400, detail="Not an apprentice")

    try:
        success = await service.graduate_apprentice(mentorship.get("id"))
        return {"success": success, "message": "Graduated! Congratulations!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/lesson/complete", response_model=dict)
async def complete_lesson(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Complete a lesson (as apprentice)"""
    service = MentorshipService(db)

    mentorship = await service.get_player_mentorship(current_user["_id"], as_mentor=False)
    if not mentorship:
        raise HTTPException(status_code=400, detail="Not an apprentice")

    try:
        success = await service.complete_lesson(mentorship.get("id"))
        return {"success": success, "message": "Lesson completed! XP and rewards granted."}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/mentors", response_model=list)
async def list_available_mentors(
    skip: int = 0,
    limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """List available mentors (level 50+)"""
    service = MentorshipService(db)
    mentors = await service.list_mentors(skip=skip, limit=limit)
    return mentors
