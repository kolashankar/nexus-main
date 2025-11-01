#!/usr/bin/env python3
"""
Backend API Testing for CareerGuide Admin Dashboard
Testing Priority 1: Roadmaps with Reading Time Auto-Calculation
Testing Priority 2: Sub-Admin Management (Super Admin Only)  
Testing Priority 3: DSA Companies Module
"""

import asyncio
import aiohttp
import json
import uuid
from typing import Dict, Any, Optional
import time

# Backend URL from environment
BACKEND_URL = "https://dual-app-sync.preview.emergentagent.com/api"

# Super Admin Credentials
SUPER_ADMIN_EMAIL = "kolashankar113@gmail.com"
SUPER_ADMIN_PASSWORD = "Shankar@113"

class BackendTester:
    def __init__(self):
        self.session = None
        self.admin_token = None
        self.test_results = []
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def log_result(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": time.time()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    async def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{BACKEND_URL}{endpoint}"
        
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
            
        try:
            async with self.session.request(
                method, 
                url, 
                json=data if data else None,
                headers=default_headers
            ) as response:
                try:
                    response_data = await response.json()
                except:
                    response_data = await response.text()
                
                return response.status < 400, response_data, response.status
                
        except Exception as e:
            return False, str(e), 0

    async def login_super_admin(self) -> bool:
        """Login as super admin and get token"""
        print("🔐 LOGGING IN AS SUPER ADMIN...")
        
        login_data = {
            "email": SUPER_ADMIN_EMAIL,
            "password": SUPER_ADMIN_PASSWORD
        }
        
        success, response, status = await self.make_request("POST", "/auth/admin/login", login_data)
        
        if success and isinstance(response, dict) and response.get("success"):
            self.admin_token = response.get("token")
            self.log_result("Super Admin Login", True, f"Token obtained: {self.admin_token[:20]}...")
            return True
        else:
            self.log_result("Super Admin Login", False, f"Status: {status}", response)
            return False

    def get_auth_headers(self) -> Dict:
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.admin_token}"}

    # =============================================================================
    # PRIORITY 1: ROADMAP WITH READING TIME AUTO-CALCULATION
    # =============================================================================
    
    async def test_roadmap_reading_time_calculation(self):
        """Test roadmap creation with reading time auto-calculation"""
        print("📚 TESTING ROADMAP READING TIME AUTO-CALCULATION...")
        
        # Test 1: Create roadmap with nodes and verify reading_time calculation
        roadmap_data = {
            "title": "Python Backend Development Roadmap",
            "description": "Complete roadmap for learning Python backend development",
            "category": "programming",
            "subcategory": "backend",
            "difficulty_level": "intermediate",
            "estimated_duration": "3 months",
            "nodes": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Python Basics",
                    "content": "Learn Python fundamentals including variables, data types, control structures, functions, and object-oriented programming. This comprehensive introduction covers all essential concepts needed for backend development. " * 10,  # ~400 words
                    "node_type": "content",
                    "position_x": 100,
                    "position_y": 100,
                    "connections": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "title": "FastAPI Framework",
                    "content": "Master FastAPI for building high-performance APIs with automatic documentation, type hints, and async support. Learn routing, dependency injection, middleware, and authentication. " * 15,  # ~600 words
                    "node_type": "content", 
                    "position_x": 300,
                    "position_y": 200,
                    "connections": []
                }
            ]
        }
        
        success, response, status = await self.make_request(
            "POST", "/admin/roadmaps", roadmap_data, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            roadmap_id = response.get("roadmap", {}).get("id")
            reading_time = response.get("roadmap", {}).get("reading_time")
            
            # Verify reading time is calculated (should be ~5 minutes for ~1000 words at 200 words/min)
            expected_min_time = 4  # At least 4 minutes
            expected_max_time = 7  # At most 7 minutes
            
            if reading_time and expected_min_time <= reading_time <= expected_max_time:
                self.log_result(
                    "Roadmap Creation with Reading Time", 
                    True, 
                    f"Reading time calculated: {reading_time} minutes (expected: {expected_min_time}-{expected_max_time})"
                )
                
                # Test 2: Update roadmap nodes and verify reading_time recalculation
                await self.test_roadmap_update_reading_time(roadmap_id)
                
                return roadmap_id
            else:
                self.log_result(
                    "Roadmap Creation with Reading Time", 
                    False, 
                    f"Reading time {reading_time} not in expected range {expected_min_time}-{expected_max_time}",
                    response
                )
        else:
            self.log_result("Roadmap Creation with Reading Time", False, f"Status: {status}", response)
            
        return None

    async def test_roadmap_update_reading_time(self, roadmap_id: str):
        """Test roadmap update with reading time recalculation"""
        
        # Add more content to increase reading time
        update_data = {
            "nodes": [
                {
                    "id": str(uuid.uuid4()),
                    "title": "Database Integration",
                    "content": "Learn database integration with SQLAlchemy, MongoDB, and PostgreSQL. Understand ORM concepts, migrations, relationships, and query optimization for scalable applications. " * 20,  # ~800 words
                    "node_type": "content",
                    "position_x": 500,
                    "position_y": 300,
                    "connections": []
                }
            ]
        }
        
        success, response, status = await self.make_request(
            "PUT", f"/admin/roadmaps/{roadmap_id}", update_data, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            updated_reading_time = response.get("roadmap", {}).get("reading_time")
            
            # Should be higher than before (now ~1800 words = ~9 minutes)
            expected_min_time = 8
            expected_max_time = 12
            
            if updated_reading_time and expected_min_time <= updated_reading_time <= expected_max_time:
                self.log_result(
                    "Roadmap Update with Reading Time Recalculation", 
                    True, 
                    f"Updated reading time: {updated_reading_time} minutes (expected: {expected_min_time}-{expected_max_time})"
                )
            else:
                self.log_result(
                    "Roadmap Update with Reading Time Recalculation", 
                    False, 
                    f"Updated reading time {updated_reading_time} not in expected range {expected_min_time}-{expected_max_time}",
                    response
                )
        else:
            self.log_result("Roadmap Update with Reading Time Recalculation", False, f"Status: {status}", response)

    async def test_roadmap_ai_generation_reading_time(self):
        """Test AI roadmap generation with reading time calculation"""
        
        ai_prompt_data = {
            "title": "Machine Learning Engineer Career Path",
            "category": "technology",
            "subcategory": "artificial-intelligence", 
            "difficulty_level": "advanced",
            "target_audience": "Software engineers transitioning to ML",
            "focus_areas": ["Python", "TensorFlow", "Data Science", "MLOps"]
        }
        
        success, response, status = await self.make_request(
            "POST", "/admin/roadmaps/generate-ai", ai_prompt_data, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            roadmap = response.get("roadmap", {})
            reading_time = roadmap.get("reading_time")
            nodes_count = len(roadmap.get("nodes", []))
            
            # AI should generate 15-25 nodes with substantial content
            if reading_time and reading_time > 10 and nodes_count >= 10:
                self.log_result(
                    "AI Roadmap Generation with Reading Time", 
                    True, 
                    f"Generated {nodes_count} nodes with {reading_time} minutes reading time"
                )
            else:
                self.log_result(
                    "AI Roadmap Generation with Reading Time", 
                    False, 
                    f"Generated {nodes_count} nodes with {reading_time} minutes reading time (expected >10 nodes, >10 min)",
                    response
                )
        else:
            self.log_result("AI Roadmap Generation with Reading Time", False, f"Status: {status}", response)

    # =============================================================================
    # PRIORITY 2: SUB-ADMIN MANAGEMENT (SUPER ADMIN ONLY)
    # =============================================================================
    
    async def test_sub_admin_management(self):
        """Test complete sub-admin management workflow"""
        print("👥 TESTING SUB-ADMIN MANAGEMENT...")
        
        # Test 1: Create sub-admin
        sub_admin_data = {
            "name": "Test Sub Admin",
            "email": f"subadmin_{int(time.time())}@test.com",
            "password": "TestPassword123!",
            "role": "admin",
            "permissions": ["jobs", "internships", "articles"]
        }
        
        success, response, status = await self.make_request(
            "POST", "/admin/sub-admins", sub_admin_data, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            sub_admin_id = response.get("admin", {}).get("id")
            self.log_result("Create Sub-Admin", True, f"Sub-admin created with ID: {sub_admin_id}")
            
            # Test remaining sub-admin operations
            await self.test_sub_admin_operations(sub_admin_id, sub_admin_data["email"])
            
        else:
            self.log_result("Create Sub-Admin", False, f"Status: {status}", response)

    async def test_sub_admin_operations(self, sub_admin_id: str, sub_admin_email: str):
        """Test all sub-admin CRUD operations"""
        
        # Test 2: List all admins
        success, response, status = await self.make_request(
            "GET", "/admin/sub-admins", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            admins = response.get("admins", [])
            found_admin = any(admin.get("id") == sub_admin_id for admin in admins)
            self.log_result("List All Admins", found_admin, f"Found {len(admins)} admins, sub-admin present: {found_admin}")
        else:
            self.log_result("List All Admins", False, f"Status: {status}", response)

        # Test 3: Get single admin details
        success, response, status = await self.make_request(
            "GET", f"/admin/sub-admins/{sub_admin_id}", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            admin = response.get("admin", {})
            email_match = admin.get("email") == sub_admin_email
            self.log_result("Get Single Admin", email_match, f"Admin email matches: {email_match}")
        else:
            self.log_result("Get Single Admin", False, f"Status: {status}", response)

        # Test 4: Update sub-admin details
        update_data = {
            "name": "Updated Sub Admin Name",
            "permissions": ["jobs", "internships", "articles", "scholarships"]
        }
        
        success, response, status = await self.make_request(
            "PUT", f"/admin/sub-admins/{sub_admin_id}", update_data, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            self.log_result("Update Sub-Admin", True, "Sub-admin updated successfully")
        else:
            self.log_result("Update Sub-Admin", False, f"Status: {status}", response)

        # Test 5: Toggle sub-admin status
        success, response, status = await self.make_request(
            "POST", f"/admin/sub-admins/{sub_admin_id}/toggle-status", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            new_status = response.get("admin", {}).get("is_active")
            self.log_result("Toggle Sub-Admin Status", True, f"New status: {new_status}")
        else:
            self.log_result("Toggle Sub-Admin Status", False, f"Status: {status}", response)

        # Test 6: Delete sub-admin
        success, response, status = await self.make_request(
            "DELETE", f"/admin/sub-admins/{sub_admin_id}", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            self.log_result("Delete Sub-Admin", True, "Sub-admin deleted successfully")
        else:
            self.log_result("Delete Sub-Admin", False, f"Status: {status}", response)

    # =============================================================================
    # PRIORITY 3: DSA COMPANIES MODULE
    # =============================================================================
    
    async def test_dsa_companies_module(self):
        """Test complete DSA Companies CRUD operations"""
        print("🏢 TESTING DSA COMPANIES MODULE...")
        
        # Test 1: Create company
        company_data = {
            "name": "Google",
            "logo": "https://logo.clearbit.com/google.com",
            "industry": "Technology",
            "description": "Leading technology company specializing in search, cloud computing, and AI",
            "website": "https://google.com",
            "headquarters": "Mountain View, CA",
            "problem_count": 150,
            "job_count": 25,
            "is_active": True
        }
        
        success, response, status = await self.make_request(
            "POST", "/admin/dsa/companies", company_data, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            company_id = response.get("company", {}).get("id")
            self.log_result("Create DSA Company", True, f"Company created with ID: {company_id}")
            
            # Test remaining company operations
            await self.test_dsa_company_operations(company_id)
            
        else:
            self.log_result("Create DSA Company", False, f"Status: {status}", response)

    async def test_dsa_company_operations(self, company_id: str):
        """Test all DSA company operations"""
        
        # Test 2: List companies with filters
        success, response, status = await self.make_request(
            "GET", "/admin/dsa/companies?industry=Technology&limit=10", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            companies = response.get("companies", [])
            found_company = any(company.get("id") == company_id for company in companies)
            self.log_result("List Companies with Filters", found_company, f"Found {len(companies)} companies, created company present: {found_company}")
        else:
            self.log_result("List Companies with Filters", False, f"Status: {status}", response)

        # Test 3: Get company statistics
        success, response, status = await self.make_request(
            "GET", "/admin/dsa/companies/stats", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            stats = response.get("stats", {})
            total_companies = stats.get("total_companies", 0)
            self.log_result("Get Company Statistics", total_companies > 0, f"Total companies: {total_companies}")
        else:
            self.log_result("Get Company Statistics", False, f"Status: {status}", response)

        # Test 4: Get top companies
        success, response, status = await self.make_request(
            "GET", "/admin/dsa/companies/top?by=problems&limit=5", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            top_companies = response.get("companies", [])
            self.log_result("Get Top Companies", len(top_companies) > 0, f"Found {len(top_companies)} top companies")
        else:
            self.log_result("Get Top Companies", False, f"Status: {status}", response)

        # Test 5: Get single company
        success, response, status = await self.make_request(
            "GET", f"/admin/dsa/companies/{company_id}", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            company = response.get("company", {})
            name_match = company.get("name") == "Google"
            self.log_result("Get Single Company", name_match, f"Company name matches: {name_match}")
        else:
            self.log_result("Get Single Company", False, f"Status: {status}", response)

        # Test 6: Update company
        update_data = {
            "problem_count": 175,
            "job_count": 30,
            "description": "Updated description for Google - Leading AI and cloud technology company"
        }
        
        success, response, status = await self.make_request(
            "PUT", f"/admin/dsa/companies/{company_id}", update_data, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            updated_company = response.get("company", {})
            problem_count_updated = updated_company.get("problem_count") == 175
            self.log_result("Update Company", problem_count_updated, f"Problem count updated: {problem_count_updated}")
        else:
            self.log_result("Update Company", False, f"Status: {status}", response)

        # Test 7: Delete company
        success, response, status = await self.make_request(
            "DELETE", f"/admin/dsa/companies/{company_id}", None, self.get_auth_headers()
        )
        
        if success and isinstance(response, dict) and response.get("success"):
            self.log_result("Delete Company", True, "Company deleted successfully")
        else:
            self.log_result("Delete Company", False, f"Status: {status}", response)

    # =============================================================================
    # MAIN TEST RUNNER
    # =============================================================================
    
    async def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 STARTING CAREERGUIDE BACKEND API TESTING")
        print("=" * 60)
        
        # Login first
        if not await self.login_super_admin():
            print("❌ CRITICAL: Cannot proceed without super admin login")
            return
        
        print("=" * 60)
        
        # Priority 1: Roadmap Reading Time Tests
        await self.test_roadmap_reading_time_calculation()
        await self.test_roadmap_ai_generation_reading_time()
        
        print("=" * 60)
        
        # Priority 2: Sub-Admin Management Tests  
        await self.test_sub_admin_management()
        
        print("=" * 60)
        
        # Priority 3: DSA Companies Tests
        await self.test_dsa_companies_module()
        
        print("=" * 60)
        
        # Summary
        self.print_test_summary()

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
            print()
        
        print("✅ PASSED TESTS:")
        for result in self.test_results:
            if result["success"]:
                print(f"  - {result['test']}")

async def main():
    """Main test runner"""
    async with BackendTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())