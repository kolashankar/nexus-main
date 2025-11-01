from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema_dict, handler):
        schema_dict.update(type="string")
        return schema_dict

class JobBase(BaseModel):
    title: str
    company: str
    description: str
    location: str
    job_type: str  # full-time, part-time, contract, remote
    category: str  # software, marketing, finance, etc.
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "USD"
    experience_level: str  # entry, mid, senior
    skills_required: List[str] = []
    qualifications: List[str] = []
    responsibilities: List[str] = []
    benefits: List[str] = []
    application_deadline: Optional[datetime] = None
    company_logo: Optional[str] = None
    apply_link: Optional[str] = None
    is_active: bool = True

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    category: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: Optional[str] = None
    experience_level: Optional[str] = None
    skills_required: Optional[List[str]] = None
    qualifications: Optional[List[str]] = None
    responsibilities: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    application_deadline: Optional[datetime] = None
    company_logo: Optional[str] = None
    apply_link: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class JobResponse(JobBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
