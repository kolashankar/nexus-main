# Authentication Errors Fix Guide

### Errors You're Seeing

```
POST http://localhost:3000/api/auth/register [HTTP/1.1 500 Internal Server Error 5181ms]
POST http://localhost:3000/api/auth/login [HTTP/1.1 422 Unprocessable Entity 101ms]
```

## Root Cause

The **backend server is not running** on port 8001. The frontend is proxying requests to `http://localhost:8001` but nothing is listening there.

## Solution

### Step 1: Start the Backend Server

**Option A: Using the helper script**
```bash
./start-backend.sh
```

**Option B: Manually**
```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

### Step 2: Verify Backend is Running

```bash
curl http://localhost:8001/health
# Should return: {"status":"healthy"}
```

### Step 3: Test Registration

```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "economic_class": "middle",
    "moral_class": "average"
  }'
```

### Step 4: Restart Frontend (if needed)

```bash
cd frontend
npm run dev
```

## Understanding the Errors

### 500 Internal Server Error on /register
**Cause:** Backend not running or database connection issue

**Check:**
1. Is backend running? `curl http://localhost:8001/health`
2. Is MongoDB accessible? Check `backend/.env` MONGO_URL
3. Check backend terminal for error messages

### 422 Unprocessable Entity on /login
**Cause:** Validation error - missing or incorrect request fields

**Required fields for login:**
```json
{
  "email": "user@example.com",  // Must be valid email
  "password": "password123"      // Required
}
```

**Required fields for registration:**
```json
{
  "username": "testuser",        // 3-30 characters
  "email": "test@example.com",   // Valid email
  "password": "testpass123",     // Min 8 characters
  "economic_class": "middle",    // Optional, default: "middle"
  "moral_class": "average"       // Optional, default: "average"
}
```

## MongoDB Configuration

Your current setup uses MongoDB Atlas (cloud):
```bash
MONGO_URL="mongodb+srv://kolashankar:L4jgVKdl7MNHlKiv@cluster0.dh7t48g.mongodb.net/game_db?appName=cluster0"
DB_NAME="game_db"
```

✅ Connection tested and working!

## Complete Startup Checklist

### Terminal 1: Backend
```bash
cd /home/cr7/Downloads/nexus-main
./start-backend.sh
```

**Expected output:**
```
Starting Karma Nexus Backend Server...
=======================================

INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started server process [xxxxx]
INFO:     Application startup complete.
```

### Terminal 2: Frontend
```bash
cd /home/cr7/Downloads/nexus-main
./start-frontend.sh
```

**Expected output:**
```
Starting Karma Nexus Frontend Server...
========================================

VITE v5.4.21  ready in XXX ms
➜  Local:   http://localhost:3000/
```

### Terminal 3: Test (Optional)
```bash
cd /home/cr7/Downloads/nexus-main
./test_auth.sh
```

## Debugging Tips

### Check if Backend is Running
```bash
# Check process
ps aux | grep uvicorn

# Check port
lsof -i :8001
# or
netstat -tulpn | grep 8001
```

### Check Backend Logs
Look at the terminal where you started the backend for error messages.

### Check Frontend Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try to register/login
4. Click on the failed request
5. Check:
   - Request URL (should be `http://localhost:3000/api/auth/...`)
   - Request payload (what data was sent)
   - Response (error message from backend)

### Common Issues

**Issue: "Failed to connect to localhost port 8001"**
- Backend is not running
- Start backend with `./start-backend.sh`

**Issue: "CORS error"**
- Check `backend/.env` has: `ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8001`

**Issue: "MongoDB connection failed"**
- Check internet connection (using MongoDB Atlas)
- Verify MONGO_URL in `backend/.env`
- Check MongoDB Atlas cluster is running

**Issue: "422 Validation Error"**
- Check request payload has all required fields
- Email must be valid format
- Password must be at least 8 characters
- Username must be 3-30 characters

## Test Script

A test script has been created at `test_auth.sh`:

```bash
chmod +x test_auth.sh
./test_auth.sh
```

This will test both registration and login endpoints directly.

## API Endpoints

### Register
- **URL:** `POST /api/auth/register`
- **Body:**
  ```json
  {
    "username": "string (3-30 chars)",
    "email": "valid@email.com",
    "password": "string (min 8 chars)",
    "economic_class": "middle|lower|upper (optional)",
    "moral_class": "average|good|evil (optional)"
  }
  ```
- **Response:** `{ "access_token": "...", "token_type": "bearer", "player": {...} }`

### Login
- **URL:** `POST /api/auth/login`
- **Body:**
  ```json
  {
    "email": "valid@email.com",
    "password": "string"
  }
  ```
- **Response:** `{ "access_token": "...", "token_type": "bearer", "player": {...} }`

## Next Steps

1. ✅ Ensure backend is running on port 8001
2. ✅ Verify MongoDB connection
3. ✅ Test endpoints with curl or test script
4. ✅ Try registration/login from frontend
5. ✅ Check browser console for any errors

---

**Status:** MongoDB connected ✅ | Backend configured ✅ | Frontend configured ✅

**Action Required:** Start the backend server!
