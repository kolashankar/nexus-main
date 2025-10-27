"""Robot manager - manage existing robots."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from bson import ObjectId

from backend.core.database import get_database


class RobotManager:
    """Manage robot operations and lifecycle."""

    async def get_player_robots(self, player_id: str) -> List[Dict[str, Any]]:
        """Get all robots owned by a player."""
        db = await get_database()

        robots = await db.robots.find({"owner_id": player_id}).to_list(length=100)

        return robots

    async def get_robot(self, robot_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific robot."""
        db = await get_database()

        robot = await db.robots.find_one({"id": robot_id})

        return robot

    async def rename_robot(
        self,
        robot_id: str,
        owner_id: str,
        new_name: str
    ) -> Dict[str, Any]:
        """Rename a robot."""
        robot = await self.get_robot(robot_id)

        if not robot:
            raise ValueError("Robot not found")

        if robot["owner_id"] != owner_id:
            raise ValueError("Not your robot")

        if len(new_name) < 3 or len(new_name) > 30:
            raise ValueError("Name must be 3-30 characters")

        db = await get_database()

        await db.robots.update_one(
            {"id": robot_id},
            {"$set": {"name": new_name}}
        )

        return {
            "success": True,
            "robot_id": robot_id,
            "new_name": new_name
        }

    async def delete_robot(
        self,
        robot_id: str,
        owner_id: str
    ) -> Dict[str, Any]:
        """Delete/scrap a robot."""
        robot = await self.get_robot(robot_id)

        if not robot:
            raise ValueError("Robot not found")

        if robot["owner_id"] != owner_id:
            raise ValueError("Not your robot")

        db = await get_database()

        # Calculate scrap value (50% of original price)
        from backend.services.robots.factory import RobotFactory
        robot_factory = RobotFactory()
        robot_type = robot["robot_type"]

        if robot_type in robot_factory.ROBOT_TYPES:
            original_price = robot_factory.ROBOT_TYPES[robot_type]["price"]
            scrap_value = original_price // 2

            # Give back scrap value
            from backend.services.economy.currency import CurrencyService
            currency_service = CurrencyService()

            await currency_service.add_currency(
                owner_id,
                "credits",
                scrap_value,
                reason=f"scrap_robot_{robot_id}"
            )
        else:
            scrap_value = 0

        # Remove robot
        await db.robots.delete_one({"id": robot_id})

        # Remove from player's inventory
        await db.players.update_one(
            {"_id": ObjectId(owner_id)},
            {"$pull": {"robots": robot_id}}
        )

        return {
            "success": True,
            "robot_id": robot_id,
            "scrap_value": scrap_value,
            "message": f"Robot scrapped for {scrap_value} credits"
        }

    async def update_robot_status(
        self,
        robot_id: str,
        status: str
    ):
        """Update robot's operational status."""
        valid_statuses = ["idle", "working",
            "training", "combat", "maintenance"]

        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status. Must be one of: {valid_statuses}")

        db = await get_database()

        await db.robots.update_one(
            {"id": robot_id},
            {
                "$set": {
                    "status": status,
                    "last_used": datetime.utcnow()
                }
            }
        )

    async def add_experience(
        self,
        robot_id: str,
        experience: int
    ) -> Dict[str, Any]:
        """Add experience to a robot and check for level up."""
        robot = await self.get_robot(robot_id)

        if not robot:
            raise ValueError("Robot not found")

        new_exp = robot.get("experience", 0) + experience
        current_level = robot.get("level", 1)

        # Calculate level up (100 XP per level)
        xp_for_next_level = current_level * 100
        level_ups = 0

        while new_exp >= xp_for_next_level:
            new_exp -= xp_for_next_level
            current_level += 1
            level_ups += 1
            xp_for_next_level = current_level * 100

        # Update database
        db = await get_database()
        update_data = {
            "experience": new_exp,
            "level": current_level
        }

        # Stat increases on level up
        if level_ups > 0:
            stats = robot.get("stats", {})
            for stat_name in stats:
                stats[stat_name] = min(100, stats[stat_name] + level_ups)
            update_data["stats"] = stats

        await db.robots.update_one(
            {"id": robot_id},
            {"$set": update_data}
        )

        return {
            "success": True,
            "robot_id": robot_id,
            "new_level": current_level,
            "level_ups": level_ups,
            "new_experience": new_exp
        }

    async def get_robot_stats(self, robot_id: str) -> Dict[str, Any]:
        """Get comprehensive robot statistics."""
        robot = await self.get_robot(robot_id)

        if not robot:
            raise ValueError("Robot not found")

        return {
            "robot_id": robot_id,
            "name": robot["name"],
            "type": robot["robot_type"],
            "level": robot.get("level", 1),
            "experience": robot.get("experience", 0),
            "stats": robot.get("stats", {}),
            "abilities": robot.get("abilities", []),
            "status": robot.get("status", "idle"),
            "loyalty": robot.get("loyalty", 100),
            "total_tasks": robot.get("total_tasks", 0),
            "created_at": robot.get("created_at"),
            "last_used": robot.get("last_used")
        }
