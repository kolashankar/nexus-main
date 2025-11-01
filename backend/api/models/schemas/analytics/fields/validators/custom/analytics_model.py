from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class UserEngagementMetrics(BaseModel):
    """User engagement metrics"""
    total_users: int = 0
    active_users_today: int = 0
    active_users_week: int = 0
    active_users_month: int = 0
    avg_session_duration: float = 0.0
    total_sessions: int = 0

class JobApplicationMetrics(BaseModel):
    """Job application statistics"""
    total_applications: int = 0
    applications_today: int = 0
    applications_week: int = 0
    applications_month: int = 0
    avg_applications_per_job: float = 0.0
    top_jobs: List[Dict] = []

class GeminiAPIUsageMetrics(BaseModel):
    """Gemini API usage tracking"""
    total_requests: int = 0
    requests_today: int = 0
    requests_week: int = 0
    requests_month: int = 0
    by_feature: Dict[str, int] = {}
    avg_response_time: float = 0.0

class AnalyticsDashboard(BaseModel):
    """Complete analytics dashboard data"""
    user_engagement: UserEngagementMetrics
    job_applications: JobApplicationMetrics
    gemini_api_usage: GeminiAPIUsageMetrics
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class UserActivity(BaseModel):
    """Track user activity for analytics"""
    user_id: Optional[str] = None
    session_id: str
    action: str
    module: str
    metadata: Optional[Dict] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class APIUsageLog(BaseModel):
    """API usage logging"""
    endpoint: str
    method: str
    user_id: Optional[str] = None
    status_code: int
    response_time: float
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class GeminiAPILog(BaseModel):
    """Gemini API usage logging"""
    feature: str  # jobs, articles, dsa, roadmaps, career_tools
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    response_time: float
    success: bool = True
    error_message: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
