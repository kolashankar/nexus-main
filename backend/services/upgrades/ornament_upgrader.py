from typing import Dict, Any
from datetime import datetime
from ..upgrades.cost_calculator import CostCalculator

"""
Ornament Upgrader Service
Handles ornament (cosmetic) upgrade logic
"""

class OrnamentUpgrader:
    """Service for upgrading ornaments and cosmetics"""
    
    # Available ornaments with unlock requirements
    AVAILABLE_ORNAMENTS = {
        'avatar_frame': {'name': 'Avatar Frame', 'unlock_level': 5},
        'title_banner': {'name': 'Title Banner', 'unlock_level': 10},
        'emote_pack': {'name': 'Emote Pack', 'unlock_level': 15},
        'victory_effect': {'name': 'Victory Effect', 'unlock_level': 20},
        'nameplate': {'name': 'Custom Nameplate', 'unlock_level': 25},
        'aura': {'name': 'Character Aura', 'unlock_level': 30}
    }
    
    def __init__(self, db):
        self.db = db
        self.cost_calculator = CostCalculator
    
    async def upgrade_ornament(self, player_id: str, ornament_id: str) -> Dict[str, Any]:
        """
        Upgrade a player's ornament
        
        Args:
            player_id: UUID of the player
            ornament_id: ID of the ornament to upgrade
            
        Returns:
            Upgrade result with new level and costs
        """
        # Validate ornament
        if ornament_id not in self.AVAILABLE_ORNAMENTS:
            raise ValueError(f"Invalid ornament: {ornament_id}")
        
        # Get player data
        player = await self.db.players.find_one({'player_id': player_id})
        if not player:
            raise ValueError("Player not found")
        
        # Check unlock requirements
        ornament_info = self.AVAILABLE_ORNAMENTS[ornament_id]
        player_level = player.get('level', 1)
        
        if player_level < ornament_info['unlock_level']:
            raise ValueError(
                f"Player level {ornament_info['unlock_level']} required to unlock {ornament_info['name']}"
            )
        
        # Get current level (0 if not yet unlocked)
        ornaments = player.get('ornaments', {})
        ornament_data = ornaments.get(ornament_id, {'level': 0, 'unlocked': False})
        current_level = ornament_data.get('level', 0)
        
        # Check if already at max level
        if self.cost_calculator.is_max_level(current_level):
            raise ValueError(f"{ornament_info['name']} is already at maximum level")
        
        # Calculate cost
        cost_level = max(current_level, 1)
        cost = self.cost_calculator.calculate_upgrade_cost(cost_level, 'ornament')
        
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
                    f'ornaments.{ornament_id}': {
                        'level': new_level,
                        'unlocked': True,
                        'name': ornament_info['name']
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
            raise ValueError("Failed to upgrade ornament")
        
        # Record upgrade history
        await self._record_upgrade_history(
            player_id, 'ornament', ornament_id, ornament_info['name'],
            current_level, new_level, cost
        )
        
        # Get updated currencies
        updated_player = await self.db.players.find_one({'player_id': player_id})
        remaining_currencies = updated_player.get('currencies', {})
        
        return {
            'success': True,
            'message': f"{ornament_info['name']} {'unlocked' if current_level == 0 else 'upgraded'} successfully",
            'upgrade_type': 'ornament',
            'item_id': ornament_id,
            'ornament_name': ornament_info['name'],
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
