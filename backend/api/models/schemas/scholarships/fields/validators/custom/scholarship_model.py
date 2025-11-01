from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class ScholarshipBase(BaseModel):
    title: str
    provider: str
    description: str
    amount: float
    currency: str = "USD"
    eligibility_criteria: List[str] = []
    benefits: List[str] = []
    application_process: str
    deadline: Optional[datetime] = None
    scholarship_type: str  # merit-based, need-based, etc.
    field_of_study: List[str] = []
    education_level: str  # undergraduate, graduate, PhD
    country: str
    apply_link: Optional[str] = None
    is_active: bool = True

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ScholarshipCreate(ScholarshipBase):
    pass

class ScholarshipUpdate(BaseModel):
    title: Optional[str] = None
    provider: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    eligibility_criteria: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    application_process: Optional[str] = None
    deadline: Optional[datetime] = None
    scholarship_type: Optional[str] = None
    field_of_study: Optional[List[str]] = None
    education_level: Optional[str] = None
    country: Optional[str] = None
    apply_link: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ScholarshipResponse(ScholarshipBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
