from fastapi import APIRouter, Depends, HTTPException, status
from ....core.security import get_current_user
from ....services.real_estate.manager import RealEstateService
from .schemas import (
    PropertyListResponse,
    PropertyDetailResponse,
    PurchasePropertyRequest,
    PurchasePropertyResponse,
    UpgradePropertyRequest,
    RentPropertyRequest
)

router = APIRouter(prefix="/real-estate", tags=["real-estate"])


@router.get("/properties", response_model=PropertyListResponse)
async def get_available_properties(
    property_type: str = None,
    max_price: int = None,
    territory_id: int = None,
    current_user: dict = Depends(get_current_user)
):
    """Get all available properties for sale."""
    real_estate_service = RealEstateService()
    properties = await real_estate_service.get_available_properties(
        property_type=property_type,
        max_price=max_price,
        territory_id=territory_id
    )
    return {"properties": properties, "total": len(properties)}


@router.get("/my-properties")
async def get_my_properties(
    current_user: dict = Depends(get_current_user)
):
    """Get player's owned properties."""
    real_estate_service = RealEstateService()
    properties = await real_estate_service.get_player_properties(current_user["_id"])
    return {"properties": properties}


@router.get("/properties/{property_id}", response_model=PropertyDetailResponse)
async def get_property_details(
    property_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed information about a property."""
    real_estate_service = RealEstateService()
    property_details = await real_estate_service.get_property_details(property_id)

    if not property_details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    return property_details


@router.post("/purchase", response_model=PurchasePropertyResponse)
async def purchase_property(
    request: PurchasePropertyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Purchase a property."""
    real_estate_service = RealEstateService()

    result = await real_estate_service.purchase_property(
        current_user["_id"],
        request.property_id
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to purchase property")
        )

    return result


@router.post("/sell/{property_id}")
async def sell_property(
    property_id: str,
    price: int,
    current_user: dict = Depends(get_current_user)
):
    """Sell a property."""
    real_estate_service = RealEstateService()

    result = await real_estate_service.sell_property(
        current_user["_id"],
        property_id,
        price
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to sell property")
        )

    return result


@router.post("/upgrade")
async def upgrade_property(
    request: UpgradePropertyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Upgrade a property."""
    real_estate_service = RealEstateService()

    result = await real_estate_service.upgrade_property(
        current_user["_id"],
        request.property_id,
        request.upgrade_type
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to upgrade property")
        )

    return result


@router.post("/rent")
async def rent_property(
    request: RentPropertyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Rent out a property to another player."""
    real_estate_service = RealEstateService()

    result = await real_estate_service.rent_property(
        current_user["_id"],
        request.property_id,
        request.tenant_id,
        request.rent_amount,
        request.duration_days
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Unable to rent property")
        )

    return result


@router.get("/income")
async def get_property_income(
    current_user: dict = Depends(get_current_user)
):
    """Get total income from properties."""
    real_estate_service = RealEstateService()
    income = await real_estate_service.calculate_property_income(current_user["_id"])
    return income
