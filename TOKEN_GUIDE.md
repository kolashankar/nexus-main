# Complete Token Guide - Step by Step

## Part 1: How to Check Your Current Token

### Option A: Using Browser Console (Easiest)

1. **Open your browser** (Chrome, Firefox, Safari, etc.)
2. **Open Developer Tools**:
   - Windows/Linux: Press `F12` or `Ctrl + Shift + I`
   - Mac: Press `Cmd + Option + I`
3. **Click on "Console" tab** at the top
4. **Copy and paste this command** into the console and press Enter:

```javascript
const stored = JSON.parse(localStorage.getItem('karma-nexus-storage') || '{}');
const token = stored.state?.accessToken;
console.log('========== YOUR TOKEN INFO ==========');
console.log('Token:', token);
console.log('Token Length:', token ? token.length : 0);
console.log('Is Valid JWT?', token ? token.split('.').length === 3 : false);
console.log('====================================');
```

5. **Read the output:**
   - ✅ **Valid token**: Length > 100, Has 3 parts (Is Valid JWT? = true)
   - ❌ **Invalid token**: Length < 50, Has 1 part (Is Valid JWT? = false)
   - ❌ **No token**: Shows "null" or "undefined"

### Option B: Using Browser Storage Tab

1. Open Developer Tools (F12)
2. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
3. Look in the left sidebar:
   - Expand "Local Storage"
   - Click on your site URL (e.g., `http://localhost:3000`)
4. Find the key: `karma-nexus-storage`
5. Look at the "Value" column - you'll see JSON data
6. Look for `"accessToken":"..."` in the JSON

---

## Part 2: How to Create/Get a Fresh Token

You have **3 ways** to get a token:

### Method 1: Via Web Interface (Recommended for Users)

#### If You Already Have an Account:
1. **Go to login page**: `http://localhost:3000/login`
2. **Enter your credentials**:
   - Email: (your registered email)
   - Password: (your password)
3. **Click "Login" button**
4. ✅ **Token is automatically created and stored** in browser
5. You're redirected to dashboard - **WebSocket connects automatically**

#### If You Don't Have an Account:
1. **Go to register page**: `http://localhost:3000/register`
2. **Fill in the form**:
   - Username: (choose a username)
   - Email: (your email)
   - Password: (choose a password, min 8 characters)
   - Confirm Password: (same password)
   - Economic Class: (select one - middle, rich, poor)
   - Moral Class: (select one - average, good, evil)
3. **Click "Register" button**
4. ✅ **Account created and token automatically generated**
5. You're redirected to dashboard

### Method 2: Via Command Line (For Testing/Development)

#### Register New User and Get Token:
```bash
# Replace with your details
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "myusername",
    "email": "myemail@example.com",
    "password": "mypassword123",
    "economic_class": "middle",
    "moral_class": "average"
  }' | jq -r '.access_token'
```

This will print your token. **Copy it!**

#### Login and Get Token (If User Already Exists):
```bash
# Replace with your credentials
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "myemail@example.com",
    "password": "mypassword123"
  }' | jq -r '.access_token'
```

This will print your token. **Copy it!**

### Method 3: Via API Testing Tool (Postman/Insomnia)

1. **Open Postman or Insomnia**
2. **Create a POST request to**: `http://localhost:8001/api/auth/login`
3. **Set Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
4. **Set Body (JSON)**:
```json
{
  "email": "your-email@example.com",
  "password": "yourpassword"
}
```
5. **Send the request**
6. **Copy the token** from the response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "player": {...}
}
```
Copy the value of `access_token`.

---

## Part 3: Where to Use/Paste the Token

### Scenario A: Testing WebSocket Manually (Command Line)

If you got a token from command line and want to test WebSocket:

```bash
# Paste your token here (replace YOUR_TOKEN_HERE)
python /app/test_websocket.py "YOUR_TOKEN_HERE"
```

**Example:**
```bash
python /app/test_websocket.py "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkNzZjYWNjYi05OGFiLTQ5OWUtYWQ5Ny0xNjJjZDViYjFlNGIiLCJ1c2VybmFtZSI6IndzdGVzdCIsImV4cCI6MTc2MTk4NzUyMX0.SJgm1E8oBxbmE7UhpTSt19iNR6uqRBsyEpxKdhfe4Ds"
```

### Scenario B: Using the Web Application (Normal Usage)

**You DON'T need to paste the token manually!**

When you login via the web interface:
1. Token is **automatically stored** in browser localStorage
2. Token is **automatically used** by the WebSocket service
3. WebSocket **automatically connects** when you're logged in

**Just login normally** and everything works automatically! 🎉

### Scenario C: Testing API Endpoints Manually

If you want to test other API endpoints with your token:

#### Using curl:
```bash
# Replace YOUR_TOKEN with your actual token
curl -X GET http://localhost:8001/api/player/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Using Postman/Insomnia:
1. Create a GET request to: `http://localhost:8001/api/player/profile`
2. Go to "Authorization" or "Headers" tab
3. Add header:
   - Key: `Authorization`
   - Value: `Bearer YOUR_TOKEN` (replace YOUR_TOKEN)
