"""Robot factory - create and configure robots."""

from typing import Dict, Any, List
from datetime import datetime
import uuid
from bson import ObjectId

from backend.core.database import get_database
from backend.services.economy.currency import CurrencyService


class RobotFactory:
    """Factory for creating robots."""

    # 15 Robot types with stats and prices
    ROBOT_TYPES = {
        # Worker Robots (Economic)
        "harvester": {
            "name": "Harvester",
            "class": "Worker",
            "description": "Gather resources automatically",
            "price": 1000,
            "stats": {
                "efficiency": 70,
                "speed": 50,
                "durability": 60,
                "intelligence": 30
            },
            "abilities": ["resource_gathering", "auto_harvest"]
        },
        "trader": {
            "name": "Trader Bot",
            "class": "Worker",
            "description": "Autonomous trading",
            "price": 3000,
            "stats": {
                "efficiency": 80,
                "speed": 60,
                "durability": 40,
                "intelligence": 70
            },
            "abilities": ["auto_trade", "market_analysis"]
        },
        "builder": {
            "name": "Builder",
            "class": "Worker",
            "description": "Construct items and structures",
            "price": 2500,
            "stats": {
                "efficiency": 75,
                "speed": 40,
                "durability": 80,
                "intelligence": 50
            },
            "abilities": ["construction", "repair"]
        },
        # Combat Robots (Military)
        "guardian": {
            "name": "Guardian",
            "class": "Combat",
            "description": "Defensive combat robot",
            "price": 5000,
            "stats": {
                "attack": 60,
                "defense": 90,
                "speed": 40,
                "intelligence": 50
            },
            "abilities": ["shield", "guard"]
        },
        "assault": {
            "name": "Assault Bot",
            "class": "Combat",
            "description": "Offensive combat",
            "price": 7000,
            "stats": {
                "attack": 90,
                "defense": 50,
                "speed": 70,
                "intelligence": 40
            },
            "abilities": ["attack_boost", "rapid_fire"]
        },
        "tactical": {
            "name": "Tactical Unit",
            "class": "Combat",
            "description": "Strategic combat support",
            "price": 10000,
            "stats": {
                "attack": 70,
                "defense": 70,
                "speed": 60,
                "intelligence": 80
            },
            "abilities": ["tactical_scan", "command"]
        },
        # Specialist Robots (Utility)
        "hacker": {
            "name": "Hacker Bot",
            "class": "Specialist",
            "description": "Cyber warfare specialist",
            "price": 8000,
            "stats": {
                "attack": 50,
                "defense": 30,
                "speed": 80,
                "intelligence": 95
            },
            "abilities": ["hack", "bypass_security", "data_theft"]
        },
        "medic": {
            "name": "Medic Bot",
            "class": "Specialist",
            "description": "Healing and support",
            "price": 6000,
            "stats": {
                "attack": 20,
                "defense": 60,
                "speed": 50,
                "intelligence": 75
            },
            "abilities": ["heal", "repair", "buff"]
        },
        "scout": {
            "name": "Scout",
            "class": "Specialist",
            "description": "Information gathering",
            "price": 4000,
            "stats": {
                "attack": 30,
                "defense": 40,
                "speed": 95,
                "intelligence": 70
            },
            "abilities": ["reconnaissance", "stealth"]
        },
        # Advanced Robots (High-Tier)
        "companion": {
            "name": "AI Companion",
            "class": "Advanced",
            "description": "Personal AI assistant",
            "price": 15000,
            "stats": {
                "attack": 40,
                "defense": 50,
                "speed": 60,
                "intelligence": 90
            },
            "abilities": ["assist", "analyze", "learn"]
        },
        "bodyguard": {
            "name": "Bodyguard",
            "class": "Advanced",
            "description": "Full protection",
            "price": 20000,
            "stats": {
                "attack": 80,
                "defense": 95,
                "speed": 70,
                "intelligence": 60
            },
            "abilities": ["protect", "counter", "intercept"]
        },
        "spy": {
            "name": "Spy Network",
            "class": "Advanced",
            "description": "Intelligence network",
            "price": 18000,
            "stats": {
                "attack": 50,
                "defense": 50,
                "speed": 85,
                "intelligence": 95
            },
            "abilities": ["surveillance", "infiltration", "intelligence"]
        },
        # Legendary Robots (Rare)
        "warmachine": {
            "name": "War Machine",
            "class": "Legendary",
            "description": "Ultimate combat robot",
            "price": 50000,
            "stats": {
                "attack": 95,
                "defense": 90,
                "speed": 75,
                "intelligence": 70
            },
            "abilities": ["devastate", "siege", "overwhelm"]
        },
        "omnidrone": {
            "name": "Omnidrone",
            "class": "Legendary",
            "description": "All-purpose advanced unit",
            "price": 75000,
            "stats": {
                "attack": 80,
                "defense": 80,
                "speed": 80,
                "intelligence": 85
            },
            "abilities": ["adapt", "multitask", "optimize"]
        },
        "sentinel": {
            "name": "Sentinel Prime",
            "class": "Legendary",
            "description": "Guild protector",
            "price": 100000,
            "stats": {
                "attack": 85,
                "defense": 100,
                "speed": 65,
                "intelligence": 80
            },
            "abilities": ["fortress", "rally", "inspire"]
        }
    }

    def __init__(self):
        self.currency_service = CurrencyService()

    def get_all_robot_types(self) -> List[Dict[str, Any]]:
        """Get all available robot types."""
        return [
            {
                "type_id": type_id,
                **type_data
            }
            for type_id, type_data in self.ROBOT_TYPES.items()
        ]

    async def create_robot(
        self,
        player_id: str,
        robot_type: str,
        custom_name: str = None
    ) -> Dict[str, Any]:
        """Create a new robot for a player."""
        robot_type = robot_type.lower()

        if robot_type not in self.ROBOT_TYPES:
            raise ValueError(f"Invalid robot type: {robot_type}")

        robot_data = self.ROBOT_TYPES[robot_type]

        # Check if player can afford
        balance = await self.currency_service.get_balance(player_id, "credits")
        if balance < robot_data["price"]:
            raise ValueError(
                f"Insufficient credits. Need {robot_data['price']}, have {balance}")

        # Deduct cost
        await self.currency_service.deduct_currency(
            player_id,
            "credits",
            robot_data["price"],
            reason=f"purchase_robot_{robot_type}"
        )

        # Create robot
        robot_id = str(uuid.uuid4())
        robot = {
            "id": robot_id,
            "robot_type": robot_type,
            "name": custom_name or robot_data["name"],
            "owner_id": player_id,
            "level": 1,
            "experience": 0,
            "stats": robot_data["stats"].copy(),
            "abilities": robot_data["abilities"].copy(),
            "status": "idle",  # idle, working, training, combat
            "loyalty": 100,  # Can decrease if mistreated
            "created_at": datetime.utcnow(),
            "last_used": None,
            "total_tasks": 0
        }

        # Save to database
        db = await get_database()
        await db.robots.insert_one(robot)

        # Add to player's robot inventory
        await db.players.update_one(
            {"_id": ObjectId(player_id)},
            {"$push": {"robots": robot_id}}
        )

        return {
            "success": True,
            "robot": robot,
            "message": f"Successfully purchased {robot_data['name']}!"
        }
