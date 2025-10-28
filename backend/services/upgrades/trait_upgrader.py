from typing import Dict, Any
from datetime import datetime
from ..upgrades.cost_calculator import CostCalculator

"""
Trait Upgrader Service
Handles trait upgrade logic and validation
"""

class TraitUpgrader:
    """Service for upgrading player traits"""
    
    # Available traits
    AVAILABLE_TRAITS = [
        'strength', 'hacking', 'charisma', 'stealth', 'intelligence', 'luck'
    ]
    
    def __init__(self, db):
        self.db = db
        self.cost_calculator = CostCalculator
    
    async def upgrade_trait(self, player_id: str, trait_id: str) -> Dict[str, Any]:
        """
        Upgrade a player's trait
        
        Args:
            player_id: UUID of the player
            trait_id: ID of the trait to upgrade
            
        Returns:
            Upgrade result with new level and costs
            
        Raises:
            ValueError: If trait is invalid or player cannot afford
        """
        # Validate trait
        if trait_id not in self.AVAILABLE_TRAITS:
            raise ValueError(f"Invalid trait: {trait_id}")
        
        # Get player data
        player = await self.db.players.find_one({'player_id': player_id})
        if not player:
            raise ValueError("Player not found")
        
        # Get current level
        current_level = player.get('traits', {}).get(trait_id, 1)
        
        # Check if already at max level
        if self.cost_calculator.is_max_level(current_level):
            raise ValueError(f"{trait_id} is already at maximum level")
        
        # Calculate cost
        cost = self.cost_calculator.calculate_upgrade_cost(current_level, 'trait')
        
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
                    f'traits.{trait_id}': new_level
                },
                '$inc': {
                    'currencies.credits': -cost['credits'],
                    'currencies.karma_tokens': -cost['karma_tokens'],
                    'currencies.dark_matter': -cost['dark_matter']
                }
            }
        )
        
        if update_result.modified_count == 0:
            raise ValueError("Failed to upgrade trait")
        
        # Record upgrade history
        await self._record_upgrade_history(
            player_id, 'trait', trait_id, trait_id.capitalize(), 
            current_level, new_level, cost
        )
        
        # Get updated currencies
        updated_player = await self.db.players.find_one({'player_id': player_id})
        remaining_currencies = updated_player.get('currencies', {})
        
        return {
            'success': True,
            'message': f'{trait_id.capitalize()} upgraded successfully',
            'upgrade_type': 'trait',
            'item_id': trait_id,
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
    
    async def get_trait_level(self, player_id: str, trait_id: str) -> int:
        """Get current level of a trait"""
        player = await self.db.players.find_one({'player_id': player_id})
        if not player:
            return 1
        return player.get('traits', {}).get(trait_id, 1)
