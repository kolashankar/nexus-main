"""Player inventory schemas."""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class AddItemRequest(BaseModel):
    """Request to add an item to inventory."""

    item_id: str = Field(..., description='Item identifier')
    quantity: int = Field(1, ge=1, description='Quantity to add')
    metadata: Optional[Dict[str, Any]] = Field(
        None, description='Optional item metadata')

    class Config:
        json_schema_extra = {
            'example': {
                'item_id': 'health_potion_01',
                'quantity': 5,
                'metadata': {
                    'source': 'quest_reward',
                    'quest_id': 'quest_123'
                }
            }
        }


class RemoveItemRequest(BaseModel):
    """Request to remove an item from inventory."""

    quantity: int = Field(1, ge=1, description='Quantity to remove')

    class Config:
        json_schema_extra = {
            'example': {
                'quantity': 1
            }
        }


class EquipItemRequest(BaseModel):
    """Request to equip an item."""

    item_id: str = Field(..., description='Item to equip')
    slot: Optional[str] = Field(None, description='Equipment slot')

    class Config:
        json_schema_extra = {
            'example': {
                'item_id': 'legendary_sword',
                'slot': 'weapon'
            }
        }
