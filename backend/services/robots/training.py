"""Robot training service."""

from typing import Dict, Any, List
from datetime import datetime, timedelta

from backend.core.database import get_database
from backend.services.robots.manager import RobotManager
from backend.services.economy.currency import CurrencyService


class RobotTrainingService:
    """Manage robot training sessions."""

    TRAINING_TYPES = {
        "combat": {
            "name": "Combat Training",
            "description": "Improve attack and defense stats",
            "cost_per_hour": 100,
            "stat_bonuses": {"attack": 2, "defense": 2},
            "xp_per_hour": 50
        },
        "efficiency": {
            "name": "Efficiency Training",
            "description": "Improve work efficiency and speed",
            "cost_per_hour": 80,
            "stat_bonuses": {"efficiency": 3, "speed": 2},
            "xp_per_hour": 40
        },
        "intelligence": {
            "name": "Intelligence Training",
            "description": "Improve AI capabilities",
            "cost_per_hour": 120,
            "stat_bonuses": {"intelligence": 3},
            "xp_per_hour": 60
        },
        "durability": {
            "name": "Durability Enhancement",
            "description": "Improve robot longevity",
            "cost_per_hour": 90,
            "stat_bonuses": {"durability": 3},
            "xp_per_hour": 45
        }
    }

    def __init__(self):
        self.robot_manager = RobotManager()
        self.currency_service = CurrencyService()

    def get_training_types(self) -> List[Dict[str, Any]]:
        """Get all available training types."""
        return [
            {
                "type_id": type_id,
                **type_data
            }
            for type_id, type_data in self.TRAINING_TYPES.items()
        ]

    async def start_training(
        self,
        robot_id: str,
        owner_id: str,
        training_type: str,
        duration_hours: int = 1
    ) -> Dict[str, Any]:
        """Start a training session for a robot."""
        # Validate training type
        if training_type not in self.TRAINING_TYPES:
            raise ValueError(f"Invalid training type: {training_type}")

        # Get robot
        robot = await self.robot_manager.get_robot(robot_id)

        if not robot:
            raise ValueError("Robot not found")

        if robot["owner_id"] != owner_id:
            raise ValueError("Not your robot")

        # Check if already training
        db = await get_database()
        existing = await db.robot_training.find_one({
            "robot_id": robot_id,
            "status": "active"
        })

        if existing:
            raise ValueError("Robot is already training")

        # Calculate cost
        training_data = self.TRAINING_TYPES[training_type]
        total_cost = training_data["cost_per_hour"] * duration_hours

        # Check balance
        balance = await self.currency_service.get_balance(owner_id, "credits")
        if balance < total_cost:
            raise ValueError(
                f"Insufficient credits. Need {total_cost}, have {balance}")

        # Deduct cost
        await self.currency_service.deduct_currency(
            owner_id,
            "credits",
            total_cost,
            reason=f"robot_training_{robot_id}"
        )

        # Create training session
        now = datetime.utcnow()
        completes_at = now + timedelta(hours=duration_hours)

        training_session = {
            "robot_id": robot_id,
            "owner_id": owner_id,
            "training_type": training_type,
            "duration_hours": duration_hours,
            "started_at": now,
            "completes_at": completes_at,
            "status": "active",
            "cost": total_cost,
            "rewards": {
                "stat_bonuses": {
                    k: v * duration_hours
                    for k, v in training_data["stat_bonuses"].items()
                },
                "xp": training_data["xp_per_hour"] * duration_hours
            }
        }

        await db.robot_training.insert_one(training_session)

        # Update robot status
        await self.robot_manager.update_robot_status(robot_id, "training")

        return {
            "success": True,
            "robot_id": robot_id,
            "training_type": training_type,
            "duration_hours": duration_hours,
            "cost": total_cost,
            "completes_at": completes_at,
            "message": f"Training started! Will complete in {duration_hours} hour(s)"
        }

    async def get_training_status(self, robot_id: str) -> Dict[str, Any]:
        """Get current training status for a robot."""
        db = await get_database()

        training = await db.robot_training.find_one({
            "robot_id": robot_id,
            "status": "active"
        })

        if not training:
            return {
                "robot_id": robot_id,
                "is_training": False
            }

        now = datetime.utcnow()
        completes_at = training["completes_at"]

        time_remaining = (completes_at - now).total_seconds()
        time_remaining = max(0, int(time_remaining))

        return {
            "robot_id": robot_id,
            "is_training": True,
            "training_type": training["training_type"],
            "started_at": training["started_at"],
            "completes_at": completes_at,
            "time_remaining_seconds": time_remaining,
            "rewards": training["rewards"]
        }

    async def complete_training(
        self,
        robot_id: str,
        owner_id: str
    ) -> Dict[str, Any]:
        """Complete training and apply rewards."""
        db = await get_database()

        training = await db.robot_training.find_one({
            "robot_id": robot_id,
            "status": "active"
        })

        if not training:
            raise ValueError("No active training session")

        if training["owner_id"] != owner_id:
            raise ValueError("Not your robot")

        # Check if training is complete
        now = datetime.utcnow()
        if now < training["completes_at"]:
            time_remaining = (training["completes_at"] - now).total_seconds()
            raise ValueError(
                f"Training not complete yet. {int(time_remaining)} seconds remaining")

        # Get robot
        robot = await self.robot_manager.get_robot(robot_id)

        if not robot:
            raise ValueError("Robot not found")

        # Apply stat bonuses
        stats = robot.get("stats", {})
        rewards = training["rewards"]

        for stat_name, bonus in rewards["stat_bonuses"].items():
            if stat_name in stats:
                stats[stat_name] = min(100, stats[stat_name] + bonus)

        await db.robots.update_one(
            {"id": robot_id},
            {"$set": {"stats": stats}}
        )

        # Add experience
        xp_gained = rewards["xp"]
        await self.robot_manager.add_experience(robot_id, xp_gained)

        # Update robot status
        await self.robot_manager.update_robot_status(robot_id, "idle")

        # Mark training as complete
        await db.robot_training.update_one(
            {"robot_id": robot_id, "status": "active"},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": now
                }
            }
        )

        return {
            "success": True,
            "robot_id": robot_id,
            "stat_bonuses": rewards["stat_bonuses"],
            "xp_gained": xp_gained,
            "message": "Training completed successfully!"
        }

    async def auto_complete_training(self):
        """Auto-complete all finished training sessions (called by scheduler)."""
        db = await get_database()

        now = datetime.utcnow()

        # Find all completed training sessions
        completed = await db.robot_training.find({
            "status": "active",
            "completes_at": {"$lte": now}
        }).to_list(length=1000)

        for training in completed:
            try:
                await self.complete_training(
                    robot_id=training["robot_id"],
                    owner_id=training["owner_id"]
                )
            except Exception as e:
                print(
                    f"Error auto-completing training for robot {training['robot_id']}: {e}")
