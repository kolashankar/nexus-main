"""Multiplayer tasks API router."""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from backend.core.database import get_database
from backend.core.security import decode_access_token
from backend.services.tasks.coop_task_generator import CoopTaskGenerator
from backend.services.tasks.competitive_task_generator import CompetitiveTaskGenerator
from backend.services.tasks.pvp_moral_task_generator import PvPMoralTaskGenerator

router = APIRouter(prefix="/multiplayer", tags=["multiplayer-tasks"])
security = HTTPBearer()

class CreateCoopTaskRequest(BaseModel):
    """Request to create co-op task."""
    scenario_type: Optional[str] = None

class JoinCoopTaskRequest(BaseModel):
    """Request to join co-op task."""
    task_id: str
    selected_role: str

class CreateCompetitiveTaskRequest(BaseModel):
    """Request to create competitive task."""
    category: Optional[str] = None

class AcceptChallengeRequest(BaseModel):
    """Request to accept competitive challenge."""
    task_id: str

class CompletePvPMoralTaskRequest(BaseModel):
    """Request to complete PvP moral task."""
    task_id: str
    choice_index: int

# ============ CO-OP TASKS ============

@router.post("/coop/create")
async def create_coop_task(
    request: CreateCoopTaskRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a new co-op task."""
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
    
    # Generate co-op task
    generator = CoopTaskGenerator()
    task = generator.generate_coop_task(
        player_level=player_dict.get("level", 1),
        player_traits=player_dict.get("traits", {})
    )
    
    # Add creator info
    task["creator_id"] = player_id
    task["creator_name"] = player_dict.get("username", "Unknown")
    
    # Save to database
    await db.multiplayer_tasks.insert_one(task)
    
    return {
        "success": True,
        "task": task,
        "message": "Co-op task created! Now looking for partners."
    }

@router.get("/coop/available")
async def get_available_coop_tasks(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get list of available co-op tasks looking for partners."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    # Find co-op tasks looking for partners (not created by this player)
    tasks = await db.multiplayer_tasks.find({
        "type": "coop",
        "status": "looking_for_partners",
        "creator_id": {"$ne": player_id},
        "expires_at": {"$gt": datetime.now()}
    }).to_list(length=50)
    
    return {
        "success": True,
        "tasks": tasks,
        "count": len(tasks)
    }

@router.post("/coop/join")
async def join_coop_task(
    request: JoinCoopTaskRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Join an existing co-op task."""
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
    
    # Get task
    task = await db.multiplayer_tasks.find_one({"task_id": request.task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Join task
    generator = CoopTaskGenerator()
    try:
        updated_task = generator.join_coop_task(
            task=task,
            player_id=player_id,
            player_name=player_dict.get("username", "Unknown"),
            selected_role=request.selected_role
        )
        
        # Update in database
        await db.multiplayer_tasks.update_one(
            {"task_id": request.task_id},
            {"$set": {"partners_joined": updated_task["partners_joined"], "status": updated_task["status"]}}
        )
        
        return {
            "success": True,
            "task": updated_task,
            "message": "Successfully joined co-op task!"
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ============ COMPETITIVE TASKS ============

@router.post("/competitive/create")
async def create_competitive_task(
    request: CreateCompetitiveTaskRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Create a competitive challenge."""
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
    
    # Generate competitive task
    generator = CompetitiveTaskGenerator()
    task = generator.generate_competitive_task(
        player_level=player_dict.get("level", 1),
        player_traits=player_dict.get("traits", {})
    )
    
    # Add creator info
    task["creator_id"] = player_id
    task["creator_name"] = player_dict.get("username", "Unknown")
    
    # Save to database
    await db.multiplayer_tasks.insert_one(task)
    
    return {
        "success": True,
        "task": task,
        "message": "Competitive challenge created! Looking for opponent."
    }

@router.get("/competitive/challenges")
async def get_competitive_challenges(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get list of competitive challenges."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    player_dict = await db.players.find_one({"_id": player_id})
    
    # Find challenges looking for opponent (not created by this player)
    challenges = await db.multiplayer_tasks.find({
        "type": "competitive",
        "status": "looking_for_opponent",
        "creator_id": {"$ne": player_id},
        "expires_at": {"$gt": datetime.now()}
    }).to_list(length=50)
    
    # Filter by player's skill level (show appropriate challenges)
    player_level = player_dict.get("level", 1)
    suitable_challenges = [
        c for c in challenges
        if abs(c.get("creator_level", 1) - player_level) <= 10  # Within 10 levels
    ]
    
    return {
        "success": True,
        "challenges": suitable_challenges,
        "count": len(suitable_challenges)
    }

@router.post("/competitive/accept")
async def accept_competitive_challenge(
    request: AcceptChallengeRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Accept a competitive challenge."""
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
    
    # Get task
    task = await db.multiplayer_tasks.find_one({"task_id": request.task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    # Match opponent
    generator = CompetitiveTaskGenerator()
    try:
        updated_task = generator.match_opponent(
            task=task,
            opponent_id=player_id,
            opponent_name=player_dict.get("username", "Unknown"),
            opponent_level=player_dict.get("level", 1),
            opponent_traits=player_dict.get("traits", {})
        )
        
        # Update in database
        await db.multiplayer_tasks.update_one(
            {"task_id": request.task_id},
            {"$set": {"opponent": updated_task["opponent"], "status": updated_task["status"]}}
        )
        
        return {
            "success": True,
            "task": updated_task,
            "message": "Challenge accepted! Prepare for battle."
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# ============ PVP MORAL TASKS ============

@router.get("/pvp-moral/pending")
async def get_pending_pvp_moral_tasks(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get PvP moral tasks where player must make a choice."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    # Find pending PvP moral tasks for this player
    tasks = await db.multiplayer_tasks.find({
        "type": "pvp_moral",
        "player_id": player_id,
        "status": "pending_choice",
        "expires_at": {"$gt": datetime.now()}
    }).to_list(length=20)
    
    return {
        "success": True,
        "tasks": tasks,
        "count": len(tasks)
    }

@router.post("/pvp-moral/complete")
async def complete_pvp_moral_task(
    request: CompletePvPMoralTaskRequest,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Complete a PvP moral task by making a choice."""
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
    
    # Get task
    task = await db.multiplayer_tasks.find_one({"task_id": request.task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    if task["player_id"] != player_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not your task"
        )
    
    # Complete task
    generator = PvPMoralTaskGenerator()
    try:
        result = generator.complete_pvp_moral_task(
            task=task,
            choice_index=request.choice_index,
            player_id=player_id,
            player_name=player_dict.get("username", "Unknown")
        )
        
        # Update player's traits and rewards
        player_effects = result["player_effects"]["effects"]
        if "traits" in player_effects:
            for trait, change in player_effects["traits"].items():
                current_value = player_dict.get("traits", {}).get(trait, 50)
                new_value = max(0, min(100, current_value + change))
                await db.players.update_one(
                    {"_id": player_id},
                    {"$set": {f"traits.{trait}": new_value}}
                )
        
        # Apply other rewards
        if "xp" in player_effects:
            await db.players.update_one(
                {"_id": player_id},
                {"$inc": {"xp": player_effects["xp"]}}
            )
        if "credits" in player_effects:
            await db.players.update_one(
                {"_id": player_id},
                {"$inc": {"currencies.credits": player_effects["credits"]}}
            )
        if "karma" in player_effects:
            await db.players.update_one(
                {"_id": player_id},
                {"$inc": {"karma": player_effects["karma"]}}
            )
        
        # Apply effects to target player
        target_effects = result["target_player_effects"]["effects"]
        target_id = result["target_player_effects"]["player_id"]
        
        if "credits" in target_effects:
            await db.players.update_one(
                {"_id": target_id},
                {"$inc": {"currencies.credits": target_effects["credits"]}}
            )
        if "karma" in target_effects:
            await db.players.update_one(
                {"_id": target_id},
                {"$inc": {"karma": target_effects["karma"]}}
            )
        
        # Send notification to target player
        notification = {
            "_id": f"notif_{datetime.now().strftime('%Y%m%d%H%M%S')}_{player_id[:8]}",
            "player_id": target_id,
            "type": "pvp_moral_task_effect",
            "message": target_effects.get("message", "You've been affected by another player's choice."),
            "effects": target_effects,
            "from_player": player_dict.get("username", "Unknown"),
            "created_at": datetime.now(),
            "read": False
        }
        await db.notifications.insert_one(notification)
        
        # Mark task as completed
        await db.multiplayer_tasks.update_one(
            {"task_id": request.task_id},
            {"$set": {"status": "completed", "chosen_index": request.choice_index, "choice_made_at": datetime.now()}}
        )
        
        return {
            "success": True,
            "result": result,
            "message": "Choice made. Both players have been affected."
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
