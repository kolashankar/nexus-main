from pydantic import BaseModel, Field
from typing import List, Dict


class CreateGuildQuestRequest(BaseModel):
    title: str = Field(..., description="Quest title")
    description: str = Field(..., description="Quest description")
    objectives: List[Dict] = Field(..., description="Quest objectives")
    rewards: Dict = Field(..., description="Quest rewards")
    required_members: int = Field(
        default=5, ge=3, le=20, description="Required participants")
