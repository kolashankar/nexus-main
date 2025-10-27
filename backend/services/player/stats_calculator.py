"""Player statistics calculator service."""

from typing import Dict, Any
import math


class StatsCalculator:
    """Calculate player stats from traits and level."""

    @staticmethod
    def calculate_combat_stats(player: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate combat-related stats from player data.
        
        Args:
            player: Player document with traits and level
            
        Returns:
            Dictionary with calculated combat stats
        """
        traits = player.get('traits', {})
        meta_traits = player.get('meta_traits', {})
        level = player.get('level', 1)

        # Base stats
        strength = traits.get('physical_strength', 50)
        dexterity = traits.get('dexterity', 50)
        endurance = traits.get('endurance', 50)
        speed = traits.get('speed', 50)
        resilience = traits.get('resilience', 50)
        perception = traits.get('perception', 50)

        # Calculate derived stats
        hp = int((endurance * 10) + (level * 5))
        attack = int((strength + dexterity) / 2) + level
        defense = int((resilience + perception) / 2) + level
        evasion = int(speed / 2)
        crit_chance = min(50, int(perception / 4))  # Max 50%

        # Apply combat rating from meta traits
        combat_rating = meta_traits.get('combat_rating', 0)
        if combat_rating > 0:
            attack = int(attack * (1 + combat_rating / 100))
            defense = int(defense * (1 + combat_rating / 100))

        return {
            'hp': hp,
            'max_hp': hp,
            'attack': attack,
            'defense': defense,
            'evasion': evasion,
            'crit_chance': crit_chance,
            'combat_rating': combat_rating
        }

    @staticmethod
    def calculate_derived_traits(player: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived traits from base traits.
        
        Args:
            player: Player document with traits
            
        Returns:
            Dictionary with calculated derived traits
        """
        traits = player.get('traits', {})

        # Social derived traits
        charisma = traits.get('charisma', 50)
        kindness = traits.get('kindness', 50)
        honesty = traits.get('honesty', 50)
        deceit = traits.get('deceit', 50)

        # Calculate reputation (charisma + kindness - deceit)
        reputation = int((charisma + kindness - deceit) / 3)
        reputation = max(0, min(100, reputation))

        # Calculate influence (charisma + leadership)
        leadership = traits.get('leadership', 50)
        influence = int((charisma + leadership) / 2)

        # Calculate trustworthiness (honesty + integrity - deceit)
        integrity = traits.get('integrity', 50)
        trustworthiness = int((honesty + integrity - deceit) / 3)
        trustworthiness = max(0, min(100, trustworthiness))

        # Economic traits
        trading = traits.get('trading', 50)
        negotiation = traits.get('negotiation', 50)
        greed = traits.get('greed', 50)
        perception_trait = traits.get('perception', 50)

        business_acumen = int((trading + negotiation) / 2)
        market_intuition = int((trading + perception_trait) / 2)

        # Spiritual traits
        meditation = traits.get('meditation', 50)
        wisdom = traits.get('wisdom', 50)

        enlightenment = int((meditation + wisdom) / 2)

        return {
            'reputation': reputation,
            'influence': influence,
            'trustworthiness': trustworthiness,
            'business_acumen': business_acumen,
            'market_intuition': market_intuition,
            'enlightenment': enlightenment,
            'karmic_balance': 50  # Base value, adjusted by karma
        }

    @staticmethod
    def calculate_power_unlock_requirements(
        superpower: Dict[str, Any],
        player_traits: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check if player meets requirements for a superpower.
        
        Args:
            superpower: Superpower data with requirements
            player_traits: Player's current trait values
            
        Returns:
            Dictionary with unlock status and missing requirements
        """
        requirements = superpower.get('requirements', {})
        missing = []
        met = True

        for trait_name, required_value in requirements.items():
            player_value = player_traits.get(trait_name, 0)
            if player_value < required_value:
                met = False
                missing.append({
                    'trait': trait_name,
                    'required': required_value,
                    'current': player_value,
                    'difference': required_value - player_value
                })

        return {
            'unlockable': met,
            'missing_requirements': missing,
            'progress_percentage': StatsCalculator._calculate_progress_percentage(
                requirements, player_traits
            )
        }

    @staticmethod
    def _calculate_progress_percentage(
        requirements: Dict[str, int],
        player_traits: Dict[str, int]
    ) -> float:
        """Calculate overall progress towards meeting requirements."""
        if not requirements:
            return 100.0

        total_progress = 0
        for trait_name, required_value in requirements.items():
            current_value = player_traits.get(trait_name, 0)
            trait_progress = min(100, (current_value / required_value) * 100)
            total_progress += trait_progress

        return round(total_progress / len(requirements), 2)

    @staticmethod
    def calculate_level_progress(xp: int, level: int) -> Dict[str, Any]:
        """Calculate level progression.
        
        Args:
            xp: Current XP
            level: Current level
            
        Returns:
            Dictionary with level progression data
        """
        # XP formula: level^2 * 100
        current_level_xp = (level ** 2) * 100
        next_level_xp = ((level + 1) ** 2) * 100
        xp_needed = next_level_xp - xp
        xp_in_current_level = xp - current_level_xp
        level_progress = (xp_in_current_level / \
                          (next_level_xp - current_level_xp)) * 100

        return {
            'level': level,
            'xp': xp,
            'xp_needed_for_next': xp_needed,
            'xp_in_current_level': xp_in_current_level,
            'level_progress_percentage': round(level_progress, 2),
            'next_level_xp_threshold': next_level_xp
        }
