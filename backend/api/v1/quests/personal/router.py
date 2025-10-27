"""Personal quests API routes."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

from backend.core.database import get_database
from backend.api.deps import get_current_user
from backend.services.quests.manager import QuestManager
from backend.api.v1.quests.schemas import QuestResponse

router = APIRouter()

@router.get("/", response_model=List[QuestResponse])
async def get_personal_quests(
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """Get personal quests for current player."""
    try:
        manager = QuestManager(db)
        quests = await manager.get_available_quests(
            player_id=current_user["_id"],
            quest_type="personal"
        )

        return {"quests": quests}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_personal_quest(
    db: AsyncIOMotorClient = Depends(get_database),
    current_user: dict = Depends(get_current_user)
):
    """Generate a new AI-powered personal quest."""
    try:
        from backend.services.ai.oracle.oracle import Oracle

        oracle = Oracle()
        quest_data = await oracle.generate_quest(
            player=current_user,
            quest_type="personal"
        )

        # Save quest to database
        quest_data["player_id"] = current_user["_id"]
        quest_data["quest_type"] = "personal"
        quest_data["generated_by"] = "oracle"

        result = await db.quests.insert_one(quest_data)
        quest_data["_id"] = str(result.inserted_id)

        return {"quest": quest_data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
