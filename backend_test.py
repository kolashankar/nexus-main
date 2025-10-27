#!/usr/bin/env python3
"""
Backend API Testing Script for Karma Nexus 2.0
Tests health endpoints, auth endpoints, and protected endpoints.
"""

import requests
import json
import sys
import os
from typing import Dict, Any, Optional

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

class KarmaNexusAPITester:
    def __init__(self):
        self.base_url = get_backend_url()
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        self.test_user_data = {
            "username": "karma_tester_2024",
            "email": "karma.tester.2024@example.com", 
            "password": "SecureTestPass123!",
            "economic_class": "middle",
            "moral_class": "average"
        }
        
        print(f"🔗 Testing backend at: {self.base_url}")
        print(f"🔗 API endpoints at: {self.api_url}")
        print("=" * 60)

    def test_health_endpoints(self) -> Dict[str, bool]:
        """Test health and status endpoints."""
        results = {}
        
        print("🏥 TESTING HEALTH ENDPOINTS")
        print("-" * 40)
        
        # Test root endpoint
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint (/) - Status: {response.status_code}")
                print(f"   Response: {data}")
                results['root_endpoint'] = True
            else:
                print(f"❌ Root endpoint (/) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['root_endpoint'] = False
        except Exception as e:
            print(f"❌ Root endpoint (/) - Error: {str(e)}")
            results['root_endpoint'] = False

        # Test health endpoint
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health endpoint (/health) - Status: {response.status_code}")
                print(f"   Response: {data}")
                results['health_endpoint'] = True
            else:
                print(f"❌ Health endpoint (/health) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['health_endpoint'] = False
        except Exception as e:
            print(f"❌ Health endpoint (/health) - Error: {str(e)}")
            results['health_endpoint'] = False

        print()
        return results

    def test_auth_endpoints(self) -> Dict[str, bool]:
        """Test authentication endpoints."""
        results = {}
        
        print("🔐 TESTING AUTH ENDPOINTS")
        print("-" * 40)
        
        # Test user registration
        try:
            response = self.session.post(
                f"{self.api_url}/auth/register",
                json=self.test_user_data,
                timeout=10
            )
            
            if response.status_code == 201:
                data = response.json()
                self.auth_token = data.get('access_token')
                print(f"✅ Registration (/api/auth/register) - Status: {response.status_code}")
                print(f"   User created: {data.get('player', {}).get('username', 'Unknown')}")
                print(f"   Token received: {'Yes' if self.auth_token else 'No'}")
                results['register'] = True
            elif response.status_code == 400 and "already registered" in response.text:
                print(f"⚠️  Registration (/api/auth/register) - User already exists")
                print("   Proceeding with login test...")
                results['register'] = True  # Consider this a success for testing
            else:
                print(f"❌ Registration (/api/auth/register) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['register'] = False
        except Exception as e:
            print(f"❌ Registration (/api/auth/register) - Error: {str(e)}")
            results['register'] = False

        # Test user login
        try:
            login_data = {
                "email": self.test_user_data["email"],
                "password": self.test_user_data["password"]
            }
            
            response = self.session.post(
                f"{self.api_url}/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('access_token')
                print(f"✅ Login (/api/auth/login) - Status: {response.status_code}")
                print(f"   User: {data.get('player', {}).get('username', 'Unknown')}")
                print(f"   Token received: {'Yes' if self.auth_token else 'No'}")
                results['login'] = True
            else:
                print(f"❌ Login (/api/auth/login) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['login'] = False
        except Exception as e:
            print(f"❌ Login (/api/auth/login) - Error: {str(e)}")
            results['login'] = False

        print()
        return results

    def test_protected_endpoints(self) -> Dict[str, bool]:
        """Test protected endpoints that require authentication."""
        results = {}
        
        print("🔒 TESTING PROTECTED ENDPOINTS")
        print("-" * 40)
        
        if not self.auth_token:
            print("❌ No auth token available - skipping protected endpoint tests")
            return {'profile_endpoint': False}

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Test player profile endpoint
        try:
            response = self.session.get(
                f"{self.api_url}/player/profile",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Player Profile (/api/player/profile) - Status: {response.status_code}")
                print(f"   Username: {data.get('username', 'Unknown')}")
                print(f"   Level: {data.get('level', 'Unknown')}")
                results['profile_endpoint'] = True
            else:
                print(f"❌ Player Profile (/api/player/profile) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['profile_endpoint'] = False
        except Exception as e:
            print(f"❌ Player Profile (/api/player/profile) - Error: {str(e)}")
            results['profile_endpoint'] = False

        # Test auth/me endpoint
        try:
            response = self.session.get(
                f"{self.api_url}/auth/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Auth Me (/api/auth/me) - Status: {response.status_code}")
                print(f"   Username: {data.get('username', 'Unknown')}")
                results['auth_me'] = True
            else:
                print(f"❌ Auth Me (/api/auth/me) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['auth_me'] = False
        except Exception as e:
            print(f"❌ Auth Me (/api/auth/me) - Error: {str(e)}")
            results['auth_me'] = False

        print()
        return results

    def test_additional_endpoints(self) -> Dict[str, bool]:
        """Test additional API endpoints for completeness."""
        results = {}
        
        print("🔍 TESTING ADDITIONAL ENDPOINTS")
        print("-" * 40)
        
        if not self.auth_token:
            print("❌ No auth token available - skipping additional endpoint tests")
            return {}

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Test player currencies
        try:
            response = self.session.get(
                f"{self.api_url}/player/currencies",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Player Currencies (/api/player/currencies) - Status: {response.status_code}")
                print(f"   Currencies: {data.get('currencies', {})}")
                results['currencies'] = True
            else:
                print(f"❌ Player Currencies (/api/player/currencies) - Status: {response.status_code}")
                results['currencies'] = False
        except Exception as e:
            print(f"❌ Player Currencies (/api/player/currencies) - Error: {str(e)}")
            results['currencies'] = False

        # Test player stats
        try:
            response = self.session.get(
                f"{self.api_url}/player/stats",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Player Stats (/api/player/stats) - Status: {response.status_code}")
                results['stats'] = True
            else:
                print(f"❌ Player Stats (/api/player/stats) - Status: {response.status_code}")
                results['stats'] = False
        except Exception as e:
            print(f"❌ Player Stats (/api/player/stats) - Error: {str(e)}")
            results['stats'] = False

        print()
        return results

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all backend tests and return comprehensive results."""
        print("🚀 KARMA NEXUS 2.0 - BACKEND API TESTING")
        print("=" * 60)
        
        all_results = {}
        
        # Run test suites
        health_results = self.test_health_endpoints()
        auth_results = self.test_auth_endpoints()
        protected_results = self.test_protected_endpoints()
        additional_results = self.test_additional_endpoints()
        
        # Combine results
        all_results.update(health_results)
        all_results.update(auth_results)
        all_results.update(protected_results)
        all_results.update(additional_results)
        
        # Print summary
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in all_results.values() if result)
        total = len(all_results)
        
        for test_name, result in all_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print("-" * 60)
        print(f"📈 OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - Backend is fully operational!")
        elif passed >= total * 0.8:
            print("⚠️  Most tests passed - Minor issues detected")
        else:
            print("❌ Multiple failures detected - Backend needs attention")
        
        return all_results

def main():
    """Main test execution function."""
    tester = KarmaNexusAPITester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    failed_tests = [name for name, result in results.items() if not result]
    if failed_tests:
        print(f"\n❌ Failed tests: {', '.join(failed_tests)}")
        sys.exit(1)
    else:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()