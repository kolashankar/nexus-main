"""
Career Tools Gemini Generator & Handlers
8-Level Nested Architecture: routes/career_tools/management/operations/handlers/career_tools_handlers.py
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import Dict, Any, Optional
import google.generativeai as genai


class CareerToolsHandlers:
    """Handlers for Career Tools with Gemini AI"""
    
    def __init__(self, db: AsyncIOMotorDatabase, gemini_api_key: str):
        self.db = db
        self.usage_collection = db.career_tool_usage
        self.templates_collection = db.career_tool_templates
        
        # Initialize Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        
        # Initialize default templates
        self.default_templates = {
            "resume_review": """
You are an expert career coach and resume reviewer. Analyze the following resume and provide comprehensive feedback.

Resume Content:
{resume_text}

Target Role: {target_role}
Industry: {industry}

Provide detailed feedback in the following format:

## Overall Assessment
[Brief overall assessment of the resume]

## Strengths
[List 3-5 key strengths]

## Areas for Improvement
[List specific areas that need improvement]

## Content Analysis
- **Experience Section**: [Feedback on experience descriptions]
- **Skills Section**: [Feedback on skills presentation]
- **Education Section**: [Feedback on education section]
- **Formatting**: [Feedback on layout and structure]

## Keyword Optimization
[Suggest important keywords for the target role that are missing]

## Action Items
[Provide 5-7 specific, actionable recommendations]

## ATS Compatibility Score
[Rate ATS compatibility out of 10 with explanation]

Make your feedback specific, actionable, and professional.
""",
            "cover_letter": """
You are an expert career writer. Generate a compelling cover letter based on the following details.

Job Title: {job_title}
Company Name: {company_name}
Job Description: {job_description}
Candidate Experience: {user_experience}
Candidate Skills: {user_skills}
Tone: {tone}

Generate a professional cover letter with the following structure:

[Your Name]
[Your Contact Information]
[Date]

[Hiring Manager]
{company_name}

Dear Hiring Manager,

[Opening paragraph - Strong hook expressing enthusiasm]

[Body paragraph 1 - Relevant experience and achievements]

[Body paragraph 2 - Specific skills and how they align with the role]

