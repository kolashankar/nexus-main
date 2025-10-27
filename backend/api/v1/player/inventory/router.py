"""Player inventory routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import get_database
from backend.api.deps import get_current_user
from backend.services.player.inventory_manager import InventoryManager
from backend.models.player.inventory import (
    InventoryItem,
    PlayerInventory,
    ItemUsageRequest,
    ItemUsageResponse
)
from backend.api.v1.player.inventory.schemas import (
    AddItemRequest,
    RemoveItemRequest
)

router = APIRouter()


@router.get('/me', response_model=List[InventoryItem])
async def get_my_inventory(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get current player's inventory."""
    inventory_manager = InventoryManager(db)

    items = await inventory_manager.get_inventory(current_user['_id'])

    return items


@router.get('/me/equipped', response_model=List[InventoryItem])
async def get_equipped_items(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get currently equipped items."""
    inventory_manager = InventoryManager(db)

    equipped = await inventory_manager.get_equipped_items(current_user['_id'])

    return equipped


@router.post('/me/items')
async def add_item_to_inventory(
    request: AddItemRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Add an item to inventory (admin or reward)."""
    inventory_manager = InventoryManager(db)

    item = await inventory_manager.add_item(
        current_user['_id'],
        request.item_id,
        request.quantity,
        request.metadata
    )

    return {
        'success': True,
        'message': f'Added {request.quantity}x {request.item_id}',
        'item': item
    }


@router.delete('/me/items/{item_id}')
async def remove_item_from_inventory(
    item_id: str,
    request: RemoveItemRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Remove an item from inventory."""
    inventory_manager = InventoryManager(db)

    removed = await inventory_manager.remove_item(
        current_user['_id'],
        item_id,
        request.quantity
    )

    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item {item_id} not found in inventory'
        )

    return {
        'success': True,
        'message': f'Removed {request.quantity}x {item_id}'
    }


@router.post('/me/items/{item_id}/equip')
async def equip_item(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Equip an item."""
    inventory_manager = InventoryManager(db)

    equipped = await inventory_manager.equip_item(
        current_user['_id'],
        item_id
    )

    if not equipped:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item {item_id} not found'
        )

    return {
        'success': True,
        'message': f'Equipped {item_id}'
    }


@router.post('/me/items/{item_id}/unequip')
async def unequip_item(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Unequip an item."""
    inventory_manager = InventoryManager(db)

    unequipped = await inventory_manager.unequip_item(
        current_user['_id'],
        item_id
    )

    if not unequipped:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item {item_id} not found or not equipped'
        )

    return {
        'success': True,
        'message': f'Unequipped {item_id}'
    }


@router.post('/me/items/use', response_model=ItemUsageResponse)
async def use_item(
    request: ItemUsageRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Use a consumable item."""
    inventory_manager = InventoryManager(db)

    # Check if player has the item
    has_item = await inventory_manager.has_item(
        current_user['_id'],
        request.item_id,
        request.quantity
    )

    if not has_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Insufficient quantity of item'
        )

    # TODO: Implement item effects based on item type
    # For now, just remove the item
    removed = await inventory_manager.remove_item(
        current_user['_id'],
        request.item_id,
        request.quantity
    )

    remaining = await inventory_manager.get_item_count(
        current_user['_id'],
        request.item_id
    )

    return ItemUsageResponse(
        success=True,
        item_id=request.item_id,
        quantity_used=request.quantity,
        remaining_quantity=remaining,
        effect_description=f'Used {request.quantity}x {request.item_id}',
        effects={}
    )


@router.get('/me/items/{item_id}/count')
async def get_item_count(
    item_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """Get count of a specific item."""
    inventory_manager = InventoryManager(db)

    count = await inventory_manager.get_item_count(
        current_user['_id'],
        item_id
    )

    return {
        'item_id': item_id,
        'quantity': count
    }
