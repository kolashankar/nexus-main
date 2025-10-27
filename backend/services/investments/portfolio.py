from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
from ...models.player.player import Player
from ...models.economy.transaction import Transaction
from .opportunities import InvestmentOpportunities


class InvestmentService:
    """Service for managing investment portfolio."""

    def __init__(self):
        self.opportunities = InvestmentOpportunities()

    async def get_portfolio(self, player_id: str) -> Dict:
        """Get player's investment portfolio."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return {
                "total_invested": 0,
                "current_value": 0,
                "total_profit_loss": 0,
                "roi_percentage": 0.0,
                "investments": []
            }

        investments = player.get("investments", [])

        total_invested = sum(inv.get("amount_invested", 0)
                             for inv in investments)
        current_value = sum(inv.get("current_value", 0) for inv in investments)
        total_profit_loss = current_value - total_invested
        roi_percentage = (total_profit_loss / total_invested * \
                          100) if total_invested > 0 else 0.0

        # Update current values (simulate market changes)
        updated_investments = []
        for inv in investments:
            # Simulate market fluctuation
            days_held = (datetime.utcnow() - \
                         inv.get("investment_date", datetime.utcnow())).days
            expected_return = inv.get("expected_return", 5.0)
            risk_multiplier = {"low": 0.5, "medium": 1.0, "high": 1.5, "very_high": 2.0}.get(
                inv.get("risk_level", "medium"), 1.0
            )

            # Calculate current value with some randomness
            daily_return = (expected_return / 365) / 100
            market_variance = random.uniform(-0.02, 0.02) * risk_multiplier
            total_return = (daily_return + market_variance) * days_held

            current_val = int(inv.get("amount_invested", 0)
                              * (1 + total_return))

            updated_inv = inv.copy()
            updated_inv["current_value"] = current_val
            updated_inv["profit_loss"] = current_val - \
                inv.get("amount_invested", 0)
            updated_inv["profit_loss_percentage"] = (
                (current_val - inv.get("amount_invested", 0)) / \
                 inv.get("amount_invested", 1) * 100
            )
            updated_investments.append(updated_inv)

        return {
            "total_invested": total_invested,
            "current_value": sum(i["current_value"] for i in updated_investments),
            "total_profit_loss": sum(i["profit_loss"] for i in updated_investments),
            "roi_percentage": roi_percentage,
            "investments": updated_investments
        }

    async def get_opportunities(
        self,
        risk_level: Optional[str] = None,
        min_return: Optional[float] = None
    ) -> List[Dict]:
        """Get available investment opportunities."""
        all_opportunities = self.opportunities.get_all_opportunities()

        filtered = []
        for opp in all_opportunities:
            if risk_level and opp.get("risk_level") != risk_level:
                continue
            if min_return and opp.get("expected_return", 0) < min_return:
                continue
            filtered.append(opp)

        return filtered

    async def make_investment(
        self,
        player_id: str,
        investment_id: str,
        amount: int
    ) -> Dict:
        """Make an investment."""
        player = await Player.find_one({"_id": player_id})
        opportunity = self.opportunities.get_opportunity_by_id(investment_id)

        if not player or not opportunity:
            return {"success": False, "error": "Invalid player or investment"}

        # Check minimum investment
        if amount < opportunity.get("min_investment", 0):
            return {"success": False, "error": "Amount below minimum investment"}

        # Check if player can afford
        player_credits = player.get("currencies", {}).get("credits", 0)
        if player_credits < amount:
            return {"success": False, "error": "Insufficient credits"}

        # Create investment
        duration_days = opportunity.get("duration_days", 30)
        maturity_date = datetime.utcnow() + timedelta(days=duration_days)

        investment = {
            "id": investment_id,
            "name": opportunity.get("name"),
            "description": opportunity.get("description"),
            "investment_type": opportunity.get("investment_type"),
            "risk_level": opportunity.get("risk_level"),
            "amount_invested": amount,
            "investment_date": datetime.utcnow(),
            "expected_return": opportunity.get("expected_return"),
            "duration_days": duration_days,
            "maturity_date": maturity_date,
            "current_value": amount,
            "status": "active"
        }

        # Update player
        player_investments = player.get("investments", [])
        player_investments.append(investment)

        await Player.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "currencies.credits": player_credits - amount,
                    "investments": player_investments
                }
            }
        )

        # Log transaction
        await Transaction.insert_one({
            "player_id": player_id,
            "type": "investment",
            "amount": -amount,
            "details": {
                "investment_id": investment_id,
                "investment_name": opportunity.get("name")
            },
            "timestamp": datetime.utcnow()
        })

        return {
            "success": True,
            "investment_id": investment_id,
            "investment_name": opportunity.get("name"),
            "amount_invested": amount,
            "expected_return": opportunity.get("expected_return"),
            "maturity_date": maturity_date,
            "new_balance": player_credits - amount
        }

    async def withdraw_investment(
        self,
        player_id: str,
        investment_id: str
    ) -> Dict:
        """Withdraw from an investment."""
        player = await Player.find_one({"_id": player_id})
        if not player:
            return {"success": False, "error": "Player not found"}

        # Find investment
        player_investments = player.get("investments", [])
        investment_index = next(
            (i for i, inv in enumerate(player_investments)
             if inv.get("id") == investment_id),
            None
        )

        if investment_index is None:
            return {"success": False, "error": "Investment not found"}

        investment = player_investments[investment_index]

        # Calculate withdrawal value (may include penalties for early withdrawal)
        current_value = investment.get(
            "current_value", investment.get("amount_invested", 0))
        maturity_date = investment.get("maturity_date", datetime.utcnow())

        # Early withdrawal penalty
        if datetime.utcnow() < maturity_date:
            penalty_rate = 0.10  # 10% penalty
            current_value = int(current_value * (1 - penalty_rate))

        # Remove investment
        player_investments.pop(investment_index)

        # Add credits
        player_credits = player.get("currencies", {}).get("credits", 0)
        new_balance = player_credits + current_value

        # Update player
        await Player.update_one(
            {"_id": player_id},
            {
                "$set": {
                    "currencies.credits": new_balance,
                    "investments": player_investments
                }
            }
        )

        # Log transaction
        await Transaction.insert_one({
            "player_id": player_id,
            "type": "investment_withdrawal",
            "amount": current_value,
            "details": {
                "investment_id": investment_id,
                "investment_name": investment.get("name"),
                "original_amount": investment.get("amount_invested"),
                "profit_loss": current_value - investment.get("amount_invested", 0)
            },
            "timestamp": datetime.utcnow()
        })

        return {
            "success": True,
            "investment_id": investment_id,
            "withdrawal_amount": current_value,
            "profit_loss": current_value - investment.get("amount_invested", 0),
            "new_balance": new_balance
        }

    async def get_dividend_history(
        self,
        player_id: str,
        limit: int = 50
    ) -> List[Dict]:
        """Get dividend payout history."""
        transactions = await Transaction.find(
            {"player_id": player_id, "type": "dividend_payout"}
        ).sort("timestamp", -1).limit(limit).to_list()

        return [
            {
                "investment_id": t.get("details", {}).get("investment_id"),
                "investment_name": t.get("details", {}).get("investment_name"),
                "amount": t.get("amount", 0),
                "payout_date": t.get("timestamp"),
                "type": t.get("details", {}).get("dividend_type", "quarterly")
            }
            for t in transactions
        ]

    async def calculate_performance(self, player_id: str) -> Dict:
        """Calculate investment performance metrics."""
        portfolio = await self.get_portfolio(player_id)

        # Calculate various performance metrics
        total_invested = portfolio["total_invested"]
        current_value = portfolio["current_value"]
        total_return = current_value - total_invested
        roi = (total_return / total_invested * \
               100) if total_invested > 0 else 0.0

        # Best and worst performing investments
        investments = portfolio["investments"]
        if investments:
            best_investment = max(investments, key=lambda x: x.get(
                "profit_loss_percentage", 0))
            worst_investment = min(
                investments, key=lambda x: x.get("profit_loss_percentage", 0))
        else:
            best_investment = None
            worst_investment = None

        return {
            "total_invested": total_invested,
            "current_value": current_value,
            "total_return": total_return,
            "roi_percentage": roi,
            "active_investments": len(investments),
            "best_performing": {
                "name": best_investment.get("name") if best_investment else None,
                "return_percentage": best_investment.get("profit_loss_percentage", 0) if best_investment else 0
            } if best_investment else None,
            "worst_performing": {
                "name": worst_investment.get("name") if worst_investment else None,
                "return_percentage": worst_investment.get("profit_loss_percentage", 0) if worst_investment else 0
            } if worst_investment else None
        }
