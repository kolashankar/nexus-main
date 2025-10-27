#!/bin/bash

echo "======================================"
echo "Gemini API Key Tester"
echo "======================================"
echo ""

cd backend
source venv/bin/activate

python << 'PYTHON_SCRIPT'
import sys
sys.path.insert(0, '..')
from backend.core.config import settings

print("1. Checking if API key is loaded...")
if settings.GEMINI_API_KEY:
    print(f"   ✅ Key found in config")
    print(f"   Length: {len(settings.GEMINI_API_KEY)} characters")
    print(f"   Preview: {settings.GEMINI_API_KEY[:15]}...{settings.GEMINI_API_KEY[-5:]}")
else:
    print("   ❌ No API key found in config")
    sys.exit(1)

print("\n2. Checking if google-generativeai is installed...")
try:
    import google.generativeai as genai
    print("   ✅ Package is installed")
except ImportError:
    print("   ❌ Package not installed")
    print("   Run: pip install google-generativeai")
    sys.exit(1)

print("\n3. Testing API key with Google Gemini...")
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    models = list(genai.list_models())
    
    if models:
        print(f"   ✅ API Key is VALID!")
        print(f"   ✅ Connected successfully")
        print(f"   ✅ Found {len(models)} available models")
        print(f"\n   Available models:")
        for model in models[:5]:
            print(f"      - {model.name}")
    else:
        print("   ⚠️  API Key accepted but no models available")
        
except Exception as e:
    error_msg = str(e)
    print(f"   ❌ API Key is INVALID")
    if "API_KEY_INVALID" in error_msg:
        print("   Reason: The API key is not valid")
        print("\n   How to fix:")
        print("   1. Go to: https://makersuite.google.com/app/apikey")
        print("   2. Create a new API key")
        print("   3. Update backend/.env with the new key")
        print("   4. Restart the backend server")
    elif "PERMISSION_DENIED" in error_msg:
        print("   Reason: API key doesn't have permission")
    else:
        print(f"   Error: {error_msg}")
    sys.exit(1)

print("\n======================================")
print("✅ ALL TESTS PASSED!")
print("======================================")
print("\nYour Gemini API key is working correctly.")
print("AI features are fully operational.")
PYTHON_SCRIPT

echo ""
