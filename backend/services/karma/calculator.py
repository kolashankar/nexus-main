from typing import Dict, Optional

class KarmaCalculator:
    """Basic karma calculation service (rule-based, before AI)."""

    # Karma thresholds
    KARMA_LEVELS = {
        "saint": (2000, float('inf')),
        "virtuous": (1000, 2000),
        "good": (500, 1000),
        "neutral_good": (100, 500),
        "neutral": (-100, 100),
        "neutral_bad": (-500, -100),
        "bad": (-1000, -500),
        "evil": (-2000, -1000),
        "demon": (float('-inf'), -2000)
    }

    MORAL_CLASS_THRESHOLDS = {
        "good": 500,
        "bad": -500
    }

    def determine_moral_class(self, karma_points: int) -> str:
        """Determine moral class based on karma."""
        if karma_points >= self.MORAL_CLASS_THRESHOLDS["good"]:
            return "good"
        elif karma_points <= self.MORAL_CLASS_THRESHOLDS["bad"]:
            return "bad"
        else:
            return "average"

    def get_karma_level(self, karma_points: int) -> str:
        """Get karma level descriptor."""
        for level, (min_karma, max_karma) in self.KARMA_LEVELS.items():
            if min_karma <= karma_points < max_karma:
                return level
        return "neutral"

    def get_next_milestone(self, karma_points: int) -> Optional[int]:
        """Get next karma milestone."""
        milestones = [100, 500, 1000, 2000, 5000, -100, -500, -1000, -2000]

        if karma_points >= 0:
            # Find next positive milestone
            for milestone in sorted([m for m in milestones if m > 0]):
                if karma_points < milestone:
                    return milestone
        else:
            # Find next negative milestone
            for milestone in sorted([m for m in milestones if m < 0], reverse=True):
                if karma_points > milestone:
                    return milestone

        return None

    def calculate_karma_multiplier(
        self,
        actor_karma: int,
        target_karma: int,
        action_type: str
    ) -> float:
        """Calculate karma multiplier based on actor and target karma."""
        multiplier = 1.0

        # Actions against good people are worse
        if target_karma > 500 and action_type in ["hack", "steal"]:
            multiplier *= 1.5

        # Actions to help bad people give less karma
        if target_karma < -500 and action_type in ["help", "donate"]:
            multiplier *= 0.7

        # Repeated bad actions by bad people get less penalty (they're already evil)
        if actor_karma < -1000 and action_type in ["hack", "steal"]:
            multiplier *= 0.8

        return multiplier

    def calculate_trait_karma_bonus(self, traits: Dict[str, float]) -> int:
        """Calculate karma bonus based on trait composition."""
        # Virtuous traits give karma bonus
        virtue_bonus = int((
            traits.get("kindness", 50) +
            traits.get("generosity", 50) +
            traits.get("empathy", 50)
        ) / 10)

        # Vicious traits reduce karma
        vice_penalty = int((
            traits.get("greed", 50) +
            traits.get("cruelty", 50) +
            traits.get("deceit", 50)
        ) / 10)

        return virtue_bonus - vice_penalty