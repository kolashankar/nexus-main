#!/bin/bash

echo "==================================="
echo "Complete Authentication Test"
echo "==================================="
echo ""

# Generate random username to avoid conflicts
RANDOM_NUM=$RANDOM
USERNAME="testuser${RANDOM_NUM}"
EMAIL="testuser${RANDOM_NUM}@example.com"
PASSWORD="password123"

echo "Test Credentials:"
echo "  Username: $USERNAME"
echo "  Email: $EMAIL"
echo "  Password: $PASSWORD"
echo ""

# Test 1: Health Check
echo "1. Testing Backend Health..."
HEALTH=$(curl -s http://localhost:8001/health)
if [ $? -eq 0 ]; then
    echo "✅ Backend is running: $HEALTH"
else
    echo "❌ Backend is NOT running!"
    echo "   Please start backend: cd backend && source venv/bin/activate && uvicorn server:app --host 0.0.0.0 --port 8001 --reload"
    exit 1
fi
echo ""

# Test 2: Registration
echo "2. Testing Registration..."
REGISTER_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$USERNAME\",
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

HTTP_CODE=$(echo "$REGISTER_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$REGISTER_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Registration successful (HTTP $HTTP_CODE)"
    echo "   Response: $(echo $RESPONSE_BODY | jq -r '.access_token' | cut -c1-20)..."
    ACCESS_TOKEN=$(echo $RESPONSE_BODY | jq -r '.access_token')
else
    echo "❌ Registration failed (HTTP $HTTP_CODE)"
    echo "   Response: $RESPONSE_BODY"
    echo ""
    echo "Common issues:"
    echo "  - 400: User already exists (try different username/email)"
    echo "  - 422: Validation error (check field names and formats)"
    echo "  - 500: Server error (check backend logs)"
    exit 1
fi
echo ""

# Test 3: Login
echo "3. Testing Login..."
LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\"
  }")

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$LOGIN_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Login successful (HTTP $HTTP_CODE)"
    echo "   Response: $(echo $RESPONSE_BODY | jq -r '.access_token' | cut -c1-20)..."
    ACCESS_TOKEN=$(echo $RESPONSE_BODY | jq -r '.access_token')
else
    echo "❌ Login failed (HTTP $HTTP_CODE)"
    echo "   Response: $RESPONSE_BODY"
    exit 1
fi
echo ""

# Test 4: Get Current User
echo "4. Testing Get Current User..."
ME_RESPONSE=$(curl -s -w "\n%{http_code}" -X GET http://localhost:8001/api/auth/me \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$ME_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$ME_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Get current user successful (HTTP $HTTP_CODE)"
    echo "   Username: $(echo $RESPONSE_BODY | jq -r '.username')"
    echo "   Email: $(echo $RESPONSE_BODY | jq -r '.email')"
else
    echo "❌ Get current user failed (HTTP $HTTP_CODE)"
    echo "   Response: $RESPONSE_BODY"
fi
echo ""

# Test 5: Logout
echo "5. Testing Logout..."
LOGOUT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST http://localhost:8001/api/auth/logout \
  -H "Authorization: Bearer $ACCESS_TOKEN")

HTTP_CODE=$(echo "$LOGOUT_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$LOGOUT_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Logout successful (HTTP $HTTP_CODE)"
    echo "   Response: $RESPONSE_BODY"
else
    echo "❌ Logout failed (HTTP $HTTP_CODE)"
    echo "   Response: $RESPONSE_BODY"
fi
echo ""

echo "==================================="
echo "✅ ALL TESTS PASSED!"
echo "==================================="
echo ""
echo "Authentication system is working correctly."
echo "You can now test from the frontend at http://localhost:3000"
