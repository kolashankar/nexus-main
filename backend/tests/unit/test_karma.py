"""Unit tests for karma system."""
from backend.services.karma.calculator import KarmaCalculator


class TestKarmaCalculation:
    """Test karma calculation logic."""

    def test_positive_action_increases_karma(self):
        """Test that positive actions increase karma."""
        calc = KarmaCalculator()

        karma_change = calc.calculate_action_karma(
            action_type="help",
            actor_karma=0,
            target_moral_class="poor",
            amount=100
        )

        assert karma_change > 0

    def test_negative_action_decreases_karma(self):
        """Test that negative actions decrease karma."""
        calc = KarmaCalculator()

        karma_change = calc.calculate_action_karma(
            action_type="steal",
            actor_karma=0,
            target_moral_class="good",
            amount=100
        )

        assert karma_change < 0

    def test_helping_poor_gives_more_karma(self):
        """Test that helping poor gives more karma than helping rich."""
        calc = KarmaCalculator()

        karma_poor = calc.calculate_action_karma(
            action_type="help",
            actor_karma=0,
            target_moral_class="poor",
            amount=100
        )

        karma_rich = calc.calculate_action_karma(
            action_type="help",
            actor_karma=0,
            target_moral_class="rich",
            amount=100
        )

        assert karma_poor > karma_rich

    def test_stealing_from_poor_more_negative(self):
        """Test that stealing from poor is more negative."""
        calc = KarmaCalculator()

        karma_poor = calc.calculate_action_karma(
            action_type="steal",
            actor_karma=0,
            target_moral_class="poor",
            amount=100
        )

        karma_rich = calc.calculate_action_karma(
            action_type="steal",
            actor_karma=0,
            target_moral_class="rich",
            amount=100
        )

        assert abs(karma_poor) > abs(karma_rich)

    def test_karma_scaling_with_amount(self):
        """Test that karma scales with action amount."""
        calc = KarmaCalculator()

        karma_small = calc.calculate_action_karma(
            action_type="help",
            actor_karma=0,
            target_moral_class="middle",
            amount=50
        )

        karma_large = calc.calculate_action_karma(
            action_type="help",
            actor_karma=0,
            target_moral_class="middle",
            amount=200
        )

        assert karma_large > karma_small


class TestKarmaClassification:
    """Test karma-based classification."""

    def test_determine_moral_class_good(self):
        """Test determining good moral class."""
        calc = KarmaCalculator()

        moral_class = calc.determine_moral_class(karma=600)
        assert moral_class == "good"

    def test_determine_moral_class_average(self):
        """Test determining average moral class."""
        calc = KarmaCalculator()

        moral_class = calc.determine_moral_class(karma=0)
        assert moral_class == "average"

    def test_determine_moral_class_bad(self):
        """Test determining bad moral class."""
        calc = KarmaCalculator()

        moral_class = calc.determine_moral_class(karma=-600)
        assert moral_class == "bad"

    def test_moral_class_boundaries(self):
        """Test moral class boundary values."""
        calc = KarmaCalculator()

        assert calc.determine_moral_class(499) == "average"
        assert calc.determine_moral_class(500) == "good"
        assert calc.determine_moral_class(-499) == "average"
        assert calc.determine_moral_class(-500) == "bad"