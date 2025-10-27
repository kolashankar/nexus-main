"""Player inventory model."""

from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field


class InventoryItem(BaseModel):
    """Single inventory item."""

    item_id: str = Field(..., description='Item identifier')
    name: str = Field(..., description='Item name')
    quantity: int = Field(1, ge=1, description='Item quantity')
    equipped: bool = Field(False, description='Whether item is equipped')
    rarity: str = Field('common', description='Item rarity')
    item_type: str = Field('consumable', description='Type of item')
    acquired_at: datetime = Field(
        default_factory=datetime.utcnow, description='When item was acquired')
    metadata: Optional[Dict[str, Any]] = Field(
        None, description='Additional item data')

    class Config:
        json_schema_extra = {
            'example': {
                'item_id': 'health_potion_01',
                'name': 'Health Potion',
                'quantity': 5,
                'equipped': False,
                'rarity': 'common',
                'item_type': 'consumable',
                'acquired_at': '2025-01-15T10:30:00Z',
                'metadata': {
                    'healing_amount': 50,
                    'cooldown': 60
                }
            }
        }


class PlayerInventory(BaseModel):
    """Player inventory collection."""

    player_id: str = Field(..., description='Player ID')
    items: List[InventoryItem] = Field(
        default_factory=list, description='List of inventory items')
    max_capacity: int = Field(100, description='Maximum inventory capacity')
    total_items: int = Field(0, description='Total number of items')
    last_updated: datetime = Field(
        default_factory=datetime.utcnow, description='Last inventory update')

    class Config:
        json_schema_extra = {
            'example': {
                'player_id': '507f1f77bcf86cd799439011',
                'items': [
                    {
                        'item_id': 'health_potion_01',
                        'name': 'Health Potion',
                        'quantity': 5,
                        'equipped': False
                    }
                ],
                'max_capacity': 100,
                'total_items': 5,
                'last_updated': '2025-01-15T10:30:00Z'
            }
        }


class ItemUsageRequest(BaseModel):
    """Request to use an item."""

    item_id: str = Field(..., description='Item to use')
    target_id: Optional[str] = Field(
        None, description='Target player ID (if applicable)')
    quantity: int = Field(1, ge=1, description='Quantity to use')

    class Config:
        json_schema_extra = {
            'example': {
                'item_id': 'health_potion_01',
                'quantity': 1
            }
        }


class ItemUsageResponse(BaseModel):
    """Response after using an item."""

    success: bool = Field(...,
                          description='Whether item was used successfully')
    item_id: str = Field(..., description='Item that was used')
    quantity_used: int = Field(..., description='Quantity used')
    remaining_quantity: int = Field(..., description='Quantity remaining')
    effect_description: str = Field(...,
                                    description='Description of item effect')
    effects: Dict[str, Any] = Field(
        default_factory=dict, description='Applied effects')

    class Config:
        json_schema_extra = {
            'example': {
                'success': True,
                'item_id': 'health_potion_01',
                'quantity_used': 1,
                'remaining_quantity': 4,
                'effect_description': 'Restored 50 HP',
                'effects': {
                    'hp_restored': 50,
                    'current_hp': 500
                }
            }
        }
