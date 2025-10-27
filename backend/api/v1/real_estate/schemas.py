from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class PropertyBase(BaseModel):
    id: str
    name: str
    description: str
    property_type: str  # apartment, house, mansion, commercial, industrial
    size: int  # square meters
    location: Dict[str, Any]
    territory_id: int


class PropertyListItem(PropertyBase):
    price: int
    passive_income: int  # credits per day
    status: str  # available, owned, rented


class PropertyDetailResponse(PropertyBase):
    price: int
    passive_income: int
    maintenance_cost: int
    upgrades: List[Dict[str, Any]]
    owner_id: Optional[str]
    tenant_id: Optional[str]
    status: str
    purchase_date: Optional[datetime]


class PropertyListResponse(BaseModel):
    properties: List[PropertyListItem]
    total: int


class PurchasePropertyRequest(BaseModel):
    property_id: str = Field(..., description="Property ID to purchase")


class PurchasePropertyResponse(BaseModel):
    success: bool
    property_id: str
    property_name: str
    price_paid: int
    new_balance: int
    passive_income: int


class UpgradePropertyRequest(BaseModel):
    property_id: str = Field(..., description="Property ID to upgrade")
    upgrade_type: str = Field(..., description="Type of upgrade")


class RentPropertyRequest(BaseModel):
    property_id: str = Field(..., description="Property ID to rent")
    tenant_id: str = Field(..., description="Tenant player ID")
    rent_amount: int = Field(..., ge=1, description="Monthly rent amount")
    duration_days: int = Field(
        default=30, ge=1, le=365, description="Rental duration")
