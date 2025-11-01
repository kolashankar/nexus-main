from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class InternshipBase(BaseModel):
    title: str
    company: str
    description: str
    location: str
    duration: str  # 3 months, 6 months, etc.
    internship_type: str  # paid, unpaid, stipend
    category: str
    stipend_amount: Optional[float] = None
    currency: str = "USD"
    skills_required: List[str] = []
    qualifications: List[str] = []
    responsibilities: List[str] = []
    learning_outcomes: List[str] = []
    application_deadline: Optional[datetime] = None
    company_logo: Optional[str] = None
    apply_link: Optional[str] = None
    is_active: bool = True

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class InternshipCreate(InternshipBase):
    pass

class InternshipUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[str] = None
    internship_type: Optional[str] = None
    category: Optional[str] = None
    stipend_amount: Optional[float] = None
    currency: Optional[str] = None
    skills_required: Optional[List[str]] = None
    qualifications: Optional[List[str]] = None
    responsibilities: Optional[List[str]] = None
    learning_outcomes: Optional[List[str]] = None
    application_deadline: Optional[datetime] = None
    company_logo: Optional[str] = None
    apply_link: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class InternshipResponse(InternshipBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
