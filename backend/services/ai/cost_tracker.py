"""AI Cost Tracker for monitoring API usage"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class AICostTracker:
    """Track AI API costs and usage"""

    # Pricing per 1M tokens (as of 2024)
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }

    def __init__(self):
        self.usage_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "calls": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "cache_hits": 0,
                "cache_misses": 0,
            }
        )
        self.start_time = datetime.utcnow()

    def track_call(
        self,
        service: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cached: bool = False
    ) -> None:
        """Track an AI API call"""
        stats = self.usage_stats[service]

        stats["calls"] += 1

        if cached:
            stats["cache_hits"] += 1
        else:
            stats["cache_misses"] += 1
            stats["input_tokens"] += input_tokens
            stats["output_tokens"] += output_tokens
            stats["total_tokens"] += input_tokens + output_tokens

            # Calculate cost
            if model in self.PRICING:
                input_cost = (input_tokens / 1_000_000) * \
                              self.PRICING[model]["input"]
                output_cost = (output_tokens / 1_000_000) * \
                               self.PRICING[model]["output"]
                stats["estimated_cost"] += input_cost + output_cost

    def get_stats(self, service: Optional[str] = None) -> Dict[str, Any]:
        """Get usage statistics"""
        if service:
            stats = dict(self.usage_stats.get(service, {}))
            stats["cache_hit_rate"] = self._calculate_cache_hit_rate(stats)
            return stats

        # Return all stats
        total_stats = {
            "services": {},
            "total": {
                "calls": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "cache_hits": 0,
                "cache_misses": 0,
            },
            "uptime_hours": (datetime.utcnow() - self.start_time).total_seconds() / 3600
        }

        for service, stats in self.usage_stats.items():
            service_stats = dict(stats)
            service_stats["cache_hit_rate"] = self._calculate_cache_hit_rate(
                stats)
            total_stats["services"][service] = service_stats

            # Aggregate totals
            for key in ["calls", "input_tokens", "output_tokens", "total_tokens", "estimated_cost", "cache_hits", "cache_misses"]:
                total_stats["total"][key] += stats[key]

        total_stats["total"]["cache_hit_rate"] = self._calculate_cache_hit_rate(
            total_stats["total"])

        return total_stats

    def _calculate_cache_hit_rate(self, stats: Dict[str, Any]) -> float:
        """Calculate cache hit rate percentage"""
        total_requests = stats["cache_hits"] + stats["cache_misses"]
        if total_requests == 0:
            return 0.0
        return (stats["cache_hits"] / total_requests) * 100

    def reset_stats(self) -> None:
        """Reset all statistics"""
        self.usage_stats.clear()
        self.start_time = datetime.utcnow()
        logger.info("AI cost tracker stats reset")


# Global cost tracker instance
cost_tracker = AICostTracker()
