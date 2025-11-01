"""
Career Tools Models
8-Level Nested Architecture: models/schemas/career_tools/fields/validators/custom/career_tools_model.py
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CareerToolPromptTemplate(BaseModel):
    """Prompt template for career tools"""
    id: Optional[str] = Field(None, description="Template ID")
    tool_type: str = Field(..., description="Tool type: resume_review, cover_letter, ats_hack, cold_email")
    prompt_template: str = Field(..., description="Gemini AI prompt template")
    is_active: bool = Field(default=True, description="Template is active")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool_type": "resume_review",
                "prompt_template": "Review the following resume and provide detailed feedback...",
                "is_active": True
            }
        }


class ResumeReviewRequest(BaseModel):
    """Request for resume review"""
    resume_text: str = Field(..., description="Resume text content")
    target_role: Optional[str] = Field(None, description="Target job role")
    industry: Optional[str] = Field(None, description="Target industry")


class CoverLetterRequest(BaseModel):
    """Request for cover letter generation"""
    job_title: str = Field(..., description="Job title")
    company_name: str = Field(..., description="Company name")
    job_description: Optional[str] = Field(None, description="Job description")
    user_experience: Optional[str] = Field(None, description="User's relevant experience")
    user_skills: Optional[List[str]] = Field(None, description="User's skills")
    tone: str = Field(default="professional", description="Tone: professional, enthusiastic, formal")


class ATSHackRequest(BaseModel):
    """Request for ATS optimization"""
    resume_text: str = Field(..., description="Resume text content")
    job_description: str = Field(..., description="Target job description")
    keywords: Optional[List[str]] = Field(None, description="Additional keywords to optimize for")


class ColdEmailRequest(BaseModel):
    """Request for cold email generation"""
    recipient_name: Optional[str] = Field(None, description="Recipient's name")
    recipient_title: Optional[str] = Field(None, description="Recipient's job title")
    company_name: str = Field(..., description="Company name")
    purpose: str = Field(..., description="Purpose of email: job_inquiry, networking, informational_interview")
    sender_background: Optional[str] = Field(None, description="Sender's background/experience")
    tone: str = Field(default="professional", description="Tone: professional, friendly, formal")


class CareerToolUsage(BaseModel):
    """Career tool usage record"""
    id: Optional[str] = Field(None, description="Usage ID")
    user_id: str = Field(..., description="User ID")
    tool_type: str = Field(..., description="Tool type")
    input_data: Dict[str, Any] = Field(..., description="Input data")
    output_data: str = Field(..., description="AI-generated output")
    tokens_used: Optional[int] = Field(None, description="API tokens used")
    created_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "tool_type": "resume_review",
                "input_data": {"resume_text": "..."},
                "output_data": "AI feedback...",
                "tokens_used": 1500
            }
        }


class PromptTemplateCreate(BaseModel):
    """Schema for creating prompt template"""
    tool_type: str = Field(..., description="Tool type: resume_review, cover_letter, ats_hack, cold_email")
    prompt_template: str = Field(..., description="Prompt template with placeholders")
    is_active: bool = True


class PromptTemplateUpdate(BaseModel):
    """Schema for updating prompt template"""
    prompt_template: Optional[str] = None
    is_active: Optional[bool] = None
