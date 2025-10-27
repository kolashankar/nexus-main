"""Main robot routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from backend.api.deps import get_current_user
from backend.services.robots.factory import RobotFactory
from backend.services.robots.manager import RobotManager
from .schemas import PurchaseRobotRequest, RobotResponse

router = APIRouter(prefix="/robots", tags=["robots"])
robot_factory = RobotFactory()
robot_manager = RobotManager()


@router.get("/types", response_model=List[Dict[str, Any]])
async def get_robot_types():
    """Get all available robot types."""
    return robot_factory.get_all_robot_types()


@router.post("/purchase")
async def purchase_robot(
    request: PurchaseRobotRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Purchase a robot."""
    try:
        result = await robot_factory.create_robot(
            player_id=current_user["_id"],
            robot_type=request.robot_type,
            custom_name=request.custom_name
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


@router.get("/my-robots", response_model=List[RobotResponse])
async def get_my_robots(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all robots owned by the player."""
    try:
        robots = await robot_manager.get_player_robots(current_user["_id"])
        return robots
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{robot_id}", response_model=RobotResponse)
async def get_robot(
    robot_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get detailed information about a specific robot."""
    try:
        robot = await robot_manager.get_robot(robot_id)

        if not robot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Robot not found"
            )

        # Verify ownership
        if robot["owner_id"] != current_user["_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not your robot"
            )

        return robot
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/{robot_id}/name")
async def rename_robot(
    robot_id: str,
    new_name: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Rename a robot."""
    try:
        result = await robot_manager.rename_robot(
            robot_id=robot_id,
            owner_id=current_user["_id"],
            new_name=new_name
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


@router.delete("/{robot_id}")
async def delete_robot(
    robot_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Delete/scrap a robot."""
    try:
        result = await robot_manager.delete_robot(
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
