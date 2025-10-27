"""Transaction processing service."""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from backend.core.database import get_database
from .currency import CurrencyService


class TransactionService:
    """Handle complex transactions and payments."""

    def __init__(self):
        self.currency_service = CurrencyService()

    async def create_transaction(
        self,
        transaction_type: str,
        from_player: Optional[str] = None,
        to_player: Optional[str] = None,
        currency_type: str = "credits",
        amount: int = 0,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Create a transaction record."""
        db = await get_database()

        transaction_id = str(uuid.uuid4())

        transaction = {
            "transaction_id": transaction_id,
            "type": transaction_type,
            "from_player": from_player,
            "to_player": to_player,
            "currency_type": currency_type,
            "amount": amount,
            "status": "pending",
            "metadata": metadata or {},
            "created_at": datetime.utcnow(),
            "completed_at": None
        }

        await db.transactions.insert_one(transaction)

        return transaction_id

    async def execute_transaction(
        self,
        transaction_id: str
    ) -> Dict[str, Any]:
        """Execute a pending transaction."""
        db = await get_database()

        transaction = await db.transactions.find_one({"transaction_id": transaction_id})

        if not transaction:
            raise ValueError("Transaction not found")

        if transaction["status"] != "pending":
            raise ValueError(f"Transaction already {transaction['status']}")

        try:
            # Execute based on type
            if transaction["type"] == "transfer":
                await self.currency_service.transfer_currency(
                    from_player_id=transaction["from_player"],
                    to_player_id=transaction["to_player"],
                    currency_type=transaction["currency_type"],
                    amount=transaction["amount"]
                )
            elif transaction["type"] == "purchase":
                await self.currency_service.deduct_currency(
                    player_id=transaction["from_player"],
                    currency_type=transaction["currency_type"],
                    amount=transaction["amount"],
                    reason="purchase"
                )
            elif transaction["type"] == "reward":
                await self.currency_service.add_currency(
                    player_id=transaction["to_player"],
                    currency_type=transaction["currency_type"],
                    amount=transaction["amount"],
                    reason="reward"
                )

            # Mark as completed
            await db.transactions.update_one(
                {"transaction_id": transaction_id},
                {
                    "$set": {
                        "status": "completed",
                        "completed_at": datetime.utcnow()
                    }
                }
            )

            return {"success": True, "transaction_id": transaction_id}

        except Exception as e:
            # Mark as failed
            await db.transactions.update_one(
                {"transaction_id": transaction_id},
                {
                    "$set": {
                        "status": "failed",
                        "error": str(e),
                        "completed_at": datetime.utcnow()
                    }
                }
            )

            raise

    async def cancel_transaction(
        self,
        transaction_id: str
    ) -> Dict[str, Any]:
        """Cancel a pending transaction."""
        db = await get_database()

        result = await db.transactions.update_one(
            {"transaction_id": transaction_id, "status": "pending"},
            {
                "$set": {
                    "status": "cancelled",
                    "completed_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count == 0:
            raise ValueError("Cannot cancel transaction")

        return {"success": True, "transaction_id": transaction_id}

    async def get_transaction_status(
        self,
        transaction_id: str
    ) -> Dict[str, Any]:
        """Get transaction status."""
        db = await get_database()

        transaction = await db.transactions.find_one({"transaction_id": transaction_id})

        if not transaction:
            raise ValueError("Transaction not found")

        return transaction
