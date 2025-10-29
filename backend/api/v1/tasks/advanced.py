"""Advanced tasks API router."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from pydantic import BaseModel

from backend.core.database import get_database
from backend.core.security import decode_access_token
from backend.services.tasks.combat_task_generator import CombatTaskGenerator
from backend.services.tasks.economic_task_generator import EconomicTaskGenerator
from backend.services.tasks.relationship_task_generator import RelationshipTaskGenerator
from backend.services.tasks.guild_task_generator import GuildTaskGenerator
from backend.services.tasks.ethical_dilemma_generator import EthicalDilemmaGenerator
from backend.services.tasks.difficulty_scaler import DifficultyScaler
from backend.services.tasks.skill_requirement_validator import SkillRequirementValidator
from backend.models.tasks.task_types import TaskType

router = APIRouter(prefix="/advanced-tasks", tags=["advanced-tasks"])
security = HTTPBearer()

class GenerateTaskRequest(BaseModel):
    """Request to generate specific task type."""
    task_type: TaskType
    count: int = 1

class SkillCheckRequest(BaseModel):
    """Request to check skill requirements."""
    skill_requirements: List[dict]

@router.post("/generate")
async def generate_advanced_tasks(
    request: GenerateTaskRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Generate advanced tasks of specific type."""
    # Decode token
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    # Get player data
    player_dict = await db.players.find_one({"_id": player_id})
    if not player_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    player_level = player_dict.get("level", 1)
    player_traits = player_dict.get("traits", {})
    player_credits = player_dict.get("currencies", {}).get("credits", 1000)
    
    # Generate tasks based on type
    tasks = []
    for _ in range(request.count):
        if request.task_type == TaskType.COMBAT:
            generator = CombatTaskGenerator()
            task = generator.generate_combat_task(player_level, player_traits)
        elif request.task_type == TaskType.ECONOMIC:
            generator = EconomicTaskGenerator()
            task = generator.generate_economic_task(player_level, player_credits, player_traits)
        elif request.task_type == TaskType.RELATIONSHIP:
            generator = RelationshipTaskGenerator()
            task = generator.generate_relationship_task(player_level, player_traits)
        elif request.task_type == TaskType.GUILD:
            generator = GuildTaskGenerator()
            is_guild_member = player_dict.get("guild_id") is not None
            task = generator.generate_guild_task(player_level, player_traits, is_guild_member)
        elif request.task_type == TaskType.ETHICAL_DILEMMA:
            generator = EthicalDilemmaGenerator()
            task = generator.generate_ethical_dilemma(player_level, player_traits)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Task type {request.task_type} not supported yet"
            )
        
        tasks.append(task)
    
    return {"tasks": tasks}

@router.get("/difficulty/appropriate")
async def get_appropriate_difficulties(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get appropriate task difficulties for player."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    player_dict = await db.players.find_one({"_id": player_id})
    if not player_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    scaler = DifficultyScaler()
    player_level = player_dict.get("level", 1)
    
    appropriate = scaler.get_appropriate_difficulties(player_level)
    suggested = scaler.suggest_difficulty(player_dict)
    
    return {
        "appropriate_difficulties": [d.value for d in appropriate],
        "suggested_difficulty": suggested
    }

@router.post("/skills/validate")
async def validate_skill_requirements(
    request: SkillCheckRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Validate if player meets skill requirements."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    player_dict = await db.players.find_one({"_id": player_id})
    if not player_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    validator = SkillRequirementValidator()
    player_traits = player_dict.get("traits", {})
    
    meets_requirements, missing_skills = validator.validate_skill_requirements(
        player_traits,
        request.skill_requirements
    )
    
    return {
        "meets_requirements": meets_requirements,
        "missing_skills": missing_skills
    }

@router.get("/skills/levels")
async def get_player_skill_levels(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get player's skill levels across all categories."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    player_dict = await db.players.find_one({"_id": player_id})
    if not player_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    validator = SkillRequirementValidator()
    player_traits = player_dict.get("traits", {})
    
    # Calculate levels for all skill categories
    skill_levels = {}
    for skill_name in validator.TRAIT_TO_SKILL_MAP.keys():
        skill_levels[skill_name] = round(validator.get_skill_level(player_traits, skill_name), 1)
    
    return {"skill_levels": skill_levels}
