from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_database
from backend.services.social.relationships import RelationshipService
from backend.api.deps import get_current_user
from backend.models.social.relationship import RelationshipType
from typing import List, Optional

router = APIRouter()


@router.get("/nearby", response_model=List[dict])
async def get_nearby_players(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
    limit: int = 20
):
    """Get nearby online players"""
    # Get players in same location/territory
    cursor = db.players.find(
        {
            "_id": {"$ne": current_user["_id"]},
            "online": True
        },
        {"password_hash": 0}
    ).limit(limit)

    players = await cursor.to_list(length=limit)
    return players


@router.get("/online", response_model=List[dict])
async def get_online_players(
    db: AsyncIOMotorDatabase = Depends(get_database),
    skip: int = 0,
    limit: int = 20
):
    """Get all online players"""
    cursor = db.players.find(
        {"online": True},
        {"password_hash": 0}
    ).skip(skip).limit(limit)

    players = await cursor.to_list(length=limit)
    return players


@router.get("/relationships", response_model=List[dict])
async def get_my_relationships(
    current_user: dict = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
    type: Optional[str] = None
):
    """Get my relationships"""
    service = RelationshipService(db)

    relationship_type = None
    if type:
        try:
            relationship_type = RelationshipType(type)
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid relationship type")

    relationships = await service.get_player_relationships(
        player_id=current_user["_id"],
        type=relationship_type
    )

    return relationships


@router.get("/players/{player_id}", response_model=dict)
async def get_player_profile(
    player_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get public player profile"""
    player = await db.players.find_one(
        {"_id": player_id},
        {"password_hash": 0}
    )

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Respect privacy settings
    visibility = player.get("visibility", {})
    if visibility.get("privacy_tier") in ["ghost", "phantom"]:
        # Return minimal info
        return {
            "_id": player["_id"],
            "username": player.get("username", "Hidden")
        }

    return player
