from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class InvestmentBase(BaseModel):
    id: str
    name: str
    description: str
    investment_type: str  # stocks, bonds, crypto, startup, venture
    risk_level: str  # low, medium, high, very_high


class InvestmentOpportunity(InvestmentBase):
    min_investment: int
    expected_return: float  # percentage
    duration_days: int
    current_investors: int
    total_raised: int
    target_amount: int


class PortfolioInvestment(InvestmentBase):
    amount_invested: int
    investment_date: datetime
    current_value: int
    profit_loss: int
    profit_loss_percentage: float
    status: str  # active, matured, withdrawn


class PortfolioResponse(BaseModel):
    total_invested: int
    current_value: int
    total_profit_loss: int
    roi_percentage: float
    investments: List[PortfolioInvestment]


class InvestmentOpportunityResponse(BaseModel):
    opportunities: List[InvestmentOpportunity]


class MakeInvestmentRequest(BaseModel):
    investment_id: str = Field(..., description="Investment opportunity ID")
    amount: int = Field(..., ge=100, description="Amount to invest")


class MakeInvestmentResponse(BaseModel):
    success: bool
    investment_id: str
    investment_name: str
    amount_invested: int
    expected_return: float
    maturity_date: datetime
    new_balance: int


class DividendPayout(BaseModel):
    investment_id: str
    investment_name: str
    amount: int
    payout_date: datetime
    type: str  # quarterly, annual, special


class DividentPayoutResponse(BaseModel):
    dividends: List[DividendPayout]
    total: int
