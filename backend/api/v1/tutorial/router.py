"""Tutorial routes for player onboarding."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from backend.tutorial.tutorial import TutorialManager
from backend.api.deps import get_current_player, get_database

router = APIRouter(prefix="/tutorial", tags=["tutorial"])


class CompleteStepRequest(BaseModel):
    step_id: str


class SkipStepRequest(BaseModel):
    step_id: str


@router.post("/start", response_model=Dict[str, Any])
async def start_tutorial(
    player = Depends(get_current_player),
    db = Depends(get_database)
):
    """Start the tutorial for a new player."""
    manager = TutorialManager(player['_id'], db)

    # Check if tutorial already started
    progress = await manager.get_progress()
    if progress['status'] != 'not_started':
        raise HTTPException(status_code=400, detail="Tutorial already started")

    return await manager.start_tutorial()


@router.get("/progress", response_model=Dict[str, Any])
async def get_tutorial_progress(
    player = Depends(get_current_player),
    db = Depends(get_database)
):
    """Get player's tutorial progress."""
    manager = TutorialManager(player['_id'], db)
    return await manager.get_progress()


@router.get("/current", response_model=Dict[str, Any])
async def get_current_step(
    player = Depends(get_current_player),
    db = Depends(get_database)
):
    """Get the current tutorial step."""
    manager = TutorialManager(player['_id'], db)
    step = await manager.get_current_step()

    if not step:
        raise HTTPException(status_code=404, detail="No active tutorial step")

    return step


@router.post("/complete", response_model=Dict[str, Any])
async def complete_step(
    request: CompleteStepRequest,
    player = Depends(get_current_player),
    db = Depends(get_database)
):
    """Complete a tutorial step."""
    manager = TutorialManager(player['_id'], db)

    try:
        result = await manager.complete_step(request.step_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/skip", response_model=Dict[str, Any])
async def skip_step(
    request: SkipStepRequest,
    player = Depends(get_current_player),
    db = Depends(get_database)
):
    """Skip a tutorial step."""
    manager = TutorialManager(player['_id'], db)

    try:
        result = await manager.skip_step(request.step_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/skip-all", response_model=Dict[str, Any])
async def skip_tutorial(
    player = Depends(get_current_player),
    db = Depends(get_database)
):
    """Skip the entire tutorial."""
    manager = TutorialManager(player['_id'], db)
    return await manager.skip_tutorial()


@router.post("/reset", response_model=Dict[str, Any])
async def reset_tutorial(
    player = Depends(get_current_player),
    db = Depends(get_database)
):
    """Reset tutorial progress (for testing or replay)."""
    manager = TutorialManager(player['_id'], db)
    return await manager.reset_tutorial()
