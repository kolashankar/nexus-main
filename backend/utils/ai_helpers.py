"""AI Helper Utilities"""

import hashlib
import json
from typing import Dict, Any


def generate_cache_key(service: str, params: Dict[str, Any]) -> str:
    """Generate a cache key from service and parameters"""
    params_str = json.dumps(params, sort_keys=True)
    hash_obj = hashlib.md5(params_str.encode())
    return f"ai:{service}:{hash_obj.hexdigest()}"


def normalize_karma_value(karma: float, bucket_size: int = 100) -> int:
    """Normalize karma value into buckets for caching"""
    return int(karma / bucket_size) * bucket_size


def extract_top_traits(traits: Dict[str, float], count: int = 5) -> Dict[str, float]:
    """Extract top N traits from player traits"""
    sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_traits[:count])


def format_trait_summary(traits: Dict[str, float]) -> str:
    """Format traits into a readable summary"""
    top_traits = extract_top_traits(traits)
    return ", ".join([f"{trait}: {value:.0f}%" for trait, value in top_traits.items()])


def calculate_ai_cost(input_tokens: int, output_tokens: int, model: str = "gpt-4o") -> float:
    """Calculate estimated AI API cost"""
    pricing = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60}
    }

    if model not in pricing:
        return 0.0

    input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
    output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]

    return input_cost + output_cost
