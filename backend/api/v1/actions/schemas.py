from pydantic import BaseModel, Field

class HackAction(BaseModel):
    target_id: str = Field(..., description="Player ID to hack")

class HelpAction(BaseModel):
    target_id: str = Field(..., description="Player ID to help")
    amount: int = Field(..., gt=0, description="Credits to give")

class StealAction(BaseModel):
    target_id: str = Field(..., description="Player ID to steal from")

class DonateAction(BaseModel):
    target_id: str = Field(..., description="Player ID to donate to")
    amount: int = Field(..., gt=0, description="Credits to donate")

class TradeAction(BaseModel):
    target_id: str = Field(..., description="Player ID to trade with")
    offer_amount: int = Field(..., gt=0, description="Credits to offer")
    request_amount: int = Field(..., gt=0, description="Credits requested")

class ActionResponse(BaseModel):
    success: bool
    message: str
    karma_change: int
    trait_changes: dict
    credits_change: int = 0
