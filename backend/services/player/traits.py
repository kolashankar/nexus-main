from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Dict, List
from backend.models.player.player import Player
from fastapi import HTTPException

class TraitsService:
    """Service for managing player traits."""

    # Trait categories
    VIRTUES = [
        "empathy", "integrity", "discipline", "creativity", "resilience",
        "curiosity", "kindness", "courage", "patience", "adaptability",
        "wisdom", "humility", "vision", "honesty", "loyalty",
        "generosity", "self_awareness", "gratitude", "optimism", "loveability"
    ]

    VICES = [
        "greed", "arrogance", "deceit", "cruelty", "selfishness",
        "envy", "wrath", "cowardice", "laziness", "gluttony",
        "paranoia", "impulsiveness", "vengefulness", "manipulation", "prejudice",
        "betrayal", "stubbornness", "pessimism", "recklessness", "vanity"
    ]

    SKILLS = [
        "hacking", "negotiation", "stealth", "leadership", "technical_knowledge",
        "physical_strength", "speed", "intelligence", "charisma", "perception",
        "endurance", "dexterity", "memory", "focus", "networking",
        "strategy", "trading", "engineering", "medicine", "meditation"
    ]

    META_TRAITS = [
        "reputation", "influence", "fame", "infamy", "trustworthiness",
        "combat_rating", "tactical_mastery", "survival_instinct",
        "business_acumen", "market_intuition", "wealth_management",
        "enlightenment", "karmic_balance", "divine_favor",
        "guild_loyalty", "political_power", "diplomatic_skill",
        "legendary_status", "mentorship", "historical_impact"
    ]

    TRAIT_DESCRIPTIONS = {
        "empathy": "Feel and understand others' emotions",
        "integrity": "Moral principles and honesty",
        "discipline": "Self-control and focus",
        "hacking": "Digital penetration and cyber skills",
        "reputation": "How others perceive you",
        # Add more as needed
    }

    def get_top_traits(self, player: Player, limit: int = 10) -> Dict:
        """Get player's highest traits."""
        all_traits = {**player.traits.model_dump(), **
                                                 player.meta_traits.model_dump()}
        sorted_traits = sorted(
            all_traits.items(), key=lambda x: x[1], reverse=True)

        return {
            "top_traits": [
                {"name": name, "value": value,
                    "category": self._get_trait_category(name)}
                for name, value in sorted_traits[:limit]
            ],
            "count": limit
        }

    def get_bottom_traits(self, player: Player, limit: int = 10) -> Dict:
        """Get player's lowest traits."""
        all_traits = {**player.traits.model_dump(), **
                                                 player.meta_traits.model_dump()}
        sorted_traits = sorted(all_traits.items(), key=lambda x: x[1])

        return {
            "bottom_traits": [
                {"name": name, "value": value,
                    "category": self._get_trait_category(name)}
                for name, value in sorted_traits[:limit]
            ],
            "count": limit
        }

    def get_trait_details(self, player: Player, trait_name: str) -> Dict:
        """Get detailed information about a specific trait."""
        # Check if trait exists
        all_traits = {**player.traits.model_dump(), **
                                                 player.meta_traits.model_dump()}

        if trait_name not in all_traits:
            raise HTTPException(status_code=404, detail="Trait not found")

        value = all_traits[trait_name]
        category = self._get_trait_category(trait_name)
        description = self.TRAIT_DESCRIPTIONS.get(
            trait_name, "No description available")

        # Determine what this trait affects
        affects = self._get_trait_effects(trait_name)

        return {
            "trait_name": trait_name,
            "current_value": value,
            "category": category,
            "description": description,
            "affects": affects
        }

    def _get_trait_category(self, trait_name: str) -> str:
        """Determine trait category."""
        if trait_name in self.VIRTUES:
            return "virtue"
        elif trait_name in self.VICES:
            return "vice"
        elif trait_name in self.SKILLS:
            return "skill"
        elif trait_name in self.META_TRAITS:
            return "meta"
        else:
            return "unknown"

    def _get_trait_effects(self, trait_name: str) -> List[str]:
        """Get what this trait affects (e.g., superpowers, actions)."""
        effects_map = {
            "hacking": ["Hack action success rate", "Technical challenges"],
            "empathy": ["Help action karma bonus", "Social interactions"],
            "stealth": ["Steal action success rate", "Detection avoidance"],
            "negotiation": ["Trade outcomes", "Diplomatic actions"],
            "reputation": ["Social influence", "First impressions"],
            # Add more mappings
        }
        return effects_map.get(trait_name, [])

    async def allocate_points(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        trait_name: str,
        points: int
    ) -> Dict:
        """Allocate points to a trait (for future skill tree)."""
        # Check if trait exists
        if trait_name not in (self.VIRTUES + self.VICES + self.SKILLS + self.META_TRAITS):
            raise HTTPException(status_code=404, detail="Trait not found")

        # Determine if it's a meta trait or regular trait
        is_meta = trait_name in self.META_TRAITS
        field_name = f"meta_traits.{trait_name}" if is_meta else f"traits.{trait_name}"

        # Update trait (with clamping to 0-100)
        await db.players.update_one(
            {"_id": player_id},
            {"$inc": {field_name: points}}
        )

        # Clamp to 100
        await db.players.update_one(
            {"_id": player_id, field_name: {"$gt": 100}},
            {"$set": {field_name: 100}}
        )

        # Get updated value
        player_dict = await db.players.find_one({"_id": player_id})
        player = Player(**player_dict)

        if is_meta:
            new_value = getattr(player.meta_traits, trait_name)
        else:
            new_value = getattr(player.traits, trait_name)

        return {
            "trait_name": trait_name,
            "points_added": points,
            "new_value": new_value,
            "message": f"{trait_name} increased by {points} points!"
        }