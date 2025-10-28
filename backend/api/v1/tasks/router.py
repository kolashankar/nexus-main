"""Tasks API Router"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from backend.core.database import get_database
from backend.api.deps import get_current_user
from backend.services.ai.task_generator import TaskGenerator
from backend.services.tasks.task_manager import TaskManager

router = APIRouter()

class TaskCompleteRequest(BaseModel):
    task_id: str

@router.post('/generate')
async def generate_task(
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Generate a new task for the player"""
    try:
        # Check if player already has active task
        task_manager = TaskManager(db)
        existing_task = await task_manager.get_current_task(current_user['_id'])
        
        if existing_task:
            return {
                'success': False,
                'error': 'You already have an active task',
                'current_task': existing_task
            }
        
        # Generate new task
        task_generator = TaskGenerator()
        task_data = await task_generator.generate_task(current_user)
        
        # Save task
        task = await task_manager.create_task(task_data)
        
        return {
            'success': True,
            'task': task
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/current')
async def get_current_task(
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Get player's current active task"""
    try:
        task_manager = TaskManager(db)
        task = await task_manager.get_current_task(current_user['_id'])
        
        if not task:
            return {'success': False, 'task': None}
        
        return {'success': True, 'task': task}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/complete')
async def complete_task(
    request: TaskCompleteRequest,
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """Complete a task"""
    try:
        task_manager = TaskManager(db)
        result = await task_manager.complete_task(request.task_id, current_user['_id'])
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
