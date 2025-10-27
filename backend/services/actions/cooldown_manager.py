"""Action cooldown management service."""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId


class CooldownManager:
    """Manage action cooldowns."""

    # Cooldown durations in seconds
    COOLDOWNS = {
        'hack': 300,      # 5 minutes
        'steal': 600,     # 10 minutes
        'help': 60,       # 1 minute
        'donate': 120,    # 2 minutes
        'trade': 180,     # 3 minutes
        'attack': 300,    # 5 minutes
        'use_superpower': 3600,  # 1 hour (varies by power)
    }

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize cooldown manager.
        
        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.players = db.players
        self.cooldowns = db.action_cooldowns

    async def set_cooldown(
        self,
        player_id: str,
        action_type: str,
        duration_seconds: Optional[int] = None
    ) -> datetime:
        """Set cooldown for an action.
        
        Args:
            player_id: Player ID
            action_type: Type of action
            duration_seconds: Optional custom duration (uses default if not provided)
            
        Returns:
            Datetime when cooldown expires
        """
        duration = duration_seconds or self.COOLDOWNS.get(action_type, 60)
        expires_at = datetime.utcnow() + timedelta(seconds=duration)

        await self.cooldowns.update_one(
            {
                'player_id': player_id,
                'action_type': action_type
            },
            {
                '$set': {
                    'player_id': player_id,
                    'action_type': action_type,
                    'expires_at': expires_at,
                    'set_at': datetime.utcnow()
                }
            },
            upsert=True
        )

        return expires_at

    async def check_cooldown(self, player_id: str, action_type: str) -> Dict[str, Any]:
        """Check if action is on cooldown.
        
        Args:
            player_id: Player ID
            action_type: Type of action
            
        Returns:
            Dictionary with cooldown status
        """
        cooldown = await self.cooldowns.find_one({
            'player_id': player_id,
            'action_type': action_type
        })

        if not cooldown:
            return {
                'on_cooldown': False,
                'can_perform': True,
                'expires_at': None,
                'remaining_seconds': 0
            }

        expires_at = cooldown['expires_at']
        now = datetime.utcnow()

        if now >= expires_at:
            # Cooldown expired, clean up
            await self.cooldowns.delete_one({'_id': cooldown['_id']})
            return {
                'on_cooldown': False,
                'can_perform': True,
                'expires_at': None,
                'remaining_seconds': 0
            }

        remaining = (expires_at - now).total_seconds()

        return {
            'on_cooldown': True,
            'can_perform': False,
            'expires_at': expires_at,
            'remaining_seconds': int(remaining),
            'remaining_minutes': round(remaining / 60, 1)
        }

    async def clear_cooldown(self, player_id: str, action_type: str) -> bool:
        """Clear a cooldown (admin use or special items).
        
        Args:
            player_id: Player ID
            action_type: Type of action
            
        Returns:
            True if cooldown was cleared
        """
        result = await self.cooldowns.delete_one({
            'player_id': player_id,
            'action_type': action_type
        })

        return result.deleted_count > 0

    async def get_all_cooldowns(self, player_id: str) -> Dict[str, Dict[str, Any]]:
        """Get all active cooldowns for a player.
        
        Args:
            player_id: Player ID
            
        Returns:
            Dictionary of action types to cooldown info
        """
        cursor = self.cooldowns.find({'player_id': player_id})
        cooldowns = {}
        now = datetime.utcnow()

        async for cooldown in cursor:
            expires_at = cooldown['expires_at']

            if now < expires_at:
                remaining = (expires_at - now).total_seconds()
                cooldowns[cooldown['action_type']] = {
                    'expires_at': expires_at,
                    'remaining_seconds': int(remaining),
                    'remaining_minutes': round(remaining / 60, 1)
                }
            else:
                # Clean up expired cooldown
                await self.cooldowns.delete_one({'_id': cooldown['_id']})

        return cooldowns

    async def reduce_cooldown(
        self,
        player_id: str,
        action_type: str,
        reduction_seconds: int
    ) -> Dict[str, Any]:
        """Reduce cooldown time (power/item effect).
        
        Args:
            player_id: Player ID
            action_type: Type of action
            reduction_seconds: Seconds to reduce
            
        Returns:
            Updated cooldown info
        """
        cooldown = await self.cooldowns.find_one({
            'player_id': player_id,
            'action_type': action_type
        })

        if not cooldown:
            return {'on_cooldown': False}

        new_expires_at = cooldown['expires_at'] - \
            timedelta(seconds=reduction_seconds)
        now = datetime.utcnow()

        if new_expires_at <= now:
            # Cooldown completely removed
            await self.cooldowns.delete_one({'_id': cooldown['_id']})
            return {
                'on_cooldown': False,
                'can_perform': True,
                'removed': True
            }

        # Update cooldown
        await self.cooldowns.update_one(
            {'_id': cooldown['_id']},
            {'$set': {'expires_at': new_expires_at}}
        )

        remaining = (new_expires_at - now).total_seconds()

        return {
            'on_cooldown': True,
            'can_perform': False,
            'expires_at': new_expires_at,
            'remaining_seconds': int(remaining),
            'reduced_by': reduction_seconds
        }

    async def cleanup_expired_cooldowns(self) -> int:
        """Clean up all expired cooldowns (maintenance task).
        
        Returns:
            Number of cooldowns cleaned up
        """
        result = await self.cooldowns.delete_many({
            'expires_at': {'$lt': datetime.utcnow()}
        })

        return result.deleted_count
