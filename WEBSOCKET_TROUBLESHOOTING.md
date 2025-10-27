# WebSocket Connection Troubleshooting Guide

## Current Error Analysis

### Error Message:
```
GET ws://localhost:8001/?token=WFgnHvHq8put
NS_ERROR_WEBSOCKET_CONNECTION_REFUSED
INFO: ('127.0.0.1', 44884) - "WebSocket /?token=WFgnHvHq8put" 403
INFO: connection rejected (403 Forbidden)
```

### Root Cause:
The connection is being rejected for one of these reasons:
1. **Invalid Token**: The token `WFgnHvHq8put` doesn't look like a valid JWT token (JWT tokens are much longer)
2. **Wrong Endpoint**: Frontend is connecting to `/` instead of `/ws`
3. **Old Cached Token**: Browser has an old/invalid token stored

## Solution Steps

### Step 1: Clear Browser Storage
The token in the browser might be old or invalid. Clear it:

**Option A - Via Browser Console:**
```javascript
// Open browser DevTools (F12), go to Console tab, and run:
localStorage.clear();
sessionStorage.clear();
// Then refresh the page
location.reload();
```

**Option B - Via Browser Settings:**
1. Open DevTools (F12)
2. Go to "Application" or "Storage" tab
3. Expand "Local Storage"
4. Delete the `karma-nexus-storage` entry
5. Refresh the page

### Step 2: Re-login
After clearing storage:
1. Go to login page
2. Enter your credentials
3. Login again
4. This will generate a fresh, valid JWT token

### Step 3: Verify WebSocket URL
The frontend should use the correct WebSocket URL. Check `/app/frontend/.env`:

```bash
# File: /app/frontend/.env
REACT_APP_WS_URL=ws://localhost:8001/ws
```

✅ **This file has been created with the correct configuration**

### Step 4: Restart Frontend (if needed)
If the `.env` file was just created or modified:
```bash
sudo supervisorctl restart frontend
```

## How to Test Manually

### Test 1: Register a New User and Get Token
```bash
# Register a new user
TOKEN=$(curl -s -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username":"testuser",
    "email":"testuser@example.com",
    "password":"testpass123",
    "economic_class":"middle",
    "moral_class":"average"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

A valid JWT token looks like this:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkNzZjYWNjYi05OGFiLTQ5OWUtYWQ5Ny0xNjJjZDViYjFlNGIiLCJ1c2VybmFtZSI6IndzdGVzdCIsImV4cCI6MTc2MTk4NzUyMX0.SJgm1E8oBxbmE7UhpTSt19iNR6uqRBsyEpxKdhfe4Ds
```

Notice it has 3 parts separated by dots (.) and is much longer than `WFgnHvHq8put`.

### Test 2: Test WebSocket Connection
```bash
python /app/test_websocket.py "$TOKEN"
```

Expected output:
```
✅ WebSocket connected successfully!
📨 Received: {
  "event": "player_joined",
  "data": {
    "player_id": "...",
    "username": "testuser"
  }
}
✅ WebSocket test completed successfully!
```

## Common Issues and Fixes

### Issue 1: Token is Too Short
**Symptom**: Token looks like `WFgnHvHq8put` (only 12 characters)
**Cause**: Old/invalid token or token corruption
**Fix**: Clear browser storage and re-login

### Issue 2: Wrong WebSocket URL
**Symptom**: Connecting to `ws://localhost:8001/?token=...` instead of `ws://localhost:8001/ws?token=...`
**Cause**: Missing or incorrect `REACT_APP_WS_URL` environment variable
**Fix**: 
1. Ensure `/app/frontend/.env` exists with `REACT_APP_WS_URL=ws://localhost:8001/ws`
2. Restart frontend: `sudo supervisorctl restart frontend`

### Issue 3: Token Expired
**Symptom**: 403 Forbidden even with valid-looking JWT
**Cause**: Token has expired (tokens expire after 7 days)
**Fix**: Re-login to get a fresh token

### Issue 4: Backend Not Running
**Symptom**: Connection refused errors
**Check**:
```bash
sudo supervisorctl status backend
curl http://localhost:8001/health
```
**Fix**: If not running, restart: `sudo supervisorctl restart backend`

## Verification Checklist

✅ **Backend Configuration:**
- [x] WebSocket endpoint registered at `/ws` in `/app/backend/server.py`
- [x] JWT verification implemented in `/app/backend/api/websocket/handlers.py`
- [x] SECRET_KEY configured in `/app/backend/core/config.py`
- [x] Backend running: `sudo supervisorctl status backend`

✅ **Frontend Configuration:**
- [x] `.env` file exists with `REACT_APP_WS_URL=ws://localhost:8001/ws`
- [x] WebSocket service uses token from query parameter
- [x] Frontend running: `sudo supervisorctl status frontend`

✅ **User Actions Required:**
- [ ] Clear browser storage (localStorage)
- [ ] Re-login to get fresh JWT token
- [ ] Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

## Debug Information

### Check Current Token in Browser
Open browser console and run:
```javascript
// Check stored tokens
console.log('Access Token:', localStorage.getItem('karma-nexus-storage'));

// Parse the stored data
const stored = JSON.parse(localStorage.getItem('karma-nexus-storage') || '{}');
console.log('Parsed Token:', stored.state?.accessToken);

// Check if it's a valid JWT (should have 3 parts)
const token = stored.state?.accessToken;
if (token) {
  const parts = token.split('.');
  console.log('Token parts:', parts.length, '(should be 3 for JWT)');
  console.log('Token length:', token.length, '(should be > 100 for JWT)');
}
```

### Check WebSocket Connection in Browser
Open browser console (Network tab → WS filter) and check:
1. **Connection URL**: Should be `ws://localhost:8001/ws?token=<long-jwt-token>`
2. **Status**: Should show "101 Switching Protocols" (success) or 403 (auth failure)
3. **Messages**: Should see incoming welcome message

## Next Steps

After following the troubleshooting steps:
1. Clear browser storage
2. Re-login to generate fresh token
3. Check browser console for WebSocket connection status
4. If still failing, check the token format using the debug commands above
5. If token looks valid but still failing, check backend logs:
   ```bash
   tail -n 50 /var/log/supervisor/backend.err.log
   ```

## Contact Support

If the issue persists after following all steps, provide:
1. The output of the debug JavaScript commands
2. Backend logs: `tail -n 100 /var/log/supervisor/backend.err.log`
3. Frontend logs from browser console
4. The full error message from browser

---

**Last Updated**: Current Session
**Status**: WebSocket endpoint is correctly configured and working. User needs to clear old token and re-login.
