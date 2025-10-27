from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ...models.player.player import Player
from ...models.economy.transaction import Transaction
from .property_types import PropertyTypes


class RealEstateService:
    """Service for managing real estate transactions."""

    def __init__(self):
        self.property_types = PropertyTypes()

    async def get_available_properties(
        self,
        property_type: Optional[str] = None,
        max_price: Optional[int] = None,
        territory_id: Optional[int] = None
    ) -> List[Dict]:
        """Get available properties for purchase."""
        all_properties = self.property_types.get_all_properties()

        filtered = []
        for prop in all_properties:
            # Filter by type
            if property_type and prop.get("property_type") != property_type:
                continue

            # Filter by price
            if max_price and prop.get("price", 0) > max_price:
                continue

            # Filter by territory
            if territory_id and prop.get("territory_id") != territory_id:
                continue

            # Only show available properties
            if prop.get("status") == "available":
                filtered.append(prop)

        return filtered

    async def get_player_properties(self, player_id: str) -> List[Dict]:
        """Get properties owned by player."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return []

        return player.get("properties", [])

    async def get_property_details(self, property_id: str) -> Optional[Dict]:
        """Get detailed information about a property."""
        return self.property_types.get_property_by_id(property_id)

    async def purchase_property(
        self,
        player_id: str,
        property_id: str
    ) -> Dict:
        """Purchase a property."""
        player = await Player.find_one({"_id": player_id})
        property_data = self.property_types.get_property_by_id(property_id)

        if not player or not property_data:
            return {"success": False, "error": "Invalid player or property"}

        price = property_data.get("price", 0)
        player_credits = player.get("currencies", {}).get("credits", 0)

        # Check if player can afford
        if player_credits < price:
            return {"success": False, "error": "Insufficient credits"}

        # Deduct payment
        new_balance = player_credits - price

        # Add property to player's portfolio
        player_properties = player.get("properties", [])
        player_properties.append({
            "property_id": property_id,
            "name": property_data.get("name"),
            "property_type": property_data.get("property_type"),
            "purchase_price": price,
            "purchase_date": datetime.utcnow(),
            "passive_income": property_data.get("passive_income", 0),
            "upgrades": []
        })

        # Update player
        await Player.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "currencies.credits": new_balance,
                    "properties": player_properties
                }
            }
        )

        # Log transaction
        await Transaction.insert_one({
            "player_id": player_id,
            "type": "real_estate_purchase",
            "amount": -price,
            "details": {
                "property_id": property_id,
                "property_name": property_data.get("name")
            },
            "timestamp": datetime.utcnow()
        })

        return {
            "success": True,
            "property_id": property_id,
            "property_name": property_data.get("name"),
            "price_paid": price,
            "new_balance": new_balance,
            "passive_income": property_data.get("passive_income", 0)
        }

    async def sell_property(
        self,
        player_id: str,
        property_id: str,
        sale_price: int
    ) -> Dict:
        """Sell a property."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return {"success": False, "error": "Player not found"}

        # Find property in player's portfolio
        player_properties = player.get("properties", [])
        property_to_sell = next(
            (p for p in player_properties if p.get("property_id") == property_id),
            None
        )

        if not property_to_sell:
            return {"success": False, "error": "Property not owned"}

        # Remove property
        player_properties = [p for p in player_properties if p.get(
            "property_id") != property_id]

        # Add credits
        player_credits = player.get("currencies", {}).get("credits", 0)
        new_balance = player_credits + sale_price

        # Update player
        await Player.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "currencies.credits": new_balance,
                    "properties": player_properties
                }
            }
        )

        # Log transaction
        await Transaction.insert_one({
            "player_id": player_id,
            "type": "real_estate_sale",
            "amount": sale_price,
            "details": {
                "property_id": property_id,
                "property_name": property_to_sell.get("name")
            },
            "timestamp": datetime.utcnow()
        })

        return {
            "success": True,
            "property_id": property_id,
            "sale_price": sale_price,
            "new_balance": new_balance
        }

    async def upgrade_property(
        self,
        player_id: str,
        property_id: str,
        upgrade_type: str
    ) -> Dict:
        """Upgrade a property."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return {"success": False, "error": "Player not found"}

        # Find property
        player_properties = player.get("properties", [])
        property_index = next(
            (i for i, p in enumerate(player_properties)
             if p.get("property_id") == property_id),
            None
        )

        if property_index is None:
            return {"success": False, "error": "Property not owned"}

        # Upgrade costs and benefits
        upgrades = {
            "security_system": {"cost": 5000, "income_boost": 50},
            "automation": {"cost": 10000, "income_boost": 100},
            "expansion": {"cost": 20000, "income_boost": 200},
            "luxury_finish": {"cost": 50000, "income_boost": 500}
        }

        upgrade = upgrades.get(upgrade_type)
        if not upgrade:
            return {"success": False, "error": "Invalid upgrade type"}

        # Check if player can afford
        player_credits = player.get("currencies", {}).get("credits", 0)
        if player_credits < upgrade["cost"]:
            return {"success": False, "error": "Insufficient credits"}

        # Apply upgrade
        property_to_upgrade = player_properties[property_index]
        property_to_upgrade.setdefault("upgrades", []).append({
            "type": upgrade_type,
            "applied_date": datetime.utcnow()
        })
        property_to_upgrade["passive_income"] = property_to_upgrade.get(
            "passive_income", 0) + upgrade["income_boost"]

        # Update player
        await Player.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "currencies.credits": player_credits - upgrade["cost"],
                    "properties": player_properties
                }
            }
        )

        return {
            "success": True,
            "upgrade_type": upgrade_type,
            "cost": upgrade["cost"],
            "new_income": property_to_upgrade["passive_income"]
        }

    async def rent_property(
        self,
        player_id: str,
        property_id: str,
        tenant_id: str,
        rent_amount: int,
        duration_days: int
    ) -> Dict:
        """Rent out a property."""
        # Implementation for renting properties
        return {
            "success": True,
            "property_id": property_id,
            "tenant_id": tenant_id,
            "rent_amount": rent_amount,
            "duration_days": duration_days,
            "rental_start": datetime.utcnow(),
            "rental_end": datetime.utcnow() + timedelta(days=duration_days)
        }

    async def calculate_property_income(self, player_id: str) -> Dict:
        """Calculate total income from all properties."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return {"total_daily_income": 0, "properties": []}

        player_properties = player.get("properties", [])
        total_income = sum(p.get("passive_income", 0)
                           for p in player_properties)

        return {
            "total_daily_income": total_income,
            "total_properties": len(player_properties),
            "properties": [
                {
                    "property_id": p.get("property_id"),
                    "name": p.get("name"),
                    "daily_income": p.get("passive_income", 0)
                }
                for p in player_properties
            ]
        }
