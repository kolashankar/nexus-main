from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Rental(BaseModel):
    """Property rental agreement."""
    id: str = Field(..., description="Unique rental ID")
    property_id: str = Field(..., description="Property ID")

    landlord_id: str = Field(..., description="Landlord player ID")
    tenant_id: str = Field(..., description="Tenant player ID")

    rent_amount: int = Field(..., ge=1, description="Monthly rent amount")
    duration_days: int = Field(..., ge=1,
                               description="Rental duration in days")

    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime = Field(..., description="Rental end date")

    status: str = Field(
        default="active", description="Rental status (active, expired, terminated)")

    payments_made: int = Field(
        default=0, ge=0, description="Number of payments made")
    last_payment_date: Optional[datetime] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "rental_123",
                "property_id": "apartment_1",
                "landlord_id": "player_1",
                "tenant_id": "player_2",
                "rent_amount": 1000,
                "duration_days": 30,
                "start_date": "2025-01-01T00:00:00Z",
                "end_date": "2025-01-31T23:59:59Z",
                "status": "active",
                "payments_made": 0
            }
        }
