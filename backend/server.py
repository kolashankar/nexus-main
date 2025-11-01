from fastapi import FastAPI, APIRouter, Query, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import models
from api.models.schemas.jobs.fields.validators.custom.job_model import JobCreate, JobUpdate, JobResponse
from api.models.schemas.internships.fields.validators.custom.internship_model import InternshipCreate, InternshipUpdate, InternshipResponse
from api.models.schemas.scholarships.fields.validators.custom.scholarship_model import ScholarshipCreate, ScholarshipUpdate, ScholarshipResponse
from api.models.schemas.articles.fields.validators.custom.article_model import ArticleCreate, ArticleUpdate, ArticleResponse
from api.models.schemas.dsa.topics.fields.validators.custom.topic_model import DSATopicCreate, DSATopicUpdate, DSATopicResponse
from api.models.schemas.dsa.questions.fields.validators.custom.question_model import DSAQuestionCreate, DSAQuestionUpdate, DSAQuestionResponse
from api.models.schemas.dsa.sheets.fields.validators.custom.sheet_model import DSASheetCreate, DSASheetUpdate, DSASheetResponse
from api.models.schemas.dsa.companies.fields.validators.custom.company_model import CompanyCreate, CompanyUpdate, Company
from api.models.schemas.roadmaps.fields.validators.custom.roadmap_model import RoadmapCreate, RoadmapUpdate, Roadmap, RoadmapNode, RoadmapAIGenerate
from api.models.schemas.auth.fields.validators.custom.auth_model import AdminRegister, UserRegister, LoginRequest, ChangePasswordRequest, UpdateProfileRequest
from api.models.schemas.career_tools.fields.validators.custom.career_tools_model import (
    ResumeReviewRequest, CoverLetterRequest, ATSHackRequest, ColdEmailRequest, 
    PromptTemplateCreate, PromptTemplateUpdate
)

# Import handlers
from api.routes.admin.jobs.management.crud.operations.handlers.job_handlers import JobHandlers
from api.routes.admin.internships.management.crud.operations.handlers.internship_handlers import InternshipHandlers
from api.routes.admin.scholarships.management.crud.operations.handlers.scholarship_handlers import ScholarshipHandlers
from api.routes.admin.articles.management.crud.operations.handlers.article_handlers import ArticleHandlers
from api.routes.admin.dsa.topics.management.crud.operations.handlers.topic_handlers import DSATopicHandlers
from api.routes.admin.dsa.questions.management.crud.operations.handlers.question_handlers import DSAQuestionHandlers
from api.routes.admin.dsa.sheets.management.crud.operations.handlers.sheet_handlers import DSASheetHandlers
from api.routes.admin.dsa.companies.management.crud.operations.handlers.company_handlers import CompanyHandlers
from api.routes.admin.roadmaps.management.crud.operations.handlers.roadmap_handlers import RoadmapHandlers
from api.routes.auth.management.operations.handlers.auth_handlers import AuthHandlers
from api.routes.career_tools.management.operations.handlers.career_tools_handlers import CareerToolsHandlers
from api.routes.admin.analytics.management.crud.operations.handlers.analytics_handlers import AnalyticsHandlers
from api.routes.admin.bulk.management.operations.handlers.bulk_handlers import BulkOperationsHandlers
from api.routes.admin.advanced.management.operations.handlers.advanced_handlers import ContentApprovalHandlers, PushNotificationHandlers

# Import AI generators
from api.utils.ai.gemini.generators.jobs.prompts.generator import GeminiJobGenerator
from api.utils.ai.gemini.generators.articles.prompts.generator import GeminiArticleGenerator
from api.utils.ai.gemini.generators.dsa.questions.prompts.generator import GeminiDSAGenerator
from api.utils.ai.gemini.generators.roadmaps.prompts.generator import GeminiRoadmapGenerator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize handlers
job_handlers = JobHandlers(db)
internship_handlers = InternshipHandlers(db)
scholarship_handlers = ScholarshipHandlers(db)
article_handlers = ArticleHandlers(db)
dsa_topic_handlers = DSATopicHandlers(db)
dsa_question_handlers = DSAQuestionHandlers(db)
dsa_sheet_handlers = DSASheetHandlers(db)
company_handlers = CompanyHandlers(db)
roadmap_handlers = RoadmapHandlers(db)
auth_handlers = AuthHandlers(db)
analytics_handlers = AnalyticsHandlers(db)
bulk_operations_handlers = BulkOperationsHandlers(db)
content_approval_handlers = ContentApprovalHandlers(db)
push_notification_handlers = PushNotificationHandlers(db)

# Initialize Gemini AI
gemini_api_key = os.environ.get('GEMINI_API_KEY')
gemini_generator = GeminiJobGenerator(gemini_api_key) if gemini_api_key else None
article_gemini_generator = GeminiArticleGenerator(gemini_api_key) if gemini_api_key else None
dsa_gemini_generator = GeminiDSAGenerator(gemini_api_key) if gemini_api_key else None
roadmap_gemini_generator = GeminiRoadmapGenerator(gemini_api_key) if gemini_api_key else None
career_tools_handlers = CareerToolsHandlers(db, gemini_api_key) if gemini_api_key else None

# Security
security = HTTPBearer()

# =============================================================================
# AUTH DEPENDENCY
# =============================================================================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from token"""
    token = credentials.credentials
    user = await auth_handlers.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

async def get_current_admin(user = Depends(get_current_user)):
    """Ensure current user is admin"""
    if user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# Create the main app without a prefix
