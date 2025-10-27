"""Unit tests for combat system."""
from backend.services.combat.calculator import CombatCalculator
from backend.models.combat.stats import calculate_combat_stats


class TestCombatStats:
    """Test combat stats calculation."""

    def test_calculate_hp_from_endurance(self):
        """Test HP calculation from endurance trait."""
        traits = {"endurance": 50}
        stats = calculate_combat_stats(traits)

        assert stats["hp"] == 500  # 50 * 10
        assert stats["max_hp"] == 500

    def test_calculate_attack_from_traits(self):
        """Test attack calculation from strength and dexterity."""
        traits = {
            "physical_strength": 60,
            "dexterity": 40
        }
        stats = calculate_combat_stats(traits)

        expected_attack = (60 + 40) / 2
        assert stats["attack"] == expected_attack

    def test_calculate_defense_from_traits(self):
        """Test defense calculation from resilience and perception."""
        traits = {
            "resilience": 70,
            "perception": 50
        }
        stats = calculate_combat_stats(traits)

        expected_defense = (70 + 50) / 2
        assert stats["defense"] == expected_defense

    def test_calculate_evasion_from_speed(self):
        """Test evasion calculation from speed trait."""
        traits = {"speed": 80}
        stats = calculate_combat_stats(traits)

        assert stats["evasion"] == 40  # 80 / 2


class TestDamageCalculation:
    """Test damage calculation."""

    def test_basic_damage_calculation(self):
        """Test basic damage without crits or evasion."""
        calc = CombatCalculator()

        attacker_stats = {"attack": 50}
        defender_stats = {"defense": 30, "evasion": 0}

        damage = calc.calculate_damage(
            attacker_stats,
            defender_stats,
            ability_modifier=1.0
        )

        assert damage > 0
        assert damage <= attacker_stats["attack"]

    def test_defense_reduces_damage(self):
        """Test that defense reduces incoming damage."""
        calc = CombatCalculator()

        attacker_stats = {"attack": 50}
        high_defense = {"defense": 40, "evasion": 0}
        low_defense = {"defense": 10, "evasion": 0}

        damage_high_def = calc.calculate_damage(attacker_stats, high_defense)
        damage_low_def = calc.calculate_damage(attacker_stats, low_defense)

        assert damage_high_def < damage_low_def

    def test_ability_modifier_increases_damage(self):
        """Test that ability modifiers increase damage."""
        calc = CombatCalculator()

        attacker_stats = {"attack": 50}
        defender_stats = {"defense": 20, "evasion": 0}

        normal_damage = calc.calculate_damage(
            attacker_stats,
            defender_stats,
            ability_modifier=1.0
        )

        boosted_damage = calc.calculate_damage(
            attacker_stats,
            defender_stats,
            ability_modifier=1.5
        )

        assert boosted_damage > normal_damage


class TestCombatRound:
    """Test combat round execution."""

    def test_execute_attack_reduces_hp(self):
        """Test that attacks reduce target HP."""
        calc = CombatCalculator()

        attacker = {
            "attack": 50,
            "hp": 500
        }

        defender = {
            "defense": 20,
            "evasion": 0,
            "hp": 500,
            "max_hp": 500
        }

        result = calc.execute_attack(attacker, defender)

        assert result["defender_hp"] < defender["hp"]
        assert result["damage"] > 0

    def test_hp_cannot_go_negative(self):
        """Test that HP doesn't go below 0."""
        calc = CombatCalculator()

        attacker = {"attack": 1000}
        defender = {
            "defense": 0,
            "evasion": 0,
            "hp": 100,
            "max_hp": 500
        }

        result = calc.execute_attack(attacker, defender)

        assert result["defender_hp"] >= 0