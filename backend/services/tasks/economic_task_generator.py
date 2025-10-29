"""Economic task generator service."""

import random
from typing import Dict, Any, List

class EconomicTaskGenerator:
    """Generates economic choice tasks."""
    
    ECONOMIC_SCENARIOS = [
        {
            "title": "Investment Opportunity",
            "description": "A trader offers you a chance to invest in a new mining operation. They promise high returns, but the wasteland is unpredictable.",
            "risk_level": "medium",
            "investment_amount": 500
        },
        {
            "title": "Black Market Deal",
            "description": "Someone in the shadows offers to sell you rare tech at half price. It could be stolen or defective.",
            "risk_level": "high",
            "investment_amount": 1000
        },
        {
            "title": "Guild Treasury",
            "description": "Your guild is pooling resources for a major expansion. Contributing could strengthen your position.",
            "risk_level": "low",
            "investment_amount": 300
        },
        {
            "title": "Casino Challenge",
            "description": "A high-stakes game is about to begin at the local casino. The pot is massive, but so are the risks.",
            "risk_level": "high",
            "investment_amount": 800
        },
        {
            "title": "Refugee Support",
            "description": "Refugees from a destroyed sector need supplies. You could help them, but it won't be profitable.",
            "risk_level": "none",
            "investment_amount": 200
        }
    ]
    
    def generate_economic_task(self, player_level: int, player_credits: int, player_traits: Dict[str, float]) -> Dict[str, Any]:
        """Generate an economic task."""
        # Filter scenarios player can afford
        affordable_scenarios = [
            s for s in self.ECONOMIC_SCENARIOS 
            if s["investment_amount"] <= player_credits * 0.8  # Leave some buffer
        ]
        
        if not affordable_scenarios:
            affordable_scenarios = [self.ECONOMIC_SCENARIOS[-1]]  # Cheapest option
        
        scenario = random.choice(affordable_scenarios)
        
        choices = self._generate_economic_choices(
            scenario,
            player_traits.get("greed", 50),
            player_traits.get("compassion", 50),
            player_traits.get("wisdom", 50)
        )
        
        return {
            "task_id": f"economic_{random.randint(10000, 99999)}",
            "title": scenario["title"],
            "description": scenario["description"],
            "type": "economic",
            "difficulty": self._map_risk_to_difficulty(scenario["risk_level"]),
            "xp_reward": 80,
            "credits_reward": 0,  # Economic tasks have variable rewards
            "choices": choices
        }
    
    def _generate_economic_choices(
        self,
        scenario: Dict[str, Any],
        greed: float,
        compassion: float,
        wisdom: float
    ) -> List[Dict[str, Any]]:
        """Generate economic choices."""
        investment = scenario["investment_amount"]
        risk = scenario["risk_level"]
        
        choices = []
        
        # INVEST option
        potential_return = investment * self._get_return_multiplier(risk)
        choices.append({
            "text": f"Invest {investment} credits (Potential return: {int(potential_return)} credits)",
            "traits_impact": {
                "greed": 8,
                "courage": 5,
                "wisdom": 3,
                "karma_points": -5 if risk == "high" else 0
            }
        })
        
        # SAVE option
        choices.append({
            "text": "Save your credits for a better opportunity",
            "traits_impact": {
                "wisdom": 10,
                "patience": 8,
                "greed": -5,
                "karma_points": 5
            }
        })
        
        # GAMBLE option (high risk scenarios)
        if risk == "high":
            choices.append({
                "text": f"Go all in! Double your investment to {investment * 2} credits",
                "traits_impact": {
                    "greed": 15,
                    "recklessness": 12,
                    "courage": 8,
                    "karma_points": -10
                }
            })
        
        # DONATE option (compassion scenarios)
        if "refugee" in scenario["title"].lower() or compassion >= 60:
            choices.append({
                "text": f"Donate {investment} credits to help those in need",
                "traits_impact": {
                    "compassion": 15,
                    "generosity": 12,
                    "greed": -10,
                    "karma_points": 25
                }
            })
        
        return choices
    
    def _get_return_multiplier(self, risk: str) -> float:
        """Get return multiplier based on risk."""
        multipliers = {
            "none": 1.0,
            "low": 1.5,
            "medium": 2.5,
            "high": 4.0
        }
        return multipliers.get(risk, 1.5)
    
    def _map_risk_to_difficulty(self, risk: str) -> str:
        """Map risk level to task difficulty."""
        risk_map = {
            "none": "easy",
            "low": "easy",
            "medium": "medium",
            "high": "hard"
        }
        return risk_map.get(risk, "medium")
