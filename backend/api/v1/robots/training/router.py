"""Robot training routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user
from backend.services.robots.training import RobotTrainingService
from .schemas import StartTrainingRequest, TrainingStatusResponse

router = APIRouter(prefix="/training", tags=["robots", "training"])
training_service = RobotTrainingService()


@router.post("/start")
async def start_training(
    request: StartTrainingRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Start training a robot."""
    try:
        result = await training_service.start_training(
            robot_id=request.robot_id,
            owner_id=current_user["_id"],
            training_type=request.training_type,
            duration_hours=request.duration_hours
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{robot_id}/status", response_model=TrainingStatusResponse)
async def get_training_status(
    robot_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get training status for a robot."""
    try:
        status = await training_service.get_training_status(robot_id)
        return status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/{robot_id}/complete")
async def complete_training(
    robot_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Complete training and claim rewards."""
    try:
        result = await training_service.complete_training(
            robot_id=robot_id,
            owner_id=current_user["_id"]
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/types")
async def get_training_types():
    """Get available training types."""
    return training_service.get_training_types()
