from typing import List, Dict, Optional


class InvestmentOpportunities:
    """Manages investment opportunities."""

    def __init__(self):
        self.opportunities = self._initialize_opportunities()

    def _initialize_opportunities(self) -> Dict[str, Dict]:
        """Initialize investment opportunities."""
        return {
            "tech_startup_1": {
                "id": "tech_startup_1",
                "name": "NanoTech Innovations",
                "description": "Cutting-edge nanotechnology startup",
                "investment_type": "startup",
                "risk_level": "high",
                "min_investment": 10000,
                "expected_return": 25.0,
                "duration_days": 365,
                "current_investors": 45,
                "total_raised": 500000,
                "target_amount": 1000000
            },
            "corporate_bonds_1": {
                "id": "corporate_bonds_1",
                "name": "RoboCorp Bonds",
                "description": "Stable corporate bonds with fixed returns",
                "investment_type": "bonds",
                "risk_level": "low",
                "min_investment": 1000,
                "expected_return": 5.0,
                "duration_days": 180,
                "current_investors": 120,
                "total_raised": 2000000,
                "target_amount": 5000000
            },
            "crypto_fund": {
                "id": "crypto_fund",
                "name": "Digital Currency Fund",
                "description": "Diversified cryptocurrency investment fund",
                "investment_type": "crypto",
                "risk_level": "very_high",
                "min_investment": 5000,
                "expected_return": 40.0,
                "duration_days": 90,
                "current_investors": 80,
                "total_raised": 800000,
                "target_amount": 2000000
            },
            "real_estate_fund": {
                "id": "real_estate_fund",
                "name": "Urban Development Fund",
                "description": "Real estate investment trust",
                "investment_type": "real_estate",
                "risk_level": "medium",
                "min_investment": 25000,
                "expected_return": 12.0,
                "duration_days": 730,
                "current_investors": 60,
                "total_raised": 3000000,
                "target_amount": 10000000
            },
            "ai_venture": {
                "id": "ai_venture",
                "name": "AI Solutions Venture",
                "description": "Artificial intelligence venture capital fund",
                "investment_type": "venture",
                "risk_level": "high",
                "min_investment": 50000,
                "expected_return": 30.0,
                "duration_days": 1095,
                "current_investors": 25,
                "total_raised": 5000000,
                "target_amount": 20000000
            },
            "green_energy": {
                "id": "green_energy",
                "name": "Renewable Energy Co-op",
                "description": "Sustainable energy investment",
                "investment_type": "stocks",
                "risk_level": "medium",
                "min_investment": 5000,
                "expected_return": 15.0,
                "duration_days": 365,
                "current_investors": 150,
                "total_raised": 1500000,
                "target_amount": 3000000
            },
            "biotech_ipo": {
                "id": "biotech_ipo",
                "name": "BioGenetics IPO",
                "description": "Pre-IPO investment in biotech company",
                "investment_type": "stocks",
                "risk_level": "high",
                "min_investment": 20000,
                "expected_return": 35.0,
                "duration_days": 540,
                "current_investors": 30,
                "total_raised": 1000000,
                "target_amount": 5000000
            },
            "stable_income": {
                "id": "stable_income",
                "name": "Dividend Growth Portfolio",
                "description": "Low-risk dividend-paying stocks",
                "investment_type": "stocks",
                "risk_level": "low",
                "min_investment": 2000,
                "expected_return": 7.0,
                "duration_days": 365,
                "current_investors": 200,
                "total_raised": 4000000,
                "target_amount": 10000000
            }
        }

    def get_all_opportunities(self) -> List[Dict]:
        """Get all investment opportunities."""
        return list(self.opportunities.values())

    def get_opportunity_by_id(self, opportunity_id: str) -> Optional[Dict]:
        """Get a specific opportunity by ID."""
        return self.opportunities.get(opportunity_id)

    def get_opportunities_by_type(self, investment_type: str) -> List[Dict]:
        """Get opportunities by type."""
        return [
            opp for opp in self.opportunities.values()
            if opp.get("investment_type") == investment_type
        ]

    def get_opportunities_by_risk(self, risk_level: str) -> List[Dict]:
        """Get opportunities by risk level."""
        return [
            opp for opp in self.opportunities.values()
            if opp.get("risk_level") == risk_level
        ]
