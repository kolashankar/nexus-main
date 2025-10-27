from fastapi import APIRouter, Depends, HTTPException
from ....services.actions.handler import ActionHandler
from ....api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

class HelpRequest(BaseModel):
    target_id: str

@router.post("/help")
async def help_player(
    request: HelpRequest,
    current_user: dict = Depends(get_current_user)
):
    """Help another player"""
    handler = ActionHandler()

    try:
        result = await handler.execute_action(
            action_type="help",
            actor_id=current_user["_id"],
            target_id=request.target_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Action failed: {str(e)}")
