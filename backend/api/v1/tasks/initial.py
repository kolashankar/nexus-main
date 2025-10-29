"""Initial tasks API router."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

from backend.core.database import get_database
from backend.core.security import decode_access_token
from backend.services.tasks.initial_tasks_service import InitialTasksService
from backend.models.tasks.initial_task import InitialTask, TaskCompletion
from pydantic import BaseModel

router = APIRouter(prefix="/initial-tasks", tags=["initial-tasks"])
security = HTTPBearer()

class CompleteTaskRequest(BaseModel):
    """Request to complete a task."""
    task_id: str
    choice_index: int

@router.get("/", response_model=List[InitialTask])
async def get_initial_tasks(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get initial tasks for the authenticated player."""
    # Decode token
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    # Get tasks
    service = InitialTasksService()
    tasks = await service.get_initial_tasks(player_id, db, count=3)
    
    return tasks

@router.post("/complete", response_model=TaskCompletion)
async def complete_task(
    request: CompleteTaskRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Complete an initial task with a chosen action."""
    # Decode token
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    try:
        # Complete task
        service = InitialTasksService()
        completion = await service.complete_task(
            player_id,
            request.task_id,
            request.choice_index,
            db
        )
        
        return completion
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/progress")
async def get_task_progress(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get player's progress on initial tasks."""
    # Decode token
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    # Get progress
    service = InitialTasksService()
    progress = await service.get_player_progress(player_id, db)
    
    return progress
