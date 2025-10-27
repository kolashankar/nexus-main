from fastapi import APIRouter, Depends, HTTPException
from ....services.actions.handler import ActionHandler
from ....api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()

class DonateRequest(BaseModel):
    target_id: str
    amount: int

@router.post("/donate")
async def donate_to_player(
    request: DonateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Donate credits to another player"""
    handler = ActionHandler()

    try:
        result = await handler.execute_action(
            action_type="donate",
            actor_id=current_user["_id"],
            target_id=request.target_id,
            params={"amount": request.amount}
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Action failed: {str(e)}")
