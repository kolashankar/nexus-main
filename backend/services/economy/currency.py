"""Currency management service."""

from typing import Dict, Any
from bson import ObjectId
from datetime import datetime

from backend.core.database import get_database


class CurrencyService:
    """Manage player currencies and conversions."""

    CURRENCY_TYPES = [
        "credits",
        "karma_tokens",
        "dark_matter",
        "prestige_points",
        "guild_coins",
        "legacy_shards"
    ]

    async def get_balance(
        self,
        player_id: str,
        currency_type: str = "credits"
    ) -> int:
        """Get player's currency balance."""
        if currency_type not in self.CURRENCY_TYPES:
            raise ValueError(f"Invalid currency type: {currency_type}")

        db = await get_database()
        player = await db.players.find_one({"_id": ObjectId(player_id)})

        if not player:
            raise ValueError("Player not found")

        return player.get("currencies", {}).get(currency_type, 0)

    async def add_currency(
        self,
        player_id: str,
        currency_type: str,
        amount: int,
        reason: str = "generic"
    ) -> Dict[str, Any]:
        """Add currency to player's balance."""
        if currency_type not in self.CURRENCY_TYPES:
            raise ValueError(f"Invalid currency type: {currency_type}")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        db = await get_database()

        # Update balance
        result = await db.players.update_one(
            {"_id": ObjectId(player_id)},
            {
                "$inc": {f"currencies.{currency_type}": amount}
            }
        )

        if result.modified_count == 0:
            raise ValueError("Failed to update balance")

        # Log transaction
        await self._log_transaction(
            player_id=player_id,
            currency_type=currency_type,
            amount=amount,
            transaction_type="earn",
            reason=reason
        )

        new_balance = await self.get_balance(player_id, currency_type)

        return {
            "success": True,
            "currency_type": currency_type,
            "amount_added": amount,
            "new_balance": new_balance
        }

    async def deduct_currency(
        self,
        player_id: str,
        currency_type: str,
        amount: int,
        reason: str = "purchase"
    ) -> Dict[str, Any]:
        """Deduct currency from player's balance."""
        if currency_type not in self.CURRENCY_TYPES:
            raise ValueError(f"Invalid currency type: {currency_type}")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Check balance
        current_balance = await self.get_balance(player_id, currency_type)

        if current_balance < amount:
            raise ValueError(f"Insufficient {currency_type}")

        db = await get_database()

        # Deduct balance
        result = await db.players.update_one(
            {"_id": ObjectId(player_id)},
            {
                "$inc": {f"currencies.{currency_type}": -amount}
            }
        )

        if result.modified_count == 0:
            raise ValueError("Failed to update balance")

        # Log transaction
        await self._log_transaction(
            player_id=player_id,
            currency_type=currency_type,
            amount=-amount,
            transaction_type="spend",
            reason=reason
        )

        new_balance = await self.get_balance(player_id, currency_type)

        return {
            "success": True,
            "currency_type": currency_type,
            "amount_deducted": amount,
            "new_balance": new_balance
        }

    async def transfer_currency(
        self,
        from_player_id: str,
        to_player_id: str,
        currency_type: str,
        amount: int
    ) -> Dict[str, Any]:
        """Transfer currency between players."""
        if currency_type not in self.CURRENCY_TYPES:
            raise ValueError(f"Invalid currency type: {currency_type}")

        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Deduct from sender
        await self.deduct_currency(
            from_player_id,
            currency_type,
            amount,
            reason=f"transfer_to_{to_player_id}"
        )

        # Add to receiver
        await self.add_currency(
            to_player_id,
            currency_type,
            amount,
            reason=f"transfer_from_{from_player_id}"
        )

        return {
            "success": True,
            "from_player": from_player_id,
            "to_player": to_player_id,
            "currency_type": currency_type,
            "amount": amount
        }

    async def convert_currency(
        self,
        player_id: str,
        from_currency: str,
        to_currency: str,
        amount: int
    ) -> Dict[str, Any]:
        """Convert one currency to another."""
        # Define conversion rates
        conversion_rates = {
            ("credits", "karma_tokens"): 0.1,  # 10 credits = 1 karma token
            ("credits", "dark_matter"): 0.1,
            ("karma_tokens", "credits"): 10,
            ("dark_matter", "credits"): 10,
        }

        rate = conversion_rates.get((from_currency, to_currency))

        if rate is None:
            raise ValueError(
                f"Cannot convert {from_currency} to {to_currency}")

        # Deduct source currency
        await self.deduct_currency(
            player_id,
            from_currency,
            amount,
            reason=f"convert_to_{to_currency}"
        )

        # Add target currency
        converted_amount = int(amount * rate)
        await self.add_currency(
            player_id,
            to_currency,
            converted_amount,
            reason=f"convert_from_{from_currency}"
        )

        return {
            "success": True,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount_converted": amount,
            "amount_received": converted_amount,
            "rate": rate
        }

    async def _log_transaction(
        self,
        player_id: str,
        currency_type: str,
        amount: int,
        transaction_type: str,
        reason: str
    ):
        """Log a currency transaction."""
        db = await get_database()

        transaction = {
            "player_id": player_id,
            "currency_type": currency_type,
            "amount": amount,
            "transaction_type": transaction_type,
            "reason": reason,
            "timestamp": datetime.utcnow()
        }

        await db.currency_transactions.insert_one(transaction)

    async def get_transaction_history(
        self,
        player_id: str,
        limit: int = 50,
        skip: int = 0
    ) -> list:
        """Get player's transaction history."""
        db = await get_database()

        transactions = await db.currency_transactions.find(
            {"player_id": player_id}
        ).sort("timestamp", -1).skip(skip).limit(limit).to_list(length=limit)

        return transactions
