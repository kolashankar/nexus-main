from typing import Dict, Any
import math

"""
Cost Calculator Service
Handles exponential cost calculations for all upgrade types
"""

class CostCalculator:
    """Calculate upgrade costs with exponential scaling"""
    
    # Base costs for each upgrade type
    BASE_COSTS = {
        'trait': {
            'credits': 100,
            'karma_tokens': 10,
            'dark_matter': 1
        },
        'robot': {
            'credits': 200,
            'karma_tokens': 20,
            'dark_matter': 2
        },
        'ornament': {
            'credits': 150,
            'karma_tokens': 15,
            'dark_matter': 1
        },
        'chip': {
            'credits': 250,
            'karma_tokens': 25,
            'dark_matter': 3
        }
    }
    
    # Exponential multiplier (1.15 means 15% increase per level)
    COST_MULTIPLIER = 1.15
    
    # Maximum level for all upgrades
    MAX_LEVEL = 100
    
    @classmethod
    def calculate_upgrade_cost(cls, current_level: int, upgrade_type: str) -> Dict[str, int]:
        """
        Calculate the cost to upgrade from current level to next level
        
        Formula: cost = base_cost * (multiplier ^ current_level)
        
        Args:
            current_level: Current level of the item
            upgrade_type: Type of upgrade (trait, robot, ornament, chip)
            
        Returns:
            Dictionary with credits, karma_tokens, and dark_matter costs
        """
        if current_level >= cls.MAX_LEVEL:
            return {'credits': 0, 'karma_tokens': 0, 'dark_matter': 0}
        
        base_costs = cls.BASE_COSTS.get(upgrade_type, cls.BASE_COSTS['trait'])
        multiplier = math.pow(cls.COST_MULTIPLIER, current_level)
        
        return {
            'credits': math.floor(base_costs['credits'] * multiplier),
            'karma_tokens': math.floor(base_costs['karma_tokens'] * multiplier),
            'dark_matter': math.floor(base_costs['dark_matter'] * multiplier)
        }
    
    @classmethod
    def calculate_total_cost(cls, from_level: int, to_level: int, upgrade_type: str) -> Dict[str, int]:
        """
        Calculate total cost to upgrade from one level to another
        
        Args:
            from_level: Starting level
            to_level: Target level
            upgrade_type: Type of upgrade
            
        Returns:
            Total cost dictionary
        """
        total_cost = {'credits': 0, 'karma_tokens': 0, 'dark_matter': 0}
        
        for level in range(from_level, min(to_level, cls.MAX_LEVEL)):
            cost = cls.calculate_upgrade_cost(level, upgrade_type)
            total_cost['credits'] += cost['credits']
            total_cost['karma_tokens'] += cost['karma_tokens']
            total_cost['dark_matter'] += cost['dark_matter']
        
        return total_cost
    
    @classmethod
    def can_afford(cls, player_currencies: Dict[str, int], cost: Dict[str, int]) -> bool:
        """
        Check if player can afford the upgrade
        
        Args:
            player_currencies: Player's current currencies
            cost: Required cost
            
        Returns:
            True if player can afford, False otherwise
        """
        return (
            player_currencies.get('credits', 0) >= cost['credits'] and
            player_currencies.get('karma_tokens', 0) >= cost['karma_tokens'] and
            player_currencies.get('dark_matter', 0) >= cost['dark_matter']
        )
    
    @classmethod
    def is_max_level(cls, level: int) -> bool:
        """Check if item is at max level"""
        return level >= cls.MAX_LEVEL
