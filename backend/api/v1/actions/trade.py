from fastapi import APIRouter, Depends, HTTPException
from ....services.actions.handler import ActionHandler
from ....api.deps import get_current_user
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class TradeRequest(BaseModel):
    target_id: str
    offer: Dict[str, Any]
    request: Dict[str, Any]

@router.post("/trade")
async def trade_with_player(
    request: TradeRequest,
    current_user: dict = Depends(get_current_user)
):
    """Initiate a trade with another player"""
    handler = ActionHandler()

    try:
        result = await handler.execute_action(
            action_type="trade",
            actor_id=current_user["_id"],
            target_id=request.target_id,
            params={
                "offer": request.offer,
                "request": request.request
            }
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Action failed: {str(e)}")
