from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from backend.models.player.skill_trees import PlayerSkillTrees
from backend.services.player.skill_trees import SkillTreeService
from backend.api.deps import get_current_player
from pydantic import BaseModel

router = APIRouter(prefix="/skill-trees", tags=["Skill Trees"])

class UnlockNodeRequest(BaseModel):
    trait_name: str
    node_id: int

class ChooseBranchRequest(BaseModel):
    trait_name: str
    branch: str

@router.get("/")
async def get_skill_trees(current_player: Dict = Depends(get_current_player)):
    """Get all skill trees for the current player"""
    player_id = current_player.get("_id")

    # Get or initialize skill trees
    skill_trees_data = current_player.get("skill_trees")
    if not skill_trees_data:
        skill_trees = SkillTreeService.initialize_skill_trees(str(player_id))
        return skill_trees.dict()

    return skill_trees_data

@router.get("/summary")
async def get_skill_tree_summary(current_player: Dict = Depends(get_current_player)):
    """Get skill tree summary"""
    skill_trees_data = current_player.get("skill_trees", {})

    if not skill_trees_data:
        return {"message": "No skill trees initialized"}

    skill_trees = PlayerSkillTrees(**skill_trees_data)
    summary = SkillTreeService.get_skill_tree_summary(skill_trees)

    return summary

@router.get("/{trait_name}")
async def get_skill_tree(
    trait_name: str,
    current_player: Dict = Depends(get_current_player)
):
    """Get a specific skill tree"""
    skill_trees_data = current_player.get("skill_trees")

    if not skill_trees_data:
        raise HTTPException(
            status_code=404, detail="Skill trees not initialized")

    skill_trees = PlayerSkillTrees(**skill_trees_data)

    if trait_name not in skill_trees.skill_trees:
        raise HTTPException(
            status_code=404, detail=f"Skill tree not found: {trait_name}")

    return skill_trees.skill_trees[trait_name].dict()

@router.post("/unlock-node")
async def unlock_node(
    request: UnlockNodeRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Unlock a skill node"""
    skill_trees_data = current_player.get("skill_trees")

    if not skill_trees_data:
        skill_trees = SkillTreeService.initialize_skill_trees(
            str(current_player["_id"]))
    else:
        skill_trees = PlayerSkillTrees(**skill_trees_data)

    success, message = SkillTreeService.unlock_node(
        skill_trees,
        request.trait_name,
        request.node_id
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    # Update player in database (would be done via service)
    return {
        "success": True,
        "message": message,
        "available_points": skill_trees.available_points,
        "skill_tree": skill_trees.skill_trees[request.trait_name].dict()
    }

@router.post("/choose-branch")
async def choose_branch(
    request: ChooseBranchRequest,
    current_player: Dict = Depends(get_current_player)
):
    """Choose a branch path (A or B)"""
    skill_trees_data = current_player.get("skill_trees")

    if not skill_trees_data:
        raise HTTPException(
            status_code=404, detail="Skill trees not initialized")

    skill_trees = PlayerSkillTrees(**skill_trees_data)

    success, message = SkillTreeService.choose_branch(
        skill_trees,
        request.trait_name,
        request.branch
    )

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {
        "success": True,
        "message": message,
        "skill_tree": skill_trees.skill_trees[request.trait_name].dict()
    }

@router.get("/synergies/calculate")
async def calculate_synergies(current_player: Dict = Depends(get_current_player)):
    """Calculate synergy bonuses"""
    skill_trees_data = current_player.get("skill_trees")
    player_traits = current_player.get("traits", {})

    if not skill_trees_data:
        return {"synergies": {}}

    skill_trees = PlayerSkillTrees(**skill_trees_data)
    synergies = SkillTreeService.calculate_synergy_bonuses(
        skill_trees, player_traits)

    return {"synergies": synergies}
