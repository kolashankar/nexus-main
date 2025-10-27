"""Trait analyzer for determining player alignment and characteristics"""

from typing import Dict, List, Tuple


class TraitAnalyzer:
    """Analyzes player traits to determine task generation parameters"""

    # Trait categories
    VIRTUES = [
        "compassion", "honesty", "courage", "wisdom", "justice",
        "temperance", "humility", "patience", "gratitude", "kindness",
        "loyalty", "generosity", "integrity", "respect", "forgiveness",
        "responsibility", "self-discipline", "perseverance", "empathy", "fairness"
    ]

    VICES = [
        "greed", "envy", "wrath", "pride", "lust",
        "gluttony", "sloth", "cruelty", "dishonesty", "cowardice",
        "arrogance", "impatience", "selfishness", "vengeance", "manipulation",
        "betrayal", "recklessness", "apathy", "prejudice", "corruption"
    ]

    SKILLS = [
        "combat", "stealth", "hacking", "persuasion", "intimidation",
        "crafting", "trading", "leadership", "strategy", "technology",
        "medicine", "engineering", "athletics", "investigation", "survival",
        "diplomacy", "deception", "perception", "lockpicking", "piloting"
    ]

    META_TRAITS = [
        "charisma", "intelligence", "strength", "agility", "endurance",
        "willpower", "luck", "creativity", "adaptability", "resilience",
        "focus", "reflexes", "intuition", "memory", "precision",
        "determination", "composure", "awareness", "coordination", "fortitude"
    ]

    @classmethod
    def analyze_player(cls, traits: Dict[str, int]) -> Dict[str, any]:
        """
        Analyze player traits to determine their alignment and characteristics.
        
        Args:
            traits: Dictionary of trait names to values (0-100)
            
        Returns:
            Dictionary containing analysis results
        """
        if not traits:
            return cls._default_analysis()

        # Separate traits by category
        player_virtues = {k: v for k, v in traits.items() if k.lower() in cls.VIRTUES}
        player_vices = {k: v for k, v in traits.items() if k.lower() in cls.VICES}
        player_skills = {k: v for k, v in traits.items() if k.lower() in cls.SKILLS}
        player_meta = {k: v for k, v in traits.items() if k.lower() in cls.META_TRAITS}

        # Calculate totals
        virtue_total = sum(player_virtues.values()) if player_virtues else 0
        vice_total = sum(player_vices.values()) if player_vices else 0

        # Determine alignment (karma value)
        karma_score = virtue_total - vice_total
        
        # Determine task type preference
        if karma_score > 50:
            task_preference = "good"
            alignment = "virtuous"
        elif karma_score < -50:
            task_preference = "bad"
            alignment = "corrupt"
        else:
            task_preference = "neutral"
            alignment = "balanced"

        # Get top traits
        top_virtues = cls._get_top_traits(player_virtues, 5)
        top_vices = cls._get_top_traits(player_vices, 5)
        top_skills = cls._get_top_traits(player_skills, 5)

        return {
            "karma_score": karma_score,
            "alignment": alignment,
            "task_preference": task_preference,
            "top_virtues": top_virtues,
            "top_vices": top_vices,
            "top_skills": top_skills,
            "virtue_total": virtue_total,
            "vice_total": vice_total
        }

    @staticmethod
    def _get_top_traits(traits: Dict[str, int], count: int) -> List[Tuple[str, int]]:
        """Get top N traits sorted by value"""
        if not traits:
            return []
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        return sorted_traits[:count]

    @classmethod
    def _default_analysis(cls) -> Dict[str, any]:
        """Return default analysis for players without traits"""
        return {
            "karma_score": 0,
            "alignment": "neutral",
            "task_preference": "neutral",
            "top_virtues": [],
            "top_vices": [],
            "top_skills": [],
            "virtue_total": 0,
            "vice_total": 0
        }
