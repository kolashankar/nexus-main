"""Unit tests for superpower system."""
import pytest
from backend.services.player.superpowers import SuperpowerService
from backend.models.player.superpowers import SUPERPOWER_REQUIREMENTS


class TestSuperpowerUnlocking:
    """Test superpower unlocking logic."""

    def test_check_requirements_met(self):
        """Test checking if superpower requirements are met."""
        service = SuperpowerService()

        # Mind Reading requires: empathy 80%, perception 70%
        traits = {
            "empathy": 85,
            "perception": 75
        }

        can_unlock = service.can_unlock_power("mind_reading", traits)
        assert can_unlock is True

    def test_check_requirements_not_met(self):
        """Test checking when requirements are not met."""
        service = SuperpowerService()

        traits = {
            "empathy": 50,
            "perception": 60
        }

        can_unlock = service.can_unlock_power("mind_reading", traits)
        assert can_unlock is False

    def test_unlock_power_basic(self):
        """Test unlocking a superpower."""
        service = SuperpowerService()

        traits = {
            "empathy": 85,
            "perception": 75
        }

        superpowers = []
        updated_powers = service.unlock_power(
            "mind_reading", superpowers, traits)

        assert len(updated_powers) == 1
        assert updated_powers[0]["name"] == "mind_reading"
        assert updated_powers[0]["tier"] == 1

    def test_cannot_unlock_same_power_twice(self):
        """Test that same power cannot be unlocked twice."""
        service = SuperpowerService()

        traits = {
            "empathy": 85,
            "perception": 75
        }

        superpowers = [
            {"name": "mind_reading", "tier": 1}
        ]

        with pytest.raises(ValueError):
            service.unlock_power("mind_reading", superpowers, traits)


class TestSuperpowerTiers:
    """Test superpower tier system."""

    def test_tier_1_powers_easier_to_unlock(self):
        """Test that tier 1 powers have lower requirements."""
        SuperpowerService()

        tier1_reqs = SUPERPOWER_REQUIREMENTS["mind_reading"]
        tier3_reqs = SUPERPOWER_REQUIREMENTS["time_slow"]

        # Tier 1 should have lower requirements
        tier1_total = sum(tier1_reqs.values())
        tier3_total = sum(tier3_reqs.values())

        assert tier1_total < tier3_total

    def test_get_available_powers(self):
        """Test getting list of available powers to unlock."""
        service = SuperpowerService()

        traits = {
            "empathy": 85,
            "perception": 75,
            "speed": 80,
            "dexterity": 75
        }

        superpowers = []
        available = service.get_available_powers(traits, superpowers)

        assert len(available) > 0
        assert "mind_reading" in available
        assert "enhanced_reflexes" in available


class TestSuperpowerCooldowns:
    """Test superpower cooldown system."""

    def test_power_has_cooldown_after_use(self):
        """Test that power goes on cooldown after use."""
        service = SuperpowerService()

        power = {
            "name": "mind_reading",
            "tier": 1,
            "usage_count": 0,
            "cooldown_until": None
        }

        updated_power = service.use_power(power)

        assert updated_power["usage_count"] == 1
        assert updated_power["cooldown_until"] is not None

    def test_cannot_use_power_on_cooldown(self):
        """Test that power cannot be used while on cooldown."""
        service = SuperpowerService()
        from datetime import datetime, timedelta

        power = {
            "name": "mind_reading",
            "tier": 1,
            "usage_count": 1,
            "cooldown_until": datetime.utcnow() + timedelta(hours=1)
        }

        can_use = service.is_power_available(power)
        assert can_use is False

    def test_power_available_after_cooldown(self):
        """Test that power becomes available after cooldown."""
        service = SuperpowerService()
        from datetime import datetime, timedelta

        power = {
            "name": "mind_reading",
            "tier": 1,
            "usage_count": 1,
            "cooldown_until": datetime.utcnow() - timedelta(hours=1)
        }

        can_use = service.is_power_available(power)
        assert can_use is True