[Body paragraph 3 - Why you're interested in the company]

[Closing paragraph - Call to action]

Sincerely,
[Your Name]

Requirements:
- Use a {tone} tone throughout
- Highlight specific achievements with metrics when possible
- Show genuine interest in the company and role
- Keep it concise (300-400 words)
- Make it personalized and compelling
""",
            "ats_hack": """
You are an ATS (Applicant Tracking System) optimization expert. Analyze the resume against the job description and provide optimization recommendations.

Resume Content:
{resume_text}

Job Description:
{job_description}

Additional Keywords: {keywords}

Provide comprehensive ATS optimization advice in the following format:

## ATS Compatibility Score
[Current score out of 10 with detailed explanation]

## Keyword Analysis
### Missing Keywords
[List critical keywords from job description that are absent]

### Keyword Density
[Analyze if current keywords are used appropriately]

## Formatting Issues
[Identify any ATS-unfriendly formatting]

## Section Optimization
### Professional Summary
[Suggestions for optimization]

### Work Experience
[Suggestions with keyword integration]

### Skills Section
[Recommended additions and restructuring]

## Optimized Resume Sections
[Provide rewritten versions of key sections with proper keyword integration]

## Action Plan
[Step-by-step guide to optimize the resume for ATS]

Make recommendations specific and actionable.
""",
            "cold_email": """
You are an expert in professional networking and cold email outreach. Generate a compelling cold email based on the following details.

Recipient Name: {recipient_name}
Recipient Title: {recipient_title}
Company Name: {company_name}
Purpose: {purpose}
Sender Background: {sender_background}
Tone: {tone}

Generate a professional cold email with the following structure:

Subject: [Compelling subject line - keep it short and intriguing]

{recipient_name},

[Opening - Personalized connection or hook]

[Body paragraph 1 - Brief introduction and credibility]

[Body paragraph 2 - Value proposition or reason for reaching out]

[Body paragraph 3 - Clear, specific ask or call to action]

[Closing - Professional sign-off]

Best regards,
[Sender Name]

Requirements:
- Keep it concise (150-200 words)
- Use a {tone} tone
- Make it highly personalized
- Include a clear call to action
- Show respect for their time
- Avoid sounding desperate or overly salesy
"""
        }
    
    # =============================================================================
    # RESUME REVIEW
    # =============================================================================
    
    async def review_resume(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Review resume using Gemini AI"""
        try:
            # Get template
            template = await self._get_template("resume_review")
            
            # Format prompt
            prompt = template.format(
                resume_text=request_data.get("resume_text", ""),
                target_role=request_data.get("target_role", "Not specified"),
                industry=request_data.get("industry", "Not specified")
            )
            
            # Generate feedback
            response = self.model.generate_content(prompt)
            feedback = response.text.strip()
            
            # Log usage
            await self._log_usage(user_id, "resume_review", request_data, feedback)
            
            # Increment user counter
            await self._increment_user_counter(user_id)
            
            return {
                "success": True,
                "feedback": feedback,
                "tool_type": "resume_review"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # =============================================================================
    # COVER LETTER GENERATOR
    # =============================================================================
    
    async def generate_cover_letter(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cover letter using Gemini AI"""
        try:
            # Get template
            template = await self._get_template("cover_letter")
            
            # Format prompt
            skills = request_data.get("user_skills", [])
            skills_str = ", ".join(skills) if skills else "Not specified"
            
            prompt = template.format(
                job_title=request_data.get("job_title", ""),
                company_name=request_data.get("company_name", ""),
                job_description=request_data.get("job_description", "Not provided"),
                user_experience=request_data.get("user_experience", "Not specified"),
                user_skills=skills_str,
                tone=request_data.get("tone", "professional")
            )
            
            # Generate cover letter
            response = self.model.generate_content(prompt)
            cover_letter = response.text.strip()
            
            # Log usage
            await self._log_usage(user_id, "cover_letter", request_data, cover_letter)
            
            # Increment user counter
            await self._increment_user_counter(user_id)
            
            return {
                "success": True,
                "cover_letter": cover_letter,
                "tool_type": "cover_letter"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # =============================================================================
    # ATS HACK
    # =============================================================================
    
    async def optimize_for_ats(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize resume for ATS using Gemini AI"""
        try:
            # Get template
            template = await self._get_template("ats_hack")
            
            # Format prompt
            keywords = request_data.get("keywords", [])
            keywords_str = ", ".join(keywords) if keywords else "None specified"
            
            prompt = template.format(
                resume_text=request_data.get("resume_text", ""),
                job_description=request_data.get("job_description", ""),
                keywords=keywords_str
            )
            
            # Generate optimization advice
            response = self.model.generate_content(prompt)
            optimization = response.text.strip()
            
            # Log usage
            await self._log_usage(user_id, "ats_hack", request_data, optimization)
            
            # Increment user counter
            await self._increment_user_counter(user_id)
            
            return {
                "success": True,
                "optimization": optimization,
                "tool_type": "ats_hack"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # =============================================================================
    # COLD EMAIL GENERATOR
    # =============================================================================
    
    async def generate_cold_email(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cold email using Gemini AI"""
        try:
            # Get template
            template = await self._get_template("cold_email")
            
            # Format prompt
            prompt = template.format(
                recipient_name=request_data.get("recipient_name", "there"),
                recipient_title=request_data.get("recipient_title", ""),
                company_name=request_data.get("company_name", ""),
                purpose=request_data.get("purpose", "networking"),
                sender_background=request_data.get("sender_background", "Not specified"),
                tone=request_data.get("tone", "professional")
            )
            
            # Generate email
            response = self.model.generate_content(prompt)
            email = response.text.strip()
            
            # Log usage
            await self._log_usage(user_id, "cold_email", request_data, email)
            
            # Increment user counter
            await self._increment_user_counter(user_id)
            
            return {
                "success": True,
                "email": email,
                "tool_type": "cold_email"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # =============================================================================
    # PROMPT TEMPLATE MANAGEMENT
    # =============================================================================
    
    async def create_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new prompt template"""
        template_data["created_at"] = datetime.utcnow()
        template_data["updated_at"] = datetime.utcnow()
        
        result = await self.templates_collection.insert_one(template_data)
        template_data["_id"] = result.inserted_id
        
        return {"success": True, "template": self._format_template(template_data)}
    
    async def get_templates(self) -> Dict[str, Any]:
        """Get all prompt templates"""
        templates = await self.templates_collection.find().to_list(length=100)
        return {
            "success": True,
            "templates": [self._format_template(t) for t in templates]
        }
    
    async def update_template(self, template_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update prompt template"""
        try:
            update_data["updated_at"] = datetime.utcnow()
            
            result = await self.templates_collection.find_one_and_update(
                {"_id": ObjectId(template_id)},
                {"$set": update_data},
                return_document=True
            )
            
            return {"success": True, "template": self._format_template(result)} if result else {"success": False}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def delete_template(self, template_id: str) -> bool:
        """Delete prompt template"""
        try:
            result = await self.templates_collection.delete_one({"_id": ObjectId(template_id)})
            return result.deleted_count > 0
        except Exception:
            return False
    
    # =============================================================================
    # USAGE STATISTICS
    # =============================================================================
    
    async def get_user_usage(self, user_id: str) -> Dict[str, Any]:
        """Get user's career tools usage"""
        usage = await self.usage_collection.find({"user_id": user_id}).to_list(length=100)
        return {
            "success": True,
            "usage": [self._format_usage(u) for u in usage],
            "total_uses": len(usage)
        }
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get overall usage statistics"""
        pipeline = [
            {
                "$group": {
                    "_id": "$tool_type",
                    "count": {"$sum": 1},
                    "total_tokens": {"$sum": "$tokens_used"}
                }
            }
        ]
        
        stats = await self.usage_collection.aggregate(pipeline).to_list(length=10)
        
        return {
            "success": True,
            "stats": stats,
            "total_uses": sum(s["count"] for s in stats)
        }
    
    # =============================================================================
    # HELPER METHODS
    # =============================================================================
    
    async def _get_template(self, tool_type: str) -> str:
        """Get prompt template for tool type"""
        template = await self.templates_collection.find_one({
            "tool_type": tool_type,
            "is_active": True
        })
        
        if template:
            return template["prompt_template"]
        
        return self.default_templates.get(tool_type, "")
    
    async def _log_usage(self, user_id: str, tool_type: str, input_data: Dict, output_data: str):
        """Log career tool usage"""
        usage_data = {
            "user_id": user_id,
            "tool_type": tool_type,
            "input_data": input_data,
            "output_data": output_data,
            "tokens_used": len(output_data.split()),  # Rough estimate
            "created_at": datetime.utcnow()
        }
        await self.usage_collection.insert_one(usage_data)
    
    async def _increment_user_counter(self, user_id: str):
        """Increment user's career tools usage counter"""
        await self.db.app_users.update_one(
            {"_id": ObjectId(user_id)},
            {"$inc": {"career_tools_used": 1}}
        )
    
    def _format_template(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Format template for response"""
        if not template:
            return {}
        template["id"] = str(template.pop("_id"))
        if "created_at" in template:
            template["created_at"] = template["created_at"].isoformat()
        if "updated_at" in template:
            template["updated_at"] = template["updated_at"].isoformat()
        return template
    
    def _format_usage(self, usage: Dict[str, Any]) -> Dict[str, Any]:
        """Format usage record for response"""
        if not usage:
            return {}
        usage["id"] = str(usage.pop("_id"))
        if "created_at" in usage:
            usage["created_at"] = usage["created_at"].isoformat()
        return usage
