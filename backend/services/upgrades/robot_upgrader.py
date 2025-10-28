from typing import Dict, Any
from datetime import datetime
from ..upgrades.cost_calculator import CostCalculator

"""
Robot Upgrader Service
Handles robot companion upgrade logic
"""

class RobotUpgrader:
    """Service for upgrading robot companions"""
    
    # Available robots with unlock requirements
    AVAILABLE_ROBOTS = {
        'scout': {'name': 'Scout Bot', 'unlock_level': 1},
        'combat': {'name': 'Combat Droid', 'unlock_level': 10},
        'hacker': {'name': 'Hacker Bot', 'unlock_level': 15},
        'medic': {'name': 'Medic Bot', 'unlock_level': 20},
        'trader': {'name': 'Trader Bot', 'unlock_level': 25},
        'guardian': {'name': 'Guardian Mech', 'unlock_level': 35}
    }
    
    def __init__(self, db):
        self.db = db
        self.cost_calculator = CostCalculator
    
    async def upgrade_robot(self, player_id: str, robot_id: str) -> Dict[str, Any]:
        """
        Upgrade a player's robot
        
        Args:
            player_id: UUID of the player
            robot_id: ID of the robot to upgrade
            
        Returns:
            Upgrade result with new level and costs
        """
        # Validate robot
        if robot_id not in self.AVAILABLE_ROBOTS:
            raise ValueError(f"Invalid robot: {robot_id}")
        
        # Get player data
        player = await self.db.players.find_one({'player_id': player_id})
        if not player:
            raise ValueError("Player not found")
        
        # Check unlock requirements
        robot_info = self.AVAILABLE_ROBOTS[robot_id]
        player_level = player.get('level', 1)
        
        if player_level < robot_info['unlock_level']:
            raise ValueError(
                f"Player level {robot_info['unlock_level']} required to unlock {robot_info['name']}"
            )
        
        # Get current level (0 if not yet unlocked)
        robots = player.get('robots', {})
        robot_data = robots.get(robot_id, {'level': 0, 'unlocked': False})
        current_level = robot_data.get('level', 0)
        
        # Check if already at max level
        if self.cost_calculator.is_max_level(current_level):
            raise ValueError(f"{robot_info['name']} is already at maximum level")
        
        # Calculate cost (use level 1 as base for first unlock)
        cost_level = max(current_level, 1)
        cost = self.cost_calculator.calculate_upgrade_cost(cost_level, 'robot')
        
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
                    f'robots.{robot_id}': {
                        'level': new_level,
                        'unlocked': True,
                        'name': robot_info['name']
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
            raise ValueError("Failed to upgrade robot")
        
        # Record upgrade history
        await self._record_upgrade_history(
            player_id, 'robot', robot_id, robot_info['name'],
            current_level, new_level, cost
        )
        
        # Get updated currencies
        updated_player = await self.db.players.find_one({'player_id': player_id})
        remaining_currencies = updated_player.get('currencies', {})
        
        return {
            'success': True,
            'message': f"{robot_info['name']} {'unlocked' if current_level == 0 else 'upgraded'} successfully",
            'upgrade_type': 'robot',
            'item_id': robot_id,
            'robot_name': robot_info['name'],
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
