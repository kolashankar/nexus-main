from fastapi import APIRouter, Depends, HTTPException, status
from ....core.security import get_current_user
from ....services.investments.portfolio import InvestmentService
from .schemas import (
    PortfolioResponse,
    InvestmentOpportunityResponse,
    MakeInvestmentRequest,
    MakeInvestmentResponse,
    DividentPayoutResponse
)

router = APIRouter(prefix="/investments", tags=["investments"])


@router.get("/portfolio", response_model=PortfolioResponse)
async def get_portfolio(
    current_user: dict = Depends(get_current_user)
):
    """Get player's investment portfolio."""
    investment_service = InvestmentService()
    portfolio = await investment_service.get_portfolio(current_user["_id"])
    return portfolio


@router.get("/opportunities", response_model=InvestmentOpportunityResponse)
async def get_investment_opportunities(
    risk_level: str = None,
    min_return: float = None,
    current_user: dict = Depends(get_current_user)
):
    """Get available investment opportunities."""
    investment_service = InvestmentService()
    opportunities = await investment_service.get_opportunities(
        risk_level=risk_level,
        min_return=min_return
    )
    return {"opportunities": opportunities}


@router.post("/invest", response_model=MakeInvestmentResponse)
async def make_investment(
    request: MakeInvestmentRequest,
    current_user: dict = Depends(get_current_user)
):
    """Make an investment."""
    investment_service = InvestmentService()

    result = await investment_service.make_investment(
        current_user["_id"],
        request.investment_id,
        request.amount
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to make investment")
        )

    return result


@router.post("/withdraw/{investment_id}")
async def withdraw_investment(
    investment_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Withdraw from an investment."""
    investment_service = InvestmentService()

    result = await investment_service.withdraw_investment(
        current_user["_id"],
        investment_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to withdraw investment")
        )

    return result


@router.get("/dividends", response_model=DividentPayoutResponse)
async def get_dividend_history(
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Get dividend payout history."""
    investment_service = InvestmentService()
    dividends = await investment_service.get_dividend_history(
        current_user["_id"],
        limit=limit
    )
    return {"dividends": dividends, "total": len(dividends)}


@router.get("/performance")
async def get_investment_performance(
    current_user: dict = Depends(get_current_user)
):
    """Get investment performance metrics."""
    investment_service = InvestmentService()
    performance = await investment_service.calculate_performance(current_user["_id"])
    return performance
