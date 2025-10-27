"""Unit tests for traits system."""
from backend.services.player.traits import TraitService
from backend.models.player.player import initialize_traits, VIRTUES, VICES, SKILLS


class TestTraitInitialization:
    """Test trait initialization."""

    def test_initialize_traits_structure(self):
        """Test that initialize_traits returns correct structure."""
        traits = initialize_traits()

        assert isinstance(traits, dict)
        assert len(traits) == 60  # 20 virtues + 20 vices + 20 skills

    def test_all_virtues_present(self):
        """Test that all virtues are initialized."""
        traits = initialize_traits()

        for virtue in VIRTUES:
            assert virtue in traits
            assert 0 <= traits[virtue] <= 100

    def test_all_vices_present(self):
        """Test that all vices are initialized."""
        traits = initialize_traits()

        for vice in VICES:
            assert vice in traits
            assert 0 <= traits[vice] <= 100

    def test_all_skills_present(self):
        """Test that all skills are initialized."""
        traits = initialize_traits()

        for skill in SKILLS:
            assert skill in traits
            assert 0 <= traits[skill] <= 100

    def test_default_values_range(self):
        """Test that default trait values are in valid range."""
        traits = initialize_traits()

        for trait_name, value in traits.items():
            assert 0 <= value <= 100, f"{trait_name} has invalid value: {value}"


class TestTraitModification:
    """Test trait modification logic."""

    def test_increase_trait(self):
        """Test increasing a trait value."""
        service = TraitService()
        traits = initialize_traits()

        original_value = traits["empathy"]
        changes = {"empathy": 10}

        updated_traits = service.apply_trait_changes(traits, changes)

        assert updated_traits["empathy"] == original_value + 10

    def test_decrease_trait(self):
        """Test decreasing a trait value."""
        service = TraitService()
        traits = initialize_traits()
        traits["empathy"] = 50

        changes = {"empathy": -10}
        updated_traits = service.apply_trait_changes(traits, changes)

        assert updated_traits["empathy"] == 40

    def test_trait_cap_at_100(self):
        """Test that traits are capped at 100."""
        service = TraitService()
        traits = initialize_traits()
        traits["empathy"] = 95

        changes = {"empathy": 10}
        updated_traits = service.apply_trait_changes(traits, changes)

        assert updated_traits["empathy"] == 100

    def test_trait_floor_at_0(self):
        """Test that traits have a floor at 0."""
        service = TraitService()
        traits = initialize_traits()
        traits["empathy"] = 5

        changes = {"empathy": -10}
        updated_traits = service.apply_trait_changes(traits, changes)

        assert updated_traits["empathy"] == 0

    def test_multiple_trait_changes(self):
        """Test applying multiple trait changes at once."""
        service = TraitService()
        traits = initialize_traits()

        changes = {
            "empathy": 10,
            "greed": -5,
            "hacking": 15
        }

        updated_traits = service.apply_trait_changes(traits, changes)

        assert updated_traits["empathy"] == traits["empathy"] + 10
        assert updated_traits["greed"] == max(0, traits["greed"] - 5)
        assert updated_traits["hacking"] == min(100, traits["hacking"] + 15)