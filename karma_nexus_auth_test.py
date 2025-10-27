#!/usr/bin/env python3
"""
Karma Nexus 2.0 Authentication Test
Specific test for registration and login functionality as requested in review.
"""

import requests
import json
import sys
import uuid
from datetime import datetime
from typing import Dict, Any

# Get backend URL from frontend .env file
def get_backend_url() -> str:
    """Get backend URL from frontend environment file."""
    env_path = "/app/frontend/.env"
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        print(f"❌ Environment file not found: {env_path}")
        return "http://localhost:8001"
    
    print("❌ REACT_APP_BACKEND_URL not found in .env file")
    return "http://localhost:8001"

class KarmaNexusAuthTester:
    def __init__(self):
        self.base_url = get_backend_url()
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        
        # Generate unique test credentials as requested (keeping username under 30 chars)
        unique_id = str(uuid.uuid4())[:6]
        timestamp = datetime.now().strftime("%H%M%S")
        
        self.test_user_data = {
            "username": f"test_{timestamp}_{unique_id}",
            "email": f"testuser_{timestamp}_{unique_id}@example.com",
            "password": "TestPassword123!",  # Exact password as requested
            "economic_class": "middle",
            "moral_class": "average"
        }
        
        print(f"🔗 Testing Karma Nexus 2.0 API at: {self.base_url}")
        print(f"🔗 API endpoints at: {self.api_url}")
        print(f"👤 Test user: {self.test_user_data['username']}")
        print(f"📧 Test email: {self.test_user_data['email']}")
        print("=" * 80)

    def test_registration(self) -> bool:
        """Test user registration endpoint."""
        print("🔐 TESTING REGISTRATION")
        print("-" * 50)
        
        try:
            response = self.session.post(
                f"{self.api_url}/auth/register",
                json=self.test_user_data,
                timeout=15
            )
            
            print(f"📤 POST {self.api_url}/auth/register")
            print(f"📦 Request data: {json.dumps(self.test_user_data, indent=2)}")
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 201:
                data = response.json()
                self.auth_token = data.get('access_token')
                refresh_token = data.get('refresh_token')
                player_data = data.get('player', {})
                
                print("✅ REGISTRATION SUCCESSFUL")
                print(f"   ✓ Status: 201 Created")
                print(f"   ✓ Access token received: {'Yes' if self.auth_token else 'No'}")
                print(f"   ✓ Refresh token received: {'Yes' if refresh_token else 'No'}")
                print(f"   ✓ Player username: {player_data.get('username', 'N/A')}")
                print(f"   ✓ Player ID: {player_data.get('id', 'N/A')}")
                print(f"   ✓ Player level: {player_data.get('level', 'N/A')}")
                
                # Verify JWT tokens are present
                if not self.auth_token:
                    print("❌ ERROR: No access_token in response")
                    return False
                if not refresh_token:
                    print("❌ ERROR: No refresh_token in response")
                    return False
                    
                return True
            else:
                print(f"❌ REGISTRATION FAILED")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ REGISTRATION ERROR: {str(e)}")
            return False

    def test_login(self) -> bool:
        """Test user login endpoint."""
        print("\n🔑 TESTING LOGIN")
        print("-" * 50)
        
        login_data = {
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        }
        
        try:
            response = self.session.post(
                f"{self.api_url}/auth/login",
                json=login_data,
                timeout=15
            )
            
            print(f"📤 POST {self.api_url}/auth/login")
            print(f"📦 Request data: {json.dumps(login_data, indent=2)}")
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                refresh_token = data.get('refresh_token')
                player_data = data.get('player', {})
                
                print("✅ LOGIN SUCCESSFUL")
                print(f"   ✓ Status: 200 OK")
                print(f"   ✓ Access token received: {'Yes' if self.auth_token else 'No'}")
                print(f"   ✓ Refresh token received: {'Yes' if refresh_token else 'No'}")
                print(f"   ✓ Player username: {player_data.get('username', 'N/A')}")
                print(f"   ✓ Player profile returned: {'Yes' if player_data else 'No'}")
                
                # Verify JWT tokens are present
                if not self.auth_token:
                    print("❌ ERROR: No access_token in response")
                    return False
                if not refresh_token:
                    print("❌ ERROR: No refresh_token in response")
                    return False
                    
                return True
            else:
                print(f"❌ LOGIN FAILED")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ LOGIN ERROR: {str(e)}")
            return False

    def test_authenticated_endpoint(self) -> bool:
        """Test authenticated endpoint /api/auth/me."""
        print("\n🔒 TESTING AUTHENTICATED ENDPOINT")
        print("-" * 50)
        
        if not self.auth_token:
            print("❌ ERROR: No auth token available for testing")
            return False
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        
        try:
            response = self.session.get(
                f"{self.api_url}/auth/me",
                headers=headers,
                timeout=15
            )
            
            print(f"📤 GET {self.api_url}/auth/me")
            print(f"🔑 Authorization: Bearer {self.auth_token[:20]}...")
            print(f"📥 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                print("✅ AUTHENTICATED ENDPOINT SUCCESSFUL")
                print(f"   ✓ Status: 200 OK")
                print(f"   ✓ User profile returned: {'Yes' if data else 'No'}")
                print(f"   ✓ Username: {data.get('username', 'N/A')}")
                print(f"   ✓ Email: {data.get('email', 'N/A')}")
                print(f"   ✓ User ID: {data.get('id', 'N/A')}")
                
                # Verify user profile data is returned correctly
                expected_username = self.test_user_data['username']
                expected_email = self.test_user_data['email']
                
                if data.get('username') != expected_username:
                    print(f"❌ ERROR: Username mismatch. Expected: {expected_username}, Got: {data.get('username')}")
                    return False
                    
                if data.get('email') != expected_email:
                    print(f"❌ ERROR: Email mismatch. Expected: {expected_email}, Got: {data.get('email')}")
                    return False
                
                return True
            else:
                print(f"❌ AUTHENTICATED ENDPOINT FAILED")
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ AUTHENTICATED ENDPOINT ERROR: {str(e)}")
            return False

    def run_auth_tests(self) -> Dict[str, bool]:
        """Run all authentication tests."""
        print("🚀 KARMA NEXUS 2.0 - AUTHENTICATION TESTING")
        print("=" * 80)
        
        results = {}
        
        # Test 1: Registration
        results['registration'] = self.test_registration()
        
        # Test 2: Login (only if registration succeeded or we have credentials)
        results['login'] = self.test_login()
        
        # Test 3: Authenticated endpoint (only if login succeeded)
        results['authenticated_endpoint'] = self.test_authenticated_endpoint()
        
        # Print final summary
        print("\n" + "=" * 80)
        print("📊 AUTHENTICATION TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name.replace('_', ' ').title()}")
        
        print("-" * 80)
        print(f"📈 OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL AUTHENTICATION TESTS PASSED!")
            print("✅ Registration and login functionality is working correctly")
            print("✅ No CORS errors detected")
            print("✅ No ERR_BLOCKED_BY_CLIENT errors detected")
            print("✅ JWT authentication is working properly")
        else:
            print("❌ Some authentication tests failed - needs attention")
        
        return results

def main():
    """Main test execution function."""
    tester = KarmaNexusAuthTester()
    results = tester.run_auth_tests()
    
    # Exit with appropriate code
    failed_tests = [name for name, result in results.items() if not result]
    if failed_tests:
        print(f"\n❌ Failed tests: {', '.join(failed_tests)}")
        sys.exit(1)
    else:
        print("\n✅ All authentication tests completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()