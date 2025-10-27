from typing import Dict, List
from datetime import datetime


def calculate_compound_interest(
    principal: float,
    rate: float,
    time: int,
    compounds_per_year: int = 365
) -> float:
    """Calculate compound interest."""
    return principal * (1 + rate / compounds_per_year) ** (compounds_per_year * time)


def calculate_roi(initial_investment: float, current_value: float) -> float:
    """Calculate return on investment percentage."""
    if initial_investment == 0:
        return 0.0
    return ((current_value - initial_investment) / initial_investment) * 100


def calculate_daily_income(properties: List[Dict]) -> int:
    """Calculate total daily income from properties."""
    return sum(prop.get("passive_income", 0) for prop in properties)


def calculate_property_value_appreciation(
    purchase_price: int,
    days_owned: int,
    appreciation_rate: float = 0.05
) -> int:
    """Calculate appreciated property value."""
    years_owned = days_owned / 365
    appreciated_value = purchase_price * \
        ((1 + appreciation_rate) ** years_owned)
    return int(appreciated_value)


def calculate_investment_returns(
    investments: List[Dict],
    current_date: datetime
) -> Dict:
    """Calculate total returns from all investments."""
    total_invested = 0
    total_current_value = 0

    for inv in investments:
        total_invested += inv.get("amount_invested", 0)

        # Calculate current value based on expected return and time
        investment_date = inv.get("investment_date", current_date)
        days_invested = (current_date - investment_date).days
        expected_annual_return = inv.get("expected_return", 0) / 100

        current_value = inv.get("amount_invested", 0) * (
            1 + (expected_annual_return * days_invested / 365)
        )
        total_current_value += current_value

    return {
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "total_profit_loss": total_current_value - total_invested,
        "roi_percentage": calculate_roi(total_invested, total_current_value)
    }


def calculate_crafting_success_rate(
    base_rate: float,
    player_skill: int,
    recipe_difficulty: int
) -> float:
    """Calculate success rate for crafting."""
    skill_bonus = (player_skill / 100) * 0.1  # Max 10% bonus
    difficulty_penalty = (recipe_difficulty / 100) * 0.05  # Max 5% penalty

    final_rate = base_rate + skill_bonus - difficulty_penalty
    return max(0.0, min(1.0, final_rate))  # Clamp between 0 and 1


def format_currency(amount: int) -> str:
    """Format currency for display."""
    return f"{amount:,}"


def calculate_market_price_fluctuation(
    base_price: int,
    demand: float,
    supply: float,
    volatility: float = 0.1
) -> int:
    """Calculate market price with demand/supply dynamics."""
    import random

    # Demand/supply ratio affects price
    demand_supply_factor = demand / max(supply, 1)

    # Add random volatility
    volatility_factor = random.uniform(-volatility, volatility)

    # Calculate final price
    price_multiplier = 1 + ((demand_supply_factor - 1)
                            * 0.5) + volatility_factor
    final_price = int(base_price * price_multiplier)

    return max(1, final_price)  # Minimum price of 1
