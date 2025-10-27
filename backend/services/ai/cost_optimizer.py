"""AI Cost Optimization Utilities"""

import logging
from typing import Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CostOptimizer:
    """Optimizes AI API costs through smart strategies"""

    def __init__(self):
        self.daily_budget = 100.0  # $100 daily budget
        self.current_spend = 0.0
        self.last_reset = datetime.utcnow()
        self.alert_threshold = 0.8  # Alert at 80% of budget

    def can_make_call(self, estimated_cost: float) -> bool:
        """Check if we can make an AI call within budget"""

        # Reset daily budget if needed
        if (datetime.utcnow() - self.last_reset) > timedelta(days=1):
            self.current_spend = 0.0
            self.last_reset = datetime.utcnow()
            logger.info("Daily AI budget reset")

        # Check if call would exceed budget
        if (self.current_spend + estimated_cost) > self.daily_budget:
            logger.warning(
                f"AI call would exceed daily budget. "
                f"Current: ${self.current_spend:.2f}, "
                f"Estimated: ${estimated_cost:.2f}, "
                f"Budget: ${self.daily_budget:.2f}"
            )
            return False

        # Alert if approaching threshold
        if (self.current_spend + estimated_cost) > (self.daily_budget * self.alert_threshold):
            logger.warning(
                f"Approaching daily AI budget threshold. "
                f"Current: ${self.current_spend:.2f}, "
                f"Budget: ${self.daily_budget:.2f}"
            )

        return True

    def record_spend(self, cost: float) -> None:
        """Record AI API spending"""
        self.current_spend += cost
        logger.info(
            f"AI spend recorded: ${cost:.4f}. "
            f"Total today: ${self.current_spend:.2f}/${self.daily_budget:.2f}"
        )

    def get_spending_summary(self) -> Dict[str, Any]:
        """Get current spending summary"""
        return {
            "current_spend": round(self.current_spend, 2),
            "daily_budget": self.daily_budget,
            "remaining": round(self.daily_budget - self.current_spend, 2),
            "percentage_used": round((self.current_spend / self.daily_budget) * 100, 1),
            "last_reset": self.last_reset.isoformat()
        }

    def set_daily_budget(self, budget: float) -> None:
        """Set daily AI budget"""
        self.daily_budget = budget
        logger.info(f"Daily AI budget set to ${budget:.2f}")

    def suggest_model(self, complexity: str = "medium") -> str:
        """Suggest appropriate model based on budget and complexity"""

        # If over 90% of budget used, suggest mini for all
        if self.current_spend > (self.daily_budget * 0.9):
            return "gpt-4o-mini"

        # Otherwise, use complexity-based selection
        if complexity == "high":
            return "gpt-4o"
        elif complexity == "medium":
            return "gpt-4o" if self.current_spend < (self.daily_budget * 0.5) else "gpt-4o-mini"
        else:  # low complexity
            return "gpt-4o-mini"


# Global cost optimizer instance
cost_optimizer = CostOptimizer()


def estimate_call_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "gpt-4o"
) -> float:
    """Estimate cost of an AI call"""

    pricing = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60}
    }

    if model not in pricing:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
    output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]

    return input_cost + output_cost


def optimize_prompt(prompt: str, max_length: int = 2000) -> str:
    """Optimize prompt length to reduce costs"""

    if len(prompt) <= max_length:
        return prompt

    # Truncate with ellipsis
    return prompt[:max_length-3] + "..."
