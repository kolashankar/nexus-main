from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class SkillNodeResponse(BaseModel):
    node_id: int
    unlocked: bool
    level: int

class SkillTreeResponse(BaseModel):
    trait_name: str
    total_points_invested: int
    active_branch: Optional[str] = None
    milestones_reached: List[int]
    synergy_bonuses: Dict[str, float]

class UnlockNodeRequest(BaseModel):
    trait_name: str = Field(..., description="Name of the trait")
    node_id: int = Field(..., ge=1, le=20,
                         description="Node ID to unlock (1-20)")

class ChooseBranchRequest(BaseModel):
    trait_name: str = Field(..., description="Name of the trait")
    branch: str = Field(..., pattern="^[AB]$",
                        description="Branch to choose (A or B)")

class SkillTreeSummary(BaseModel):
    total_points: int
    spent_points: int
    available_points: int
    trees_with_investment: int
    total_milestones: int
    branches_chosen: int
