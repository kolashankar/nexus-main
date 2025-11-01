"""
Authentication Models
8-Level Nested Architecture: models/schemas/auth/fields/validators/custom/auth_model.py
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class AdminUser(BaseModel):
    """Admin user model"""
    id: Optional[str] = Field(None, description="User ID (MongoDB _id)")
    email: EmailStr = Field(..., description="Admin email")
    username: str = Field(..., description="Admin username", min_length=3, max_length=50)
    password_hash: str = Field(..., description="Hashed password")
    full_name: str = Field(..., description="Full name")
    
    # Role and permissions
    role: str = Field(default="admin", description="Role: admin")
    is_active: bool = Field(default=True, description="Account is active")
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@careerguide.com",
                "username": "admin",
                "full_name": "Admin User",
                "role": "admin",
                "is_active": True
            }
        }


class AppUser(BaseModel):
    """Mobile app user model"""
    id: Optional[str] = Field(None, description="User ID (MongoDB _id)")
    email: EmailStr = Field(..., description="User email")
    username: Optional[str] = Field(None, description="Username", min_length=3, max_length=50)
    password_hash: str = Field(..., description="Hashed password")
    full_name: str = Field(..., description="Full name")
    phone: Optional[str] = Field(None, description="Phone number")
    
    # Profile
    profile_picture: Optional[str] = Field(None, description="Profile picture URL or base64")
    bio: Optional[str] = Field(None, description="User bio")
    education: Optional[str] = Field(None, description="Education level")
    experience: Optional[str] = Field(None, description="Years of experience")
    skills: list[str] = Field(default=[], description="Skills")
    
    # Account status
    is_active: bool = Field(default=True, description="Account is active")
    is_verified: bool = Field(default=False, description="Email is verified")
    
    # Career tools usage
    career_tools_used: int = Field(default=0, description="Number of career tools used")
    
    # Timestamps
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "phone": "+1234567890",
                "education": "B.Tech",
                "experience": "2 years",
                "skills": ["Python", "React", "Node.js"]
            }
        }


class AdminRegister(BaseModel):
    """Schema for admin registration"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str
    role: str = "admin"


class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str
    username: Optional[str] = None
    phone: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"
    user_type: str  # "admin" or "user"
    user_id: str
    email: str
    full_name: str


class ChangePasswordRequest(BaseModel):
    """Schema for password change"""
    old_password: str
    new_password: str = Field(..., min_length=8)


class UpdateProfileRequest(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[list[str]] = None
