from fastapi import APIRouter, Depends, HTTPException
from ....services.actions.handler import ActionHandler
from ....api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

class HackRequest(BaseModel):
    target_id: str

@router.post("/hack")
async def hack_player(
    request: HackRequest,
    current_user: dict = Depends(get_current_user)
):
    """Hack another player"""
    handler = ActionHandler()

    try:
        result = await handler.execute_action(
            action_type="hack",
            actor_id=current_user["_id"],
            target_id=request.target_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Action failed: {str(e)}")
