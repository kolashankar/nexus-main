"""Task analytics API router."""

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.security import HTTPBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional

from backend.core.database import get_database
from backend.core.security import decode_access_token
from backend.services.tasks.task_history_manager import TaskHistoryManager
from backend.services.tasks.task_statistics_analyzer import TaskStatisticsAnalyzer
from backend.services.tasks.trait_evolution_tracker import TraitEvolutionTracker
from backend.services.tasks.task_achievement_manager import TaskAchievementManager

router = APIRouter(prefix="/analytics", tags=["task-analytics"])
security = HTTPBearer()

# ============ TASK HISTORY ============

@router.get("/history")
async def get_task_history(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    task_type: Optional[str] = None
):
    """Get player's task completion history."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    history_manager = TaskHistoryManager(db)
    history = await history_manager.get_player_history(
        player_id=player_id,
        limit=limit,
        skip=skip,
        task_type=task_type
    )
    
    return {
        "success": True,
        "history": history,
        "count": len(history)
    }

@router.get("/history/stats")
async def get_history_stats(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    period_days: int = Query(30, ge=1, le=365)
):
    """Get statistical summary of task history."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    history_manager = TaskHistoryManager(db)
    stats = await history_manager.get_history_stats(
        player_id=player_id,
        period_days=period_days
    )
    
    return {
        "success": True,
        "stats": stats
    }

@router.get("/history/streak")
async def get_task_streak(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get player's task completion streak."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    history_manager = TaskHistoryManager(db)
    streak = await history_manager.get_task_streak(player_id=player_id)
    
    return {
        "success": True,
        "streak": streak
    }

# ============ CHOICE STATISTICS ============

@router.get("/statistics/choices")
async def get_choice_statistics(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    task_type: Optional[str] = None,
    days: int = Query(30, ge=1, le=365)
):
    """Get global choice statistics."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    analyzer = TaskStatisticsAnalyzer(db)
    
    # Try to get cached stats first
    cached = await analyzer.get_cached_statistics()
    if cached and not task_type:  # Use cache only for general queries
        return {
            "success": True,
            "statistics": cached["global_statistics"],
            "cached": True
        }
    
    # Get fresh statistics
    stats = await analyzer.get_global_choice_statistics(
        task_type=task_type,
        days=days
    )
    
    return {
        "success": True,
        "statistics": stats,
        "cached": False
    }

@router.get("/statistics/popular-tasks")
async def get_popular_tasks(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    days: int = Query(30, ge=1, le=365)
):
    """Get most popular tasks."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    analyzer = TaskStatisticsAnalyzer(db)
    popular = await analyzer.get_task_popularity(days=days)
    
    return {
        "success": True,
        "popular_tasks": popular
    }

@router.get("/statistics/comparison")
async def get_player_comparison(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    days: int = Query(30, ge=1, le=365)
):
    """Compare player to global averages."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    analyzer = TaskStatisticsAnalyzer(db)
    comparison = await analyzer.get_player_comparison(
        player_id=player_id,
        days=days
    )
    
    return {
        "success": True,
        "comparison": comparison
    }

# ============ TRAIT EVOLUTION ============

@router.get("/traits/evolution")
async def get_trait_evolution(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    trait_name: Optional[str] = None,
    days: int = Query(30, ge=1, le=365)
):
    """Get trait evolution data for charting."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    tracker = TraitEvolutionTracker(db)
    evolution = await tracker.get_trait_evolution(
        player_id=player_id,
        trait_name=trait_name,
        days=days
    )
    
    return {
        "success": True,
        "evolution": evolution
    }

@router.get("/traits/changes")
async def get_trait_changes_from_tasks(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    days: int = Query(30, ge=1, le=90)
):
    """Get trait changes from task completions."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    tracker = TraitEvolutionTracker(db)
    changes = await tracker.get_trait_changes_from_tasks(
        player_id=player_id,
        days=days
    )
    
    return {
        "success": True,
        "changes": changes,
        "count": len(changes)
    }

@router.get("/traits/velocity")
async def get_trait_velocity(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database),
    days: int = Query(7, ge=1, le=30)
):
    """Get trait velocity (rate of change)."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    tracker = TraitEvolutionTracker(db)
    velocities = await tracker.get_trait_velocity(
        player_id=player_id,
        days=days
    )
    
    return {
        "success": True,
        "velocities": velocities
    }

# ============ ACHIEVEMENTS ============

@router.get("/achievements")
async def get_achievements(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get player's achievements."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    achievement_manager = TaskAchievementManager(db)
    achievements = await achievement_manager.get_player_achievements(player_id=player_id)
    
    return {
        "success": True,
        "achievements": achievements
    }

@router.post("/achievements/check")
async def check_achievements(
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Check and award new achievements."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    achievement_manager = TaskAchievementManager(db)
    newly_earned = await achievement_manager.check_and_award_achievements(player_id=player_id)
    
    return {
        "success": True,
        "newly_earned": newly_earned,
        "count": len(newly_earned)
    }

@router.get("/achievements/{achievement_id}/progress")
async def get_achievement_progress(
    achievement_id: str,
    token: str = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get progress towards a specific achievement."""
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    player_id = payload.get("sub")
    
    achievement_manager = TaskAchievementManager(db)
    progress = await achievement_manager.get_achievement_progress(
        player_id=player_id,
        achievement_id=achievement_id
    )
    
    return {
        "success": True,
        "progress": progress
    }
