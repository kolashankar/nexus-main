#!/usr/bin/env python3
"""
Character Update Endpoint Testing for Karma Nexus 2.0
Focused test for the newly integrated character update functionality.
"""

import requests
import json
import sys

def test_character_update():
    """Test the character update endpoint specifically."""
    
    base_url = "https://navmesh-roadways.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("🎮 KARMA NEXUS 2.0 - CHARACTER UPDATE ENDPOINT TEST")
    print("=" * 60)
    print(f"Backend URL: {base_url}")
    print(f"API URL: {api_url}")
    print()
    
    # Test user credentials
    test_user = {
        "email": "karma.nexus.tester@gametest.com", 
        "password": "GameTest2024!"
    }
    
    session = requests.Session()
    auth_token = None
    
    # Step 1: Login to get auth token
    print("🔐 Step 1: Authentication")
    print("-" * 30)
    
    try:
        login_response = session.post(
            f"{api_url}/auth/login",
            json=test_user,
            timeout=10
        )
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            auth_token = login_data.get('access_token')
            print(f"✅ Login successful - Token received: {'Yes' if auth_token else 'No'}")
            print(f"   User: {login_data.get('player', {}).get('username', 'Unknown')}")
        else:
            print(f"❌ Login failed - Status: {login_response.status_code}")
            print(f"   Response: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False
    
    if not auth_token:
        print("❌ No auth token - cannot proceed with character update test")
        return False
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Step 2: Get current profile
    print("\n📋 Step 2: Get Current Profile")
    print("-" * 30)
    
    try:
        profile_response = session.get(
            f"{api_url}/player/profile",
            headers=headers,
            timeout=10
        )
        
        if profile_response.status_code == 200:
            current_profile = profile_response.json()
            print(f"✅ Current profile retrieved")
            print(f"   Username: {current_profile.get('username', 'Unknown')}")
            print(f"   Current character_model: {current_profile.get('character_model', 'None')}")
            print(f"   Current appearance: {current_profile.get('appearance', {})}")
        else:
            print(f"❌ Failed to get profile - Status: {profile_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Profile retrieval error: {str(e)}")
        return False
    
    # Step 3: Test character update
    print("\n🎨 Step 3: Character Update Test")
    print("-" * 30)
    
    # Character update data as specified in the review request
    character_update_data = {
        "character_model": "female_athletic",
        "skin_tone": "medium",
        "hair_color": "brown",
        "appearance": {
            "model": "female_athletic",
            "skin_tone": "medium",
            "hair_color": "brown"
        }
    }
    
    print(f"📝 Updating character with:")
    print(f"   Model: {character_update_data['character_model']}")
    print(f"   Skin Tone: {character_update_data['skin_tone']}")
    print(f"   Hair Color: {character_update_data['hair_color']}")
    
    try:
        update_response = session.put(
            f"{api_url}/player/profile",
            json=character_update_data,
            headers=headers,
            timeout=15
        )
        
        if update_response.status_code == 200:
            update_data = update_response.json()
            print(f"✅ Character update successful - Status: {update_response.status_code}")
            
            # Check if the response includes updated fields
            updated_character_model = update_data.get('character_model')
            updated_appearance = update_data.get('appearance', {})
            
            print(f"   Updated character_model: {updated_character_model}")
            print(f"   Updated appearance: {updated_appearance}")
            
            # Verify the update was applied correctly
            if updated_character_model == character_update_data['character_model']:
                print("✅ Character model updated correctly")
            else:
                print(f"⚠️  Character model mismatch: expected {character_update_data['character_model']}, got {updated_character_model}")
            
            if updated_appearance.get('model') == character_update_data['appearance']['model']:
                print("✅ Appearance model updated correctly")
            else:
                print(f"⚠️  Appearance model mismatch")
                
        else:
            print(f"❌ Character update failed - Status: {update_response.status_code}")
            print(f"   Response: {update_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Character update error: {str(e)}")
        return False
    
    # Step 4: Verify persistence by fetching profile again
    print("\n🔍 Step 4: Verify Update Persistence")
    print("-" * 30)
    
    try:
        verify_response = session.get(
            f"{api_url}/player/profile",
            headers=headers,
            timeout=10
        )
        
        if verify_response.status_code == 200:
            updated_profile = verify_response.json()
            print(f"✅ Profile retrieved for verification")
            
            # Check if changes persisted
            persisted_model = updated_profile.get('character_model')
            persisted_appearance = updated_profile.get('appearance', {})
            
            print(f"   Persisted character_model: {persisted_model}")
            print(f"   Persisted appearance: {persisted_appearance}")
            
            # Verify persistence
            if persisted_model == character_update_data['character_model']:
                print("✅ Character model changes persisted correctly")
            else:
                print(f"❌ Character model not persisted: expected {character_update_data['character_model']}, got {persisted_model}")
                return False
            
            if persisted_appearance.get('model') == character_update_data['appearance']['model']:
                print("✅ Appearance changes persisted correctly")
            else:
                print(f"❌ Appearance not persisted correctly")
                return False
                
        else:
            print(f"❌ Failed to verify persistence - Status: {verify_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {str(e)}")
        return False
    
    print("\n🎉 CHARACTER UPDATE TEST COMPLETED SUCCESSFULLY!")
    print("✅ All character update functionality is working correctly")
    return True

def test_feature_endpoints():
    """Test if feature endpoints are registered (not necessarily working)."""
    
    base_url = "https://navmesh-roadways.preview.emergentagent.com"
    api_url = f"{base_url}/api"
    
    print("\n🔍 FEATURE ENDPOINTS REGISTRATION TEST")
    print("=" * 60)
    
    # Test user credentials for authentication
    test_user = {
        "email": "karma.nexus.tester@gametest.com", 
        "password": "GameTest2024!"
    }
    
    session = requests.Session()
    
    # Get auth token
    try:
        login_response = session.post(f"{api_url}/auth/login", json=test_user, timeout=10)
        if login_response.status_code == 200:
            auth_token = login_response.json().get('access_token')
            headers = {"Authorization": f"Bearer {auth_token}"}
        else:
            print("❌ Could not authenticate for feature endpoint tests")
            return {}
    except:
        print("❌ Authentication failed for feature endpoint tests")
        return {}
    
    # Feature endpoints to test
    feature_endpoints = {
        "Initial Tasks": f"{api_url}/tasks/initial",
        "Marketplace Robots": f"{api_url}/marketplace/robots", 
        "Available Upgrades": f"{api_url}/upgrades/available",
        "Trait Actions": f"{api_url}/traits/actions"
    }
    
    results = {}
    
    for feature_name, endpoint in feature_endpoints.items():
        try:
            response = session.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 404:
                print(f"❌ {feature_name} - NOT REGISTERED (404)")
                results[feature_name] = "not_registered"
            elif response.status_code in [200, 401, 403, 500]:
                print(f"✅ {feature_name} - REGISTERED (Status: {response.status_code})")
                results[feature_name] = "registered"
            else:
                print(f"⚠️  {feature_name} - UNKNOWN STATUS ({response.status_code})")
                results[feature_name] = "unknown"
                
        except Exception as e:
            print(f"❌ {feature_name} - ERROR: {str(e)}")
            results[feature_name] = "error"
    
    return results

def main():
    """Main test execution."""
    
    # Test character update functionality
    character_test_passed = test_character_update()
    
    # Test feature endpoint registration
    feature_results = test_feature_endpoints()
    
    # Summary
    print("\n📊 FINAL TEST SUMMARY")
    print("=" * 60)
    
    print(f"Character Update Endpoint: {'✅ WORKING' if character_test_passed else '❌ FAILED'}")
    
    print("\nFeature Endpoint Registration:")
    for feature, status in feature_results.items():
        if status == "registered":
            print(f"✅ {feature}: Registered")
        elif status == "not_registered":
            print(f"❌ {feature}: Not Registered (404)")
        else:
            print(f"⚠️  {feature}: {status}")
    
    # Overall assessment
    registered_count = sum(1 for status in feature_results.values() if status == "registered")
    total_features = len(feature_results)
    
    print(f"\nOverall Status:")
    print(f"- Character Update: {'✅ Working' if character_test_passed else '❌ Failed'}")
    print(f"- Feature Endpoints: {registered_count}/{total_features} registered")
    
    if character_test_passed and registered_count >= 2:
        print("\n🎉 CORE FUNCTIONALITY IS WORKING!")
        return True
    else:
        print("\n⚠️  SOME ISSUES DETECTED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)