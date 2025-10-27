from datetime import datetime
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.guilds.war import GuildWar, WarStatus


class GuildWarService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.wars = db.guild_wars
        self.guilds = db.guilds

    async def declare_war(self, attacker_guild_id: str, defender_guild_id: str, target_territory: Optional[int] = None) -> GuildWar:
        """Declare war on another guild"""
        if attacker_guild_id == defender_guild_id:
            raise ValueError("Cannot declare war on yourself")

        # Check if already at war
        existing = await self.wars.find_one({
            "$or": [
                {"attacker_guild_id": attacker_guild_id,
                    "defender_guild_id": defender_guild_id, "status": "active"},
                {"attacker_guild_id": defender_guild_id,
                    "defender_guild_id": attacker_guild_id, "status": "active"}
            ]
        })

        if existing:
            raise ValueError("Already at war with this guild")

        # Create war
        war = GuildWar(
            attacker_guild_id=attacker_guild_id,
            defender_guild_id=defender_guild_id,
            target_territory=target_territory
        )

        await self.wars.insert_one(war.model_dump())

        # Add to both guilds' active wars
        war_ref = {
            "war_id": war.id,
            "enemy_guild_id": defender_guild_id,
            "started_at": war.started_at,
            "war_points": 0,
            "status": "active"
        }

        await self.guilds.update_one(
            {"id": attacker_guild_id},
            {"$push": {"active_wars": war_ref}}
        )

        war_ref["enemy_guild_id"] = attacker_guild_id
        await self.guilds.update_one(
            {"id": defender_guild_id},
            {"$push": {"active_wars": war_ref}}
        )

        return war

    async def add_war_points(self, war_id: str, guild_id: str, points: int) -> bool:
        """Add war points to a guild"""
        war = await self.wars.find_one({"id": war_id})
        if not war:
            raise ValueError("War not found")

        if war.get("attacker_guild_id") == guild_id:
            await self.wars.update_one(
                {"id": war_id},
                {"$inc": {"attacker_points": points}}
            )
        elif war.get("defender_guild_id") == guild_id:
            await self.wars.update_one(
                {"id": war_id},
                {"$inc": {"defender_points": points}}
            )
        else:
            raise ValueError("Guild not part of this war")

        # Check if war should end (first to 1000 points wins)
        updated_war = await self.wars.find_one({"id": war_id})
        if updated_war.get("attacker_points", 0) >= 1000:
            await self.end_war(war_id, updated_war.get("attacker_guild_id"))
        elif updated_war.get("defender_points", 0) >= 1000:
            await self.end_war(war_id, updated_war.get("defender_guild_id"))

        return True

    async def offer_peace(self, war_id: str, offering_guild_id: str, terms: dict) -> bool:
        """Offer peace treaty"""
        war = await self.wars.find_one({"id": war_id})
        if not war:
            raise ValueError("War not found")

        if war.get("status") != "active":
            raise ValueError("War is not active")

        await self.wars.update_one(
            {"id": war_id},
            {
                "$set": {
                    "status": WarStatus.PEACE_NEGOTIATION.value,
                    "peace_offer": terms,
                    "peace_offered_by": offering_guild_id
                }
            }
        )

        return True

    async def accept_peace(self, war_id: str, accepting_guild_id: str) -> bool:
        """Accept peace treaty"""
        war = await self.wars.find_one({"id": war_id})
        if not war:
            raise ValueError("War not found")

        if war.get("peace_offered_by") == accepting_guild_id:
            raise ValueError("Cannot accept your own peace offer")

        # End war peacefully
        await self.end_war(war_id, None)  # No winner

        return True

    async def reject_peace(self, war_id: str) -> bool:
        """Reject peace treaty"""
        await self.wars.update_one(
            {"id": war_id},
            {
                "$set": {
                    "status": WarStatus.ACTIVE.value,
                    "peace_offer": None,
                    "peace_offered_by": None
                }
            }
        )
        return True

    async def end_war(self, war_id: str, winner_guild_id: Optional[str]) -> bool:
        """End a war"""
        war = await self.wars.find_one({"id": war_id})
        if not war:
            raise ValueError("War not found")

        # Update war
        await self.wars.update_one(
            {"id": war_id},
            {
                "$set": {
                    "status": WarStatus.ENDED.value,
                    "ended_at": datetime.utcnow(),
                    "winner_guild_id": winner_guild_id
                }
            }
        )

        # Remove from guilds' active wars
        await self.guilds.update_one(
            {"id": war.get("attacker_guild_id")},
            {"$pull": {"active_wars": {"war_id": war_id}}}
        )

        await self.guilds.update_one(
            {"id": war.get("defender_guild_id")},
            {"$pull": {"active_wars": {"war_id": war_id}}}
        )

        return True

    async def get_war(self, war_id: str) -> Optional[dict]:
        """Get war by ID"""
        return await self.wars.find_one({"id": war_id})

    async def get_guild_wars(self, guild_id: str) -> List[dict]:
        """Get all wars for a guild"""
        cursor = self.wars.find({
            "$or": [
                {"attacker_guild_id": guild_id},
                {"defender_guild_id": guild_id}
            ],
            "status": "active"
        })
        return await cursor.to_list(length=100)
