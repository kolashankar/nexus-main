"""Bonus calculation utilities"""

from typing import Dict


class BonusCalculator:
    """Utility class for calculating ornament bonuses"""

    # Bonus percentages
    CHAIN_BONUS = 3  # 3% per chain
    RING_BONUS = 7   # 7% per ring

    @classmethod
    def calculate_total_bonus(cls, chains: int, rings: int) -> float:
        """
        Calculate total bonus percentage from ornaments.
        
        Args:
            chains: Number of chains owned
            rings: Number of rings owned
            
        Returns:
            Total bonus percentage
        """
        return (chains * cls.CHAIN_BONUS) + (rings * cls.RING_BONUS)

    @classmethod
    def apply_bonus(cls, base_amount: int, chains: int, rings: int) -> Dict:
        """
        Apply bonus to a base amount.
        
        Args:
            base_amount: Base coin amount
            chains: Number of chains
            rings: Number of rings
            
        Returns:
            Dictionary with breakdown
        """
        total_bonus_percentage = cls.calculate_total_bonus(chains, rings)
        bonus_amount = int(base_amount * (total_bonus_percentage / 100))
        total_amount = base_amount + bonus_amount
        
        return {
            "base": base_amount,
            "bonus_percentage": total_bonus_percentage,
            "bonus_amount": bonus_amount,
            "total": total_amount
        }