4. Send request

### Scenario D: Fixing WebSocket Connection Issues

If WebSocket isn't connecting, paste token in browser console to test:

1. Open browser console (F12)
2. Get your token (see Part 1)
3. **Manually test WebSocket connection**:

```javascript
// Paste this in console (replace YOUR_TOKEN)
const token = 'YOUR_TOKEN_HERE';
const ws = new WebSocket(`ws://localhost:8001/ws?token=${token}`);

ws.onopen = () => console.log('✅ WebSocket connected!');
ws.onerror = (err) => console.error('❌ WebSocket error:', err);
ws.onmessage = (msg) => console.log('📨 Message:', msg.data);
ws.onclose = (event) => console.log('🔌 WebSocket closed:', event.code, event.reason);
```

---

## Quick Troubleshooting

### Problem: "Token is null or undefined"
**Solution:** You need to login first
```
1. Go to http://localhost:3000/login
2. Login with your credentials
3. Token will be automatically created
```

### Problem: "Token is too short" or "Invalid JWT"
**Solution:** Clear storage and login again
```javascript
// Run in browser console:
localStorage.clear();
sessionStorage.clear();
location.reload();
// Then login again
```

### Problem: "I forgot my password"
**Solution:** Register a new account
```
1. Go to http://localhost:3000/register
2. Use a different email
3. Register new account
```

### Problem: "Email already registered"
**Solution:** Use login instead of register
```
1. Go to http://localhost:3000/login
2. Enter your email and password
3. Click Login
```

---

## Complete Example Workflow

### For a New User (First Time):

1. **Register an account:**
   - Go to: `http://localhost:3000/register`
   - Fill form and submit
   - ✅ Token automatically created

2. **Verify token is stored:**
   - Press F12 → Console tab
   - Run: `console.log(localStorage.getItem('karma-nexus-storage'))`
   - Should see JSON with `accessToken`

3. **Check WebSocket connection:**
   - Stay on the page after login
   - Open Console tab (F12)
   - Look for: `WebSocket: Connected successfully`
   - ✅ If you see this, everything is working!

### For Existing User (Already Have Account):

1. **Clear old token (if having issues):**
```javascript
localStorage.clear();
location.reload();
```

2. **Login:**
   - Go to: `http://localhost:3000/login`
   - Enter credentials
   - Click Login
   - ✅ Fresh token created

3. **Verify connection:**
   - Check console for: `WebSocket: Connected successfully`

---

## Token Format Reference

### ✅ Valid JWT Token Example:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkNzZjYWNjYi05OGFiLTQ5OWUtYWQ5Ny0xNjJjZDViYjFlNGIiLCJ1c2VybmFtZSI6IndzdGVzdCIsImV4cCI6MTc2MTk4NzUyMX0.SJgm1E8oBxbmE7UhpTSt19iNR6uqRBsyEpxKdhfe4Ds
```
- **Length**: 150-300 characters
- **Parts**: 3 parts separated by dots (.)
- **Structure**: `header.payload.signature`

### ❌ Invalid Token Examples:
```
WFgnHvHq8put          ❌ Too short (only 12 chars)
null                  ❌ No token
undefined             ❌ No token
eyJhbGciOi           ❌ Incomplete token
```

---

## Still Having Issues?

### Check These:

1. **Backend is running:**
```bash
sudo supervisorctl status backend
curl http://localhost:8001/health
# Should return: {"status":"healthy"}
```

2. **Frontend is running:**
```bash
sudo supervisorctl status frontend
curl http://localhost:3000
# Should return HTML
```

3. **WebSocket endpoint is accessible:**
```bash
curl -i http://localhost:8001/ws
# Should return: 426 Upgrade Required (this is correct for WebSocket)
```

4. **Create a test token and verify it works:**
```bash
# Get a fresh token
TOKEN=$(curl -s -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"test'$(date +%s)'",
    "email":"test'$(date +%s)'@example.com",
    "password":"testpass123",
    "economic_class":"middle",
    "moral_class":"average"
  }' | jq -r '.access_token')

# Test the token
echo "Token: $TOKEN"
python /app/test_websocket.py "$TOKEN"
```

If this test works (✅), then the backend is fine and you just need to login via the web interface!

---

**Need More Help?**
- See: `/app/WEBSOCKET_TROUBLESHOOTING.md` for detailed troubleshooting
- See: `/app/WEBSOCKET_FIX_SUMMARY.md` for technical details
