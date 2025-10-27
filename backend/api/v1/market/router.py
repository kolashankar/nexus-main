"""Main market routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from backend.api.deps import get_current_user
from backend.core.database import get_database

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/")
async def get_market_overview():
    """Get market overview."""
    return {
        "status": "operational",
        "markets": [
            {"name": "Stock Market", "endpoint": "/api/market/stocks"},
            {"name": "Robot Marketplace", "endpoint": "/api/robots/marketplace"},
            {"name": "Item Market", "endpoint": "/api/market/items"},
            {"name": "Real Estate", "endpoint": "/api/market/real-estate"}
        ]
    }


@router.get("/currencies")
async def get_currencies(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get all currency types and player's balances."""
    from bson import ObjectId
    db = await get_database()

    player = await db.players.find_one({"_id": ObjectId(current_user["_id"])})

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )

    currencies = player.get("currencies", {})

    return {
        "currencies": {
            "credits": {
                "balance": currencies.get("credits", 0),
                "name": "Credits",
                "description": "Basic currency - earned from actions and quests",
                "icon": "💰"
            },
            "karma_tokens": {
                "balance": currencies.get("karma_tokens", 0),
                "name": "Karma Tokens",
                "description": "Earned from positive karma - special purchases",
                "icon": "✨"
            },
            "dark_matter": {
                "balance": currencies.get("dark_matter", 0),
                "name": "Dark Matter",
                "description": "Earned from negative karma - black market",
                "icon": "🌑"
            },
            "prestige_points": {
                "balance": currencies.get("prestige_points", 0),
                "name": "Prestige Points",
                "description": "From prestiging - permanent upgrades",
                "icon": "⭐"
            },
            "guild_coins": {
                "balance": currencies.get("guild_coins", 0),
                "name": "Guild Coins",
                "description": "Guild contributions - guild items",
                "icon": "🏰"
            },
            "legacy_shards": {
                "balance": currencies.get("legacy_shards", 0),
                "name": "Legacy Shards",
                "description": "Cross-season currency - account-wide",
                "icon": "💎"
            }
        },
        "total_wealth_score": _calculate_wealth_score(currencies)
    }


def _calculate_wealth_score(currencies: Dict[str, int]) -> int:
    """Calculate overall wealth score."""
    weights = {
        "credits": 1,
        "karma_tokens": 10,
        "dark_matter": 10,
        "prestige_points": 50,
        "guild_coins": 5,
        "legacy_shards": 100
    }

    score = 0
    for currency, balance in currencies.items():
        weight = weights.get(currency, 1)
        score += balance * weight

    return score
