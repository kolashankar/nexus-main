from typing import List, Dict, Optional
from datetime import datetime
import random
from ...models.player.player import Player
from ...models.economy.transaction import Transaction
from .recipes import RecipeManager
import uuid


class CraftingService:
    """Service for handling item crafting."""

    def __init__(self):
        self.recipe_manager = RecipeManager()

    async def get_recipes(
        self,
        player_level: int,
        category: Optional[str] = None,
        min_level: Optional[int] = None
    ) -> List[Dict]:
        """Get available recipes for player."""
        all_recipes = await self.recipe_manager.get_all_recipes()

        filtered_recipes = []
        for recipe in all_recipes:
            # Filter by category
            if category and recipe.get("category") != category:
                continue

            # Filter by min level
            if min_level and recipe.get("level_required", 0) < min_level:
                continue

            # Add unlocked status
            recipe["unlocked"] = player_level >= recipe.get(
                "level_required", 0)
            filtered_recipes.append(recipe)

        return filtered_recipes

    async def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict]:
        """Get recipe by ID."""
        return await self.recipe_manager.get_recipe(recipe_id)

    async def can_craft(
        self,
        player_id: str,
        recipe_id: str,
        quantity: int = 1
    ) -> bool:
        """Check if player can craft item."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return False

        recipe = await self.recipe_manager.get_recipe(recipe_id)
        if not recipe:
            return False

        # Check level requirement
        if player.get("level", 1) < recipe.get("level_required", 0):
            return False

        # Check materials
        player_inventory = player.get("items", [])
        materials_required = recipe.get("materials_required", [])

        for material in materials_required:
            material_id = material["material_id"]
            required_qty = material["quantity"] * quantity

            # Find material in inventory
            inventory_item = next(
                (item for item in player_inventory if item["item_id"] == material_id),
                None
            )

            if not inventory_item or inventory_item["quantity"] < required_qty:
                return False

        return True

    async def craft_item(
        self,
        player_id: str,
        recipe_id: str,
        quantity: int = 1
    ) -> Dict:
        """Craft an item."""
        player = await Player.find_one({"_id": player_id})
        recipe = await self.recipe_manager.get_recipe(recipe_id)

        if not player or not recipe:
            return {"success": False, "error": "Invalid player or recipe"}

        # Calculate success rate (base + player skill bonuses)
        base_success = recipe.get("success_rate", 0.95)
        player_crafting_skill = player.get(
            "traits", {}).get("engineering", 50) / 100
        success_rate = min(0.99, base_success + (player_crafting_skill * 0.05))

        crafted_items = []
        total_xp = 0
        materials_consumed = []

        for i in range(quantity):
            # Roll for success
            if random.random() <= success_rate:
                # Successful craft
                item_id = str(uuid.uuid4())
                result_item = recipe.get("result_item", {})

                crafted_items.append({
                    "item_id": item_id,
                    "name": result_item.get("name"),
                    "type": result_item.get("type"),
                    "quantity": 1
                })

                total_xp += recipe.get("xp_reward", 10)

        # Consume materials
        player_inventory = player.get("items", [])
        for material in recipe.get("materials_required", []):
            material_id = material["material_id"]
            consumed_qty = material["quantity"] * len(crafted_items)

            # Update inventory
            for item in player_inventory:
                if item["item_id"] == material_id:
                    item["quantity"] -= consumed_qty
                    materials_consumed.append({
                        "material_id": material_id,
                        "name": material.get("name"),
                        "quantity": consumed_qty
                    })
                    break

        # Add crafted items to inventory
        for crafted in crafted_items:
            player_inventory.append(crafted)

        # Update player
        await Player.update_one(
            {"_id": player_id},
            {
                "$set": {"items": player_inventory},
                "$inc": {"xp": total_xp}
            }
        )

        # Log transaction
        await Transaction.insert_one({
            "player_id": player_id,
            "type": "crafting",
            "details": {
                "recipe_id": recipe_id,
                "quantity": len(crafted_items),
                "materials": materials_consumed
            },
            "timestamp": datetime.utcnow()
        })

        return {
            "success": True,
            "item_id": crafted_items[0]["item_id"] if crafted_items else None,
            "item_name": recipe["result_item"]["name"],
            "quantity_crafted": len(crafted_items),
            "xp_gained": total_xp,
            "materials_consumed": materials_consumed,
            "bonus_received": None
        }

    async def dismantle_item(
        self,
        player_id: str,
        item_id: str
    ) -> Optional[Dict]:
        """Dismantle an item to get materials."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return None

        # Find item in inventory
        player_inventory = player.get("items", [])
        item = next((i for i in player_inventory if i.get(
            "item_id") == item_id), None)

        if not item:
            return None

        # Calculate materials returned (50-75% of original)
        return_rate = random.uniform(0.5, 0.75)
        materials_returned = []

        # Remove item from inventory
        player_inventory = [
            i for i in player_inventory if i.get("item_id") != item_id]

        # Add materials (simplified - would lookup recipe materials)
        # For now, return generic materials
        materials_returned.append({
            "material_id": "scrap_metal",
            "name": "Scrap Metal",
            "quantity": int(5 * return_rate)
        })

        # Update player
        await Player.update_one(
            {"_id": player_id},
            {"$set": {"items": player_inventory}}
        )

        return {
            "success": True,
            "item_dismantled": item.get("name"),
            "materials_returned": materials_returned
        }

    async def get_crafting_history(
        self,
        player_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """Get player's crafting history."""
        transactions = await Transaction.find(
            {"player_id": player_id, "type": "crafting"}
        ).sort("timestamp", -1).limit(limit).to_list()

        return [
            {
                "timestamp": t.get("timestamp"),
                "recipe_name": t.get("details", {}).get("recipe_id"),
                "item_crafted": "Item",
                "quantity": t.get("details", {}).get("quantity", 1),
                "success": True,
                "xp_gained": 10
            }
            for t in transactions
        ]
