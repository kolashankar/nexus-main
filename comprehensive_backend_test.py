#!/usr/bin/env python3
"""
Comprehensive Backend Testing for CareerGuide API - ALL 7 MODULES
Testing scope:
1. DSA Companies Module (Module 1)
2. Roadmaps Module (Module 2) 
3. Authentication System (Module 3)
4. Career Tools Module (Module 4)
5. Analytics Dashboard (Module 5) - NEW FOCUS
6. Advanced Features (Module 6) - NEW FOCUS
   - Bulk Operations
   - Content Approval Workflow
   - Push Notifications Management
7. Admin Dashboard Pages (Module 7)
"""

import requests
import json
import uuid
import csv
import io
from typing import Dict, Any, Optional, List
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://dual-app-sync.preview.emergentagent.com/api"

class ComprehensiveBackendTester:
    def __init__(self):
        self.session = None
        self.admin_token = None
        self.user_token = None
        self.test_results = {
            "dsa_companies": [],
            "roadmaps": [],
            "authentication": [],
            "career_tools": [],
            "analytics": [],
            "bulk_operations": [],
            "content_approval": [],
            "push_notifications": []
        }
        self.created_resources = {
            "companies": [],
            "roadmaps": [],
            "admin_users": [],
            "app_users": [],
            "jobs": [],
            "internships": [],
            "notifications": [],
            "submissions": []
        }

    async def setup_session(self):
        """Setup HTTP session"""
        self.session = aiohttp.ClientSession()

    async def cleanup_session(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()

    async def make_request(self, method: str, endpoint: str, data: Dict = None, 
                          headers: Dict = None, params: Dict = None) -> Dict:
        """Make HTTP request to backend"""
        url = f"{BACKEND_URL}{endpoint}"
        
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
            
        try:
            async with self.session.request(
                method, url, 
                json=data if data else None,
                headers=default_headers,
                params=params
            ) as response:
                response_text = await response.text()
                try:
                    response_data = json.loads(response_text) if response_text else {}
                except json.JSONDecodeError:
                    response_data = {"raw_response": response_text}
                
                return {
                    "status_code": response.status,
                    "data": response_data,
                    "success": 200 <= response.status < 300
                }
        except Exception as e:
            return {
                "status_code": 0,
                "data": {"error": str(e)},
                "success": False
            }

    def log_test_result(self, module: str, test_name: str, success: bool, 
                       details: str, response_data: Dict = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results[module].append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} [{module.upper()}] {test_name}: {details}")

    # =============================================================================
    # AUTHENTICATION SYSTEM TESTS (Module 3)
    # =============================================================================

    async def test_authentication_system(self):
        """Test complete authentication system"""
        print("\n🔐 TESTING AUTHENTICATION SYSTEM (Module 3)...")
        
        # Test 1: Admin Registration
        admin_data = {
            "email": f"admin_{uuid.uuid4().hex[:8]}@careerguide.com",
            "username": f"admin_{uuid.uuid4().hex[:8]}",
            "password": "AdminPass123!",
            "full_name": "Test Admin User"
        }
        
        response = await self.make_request("POST", "/auth/admin/register", admin_data)
        success = response["success"] and response["data"].get("success", False)
        self.log_test_result("authentication", "Admin Registration", success,
                           f"Status: {response['status_code']}, Response: {response['data']}")
        
        if success:
            self.created_resources["admin_users"].append(admin_data["email"])

        # Test 2: Admin Login
        login_data = {"email": admin_data["email"], "password": admin_data["password"]}
        response = await self.make_request("POST", "/auth/admin/login", login_data)
        success = response["success"] and "token" in response["data"]
        
        if success:
            self.admin_token = response["data"]["token"]
            
        self.log_test_result("authentication", "Admin Login", success,
                           f"Status: {response['status_code']}, Token received: {'Yes' if success else 'No'}")

        # Test 3: User Registration
        user_data = {
            "email": f"user_{uuid.uuid4().hex[:8]}@careerguide.com",
            "password": "UserPass123!",
            "full_name": "Test App User"
        }
        
        response = await self.make_request("POST", "/auth/user/register", user_data)
        success = response["success"] and response["data"].get("success", False)
        self.log_test_result("authentication", "User Registration", success,
                           f"Status: {response['status_code']}, Response: {response['data']}")
        
        if success:
            self.created_resources["app_users"].append(user_data["email"])

        # Test 4: User Login
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = await self.make_request("POST", "/auth/user/login", login_data)
        success = response["success"] and "token" in response["data"]
        
        if success:
            self.user_token = response["data"]["token"]
            
        self.log_test_result("authentication", "User Login", success,
                           f"Status: {response['status_code']}, Token received: {'Yes' if success else 'No'}")

        # Test 5: Get Current User (with token)
        if self.user_token:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = await self.make_request("GET", "/auth/me", headers=headers)
            success = response["success"] and "user" in response["data"]
            self.log_test_result("authentication", "Get Current User", success,
                               f"Status: {response['status_code']}, User data received: {'Yes' if success else 'No'}")

    # =============================================================================
    # DSA COMPANIES MODULE TESTS (Module 1)
    # =============================================================================

    async def test_dsa_companies_module(self):
        """Test DSA Companies CRUD operations and statistics"""
        print("\n🏢 TESTING DSA COMPANIES MODULE (Module 1)...")
        
        # Test 1: Create Company
        company_data = {
            "name": "Microsoft Corporation",
            "logo": "https://example.com/microsoft-logo.png",
            "industry": "Technology",
            "website": "https://microsoft.com",
            "description": "Leading technology company specializing in software and cloud services"
        }
        
        response = await self.make_request("POST", "/admin/dsa/companies", company_data)
        success = response["success"] and response["data"].get("success", False)
        company_id = response["data"].get("company", {}).get("id") if success else None
        
        if company_id:
            self.created_resources["companies"].append(company_id)
            
        self.log_test_result("dsa_companies", "Create Company", success,
                           f"Status: {response['status_code']}, Company ID: {company_id}")

        # Test 2: Get All Companies
        response = await self.make_request("GET", "/admin/dsa/companies")
        success = response["success"] and "companies" in response["data"]
        companies_count = len(response["data"].get("companies", [])) if success else 0
        
        self.log_test_result("dsa_companies", "List Companies", success,
                           f"Status: {response['status_code']}, Companies found: {companies_count}")

        # Test 3: Get Company Statistics
        response = await self.make_request("GET", "/admin/dsa/companies/stats")
        success = response["success"] and "total_companies" in response["data"]
        
        self.log_test_result("dsa_companies", "Get Company Statistics", success,
                           f"Status: {response['status_code']}, Stats available: {'Yes' if success else 'No'}")

        # Test 4: Get Top Companies
        params = {"limit": 10, "by": "problems"}
        response = await self.make_request("GET", "/admin/dsa/companies/top", params=params)
        success = response["success"] and "companies" in response["data"]
        
        self.log_test_result("dsa_companies", "Get Top Companies", success,
                           f"Status: {response['status_code']}, Top companies retrieved: {'Yes' if success else 'No'}")

        # Test 5: Get Single Company
        if company_id:
            response = await self.make_request("GET", f"/admin/dsa/companies/{company_id}")
            success = response["success"] and "company" in response["data"]
            
            self.log_test_result("dsa_companies", "Get Single Company", success,
                               f"Status: {response['status_code']}, Company retrieved: {'Yes' if success else 'No'}")

        # Test 6: Update Company
        if company_id:
            update_data = {
                "description": "Updated: Leading technology company with cloud and AI solutions",
                "industry": "Technology & Cloud"
            }
            response = await self.make_request("PUT", f"/admin/dsa/companies/{company_id}", update_data)
            success = response["success"]
            
            self.log_test_result("dsa_companies", "Update Company", success,
                               f"Status: {response['status_code']}, Company updated: {'Yes' if success else 'No'}")

        # Test 7: Delete Company
        if company_id:
            response = await self.make_request("DELETE", f"/admin/dsa/companies/{company_id}")
            success = response["success"]
            
            self.log_test_result("dsa_companies", "Delete Company", success,
                               f"Status: {response['status_code']}, Company deleted: {'Yes' if success else 'No'}")

    # =============================================================================
    # ROADMAPS MODULE TESTS (Module 2)
    # =============================================================================

    async def test_roadmaps_module(self):
        """Test Roadmaps CRUD operations, AI generation, and node management"""
        print("\n🗺️ TESTING ROADMAPS MODULE (Module 2)...")
        
        # Test 1: AI Generate Roadmap (15-25 nodes)
        ai_data = {
            "title": "Data Science Roadmap 2025",
            "category": "tech_roadmap",
            "subcategory": "data_science",
            "difficulty_level": "intermediate"
        }
        
        response = await self.make_request("POST", "/admin/roadmaps/generate-ai", ai_data)
        success = response["success"] and response["data"].get("success", False)
        ai_roadmap_id = response["data"].get("roadmap", {}).get("id") if success else None
        nodes_count = len(response["data"].get("roadmap", {}).get("nodes", [])) if success else 0
        
        if ai_roadmap_id:
            self.created_resources["roadmaps"].append(ai_roadmap_id)
            
        # Verify 15-25 nodes were created
        nodes_valid = 15 <= nodes_count <= 25 if success else False
        
        self.log_test_result("roadmaps", "AI Generate Roadmap", success and nodes_valid,
                           f"Status: {response['status_code']}, Nodes created: {nodes_count}, Valid range (15-25): {'Yes' if nodes_valid else 'No'}")

        # Test 2: Get All Roadmaps
        response = await self.make_request("GET", "/admin/roadmaps")
        success = response["success"] and "roadmaps" in response["data"]
        roadmaps_count = len(response["data"].get("roadmaps", [])) if success else 0
        
        self.log_test_result("roadmaps", "List Roadmaps", success,
                           f"Status: {response['status_code']}, Roadmaps found: {roadmaps_count}")

        # Test 3: Get Single Roadmap
        if ai_roadmap_id:
            response = await self.make_request("GET", f"/admin/roadmaps/{ai_roadmap_id}")
            success = response["success"] and "roadmap" in response["data"]
            
            self.log_test_result("roadmaps", "Get Single Roadmap", success,
                               f"Status: {response['status_code']}, Roadmap retrieved: {'Yes' if success else 'No'}")

        # Test 4: Add Node to Roadmap
        if ai_roadmap_id:
            node_data = {
                "id": str(uuid.uuid4()),
                "title": "Advanced Statistics",
                "description": "Learn advanced statistical concepts",
                "node_type": "content",
                "position_x": 300,
                "position_y": 200,
                "is_completed": False,
                "dependencies": []
            }
            response = await self.make_request("POST", f"/admin/roadmaps/{ai_roadmap_id}/nodes", node_data)
            success = response["success"]
            
            self.log_test_result("roadmaps", "Add Node to Roadmap", success,
                               f"Status: {response['status_code']}, Node added: {'Yes' if success else 'No'}")

    # =============================================================================
    # CAREER TOOLS MODULE TESTS (Module 4)
    # =============================================================================

    async def test_career_tools_module(self):
        """Test Career Tools AI-powered features with authentication"""
        print("\n🛠️ TESTING CAREER TOOLS MODULE (Module 4)...")
        
        if not self.user_token:
            self.log_test_result("career_tools", "Authentication Check", False,
                               "No user token available - skipping career tools tests")
            return

        headers = {"Authorization": f"Bearer {self.user_token}"}

        # Test 1: Resume Review
        resume_data = {
            "resume_text": "Sarah Johnson\nData Scientist\n\nExperience:\n- 4 years at DataCorp\n- Developed ML models using Python and TensorFlow\n- Led analytics team of 6 members\n\nSkills:\n- Python, R, SQL, TensorFlow\n- AWS, GCP, Docker\n- Machine Learning, Statistics",
            "target_role": "Senior Data Scientist",
            "industry": "Technology"
        }
        
        response = await self.make_request("POST", "/career-tools/resume-review", resume_data, headers=headers)
        success = response["success"] and "review" in response["data"]
        
        self.log_test_result("career_tools", "Resume Review", success,
                           f"Status: {response['status_code']}, Review generated: {'Yes' if success else 'No'}")

        # Test 2: Cover Letter Generation
        cover_letter_data = {
            "job_title": "Senior Data Scientist",
            "company_name": "Netflix",
            "tone": "professional"
        }
        
        response = await self.make_request("POST", "/career-tools/cover-letter", cover_letter_data, headers=headers)
        success = response["success"] and "cover_letter" in response["data"]
        
        self.log_test_result("career_tools", "Cover Letter Generation", success,
                           f"Status: {response['status_code']}, Cover letter generated: {'Yes' if success else 'No'}")

        # Test 3: ATS Optimization
        ats_data = {
            "resume_text": "Sarah Johnson\nData Scientist with 4 years experience in machine learning",
            "job_description": "We are looking for a Senior Data Scientist with experience in Python, TensorFlow, and cloud technologies. Must have 4+ years experience and team leadership skills."
        }
        
        response = await self.make_request("POST", "/career-tools/ats-hack", ats_data, headers=headers)
        success = response["success"] and "optimized_resume" in response["data"]
        
        self.log_test_result("career_tools", "ATS Optimization", success,
                           f"Status: {response['status_code']}, ATS optimization generated: {'Yes' if success else 'No'}")

        # Test 4: Cold Email Generation
        cold_email_data = {
            "company_name": "Netflix",
            "purpose": "job_inquiry",
            "tone": "professional"
        }
        
        response = await self.make_request("POST", "/career-tools/cold-email", cold_email_data, headers=headers)
        success = response["success"] and "cold_email" in response["data"]
        
        self.log_test_result("career_tools", "Cold Email Generation", success,
                           f"Status: {response['status_code']}, Cold email generated: {'Yes' if success else 'No'}")

        # Test 5: Get User Usage History
        response = await self.make_request("GET", "/career-tools/my-usage", headers=headers)
        success = response["success"] and "usage_history" in response["data"]
        
        self.log_test_result("career_tools", "Get Usage History", success,
                           f"Status: {response['status_code']}, Usage history retrieved: {'Yes' if success else 'No'}")

    # =============================================================================
    # ANALYTICS DASHBOARD TESTS (Module 5) - NEW FOCUS
    # =============================================================================

    async def test_analytics_dashboard(self):
        """Test Analytics Dashboard endpoints"""
        print("\n📊 TESTING ANALYTICS DASHBOARD (Module 5) - NEW FOCUS...")
        
        if not self.admin_token:
            self.log_test_result("analytics", "Authentication Check", False,
                               "No admin token available - skipping analytics tests")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test 1: Get Complete Dashboard Analytics
        response = await self.make_request("GET", "/admin/analytics/dashboard", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        self.log_test_result("analytics", "Complete Dashboard Analytics", success,
                           f"Status: {response['status_code']}, Dashboard data retrieved: {'Yes' if success else 'No'}")

        # Test 2: Get User Engagement Metrics
        response = await self.make_request("GET", "/admin/analytics/user-engagement", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        self.log_test_result("analytics", "User Engagement Metrics", success,
                           f"Status: {response['status_code']}, Engagement metrics retrieved: {'Yes' if success else 'No'}")

        # Test 3: Get Job Application Statistics
        response = await self.make_request("GET", "/admin/analytics/job-applications", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        self.log_test_result("analytics", "Job Application Statistics", success,
                           f"Status: {response['status_code']}, Job stats retrieved: {'Yes' if success else 'No'}")

        # Test 4: Get Gemini API Usage Tracking
        response = await self.make_request("GET", "/admin/analytics/gemini-usage", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        self.log_test_result("analytics", "Gemini API Usage Tracking", success,
                           f"Status: {response['status_code']}, Gemini usage retrieved: {'Yes' if success else 'No'}")

        # Test 5: Get API Usage Logs
        params = {"limit": 50, "skip": 0}
        response = await self.make_request("GET", "/admin/analytics/api-logs", headers=headers, params=params)
        success = response["success"] and "logs" in response["data"]
        
        self.log_test_result("analytics", "API Usage Logs", success,
                           f"Status: {response['status_code']}, API logs retrieved: {'Yes' if success else 'No'}")

        # Test 6: Get Error Logs
        params = {"limit": 50, "skip": 0}
        response = await self.make_request("GET", "/admin/analytics/error-logs", headers=headers, params=params)
        success = response["success"] and "logs" in response["data"]
        
        self.log_test_result("analytics", "Error Logs", success,
                           f"Status: {response['status_code']}, Error logs retrieved: {'Yes' if success else 'No'}")

        # Test 7: Filter API Logs by Status Code
        params = {"limit": 20, "status_code": 200}
        response = await self.make_request("GET", "/admin/analytics/api-logs", headers=headers, params=params)
        success = response["success"] and "logs" in response["data"]
        
        self.log_test_result("analytics", "Filter API Logs by Status", success,
                           f"Status: {response['status_code']}, Filtered logs retrieved: {'Yes' if success else 'No'}")

    # =============================================================================
    # BULK OPERATIONS TESTS (Module 6) - NEW FOCUS
    # =============================================================================

    async def test_bulk_operations(self):
        """Test Bulk Import/Export Operations"""
        print("\n📦 TESTING BULK OPERATIONS (Module 6) - NEW FOCUS...")
        
        if not self.admin_token:
            self.log_test_result("bulk_operations", "Authentication Check", False,
                               "No admin token available - skipping bulk operations tests")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # First, create some test jobs for export
        job_data = {
            "title": "Senior Python Developer",
            "company": "TechCorp Inc",
            "location": "San Francisco, CA",
            "job_type": "full-time",
            "category": "technology",
            "experience_level": "senior",
            "description": "We are looking for a senior Python developer with 5+ years of experience.",
            "skills": ["Python", "Django", "PostgreSQL", "AWS"],
            "qualifications": ["Bachelor's degree in CS", "5+ years Python experience"],
            "responsibilities": ["Develop backend services", "Code reviews", "Mentor junior developers"],
            "benefits": ["Health insurance", "401k", "Remote work"],
            "salary_min": 120000,
            "salary_max": 180000
        }
        
        job_response = await self.make_request("POST", "/admin/jobs", job_data)
        job_id = job_response["data"].get("job", {}).get("id") if job_response["success"] else None
        if job_id:
            self.created_resources["jobs"].append(job_id)

        # Test 1: Export Jobs to CSV
        response = await self.make_request("GET", "/admin/bulk/jobs/export", headers=headers)
        success = response["success"] and response["status_code"] == 200
        
        self.log_test_result("bulk_operations", "Export Jobs CSV", success,
                           f"Status: {response['status_code']}, CSV export successful: {'Yes' if success else 'No'}")

        # Test 2: Import Jobs from CSV
        csv_data = """title,company,location,job_type,category,experience_level,description,salary_min,salary_max
"Data Analyst","DataCorp","New York, NY","full-time","technology","mid","Analyze data and create reports",70000,100000
"Marketing Manager","MarketingPro","Los Angeles, CA","full-time","marketing","senior","Lead marketing campaigns",80000,120000"""
        
        response = await self.make_request("POST", "/admin/bulk/jobs/import", {"csv_data": csv_data}, headers=headers)
        success = response["success"] and response["data"].get("imported_count", 0) > 0
        
        self.log_test_result("bulk_operations", "Import Jobs CSV", success,
                           f"Status: {response['status_code']}, Jobs imported: {response['data'].get('imported_count', 0) if success else 0}")

        # Test 3: Export Internships to CSV
        response = await self.make_request("GET", "/admin/bulk/internships/export", headers=headers)
        success = response["success"] and response["status_code"] == 200
        
        self.log_test_result("bulk_operations", "Export Internships CSV", success,
                           f"Status: {response['status_code']}, CSV export successful: {'Yes' if success else 'No'}")

        # Test 4: Import Internships from CSV
        internship_csv = """title,company,location,duration,category,description,stipend
"Software Engineering Intern","TechStart","Remote","3 months","technology","Learn full-stack development",2000
"Marketing Intern","BrandCorp","Chicago, IL","6 months","marketing","Support marketing campaigns",1500"""
        
        response = await self.make_request("POST", "/admin/bulk/internships/import", {"csv_data": internship_csv}, headers=headers)
        success = response["success"] and response["data"].get("imported_count", 0) > 0
        
        self.log_test_result("bulk_operations", "Import Internships CSV", success,
                           f"Status: {response['status_code']}, Internships imported: {response['data'].get('imported_count', 0) if success else 0}")

        # Test 5: Bulk Delete Jobs
        if job_id:
            response = await self.make_request("POST", "/admin/bulk/jobs/delete", {"job_ids": [job_id]}, headers=headers)
            success = response["success"] and response["data"].get("deleted_count", 0) > 0
            
            self.log_test_result("bulk_operations", "Bulk Delete Jobs", success,
                               f"Status: {response['status_code']}, Jobs deleted: {response['data'].get('deleted_count', 0) if success else 0}")

        # Test 6: Bulk Update Jobs Status
        # First get some job IDs
        jobs_response = await self.make_request("GET", "/admin/jobs", headers=headers, params={"limit": 5})
        if jobs_response["success"] and jobs_response["data"].get("jobs"):
            job_ids = [job["id"] for job in jobs_response["data"]["jobs"][:2]]
            
            response = await self.make_request("POST", "/admin/bulk/jobs/update-status", 
                                             {"job_ids": job_ids, "is_active": False}, headers=headers)
            success = response["success"] and response["data"].get("updated_count", 0) > 0
            
            self.log_test_result("bulk_operations", "Bulk Update Jobs Status", success,
                               f"Status: {response['status_code']}, Jobs updated: {response['data'].get('updated_count', 0) if success else 0}")

        # Test 7: Bulk Update Internships Status
        internships_response = await self.make_request("GET", "/admin/internships", headers=headers, params={"limit": 5})
        if internships_response["success"] and internships_response["data"].get("internships"):
            internship_ids = [internship["id"] for internship in internships_response["data"]["internships"][:2]]
            
            response = await self.make_request("POST", "/admin/bulk/internships/update-status", 
                                             {"internship_ids": internship_ids, "is_active": False}, headers=headers)
            success = response["success"] and response["data"].get("updated_count", 0) > 0
            
            self.log_test_result("bulk_operations", "Bulk Update Internships Status", success,
                               f"Status: {response['status_code']}, Internships updated: {response['data'].get('updated_count', 0) if success else 0}")

    # =============================================================================
    # CONTENT APPROVAL WORKFLOW TESTS (Module 6) - NEW FOCUS
    # =============================================================================

    async def test_content_approval_workflow(self):
        """Test Content Approval Workflow"""
        print("\n✅ TESTING CONTENT APPROVAL WORKFLOW (Module 6) - NEW FOCUS...")
        
        if not self.user_token or not self.admin_token:
            self.log_test_result("content_approval", "Authentication Check", False,
                               "Missing user or admin token - skipping content approval tests")
            return

        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        admin_headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test 1: Submit Content for Approval
        content_data = {
            "title": "How to Ace Technical Interviews",
            "content": "This article covers best practices for technical interviews...",
            "category": "career_advice",
            "tags": ["interviews", "technical", "career"]
        }
        
        response = await self.make_request("POST", "/admin/content/submit", 
                                         {"content_type": "article", "content_data": content_data}, 
                                         headers=user_headers)
        success = response["success"] and response["data"].get("submission_id")
        submission_id = response["data"].get("submission_id") if success else None
        
        if submission_id:
            self.created_resources["submissions"].append(submission_id)
        
        self.log_test_result("content_approval", "Submit Content for Approval", success,
                           f"Status: {response['status_code']}, Submission ID: {submission_id}")

        # Test 2: Get Pending Submissions
        response = await self.make_request("GET", "/admin/content/pending", headers=admin_headers)
        success = response["success"] and "submissions" in response["data"]
        pending_count = len(response["data"].get("submissions", [])) if success else 0
        
        self.log_test_result("content_approval", "Get Pending Submissions", success,
                           f"Status: {response['status_code']}, Pending submissions: {pending_count}")

        # Test 3: Filter Pending Submissions by Content Type
        params = {"content_type": "article", "limit": 10}
        response = await self.make_request("GET", "/admin/content/pending", headers=admin_headers, params=params)
        success = response["success"] and "submissions" in response["data"]
        
        self.log_test_result("content_approval", "Filter Pending by Content Type", success,
                           f"Status: {response['status_code']}, Filtered submissions retrieved: {'Yes' if success else 'No'}")

        # Test 4: Approve Submission
        if submission_id:
            response = await self.make_request("POST", f"/admin/content/{submission_id}/approve", 
                                             {"review_notes": "Great article, approved for publication"}, 
                                             headers=admin_headers)
            success = response["success"]
            
            self.log_test_result("content_approval", "Approve Submission", success,
                               f"Status: {response['status_code']}, Submission approved: {'Yes' if success else 'No'}")

        # Test 5: Submit Another Content for Rejection Test
        reject_content_data = {
            "title": "Poor Quality Article",
            "content": "This is a low quality article...",
            "category": "general",
            "tags": ["test"]
        }
        
        response = await self.make_request("POST", "/admin/content/submit", 
                                         {"content_type": "article", "content_data": reject_content_data}, 
                                         headers=user_headers)
        reject_submission_id = response["data"].get("submission_id") if response["success"] else None

        # Test 6: Reject Submission
        if reject_submission_id:
            response = await self.make_request("POST", f"/admin/content/{reject_submission_id}/reject", 
                                             {"review_notes": "Content quality does not meet our standards"}, 
                                             headers=admin_headers)
            success = response["success"]
            
            self.log_test_result("content_approval", "Reject Submission", success,
                               f"Status: {response['status_code']}, Submission rejected: {'Yes' if success else 'No'}")

        # Test 7: Get Content Approval Statistics
        response = await self.make_request("GET", "/admin/content/stats", headers=admin_headers)
        success = response["success"] and "total_submissions" in response["data"]
        
        self.log_test_result("content_approval", "Get Approval Statistics", success,
                           f"Status: {response['status_code']}, Stats retrieved: {'Yes' if success else 'No'}")

    # =============================================================================
    # PUSH NOTIFICATIONS TESTS (Module 6) - NEW FOCUS
    # =============================================================================

    async def test_push_notifications(self):
        """Test Push Notifications Management"""
        print("\n🔔 TESTING PUSH NOTIFICATIONS (Module 6) - NEW FOCUS...")
        
        if not self.admin_token:
            self.log_test_result("push_notifications", "Authentication Check", False,
                               "No admin token available - skipping push notifications tests")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test 1: Create Push Notification (All Users)
        notification_data = {
            "title": "New Job Opportunities Available!",
            "message": "Check out the latest job postings in your field.",
            "target": "all",
            "data": {"type": "job_alert", "category": "technology"}
        }
        
        response = await self.make_request("POST", "/admin/notifications", notification_data, headers=headers)
        success = response["success"] and response["data"].get("notification_id")
        notification_id = response["data"].get("notification_id") if success else None
        
        if notification_id:
            self.created_resources["notifications"].append(notification_id)
        
        self.log_test_result("push_notifications", "Create Notification (All Users)", success,
                           f"Status: {response['status_code']}, Notification ID: {notification_id}")

        # Test 2: Create Push Notification (Specific Users)
        specific_notification_data = {
            "title": "Welcome to CareerGuide!",
            "message": "Complete your profile to get personalized job recommendations.",
            "target": "specific_users",
            "target_ids": ["user1", "user2"],
            "data": {"type": "welcome", "action": "complete_profile"}
        }
        
        response = await self.make_request("POST", "/admin/notifications", specific_notification_data, headers=headers)
        success = response["success"] and response["data"].get("notification_id")
        specific_notification_id = response["data"].get("notification_id") if success else None
        
        if specific_notification_id:
            self.created_resources["notifications"].append(specific_notification_id)
        
        self.log_test_result("push_notifications", "Create Notification (Specific Users)", success,
                           f"Status: {response['status_code']}, Notification ID: {specific_notification_id}")

        # Test 3: Create Push Notification (Admins Only)
        admin_notification_data = {
            "title": "System Maintenance Scheduled",
            "message": "System maintenance is scheduled for tonight at 2 AM EST.",
            "target": "admins",
            "data": {"type": "system_alert", "priority": "high"}
        }
        
        response = await self.make_request("POST", "/admin/notifications", admin_notification_data, headers=headers)
        success = response["success"] and response["data"].get("notification_id")
        admin_notification_id = response["data"].get("notification_id") if success else None
        
        if admin_notification_id:
            self.created_resources["notifications"].append(admin_notification_id)
        
        self.log_test_result("push_notifications", "Create Notification (Admins)", success,
                           f"Status: {response['status_code']}, Notification ID: {admin_notification_id}")

        # Test 4: Get All Notifications
        response = await self.make_request("GET", "/admin/notifications", headers=headers)
        success = response["success"] and "notifications" in response["data"]
        notifications_count = len(response["data"].get("notifications", [])) if success else 0
        
        self.log_test_result("push_notifications", "Get All Notifications", success,
                           f"Status: {response['status_code']}, Notifications found: {notifications_count}")

        # Test 5: Filter Notifications by Status
        params = {"status": "pending", "limit": 20}
        response = await self.make_request("GET", "/admin/notifications", headers=headers, params=params)
        success = response["success"] and "notifications" in response["data"]
        
        self.log_test_result("push_notifications", "Filter Notifications by Status", success,
                           f"Status: {response['status_code']}, Filtered notifications retrieved: {'Yes' if success else 'No'}")

        # Test 6: Send Push Notification
        if notification_id:
            response = await self.make_request("POST", f"/admin/notifications/{notification_id}/send", headers=headers)
            success = response["success"]
            
            self.log_test_result("push_notifications", "Send Push Notification", success,
                               f"Status: {response['status_code']}, Notification sent: {'Yes' if success else 'No'}")

        # Test 7: Get Notification Statistics
        response = await self.make_request("GET", "/admin/notifications/stats", headers=headers)
        success = response["success"] and "total_notifications" in response["data"]
        
        self.log_test_result("push_notifications", "Get Notification Statistics", success,
                           f"Status: {response['status_code']}, Stats retrieved: {'Yes' if success else 'No'}")

        # Test 8: Delete Push Notification
        if specific_notification_id:
            response = await self.make_request("DELETE", f"/admin/notifications/{specific_notification_id}", headers=headers)
            success = response["success"]
            
            self.log_test_result("push_notifications", "Delete Push Notification", success,
                               f"Status: {response['status_code']}, Notification deleted: {'Yes' if success else 'No'}")

    # =============================================================================
    # MAIN TEST RUNNER
    # =============================================================================

    async def run_all_tests(self):
        """Run all backend tests for modules 1-7"""
        print("🚀 STARTING COMPREHENSIVE BACKEND TESTING - ALL 7 MODULES...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 80)
        
        await self.setup_session()
        
        try:
            # Test all modules in order
            await self.test_authentication_system()  # Module 3
            await self.test_dsa_companies_module()   # Module 1
            await self.test_roadmaps_module()        # Module 2
            await self.test_career_tools_module()    # Module 4
            
            # NEW MODULES - HEAVY FOCUS
            await self.test_analytics_dashboard()    # Module 5 - NEW
            await self.test_bulk_operations()        # Module 6 - NEW
            await self.test_content_approval_workflow()  # Module 6 - NEW
            await self.test_push_notifications()     # Module 6 - NEW
            
            # Print summary
            self.print_test_summary()
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR during testing: {str(e)}")
        finally:
            await self.cleanup_session()

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY - ALL 7 MODULES")
        print("=" * 80)
        
        total_tests = 0
        total_passed = 0
        
        module_names = {
            "authentication": "Module 3: Authentication System",
            "dsa_companies": "Module 1: DSA Companies",
            "roadmaps": "Module 2: Roadmaps (Visual Node-Based)",
            "career_tools": "Module 4: Career Tools (AI-Powered)",
            "analytics": "Module 5: Analytics Dashboard (NEW)",
            "bulk_operations": "Module 6: Bulk Operations (NEW)",
            "content_approval": "Module 6: Content Approval (NEW)",
            "push_notifications": "Module 6: Push Notifications (NEW)"
        }
        
        for module, tests in self.test_results.items():
            if not tests:
                continue
                
            module_passed = sum(1 for test in tests if test["success"])
            module_total = len(tests)
            total_tests += module_total
            total_passed += module_passed
            
            print(f"\n🔹 {module_names.get(module, module.upper())}:")
            print(f"   Passed: {module_passed}/{module_total} ({(module_passed/module_total*100):.1f}%)")
            
            # Show failed tests
            failed_tests = [test for test in tests if not test["success"]]
            if failed_tests:
                print("   ❌ Failed Tests:")
                for test in failed_tests:
                    print(f"      - {test['test']}: {test['details']}")
        
        print(f"\n🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {total_passed}")
        print(f"   Failed: {total_tests - total_passed}")
        print(f"   Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "   Success Rate: 0%")
        
        if total_passed == total_tests:
            print("\n🎉 ALL TESTS PASSED! All 7 modules are fully functional.")
        else:
            print(f"\n⚠️  {total_tests - total_passed} tests failed. Review failed tests above.")
            
        # Special focus on new modules
        new_modules = ["analytics", "bulk_operations", "content_approval", "push_notifications"]
        new_module_tests = sum(len(self.test_results.get(module, [])) for module in new_modules)
        new_module_passed = sum(sum(1 for test in self.test_results.get(module, []) if test["success"]) for module in new_modules)
        
        print(f"\n🆕 NEW MODULES (5-6) FOCUS:")
        print(f"   Tests: {new_module_passed}/{new_module_tests}")
        print(f"   Success Rate: {(new_module_passed/new_module_tests*100):.1f}%" if new_module_tests > 0 else "   Success Rate: 0%")

async def main():
    """Main test runner"""
    tester = ComprehensiveBackendTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())