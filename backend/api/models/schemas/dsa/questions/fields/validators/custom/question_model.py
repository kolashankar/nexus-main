from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class DSAQuestionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str = Field(..., min_length=10)
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")
    topics: List[str] = Field(default_factory=list)  # List of topic IDs
    companies: List[str] = Field(default_factory=list)  # Companies that asked this
    
    # Problem details
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None
    examples: List[dict] = Field(default_factory=list)  # [{"input": "...", "output": "...", "explanation": "..."}]
    
    # Solutions
    solution_approach: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    code_solutions: List[dict] = Field(default_factory=list)  # [{"language": "python", "code": "..."}]
    
    # Additional info
    hints: List[str] = Field(default_factory=list)
    related_questions: List[str] = Field(default_factory=list)  # Question IDs
    video_solution_url: Optional[str] = None
    
    # Stats
    acceptance_rate: Optional[float] = Field(None, ge=0, le=100)
    total_submissions: int = 0
    total_accepted: int = 0
    
    is_active: bool = True
    is_premium: bool = False

class DSAQuestionCreate(DSAQuestionBase):
    pass

class DSAQuestionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    topics: Optional[List[str]] = None
    companies: Optional[List[str]] = None
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None
    examples: Optional[List[dict]] = None
    solution_approach: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    code_solutions: Optional[List[dict]] = None
    hints: Optional[List[str]] = None
    related_questions: Optional[List[str]] = None
    video_solution_url: Optional[str] = None
    acceptance_rate: Optional[float] = Field(None, ge=0, le=100)
    total_submissions: Optional[int] = None
    total_accepted: Optional[int] = None
    is_active: Optional[bool] = None
    is_premium: Optional[bool] = None

class DSAQuestionResponse(DSAQuestionBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
