from datetime import datetime
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.guilds.territory import Territory, TERRITORIES


class TerritoryService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.territories = db.territories
        self.guilds = db.guilds

    async def initialize_territories(self):
        """Initialize all 20 territories"""
        for territory_data in TERRITORIES:
            territory = Territory(**territory_data)
            existing = await self.territories.find_one({"territory_id": territory.territory_id})
            if not existing:
                await self.territories.insert_one(territory.model_dump())

    async def get_territory(self, territory_id: int) -> Optional[dict]:
        """Get territory by ID"""
        return await self.territories.find_one({"territory_id": territory_id})

    async def get_all_territories(self) -> List[dict]:
        """Get all territories"""
        cursor = self.territories.find({})
        return await cursor.to_list(length=20)

    async def get_guild_territories(self, guild_id: str) -> List[dict]:
        """Get all territories controlled by a guild"""
        cursor = self.territories.find({"controlling_guild_id": guild_id})
        return await cursor.to_list(length=20)

    async def capture_territory(self, territory_id: int, guild_id: str) -> bool:
        """Capture a territory"""
        territory = await self.territories.find_one({"territory_id": territory_id})
        if not territory:
            raise ValueError("Territory not found")

        # Check if already controlled
        if territory.get("controlling_guild_id") == guild_id:
            raise ValueError("Already controlling this territory")

        # Remove from previous controller
        old_controller = territory.get("controlling_guild_id")
        if old_controller:
            await self.guilds.update_one(
                {"id": old_controller},
                {"$pull": {"controlled_territories": territory_id}}
            )

        # Update territory
        await self.territories.update_one(
            {"territory_id": territory_id},
            {
                "$set": {
                    "controlling_guild_id": guild_id,
                    "controlled_since": datetime.utcnow(),
                    "contested": False,
                    "last_attacked": datetime.utcnow()
                }
            }
        )

        # Add to new controller
        await self.guilds.update_one(
            {"id": guild_id},
            {"$addToSet": {"controlled_territories": territory_id}}
        )

        return True

    async def attack_territory(self, territory_id: int, attacker_guild_id: str) -> dict:
        """Initiate territory attack"""
        territory = await self.territories.find_one({"territory_id": territory_id})
        if not territory:
            raise ValueError("Territory not found")

        defender_guild_id = territory.get("controlling_guild_id")
        if not defender_guild_id:
            # Unclaimed territory, capture directly
            await self.capture_territory(territory_id, attacker_guild_id)
            return {"success": True, "message": "Territory captured without resistance"}

        if defender_guild_id == attacker_guild_id:
            raise ValueError("Cannot attack your own territory")

        # Mark as contested
        await self.territories.update_one(
            {"territory_id": territory_id},
            {
                "$set": {
                    "contested": True,
                    "last_attacked": datetime.utcnow()
                }
            }
        )

        # Determine outcome (simplified - can be enhanced with more complex logic)
        attacker_guild = await self.guilds.find_one({"id": attacker_guild_id})
        defender_guild = await self.guilds.find_one({"id": defender_guild_id})

        attacker_power = attacker_guild.get(
            "level", 1) * attacker_guild.get("total_members", 1)
        defender_power = (defender_guild.get("level", 1) * defender_guild.get("total_members", 1) *
                         territory.get("defense_level", 1))

        if attacker_power > defender_power:
            await self.capture_territory(territory_id, attacker_guild_id)
            return {
                "success": True,
                "message": "Territory captured!",
                "attacker_power": attacker_power,
                "defender_power": defender_power
            }
        else:
            await self.territories.update_one(
                {"territory_id": territory_id},
                {"$set": {"contested": False}}
            )
            return {
                "success": False,
                "message": "Attack repelled!",
                "attacker_power": attacker_power,
                "defender_power": defender_power
            }

    async def defend_territory(self, territory_id: int, guild_id: str) -> bool:
        """Defend territory (upgrade defense)"""
        territory = await self.territories.find_one({"territory_id": territory_id})
        if not territory:
            raise ValueError("Territory not found")

        if territory.get("controlling_guild_id") != guild_id:
            raise ValueError("Not your territory")

        # Upgrade defense
        await self.territories.update_one(
            {"territory_id": territory_id},
            {"$inc": {"defense_level": 1}}
        )

        return True
