from typing import Dict, Tuple, Any
from backend.models.player.legacy import (
    PlayerLegacy, LegacyTitle, HeirloomItem, LegacyPerk
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Available legacy perks
LEGACY_PERKS = [
    LegacyPerk(
        perk_id="xp_boost_1",
        name="Experience Boost I",
        description="+10% XP gain on all new characters",
        bonus_type="xp_boost",
        bonus_value=0.10,
        cost=100
    ),
    LegacyPerk(
        perk_id="xp_boost_2",
        name="Experience Boost II",
        description="+25% XP gain on all new characters",
        bonus_type="xp_boost",
        bonus_value=0.25,
        cost=250
    ),
    LegacyPerk(
        perk_id="karma_multiplier_1",
        name="Karma Multiplier I",
        description="+15% karma gain on all characters",
        bonus_type="karma_multiplier",
        bonus_value=0.15,
        cost=150
    ),
    LegacyPerk(
        perk_id="trait_boost_1",
        name="Trait Growth I",
        description="+5% faster trait improvement",
        bonus_type="trait_gain_bonus",
        bonus_value=0.05,
        cost=200
    ),
    LegacyPerk(
        perk_id="starting_wealth",
        name="Trust Fund",
        description="Start new characters with 10,000 credits",
        bonus_type="starting_wealth",
        bonus_value=10000,
        cost=300
    ),
    LegacyPerk(
        perk_id="skill_points_bonus",
        name="Head Start",
        description="Start with +10 skill points",
        bonus_type="skill_points",
        bonus_value=10,
        cost=250
    ),
    LegacyPerk(
        perk_id="mentor_mastery",
        name="Master Mentor",
        description="+50% mentorship rewards",
        bonus_type="mentorship_bonus",
        bonus_value=0.50,
        cost=200
    ),
    LegacyPerk(
        perk_id="achievement_hunter",
        name="Achievement Hunter",
        description="+20% achievement point rewards",
        bonus_type="achievement_bonus",
        bonus_value=0.20,
        cost=175
    ),
]

class LegacyService:
    """Service for managing cross-season legacy system"""

    @staticmethod
    def initialize_legacy(account_id: str) -> PlayerLegacy:
        """Initialize legacy for a new account"""
        return PlayerLegacy(account_id=account_id)

    @staticmethod
    def earn_legacy_points(
        player_legacy: PlayerLegacy,
        amount: int,
        source: str
    ) -> Tuple[bool, str]:
        """Award legacy points"""
        player_legacy.earn_legacy_points(amount, source)

        level_up = False
        points_for_next = player_legacy.legacy_level * 1000
        if player_legacy.lifetime_legacy_points >= points_for_next:
            level_up = True

        message = f"Earned {amount} legacy points from {source}"
        if level_up:
            message += f" | Legacy Level Up: {player_legacy.legacy_level}"

        return True, message

    @staticmethod
    def unlock_perk(
        player_legacy: PlayerLegacy,
        perk_id: str
    ) -> Tuple[bool, str]:
        """Unlock a legacy perk"""
        # Find perk
        perk = next((p for p in LEGACY_PERKS if p.perk_id == perk_id), None)
        if not perk:
            return False, "Perk not found"

        # Check if already unlocked
        if any(p.perk_id == perk_id for p in player_legacy.unlocked_perks):
            return False, "Perk already unlocked"

        # Check if player has enough points
        if player_legacy.legacy_points < perk.cost:
            return False, f"Not enough legacy points (need {perk.cost}, have {player_legacy.legacy_points})"

        # Spend points and unlock
        if not player_legacy.spend_legacy_points(perk.cost):
            return False, "Failed to spend legacy points"

        perk.unlocked = True
        player_legacy.unlocked_perks.append(perk)

        return True, f"Unlocked {perk.name}!"

    @staticmethod
    def activate_perk(
        player_legacy: PlayerLegacy,
        perk_id: str
    ) -> Tuple[bool, str]:
        """Activate a legacy perk"""
        # Check if perk is unlocked
        if not any(p.perk_id == perk_id for p in player_legacy.unlocked_perks):
            return False, "Perk not unlocked"

        # Check if already active
        if perk_id in player_legacy.active_perks:
            return False, "Perk already active"

        # Activate
        player_legacy.active_perks.append(perk_id)
        return True, "Perk activated"

    @staticmethod
    def add_legacy_title(
        player_legacy: PlayerLegacy,
        title_id: str,
        title_name: str,
        description: str,
        season: int
    ) -> Tuple[bool, str]:
        """Add a legacy title"""
        title = LegacyTitle(
            title_id=title_id,
            name=title_name,
            description=description,
            earned_at=datetime.utcnow(),
            season_earned=season
        )

        player_legacy.add_title(title)
        return True, f"Earned legacy title: {title_name}"

    @staticmethod
    def add_heirloom(
        player_legacy: PlayerLegacy,
        item_id: str,
        name: str,
        description: str,
        power_level: int,
        season: int
    ) -> Tuple[bool, str]:
        """Add an heirloom item"""
        heirloom = HeirloomItem(
            item_id=item_id,
            name=name,
            description=description,
            power_level=power_level,
            season_acquired=season
        )

        player_legacy.heirloom_items.append(heirloom)
        return True, f"Acquired heirloom: {name}"

    @staticmethod
    def update_mentorship(
        player_legacy: PlayerLegacy,
        apprentice_graduated: bool = False
    ):
        """Update mentorship statistics"""
        if apprentice_graduated:
            player_legacy.apprentices_taught += 1
            player_legacy.mentorship_rewards_earned += 50

            # Level up mentorship
            if player_legacy.apprentices_taught % 5 == 0:
                player_legacy.mentorship_level += 1

    @staticmethod
    def get_legacy_summary(player_legacy: PlayerLegacy) -> Dict:
        """Get legacy system summary"""
        return {
            "legacy_level": player_legacy.legacy_level,
            "legacy_points": player_legacy.legacy_points,
            "lifetime_points": player_legacy.lifetime_legacy_points,
            "seasons_played": player_legacy.seasons_played,
            "titles_earned": len(player_legacy.earned_titles),
            "active_title": player_legacy.active_title,
            "heirlooms": len(player_legacy.heirloom_items),
            "unlocked_perks": len(player_legacy.unlocked_perks),
            "active_perks": player_legacy.active_perks,
            "mentorship_level": player_legacy.mentorship_level,
            "apprentices_taught": player_legacy.apprentices_taught,
            "achievements": player_legacy.total_achievements
        }

    @staticmethod
    def apply_new_character_bonuses(
        player_legacy: PlayerLegacy
    ) -> Dict[str, Any]:
        """Apply legacy bonuses to a new character"""
        bonuses = {
            "xp_multiplier": 1.0,
            "karma_multiplier": 1.0,
            "trait_multiplier": 1.0,
            "starting_credits": 1000,
            "starting_skill_points": 0
        }

        for perk in player_legacy.unlocked_perks:
            if not perk.unlocked or perk.perk_id not in player_legacy.active_perks:
                continue

            if perk.bonus_type == "xp_boost":
                bonuses["xp_multiplier"] += perk.bonus_value
            elif perk.bonus_type == "karma_multiplier":
                bonuses["karma_multiplier"] += perk.bonus_value
            elif perk.bonus_type == "trait_gain_bonus":
                bonuses["trait_multiplier"] += perk.bonus_value
            elif perk.bonus_type == "starting_wealth":
                bonuses["starting_credits"] += int(perk.bonus_value)
            elif perk.bonus_type == "skill_points":
                bonuses["starting_skill_points"] += int(perk.bonus_value)

        return bonuses
