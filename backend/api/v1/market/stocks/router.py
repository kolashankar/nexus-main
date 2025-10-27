"""Stock market routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List

from backend.api.deps import get_current_user
from backend.services.economy.currency import CurrencyService
from backend.services.market.stocks import StockMarketService
from .schemas import BuyStockRequest, SellStockRequest, StockPriceResponse

router = APIRouter(prefix="/stocks", tags=["market", "stocks"])
stock_service = StockMarketService()
currency_service = CurrencyService()


@router.get("/", response_model=List[StockPriceResponse])
async def get_all_stocks():
    """Get all available stocks and their current prices."""
    try:
        stocks = await stock_service.get_all_stocks()
        return stocks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{ticker}", response_model=StockPriceResponse)
async def get_stock(
    ticker: str
):
    """Get detailed information about a specific stock."""
    try:
        stock = await stock_service.get_stock(ticker)
        if not stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock not found"
            )
        return stock
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/buy")
async def buy_stock(
    request: BuyStockRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Buy stocks."""
    try:
        result = await stock_service.buy_stock(
            player_id=current_user["_id"],
            ticker=request.ticker,
            quantity=request.quantity
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/sell")
async def sell_stock(
    request: SellStockRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Sell stocks."""
    try:
        result = await stock_service.sell_stock(
            player_id=current_user["_id"],
            ticker=request.ticker,
            quantity=request.quantity
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/portfolio/mine")
async def get_my_portfolio(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get player's stock portfolio."""
    try:
        portfolio = await stock_service.get_portfolio(current_user["_id"])
        return portfolio
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/history/{ticker}")
async def get_stock_history(
    ticker: str,
    days: int = 30
):
    """Get historical stock prices."""
    try:
        history = await stock_service.get_stock_history(ticker, days)
        return {"ticker": ticker, "history": history}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
