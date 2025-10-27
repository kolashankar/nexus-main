"""Territory Manager"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...models.world.territory import TerritoryModel, TerritoryEvent

logger = logging.getLogger(__name__)


class TerritoryManager:
    """
    Manages territories and regional state
    Used for regional events and guild control
    """

    TOTAL_TERRITORIES = 20

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.territories
        logger.info("TerritoryManager initialized")

    async def get_territory(self, territory_id: int) -> Optional[TerritoryModel]:
        """
        Get territory by ID
        
        Args:
            territory_id: Territory ID (1-20)
        
        Returns:
            TerritoryModel or None
        """
        territory_doc = await self.collection.find_one({"territory_id": territory_id})

        if not territory_doc:
            return None

        territory_doc.pop("_id", None)
        return TerritoryModel(**territory_doc)

    async def get_all_territories(self) -> List[TerritoryModel]:
        """
        Get all territories
        
        Returns:
            List of all territories
        """
        cursor = self.collection.find().sort("territory_id", 1)

        territories = []
        async for doc in cursor:
            doc.pop("_id", None)
            territories.append(TerritoryModel(**doc))

        return territories

    async def get_contested_territories(self) -> List[TerritoryModel]:
        """
        Get all contested territories
        
        Returns:
            List of contested territories
        """
        cursor = self.collection.find({"contested": True})

        territories = []
        async for doc in cursor:
            doc.pop("_id", None)
            territories.append(TerritoryModel(**doc))

        return territories

    async def get_guild_territories(self, guild_id: str) -> List[TerritoryModel]:
        """
        Get territories controlled by a guild
        
        Args:
            guild_id: Guild ID
        
        Returns:
            List of controlled territories
        """
        cursor = self.collection.find({"controlling_guild_id": guild_id})

        territories = []
        async for doc in cursor:
            doc.pop("_id", None)
            territories.append(TerritoryModel(**doc))

        return territories

    async def update_territory(
        self,
        territory_id: int,
        updates: Dict[str, Any]
    ) -> TerritoryModel:
        """
        Update territory data
        
        Args:
            territory_id: Territory ID
            updates: Fields to update
        
        Returns:
            Updated territory
        """
        updates["last_updated"] = datetime.utcnow()

        await self.collection.update_one(
            {"territory_id": territory_id},
            {"$set": updates}
        )

        return await self.get_territory(territory_id)

    async def add_regional_event(
        self,
        territory_id: int,
        event_id: str,
        event_type: str,
        name: str,
        duration_hours: float
    ) -> None:
        """
        Add a regional event to territory
        
        Args:
            territory_id: Territory ID
            event_id: Event ID
            event_type: Event type
            name: Event name
            duration_hours: Event duration
        """
        event = TerritoryEvent(
            event_id=event_id,
            event_type=event_type,
            name=name,
            started_at=datetime.utcnow(),
            ends_at=datetime.utcnow() + timedelta(hours=duration_hours),
            is_active=True
        )

        await self.collection.update_one(
            {"territory_id": territory_id},
            {
                "$push": {"active_events": event.dict()},
                "$set": {
                    "last_event_type": event_type,
                    "last_event_time": datetime.utcnow()
                }
            }
        )

        logger.info(f"Regional event {name} added to territory {territory_id}")

    async def get_territory_state(self, territory_id: int) -> Dict[str, Any]:
        """
        Get territory state for event generation
        
        Args:
            territory_id: Territory ID
        
        Returns:
            Dictionary with territory state data
        """
        territory = await self.get_territory(territory_id)

        if not territory:
            return {}

        return {
            "territory_id": territory.territory_id,
            "name": territory.name,
            "controlling_guild_id": territory.controlling_guild_id,
            "guild_name": territory.controlling_guild_name,
            "contested": territory.contested,
            "population": territory.total_residents,
            "local_karma": territory.local_karma,
            "prosperity_level": territory.prosperity_level,
            "conflict_level": territory.conflict_level,
            "resources": territory.resources
        }

    async def sync_territory_population(self, territory_id: int) -> int:
        """
        Sync territory population from player data
        
        Args:
            territory_id: Territory ID
        
        Returns:
            Updated population count
        """
        # Count players who have this territory as home
        population = await self.db.players.count_documents({
            "location.territory_id": territory_id
        })

        # Count online players in territory
        online = await self.db.players.count_documents({
            "location.territory_id": territory_id,
            "online": True
        })

        await self.update_territory(territory_id, {
            "total_residents": population,
            "online_players": online
        })

        return population

    async def calculate_local_karma(self, territory_id: int) -> float:
        """
        Calculate combined karma of territory residents
        
        Args:
            territory_id: Territory ID
        
        Returns:
            Local karma sum
        """
        pipeline = [
            {"$match": {"location.territory_id": territory_id}},
            {"$group": {
                "_id": None,
                "total_karma": {"$sum": "$karma_points"},
                "avg_karma": {"$avg": "$karma_points"}
            }}
        ]

        result = await self.db.players.aggregate(pipeline).to_list(1)

        if result:
            local_karma = result[0].get("total_karma", 0.0)
            avg_karma = result[0].get("avg_karma", 0.0)

            await self.update_territory(territory_id, {
                "local_karma": local_karma,
                "average_karma": avg_karma
            })

            return local_karma

        return 0.0

    async def initialize_territories(self) -> int:
        """
        Initialize all 20 territories if they don't exist
        
        Returns:
            Number of territories created
        """
        existing_count = await self.collection.count_documents({})

        if existing_count >= self.TOTAL_TERRITORIES:
            logger.info(
                f"Territories already initialized ({existing_count} exist)")
            return 0

        territories_data = [
            {"id": 1, "name": "Silicon Valley", "region": "west"},
            {"id": 2, "name": "Cyber Tokyo", "region": "east"},
            {"id": 3, "name": "Neural London", "region": "west"},
            {"id": 4, "name": "Code Moscow", "region": "east"},
            {"id": 5, "name": "Data Dubai", "region": "central"},
            {"id": 6, "name": "Quantum Beijing", "region": "east"},
            {"id": 7, "name": "Binary Berlin", "region": "west"},
            {"id": 8, "name": "Tech Seoul", "region": "east"},
            {"id": 9, "name": "Cloud Mumbai", "region": "central"},
            {"id": 10, "name": "Matrix Paris", "region": "west"},
            {"id": 11, "name": "Grid Sydney", "region": "south"},
            {"id": 12, "name": "Byte Toronto", "region": "north"},
            {"id": 13, "name": "Nano Bangalore", "region": "central"},
            {"id": 14, "name": "Pixel Cairo", "region": "central"},
            {"id": 15, "name": "Logic Lagos", "region": "central"},
            {"id": 16, "name": "Circuit Mexico City", "region": "north"},
            {"id": 17, "name": "Algorithm Amsterdam", "region": "west"},
            {"id": 18, "name": "System Singapore", "region": "east"},
            {"id": 19, "name": "Network New York", "region": "north"},
            {"id": 20, "name": "Virtual Sau Paulo", "region": "south"}
        ]

        created = 0
        for data in territories_data:
            # Check if exists
            existing = await self.collection.find_one({"territory_id": data["id"]})
            if existing:
                continue

            territory = TerritoryModel(
                territory_id=data["id"],
                name=data["name"],
                description=f"A major technological hub in the {data['region']}ern region.",
                region=data["region"]
            )

            await self.collection.insert_one(territory.dict())
            created += 1

        logger.info(f"Initialized {created} new territories")
        return created
