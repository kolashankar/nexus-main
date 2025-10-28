"""Gemini AI-based pricing service for world items."""

from typing import Dict, Optional
import os
import google.generativeai as genai
import json

class GeminiPricingService:
    """Uses Gemini AI to calculate dynamic pricing for world items."""
    
    # Base costs for reference
    BASE_COSTS = {
        "skill": {"min": 100, "max": 500},
        "superpower_tool": {"min": 1000, "max": 3000},
        "meta_trait": {"min": 5000, "max": 10000}
    }
    
    def __init__(self):
        # Initialize Gemini
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("EMERGENT_LLM_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.enabled = True
        else:
            self.enabled = False
    
    async def calculate_item_cost(
        self,
        item_type: str,
        item_name: str,
        player_level: int,
        current_trait_value: float = 50.0,
        market_demand: int = 1
    ) -> int:
        """Calculate item cost based on various factors."""
        
        if not self.enabled:
            # Fallback to simple calculation
            return self._calculate_fallback_cost(item_type, player_level)
        
        try:
            prompt = f"""Calculate the cost for a game item with the following parameters:

Item Type: {item_type}
Item Name: {item_name}
Player Level: {player_level}
Current Trait Value: {current_trait_value}/100
Market Demand: {market_demand}

Base cost ranges:
- Skills: 100-500 credits
- Superpower Tools: 1000-3000 credits
- Meta Traits: 5000-10000 credits

Consider:
1. Player level (higher level = higher cost)
2. Current trait value (higher value = higher upgrade cost)
3. Market demand (higher demand = higher cost)
4. Item rarity

Return ONLY a JSON object with this format:
{{
    "cost": <integer>,
    "reasoning": "<brief explanation>"
}}"""
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text.strip())
            
            cost = result.get("cost", self._calculate_fallback_cost(item_type, player_level))
            
            # Ensure cost is within reasonable bounds
            min_cost = self.BASE_COSTS[item_type]["min"]
            max_cost = self.BASE_COSTS[item_type]["max"] * 2  # Allow up to 2x max
            
            return max(min_cost, min(cost, max_cost))
        
        except Exception as e:
            print(f"Gemini pricing error: {e}")
            return self._calculate_fallback_cost(item_type, player_level)
    
    def _calculate_fallback_cost(self, item_type: str, player_level: int) -> int:
        """Simple fallback cost calculation without AI."""
        base_range = self.BASE_COSTS.get(item_type, {"min": 100, "max": 500})
        
        # Linear scaling based on player level
        level_factor = player_level / 100.0
        cost_range = base_range["max"] - base_range["min"]
        
        cost = base_range["min"] + int(cost_range * level_factor)
        
        return cost
    
    async def get_upgrade_cost(
        self,
        item_type: str,
        item_name: str,
        current_level: int,
        player_level: int
    ) -> int:
        """Calculate cost for upgrading an already-owned item."""
        
        # Base cost for the item
        base_cost = await self.calculate_item_cost(
            item_type, item_name, player_level, current_level * 10.0
        )
        
        # Upgrade costs increase exponentially
        upgrade_multiplier = 1.5 ** current_level
        
        return int(base_cost * upgrade_multiplier)
