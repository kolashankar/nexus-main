from datetime import datetime
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.social.relationship import Relationship, RelationshipType


class RelationshipService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.relationships = db.relationships
        self.players = db.players

    async def create_relationship(
        self,
        type: RelationshipType,
        player1_id: str,
        player2_id: str,
        metadata: dict = None
    ) -> Relationship:
        """Create a new relationship"""
        if player1_id == player2_id:
            raise ValueError("Cannot create relationship with yourself")

        # Check if relationship already exists
        existing = await self.relationships.find_one({
            "type": type.value,
            "$or": [
                {"player1_id": player1_id, "player2_id": player2_id},
                {"player1_id": player2_id, "player2_id": player1_id}
            ],
            "active": True
        })

        if existing:
            raise ValueError(f"{type.value} relationship already exists")

        relationship = Relationship(
            type=type,
            player1_id=player1_id,
            player2_id=player2_id,
            metadata=metadata or {}
        )

        await self.relationships.insert_one(relationship.model_dump())
        return relationship

    async def end_relationship(self, relationship_id: str) -> bool:
        """End a relationship"""
        await self.relationships.update_one(
            {"id": relationship_id},
            {
                "$set": {
                    "active": False,
                    "ended_at": datetime.utcnow()
                }
            }
        )
        return True

    async def get_relationship(self, relationship_id: str) -> Optional[dict]:
        """Get relationship by ID"""
        return await self.relationships.find_one({"id": relationship_id})

    async def get_player_relationships(
        self,
        player_id: str,
        type: Optional[RelationshipType] = None,
        active_only: bool = True
    ) -> List[dict]:
        """Get all relationships for a player"""
        query = {
            "$or": [
                {"player1_id": player_id},
                {"player2_id": player_id}
            ]
        }

        if type:
            query["type"] = type.value

        if active_only:
            query["active"] = True

        cursor = self.relationships.find(query)
        return await cursor.to_list(length=100)

    async def are_related(
        self,
        player1_id: str,
        player2_id: str,
        type: Optional[RelationshipType] = None
    ) -> bool:
        """Check if two players are related"""
        query = {
            "$or": [
                {"player1_id": player1_id, "player2_id": player2_id},
                {"player1_id": player2_id, "player2_id": player1_id}
            ],
            "active": True
        }

        if type:
            query["type"] = type.value

        result = await self.relationships.find_one(query)
        return result is not None
