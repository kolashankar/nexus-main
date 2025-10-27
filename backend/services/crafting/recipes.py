from typing import List, Dict, Optional


class RecipeManager:
    """Manages crafting recipes."""

    def __init__(self):
        self.recipes = self._load_recipes()

    def _load_recipes(self) -> Dict[str, Dict]:
        """Load recipes from configuration."""
        # In production, this would load from database or config file
        # For now, return hardcoded recipes
        return {
            "basic_robot_parts": {
                "id": "basic_robot_parts",
                "name": "Basic Robot Parts",
                "description": "Essential components for robot construction",
                "category": "robot_parts",
                "level_required": 1,
                "crafting_time": 60,
                "xp_reward": 25,
                "success_rate": 0.95,
                "materials_required": [
                    {"material_id": "scrap_metal",
                        "name": "Scrap Metal", "quantity": 5},
                    {"material_id": "circuits", "name": "Circuits", "quantity": 2}
                ],
                "result_item": {
                    "name": "Basic Robot Parts",
                    "type": "robot_component",
                    "rarity": "common"
                }
            },
            "advanced_circuit": {
                "id": "advanced_circuit",
                "name": "Advanced Circuit",
                "description": "High-quality electronic circuits",
                "category": "electronics",
                "level_required": 10,
                "crafting_time": 120,
                "xp_reward": 50,
                "success_rate": 0.85,
                "materials_required": [
                    {"material_id": "circuits", "name": "Circuits", "quantity": 3},
                    {"material_id": "rare_metals",
                        "name": "Rare Metals", "quantity": 2},
                    {"material_id": "silicon", "name": "Silicon", "quantity": 1}
                ],
                "result_item": {
                    "name": "Advanced Circuit",
                    "type": "electronic_component",
                    "rarity": "uncommon"
                }
            },
            "energy_cell": {
                "id": "energy_cell",
                "name": "Energy Cell",
                "description": "Portable energy storage unit",
                "category": "power",
                "level_required": 15,
                "crafting_time": 180,
                "xp_reward": 75,
                "success_rate": 0.80,
                "materials_required": [
                    {"material_id": "power_core",
                        "name": "Power Core", "quantity": 1},
                    {"material_id": "rare_metals",
                        "name": "Rare Metals", "quantity": 3},
                    {"material_id": "coolant", "name": "Coolant", "quantity": 2}
                ],
                "result_item": {
                    "name": "Energy Cell",
                    "type": "power_source",
                    "rarity": "rare"
                }
            },
            "cybernetic_implant": {
                "id": "cybernetic_implant",
                "name": "Cybernetic Implant",
                "description": "Augmentation device for enhanced abilities",
                "category": "augmentation",
                "level_required": 25,
                "crafting_time": 300,
                "xp_reward": 150,
                "success_rate": 0.70,
                "materials_required": [
                    {"material_id": "bio_gel", "name": "Bio-Gel", "quantity": 2},
                    {"material_id": "advanced_circuit",
                        "name": "Advanced Circuit", "quantity": 2},
                    {"material_id": "nano_fibers",
                        "name": "Nano Fibers", "quantity": 3}
                ],
                "result_item": {
                    "name": "Cybernetic Implant",
                    "type": "augmentation",
                    "rarity": "epic"
                }
            },
            "quantum_processor": {
                "id": "quantum_processor",
                "name": "Quantum Processor",
                "description": "Cutting-edge computational unit",
                "category": "electronics",
                "level_required": 40,
                "crafting_time": 600,
                "xp_reward": 300,
                "success_rate": 0.60,
                "materials_required": [
                    {"material_id": "quantum_crystal",
                        "name": "Quantum Crystal", "quantity": 1},
                    {"material_id": "advanced_circuit",
                        "name": "Advanced Circuit", "quantity": 5},
                    {"material_id": "exotic_matter",
                        "name": "Exotic Matter", "quantity": 2}
                ],
                "result_item": {
                    "name": "Quantum Processor",
                    "type": "advanced_component",
                    "rarity": "legendary"
                }
            }
        }

    async def get_all_recipes(self) -> List[Dict]:
        """Get all available recipes."""
        return list(self.recipes.values())

    async def get_recipe(self, recipe_id: str) -> Optional[Dict]:
        """Get a specific recipe by ID."""
        return self.recipes.get(recipe_id)

    async def get_recipes_by_category(self, category: str) -> List[Dict]:
        """Get recipes by category."""
        return [
            recipe for recipe in self.recipes.values()
            if recipe.get("category") == category
        ]

    async def get_recipes_by_level(self, min_level: int, max_level: int = 100) -> List[Dict]:
        """Get recipes by level range."""
        return [
            recipe for recipe in self.recipes.values()
            if min_level <= recipe.get("level_required", 0) <= max_level
        ]
