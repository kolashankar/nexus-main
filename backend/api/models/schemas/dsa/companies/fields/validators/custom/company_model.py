"""
DSA Company Model
8-Level Nested Architecture: models/schemas/dsa/companies/fields/validators/custom/company_model.py
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Company(BaseModel):
    """Company model for DSA Corner - tracks companies associated with problems"""
    id: Optional[str] = Field(None, description="Company ID (MongoDB _id)")
    name: str = Field(..., description="Company name", min_length=1, max_length=100)
    logo: Optional[str] = Field(None, description="Company logo URL or base64")
    industry: str = Field(..., description="Industry/sector", min_length=1)
    website: Optional[str] = Field(None, description="Company website URL")
    description: Optional[str] = Field(None, description="Company description")
    
    # Statistics
    problem_count: int = Field(default=0, description="Number of DSA problems associated")
    job_count: int = Field(default=0, description="Number of job postings")
    
    # Metadata
    is_active: bool = Field(default=True, description="Company is active")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Google",
                "logo": "https://example.com/google-logo.png",
                "industry": "Technology",
                "website": "https://google.com",
                "description": "Multinational technology company",
                "problem_count": 150,
                "job_count": 25,
                "is_active": True
            }
        }


class CompanyCreate(BaseModel):
    """Schema for creating a new company"""
    name: str = Field(..., min_length=1, max_length=100)
    logo: Optional[str] = None
    industry: str = Field(..., min_length=1)
    website: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class CompanyUpdate(BaseModel):
    """Schema for updating a company"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    logo: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
