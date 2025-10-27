from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.social.relationship import Alliance


class AllianceService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.alliances = db.alliances
        self.players = db.players

    async def create_alliance(self, creator_id: str, alliance_name: Optional[str] = None) -> Alliance:
        """Create a new alliance"""
        # Check if player already in an alliance
        existing = await self.alliances.find_one({
            "members": creator_id
        })

        if existing:
            raise ValueError("Already in an alliance")

        alliance = Alliance(
            members=[creator_id],
            alliance_name=alliance_name
        )

        await self.alliances.insert_one(alliance.model_dump())

        # Update player
        await self.players.update_one(
            {"_id": creator_id},
            {"$set": {"alliance_id": alliance.id}}
        )

        return alliance

    async def add_member(self, alliance_id: str, player_id: str) -> bool:
        """Add member to alliance"""
        alliance = await self.alliances.find_one({"id": alliance_id})
        if not alliance:
            raise ValueError("Alliance not found")

        # Check max members (3)
        if len(alliance.get("members", [])) >= 3:
            raise ValueError("Alliance is full (max 3 members)")

        # Check if player already in an alliance
        existing = await self.alliances.find_one({"members": player_id})
        if existing:
            raise ValueError("Player already in an alliance")

        # Add member
        await self.alliances.update_one(
            {"id": alliance_id},
            {"$push": {"members": player_id}}
        )

        # Update player
        await self.players.update_one(
            {"_id": player_id},
            {"$set": {"alliance_id": alliance_id}}
        )

        return True

    async def remove_member(self, alliance_id: str, player_id: str) -> bool:
        """Remove member from alliance"""
        alliance = await self.alliances.find_one({"id": alliance_id})
        if not alliance:
            raise ValueError("Alliance not found")

        # Remove member
        await self.alliances.update_one(
            {"id": alliance_id},
            {"$pull": {"members": player_id}}
        )

        # Update player
        await self.players.update_one(
            {"_id": player_id},
            {"$unset": {"alliance_id": ""}}
        )

        # Delete alliance if empty
        updated_alliance = await self.alliances.find_one({"id": alliance_id})
        if not updated_alliance.get("members"):
            await self.alliances.delete_one({"id": alliance_id})

        return True

    async def disband_alliance(self, alliance_id: str) -> bool:
        """Disband an alliance"""
        alliance = await self.alliances.find_one({"id": alliance_id})
        if not alliance:
            raise ValueError("Alliance not found")

        # Remove alliance from all members
        member_ids = alliance.get("members", [])
        await self.players.update_many(
            {"_id": {"$in": member_ids}},
            {"$unset": {"alliance_id": ""}}
        )

        # Delete alliance
        await self.alliances.delete_one({"id": alliance_id})

        return True

    async def get_alliance(self, alliance_id: str) -> Optional[dict]:
        """Get alliance by ID"""
        return await self.alliances.find_one({"id": alliance_id})

    async def get_player_alliance(self, player_id: str) -> Optional[dict]:
        """Get player's alliance"""
        return await self.alliances.find_one({"members": player_id})

    async def list_alliances(self, skip: int = 0, limit: int = 20) -> List[dict]:
        """List all alliances"""
        cursor = self.alliances.find({}).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
