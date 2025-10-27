"""Robot marketplace service."""

from typing import Dict, Any, List
from datetime import datetime
import uuid
from bson import ObjectId

from backend.core.database import get_database
from backend.services.economy.currency import CurrencyService
from backend.services.robots.manager import RobotManager


class RobotMarketplace:
    """Manage robot buying and selling."""

    def __init__(self):
        self.currency_service = CurrencyService()
        self.robot_manager = RobotManager()

    async def get_listings(
        self,
        limit: int = 50,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """Get active marketplace listings."""
        db = await get_database()

        listings = await db.robot_listings.find(
            {"status": "active"}
        ).sort("listed_at", -1).skip(skip).limit(limit).to_list(length=limit)

        # Enhance with robot details
        for listing in listings:
            robot = await self.robot_manager.get_robot(listing["robot_id"])
            if robot:
                listing["robot_details"] = {
                    "name": robot["name"],
                    "type": robot["robot_type"],
                    "level": robot.get("level", 1),
                    "stats": robot.get("stats", {})
                }

        return listings

    async def list_robot(
        self,
        robot_id: str,
        seller_id: str,
        price: int
    ) -> Dict[str, Any]:
        """List a robot for sale."""
        # Verify ownership
        robot = await self.robot_manager.get_robot(robot_id)

        if not robot:
            raise ValueError("Robot not found")

        if robot["owner_id"] != seller_id:
            raise ValueError("Not your robot")

        if price < 100:
            raise ValueError("Price too low (minimum 100 credits)")

        # Check if already listed
        db = await get_database()
        existing = await db.robot_listings.find_one({
            "robot_id": robot_id,
            "status": "active"
        })

        if existing:
            raise ValueError("Robot already listed")

        # Create listing
        listing_id = str(uuid.uuid4())
        listing = {
            "listing_id": listing_id,
            "robot_id": robot_id,
            "seller_id": seller_id,
            "price": price,
            "status": "active",
            "listed_at": datetime.utcnow(),
            "views": 0
        }

        await db.robot_listings.insert_one(listing)

        # Update robot status
        await self.robot_manager.update_robot_status(robot_id, "marketplace")

        return {
            "success": True,
            "listing_id": listing_id,
            "message": f"Robot listed for {price} credits"
        }

    async def buy_robot(
        self,
        listing_id: str,
        buyer_id: str
    ) -> Dict[str, Any]:
        """Buy a robot from marketplace."""
        db = await get_database()

        # Get listing
        listing = await db.robot_listings.find_one({"listing_id": listing_id})

        if not listing:
            raise ValueError("Listing not found")

        if listing["status"] != "active":
            raise ValueError("Listing no longer available")

        if listing["seller_id"] == buyer_id:
            raise ValueError("Cannot buy your own robot")

        # Check buyer's balance
        balance = await self.currency_service.get_balance(buyer_id, "credits")
        if balance < listing["price"]:
            raise ValueError("Insufficient credits")

        # Transfer payment
        await self.currency_service.transfer_currency(
            from_player_id=buyer_id,
            to_player_id=listing["seller_id"],
            currency_type="credits",
            amount=listing["price"]
        )

        # Transfer robot ownership
        robot_id = listing["robot_id"]

        await db.robots.update_one(
            {"id": robot_id},
            {"$set": {"owner_id": buyer_id, "status": "idle"}}
        )

        # Remove from seller's inventory
        await db.players.update_one(
            {"_id": ObjectId(listing["seller_id"])},
            {"$pull": {"robots": robot_id}}
        )

        # Add to buyer's inventory
        await db.players.update_one(
            {"_id": ObjectId(buyer_id)},
            {"$push": {"robots": robot_id}}
        )

        # Mark listing as sold
        await db.robot_listings.update_one(
            {"listing_id": listing_id},
            {
                "$set": {
                    "status": "sold",
                    "buyer_id": buyer_id,
                    "sold_at": datetime.utcnow()
                }
            }
        )

        return {
            "success": True,
            "robot_id": robot_id,
            "price_paid": listing["price"],
            "message": "Robot purchased successfully!"
        }

    async def cancel_listing(
        self,
        listing_id: str,
        seller_id: str
    ) -> Dict[str, Any]:
        """Cancel a marketplace listing."""
        db = await get_database()

        listing = await db.robot_listings.find_one({"listing_id": listing_id})

        if not listing:
            raise ValueError("Listing not found")

        if listing["seller_id"] != seller_id:
            raise ValueError("Not your listing")

        if listing["status"] != "active":
            raise ValueError("Listing is not active")

        # Cancel listing
        await db.robot_listings.update_one(
            {"listing_id": listing_id},
            {"$set": {"status": "cancelled"}}
        )

        # Update robot status
        await self.robot_manager.update_robot_status(listing["robot_id"], "idle")

        return {
            "success": True,
            "listing_id": listing_id,
            "message": "Listing cancelled"
        }

    async def get_seller_listings(self, seller_id: str) -> List[Dict[str, Any]]:
        """Get all listings by a seller."""
        db = await get_database()

        listings = await db.robot_listings.find({
            "seller_id": seller_id,
            "status": "active"
        }).to_list(length=100)

        return listings
