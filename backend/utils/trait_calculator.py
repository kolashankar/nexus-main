"""Trait calculation utilities."""

from typing import Dict, List, Tuple, Any
import math


class TraitCalculator:
    """Utility functions for trait calculations."""

    # Trait categories
    VIRTUES = [
        'empathy', 'integrity', 'discipline', 'creativity', 'resilience',
        'curiosity', 'kindness', 'courage', 'patience', 'adaptability',
        'wisdom', 'humility', 'vision', 'honesty', 'loyalty',
        'generosity', 'self_awareness', 'gratitude', 'optimism', 'loveability'
    ]

    VICES = [
        'greed', 'arrogance', 'deceit', 'cruelty', 'selfishness',
        'envy', 'wrath', 'cowardice', 'laziness', 'gluttony',
        'paranoia', 'impulsiveness', 'vengefulness', 'manipulation', 'prejudice',
        'betrayal', 'stubbornness', 'pessimism', 'recklessness', 'vanity'
    ]

    SKILLS = [
        'hacking', 'negotiation', 'stealth', 'leadership', 'technical_knowledge',
        'physical_strength', 'speed', 'intelligence', 'charisma', 'perception',
        'endurance', 'dexterity', 'memory', 'focus', 'networking',
        'strategy', 'trading', 'engineering', 'medicine', 'meditation'
    ]

    @staticmethod
    def get_trait_category(trait_name: str) -> str:
        """Get the category of a trait.
        
        Args:
            trait_name: Name of the trait
            
        Returns:
            Category: 'virtue', 'vice', 'skill', or 'unknown'
        """
        if trait_name in TraitCalculator.VIRTUES:
            return 'virtue'
        elif trait_name in TraitCalculator.VICES:
            return 'vice'
        elif trait_name in TraitCalculator.SKILLS:
            return 'skill'
        return 'unknown'

    @staticmethod
    def calculate_moral_alignment(traits: Dict[str, int]) -> Tuple[str, int]:
        """Calculate moral alignment from traits.
        
        Args:
            traits: Dictionary of trait values
            
        Returns:
            Tuple of (alignment_name, alignment_score)
        """
        virtue_sum = sum(
            traits.get(v, 50) for v in TraitCalculator.VIRTUES
        )
        vice_sum = sum(
            traits.get(v, 50) for v in TraitCalculator.VICES
        )

        virtue_avg = virtue_sum / len(TraitCalculator.VIRTUES)
        vice_avg = vice_sum / len(TraitCalculator.VICES)

        # Alignment score (-100 to +100)
        alignment_score = int(virtue_avg - vice_avg)

        if alignment_score > 20:
            return ('good', alignment_score)
        elif alignment_score < -20:
            return ('bad', alignment_score)
        else:
            return ('average', alignment_score)

    @staticmethod
    def calculate_trait_balance(traits: Dict[str, int]) -> Dict[str, Any]:
        """Calculate overall trait balance.
        
        Args:
            traits: Dictionary of trait values
            
        Returns:
            Dictionary with balance metrics
        """
        values = list(traits.values())
        if not values:
            return {
                'balance_score': 0,
                'spread': 0,
                'specialization': 0
            }

        avg = sum(values) / len(values)
        variance = sum((x - avg) ** 2 for x in values) / len(values)
        std_dev = math.sqrt(variance)

        # Balance score (0-100, higher = more balanced)
        balance_score = max(0, 100 - (std_dev / 50 * 100))

        # Spread (how wide the trait range is)
        spread = max(values) - min(values)

        # Specialization (how focused on specific traits)
        high_traits = [v for v in values if v > 80]
        specialization = len(high_traits)

        return {
            'balance_score': round(balance_score, 2),
            'spread': spread,
            'specialization': specialization,
            'average': round(avg, 2),
            'std_deviation': round(std_dev, 2)
        }

    @staticmethod
    def get_dominant_traits(traits: Dict[str, int], count: int = 5) -> List[Tuple[str, int]]:
        """Get the most dominant traits.
        
        Args:
            traits: Dictionary of trait values
            count: Number of top traits to return
            
        Returns:
            List of (trait_name, value) tuples
        """
        sorted_traits = sorted(
            traits.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_traits[:count]

    @staticmethod
    def get_weakest_traits(traits: Dict[str, int], count: int = 5) -> List[Tuple[str, int]]:
        """Get the weakest traits.
        
        Args:
            traits: Dictionary of trait values
            count: Number of bottom traits to return
            
        Returns:
            List of (trait_name, value) tuples
        """
        sorted_traits = sorted(
            traits.items(),
            key=lambda x: x[1]
        )
        return sorted_traits[:count]

    @staticmethod
    def suggest_trait_improvements(traits: Dict[str, int]) -> List[Dict[str, Any]]:
        """Suggest traits that should be improved.
        
        Args:
            traits: Dictionary of trait values
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Get weakest traits
        weak_traits = TraitCalculator.get_weakest_traits(traits, 3)

        for trait_name, value in weak_traits:
            if value < 40:
                category = TraitCalculator.get_trait_category(trait_name)
                suggestions.append({
                    'trait': trait_name,
                    'current_value': value,
                    'suggested_target': 50,
                    'priority': 'high' if value < 25 else 'medium',
                    'category': category
                })

        return suggestions

    @staticmethod
    def calculate_synergies(traits: Dict[str, int]) -> List[Dict[str, Any]]:
        """Calculate trait synergies.
        
        Args:
            traits: Dictionary of trait values
            
        Returns:
            List of active synergies
        """
        synergies = []

        # Hacker synergy (hacking + technical_knowledge + intelligence)
        if all(traits.get(t, 0) > 70 for t in ['hacking', 'technical_knowledge', 'intelligence']):
            synergies.append({
                'name': 'Master Hacker',
                'traits': ['hacking', 'technical_knowledge', 'intelligence'],
                'bonus': 'Hacking actions 25% more effective'
            })

        # Leader synergy (leadership + charisma + vision)
        if all(traits.get(t, 0) > 70 for t in ['leadership', 'charisma', 'vision']):
            synergies.append({
                'name': 'Inspirational Leader',
                'traits': ['leadership', 'charisma', 'vision'],
                'bonus': 'Guild members gain +10% effectiveness'
            })

        # Warrior synergy (physical_strength + courage + endurance)
        if all(traits.get(t, 0) > 70 for t in ['physical_strength', 'courage', 'endurance']):
            synergies.append({
                'name': 'Fearless Warrior',
                'traits': ['physical_strength', 'courage', 'endurance'],
                'bonus': '+20% combat effectiveness'
            })

        # Sage synergy (wisdom + meditation + patience)
        if all(traits.get(t, 0) > 70 for t in ['wisdom', 'meditation', 'patience']):
            synergies.append({
                'name': 'Enlightened Sage',
                'traits': ['wisdom', 'meditation', 'patience'],
                'bonus': 'Karma gains +15%'
            })

        return synergies
