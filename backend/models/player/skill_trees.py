from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class SkillNode(BaseModel):
    """Individual skill node in a tree"""
    node_id: int = Field(..., ge=1, le=20)
    unlocked: bool = False
    unlocked_at: Optional[datetime] = None
    level: int = Field(0, ge=0, le=5)

class SkillBranch(BaseModel):
    """Branching path in skill tree"""
    branch_type: str = Field(..., description="A or B branch")
    selected: bool = False
    selected_at: Optional[datetime] = None

class SkillTree(BaseModel):
    """Complete skill tree for a single trait"""
    trait_name: str
    total_points_invested: int = 0
    nodes: List[SkillNode] = Field(default_factory=list)
    active_branch: Optional[str] = None  # "A" or "B"
    branch_choice_made_at: Optional[datetime] = None
    milestones_reached: List[int] = Field(default_factory=list)
    synergy_bonuses: Dict[str, float] = Field(default_factory=dict)

    def unlock_node(self, node_id: int) -> bool:
        """Unlock a specific node"""
        for node in self.nodes:
            if node.node_id == node_id and not node.unlocked:
                node.unlocked = True
                node.unlocked_at = datetime.utcnow()
                self.total_points_invested += 1
                return True
        return False

    def choose_branch(self, branch: str) -> bool:
        """Choose between branch A or B"""
        if self.active_branch is None and branch in ["A", "B"]:
            self.active_branch = branch
            self.branch_choice_made_at = datetime.utcnow()
            return True
        return False

class PlayerSkillTrees(BaseModel):
    """All skill trees for a player"""
    player_id: str
    skill_trees: Dict[str, SkillTree] = Field(default_factory=dict)
    total_skill_points: int = 0
    total_points_spent: int = 0
    available_points: int = 0

    def add_skill_points(self, amount: int):
        """Add skill points from leveling up"""
        self.total_skill_points += amount
        self.available_points += amount

    def spend_skill_point(self, trait_name: str, node_id: int) -> bool:
        """Spend a skill point on a specific node"""
        if self.available_points <= 0:
            return False

        if trait_name not in self.skill_trees:
            return False

        if self.skill_trees[trait_name].unlock_node(node_id):
            self.available_points -= 1
            self.total_points_spent += 1
            return True
        return False
