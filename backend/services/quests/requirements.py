from typing import Dict, List
from ...models.player.player import Player


class QuestRequirementChecker:
    """Service for checking quest requirements."""

    async def check_requirements(
        self,
        player_id: str,
        requirements: Dict
    ) -> Dict:
        """Check if player meets quest requirements."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return {"meets_requirements": False, "reason": "Player not found"}

        # Check level
        min_level = requirements.get("min_level", 0)
        if player.get("level", 1) < min_level:
            return {
                "meets_requirements": False,
                "reason": f"Requires level {min_level}"
            }

        # Check karma
        min_karma = requirements.get("min_karma")
        if min_karma is not None:
            if player.get("karma_points", 0) < min_karma:
                return {
                    "meets_requirements": False,
                    "reason": f"Requires {min_karma} karma"
                }

        max_karma = requirements.get("max_karma")
        if max_karma is not None:
            if player.get("karma_points", 0) > max_karma:
                return {
                    "meets_requirements": False,
                    "reason": f"Maximum karma: {max_karma}"
                }

        # Check traits
        required_traits = requirements.get("required_traits", {})
        player_traits = player.get("traits", {})
        for trait, min_value in required_traits.items():
            if player_traits.get(trait, 0) < min_value:
                return {
                    "meets_requirements": False,
                    "reason": f"Requires {trait} >= {min_value}"
                }

        # Check items
        required_items = requirements.get("required_items", [])
        player_inventory = player.get("items", [])
        player_item_ids = [item.get("item_id") for item in player_inventory]
        for item_id in required_items:
            if item_id not in player_item_ids:
                return {
                    "meets_requirements": False,
                    "reason": f"Requires item: {item_id}"
                }

        # Check guild membership
        required_guild = requirements.get("guild_member")
        if required_guild and not player.get("guild_id"):
            return {
                "meets_requirements": False,
                "reason": "Must be in a guild"
            }

        # Check completed quests
        required_quests = requirements.get("completed_quests", [])
        completed_quests = player.get("completed_quests", [])
        for quest_id in required_quests:
            if quest_id not in completed_quests:
                return {
                    "meets_requirements": False,
                    "reason": f"Must complete quest: {quest_id}"
                }

        return {"meets_requirements": True}

    def get_requirement_description(self, requirements: Dict) -> List[str]:
        """Get human-readable requirement descriptions."""
        descriptions = []

        if requirements.get("min_level", 0) > 0:
            descriptions.append(f"Level {requirements['min_level']}+")

        if requirements.get("min_karma") is not None:
            descriptions.append(f"Karma: {requirements['min_karma']}+")

        for trait, value in requirements.get("required_traits", {}).items():
            descriptions.append(f"{trait.capitalize()}: {value}+")

        if requirements.get("guild_member"):
            descriptions.append("Guild membership required")

        return descriptions
