#!/usr/bin/env python3
"""
Comprehensive Backend Testing for DSA Corner Module
Tests all DSA Topics, Questions, and Sheets endpoints with AI generation
"""

import requests
import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://dual-app-sync.preview.emergentagent.com/api"

class DSABackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BACKEND_URL
        self.test_results = {
            "topics": {"passed": 0, "failed": 0, "errors": []},
            "questions": {"passed": 0, "failed": 0, "errors": []},
            "sheets": {"passed": 0, "failed": 0, "errors": []},
            "integration": {"passed": 0, "failed": 0, "errors": []},
            "ai_generation": {"passed": 0, "failed": 0, "errors": []}
        }
        self.created_resources = {
            "topics": [],
            "questions": [],
            "sheets": []
        }

    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """Make HTTP request and return response"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params)
                response_data = response.json()
                return {
                    "status": response.status_code,
                    "data": response_data,
                    "success": response.status_code < 400
                }
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, params=params)
                response_data = response.json()
                return {
                    "status": response.status_code,
                    "data": response_data,
                    "success": response.status_code < 400
                }
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data)
                response_data = response.json()
                return {
                    "status": response.status_code,
                    "data": response_data,
                    "success": response.status_code < 400
                }
            elif method.upper() == "DELETE":
                response = self.session.delete(url)
                response_data = response.json()
                return {
                    "status": response.status_code,
                    "data": response_data,
                    "success": response.status_code < 400
                }
        except Exception as e:
            return {
                "status": 500,
                "data": {"error": str(e)},
                "success": False
            }

    def log_test_result(self, category: str, test_name: str, success: bool, error_msg: str = None):
        """Log test result"""
        if success:
            self.test_results[category]["passed"] += 1
            print(f"✅ {test_name}")
        else:
            self.test_results[category]["failed"] += 1
            self.test_results[category]["errors"].append(f"{test_name}: {error_msg}")
            print(f"❌ {test_name}: {error_msg}")

    # =============================================================================
    # DSA TOPICS TESTING
    # =============================================================================

    def test_dsa_topics_crud(self):
        """Test all DSA Topics CRUD operations"""
        print("\n🔍 TESTING DSA TOPICS CRUD OPERATIONS")
        print("=" * 50)

        # Test 1: Create Topics
        topics_data = [
            {
                "name": "Arrays",
                "description": "Linear data structure storing elements in contiguous memory locations",
                "icon": "📊",
                "color": "#FF6B6B",
                "is_active": True
            },
            {
                "name": "Trees",
                "description": "Hierarchical data structure with nodes connected by edges",
                "icon": "🌳",
                "color": "#4ECDC4",
                "is_active": True
            },
            {
                "name": "Graphs",
                "description": "Non-linear data structure consisting of vertices and edges",
                "icon": "🕸️",
                "color": "#45B7D1",
                "is_active": True
            },
            {
                "name": "Dynamic Programming",
                "description": "Algorithmic paradigm solving complex problems by breaking them down",
                "icon": "⚡",
                "color": "#96CEB4",
                "is_active": True
            }
        ]

        for topic_data in topics_data:
            response = self.make_request("POST", "/admin/dsa/topics", topic_data)
            if response["success"] and "id" in response["data"]:
                self.created_resources["topics"].append(response["data"]["id"])
                self.log_test_result("topics", f"Create topic '{topic_data['name']}'", True)
            else:
                self.log_test_result("topics", f"Create topic '{topic_data['name']}'", False, 
                                   response["data"].get("detail", "Unknown error"))

        # Test 2: Get All Topics
        response = self.make_request("GET", "/admin/dsa/topics")
        if response["success"] and isinstance(response["data"], list):
            self.log_test_result("topics", "Get all topics", True)
        else:
            self.log_test_result("topics", "Get all topics", False, 
                               response["data"].get("detail", "Failed to get topics"))

        # Test 3: Get Topics with Filters
        response = self.make_request("GET", "/admin/dsa/topics", params={"is_active": True})
        if response["success"]:
            self.log_test_result("topics", "Filter topics by is_active", True)
        else:
            self.log_test_result("topics", "Filter topics by is_active", False, 
                               response["data"].get("detail", "Filter failed"))

        # Test 4: Get Topic Statistics
        response = self.make_request("GET", "/admin/dsa/topics/stats")
        if response["success"]:
            self.log_test_result("topics", "Get topic statistics", True)
        else:
            self.log_test_result("topics", "Get topic statistics", False, 
                               response["data"].get("detail", "Stats failed"))

        # Test 5: Get Single Topic
        if self.created_resources["topics"]:
            topic_id = self.created_resources["topics"][0]
            response = self.make_request("GET", f"/admin/dsa/topics/{topic_id}")
            if response["success"]:
                self.log_test_result("topics", "Get single topic", True)
            else:
                self.log_test_result("topics", "Get single topic", False, 
                                   response["data"].get("detail", "Get single failed"))

        # Test 6: Update Topic
        if self.created_resources["topics"]:
            topic_id = self.created_resources["topics"][0]
            update_data = {"description": "Updated: Linear data structure for efficient element access"}
            response = self.make_request("PUT", f"/admin/dsa/topics/{topic_id}", update_data)
            if response["success"]:
                self.log_test_result("topics", "Update topic", True)
            else:
                self.log_test_result("topics", "Update topic", False, 
                                   response["data"].get("detail", "Update failed"))

    # =============================================================================
    # DSA QUESTIONS TESTING
    # =============================================================================

    def test_dsa_questions_crud(self):
        """Test all DSA Questions CRUD operations"""
        print("\n🔍 TESTING DSA QUESTIONS CRUD OPERATIONS")
        print("=" * 50)

        # Test 1: Create Manual Question
        question_data = {
            "title": "Two Sum Problem",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "difficulty": "easy",
            "topics": self.created_resources["topics"][:2] if self.created_resources["topics"] else [],
            "companies": ["Google", "Amazon", "Microsoft"],
            "examples": [
                {
                    "input": "nums = [2,7,11,15], target = 9",
                    "output": "[0,1]",
                    "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
                }
            ],
            "solution_approach": "Use hash map to store complement values and their indices",
            "code_solutions": {
                "python": "def twoSum(nums, target):\n    hashmap = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in hashmap:\n            return [hashmap[complement], i]\n        hashmap[num] = i\n    return []",
                "javascript": "function twoSum(nums, target) {\n    const map = new Map();\n    for (let i = 0; i < nums.length; i++) {\n        const complement = target - nums[i];\n        if (map.has(complement)) {\n            return [map.get(complement), i];\n        }\n        map.set(nums[i], i);\n    }\n    return [];\n}",
                "java": "public int[] twoSum(int[] nums, int target) {\n    Map<Integer, Integer> map = new HashMap<>();\n    for (int i = 0; i < nums.length; i++) {\n        int complement = target - nums[i];\n        if (map.containsKey(complement)) {\n            return new int[] { map.get(complement), i };\n        }\n        map.put(nums[i], i);\n    }\n    return new int[]{};\n}"
            },
            "hints": ["Use a hash map", "Store complements", "Single pass solution"],
            "time_complexity": "O(n)",
            "space_complexity": "O(n)",
            "is_active": True,
            "is_premium": False
        }

        response = self.make_request("POST", "/admin/dsa/questions", question_data)
        if response["success"] and "id" in response["data"]:
            self.created_resources["questions"].append(response["data"]["id"])
            self.log_test_result("questions", "Create manual question", True)
        else:
            self.log_test_result("questions", "Create manual question", False, 
                               response["data"].get("detail", "Unknown error"))

        # Test 2: Get All Questions
        response = self.make_request("GET", "/admin/dsa/questions")
        if response["success"] and isinstance(response["data"], list):
            self.log_test_result("questions", "Get all questions", True)
        else:
            self.log_test_result("questions", "Get all questions", False, 
                               response["data"].get("detail", "Failed to get questions"))

        # Test 3: Filter Questions by Difficulty
        response = self.make_request("GET", "/admin/dsa/questions", params={"difficulty": "easy"})
        if response["success"]:
            self.log_test_result("questions", "Filter questions by difficulty", True)
        else:
            self.log_test_result("questions", "Filter questions by difficulty", False, 
                               response["data"].get("detail", "Filter failed"))

        # Test 4: Search Questions
        response = self.make_request("GET", "/admin/dsa/questions", params={"search": "Two Sum"})
        if response["success"]:
            self.log_test_result("questions", "Search questions", True)
        else:
            self.log_test_result("questions", "Search questions", False, 
                               response["data"].get("detail", "Search failed"))

        # Test 5: Get Question Statistics by Difficulty
        response = self.make_request("GET", "/admin/dsa/questions/stats/difficulty")
        if response["success"]:
            self.log_test_result("questions", "Get difficulty statistics", True)
        else:
            self.log_test_result("questions", "Get difficulty statistics", False, 
                               response["data"].get("detail", "Stats failed"))

        # Test 6: Get Question Statistics by Topic
        response = self.make_request("GET", "/admin/dsa/questions/stats/topic")
        if response["success"]:
            self.log_test_result("questions", "Get topic statistics", True)
        else:
            self.log_test_result("questions", "Get topic statistics", False, 
                               response["data"].get("detail", "Stats failed"))

        # Test 7: Get Single Question
        if self.created_resources["questions"]:
            question_id = self.created_resources["questions"][0]
            response = self.make_request("GET", f"/admin/dsa/questions/{question_id}")
            if response["success"]:
                self.log_test_result("questions", "Get single question", True)
            else:
                self.log_test_result("questions", "Get single question", False, 
                                   response["data"].get("detail", "Get single failed"))

        # Test 8: Update Question
        if self.created_resources["questions"]:
            question_id = self.created_resources["questions"][0]
            update_data = {"difficulty": "medium"}
            response = self.make_request("PUT", f"/admin/dsa/questions/{question_id}", update_data)
            if response["success"]:
                self.log_test_result("questions", "Update question", True)
            else:
                self.log_test_result("questions", "Update question", False, 
                                   response["data"].get("detail", "Update failed"))

        # Test 9: Submit Question (Record Submission)
        if self.created_resources["questions"]:
            question_id = self.created_resources["questions"][0]
            response = self.make_request("POST", f"/admin/dsa/questions/{question_id}/submit", 
                                       params={"is_accepted": True})
            if response["success"]:
                self.log_test_result("questions", "Record question submission", True)
            else:
                self.log_test_result("questions", "Record question submission", False, 
                                   response["data"].get("detail", "Submission failed"))

    # =============================================================================
    # DSA SHEETS TESTING
    # =============================================================================

    def test_dsa_sheets_crud(self):
        """Test all DSA Sheets CRUD operations"""
        print("\n🔍 TESTING DSA SHEETS CRUD OPERATIONS")
        print("=" * 50)

        # Test 1: Create Manual Sheet
        sheet_data = {
            "name": "Beginner Arrays Practice",
            "description": "Essential array problems for coding interview preparation",
            "questions": self.created_resources["questions"] if self.created_resources["questions"] else [],
            "difficulty_breakdown": {
                "easy": 5,
                "medium": 3,
                "hard": 2
            },
            "level": "beginner",
            "tags": ["arrays", "beginner", "interview-prep"],
            "is_published": False,
            "is_featured": False,
            "is_premium": False
        }

        response = self.make_request("POST", "/admin/dsa/sheets", sheet_data)
        if response["success"] and "id" in response["data"]:
            self.created_resources["sheets"].append(response["data"]["id"])
            self.log_test_result("sheets", "Create manual sheet", True)
        else:
            self.log_test_result("sheets", "Create manual sheet", False, 
                               response["data"].get("detail", "Unknown error"))

        # Test 2: Get All Sheets
        response = self.make_request("GET", "/admin/dsa/sheets")
        if response["success"] and isinstance(response["data"], list):
            self.log_test_result("sheets", "Get all sheets", True)
        else:
            self.log_test_result("sheets", "Get all sheets", False, 
                               response["data"].get("detail", "Failed to get sheets"))

        # Test 3: Filter Sheets by Level
        response = self.make_request("GET", "/admin/dsa/sheets", params={"level": "beginner"})
        if response["success"]:
            self.log_test_result("sheets", "Filter sheets by level", True)
        else:
            self.log_test_result("sheets", "Filter sheets by level", False, 
                               response["data"].get("detail", "Filter failed"))

        # Test 4: Get Sheet Statistics
        response = self.make_request("GET", "/admin/dsa/sheets/stats")
        if response["success"]:
            self.log_test_result("sheets", "Get sheet statistics", True)
        else:
            self.log_test_result("sheets", "Get sheet statistics", False, 
                               response["data"].get("detail", "Stats failed"))

        # Test 5: Get Single Sheet
        if self.created_resources["sheets"]:
            sheet_id = self.created_resources["sheets"][0]
            response = self.make_request("GET", f"/admin/dsa/sheets/{sheet_id}")
            if response["success"]:
                self.log_test_result("sheets", "Get single sheet", True)
            else:
                self.log_test_result("sheets", "Get single sheet", False, 
                                   response["data"].get("detail", "Get single failed"))

        # Test 6: Update Sheet
        if self.created_resources["sheets"]:
            sheet_id = self.created_resources["sheets"][0]
            update_data = {"description": "Updated: Comprehensive array problems for beginners"}
            response = self.make_request("PUT", f"/admin/dsa/sheets/{sheet_id}", update_data)
            if response["success"]:
                self.log_test_result("sheets", "Update sheet", True)
            else:
                self.log_test_result("sheets", "Update sheet", False, 
                                   response["data"].get("detail", "Update failed"))

        # Test 7: Add Question to Sheet
        if self.created_resources["sheets"] and self.created_resources["questions"]:
            sheet_id = self.created_resources["sheets"][0]
            question_id = self.created_resources["questions"][0]
            response = self.make_request("POST", f"/admin/dsa/sheets/{sheet_id}/questions", 
                                       params={"question_id": question_id, "order": 1})
            if response["success"]:
                self.log_test_result("sheets", "Add question to sheet", True)
            else:
                self.log_test_result("sheets", "Add question to sheet", False, 
                                   response["data"].get("detail", "Add question failed"))

        # Test 8: Toggle Publish Status
        if self.created_resources["sheets"]:
            sheet_id = self.created_resources["sheets"][0]
            response = self.make_request("POST", f"/admin/dsa/sheets/{sheet_id}/toggle-publish")
            if response["success"]:
                self.log_test_result("sheets", "Toggle publish status", True)
            else:
                self.log_test_result("sheets", "Toggle publish status", False, 
                                   response["data"].get("detail", "Toggle failed"))

        # Test 9: Remove Question from Sheet
        if self.created_resources["sheets"] and self.created_resources["questions"]:
            sheet_id = self.created_resources["sheets"][0]
            question_id = self.created_resources["questions"][0]
            response = self.make_request("DELETE", f"/admin/dsa/sheets/{sheet_id}/questions/{question_id}")
            if response["success"]:
                self.log_test_result("sheets", "Remove question from sheet", True)
            else:
                self.log_test_result("sheets", "Remove question from sheet", False, 
                                   response["data"].get("detail", "Remove question failed"))

    # =============================================================================
    # AI GENERATION TESTING
    # =============================================================================

    def test_ai_generation(self):
        """Test AI generation for questions and sheets"""
        print("\n🔍 TESTING AI GENERATION WITH GEMINI API")
        print("=" * 50)

        # Test 1: AI Generate DSA Question - Arrays
        response = self.make_request("POST", "/admin/dsa/questions/generate-ai", 
                                   params={
                                       "topic": "Arrays",
                                       "difficulty": "medium",
                                       "company": "Google"
                                   })
        if response["success"] and "id" in response["data"]:
            self.created_resources["questions"].append(response["data"]["id"])
            self.log_test_result("ai_generation", "AI generate Arrays question", True)
        else:
            self.log_test_result("ai_generation", "AI generate Arrays question", False, 
                               response["data"].get("detail", "AI generation failed"))

        # Test 2: AI Generate DSA Question - Trees
        response = self.make_request("POST", "/admin/dsa/questions/generate-ai", 
                                   params={
                                       "topic": "Trees",
                                       "difficulty": "hard",
                                       "company": "Amazon"
                                   })
        if response["success"] and "id" in response["data"]:
            self.created_resources["questions"].append(response["data"]["id"])
            self.log_test_result("ai_generation", "AI generate Trees question", True)
        else:
            self.log_test_result("ai_generation", "AI generate Trees question", False, 
                               response["data"].get("detail", "AI generation failed"))

        # Test 3: AI Generate DSA Sheet
        response = self.make_request("POST", "/admin/dsa/sheets/generate-ai", 
                                   params={
                                       "sheet_name": "FAANG Preparation",
                                       "level": "advanced",
                                       "focus_topics": "Arrays,Trees,Graphs"
                                   })
        if response["success"] and "id" in response["data"]:
            self.created_resources["sheets"].append(response["data"]["id"])
            self.log_test_result("ai_generation", "AI generate DSA sheet", True)
        else:
            self.log_test_result("ai_generation", "AI generate DSA sheet", False, 
                               response["data"].get("detail", "AI generation failed"))

    # =============================================================================
    # INTEGRATION TESTING
    # =============================================================================

    def test_integration(self):
        """Test integration between topics, questions, and sheets"""
        print("\n🔍 TESTING INTEGRATION BETWEEN MODULES")
        print("=" * 50)

        # Test 1: Verify question count updates in topics
        if self.created_resources["topics"]:
            topic_id = self.created_resources["topics"][0]
            response = self.make_request("GET", f"/admin/dsa/topics/{topic_id}")
            if response["success"] and "question_count" in response["data"]:
                self.log_test_result("integration", "Question count tracking in topics", True)
            else:
                self.log_test_result("integration", "Question count tracking in topics", False, 
                                   "Question count not found or updated")

        # Test 2: Filter questions by topic
        if self.created_resources["topics"]:
            topic_ids = ",".join(self.created_resources["topics"][:2])
            response = self.make_request("GET", "/admin/dsa/questions", 
                                       params={"topics": topic_ids})
            if response["success"]:
                self.log_test_result("integration", "Filter questions by topic", True)
            else:
                self.log_test_result("integration", "Filter questions by topic", False, 
                                   response["data"].get("detail", "Topic filtering failed"))

        # Test 3: Verify sheet difficulty breakdown calculation
        if self.created_resources["sheets"]:
            sheet_id = self.created_resources["sheets"][0]
            response = self.make_request("GET", f"/admin/dsa/sheets/{sheet_id}")
            if response["success"] and "difficulty_breakdown" in response["data"]:
                self.log_test_result("integration", "Sheet difficulty breakdown", True)
            else:
                self.log_test_result("integration", "Sheet difficulty breakdown", False, 
                                   "Difficulty breakdown not calculated")

    # =============================================================================
    # CLEANUP AND REPORTING
    # =============================================================================

    def cleanup_test_data(self):
        """Clean up created test data"""
        print("\n🧹 CLEANING UP TEST DATA")
        print("=" * 30)

        # Delete created sheets
        for sheet_id in self.created_resources["sheets"]:
            self.make_request("DELETE", f"/admin/dsa/sheets/{sheet_id}")

        # Delete created questions
        for question_id in self.created_resources["questions"]:
            self.make_request("DELETE", f"/admin/dsa/questions/{question_id}")

        # Delete created topics
        for topic_id in self.created_resources["topics"]:
            self.make_request("DELETE", f"/admin/dsa/topics/{topic_id}")

        print("✅ Test data cleanup completed")

    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("🎯 DSA CORNER MODULE - COMPREHENSIVE TEST RESULTS")
        print("=" * 60)

        total_passed = 0
        total_failed = 0

        for category, results in self.test_results.items():
            passed = results["passed"]
            failed = results["failed"]
            total_passed += passed
            total_failed += failed

            status = "✅ PASS" if failed == 0 else "❌ FAIL"
            print(f"\n{category.upper().replace('_', ' ')}: {status}")
            print(f"  Passed: {passed}")
            print(f"  Failed: {failed}")
            
            if results["errors"]:
                print("  Errors:")
                for error in results["errors"]:
                    print(f"    - {error}")

        print(f"\n🏆 OVERALL RESULTS:")
        print(f"  Total Passed: {total_passed}")
        print(f"  Total Failed: {total_failed}")
        print(f"  Success Rate: {(total_passed / (total_passed + total_failed) * 100):.1f}%")

        if total_failed == 0:
            print("\n🎉 ALL TESTS PASSED! DSA Corner module is fully functional.")
        else:
            print(f"\n⚠️  {total_failed} tests failed. Please review the errors above.")

        return total_failed == 0

def main():
    """Main test execution function"""
    print("🚀 Starting DSA Corner Module Backend Testing")
    print(f"Backend URL: {BACKEND_URL}")
    print("=" * 60)

    tester = DSABackendTester()
    
    # Run all test suites
    tester.test_dsa_topics_crud()
    tester.test_dsa_questions_crud()
    tester.test_dsa_sheets_crud()
    tester.test_ai_generation()
    tester.test_integration()
    
    # Print results
    all_passed = tester.print_summary()
    
    # Cleanup
    tester.cleanup_test_data()
    
    return all_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        sys.exit(1)