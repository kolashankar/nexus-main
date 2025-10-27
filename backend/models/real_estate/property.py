from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class PropertyUpgrade(BaseModel):
    """Property upgrade."""
    type: str = Field(..., description="Upgrade type")
    applied_date: datetime = Field(default_factory=datetime.utcnow)
    cost: int = Field(..., ge=0)
    income_boost: int = Field(default=0)


class Property(BaseModel):
    """Real estate property model."""
    id: str = Field(..., description="Unique property ID")
    name: str = Field(..., description="Property name")
    description: str = Field(..., description="Property description")

    property_type: str = Field(
        ...,
        description="Property type (apartment, house, mansion, commercial, industrial)"
    )
    size: int = Field(..., ge=1, description="Size in square meters")

    location: Dict[str, Any] = Field(..., description="Property location")
    territory_id: int = Field(..., description="Territory ID")

    price: int = Field(..., ge=0, description="Purchase price")
    passive_income: int = Field(
        default=0, ge=0, description="Daily passive income")
    maintenance_cost: int = Field(
        default=0, ge=0, description="Daily maintenance cost")

    owner_id: Optional[str] = Field(
        default=None, description="Owner player ID")
    tenant_id: Optional[str] = Field(
        default=None, description="Tenant player ID")

    status: str = Field(default="available", description="Property status")
    purchase_date: Optional[datetime] = Field(default=None)

    upgrades: List[PropertyUpgrade] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "apartment_1",
                "name": "Downtown Apartment",
                "description": "Cozy apartment in the city center",
                "property_type": "apartment",
                "size": 60,
                "location": {"x": 100, "y": 200, "territory_id": 1},
                "territory_id": 1,
                "price": 50000,
                "passive_income": 100,
                "maintenance_cost": 20,
                "status": "available"
            }
        }
