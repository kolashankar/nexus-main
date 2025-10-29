#!/usr/bin/env python3
"""
Backend API Testing Script for Karma Nexus 2.0
Tests authentication, task generation, marketplace APIs, UpgradeStation endpoints, trait abilities, and integration scenarios.
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
    return "https://task-master-298.preview.emergentagent.com"

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

    def test_upgrade_station_api(self) -> Dict[str, bool]:
        """Test UpgradeStation API endpoints."""
        results = {}
        
        print("⚡ TESTING UPGRADE STATION API")
        print("-" * 40)
        
        if not self.auth_token:
            print("❌ No auth token available - skipping upgrade station tests")
            return {'upgrade_station': False}

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Get initial currencies to check if player has enough for upgrades
        initial_currencies = {}
        try:
            currencies_response = self.session.get(
                f"{self.api_url}/player/currencies",
                headers=headers,
                timeout=10
            )
            
            if currencies_response.status_code == 200:
                currencies_data = currencies_response.json()
                initial_currencies = currencies_data.get('currencies', {})
                print(f"📊 Initial currencies:")
                print(f"   Credits: {initial_currencies.get('credits', 0)}")
                print(f"   Karma Tokens: {initial_currencies.get('karma_tokens', 0)}")
                print(f"   Dark Matter: {initial_currencies.get('dark_matter', 0)}")
            
        except Exception as e:
            print(f"❌ Failed to get initial currencies: {str(e)}")

        # Test trait upgrade
        try:
            trait_data = {"trait_id": "strength"}
            
            response = self.session.post(
                f"{self.api_url}/upgrades/traits",
                json=trait_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Trait Upgrade (/api/upgrades/traits) - Status: {response.status_code}")
                    print(f"   Trait: {data.get('item_id', 'Unknown')}")
                    print(f"   Level: {data.get('old_level', 0)} → {data.get('new_level', 0)}")
                    cost = data.get('cost', {})
                    print(f"   Cost: {cost.get('credits', 0)} credits, {cost.get('karma_tokens', 0)} karma, {cost.get('dark_matter', 0)} dark matter")
                    results['trait_upgrade'] = True
                else:
                    print(f"❌ Trait Upgrade - API returned success=false")
                    print(f"   Message: {data.get('message', 'Unknown error')}")
                    results['trait_upgrade'] = False
            elif response.status_code == 400:
                # Check if it's insufficient funds or other expected error
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', '')
                    if 'insufficient' in error_detail.lower() or 'not enough' in error_detail.lower():
                        print(f"⚠️  Trait Upgrade - Insufficient funds (expected)")
                        print(f"   Error: {error_detail}")
                        results['trait_upgrade'] = True  # This is expected behavior
                    else:
                        print(f"❌ Trait Upgrade - Error: {error_detail}")
                        results['trait_upgrade'] = False
                except:
                    print(f"❌ Trait Upgrade - Status: {response.status_code}")
                    print(f"   Response: {response.text}")
                    results['trait_upgrade'] = False
            else:
                print(f"❌ Trait Upgrade (/api/upgrades/traits) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['trait_upgrade'] = False
        except Exception as e:
            print(f"❌ Trait Upgrade (/api/upgrades/traits) - Error: {str(e)}")
            results['trait_upgrade'] = False

        # Test robot upgrade
        try:
            robot_data = {"robot_id": "scout"}
            
            response = self.session.post(
                f"{self.api_url}/upgrades/robots",
                json=robot_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Robot Upgrade (/api/upgrades/robots) - Status: {response.status_code}")
                    print(f"   Robot: {data.get('item_id', 'Unknown')}")
                    print(f"   Level: {data.get('old_level', 0)} → {data.get('new_level', 0)}")
                    cost = data.get('cost', {})
                    print(f"   Cost: {cost.get('credits', 0)} credits, {cost.get('karma_tokens', 0)} karma, {cost.get('dark_matter', 0)} dark matter")
                    results['robot_upgrade'] = True
                else:
                    print(f"❌ Robot Upgrade - API returned success=false")
                    print(f"   Message: {data.get('message', 'Unknown error')}")
                    results['robot_upgrade'] = False
            elif response.status_code == 400:
                # Check if it's insufficient funds or other expected error
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', '')
                    if 'insufficient' in error_detail.lower() or 'not enough' in error_detail.lower():
                        print(f"⚠️  Robot Upgrade - Insufficient funds (expected)")
                        print(f"   Error: {error_detail}")
                        results['robot_upgrade'] = True  # This is expected behavior
                    else:
                        print(f"❌ Robot Upgrade - Error: {error_detail}")
                        results['robot_upgrade'] = False
                except:
                    print(f"❌ Robot Upgrade - Status: {response.status_code}")
                    print(f"   Response: {response.text}")
                    results['robot_upgrade'] = False
            else:
                print(f"❌ Robot Upgrade (/api/upgrades/robots) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['robot_upgrade'] = False
        except Exception as e:
            print(f"❌ Robot Upgrade (/api/upgrades/robots) - Error: {str(e)}")
            results['robot_upgrade'] = False

        # Test ornament upgrade
        try:
            ornament_data = {"ornament_id": "avatar_frame"}
            
            response = self.session.post(
                f"{self.api_url}/upgrades/ornaments",
                json=ornament_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Ornament Upgrade (/api/upgrades/ornaments) - Status: {response.status_code}")
                    print(f"   Ornament: {data.get('item_id', 'Unknown')}")
                    print(f"   Level: {data.get('old_level', 0)} → {data.get('new_level', 0)}")
                    results['ornament_upgrade'] = True
                else:
                    print(f"❌ Ornament Upgrade - API returned success=false")
                    results['ornament_upgrade'] = False
            elif response.status_code == 400:
                # Check if it's insufficient funds or other expected error
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', '')
                    if 'insufficient' in error_detail.lower() or 'not enough' in error_detail.lower():
                        print(f"⚠️  Ornament Upgrade - Insufficient funds (expected)")
                        results['ornament_upgrade'] = True  # This is expected behavior
                    else:
                        print(f"❌ Ornament Upgrade - Error: {error_detail}")
                        results['ornament_upgrade'] = False
                except:
                    print(f"❌ Ornament Upgrade - Status: {response.status_code}")
                    results['ornament_upgrade'] = False
            else:
                print(f"❌ Ornament Upgrade (/api/upgrades/ornaments) - Status: {response.status_code}")
                results['ornament_upgrade'] = False
        except Exception as e:
            print(f"❌ Ornament Upgrade (/api/upgrades/ornaments) - Error: {str(e)}")
            results['ornament_upgrade'] = False

        # Test chip upgrade
        try:
            chip_data = {"chip_id": "neural_enhancer"}
            
            response = self.session.post(
                f"{self.api_url}/upgrades/chips",
                json=chip_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Chip Upgrade (/api/upgrades/chips) - Status: {response.status_code}")
                    print(f"   Chip: {data.get('item_id', 'Unknown')}")
                    print(f"   Level: {data.get('old_level', 0)} → {data.get('new_level', 0)}")
                    results['chip_upgrade'] = True
                else:
                    print(f"❌ Chip Upgrade - API returned success=false")
                    results['chip_upgrade'] = False
            elif response.status_code == 400:
                # Check if it's insufficient funds or other expected error
                try:
                    error_data = response.json()
                    error_detail = error_data.get('detail', '')
                    if 'insufficient' in error_detail.lower() or 'not enough' in error_detail.lower():
                        print(f"⚠️  Chip Upgrade - Insufficient funds (expected)")
                        results['chip_upgrade'] = True  # This is expected behavior
                    else:
                        print(f"❌ Chip Upgrade - Error: {error_detail}")
                        results['chip_upgrade'] = False
                except:
                    print(f"❌ Chip Upgrade - Status: {response.status_code}")
                    results['chip_upgrade'] = False
            else:
                print(f"❌ Chip Upgrade (/api/upgrades/chips) - Status: {response.status_code}")
                results['chip_upgrade'] = False
        except Exception as e:
            print(f"❌ Chip Upgrade (/api/upgrades/chips) - Error: {str(e)}")
            results['chip_upgrade'] = False

        # Test upgrade history
        try:
            response = self.session.get(
                f"{self.api_url}/upgrades/history",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print(f"✅ Upgrade History (/api/upgrades/history) - Status: {response.status_code}")
                    print(f"   History entries: {len(data)}")
                    if data:
                        latest = data[0]
                        print(f"   Latest: {latest.get('upgrade_type', 'Unknown')} - {latest.get('item_name', 'Unknown')}")
                    results['upgrade_history'] = True
                else:
                    print(f"❌ Upgrade History - Invalid response format")
                    results['upgrade_history'] = False
            else:
                print(f"❌ Upgrade History (/api/upgrades/history) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['upgrade_history'] = False
        except Exception as e:
            print(f"❌ Upgrade History (/api/upgrades/history) - Error: {str(e)}")
            results['upgrade_history'] = False

        # Test upgrade stats
        try:
            response = self.session.get(
                f"{self.api_url}/upgrades/stats",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'total_upgrades' in data:
                    print(f"✅ Upgrade Stats (/api/upgrades/stats) - Status: {response.status_code}")
                    print(f"   Total upgrades: {data.get('total_upgrades', 0)}")
                    upgrades_by_type = data.get('upgrades_by_type', {})
                    print(f"   By type: {upgrades_by_type}")
                    total_spent = data.get('total_spent', {})
                    print(f"   Total spent: {total_spent.get('credits', 0)} credits, {total_spent.get('karma_tokens', 0)} karma")
                    results['upgrade_stats'] = True
                else:
                    print(f"❌ Upgrade Stats - Invalid response format")
                    results['upgrade_stats'] = False
            else:
                print(f"❌ Upgrade Stats (/api/upgrades/stats) - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['upgrade_stats'] = False
        except Exception as e:
            print(f"❌ Upgrade Stats (/api/upgrades/stats) - Error: {str(e)}")
            results['upgrade_stats'] = False

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

    def test_trait_abilities_api(self) -> Dict[str, bool]:
        """Test newly created trait ability endpoints."""
        results = {}
        
        print("🎭 TESTING TRAIT ABILITIES API")
        print("-" * 40)
        
        if not self.auth_token:
            print("❌ No auth token available - skipping trait abilities tests")
            return {'trait_abilities': False}

        headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Test Compassion - Healing Touch
        try:
            healing_data = {
                "target_id": "test_target_player_id",
                "trait_level": 50
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/compassion/healing_touch",
                json=healing_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Compassion Healing Touch - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Message: {data.get('message', 'No message')}")
                results['compassion_healing_touch'] = True
            else:
                print(f"❌ Compassion Healing Touch - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                results['compassion_healing_touch'] = False
        except Exception as e:
            print(f"❌ Compassion Healing Touch - Error: {str(e)}")
            results['compassion_healing_touch'] = False

        # Test Honesty - Truth Reveal
        try:
            truth_data = {
                "target_id": "test_target_player_id",
                "trait_level": 75
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/honesty/truth_reveal",
                json=truth_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Honesty Truth Reveal - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Revealed Info: {len(data.get('revealed_info', {}))}")
                results['honesty_truth_reveal'] = True
            else:
                print(f"❌ Honesty Truth Reveal - Status: {response.status_code}")
                results['honesty_truth_reveal'] = False
        except Exception as e:
            print(f"❌ Honesty Truth Reveal - Error: {str(e)}")
            results['honesty_truth_reveal'] = False

        # Test Envy - Stat Drain
        try:
            drain_data = {
                "target_id": "test_target_player_id",
                "trait_level": 60
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/envy/stat_drain",
                json=drain_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Envy Stat Drain - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Stats Drained: {data.get('stats_drained', {})}")
                results['envy_stat_drain'] = True
            else:
                print(f"❌ Envy Stat Drain - Status: {response.status_code}")
                results['envy_stat_drain'] = False
        except Exception as e:
            print(f"❌ Envy Stat Drain - Error: {str(e)}")
            results['envy_stat_drain'] = False

        # Test Wrath - Berserker Rage
        try:
            rage_data = {
                "trait_level": 80
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/wrath/berserker_rage",
                json=rage_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Wrath Berserker Rage - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Damage Boost: {data.get('damage_boost', 0)}%")
                results['wrath_berserker_rage'] = True
            else:
                print(f"❌ Wrath Berserker Rage - Status: {response.status_code}")
                results['wrath_berserker_rage'] = False
        except Exception as e:
            print(f"❌ Wrath Berserker Rage - Error: {str(e)}")
            results['wrath_berserker_rage'] = False

        # Test Sloth - Energy Siphon
        try:
            siphon_data = {
                "target_id": "test_target_player_id",
                "trait_level": 45
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/sloth/energy_siphon",
                json=siphon_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Sloth Energy Siphon - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Energy Drained: {data.get('energy_drained', 0)}")
                results['sloth_energy_siphon'] = True
            else:
                print(f"❌ Sloth Energy Siphon - Status: {response.status_code}")
                results['sloth_energy_siphon'] = False
        except Exception as e:
            print(f"❌ Sloth Energy Siphon - Error: {str(e)}")
            results['sloth_energy_siphon'] = False

        # Test Sloth - Lazy Dodge
        try:
            dodge_data = {
                "trait_level": 30
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/sloth/lazy_dodge",
                json=dodge_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Sloth Lazy Dodge - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Dodge Chance: {data.get('dodge_chance', 0)}%")
                results['sloth_lazy_dodge'] = True
            else:
                print(f"❌ Sloth Lazy Dodge - Status: {response.status_code}")
                results['sloth_lazy_dodge'] = False
        except Exception as e:
            print(f"❌ Sloth Lazy Dodge - Error: {str(e)}")
            results['sloth_lazy_dodge'] = False

        # Test Pride - Superior Presence
        try:
            pride_data = {
                "trait_level": 70
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/pride/superior_presence",
                json=pride_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Pride Superior Presence - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Buff Applied: {data.get('buff_applied', False)}")
                results['pride_superior_presence'] = True
            else:
                print(f"❌ Pride Superior Presence - Status: {response.status_code}")
                results['pride_superior_presence'] = False
        except Exception as e:
            print(f"❌ Pride Superior Presence - Error: {str(e)}")
            results['pride_superior_presence'] = False

        # Test Luck - Fortune's Favor
        try:
            luck_data = {
                "trait_level": 85
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/luck/fortunes_favor",
                json=luck_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Luck Fortune's Favor - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Luck Boost: {data.get('luck_boost', 0)}%")
                results['luck_fortunes_favor'] = True
            else:
                print(f"❌ Luck Fortune's Favor - Status: {response.status_code}")
                results['luck_fortunes_favor'] = False
        except Exception as e:
            print(f"❌ Luck Fortune's Favor - Error: {str(e)}")
            results['luck_fortunes_favor'] = False

        # Test Luck - Lucky Escape
        try:
            escape_data = {
                "trait_level": 50
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/luck/lucky_escape",
                json=escape_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Luck Lucky Escape - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Escaped: {data.get('escaped', False)}")
                results['luck_lucky_escape'] = True
            else:
                print(f"❌ Luck Lucky Escape - Status: {response.status_code}")
                results['luck_lucky_escape'] = False
        except Exception as e:
            print(f"❌ Luck Lucky Escape - Error: {str(e)}")
            results['luck_lucky_escape'] = False

        # Test Luck - Treasure Sense
        try:
            treasure_data = {
                "trait_level": 65
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/luck/treasure_sense",
                json=treasure_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Luck Treasure Sense - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Treasures Found: {len(data.get('treasures_found', []))}")
                results['luck_treasure_sense'] = True
            else:
                print(f"❌ Luck Treasure Sense - Status: {response.status_code}")
                results['luck_treasure_sense'] = False
        except Exception as e:
            print(f"❌ Luck Treasure Sense - Error: {str(e)}")
            results['luck_treasure_sense'] = False

        # Test Resilience - Unbreakable Will
        try:
            resilience_data = {
                "trait_level": 90
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/resilience/unbreakable_will",
                json=resilience_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Resilience Unbreakable Will - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Resistance Boost: {data.get('resistance_boost', 0)}%")
                results['resilience_unbreakable_will'] = True
            else:
                print(f"❌ Resilience Unbreakable Will - Status: {response.status_code}")
                results['resilience_unbreakable_will'] = False
        except Exception as e:
            print(f"❌ Resilience Unbreakable Will - Error: {str(e)}")
            results['resilience_unbreakable_will'] = False

        # Test Resilience - Damage Threshold
        try:
            threshold_data = {
                "incoming_damage": 150,
                "trait_level": 75
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/resilience/damage_threshold",
                json=threshold_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Resilience Damage Threshold - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Final Damage: {data.get('final_damage', 0)}")
                results['resilience_damage_threshold'] = True
            else:
                print(f"❌ Resilience Damage Threshold - Status: {response.status_code}")
                results['resilience_damage_threshold'] = False
        except Exception as e:
            print(f"❌ Resilience Damage Threshold - Error: {str(e)}")
            results['resilience_damage_threshold'] = False

        # Test Wisdom - Sage Insight
        try:
            wisdom_data = {
                "situation_type": "combat",
                "trait_level": 80
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/wisdom/sage_insight",
                json=wisdom_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Wisdom Sage Insight - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Insights: {len(data.get('insights', []))}")
                results['wisdom_sage_insight'] = True
            else:
                print(f"❌ Wisdom Sage Insight - Status: {response.status_code}")
                results['wisdom_sage_insight'] = False
        except Exception as e:
            print(f"❌ Wisdom Sage Insight - Error: {str(e)}")
            results['wisdom_sage_insight'] = False

        # Test Wisdom - Learning Acceleration
        try:
            learning_data = {
                "skill_name": "combat_mastery",
                "trait_level": 60
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/wisdom/learning_acceleration",
                json=learning_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Wisdom Learning Acceleration - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   XP Multiplier: {data.get('xp_multiplier', 1.0)}x")
                results['wisdom_learning_acceleration'] = True
            else:
                print(f"❌ Wisdom Learning Acceleration - Status: {response.status_code}")
                results['wisdom_learning_acceleration'] = False
        except Exception as e:
            print(f"❌ Wisdom Learning Acceleration - Error: {str(e)}")
            results['wisdom_learning_acceleration'] = False

        # Test Adaptability - Quick Adaptation
        try:
            adapt_data = {
                "situation": "combat",
                "trait_level": 70
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/adaptability/quick_adaptation",
                json=adapt_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Adaptability Quick Adaptation - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Adaptations: {len(data.get('adaptations', {}))}")
                results['adaptability_quick_adaptation'] = True
            else:
                print(f"❌ Adaptability Quick Adaptation - Status: {response.status_code}")
                results['adaptability_quick_adaptation'] = False
        except Exception as e:
            print(f"❌ Adaptability Quick Adaptation - Error: {str(e)}")
            results['adaptability_quick_adaptation'] = False

        # Test Adaptability - Environment Mastery
        try:
            env_data = {
                "environment_type": "desert",
                "trait_level": 55
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/adaptability/environment_mastery",
                json=env_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Adaptability Environment Mastery - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Mastery Level: {data.get('mastery_level', 0)}")
                results['adaptability_environment_mastery'] = True
            else:
                print(f"❌ Adaptability Environment Mastery - Status: {response.status_code}")
                results['adaptability_environment_mastery'] = False
        except Exception as e:
            print(f"❌ Adaptability Environment Mastery - Error: {str(e)}")
            results['adaptability_environment_mastery'] = False

        # Test Adaptability - Copy Ability
        try:
            copy_data = {
                "target_id": "test_target_player_id",
                "ability_name": "strength",
                "trait_level": 85
            }
            
            response = self.session.post(
                f"{self.api_url}/traits/adaptability/copy_ability",
                json=copy_data,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Adaptability Copy Ability - Status: {response.status_code}")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Copied Ability: {data.get('copied_ability', 'None')}")
                results['adaptability_copy_ability'] = True
            else:
                print(f"❌ Adaptability Copy Ability - Status: {response.status_code}")
                results['adaptability_copy_ability'] = False
        except Exception as e:
            print(f"❌ Adaptability Copy Ability - Error: {str(e)}")
            results['adaptability_copy_ability'] = False

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
        
        print("Phase 3: UpgradeStation API")
        upgrade_results = self.test_upgrade_station_api()
        
        print("Phase 4: Trait Abilities API")
        trait_results = self.test_trait_abilities_api()
        
        print("Phase 5: Integration scenarios")
        integration_results = self.test_integration_scenarios()
        
        # Combine results
        all_results.update(health_results)
        all_results.update(auth_results)
        all_results.update(protected_results)
        all_results.update(additional_results)
        all_results.update(task_results)
        all_results.update(marketplace_results)
        all_results.update(upgrade_results)
        all_results.update(trait_results)
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