app = FastAPI(title="CareerGuide API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# =============================================================================
# ADMIN ROUTES - JOBS
# =============================================================================

@api_router.post("/admin/jobs", response_model=dict, tags=["Admin - Jobs"])
async def create_job(job: JobCreate):
    """Create a new job listing manually"""
    return await job_handlers.create_job(job.dict())

@api_router.post("/admin/jobs/generate-ai", response_model=dict, tags=["Admin - Jobs"])
async def generate_job_with_ai(
    job_title: str = Query(..., description="Job title"),
    company: str = Query(..., description="Company name"),
    location: str = Query(..., description="Job location"),
    job_type: str = Query(default="full-time", description="Job type"),
    category: str = Query(default="technology", description="Job category"),
    experience_level: str = Query(default="mid", description="Experience level")
):
    """Generate a job listing using Gemini AI"""
    if not gemini_generator:
        return {"error": "Gemini API not configured"}
    
    prompt_data = {
        "job_title": job_title,
        "company": company,
        "location": location,
        "job_type": job_type,
        "category": category,
        "experience_level": experience_level
    }
    
    generated_job = await gemini_generator.generate_job_listing(prompt_data)
    return await job_handlers.create_job(generated_job)

@api_router.get("/admin/jobs", tags=["Admin - Jobs"])
async def get_all_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1, ge=-1, le=1)
):
    """Get all jobs with filtering, searching, and sorting"""
    return await job_handlers.get_all_jobs(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        job_type=job_type,
        experience_level=experience_level,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/jobs/{job_id}", tags=["Admin - Jobs"])
async def get_job(job_id: str):
    """Get a specific job by ID"""
    return await job_handlers.get_job_by_id(job_id)

@api_router.put("/admin/jobs/{job_id}", tags=["Admin - Jobs"])
async def update_job(job_id: str, job: JobUpdate):
    """Update a job listing"""
    return await job_handlers.update_job(job_id, job.dict(exclude_unset=True))

@api_router.delete("/admin/jobs/{job_id}", tags=["Admin - Jobs"])
async def delete_job(job_id: str):
    """Delete a job listing"""
    return await job_handlers.delete_job(job_id)

# =============================================================================
# ADMIN ROUTES - INTERNSHIPS
# =============================================================================

@api_router.post("/admin/internships", response_model=dict, tags=["Admin - Internships"])
async def create_internship(internship: InternshipCreate):
    """Create a new internship listing manually"""
    return await internship_handlers.create_internship(internship.dict())

@api_router.post("/admin/internships/generate-ai", response_model=dict, tags=["Admin - Internships"])
async def generate_internship_with_ai(
    title: str = Query(...),
    company: str = Query(...),
    location: str = Query(...),
    duration: str = Query(default="3 months"),
    category: str = Query(default="technology")
):
    """Generate an internship listing using Gemini AI"""
    if not gemini_generator:
        return {"error": "Gemini API not configured"}
    
    prompt_data = {
        "title": title,
        "company": company,
        "location": location,
        "duration": duration,
        "category": category
    }
    
    generated_internship = await gemini_generator.generate_internship_listing(prompt_data)
    return await internship_handlers.create_internship(generated_internship)

@api_router.get("/admin/internships", tags=["Admin - Internships"])
async def get_all_internships(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    internship_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1, ge=-1, le=1)
):
    """Get all internships with filtering and sorting"""
    return await internship_handlers.get_all_internships(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        internship_type=internship_type,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/internships/{internship_id}", tags=["Admin - Internships"])
async def get_internship(internship_id: str):
    """Get a specific internship by ID"""
    return await internship_handlers.get_internship_by_id(internship_id)

@api_router.put("/admin/internships/{internship_id}", tags=["Admin - Internships"])
async def update_internship(internship_id: str, internship: InternshipUpdate):
    """Update an internship listing"""
    return await internship_handlers.update_internship(internship_id, internship.dict(exclude_unset=True))

@api_router.delete("/admin/internships/{internship_id}", tags=["Admin - Internships"])
async def delete_internship(internship_id: str):
    """Delete an internship listing"""
    return await internship_handlers.delete_internship(internship_id)

# =============================================================================
# ADMIN ROUTES - SCHOLARSHIPS
# =============================================================================

@api_router.post("/admin/scholarships", response_model=dict, tags=["Admin - Scholarships"])
async def create_scholarship(scholarship: ScholarshipCreate):
    """Create a new scholarship listing manually"""
    return await scholarship_handlers.create_scholarship(scholarship.dict())

@api_router.post("/admin/scholarships/generate-ai", response_model=dict, tags=["Admin - Scholarships"])
async def generate_scholarship_with_ai(
    title: str = Query(...),
    provider: str = Query(...),
    country: str = Query(...),
    education_level: str = Query(default="undergraduate")
):
    """Generate a scholarship listing using Gemini AI"""
    if not gemini_generator:
        return {"error": "Gemini API not configured"}
    
    prompt_data = {
        "title": title,
        "provider": provider,
        "country": country,
        "education_level": education_level
    }
    
    generated_scholarship = await gemini_generator.generate_scholarship_listing(prompt_data)
    return await scholarship_handlers.create_scholarship(generated_scholarship)

@api_router.get("/admin/scholarships", tags=["Admin - Scholarships"])
async def get_all_scholarships(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    scholarship_type: Optional[str] = Query(None),
    education_level: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1, ge=-1, le=1)
):
    """Get all scholarships with filtering and sorting"""
    return await scholarship_handlers.get_all_scholarships(
        skip=skip,
        limit=limit,
        search=search,
        scholarship_type=scholarship_type,
        education_level=education_level,
        country=country,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/scholarships/{scholarship_id}", tags=["Admin - Scholarships"])
async def get_scholarship(scholarship_id: str):
    """Get a specific scholarship by ID"""
    return await scholarship_handlers.get_scholarship_by_id(scholarship_id)

@api_router.put("/admin/scholarships/{scholarship_id}", tags=["Admin - Scholarships"])
async def update_scholarship(scholarship_id: str, scholarship: ScholarshipUpdate):
    """Update a scholarship listing"""
    return await scholarship_handlers.update_scholarship(scholarship_id, scholarship.dict(exclude_unset=True))

@api_router.delete("/admin/scholarships/{scholarship_id}", tags=["Admin - Scholarships"])
async def delete_scholarship(scholarship_id: str):
    """Delete a scholarship listing"""
    return await scholarship_handlers.delete_scholarship(scholarship_id)

# =============================================================================
# ADMIN ROUTES - ARTICLES
# =============================================================================

@api_router.post("/admin/articles", response_model=dict, tags=["Admin - Articles"])
async def create_article(article: ArticleCreate):
    """Create a new article manually"""
    return await article_handlers.create_article(article.dict())

@api_router.post("/admin/articles/generate-ai", response_model=dict, tags=["Admin - Articles"])
async def generate_article_with_ai(
    title: str = Query(..., description="Article title"),
    category: str = Query(default="technology", description="Article category"),
    author: str = Query(default="Admin", description="Author name"),
    target_audience: str = Query(default="professionals and students", description="Target audience"),
    key_points: Optional[str] = Query(None, description="Comma-separated key points to cover")
):
    """Generate an article using Gemini AI"""
    if not article_gemini_generator:
        return {"error": "Gemini API not configured"}
    
    prompt_data = {
        "title": title,
        "category": category,
        "author": author,
        "target_audience": target_audience
    }
    
    # Parse key points if provided
    if key_points:
        prompt_data["key_points"] = [kp.strip() for kp in key_points.split(",")]
    
    generated_article = await article_gemini_generator.generate_article(prompt_data)
    return await article_handlers.create_article(generated_article)

@api_router.get("/admin/articles", tags=["Admin - Articles"])
async def get_all_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    is_published: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1, ge=-1, le=1)
):
    """Get all articles with filtering and sorting"""
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else None
    
    return await article_handlers.get_all_articles(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        tags=tags_list,
        is_published=is_published,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/articles/{article_id}", tags=["Admin - Articles"])
async def get_article(article_id: str):
    """Get a specific article by ID"""
    return await article_handlers.get_article_by_id(article_id)

@api_router.put("/admin/articles/{article_id}", tags=["Admin - Articles"])
async def update_article(article_id: str, article: ArticleUpdate):
    """Update an article"""
    return await article_handlers.update_article(article_id, article.dict(exclude_unset=True))

@api_router.delete("/admin/articles/{article_id}", tags=["Admin - Articles"])
async def delete_article(article_id: str):
    """Delete an article"""
    return await article_handlers.delete_article(article_id)

@api_router.post("/admin/articles/{article_id}/toggle-publish", tags=["Admin - Articles"])
async def toggle_article_publish(article_id: str):
    """Toggle article publish status"""
    return await article_handlers.toggle_publish_status(article_id)

# =============================================================================
# ADMIN ROUTES - DSA TOPICS
# =============================================================================

@api_router.post("/admin/dsa/topics", response_model=dict, tags=["Admin - DSA Topics"])
async def create_dsa_topic(topic: DSATopicCreate):
    """Create a new DSA topic"""
    return await dsa_topic_handlers.create_topic(topic.dict())

@api_router.get("/admin/dsa/topics", tags=["Admin - DSA Topics"])
async def get_all_dsa_topics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    parent_topic: Optional[str] = Query(None),
    sort_by: str = Query("name"),
    sort_order: int = Query(1)
):
    """Get all DSA topics with filtering and sorting"""
    return await dsa_topic_handlers.get_all_topics(
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active,
        parent_topic=parent_topic,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/dsa/topics/stats", tags=["Admin - DSA Topics"])
async def get_dsa_topic_stats():
    """Get statistics for DSA topics"""
    return await dsa_topic_handlers.get_topic_stats()

@api_router.get("/admin/dsa/topics/{topic_id}", tags=["Admin - DSA Topics"])
async def get_dsa_topic(topic_id: str):
    """Get a specific DSA topic by ID"""
    return await dsa_topic_handlers.get_topic(topic_id)

@api_router.put("/admin/dsa/topics/{topic_id}", tags=["Admin - DSA Topics"])
async def update_dsa_topic(topic_id: str, topic: DSATopicUpdate):
    """Update a DSA topic"""
    return await dsa_topic_handlers.update_topic(topic_id, topic.dict(exclude_unset=True))

@api_router.delete("/admin/dsa/topics/{topic_id}", tags=["Admin - DSA Topics"])
async def delete_dsa_topic(topic_id: str):
    """Delete a DSA topic"""
    return await dsa_topic_handlers.delete_topic(topic_id)

# =============================================================================
# ADMIN ROUTES - DSA QUESTIONS
# =============================================================================

@api_router.post("/admin/dsa/questions", response_model=dict, tags=["Admin - DSA Questions"])
async def create_dsa_question(question: DSAQuestionCreate):
    """Create a new DSA question manually"""
    return await dsa_question_handlers.create_question(question.dict())

@api_router.post("/admin/dsa/questions/generate-ai", response_model=dict, tags=["Admin - DSA Questions"])
async def generate_dsa_question_with_ai(
    topic: str = Query(..., description="Main topic (e.g., Arrays, Trees)"),
    difficulty: str = Query(default="medium", description="Difficulty level"),
    company: Optional[str] = Query(None, description="Company context (optional)")
):
    """Generate a DSA question using Gemini AI"""
    if not dsa_gemini_generator:
        return {"error": "Gemini API not configured"}
    
    prompt_data = {
        "topic": topic,
        "difficulty": difficulty,
        "company": company
    }
    
    generated_question = await dsa_gemini_generator.generate_dsa_question(prompt_data)
    return await dsa_question_handlers.create_question(generated_question)

@api_router.get("/admin/dsa/questions", tags=["Admin - DSA Questions"])
async def get_all_dsa_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    topics: Optional[str] = Query(None, description="Comma-separated topic IDs"),
    company: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_premium: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1)
):
    """Get all DSA questions with filtering and sorting"""
    return await dsa_question_handlers.get_all_questions(
        skip=skip,
        limit=limit,
        search=search,
        difficulty=difficulty,
        topics=topics,
        company=company,
        is_active=is_active,
        is_premium=is_premium,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/dsa/questions/stats/difficulty", tags=["Admin - DSA Questions"])
async def get_questions_by_difficulty():
    """Get question count by difficulty"""
    return await dsa_question_handlers.get_questions_by_difficulty()

@api_router.get("/admin/dsa/questions/stats/topic", tags=["Admin - DSA Questions"])
async def get_questions_by_topic():
    """Get question count by topic"""
    return await dsa_question_handlers.get_questions_by_topic()

@api_router.get("/admin/dsa/questions/{question_id}", tags=["Admin - DSA Questions"])
async def get_dsa_question(question_id: str):
    """Get a specific DSA question by ID"""
    return await dsa_question_handlers.get_question(question_id)

@api_router.put("/admin/dsa/questions/{question_id}", tags=["Admin - DSA Questions"])
async def update_dsa_question(question_id: str, question: DSAQuestionUpdate):
    """Update a DSA question"""
    return await dsa_question_handlers.update_question(question_id, question.dict(exclude_unset=True))

@api_router.delete("/admin/dsa/questions/{question_id}", tags=["Admin - DSA Questions"])
async def delete_dsa_question(question_id: str):
    """Delete a DSA question"""
    return await dsa_question_handlers.delete_question(question_id)

@api_router.post("/admin/dsa/questions/{question_id}/submit", tags=["Admin - DSA Questions"])
async def submit_dsa_question(question_id: str, is_accepted: bool = Query(False)):
    """Record a submission for a question"""
    return await dsa_question_handlers.increment_submission(question_id, is_accepted)

# =============================================================================
# ADMIN ROUTES - DSA SHEETS
# =============================================================================

@api_router.post("/admin/dsa/sheets", response_model=dict, tags=["Admin - DSA Sheets"])
async def create_dsa_sheet(sheet: DSASheetCreate):
    """Create a new DSA sheet manually"""
    return await dsa_sheet_handlers.create_sheet(sheet.dict())

@api_router.post("/admin/dsa/sheets/generate-ai", response_model=dict, tags=["Admin - DSA Sheets"])
async def generate_dsa_sheet_with_ai(
    sheet_name: str = Query(..., description="Sheet name"),
    level: str = Query(default="intermediate", description="Difficulty level"),
    focus_topics: str = Query(default="Arrays,Strings,Trees", description="Comma-separated topics")
):
    """Generate a DSA sheet using Gemini AI"""
    if not dsa_gemini_generator:
        return {"error": "Gemini API not configured"}
    
    prompt_data = {
        "sheet_name": sheet_name,
        "level": level,
        "focus_topics": [topic.strip() for topic in focus_topics.split(",")]
    }
    
    generated_sheet = await dsa_gemini_generator.generate_dsa_sheet(prompt_data)
    return await dsa_sheet_handlers.create_sheet(generated_sheet)

@api_router.get("/admin/dsa/sheets", tags=["Admin - DSA Sheets"])
async def get_all_dsa_sheets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    is_published: Optional[bool] = Query(None),
    is_featured: Optional[bool] = Query(None),
    is_premium: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1)
):
    """Get all DSA sheets with filtering and sorting"""
    return await dsa_sheet_handlers.get_all_sheets(
        skip=skip,
        limit=limit,
        search=search,
        level=level,
        tag=tag,
        is_published=is_published,
        is_featured=is_featured,
        is_premium=is_premium,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/dsa/sheets/stats", tags=["Admin - DSA Sheets"])
async def get_dsa_sheet_stats():
    """Get statistics for DSA sheets"""
    return await dsa_sheet_handlers.get_sheet_stats()

@api_router.get("/admin/dsa/sheets/{sheet_id}", tags=["Admin - DSA Sheets"])
async def get_dsa_sheet(sheet_id: str):
    """Get a specific DSA sheet by ID"""
    return await dsa_sheet_handlers.get_sheet(sheet_id)

@api_router.put("/admin/dsa/sheets/{sheet_id}", tags=["Admin - DSA Sheets"])
async def update_dsa_sheet(sheet_id: str, sheet: DSASheetUpdate):
    """Update a DSA sheet"""
    return await dsa_sheet_handlers.update_sheet(sheet_id, sheet.dict(exclude_unset=True))

@api_router.delete("/admin/dsa/sheets/{sheet_id}", tags=["Admin - DSA Sheets"])
async def delete_dsa_sheet(sheet_id: str):
    """Delete a DSA sheet"""
    return await dsa_sheet_handlers.delete_sheet(sheet_id)

@api_router.post("/admin/dsa/sheets/{sheet_id}/questions", tags=["Admin - DSA Sheets"])
async def add_question_to_sheet(
    sheet_id: str,
    question_id: str = Query(...),
    order: int = Query(0)
):
    """Add a question to a DSA sheet"""
    return await dsa_sheet_handlers.add_question_to_sheet(sheet_id, question_id, order)

@api_router.delete("/admin/dsa/sheets/{sheet_id}/questions/{question_id}", tags=["Admin - DSA Sheets"])
async def remove_question_from_sheet(sheet_id: str, question_id: str):
    """Remove a question from a DSA sheet"""
    return await dsa_sheet_handlers.remove_question_from_sheet(sheet_id, question_id)

@api_router.post("/admin/dsa/sheets/{sheet_id}/toggle-publish", tags=["Admin - DSA Sheets"])
async def toggle_sheet_publish(sheet_id: str):
    """Toggle publish status of a DSA sheet"""
    return await dsa_sheet_handlers.toggle_publish(sheet_id)

# =============================================================================
# ADMIN ROUTES - DSA COMPANIES
# =============================================================================

@api_router.post("/admin/dsa/companies", response_model=dict, tags=["Admin - DSA Companies"])
async def create_company(company: CompanyCreate):
    """Create a new company"""
    return await company_handlers.create_company(company.dict())

@api_router.get("/admin/dsa/companies", tags=["Admin - DSA Companies"])
async def get_all_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: str = Query("name"),
    sort_order: str = Query("asc")
):
    """Get list of companies with filters"""
    return await company_handlers.get_companies(
        skip=skip,
        limit=limit,
        search=search,
        industry=industry,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/dsa/companies/stats", tags=["Admin - DSA Companies"])
async def get_company_stats():
    """Get company statistics"""
    return await company_handlers.get_statistics()

@api_router.get("/admin/dsa/companies/top", tags=["Admin - DSA Companies"])
async def get_top_companies(
    limit: int = Query(10, ge=1, le=50),
    by: str = Query("problems", description="Sort by 'problems' or 'jobs'")
):
    """Get top companies by problem count or job count"""
    return await company_handlers.get_top_companies(limit=limit, by=by)

@api_router.get("/admin/dsa/companies/{company_id}", tags=["Admin - DSA Companies"])
async def get_company(company_id: str):
    """Get single company by ID"""
    return await company_handlers.get_company_by_id(company_id)

@api_router.put("/admin/dsa/companies/{company_id}", tags=["Admin - DSA Companies"])
async def update_company(company_id: str, company: CompanyUpdate):
    """Update company"""
    return await company_handlers.update_company(company_id, company.dict(exclude_unset=True))

@api_router.delete("/admin/dsa/companies/{company_id}", tags=["Admin - DSA Companies"])
async def delete_company(company_id: str):
    """Delete company"""
    success = await company_handlers.delete_company(company_id)
    return {"success": success, "message": "Company deleted" if success else "Company not found"}

# =============================================================================
# ADMIN ROUTES - ROADMAPS
# =============================================================================

@api_router.post("/admin/roadmaps", response_model=dict, tags=["Admin - Roadmaps"])
async def create_roadmap(roadmap: RoadmapCreate):
    """Create a new roadmap manually"""
    return await roadmap_handlers.create_roadmap(roadmap.dict())

@api_router.post("/admin/roadmaps/generate-ai", response_model=dict, tags=["Admin - Roadmaps"])
async def generate_roadmap_with_ai(prompt_data: RoadmapAIGenerate):
    """Generate a complete roadmap using Gemini AI"""
    if not roadmap_gemini_generator:
        return {"error": "Gemini API not configured"}
    
    generated_roadmap = await roadmap_gemini_generator.generate_roadmap(prompt_data.dict())
    return await roadmap_handlers.create_roadmap(generated_roadmap)

@api_router.get("/admin/roadmaps", tags=["Admin - Roadmaps"])
async def get_all_roadmaps(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    subcategory: Optional[str] = Query(None),
    difficulty_level: Optional[str] = Query(None),
    is_published: Optional[bool] = Query(None),
    is_active: Optional[bool] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc")
):
    """Get list of roadmaps with filters"""
    return await roadmap_handlers.get_roadmaps(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        subcategory=subcategory,
        difficulty_level=difficulty_level,
        is_published=is_published,
        is_active=is_active,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/admin/roadmaps/stats", tags=["Admin - Roadmaps"])
async def get_roadmap_stats():
    """Get roadmap statistics"""
    return await roadmap_handlers.get_statistics()

@api_router.get("/admin/roadmaps/{roadmap_id}", tags=["Admin - Roadmaps"])
async def get_roadmap(roadmap_id: str):
    """Get single roadmap by ID"""
    return await roadmap_handlers.get_roadmap_by_id(roadmap_id)

@api_router.put("/admin/roadmaps/{roadmap_id}", tags=["Admin - Roadmaps"])
async def update_roadmap(roadmap_id: str, roadmap: RoadmapUpdate):
    """Update roadmap"""
    return await roadmap_handlers.update_roadmap(roadmap_id, roadmap.dict(exclude_unset=True))

@api_router.delete("/admin/roadmaps/{roadmap_id}", tags=["Admin - Roadmaps"])
async def delete_roadmap(roadmap_id: str):
    """Delete roadmap"""
    success = await roadmap_handlers.delete_roadmap(roadmap_id)
    return {"success": success, "message": "Roadmap deleted" if success else "Roadmap not found"}

@api_router.post("/admin/roadmaps/{roadmap_id}/toggle-publish", tags=["Admin - Roadmaps"])
async def toggle_roadmap_publish(roadmap_id: str):
    """Toggle publish status of a roadmap"""
    return await roadmap_handlers.toggle_publish(roadmap_id)

@api_router.post("/admin/roadmaps/{roadmap_id}/nodes", tags=["Admin - Roadmaps"])
async def add_roadmap_node(roadmap_id: str, node: RoadmapNode):
    """Add a node to roadmap"""
    return await roadmap_handlers.add_node(roadmap_id, node.dict())

@api_router.put("/admin/roadmaps/{roadmap_id}/nodes/{node_id}", tags=["Admin - Roadmaps"])
async def update_roadmap_node(roadmap_id: str, node_id: str, node: RoadmapNode):
    """Update a specific node in roadmap"""
    return await roadmap_handlers.update_node(roadmap_id, node_id, node.dict())

@api_router.delete("/admin/roadmaps/{roadmap_id}/nodes/{node_id}", tags=["Admin - Roadmaps"])
async def delete_roadmap_node(roadmap_id: str, node_id: str):
    """Delete a node from roadmap"""
    return await roadmap_handlers.delete_node(roadmap_id, node_id)

# =============================================================================
# AUTHENTICATION ROUTES
# =============================================================================

# Admin registration disabled - use default admin (kolashankar113@gmail.com / Shankar@113)
# Sub-admins can be created by super admin through the admin panel
# @api_router.post("/auth/admin/register", tags=["Authentication"])
# async def register_admin(admin_data: AdminRegister):
#     """Register a new admin user"""
#     return await auth_handlers.register_admin(admin_data.dict())

@api_router.post("/auth/admin/login", tags=["Authentication"])
async def login_admin(login_data: LoginRequest):
    """Admin login"""
    return await auth_handlers.login_admin(login_data.email, login_data.password)

@api_router.post("/auth/user/register", tags=["Authentication"])
async def register_user(user_data: UserRegister):
    """Register a new app user"""
    return await auth_handlers.register_user(user_data.dict())

@api_router.post("/auth/user/login", tags=["Authentication"])
async def login_user(login_data: LoginRequest):
    """App user login"""
    return await auth_handlers.login_user(login_data.email, login_data.password)

@api_router.get("/auth/me", tags=["Authentication"])
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return {"success": True, "user": current_user}

@api_router.put("/auth/profile", tags=["Authentication"])
async def update_profile(update_data: UpdateProfileRequest, current_user = Depends(get_current_user)):
    """Update user profile"""
    if current_user.get("user_type") != "user":
        raise HTTPException(status_code=403, detail="Only app users can update profile")
    return await auth_handlers.update_user_profile(current_user["id"], update_data.dict(exclude_unset=True))

@api_router.post("/auth/change-password", tags=["Authentication"])
async def change_password(password_data: ChangePasswordRequest, current_user = Depends(get_current_user)):
    """Change user password"""
    return await auth_handlers.change_password(
        current_user["id"], 
        current_user.get("user_type", "user"),
        password_data.old_password,
        password_data.new_password
    )

# =============================================================================
# SUB-ADMIN MANAGEMENT ROUTES (Super Admin Only)
# =============================================================================

@api_router.post("/admin/sub-admins", tags=["Admin Management"])
async def create_sub_admin(admin_data: AdminRegister, current_user = Depends(get_current_user)):
    """Create a new sub-admin (Super Admin only)"""
    if current_user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await auth_handlers.create_sub_admin(admin_data.dict(), current_user.get("role", "admin"))

@api_router.get("/admin/sub-admins", tags=["Admin Management"])
async def get_all_admins(
    skip: int = 0,
    limit: int = 50,
    role: Optional[str] = None,
    current_user = Depends(get_current_user)
):
    """Get list of all admins (Super Admin only)"""
    if current_user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if current_user.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Super admin access required")
    return await auth_handlers.get_all_admins(skip, limit, role)

@api_router.get("/admin/sub-admins/{admin_id}", tags=["Admin Management"])
async def get_admin_by_id(admin_id: str, current_user = Depends(get_current_user)):
    """Get single admin by ID (Super Admin only)"""
    if current_user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    if current_user.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Super admin access required")
    admin = await auth_handlers.get_admin_by_id(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"success": True, "admin": admin}

@api_router.put("/admin/sub-admins/{admin_id}", tags=["Admin Management"])
async def update_admin(
    admin_id: str,
    update_data: Dict[str, Any],
    current_user = Depends(get_current_user)
):
    """Update admin details (Super Admin only)"""
    if current_user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await auth_handlers.update_admin(admin_id, update_data, current_user.get("role", "admin"))

@api_router.delete("/admin/sub-admins/{admin_id}", tags=["Admin Management"])
async def delete_admin(admin_id: str, current_user = Depends(get_current_user)):
    """Delete admin (Super Admin only)"""
    if current_user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await auth_handlers.delete_admin(admin_id, current_user.get("role", "admin"))

@api_router.post("/admin/sub-admins/{admin_id}/toggle-status", tags=["Admin Management"])
async def toggle_admin_status(admin_id: str, current_user = Depends(get_current_user)):
    """Toggle admin active status (Super Admin only)"""
    if current_user.get("user_type") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return await auth_handlers.toggle_admin_status(admin_id, current_user.get("role", "admin"))

# =============================================================================
# CAREER TOOLS ROUTES (Auth Required)
# =============================================================================

@api_router.post("/career-tools/resume-review", tags=["Career Tools"])
async def review_resume(request_data: ResumeReviewRequest, current_user = Depends(get_current_user)):
    """Review resume using AI (Auth Required)"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.review_resume(current_user["id"], request_data.dict())

@api_router.post("/career-tools/cover-letter", tags=["Career Tools"])
async def generate_cover_letter(request_data: CoverLetterRequest, current_user = Depends(get_current_user)):
    """Generate cover letter using AI (Auth Required)"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.generate_cover_letter(current_user["id"], request_data.dict())

@api_router.post("/career-tools/ats-hack", tags=["Career Tools"])
async def optimize_for_ats(request_data: ATSHackRequest, current_user = Depends(get_current_user)):
    """Optimize resume for ATS using AI (Auth Required)"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.optimize_for_ats(current_user["id"], request_data.dict())

@api_router.post("/career-tools/cold-email", tags=["Career Tools"])
async def generate_cold_email(request_data: ColdEmailRequest, current_user = Depends(get_current_user)):
    """Generate cold email using AI (Auth Required)"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.generate_cold_email(current_user["id"], request_data.dict())

@api_router.get("/career-tools/my-usage", tags=["Career Tools"])
async def get_my_usage(current_user = Depends(get_current_user)):
    """Get user's career tools usage history"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.get_user_usage(current_user["id"])

# =============================================================================
# ADMIN ROUTES - CAREER TOOLS MANAGEMENT
# =============================================================================

@api_router.post("/admin/career-tools/templates", tags=["Admin - Career Tools"])
async def create_prompt_template(template_data: PromptTemplateCreate, admin = Depends(get_current_admin)):
    """Create new prompt template"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.create_template(template_data.dict())

@api_router.get("/admin/career-tools/templates", tags=["Admin - Career Tools"])
async def get_all_templates(admin = Depends(get_current_admin)):
    """Get all prompt templates"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.get_templates()

@api_router.put("/admin/career-tools/templates/{template_id}", tags=["Admin - Career Tools"])
async def update_prompt_template(template_id: str, template_data: PromptTemplateUpdate, admin = Depends(get_current_admin)):
    """Update prompt template"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.update_template(template_id, template_data.dict(exclude_unset=True))

@api_router.delete("/admin/career-tools/templates/{template_id}", tags=["Admin - Career Tools"])
async def delete_prompt_template(template_id: str, admin = Depends(get_current_admin)):
    """Delete prompt template"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    success = await career_tools_handlers.delete_template(template_id)
    return {"success": success, "message": "Template deleted" if success else "Template not found"}

@api_router.get("/admin/career-tools/stats", tags=["Admin - Career Tools"])
async def get_usage_stats(admin = Depends(get_current_admin)):
    """Get career tools usage statistics"""
    if not career_tools_handlers:
        raise HTTPException(status_code=503, detail="Career tools service not available")
    return await career_tools_handlers.get_usage_stats()

# =============================================================================
# ADMIN ROUTES - ANALYTICS DASHBOARD (MODULE 5)
# =============================================================================

@api_router.get("/admin/analytics/dashboard", tags=["Admin - Analytics"])
async def get_analytics_dashboard(admin = Depends(get_current_admin)):
    """Get complete analytics dashboard data"""
    return await analytics_handlers.get_dashboard_analytics()

@api_router.get("/admin/analytics/user-engagement", tags=["Admin - Analytics"])
async def get_user_engagement_metrics(admin = Depends(get_current_admin)):
    """Get user engagement metrics"""
    metrics = await analytics_handlers.get_user_engagement_metrics()
    return {"success": True, "data": metrics}

@api_router.get("/admin/analytics/job-applications", tags=["Admin - Analytics"])
async def get_job_application_metrics(admin = Depends(get_current_admin)):
    """Get job application statistics"""
    metrics = await analytics_handlers.get_job_application_metrics()
    return {"success": True, "data": metrics}

@api_router.get("/admin/analytics/gemini-usage", tags=["Admin - Analytics"])
async def get_gemini_usage_metrics(admin = Depends(get_current_admin)):
    """Get Gemini API usage tracking"""
    metrics = await analytics_handlers.get_gemini_api_usage_metrics()
    return {"success": True, "data": metrics}

@api_router.get("/admin/analytics/api-logs", tags=["Admin - Analytics"])
async def get_api_logs(
    admin = Depends(get_current_admin),
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0),
    status_code: Optional[int] = Query(None)
):
    """Get API usage logs"""
    return await analytics_handlers.get_api_usage_logs(limit=limit, skip=skip, status_code=status_code)

@api_router.get("/admin/analytics/error-logs", tags=["Admin - Analytics"])
async def get_error_logs(
    admin = Depends(get_current_admin),
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0)
):
    """Get error logs (status code >= 400)"""
    return await analytics_handlers.get_error_logs(limit=limit, skip=skip)

# =============================================================================
# ADMIN ROUTES - BULK OPERATIONS (MODULE 6)
# =============================================================================

@api_router.get("/admin/bulk/jobs/export", tags=["Admin - Bulk Operations"])
async def export_jobs_csv(admin = Depends(get_current_admin)):
    """Export jobs to CSV format"""
    from fastapi.responses import StreamingResponse
    import io
    
    csv_data = await bulk_operations_handlers.export_jobs_csv()
    
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=jobs_export.csv"}
    )

@api_router.post("/admin/bulk/jobs/import", tags=["Admin - Bulk Operations"])
async def import_jobs_csv(csv_data: str, admin = Depends(get_current_admin)):
    """Import jobs from CSV data"""
    return await bulk_operations_handlers.import_jobs_csv(csv_data)

@api_router.get("/admin/bulk/internships/export", tags=["Admin - Bulk Operations"])
async def export_internships_csv(admin = Depends(get_current_admin)):
    """Export internships to CSV format"""
    from fastapi.responses import StreamingResponse
    import io
    
    csv_data = await bulk_operations_handlers.export_internships_csv()
    
    return StreamingResponse(
        io.StringIO(csv_data),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=internships_export.csv"}
    )

@api_router.post("/admin/bulk/internships/import", tags=["Admin - Bulk Operations"])
async def import_internships_csv(csv_data: str, admin = Depends(get_current_admin)):
    """Import internships from CSV data"""
    return await bulk_operations_handlers.import_internships_csv(csv_data)

@api_router.post("/admin/bulk/jobs/delete", tags=["Admin - Bulk Operations"])
async def bulk_delete_jobs(job_ids: List[str], admin = Depends(get_current_admin)):
    """Delete multiple jobs"""
    return await bulk_operations_handlers.bulk_delete_jobs(job_ids)

@api_router.post("/admin/bulk/internships/delete", tags=["Admin - Bulk Operations"])
async def bulk_delete_internships(internship_ids: List[str], admin = Depends(get_current_admin)):
    """Delete multiple internships"""
    return await bulk_operations_handlers.bulk_delete_internships(internship_ids)

@api_router.post("/admin/bulk/jobs/update-status", tags=["Admin - Bulk Operations"])
async def bulk_update_jobs_status(job_ids: List[str], is_active: bool, admin = Depends(get_current_admin)):
    """Update status for multiple jobs"""
    return await bulk_operations_handlers.bulk_update_jobs_status(job_ids, is_active)

@api_router.post("/admin/bulk/internships/update-status", tags=["Admin - Bulk Operations"])
async def bulk_update_internships_status(internship_ids: List[str], is_active: bool, admin = Depends(get_current_admin)):
    """Update status for multiple internships"""
    return await bulk_operations_handlers.bulk_update_internships_status(internship_ids, is_active)

# =============================================================================
# ADMIN ROUTES - CONTENT APPROVAL WORKFLOW (MODULE 6)
# =============================================================================

@api_router.post("/admin/content/submit", tags=["Admin - Content Approval"])
async def submit_content(
    content_type: str,
    content_data: Dict,
    user = Depends(get_current_user)
):
    """Submit content for admin approval"""
    return await content_approval_handlers.submit_content_for_approval(
        content_type=content_type,
        content_data=content_data,
        submitted_by=user.get("id")
    )

@api_router.get("/admin/content/pending", tags=["Admin - Content Approval"])
async def get_pending_submissions(
    admin = Depends(get_current_admin),
    content_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0)
):
    """Get all pending content submissions"""
    return await content_approval_handlers.get_pending_submissions(
        content_type=content_type,
        limit=limit,
        skip=skip
    )

@api_router.post("/admin/content/{submission_id}/approve", tags=["Admin - Content Approval"])
async def approve_submission(
    submission_id: str,
    review_notes: Optional[str] = None,
    admin = Depends(get_current_admin)
):
    """Approve a content submission"""
    return await content_approval_handlers.approve_submission(
        submission_id=submission_id,
        reviewed_by=admin.get("id"),
        review_notes=review_notes
    )

@api_router.post("/admin/content/{submission_id}/reject", tags=["Admin - Content Approval"])
async def reject_submission(
    submission_id: str,
    review_notes: str,
    admin = Depends(get_current_admin)
):
    """Reject a content submission"""
    return await content_approval_handlers.reject_submission(
        submission_id=submission_id,
        reviewed_by=admin.get("id"),
        review_notes=review_notes
    )

@api_router.get("/admin/content/stats", tags=["Admin - Content Approval"])
async def get_content_approval_stats(admin = Depends(get_current_admin)):
    """Get content approval statistics"""
    return await content_approval_handlers.get_submission_stats()

# =============================================================================
# ADMIN ROUTES - PUSH NOTIFICATIONS (MODULE 6)
# =============================================================================

@api_router.post("/admin/notifications", tags=["Admin - Push Notifications"])
async def create_notification(
    title: str,
    message: str,
    target: str = Query(..., description="all, specific_users, admins"),
    target_ids: Optional[List[str]] = None,
    data: Optional[Dict] = None,
    admin = Depends(get_current_admin)
):
    """Create a push notification"""
    return await push_notification_handlers.create_notification(
        title=title,
        message=message,
        target=target,
        target_ids=target_ids,
        data=data
    )

@api_router.get("/admin/notifications", tags=["Admin - Push Notifications"])
async def get_notifications(
    admin = Depends(get_current_admin),
    status: Optional[str] = Query(None, description="pending, sent, failed"),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0)
):
    """Get push notifications"""
    return await push_notification_handlers.get_notifications(
        status=status,
        limit=limit,
        skip=skip
    )

@api_router.post("/admin/notifications/{notification_id}/send", tags=["Admin - Push Notifications"])
async def send_notification(notification_id: str, admin = Depends(get_current_admin)):
    """Send a push notification"""
    return await push_notification_handlers.send_notification(notification_id)

@api_router.delete("/admin/notifications/{notification_id}", tags=["Admin - Push Notifications"])
async def delete_notification(notification_id: str, admin = Depends(get_current_admin)):
    """Delete a push notification"""
    return await push_notification_handlers.delete_notification(notification_id)

@api_router.get("/admin/notifications/stats", tags=["Admin - Push Notifications"])
async def get_notification_stats(admin = Depends(get_current_admin)):
    """Get push notification statistics"""
    return await push_notification_handlers.get_notification_stats()

# =============================================================================
# USER ROUTES - JOBS (Public facing)
# =============================================================================

@api_router.get("/user/jobs", tags=["User - Jobs"])
async def get_user_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1)
):
    """Public endpoint for users to browse active jobs"""
    return await job_handlers.get_all_jobs(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        job_type=job_type,
        experience_level=experience_level,
        is_active=True,  # Only show active jobs
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/user/jobs/{job_id}", tags=["User - Jobs"])
async def get_user_job(job_id: str):
    """Public endpoint to get a specific job"""
    return await job_handlers.get_job_by_id(job_id)

@api_router.get("/user/internships", tags=["User - Internships"])
async def get_user_internships(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    internship_type: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1)
):
    """Public endpoint for users to browse active internships"""
    return await internship_handlers.get_all_internships(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        internship_type=internship_type,
        is_active=True,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/user/scholarships", tags=["User - Scholarships"])
async def get_user_scholarships(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    scholarship_type: Optional[str] = Query(None),
    education_level: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1)
):
    """Public endpoint for users to browse active scholarships"""
    return await scholarship_handlers.get_all_scholarships(
        skip=skip,
        limit=limit,
        search=search,
        scholarship_type=scholarship_type,
        education_level=education_level,
        country=country,
        is_active=True,
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/user/articles", tags=["User - Articles"])
async def get_user_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: int = Query(-1)
):
    """Public endpoint for users to browse published articles"""
    tags_list = [tag.strip() for tag in tags.split(",")] if tags else None
    
    return await article_handlers.get_all_articles(
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        tags=tags_list,
        is_published=True,  # Only show published articles
        sort_by=sort_by,
        sort_order=sort_order
    )

@api_router.get("/user/articles/{article_id}", tags=["User - Articles"])
async def get_user_article(article_id: str):
    """Public endpoint to get a specific article (increments view count)"""
    return await article_handlers.get_article_by_id(article_id)

# =============================================================================
# USER - DSA ENDPOINTS
# =============================================================================

@api_router.get("/user/dsa/topics", tags=["User - DSA"])
async def get_user_dsa_topics(
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Public endpoint to get DSA topics"""
    filters = {}
    if is_active is not None:
        filters["is_active"] = is_active
    if search:
        filters["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    topics_cursor = dsa_topics_collection.find(filters).skip(skip).limit(limit)
    topics = await topics_cursor.to_list(length=limit)
    
    for topic in topics:
        topic["_id"] = str(topic["_id"])
        if "created_at" in topic:
            topic["created_at"] = topic["created_at"].isoformat()
        if "updated_at" in topic:
            topic["updated_at"] = topic["updated_at"].isoformat()
    
    return {"success": True, "data": topics}

@api_router.get("/user/dsa/questions", tags=["User - DSA"])
async def get_user_dsa_questions(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    company: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Public endpoint to get DSA questions"""
    filters = {}
    if difficulty:
        filters["difficulty"] = difficulty
    if topic:
        filters["topics"] = topic
    if company:
        filters["companies"] = company
    if search:
        filters["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    questions_cursor = dsa_questions_collection.find(filters).skip(skip).limit(limit)
    questions = await questions_cursor.to_list(length=limit)
    
    for question in questions:
        question["_id"] = str(question["_id"])
        if "created_at" in question:
            question["created_at"] = question["created_at"].isoformat()
        if "updated_at" in question:
            question["updated_at"] = question["updated_at"].isoformat()
    
    return {"success": True, "data": questions}

@api_router.get("/user/dsa/questions/{question_id}", tags=["User - DSA"])
async def get_user_dsa_question(question_id: str):
    """Public endpoint to get a specific DSA question"""
    if not ObjectId.is_valid(question_id):
        raise HTTPException(status_code=400, detail="Invalid question ID")
    
    question = await dsa_questions_collection.find_one({"_id": ObjectId(question_id)})
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question["_id"] = str(question["_id"])
    if "created_at" in question:
        question["created_at"] = question["created_at"].isoformat()
    if "updated_at" in question:
        question["updated_at"] = question["updated_at"].isoformat()
    
    return {"success": True, "data": question}

@api_router.get("/user/dsa/sheets", tags=["User - DSA"])
async def get_user_dsa_sheets(
    is_published: Optional[bool] = True,
    level: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Public endpoint to get DSA sheets (only published)"""
    filters = {}
    if is_published is not None:
        filters["is_published"] = is_published
    if level:
        filters["level"] = level
    if search:
        filters["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    sheets_cursor = dsa_sheets_collection.find(filters).skip(skip).limit(limit)
    sheets = await sheets_cursor.to_list(length=limit)
    
    for sheet in sheets:
        sheet["_id"] = str(sheet["_id"])
        if "created_at" in sheet:
            sheet["created_at"] = sheet["created_at"].isoformat()
        if "updated_at" in sheet:
            sheet["updated_at"] = sheet["updated_at"].isoformat()
    
    return {"success": True, "data": sheets}

@api_router.get("/user/dsa/companies", tags=["User - DSA"])
async def get_user_dsa_companies(
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Public endpoint to get DSA companies"""
    filters = {}
    if is_active is not None:
        filters["is_active"] = is_active
    if search:
        filters["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"industry": {"$regex": search, "$options": "i"}}
        ]
    
    companies_cursor = dsa_companies_collection.find(filters).skip(skip).limit(limit)
    companies = await companies_cursor.to_list(length=limit)
    
    for company in companies:
        company["_id"] = str(company["_id"])
        if "created_at" in company:
            company["created_at"] = company["created_at"].isoformat()
        if "updated_at" in company:
            company["updated_at"] = company["updated_at"].isoformat()
    
    return {"success": True, "data": companies}

@api_router.get("/user/dsa/companies/top", tags=["User - DSA"])
async def get_user_top_dsa_companies(limit: int = 10):
    """Public endpoint to get top DSA companies by problem count"""
    companies_cursor = dsa_companies_collection.find({"is_active": True}).sort("problem_count", -1).limit(limit)
    companies = await companies_cursor.to_list(length=limit)
    
    for company in companies:
        company["_id"] = str(company["_id"])
        if "created_at" in company:
            company["created_at"] = company["created_at"].isoformat()
        if "updated_at" in company:
            company["updated_at"] = company["updated_at"].isoformat()
    
    return {"success": True, "data": companies}

@api_router.get("/user/dsa/dashboard", tags=["User - DSA"])
async def get_user_dsa_dashboard():
    """Public endpoint to get DSA dashboard data"""
    # Get counts
    topics_count = await dsa_topics_collection.count_documents({"is_active": True})
    questions_count = await dsa_questions_collection.count_documents({})
    sheets_count = await dsa_sheets_collection.count_documents({"is_published": True})
    companies_count = await dsa_companies_collection.count_documents({"is_active": True})
    
    # Get top topics by question count
    top_topics_cursor = dsa_topics_collection.find({"is_active": True}).sort("question_count", -1).limit(5)
    top_topics = await top_topics_cursor.to_list(length=5)
    
    # Get top companies
    top_companies_cursor = dsa_companies_collection.find({"is_active": True}).sort("problem_count", -1).limit(5)
    top_companies = await top_companies_cursor.to_list(length=5)
    
    for topic in top_topics:
        topic["_id"] = str(topic["_id"])
    
    for company in top_companies:
        company["_id"] = str(company["_id"])
    
    return {
        "success": True,
        "data": {
            "stats": {
                "total_topics": topics_count,
                "total_questions": questions_count,
                "total_sheets": sheets_count,
                "total_companies": companies_count
            },
            "top_topics": top_topics,
            "top_companies": top_companies
        }
    }

# =============================================================================
# USER - ROADMAPS ENDPOINTS
# =============================================================================

@api_router.get("/user/roadmaps", tags=["User - Roadmaps"])
async def get_user_roadmaps(
    is_published: Optional[bool] = True,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Public endpoint to get roadmaps (only published)"""
    filters = {}
    if is_published is not None:
        filters["is_published"] = is_published
    if category:
        filters["category"] = category
    if difficulty:
        filters["difficulty"] = difficulty
    if search:
        filters["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    roadmaps_cursor = roadmaps_collection.find(filters).skip(skip).limit(limit)
    roadmaps = await roadmaps_cursor.to_list(length=limit)
    
    for roadmap in roadmaps:
        roadmap["_id"] = str(roadmap["_id"])
        if "created_at" in roadmap:
            roadmap["created_at"] = roadmap["created_at"].isoformat()
        if "updated_at" in roadmap:
            roadmap["updated_at"] = roadmap["updated_at"].isoformat()
    
    return {"success": True, "data": roadmaps}

@api_router.get("/user/roadmaps/{roadmap_id}", tags=["User - Roadmaps"])
async def get_user_roadmap(roadmap_id: str):
    """Public endpoint to get a specific roadmap"""
    if not ObjectId.is_valid(roadmap_id):
        raise HTTPException(status_code=400, detail="Invalid roadmap ID")
    
    roadmap = await roadmaps_collection.find_one({"_id": ObjectId(roadmap_id), "is_published": True})
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    # Increment view count
    await roadmaps_collection.update_one(
        {"_id": ObjectId(roadmap_id)},
        {"$inc": {"views": 1}}
    )
    
    roadmap["_id"] = str(roadmap["_id"])
    if "created_at" in roadmap:
        roadmap["created_at"] = roadmap["created_at"].isoformat()
    if "updated_at" in roadmap:
        roadmap["updated_at"] = roadmap["updated_at"].isoformat()
    
    return {"success": True, "data": roadmap}

# =============================================================================
# Health Check
# =============================================================================

@api_router.get("/", tags=["Health"])
async def root():
    return {
        "message": "CareerGuide API",
        "version": "1.0.0",
        "status": "operational"
    }

@api_router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "gemini_ai": "configured" if gemini_generator else "not configured"
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
