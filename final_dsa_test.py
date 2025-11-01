#!/usr/bin/env python3
"""
Final DSA Backend Testing - Including AI Generation
"""

import requests
import json

BACKEND_URL = "https://dual-app-sync.preview.emergentagent.com/api"

def test_ai_generation():
    print("🤖 Testing AI Generation Features")
    print("=" * 40)
    
    results = {"passed": 0, "failed": 0, "errors": []}
    
    def log_result(test_name, success, error=None):
        if success:
            results["passed"] += 1
            print(f"✅ {test_name}")
        else:
            results["failed"] += 1
            results["errors"].append(f"{test_name}: {error}")
            print(f"❌ {test_name}: {error}")
    
    # Test AI Question Generation
    try:
        response = requests.post(f"{BACKEND_URL}/admin/dsa/questions/generate-ai?topic=Arrays&difficulty=easy&company=Google")
        if response.status_code < 400:
            data = response.json()
            if data.get("success") and "id" in data.get("data", {}):
                question_id = data["data"]["id"]
                question_data = data["data"]
                
                # Verify the generated question has required fields
                required_fields = ["title", "description", "difficulty", "code_solutions", "examples"]
                missing_fields = [field for field in required_fields if field not in question_data]
                
                if not missing_fields:
                    log_result("AI Question Generation - Complete Structure", True)
                    
                    # Check if description is comprehensive (>200 chars)
                    if len(question_data.get("description", "")) > 200:
                        log_result("AI Question Generation - Comprehensive Description", True)
                    else:
                        log_result("AI Question Generation - Comprehensive Description", False, "Description too short")
                    
                    # Check if code solutions are provided
                    if len(question_data.get("code_solutions", [])) >= 2:
                        log_result("AI Question Generation - Multiple Code Solutions", True)
                    else:
                        log_result("AI Question Generation - Multiple Code Solutions", False, "Insufficient code solutions")
                    
                    # Clean up
                    requests.delete(f"{BACKEND_URL}/admin/dsa/questions/{question_id}")
                else:
                    log_result("AI Question Generation - Complete Structure", False, f"Missing fields: {missing_fields}")
            else:
                log_result("AI Question Generation - Complete Structure", False, "No ID in response")
        else:
            log_result("AI Question Generation - Complete Structure", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("AI Question Generation - Complete Structure", False, str(e))
    
    # Test AI Sheet Generation
    try:
        response = requests.post(f"{BACKEND_URL}/admin/dsa/sheets/generate-ai?sheet_name=AI Test Sheet&level=beginner&focus_topics=Arrays,Strings")
        if response.status_code < 400:
            data = response.json()
            if data.get("success") and "id" in data.get("data", {}):
                sheet_id = data["data"]["id"]
                sheet_data = data["data"]
                
                # Verify the generated sheet has required fields
                required_fields = ["name", "description", "questions", "difficulty_breakdown"]
                missing_fields = [field for field in required_fields if field not in sheet_data]
                
                if not missing_fields:
                    log_result("AI Sheet Generation - Complete Structure", True)
                    
                    # Check if sheet has adequate number of questions (>15)
                    if len(sheet_data.get("questions", [])) >= 15:
                        log_result("AI Sheet Generation - Adequate Questions Count", True)
                    else:
                        log_result("AI Sheet Generation - Adequate Questions Count", False, "Too few questions")
                    
                    # Check if difficulty breakdown is realistic
                    breakdown = sheet_data.get("difficulty_breakdown", {})
                    total_breakdown = sum(breakdown.values())
                    if 20 <= total_breakdown <= 30:
                        log_result("AI Sheet Generation - Realistic Difficulty Breakdown", True)
                    else:
                        log_result("AI Sheet Generation - Realistic Difficulty Breakdown", False, f"Total: {total_breakdown}")
                    
                    # Clean up
                    requests.delete(f"{BACKEND_URL}/admin/dsa/sheets/{sheet_id}")
                else:
                    log_result("AI Sheet Generation - Complete Structure", False, f"Missing fields: {missing_fields}")
            else:
                log_result("AI Sheet Generation - Complete Structure", False, "No ID in response")
        else:
            log_result("AI Sheet Generation - Complete Structure", False, f"HTTP {response.status_code}")
    except Exception as e:
        log_result("AI Sheet Generation - Complete Structure", False, str(e))
    
    return results

def main():
    print("🚀 Final DSA Corner Backend Testing")
    print("=" * 60)
    
    # Test AI Generation
    ai_results = test_ai_generation()
    
    # Print Summary
    print("\n" + "=" * 60)
    print("🎯 FINAL DSA CORNER TEST RESULTS")
    print("=" * 60)
    
    total_tests = ai_results["passed"] + ai_results["failed"]
    success_rate = (ai_results["passed"] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"AI Generation Tests: {total_tests}")
    print(f"Passed: {ai_results['passed']}")
    print(f"Failed: {ai_results['failed']}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if ai_results["errors"]:
        print("\n❌ FAILED TESTS:")
        for error in ai_results["errors"]:
            print(f"  - {error}")
    
    if ai_results["failed"] == 0:
        print("\n🎉 ALL AI GENERATION TESTS PASSED! DSA Corner module is fully functional including AI features.")
        return True
    else:
        print(f"\n⚠️  {ai_results['failed']} AI tests failed.")
        return False

if __name__ == "__main__":
    main()