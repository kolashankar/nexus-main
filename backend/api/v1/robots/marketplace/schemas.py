"""Robot marketplace schemas."""

from pydantic import BaseModel, Field


class ListRobotRequest(BaseModel):
    """Request to list a robot for sale."""
    robot_id: str = Field(..., description="ID of robot to sell")
    price: int = Field(..., gt=0, description="Asking price in credits")


class BuyRobotRequest(BaseModel):
    """Request to buy a robot."""
    listing_id: str = Field(..., description="ID of the marketplace listing")
