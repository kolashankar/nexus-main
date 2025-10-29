# Complete Solution - Authentication System

## Current Issues & Solutions

### Issue 1: MongoDB DNS Timeout ❌

**Error:**
```
pymongo.errors.ConfigurationError: The resolution lifetime expired after 21.126 seconds
```

**Cause:** Your MongoDB Atlas connection string has DNS resolution issues.

**Solutions (Choose ONE):**

#### Option A: Use Local MongoDB (Recommended for Development)
```bash
# Install MongoDB locally
sudo apt-get install mongodb

# Start MongoDB
sudo systemctl start mongodb

# Update backend/.env
MONGO_URL="mongodb+srv://pricecomparision057_db_user:aJHuxLkFGKkVVX9j@cluster0.2sx9gjg.mongodb.net/game_db?appName=Cluster0"
DB_NAME="karma_nexus"
```

#### Option B: Fix MongoDB Atlas Connection
1. Check your internet connection
2. Verify MongoDB Atlas cluster is running
3. Check if your IP is whitelisted in MongoDB Atlas
4. Try a different network (sometimes DNS is blocked)

#### Option C: Use Alternative MongoDB URL Format
Update `backend/.env`:
```
# Instead of mongodb+srv://, use direct connection
MONGO_URL="mongodb://cluster0-shard-00-00.dh7t48g.mongodb.net:27017,cluster0-shard-00-01.dh7t48g.mongodb.net:27017,cluster0-shard-00-02.dh7t48g.mongodb.net:27017/game_db?replicaSet=atlas-xxxxx-shard-0&ssl=true&authSource=admin"
```

### Issue 2: GEMINI_API_KEY Warning ⚠️

**Warning:**
```
WARNING:backend.services.ai.base:Oracle: No GEMINI_API_KEY found in environment
```

**Status:** This is just a WARNING, not an error. AI features are optional.

**To Fix (Optional):**
1. Ensure `.env` has the key without extra quotes:
   ```
   GEMINI_API_KEY=AIzaSyCrDnhg5VTo-XrfO1eoamZD9R6wVlqYSM
   ```
   (Remove the quotes around the value)

2. Restart the backend server

### Issue 3: 400 Bad Request on Register

**Possible Causes:**
- Username already exists
- Email already exists  
- Validation failed

**Solution:** Use the test script with random usernames:
```bash
./test_complete_auth.sh
```

### Issue 4: 422 Unprocessable Entity on Login

**Cause:** Request format is incorrect.

**Correct Format:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Common Mistakes:**
- Using "username" instead of "email"
- Missing Content-Type header
- Invalid JSON format

## Step-by-Step Setup

### Step 1: Fix MongoDB Connection

**Quick Fix - Use Local MongoDB:**

```bash
# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb

# Start MongoDB
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verify it's running
sudo systemctl status mongodb
```

**Update backend/.env:**
```bash
cd /home/cr7/Downloads/nexus-main/backend
nano .env
```

Change:
```
MONGO_URL="mongodb+srv://pricecomparision057_db_user:aJHuxLkFGKkVVX9j@cluster0.2sx9gjg.mongodb.net/game_db?appName=Cluster0"
DB_NAME="karma_nexus"
```

### Step 2: Start Backend

```bash
cd /home/cr7/Downloads/nexus-main/backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started server process [xxxxx]
INFO:     Application startup complete.
```

### Step 3: Test Backend

**In a NEW terminal:**
```bash
cd /home/cr7/Downloads/nexus-main
./test_complete_auth.sh
```

**Expected Output:**
```
✅ Backend is running
✅ Registration successful
✅ Login successful
✅ Get current user successful
✅ Logout successful
✅ ALL TESTS PASSED!
```

### Step 4: Start Frontend

**In ANOTHER terminal:**
```bash
cd /home/cr7/Downloads/nexus-main/frontend
npm run dev
```

**Expected Output:**
```
VITE v5.4.21  ready in XXX ms
➜  Local:   http://localhost:3000/
```

### Step 5: Test from Browser

1. Open http://localhost:3000
2. Open DevTools (F12) → Network tab
3. Try to register with NEW credentials:
   - Username: `player123`
   - Email: `player123@example.com`
   - Password: `password123`
4. Should see successful registration
5. Try to login with same credentials
6. Should receive access token

## Troubleshooting

### Backend Won't Start

**Check 1: MongoDB Connection**
```bash
# Test MongoDB
mongo --eval "db.version()"
# or
mongosh --eval "db.version()"
```

**Check 2: Port Already in Use**
```bash
# Kill existing process on port 8001
lsof -ti:8001 | xargs kill -9
```

**Check 3: Virtual Environment**
```bash
# Ensure venv is activated
which python
# Should show: /home/cr7/Downloads/nexus-main/backend/venv/bin/python
```

### Registration Fails with 400

**Solution 1: Clear Database**
```bash
mongo karma_nexus --eval "db.players.deleteMany({})"
```

**Solution 2: Use Different Credentials**
Try: `player${RANDOM}@example.com`

### Login Fails with 422

**Check Request Format:**
```bash
# Correct
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}'

# Wrong - using username instead of email
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'
```

### Frontend Can't Connect

**Check 1: Backend Running**
```bash
curl http://localhost:8001/health
```

**Check 2: Proxy Configuration**
Check `frontend/vite.config.js` has:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8001',
    changeOrigin: true,
  }
}
```

**Check 3: Environment Variables**
Check `frontend/.env` has:
```
VITE_BACKEND_URL=
VITE_WS_URL=/ws
```

## Quick Commands Reference

### Start Everything
```bash
# Terminal 1 - Backend
cd /home/cr7/Downloads/nexus-main/backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2 - Frontend  
cd /home/cr7/Downloads/nexus-main/frontend
npm run dev

# Terminal 3 - Test
cd /home/cr7/Downloads/nexus-main
./test_complete_auth.sh
```

### Stop Everything
```bash
# Stop backend
pkill -f "uvicorn server:app"

# Stop frontend
pkill -f "vite"
```

### Check Status
```bash
# Backend health
curl http://localhost:8001/health

# Frontend
curl http://localhost:3000

# Processes
ps aux | grep -E "uvicorn|vite"
```

## Files Modified

✅ `backend/core/database.py` - Fixed MongoDB connection timeout  
✅ `backend/core/security.py` - Fixed bcrypt compatibility  
✅ `backend/api/v1/auth/router.py` - Added /refresh endpoint  
✅ `backend/requirements.txt` - Pinned bcrypt version  
✅ `frontend/vite.config.js` - Fixed HMR configuration  
✅ `frontend/.env` - Updated environment variables  

## Test Scripts Created

📄 `test_complete_auth.sh` - Complete authentication test  
📄 `test_auth.sh` - Basic authentication test  
📄 `start-backend.sh` - Backend startup script  
📄 `start-frontend.sh` - Frontend startup script  

## Next Steps

1. ✅ Install local MongoDB (or fix Atlas connection)
2. ✅ Update `.env` with correct MONGO_URL
3. ✅ Start backend server
4. ✅ Run test script to verify
5. ✅ Start frontend
6. ✅ Test registration/login from browser

## Success Criteria

- [ ] Backend starts without errors
- [ ] `curl http://localhost:8001/health` returns `{"status":"healthy"}`
- [ ] `./test_complete_auth.sh` shows all tests passing
- [ ] Frontend loads at http://localhost:3000
- [ ] Can register new user from frontend
- [ ] Can login with registered user
- [ ] No connection errors in browser console

---

**Current Status:** MongoDB connection needs to be fixed before authentication can work.

**Recommended Action:** Install local MongoDB for development.
