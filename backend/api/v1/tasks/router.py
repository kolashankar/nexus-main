"""Task API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from pydantic import BaseModel

from backend.core.database import get_database
from backend.core.security import get_current_user
from backend.services.ai.task_generator import TaskGeneratorService
from backend.services.tasks.task_manager import TaskManager
from backend.services.tasks.reward_distributor import RewardDistributor
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


class CompleteTaskRequest(BaseModel):
    """Request model for task completion"""
    task_id: str


@router.post("/generate")
async def generate_task(
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Generate a new AI-powered task for the current player.
    
    Returns:
        Task details including description and reward
    """
    try:
        player_id = current_user.get('player_id')
        
        # Check if player already has an active task
        task_manager = TaskManager(db)
        existing_task = await task_manager.get_current_task(player_id)
        
        if existing_task:
            return {
                "success": False,
                "error": "You already have an active task",
                "current_task": existing_task
            }
        
        # Prepare player data for task generation
        player_data = {
            "player_id": player_id,
            "username": current_user.get('username', 'Player'),
            "level": current_user.get('level', 1),
            "traits": current_user.get('traits', {})
        }
        
        # Generate task using AI
        task_generator = TaskGeneratorService()
        task = await task_generator.generate_task(player_data)
        
        # Save task to database
        await task_manager.save_task(task)
        
        return {
            "success": True,
            "task": task
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task generation failed: {str(e)}")


@router.get("/current")
async def get_current_task(
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get the current active task for the player.
    
    Returns:
        Current task or None
    """
    try:
        player_id = current_user.get('player_id')
        task_manager = TaskManager(db)
        task = await task_manager.get_current_task(player_id)
        
        return {
            "success": True,
            "task": task
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve task: {str(e)}")


@router.post("/complete")
async def complete_task(
    request: CompleteTaskRequest,
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Complete a task and receive rewards with ornament bonuses.
    
    Args:
        request: Task completion request
        
    Returns:
        Completion result with rewards
    """
    try:
        player_id = current_user.get('player_id')
        task_manager = TaskManager(db)
        reward_distributor = RewardDistributor(db)
        
        # Get the task
        task = await task_manager.get_current_task(player_id)
        
        if not task:
            raise HTTPException(status_code=404, detail="No active task found")
        
        if task['task_id'] != request.task_id:
            raise HTTPException(status_code=400, detail="Invalid task ID")
        
        # Calculate reward with bonuses
        base_reward = task['base_reward']
        reward_breakdown = await reward_distributor.calculate_reward(player_id, base_reward)
        
        total_reward = reward_breakdown['total_reward']
        
        # Mark task as completed
        await task_manager.complete_task(request.task_id, total_reward)
        
        # Distribute coins
        await reward_distributor.distribute_reward(player_id, total_reward)
        
        return {
            "success": True,
            "message": "Task completed successfully!",
            "reward_breakdown": reward_breakdown,
            "task_completed": task['description']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Task completion failed: {str(e)}")


@router.get("/history")
async def get_task_history(
    limit: int = 10,
    current_user: Dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    Get task completion history for the player.
    
    Args:
        limit: Maximum number of tasks to return
        
    Returns:
        List of completed tasks
    """
    try:
        player_id = current_user.get('player_id')
        task_manager = TaskManager(db)
        history = await task_manager.get_task_history(player_id, limit)
        
        return {
            "success": True,
            "history": history
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")
