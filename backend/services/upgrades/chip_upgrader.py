from typing import Dict, Any
from datetime import datetime
from ..upgrades.cost_calculator import CostCalculator

"""
Chip Upgrader Service
Handles cyber chip/neural augmentation upgrade logic
"""

class ChipUpgrader:
    """Service for upgrading cyber chips and neural augmentations"""
    
    # Available chips with unlock requirements
    AVAILABLE_CHIPS = {
        'neural_enhancer': {'name': 'Neural Enhancer', 'unlock_level': 5},
        'combat_chip': {'name': 'Combat Chip', 'unlock_level': 10},
        'stealth_module': {'name': 'Stealth Module', 'unlock_level': 15},
        'hacking_chip': {'name': 'Hacking Chip', 'unlock_level': 20},
        'resource_optimizer': {'name': 'Resource Optimizer', 'unlock_level': 25},
        'quantum_processor': {'name': 'Quantum Processor', 'unlock_level': 40}
    }
    
    def __init__(self, db):
        self.db = db
        self.cost_calculator = CostCalculator
    
    async def upgrade_chip(self, player_id: str, chip_id: str) -> Dict[str, Any]:
        """
        Upgrade a player's chip
        
        Args:
            player_id: UUID of the player
            chip_id: ID of the chip to upgrade
            
        Returns:
            Upgrade result with new level and costs
        """
        # Validate chip
        if chip_id not in self.AVAILABLE_CHIPS:
            raise ValueError(f"Invalid chip: {chip_id}")
        
        # Get player data
        player = await self.db.players.find_one({'player_id': player_id})
        if not player:
            raise ValueError("Player not found")
        
        # Check unlock requirements
        chip_info = self.AVAILABLE_CHIPS[chip_id]
        player_level = player.get('level', 1)
        
        if player_level < chip_info['unlock_level']:
            raise ValueError(
                f"Player level {chip_info['unlock_level']} required to unlock {chip_info['name']}"
            )
        
        # Get current level (0 if not yet unlocked)
        chips = player.get('chips', {})
        chip_data = chips.get(chip_id, {'level': 0, 'unlocked': False})
        current_level = chip_data.get('level', 0)
        
        # Check if already at max level
        if self.cost_calculator.is_max_level(current_level):
            raise ValueError(f"{chip_info['name']} is already at maximum level")
        
        # Calculate cost
        cost_level = max(current_level, 1)
        cost = self.cost_calculator.calculate_upgrade_cost(cost_level, 'chip')
        
        # Get player currencies
        currencies = player.get('currencies', {})
        
        # Check if player can afford
        if not self.cost_calculator.can_afford(currencies, cost):
            raise ValueError("Insufficient resources")
        
        # Perform upgrade
        new_level = current_level + 1
        
        # Update player data
        update_result = await self.db.players.update_one(
            {'player_id': player_id},
            {
                '$set': {
                    f'chips.{chip_id}': {
                        'level': new_level,
                        'unlocked': True,
                        'name': chip_info['name']
                    }
                },
                '$inc': {
                    'currencies.credits': -cost['credits'],
                    'currencies.karma_tokens': -cost['karma_tokens'],
                    'currencies.dark_matter': -cost['dark_matter']
                }
            }
        )
        
        if update_result.modified_count == 0:
            raise ValueError("Failed to upgrade chip")
        
        # Record upgrade history
        await self._record_upgrade_history(
            player_id, 'chip', chip_id, chip_info['name'],
            current_level, new_level, cost
        )
        
        # Get updated currencies
        updated_player = await self.db.players.find_one({'player_id': player_id})
        remaining_currencies = updated_player.get('currencies', {})
        
        return {
            'success': True,
            'message': f"{chip_info['name']} {'installed' if current_level == 0 else 'upgraded'} successfully",
            'upgrade_type': 'chip',
            'item_id': chip_id,
            'chip_name': chip_info['name'],
            'old_level': current_level,
            'new_level': new_level,
            'cost': cost,
            'remaining_currencies': remaining_currencies,
            'timestamp': datetime.utcnow()
        }
    
    async def _record_upgrade_history(self, player_id: str, upgrade_type: str,
                                      item_id: str, item_name: str,
                                      old_level: int, new_level: int,
                                      cost: Dict[str, int]):
        """Record upgrade in player's upgrade history"""
        history_entry = {
            'player_id': player_id,
            'upgrade_type': upgrade_type,
            'item_id': item_id,
            'item_name': item_name,
            'old_level': old_level,
            'new_level': new_level,
            'cost': cost,
            'timestamp': datetime.utcnow()
        }
        
        await self.db.upgrade_history.insert_one(history_entry)
