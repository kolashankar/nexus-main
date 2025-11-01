#!/usr/bin/env python3
"""
Backend Testing for CareerGuide API - Focus on Modules 5-7
Testing scope:
1. Authentication System (Module 3) - Quick test to get tokens
2. Analytics Dashboard (Module 5) - HEAVY FOCUS
3. Advanced Features (Module 6) - HEAVY FOCUS
   - Bulk Operations
   - Content Approval Workflow
   - Push Notifications Management
4. Brief tests of existing modules 1-4 to ensure they still work
"""

import requests
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://dual-app-sync.preview.emergentagent.com/api"

class BackendTester:
    def __init__(self):
        self.admin_token = None
        self.user_token = None
        self.test_results = {
            "authentication": [],
            "analytics": [],
            "bulk_operations": [],
            "content_approval": [],
            "push_notifications": [],
            "existing_modules": []
        }
        self.created_resources = {
            "admin_users": [],
            "app_users": [],
            "jobs": [],
            "internships": [],
            "notifications": [],
            "submissions": []
        }

    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    headers: Dict = None, params: Dict = None) -> Dict:
        """Make HTTP request to backend"""
        url = f"{BACKEND_URL}{endpoint}"
        
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
            
        try:
            response = requests.request(
                method, url, 
                json=data if data else None,
                headers=default_headers,
                params=params,
                timeout=30
            )
            
            try:
                response_data = response.json() if response.text else {}
            except json.JSONDecodeError:
                response_data = {"raw_response": response.text}
            
            return {
                "status_code": response.status_code,
                "data": response_data,
                "success": 200 <= response.status_code < 300
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
    # AUTHENTICATION SYSTEM TESTS (Quick setup for tokens)
    # =============================================================================

    def test_authentication_system(self):
        """Test authentication system to get tokens"""
        print("\n🔐 TESTING AUTHENTICATION SYSTEM (Quick Setup)...")
        
        # Test 1: Admin Registration
        admin_data = {
            "email": f"admin_{uuid.uuid4().hex[:8]}@careerguide.com",
            "username": f"admin_{uuid.uuid4().hex[:8]}",
            "password": "AdminPass123!",
            "full_name": "Test Admin User"
        }
        
        response = self.make_request("POST", "/auth/admin/register", admin_data)
        success = response["success"] and response["data"].get("success", False)
        self.log_test_result("authentication", "Admin Registration", success,
                           f"Status: {response['status_code']}")
        
        if success:
            self.created_resources["admin_users"].append(admin_data["email"])

        # Test 2: Admin Login
        login_data = {"email": admin_data["email"], "password": admin_data["password"]}
        response = self.make_request("POST", "/auth/admin/login", login_data)
        success = response["success"] and "token" in response["data"]
        
        if success:
            self.admin_token = response["data"]["token"]
            
        self.log_test_result("authentication", "Admin Login", success,
                           f"Status: {response['status_code']}, Token: {'✓' if success else '✗'}")

        # Test 3: User Registration
        user_data = {
            "email": f"user_{uuid.uuid4().hex[:8]}@careerguide.com",
            "password": "UserPass123!",
            "full_name": "Test App User"
        }
        
        response = self.make_request("POST", "/auth/user/register", user_data)
        success = response["success"] and response["data"].get("success", False)
        self.log_test_result("authentication", "User Registration", success,
                           f"Status: {response['status_code']}")
        
        if success:
            self.created_resources["app_users"].append(user_data["email"])

        # Test 4: User Login
        login_data = {"email": user_data["email"], "password": user_data["password"]}
        response = self.make_request("POST", "/auth/user/login", login_data)
        success = response["success"] and "token" in response["data"]
        
        if success:
            self.user_token = response["data"]["token"]
            
        self.log_test_result("authentication", "User Login", success,
                           f"Status: {response['status_code']}, Token: {'✓' if success else '✗'}")

    # =============================================================================
    # ANALYTICS DASHBOARD TESTS (Module 5) - HEAVY FOCUS
    # =============================================================================

    def test_analytics_dashboard(self):
        """Test Analytics Dashboard endpoints - Module 5"""
        print("\n📊 TESTING ANALYTICS DASHBOARD (Module 5) - HEAVY FOCUS...")
        
        if not self.admin_token:
            self.log_test_result("analytics", "Authentication Check", False,
                               "No admin token available - skipping analytics tests")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test 1: Get Complete Dashboard Analytics
        response = self.make_request("GET", "/admin/analytics/dashboard", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        dashboard_data = response["data"].get("data", {}) if success else {}
        metrics_count = len(dashboard_data) if isinstance(dashboard_data, dict) else 0
        
        self.log_test_result("analytics", "Complete Dashboard Analytics", success,
                           f"Status: {response['status_code']}, Metrics: {metrics_count}")

        # Test 2: Get User Engagement Metrics
        response = self.make_request("GET", "/admin/analytics/user-engagement", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        engagement_data = response["data"].get("data", {}) if success else {}
        has_engagement_metrics = bool(engagement_data.get("total_users") is not None or 
                                    engagement_data.get("active_users") is not None)
        
        self.log_test_result("analytics", "User Engagement Metrics", success,
                           f"Status: {response['status_code']}, Has metrics: {'Yes' if has_engagement_metrics else 'No'}")

        # Test 3: Get Job Application Statistics
        response = self.make_request("GET", "/admin/analytics/job-applications", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        job_stats = response["data"].get("data", {}) if success else {}
        has_job_stats = bool(job_stats.get("total_applications") is not None or 
                           job_stats.get("applications_today") is not None)
        
        self.log_test_result("analytics", "Job Application Statistics", success,
                           f"Status: {response['status_code']}, Has stats: {'Yes' if has_job_stats else 'No'}")

        # Test 4: Get Gemini API Usage Tracking
        response = self.make_request("GET", "/admin/analytics/gemini-usage", headers=headers)
        success = response["success"] and "data" in response["data"]
        
        gemini_stats = response["data"].get("data", {}) if success else {}
        has_gemini_stats = bool(gemini_stats.get("total_requests") is not None or 
                              gemini_stats.get("requests_today") is not None)
        
        self.log_test_result("analytics", "Gemini API Usage Tracking", success,
                           f"Status: {response['status_code']}, Has usage data: {'Yes' if has_gemini_stats else 'No'}")

        # Test 5: Get API Usage Logs
        params = {"limit": 50, "skip": 0}
        response = self.make_request("GET", "/admin/analytics/api-logs", headers=headers, params=params)
        success = response["success"] and "logs" in response["data"]
        
        logs_count = len(response["data"].get("logs", [])) if success else 0
        
        self.log_test_result("analytics", "API Usage Logs", success,
                           f"Status: {response['status_code']}, Logs retrieved: {logs_count}")

        # Test 6: Get Error Logs
        params = {"limit": 50, "skip": 0}
        response = self.make_request("GET", "/admin/analytics/error-logs", headers=headers, params=params)
        success = response["success"] and "logs" in response["data"]
        
        error_logs_count = len(response["data"].get("logs", [])) if success else 0
        
        self.log_test_result("analytics", "Error Logs", success,
                           f"Status: {response['status_code']}, Error logs: {error_logs_count}")

        # Test 7: Filter API Logs by Status Code
        params = {"limit": 20, "status_code": 200}
        response = self.make_request("GET", "/admin/analytics/api-logs", headers=headers, params=params)
        success = response["success"] and "logs" in response["data"]
        
        filtered_logs_count = len(response["data"].get("logs", [])) if success else 0
        
        self.log_test_result("analytics", "Filter API Logs by Status", success,
                           f"Status: {response['status_code']}, Filtered logs: {filtered_logs_count}")

    # =============================================================================
    # BULK OPERATIONS TESTS (Module 6) - HEAVY FOCUS
    # =============================================================================

    def test_bulk_operations(self):
        """Test Bulk Import/Export Operations - Module 6"""
        print("\n📦 TESTING BULK OPERATIONS (Module 6) - HEAVY FOCUS...")
        
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
        
        job_response = self.make_request("POST", "/admin/jobs", job_data)
        job_id = job_response["data"].get("job", {}).get("id") if job_response["success"] else None
        if job_id:
            self.created_resources["jobs"].append(job_id)

        # Test 1: Export Jobs to CSV
        response = self.make_request("GET", "/admin/bulk/jobs/export", headers=headers)
        success = response["success"] and response["status_code"] == 200
        
        # Check if response contains CSV-like data
        has_csv_data = False
        if success and "data" in response["data"]:
            csv_content = str(response["data"])
            has_csv_data = "title" in csv_content.lower() or "company" in csv_content.lower()
        
        self.log_test_result("bulk_operations", "Export Jobs CSV", success,
                           f"Status: {response['status_code']}, CSV data: {'Yes' if has_csv_data else 'No'}")

        # Test 2: Import Jobs from CSV
        csv_data = """title,company,location,job_type,category,experience_level,description,salary_min,salary_max
"Data Analyst","DataCorp","New York, NY","full-time","technology","mid","Analyze data and create reports",70000,100000
"Marketing Manager","MarketingPro","Los Angeles, CA","full-time","marketing","senior","Lead marketing campaigns",80000,120000"""
        
        response = self.make_request("POST", "/admin/bulk/jobs/import", {"csv_data": csv_data}, headers=headers)
        success = response["success"] and response["data"].get("imported_count", 0) > 0
        imported_count = response["data"].get("imported_count", 0) if success else 0
        
        self.log_test_result("bulk_operations", "Import Jobs CSV", success,
                           f"Status: {response['status_code']}, Imported: {imported_count}")

        # Test 3: Export Internships to CSV
        response = self.make_request("GET", "/admin/bulk/internships/export", headers=headers)
        success = response["success"] and response["status_code"] == 200
        
        self.log_test_result("bulk_operations", "Export Internships CSV", success,
                           f"Status: {response['status_code']}, Export successful: {'Yes' if success else 'No'}")

        # Test 4: Import Internships from CSV
        internship_csv = """title,company,location,duration,category,description,stipend
"Software Engineering Intern","TechStart","Remote","3 months","technology","Learn full-stack development",2000
"Marketing Intern","BrandCorp","Chicago, IL","6 months","marketing","Support marketing campaigns",1500"""
        
        response = self.make_request("POST", "/admin/bulk/internships/import", {"csv_data": internship_csv}, headers=headers)
        success = response["success"] and response["data"].get("imported_count", 0) > 0
        internship_imported = response["data"].get("imported_count", 0) if success else 0
        
        self.log_test_result("bulk_operations", "Import Internships CSV", success,
                           f"Status: {response['status_code']}, Imported: {internship_imported}")

        # Test 5: Bulk Delete Jobs
        if job_id:
            response = self.make_request("POST", "/admin/bulk/jobs/delete", [job_id], headers=headers)
            success = response["success"] and response["data"].get("deleted_count", 0) > 0
            deleted_count = response["data"].get("deleted_count", 0) if success else 0
            
            self.log_test_result("bulk_operations", "Bulk Delete Jobs", success,
                               f"Status: {response['status_code']}, Deleted: {deleted_count}")

        # Test 6: Bulk Update Jobs Status
        # First get some job IDs
        jobs_response = self.make_request("GET", "/admin/jobs", headers=headers, params={"limit": 5})
        if jobs_response["success"] and jobs_response["data"].get("jobs"):
            job_ids = [job["id"] for job in jobs_response["data"]["jobs"][:2]]
            
            response = self.make_request("POST", "/admin/bulk/jobs/update-status", 
                                       {"job_ids": job_ids, "is_active": False}, headers=headers)
            success = response["success"] and response["data"].get("updated_count", 0) >= 0
            updated_count = response["data"].get("updated_count", 0) if success else 0
            
            self.log_test_result("bulk_operations", "Bulk Update Jobs Status", success,
                               f"Status: {response['status_code']}, Updated: {updated_count}")

        # Test 7: Bulk Update Internships Status
        internships_response = self.make_request("GET", "/admin/internships", headers=headers, params={"limit": 5})
        if internships_response["success"] and internships_response["data"].get("internships"):
            internship_ids = [internship["id"] for internship in internships_response["data"]["internships"][:2]]
            
            response = self.make_request("POST", "/admin/bulk/internships/update-status", 
                                       {"internship_ids": internship_ids, "is_active": False}, headers=headers)
            success = response["success"] and response["data"].get("updated_count", 0) >= 0
            internship_updated = response["data"].get("updated_count", 0) if success else 0
            
            self.log_test_result("bulk_operations", "Bulk Update Internships Status", success,
                               f"Status: {response['status_code']}, Updated: {internship_updated}")

    # =============================================================================
    # CONTENT APPROVAL WORKFLOW TESTS (Module 6) - HEAVY FOCUS
    # =============================================================================

    def test_content_approval_workflow(self):
        """Test Content Approval Workflow - Module 6"""
        print("\n✅ TESTING CONTENT APPROVAL WORKFLOW (Module 6) - HEAVY FOCUS...")
        
        if not self.user_token or not self.admin_token:
            self.log_test_result("content_approval", "Authentication Check", False,
                               "Missing user or admin token - skipping content approval tests")
            return

        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        admin_headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test 1: Submit Content for Approval
        content_data = {
            "title": "How to Ace Technical Interviews in 2025",
            "content": "This comprehensive article covers best practices for technical interviews, including coding challenges, system design, and behavioral questions...",
            "category": "career_advice",
            "tags": ["interviews", "technical", "career", "2025"]
        }
        
        response = self.make_request("POST", "/admin/content/submit", 
                                   {"content_type": "article", "content_data": content_data}, 
                                   headers=user_headers)
        success = response["success"] and response["data"].get("submission_id")
        submission_id = response["data"].get("submission_id") if success else None
        
        if submission_id:
            self.created_resources["submissions"].append(submission_id)
        
        self.log_test_result("content_approval", "Submit Content for Approval", success,
                           f"Status: {response['status_code']}, Submission ID: {submission_id}")

        # Test 2: Get Pending Submissions
        response = self.make_request("GET", "/admin/content/pending", headers=admin_headers)
        success = response["success"] and "submissions" in response["data"]
        pending_count = len(response["data"].get("submissions", [])) if success else 0
        
        self.log_test_result("content_approval", "Get Pending Submissions", success,
                           f"Status: {response['status_code']}, Pending: {pending_count}")

        # Test 3: Filter Pending Submissions by Content Type
        params = {"content_type": "article", "limit": 10}
        response = self.make_request("GET", "/admin/content/pending", headers=admin_headers, params=params)
        success = response["success"] and "submissions" in response["data"]
        filtered_count = len(response["data"].get("submissions", [])) if success else 0
        
        self.log_test_result("content_approval", "Filter Pending by Content Type", success,
                           f"Status: {response['status_code']}, Filtered: {filtered_count}")

        # Test 4: Approve Submission
        if submission_id:
            response = self.make_request("POST", f"/admin/content/{submission_id}/approve", 
                                       {"review_notes": "Excellent article, approved for publication"}, 
                                       headers=admin_headers)
            success = response["success"]
            
            self.log_test_result("content_approval", "Approve Submission", success,
                               f"Status: {response['status_code']}, Approved: {'Yes' if success else 'No'}")

        # Test 5: Submit Another Content for Rejection Test
        reject_content_data = {
            "title": "Low Quality Test Article",
            "content": "This is a test article with minimal content for rejection testing...",
            "category": "general",
            "tags": ["test"]
        }
        
        response = self.make_request("POST", "/admin/content/submit", 
                                   {"content_type": "article", "content_data": reject_content_data}, 
                                   headers=user_headers)
        reject_submission_id = response["data"].get("submission_id") if response["success"] else None

        # Test 6: Reject Submission
        if reject_submission_id:
            response = self.make_request("POST", f"/admin/content/{reject_submission_id}/reject", 
                                       {"review_notes": "Content quality does not meet our publication standards"}, 
                                       headers=admin_headers)
            success = response["success"]
            
            self.log_test_result("content_approval", "Reject Submission", success,
                               f"Status: {response['status_code']}, Rejected: {'Yes' if success else 'No'}")

        # Test 7: Get Content Approval Statistics
        response = self.make_request("GET", "/admin/content/stats", headers=admin_headers)
        success = response["success"] and "total_submissions" in response["data"]
        
        stats_data = response["data"] if success else {}
        total_submissions = stats_data.get("total_submissions", 0)
        
        self.log_test_result("content_approval", "Get Approval Statistics", success,
                           f"Status: {response['status_code']}, Total submissions: {total_submissions}")

    # =============================================================================
    # PUSH NOTIFICATIONS TESTS (Module 6) - HEAVY FOCUS
    # =============================================================================

    def test_push_notifications(self):
        """Test Push Notifications Management - Module 6"""
        print("\n🔔 TESTING PUSH NOTIFICATIONS (Module 6) - HEAVY FOCUS...")
        
        if not self.admin_token:
            self.log_test_result("push_notifications", "Authentication Check", False,
                               "No admin token available - skipping push notifications tests")
            return

        headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Test 1: Create Push Notification (All Users)
        notification_data = {
            "title": "New Job Opportunities Available!",
            "message": "Check out the latest job postings in your field. Apply now!",
            "target": "all",
            "data": {"type": "job_alert", "category": "technology"}
        }
        
        response = self.make_request("POST", "/admin/notifications", notification_data, headers=headers)
        success = response["success"] and response["data"].get("notification_id")
        notification_id = response["data"].get("notification_id") if success else None
        
        if notification_id:
            self.created_resources["notifications"].append(notification_id)
        
        self.log_test_result("push_notifications", "Create Notification (All Users)", success,
                           f"Status: {response['status_code']}, ID: {notification_id}")

        # Test 2: Create Push Notification (Specific Users)
        specific_notification_data = {
            "title": "Welcome to CareerGuide!",
            "message": "Complete your profile to get personalized job recommendations.",
            "target": "specific_users",
            "target_ids": ["user1", "user2"],
            "data": {"type": "welcome", "action": "complete_profile"}
        }
        
        response = self.make_request("POST", "/admin/notifications", specific_notification_data, headers=headers)
        success = response["success"] and response["data"].get("notification_id")
        specific_notification_id = response["data"].get("notification_id") if success else None
        
        if specific_notification_id:
            self.created_resources["notifications"].append(specific_notification_id)
        
        self.log_test_result("push_notifications", "Create Notification (Specific Users)", success,
                           f"Status: {response['status_code']}, ID: {specific_notification_id}")

        # Test 3: Create Push Notification (Admins Only)
        admin_notification_data = {
            "title": "System Maintenance Scheduled",
            "message": "System maintenance is scheduled for tonight at 2 AM EST.",
            "target": "admins",
            "data": {"type": "system_alert", "priority": "high"}
        }
        
        response = self.make_request("POST", "/admin/notifications", admin_notification_data, headers=headers)
        success = response["success"] and response["data"].get("notification_id")
        admin_notification_id = response["data"].get("notification_id") if success else None
        
        if admin_notification_id:
            self.created_resources["notifications"].append(admin_notification_id)
        
        self.log_test_result("push_notifications", "Create Notification (Admins)", success,
                           f"Status: {response['status_code']}, ID: {admin_notification_id}")

        # Test 4: Get All Notifications
        response = self.make_request("GET", "/admin/notifications", headers=headers)
        success = response["success"] and "notifications" in response["data"]
        notifications_count = len(response["data"].get("notifications", [])) if success else 0
        
        self.log_test_result("push_notifications", "Get All Notifications", success,
                           f"Status: {response['status_code']}, Count: {notifications_count}")

        # Test 5: Filter Notifications by Status
        params = {"status": "pending", "limit": 20}
        response = self.make_request("GET", "/admin/notifications", headers=headers, params=params)
        success = response["success"] and "notifications" in response["data"]
        pending_notifications = len(response["data"].get("notifications", [])) if success else 0
        
        self.log_test_result("push_notifications", "Filter Notifications by Status", success,
                           f"Status: {response['status_code']}, Pending: {pending_notifications}")

        # Test 6: Send Push Notification
        if notification_id:
            response = self.make_request("POST", f"/admin/notifications/{notification_id}/send", headers=headers)
            success = response["success"]
            
            self.log_test_result("push_notifications", "Send Push Notification", success,
                               f"Status: {response['status_code']}, Sent: {'Yes' if success else 'No'}")

        # Test 7: Get Notification Statistics
        response = self.make_request("GET", "/admin/notifications/stats", headers=headers)
        success = response["success"] and "total_notifications" in response["data"]
        
        stats_data = response["data"] if success else {}
        total_notifications = stats_data.get("total_notifications", 0)
        
        self.log_test_result("push_notifications", "Get Notification Statistics", success,
                           f"Status: {response['status_code']}, Total: {total_notifications}")

        # Test 8: Delete Push Notification
        if specific_notification_id:
            response = self.make_request("DELETE", f"/admin/notifications/{specific_notification_id}", headers=headers)
            success = response["success"]
            
            self.log_test_result("push_notifications", "Delete Push Notification", success,
                               f"Status: {response['status_code']}, Deleted: {'Yes' if success else 'No'}")

    # =============================================================================
    # EXISTING MODULES QUICK TESTS (Modules 1-4)
    # =============================================================================

    def test_existing_modules_quick(self):
        """Quick tests of existing modules to ensure they still work"""
        print("\n🔄 TESTING EXISTING MODULES (Quick Verification)...")
        
        # Test DSA Companies
        response = self.make_request("GET", "/admin/dsa/companies")
        success = response["success"] and "companies" in response["data"]
        self.log_test_result("existing_modules", "DSA Companies List", success,
                           f"Status: {response['status_code']}")

        # Test Roadmaps
        response = self.make_request("GET", "/admin/roadmaps")
        success = response["success"] and "roadmaps" in response["data"]
        self.log_test_result("existing_modules", "Roadmaps List", success,
                           f"Status: {response['status_code']}")

        # Test Career Tools (if user token available)
        if self.user_token:
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = self.make_request("GET", "/career-tools/my-usage", headers=headers)
            success = response["success"] and "usage_history" in response["data"]
            self.log_test_result("existing_modules", "Career Tools Usage", success,
                               f"Status: {response['status_code']}")

        # Test Jobs API
        response = self.make_request("GET", "/admin/jobs")
        success = response["success"] and "jobs" in response["data"]
        self.log_test_result("existing_modules", "Jobs List", success,
                           f"Status: {response['status_code']}")

    # =============================================================================
    # MAIN TEST RUNNER
    # =============================================================================

    def run_all_tests(self):
        """Run all backend tests focusing on modules 5-7"""
        print("🚀 STARTING COMPREHENSIVE BACKEND TESTING - FOCUS ON MODULES 5-7...")
        print(f"Backend URL: {BACKEND_URL}")
        print("=" * 80)
        
        try:
            # Setup authentication first
            self.test_authentication_system()
            
            # Quick test of existing modules
            self.test_existing_modules_quick()
            
            # HEAVY FOCUS ON NEW MODULES 5-6
            self.test_analytics_dashboard()      # Module 5 - NEW
            self.test_bulk_operations()          # Module 6 - NEW
            self.test_content_approval_workflow() # Module 6 - NEW
            self.test_push_notifications()       # Module 6 - NEW
            
            # Print summary
            self.print_test_summary()
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR during testing: {str(e)}")

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY - MODULES 5-7 FOCUS")
        print("=" * 80)
        
        total_tests = 0
        total_passed = 0
        
        module_names = {
            "authentication": "Module 3: Authentication System (Setup)",
            "existing_modules": "Modules 1-4: Existing Features (Quick Check)",
            "analytics": "Module 5: Analytics Dashboard (NEW - FOCUS)",
            "bulk_operations": "Module 6: Bulk Operations (NEW - FOCUS)",
            "content_approval": "Module 6: Content Approval (NEW - FOCUS)",
            "push_notifications": "Module 6: Push Notifications (NEW - FOCUS)"
        }
        
        failed_tests_summary = []
        
        for module, tests in self.test_results.items():
            if not tests:
                continue
                
            module_passed = sum(1 for test in tests if test["success"])
            module_total = len(tests)
            total_tests += module_total
            total_passed += module_passed
            
            status_icon = "✅" if module_passed == module_total else "❌" if module_passed == 0 else "⚠️"
            
            print(f"\n{status_icon} {module_names.get(module, module.upper())}:")
            print(f"   Passed: {module_passed}/{module_total} ({(module_passed/module_total*100):.1f}%)")
            
            # Collect failed tests
            failed_tests = [test for test in tests if not test["success"]]
            if failed_tests:
                for test in failed_tests:
                    failed_tests_summary.append(f"{module}: {test['test']} - {test['details']}")
        
        print(f"\n🎯 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {total_passed}")
        print(f"   Failed: {total_tests - total_passed}")
        print(f"   Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "   Success Rate: 0%")
        
        # Special focus on new modules
        new_modules = ["analytics", "bulk_operations", "content_approval", "push_notifications"]
        new_module_tests = sum(len(self.test_results.get(module, [])) for module in new_modules)
        new_module_passed = sum(sum(1 for test in self.test_results.get(module, []) if test["success"]) for module in new_modules)
        
        print(f"\n🆕 NEW MODULES (5-6) FOCUS RESULTS:")
        print(f"   Tests: {new_module_passed}/{new_module_tests}")
        print(f"   Success Rate: {(new_module_passed/new_module_tests*100):.1f}%" if new_module_tests > 0 else "   Success Rate: 0%")
        
        if total_passed == total_tests:
            print("\n🎉 ALL TESTS PASSED! All modules are fully functional.")
        else:
            print(f"\n⚠️  {total_tests - total_passed} tests failed.")
            if failed_tests_summary:
                print("\n❌ FAILED TESTS SUMMARY:")
                for failed_test in failed_tests_summary:
                    print(f"   - {failed_test}")

def main():
    """Main test runner"""
    tester = BackendTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()