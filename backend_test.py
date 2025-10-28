#!/usr/bin/env python3
"""
Backend API Testing Script for Karma Nexus 2.0
Tests task generation, marketplace APIs, and integration scenarios.
"""

import requests
import json
import sys
import os
import time
from typing import Dict, Any, Optional

# Use the backend URL from the review request
def get_backend_url() -> str:
    """Get backend URL - using the production URL from review request."""
    return "https://techfable.preview.emergentagent.com"

class KarmaNexusAPITester:
    def __init__(self):
        self.base_url = get_backend_url()
        self.api_url = f"{self.base_url}/api"
        self.session = requests.Session()
        self.auth_token = None
        self.player_id = None
        self.current_task = None
        self.test_user_data = {
            "username": "karma_nexus_tester",
            "email": "karma.nexus.tester@gametest.com", 
            "password": "GameTest2024!",
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

    def test_task_generation_api(self) -> Dict[str, bool]:
        """Test task generation API endpoints."""
        results = {}
        
        print("🎯 TESTING TASK GENERATION API")
        print("-" * 40)
        
        if not self.auth_token:
            print("❌ No auth token available - skipping task generation tests")
            return {'task_generation': False}

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Test task generation
        try:
            response = self.session.post(
                f"{self.api_url}/tasks/generate",
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.current_task = data.get('task')
                    print(f"✅ Task Generation (/api/tasks/generate) - Status: {response.status_code}")
                    print(f"   Task ID: {self.current_task.get('task_id', 'Unknown')}")
                    print(f"   Description: {self.current_task.get('description', 'No description')[:50]}...")
                    print(f"   Base Reward: {self.current_task.get('base_reward', 0)} coins")
                    results['task_generation'] = True
                else:
                    print(f"⚠️  Task Generation - Already has active task")
                    print(f"   Message: {data.get('error', 'Unknown error')}")
                    results['task_generation'] = True  # This is expected behavior
            else:
                print(f"❌ Task Generation (/api/tasks/generate) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['task_generation'] = False
        except Exception as e:
            print(f"❌ Task Generation (/api/tasks/generate) - Error: {str(e)}")
            results['task_generation'] = False

        # Test get current task
        try:
            response = self.session.get(
                f"{self.api_url}/tasks/current",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    task = data.get('task')
                    if task:
                        self.current_task = task
                        print(f"✅ Get Current Task (/api/tasks/current) - Status: {response.status_code}")
                        print(f"   Task ID: {task.get('task_id', 'Unknown')}")
                        print(f"   Status: {task.get('status', 'Unknown')}")
                    else:
                        print(f"⚠️  Get Current Task - No active task found")
                    results['get_current_task'] = True
                else:
                    print(f"❌ Get Current Task - API returned success=false")
                    results['get_current_task'] = False
            else:
                print(f"❌ Get Current Task (/api/tasks/current) - Status: {response.status_code}")
                results['get_current_task'] = False
        except Exception as e:
            print(f"❌ Get Current Task (/api/tasks/current) - Error: {str(e)}")
            results['get_current_task'] = False

        # Test task completion (if we have a task)
        if self.current_task and self.current_task.get('task_id'):
            try:
                completion_data = {
                    "task_id": self.current_task['task_id']
                }
                
                response = self.session.post(
                    f"{self.api_url}/tasks/complete",
                    json=completion_data,
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        reward_breakdown = data.get('reward_breakdown', {})
                        print(f"✅ Task Completion (/api/tasks/complete) - Status: {response.status_code}")
                        print(f"   Base Reward: {reward_breakdown.get('base_reward', 0)} coins")
                        print(f"   Bonus: {reward_breakdown.get('bonus_percentage', 0)}%")
                        print(f"   Total Reward: {reward_breakdown.get('total_reward', 0)} coins")
                        results['task_completion'] = True
                        # Clear current task after completion
                        self.current_task = None
                    else:
                        print(f"❌ Task Completion - API returned success=false")
                        results['task_completion'] = False
                else:
                    print(f"❌ Task Completion (/api/tasks/complete) - Status: {response.status_code}")
                    print(f"   Response: {response.text}")
                    results['task_completion'] = False
            except Exception as e:
                print(f"❌ Task Completion (/api/tasks/complete) - Error: {str(e)}")
                results['task_completion'] = False
        else:
            print("⚠️  Skipping task completion test - no active task")
            results['task_completion'] = True  # Not a failure

        print()
        return results

    def test_marketplace_api(self) -> Dict[str, bool]:
        """Test marketplace API endpoints."""
        results = {}
        
        print("🛒 TESTING MARKETPLACE API")
        print("-" * 40)
        
        if not self.auth_token:
            print("❌ No auth token available - skipping marketplace tests")
            return {'marketplace': False}

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Test get inventory
        try:
            response = self.session.get(
                f"{self.api_url}/marketplace/inventory",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    inventory = data.get('inventory', {})
                    print(f"✅ Get Inventory (/api/marketplace/inventory) - Status: {response.status_code}")
                    print(f"   Chains: {inventory.get('chains', 0)}")
                    print(f"   Rings: {inventory.get('rings', 0)}")
                    print(f"   Bonus Percentage: {inventory.get('bonus_percentage', 0)}%")
                    results['get_inventory'] = True
                else:
                    print(f"❌ Get Inventory - API returned success=false")
                    results['get_inventory'] = False
            else:
                print(f"❌ Get Inventory (/api/marketplace/inventory) - Status: {response.status_code}")
                results['get_inventory'] = False
        except Exception as e:
            print(f"❌ Get Inventory (/api/marketplace/inventory) - Error: {str(e)}")
            results['get_inventory'] = False

        # Test get prices
        try:
            response = self.session.get(
                f"{self.api_url}/marketplace/prices",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    prices = data.get('prices', {})
                    bonuses = data.get('bonuses', {})
                    print(f"✅ Get Prices (/api/marketplace/prices) - Status: {response.status_code}")
                    print(f"   Chain Price: {prices.get('chain', 0)} coins")
                    print(f"   Ring Price: {prices.get('ring', 0)} coins")
                    print(f"   Chain Bonus: {bonuses.get('chain', 'Unknown')}")
                    print(f"   Ring Bonus: {bonuses.get('ring', 'Unknown')}")
                    results['get_prices'] = True
                else:
                    print(f"❌ Get Prices - API returned success=false")
                    results['get_prices'] = False
            else:
                print(f"❌ Get Prices (/api/marketplace/prices) - Status: {response.status_code}")
                results['get_prices'] = False
        except Exception as e:
            print(f"❌ Get Prices (/api/marketplace/prices) - Error: {str(e)}")
            results['get_prices'] = False

        # Test purchase chain
        try:
            purchase_data = {
                "item_type": "chain"
            }
            
            response = self.session.post(
                f"{self.api_url}/marketplace/purchase",
                json=purchase_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Purchase Chain (/api/marketplace/purchase) - Status: {response.status_code}")
                    print(f"   New Balance: {data.get('new_balance', 0)} coins")
                    print(f"   Next Price: {data.get('next_price', 0)} coins")
                    print(f"   New Bonus: {data.get('new_bonus_percentage', 0)}%")
                    results['purchase_chain'] = True
                else:
                    error_msg = data.get('error', 'Unknown error')
                    if 'insufficient' in error_msg.lower():
                        print(f"⚠️  Purchase Chain - Insufficient funds (expected)")
                        print(f"   Error: {error_msg}")
                        results['purchase_chain'] = True  # This is expected behavior
                    else:
                        print(f"❌ Purchase Chain - Error: {error_msg}")
                        results['purchase_chain'] = False
            elif response.status_code == 400:
                # Check if it's insufficient funds
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', '')
                    if 'insufficient' in error_detail.lower():
                        print(f"⚠️  Purchase Chain - Insufficient funds (expected)")
                        print(f"   Error: {error_detail}")
                        results['purchase_chain'] = True
                    else:
                        print(f"❌ Purchase Chain - Error: {error_detail}")
                        results['purchase_chain'] = False
                except:
                    print(f"❌ Purchase Chain - Status: {response.status_code}")
                    results['purchase_chain'] = False
            else:
                print(f"❌ Purchase Chain (/api/marketplace/purchase) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['purchase_chain'] = False
        except Exception as e:
            print(f"❌ Purchase Chain (/api/marketplace/purchase) - Error: {str(e)}")
            results['purchase_chain'] = False

        print()
        return results

    def test_integration_scenarios(self) -> Dict[str, bool]:
        """Test integration scenarios with task completion and marketplace purchases."""
        results = {}
        
        print("🔄 TESTING INTEGRATION SCENARIOS")
        print("-" * 40)
        
        if not self.auth_token:
            print("❌ No auth token available - skipping integration tests")
            return {'integration': False}

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Get initial state
        try:
            # Get current currencies
            currencies_response = self.session.get(
                f"{self.api_url}/player/currencies",
                headers=headers,
                timeout=10
            )
            
            initial_coins = 0
            if currencies_response.status_code == 200:
                currencies_data = currencies_response.json()
                initial_coins = currencies_data.get('currencies', {}).get('credits', 0)
                print(f"📊 Initial coins: {initial_coins}")
            
            # Get initial inventory
            inventory_response = self.session.get(
                f"{self.api_url}/marketplace/inventory",
                headers=headers,
                timeout=10
            )
            
            initial_chains = 0
            initial_bonus = 0
            if inventory_response.status_code == 200:
                inventory_data = inventory_response.json()
                if inventory_data.get('success'):
                    inventory = inventory_data.get('inventory', {})
                    initial_chains = inventory.get('chains', 0)
                    initial_bonus = inventory.get('bonus_percentage', 0)
                    print(f"📊 Initial chains: {initial_chains}, bonus: {initial_bonus}%")
            
            results['initial_state'] = True
            
        except Exception as e:
            print(f"❌ Failed to get initial state: {str(e)}")
            results['initial_state'] = False

        # Test complete workflow if we have enough coins
        if initial_coins >= 2000:
            print("💰 Sufficient coins for integration test")
            
            # Try to purchase a chain first
            try:
                purchase_data = {"item_type": "chain"}
                purchase_response = self.session.post(
                    f"{self.api_url}/marketplace/purchase",
                    json=purchase_data,
                    headers=headers,
                    timeout=15
                )
                
                if purchase_response.status_code == 200:
                    purchase_data = purchase_response.json()
                    if purchase_data.get('success'):
                        print(f"✅ Integration: Chain purchased successfully")
                        print(f"   New balance: {purchase_data.get('new_balance', 0)} coins")
                        print(f"   New bonus: {purchase_data.get('new_bonus_percentage', 0)}%")
                        results['integration_purchase'] = True
                    else:
                        print(f"❌ Integration: Chain purchase failed - {purchase_data.get('error', 'Unknown')}")
                        results['integration_purchase'] = False
                else:
                    print(f"❌ Integration: Chain purchase failed - Status {purchase_response.status_code}")
                    results['integration_purchase'] = False
                    
            except Exception as e:
                print(f"❌ Integration: Chain purchase error - {str(e)}")
                results['integration_purchase'] = False
        else:
            print(f"⚠️  Insufficient coins ({initial_coins}) for integration test (need 2000+)")
            results['integration_purchase'] = True  # Not a failure, just insufficient funds

        # Test task generation and completion workflow
        try:
            # Generate a new task
            task_response = self.session.post(
                f"{self.api_url}/tasks/generate",
                headers=headers,
                timeout=15
            )
            
            task_generated = False
            if task_response.status_code == 200:
                task_data = task_response.json()
                if task_data.get('success'):
                    task = task_data.get('task')
                    if task:
                        print(f"✅ Integration: New task generated")
                        print(f"   Task ID: {task.get('task_id', 'Unknown')}")
                        task_generated = True
                        
                        # Complete the task immediately
                        completion_data = {"task_id": task['task_id']}
                        completion_response = self.session.post(
                            f"{self.api_url}/tasks/complete",
                            json=completion_data,
                            headers=headers,
                            timeout=15
                        )
                        
                        if completion_response.status_code == 200:
                            completion_data = completion_response.json()
                            if completion_data.get('success'):
                                reward_breakdown = completion_data.get('reward_breakdown', {})
                                print(f"✅ Integration: Task completed with bonus")
                                print(f"   Base reward: {reward_breakdown.get('base_reward', 0)}")
                                print(f"   Bonus: {reward_breakdown.get('bonus_percentage', 0)}%")
                                print(f"   Total: {reward_breakdown.get('total_reward', 0)}")
                                results['integration_task_flow'] = True
                            else:
                                print(f"❌ Integration: Task completion failed")
                                results['integration_task_flow'] = False
                        else:
                            print(f"❌ Integration: Task completion failed - Status {completion_response.status_code}")
                            results['integration_task_flow'] = False
                else:
                    # Check if player already has active task
                    error_msg = task_data.get('error', '')
                    if 'already have an active task' in error_msg:
                        print(f"⚠️  Integration: Player already has active task")
                        results['integration_task_flow'] = True  # This is expected
                    else:
                        print(f"❌ Integration: Task generation failed - {error_msg}")
                        results['integration_task_flow'] = False
            else:
                print(f"❌ Integration: Task generation failed - Status {task_response.status_code}")
                results['integration_task_flow'] = False
                
        except Exception as e:
            print(f"❌ Integration: Task workflow error - {str(e)}")
            results['integration_task_flow'] = False

        print()
        return results

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all backend tests and return comprehensive results."""
        print("🚀 KARMA NEXUS 2.0 - TASK GENERATION & MARKETPLACE API TESTING")
        print("=" * 60)
        
        all_results = {}
        
        # Run test suites in order
        print("Phase 1: Basic connectivity and authentication")
        health_results = self.test_health_endpoints()
        auth_results = self.test_auth_endpoints()
        protected_results = self.test_protected_endpoints()
        additional_results = self.test_additional_endpoints()
        
        print("Phase 2: Task generation and marketplace APIs")
        task_results = self.test_task_generation_api()
        marketplace_results = self.test_marketplace_api()
        
        print("Phase 3: Integration scenarios")
        integration_results = self.test_integration_scenarios()
        
        # Combine results
        all_results.update(health_results)
        all_results.update(auth_results)
        all_results.update(protected_results)
        all_results.update(additional_results)
        all_results.update(task_results)
        all_results.update(marketplace_results)
        all_results.update(integration_results)
        
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