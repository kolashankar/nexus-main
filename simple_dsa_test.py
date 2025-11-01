#!/usr/bin/env python3
"""
Simple DSA Backend Testing Script
"""

import requests
import json

BACKEND_URL = "https://dual-app-sync.preview.emergentagent.com/api"

def test_dsa_endpoints():
    print("🚀 Starting DSA Corner Backend Testing")
    print("=" * 60)
    
    results = {
        "passed": 0,
        "failed": 0,
        "errors": []
    }
    
    def log_result(test_name, success, error=None):
        if success:
            results["passed"] += 1
            print(f"✅ {test_name}")
        else:
            results["failed"] += 1
            results["errors"].append(f"{test_name}: {error}")
            print(f"❌ {test_name}: {error}")
    
    # Test 1: DSA Topics - Get All
    try:
        response = requests.get(f"{BACKEND_URL}/admin/dsa/topics")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and isinstance(data.get("data"), list):
                log_result("DSA Topics - Get All", True)
            else:
                log_result("DSA Topics - Get All", False, "Invalid response format")
        else:
            log_result("DSA Topics - Get All", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Topics - Get All", False, str(e))
    
    # Test 2: DSA Topics - Create New Topic
    topic_data = {
        "name": "Test Topic",
        "description": "Test description for DSA topic",
        "icon": "🧪",
        "color": "#FF0000",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/admin/dsa/topics", json=topic_data)
        if response.status_code < 400:
            data = response.json()
            if "id" in data:
                topic_id = data["id"]
                log_result("DSA Topics - Create Topic", True)
                
                # Test 3: DSA Topics - Get Single Topic
                try:
                    response = requests.get(f"{BACKEND_URL}/admin/dsa/topics/{topic_id}")
                    if response.status_code == 200:
                        log_result("DSA Topics - Get Single Topic", True)
                    else:
                        log_result("DSA Topics - Get Single Topic", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Topics - Get Single Topic", False, str(e))
                
                # Test 4: DSA Topics - Update Topic
                update_data = {"description": "Updated test description"}
                try:
                    response = requests.put(f"{BACKEND_URL}/admin/dsa/topics/{topic_id}", json=update_data)
                    if response.status_code < 400:
                        log_result("DSA Topics - Update Topic", True)
                    else:
                        log_result("DSA Topics - Update Topic", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Topics - Update Topic", False, str(e))
                
                # Test 5: DSA Topics - Delete Topic
                try:
                    response = requests.delete(f"{BACKEND_URL}/admin/dsa/topics/{topic_id}")
                    if response.status_code < 400:
                        log_result("DSA Topics - Delete Topic", True)
                    else:
                        log_result("DSA Topics - Delete Topic", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Topics - Delete Topic", False, str(e))
            else:
                log_result("DSA Topics - Create Topic", False, "No ID in response")
        else:
            log_result("DSA Topics - Create Topic", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Topics - Create Topic", False, str(e))
    
    # Test 6: DSA Topics - Statistics
    try:
        response = requests.get(f"{BACKEND_URL}/admin/dsa/topics/stats")
        if response.status_code == 200:
            log_result("DSA Topics - Statistics", True)
        else:
            log_result("DSA Topics - Statistics", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Topics - Statistics", False, str(e))
    
    # Test 7: DSA Questions - Get All
    try:
        response = requests.get(f"{BACKEND_URL}/admin/dsa/questions")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and isinstance(data.get("data"), list):
                log_result("DSA Questions - Get All", True)
            else:
                log_result("DSA Questions - Get All", False, "Invalid response format")
        else:
            log_result("DSA Questions - Get All", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Questions - Get All", False, str(e))
    
    # Test 8: DSA Questions - Create Manual Question
    question_data = {
        "title": "Test Two Sum Problem",
        "description": "Test description for two sum problem",
        "difficulty": "easy",
        "topics": [],
        "companies": ["TestCompany"],
        "examples": [{"input": "test", "output": "test", "explanation": "test"}],
        "solution_approach": "Test approach",
        "code_solutions": {"python": "def test(): pass"},
        "hints": ["Test hint"],
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "is_active": True,
        "is_premium": False
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/admin/dsa/questions", json=question_data)
        if response.status_code < 400:
            data = response.json()
            if "id" in data:
                question_id = data["id"]
                log_result("DSA Questions - Create Question", True)
                
                # Test 9: DSA Questions - Get Single Question
                try:
                    response = requests.get(f"{BACKEND_URL}/admin/dsa/questions/{question_id}")
                    if response.status_code == 200:
                        log_result("DSA Questions - Get Single Question", True)
                    else:
                        log_result("DSA Questions - Get Single Question", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Questions - Get Single Question", False, str(e))
                
                # Test 10: DSA Questions - Update Question
                update_data = {"difficulty": "medium"}
                try:
                    response = requests.put(f"{BACKEND_URL}/admin/dsa/questions/{question_id}", json=update_data)
                    if response.status_code < 400:
                        log_result("DSA Questions - Update Question", True)
                    else:
                        log_result("DSA Questions - Update Question", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Questions - Update Question", False, str(e))
                
                # Test 11: DSA Questions - Submit Question
                try:
                    response = requests.post(f"{BACKEND_URL}/admin/dsa/questions/{question_id}/submit?is_accepted=true")
                    if response.status_code < 400:
                        log_result("DSA Questions - Submit Question", True)
                    else:
                        log_result("DSA Questions - Submit Question", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Questions - Submit Question", False, str(e))
                
                # Test 12: DSA Questions - Delete Question
                try:
                    response = requests.delete(f"{BACKEND_URL}/admin/dsa/questions/{question_id}")
                    if response.status_code < 400:
                        log_result("DSA Questions - Delete Question", True)
                    else:
                        log_result("DSA Questions - Delete Question", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Questions - Delete Question", False, str(e))
            else:
                log_result("DSA Questions - Create Question", False, "No ID in response")
        else:
            log_result("DSA Questions - Create Question", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Questions - Create Question", False, str(e))
    
    # Test 13: DSA Questions - Statistics by Difficulty
    try:
        response = requests.get(f"{BACKEND_URL}/admin/dsa/questions/stats/difficulty")
        if response.status_code == 200:
            log_result("DSA Questions - Stats by Difficulty", True)
        else:
            log_result("DSA Questions - Stats by Difficulty", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Questions - Stats by Difficulty", False, str(e))
    
    # Test 14: DSA Questions - Statistics by Topic
    try:
        response = requests.get(f"{BACKEND_URL}/admin/dsa/questions/stats/topic")
        if response.status_code == 200:
            log_result("DSA Questions - Stats by Topic", True)
        else:
            log_result("DSA Questions - Stats by Topic", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Questions - Stats by Topic", False, str(e))
    
    # Test 15: DSA Sheets - Get All
    try:
        response = requests.get(f"{BACKEND_URL}/admin/dsa/sheets")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and isinstance(data.get("data"), list):
                log_result("DSA Sheets - Get All", True)
            else:
                log_result("DSA Sheets - Get All", False, "Invalid response format")
        else:
            log_result("DSA Sheets - Get All", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Sheets - Get All", False, str(e))
    
    # Test 16: DSA Sheets - Create Manual Sheet
    sheet_data = {
        "name": "Test Sheet",
        "description": "Test description for DSA sheet",
        "questions": [],
        "difficulty_breakdown": {"easy": 1, "medium": 1, "hard": 1},
        "level": "beginner",
        "tags": ["test"],
        "is_published": False,
        "is_featured": False,
        "is_premium": False
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/admin/dsa/sheets", json=sheet_data)
        if response.status_code < 400:
            data = response.json()
            if "id" in data:
                sheet_id = data["id"]
                log_result("DSA Sheets - Create Sheet", True)
                
                # Test 17: DSA Sheets - Get Single Sheet
                try:
                    response = requests.get(f"{BACKEND_URL}/admin/dsa/sheets/{sheet_id}")
                    if response.status_code == 200:
                        log_result("DSA Sheets - Get Single Sheet", True)
                    else:
                        log_result("DSA Sheets - Get Single Sheet", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Sheets - Get Single Sheet", False, str(e))
                
                # Test 18: DSA Sheets - Update Sheet
                update_data = {"description": "Updated test description"}
                try:
                    response = requests.put(f"{BACKEND_URL}/admin/dsa/sheets/{sheet_id}", json=update_data)
                    if response.status_code < 400:
                        log_result("DSA Sheets - Update Sheet", True)
                    else:
                        log_result("DSA Sheets - Update Sheet", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Sheets - Update Sheet", False, str(e))
                
                # Test 19: DSA Sheets - Toggle Publish
                try:
                    response = requests.post(f"{BACKEND_URL}/admin/dsa/sheets/{sheet_id}/toggle-publish")
                    if response.status_code < 400:
                        log_result("DSA Sheets - Toggle Publish", True)
                    else:
                        log_result("DSA Sheets - Toggle Publish", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Sheets - Toggle Publish", False, str(e))
                
                # Test 20: DSA Sheets - Delete Sheet
                try:
                    response = requests.delete(f"{BACKEND_URL}/admin/dsa/sheets/{sheet_id}")
                    if response.status_code < 400:
                        log_result("DSA Sheets - Delete Sheet", True)
                    else:
                        log_result("DSA Sheets - Delete Sheet", False, f"HTTP {response.status_code}")
                except Exception as e:
                    log_result("DSA Sheets - Delete Sheet", False, str(e))
            else:
                log_result("DSA Sheets - Create Sheet", False, "No ID in response")
        else:
            log_result("DSA Sheets - Create Sheet", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Sheets - Create Sheet", False, str(e))
    
    # Test 21: DSA Sheets - Statistics
    try:
        response = requests.get(f"{BACKEND_URL}/admin/dsa/sheets/stats")
        if response.status_code == 200:
            log_result("DSA Sheets - Statistics", True)
        else:
            log_result("DSA Sheets - Statistics", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("DSA Sheets - Statistics", False, str(e))
    
    # Test 22: AI Generation - DSA Question
    try:
        response = requests.post(f"{BACKEND_URL}/admin/dsa/questions/generate-ai?topic=Arrays&difficulty=medium&company=Google")
        if response.status_code < 400:
            data = response.json()
            if "id" in data:
                ai_question_id = data["id"]
                log_result("AI Generation - DSA Question", True)
                
                # Clean up AI generated question
                requests.delete(f"{BACKEND_URL}/admin/dsa/questions/{ai_question_id}")
            else:
                log_result("AI Generation - DSA Question", False, "No ID in response")
        else:
            log_result("AI Generation - DSA Question", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("AI Generation - DSA Question", False, str(e))
    
    # Test 23: AI Generation - DSA Sheet
    try:
        response = requests.post(f"{BACKEND_URL}/admin/dsa/sheets/generate-ai?sheet_name=Test AI Sheet&level=intermediate&focus_topics=Arrays,Trees")
        if response.status_code < 400:
            data = response.json()
            if "id" in data:
                ai_sheet_id = data["id"]
                log_result("AI Generation - DSA Sheet", True)
                
                # Clean up AI generated sheet
                requests.delete(f"{BACKEND_URL}/admin/dsa/sheets/{ai_sheet_id}")
            else:
                log_result("AI Generation - DSA Sheet", False, "No ID in response")
        else:
            log_result("AI Generation - DSA Sheet", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("AI Generation - DSA Sheet", False, str(e))
    
    # Print Summary
    print("\n" + "=" * 60)
    print("🎯 DSA CORNER MODULE - TEST RESULTS SUMMARY")
    print("=" * 60)
    
    total_tests = results["passed"] + results["failed"]
    success_rate = (results["passed"] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if results["errors"]:
        print("\n❌ FAILED TESTS:")
        for error in results["errors"]:
            print(f"  - {error}")
    
    if results["failed"] == 0:
        print("\n🎉 ALL TESTS PASSED! DSA Corner module is fully functional.")
        return True
    else:
        print(f"\n⚠️  {results['failed']} tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    test_dsa_endpoints()