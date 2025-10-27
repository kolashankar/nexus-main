# Troubleshooting Guide

## Frontend "Connection Lost" / Continuous Polling Issue

### Problem
Frontend shows "server connection is lost, polling to restart" and continuously restarts.

### Root Causes & Solutions

#### 1. ✅ FIXED: HMR (Hot Module Replacement) Configuration

**Problem:** Vite's HMR was configured to use a remote WebSocket server (`api-connect-setup.preview.emergentagent.com`) which caused connection failures in local development.

**Solution:** Updated `frontend/vite.config.js` to use local HMR:
```javascript
hmr: {
  protocol: 'ws',
  host: 'localhost',
  port: 3000,
}
```

#### 2. ✅ FIXED: Environment Variables

**Problem:** Environment variables had incorrect values pointing to absolute URLs instead of using Vite's proxy.

**Solution:** Updated `frontend/.env` to use proxy-friendly values:
```bash
# Use empty string to leverage Vite's proxy
VITE_BACKEND_URL=
REACT_APP_BACKEND_URL=

# Use relative path for WebSocket
VITE_WS_URL=/ws
REACT_APP_WS_URL=/ws
```

#### 3. How Vite Proxy Works

The `vite.config.js` has proxy configuration:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8001',
    changeOrigin: true,
  },
  '/ws': {
    target: 'ws://localhost:8001',
    ws: true,
    changeOrigin: true,
  },
}
```

This means:
- Frontend requests to `/api/*` → proxied to `http://localhost:8001/api/*`
- Frontend WebSocket to `/ws` → proxied to `ws://localhost:8001/ws`

### Verification Steps

1. **Check Backend is Running:**
   ```bash
   curl http://localhost:8001/health
   # Should return: {"status":"healthy"}
   ```

2. **Check Frontend Environment:**
   ```bash
   cd frontend
   cat .env
   # Verify VITE_BACKEND_URL is empty or uses proxy path
   ```

3. **Restart Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Check Browser Console:**
   - Open DevTools (F12)
   - Look for WebSocket connection in Network tab
   - Should connect to `ws://localhost:3000/ws` (which proxies to backend)

### Common Issues

#### Issue: "WebSocket connection failed"
**Solution:** Ensure backend is running on port 8001

#### Issue: "CORS errors"
**Solution:** Check `backend/.env` has correct ALLOWED_ORIGINS:
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8001
```

#### Issue: "404 on /api requests"
**Solution:** Verify Vite proxy is configured correctly in `vite.config.js`

#### Issue: "Connection keeps dropping"
**Solution:** 
1. Check if backend is stable (not restarting)
2. Verify HMR configuration uses localhost
3. Clear browser cache and restart dev server

### Files Modified to Fix This Issue

1. `frontend/vite.config.js` - Fixed HMR configuration
2. `frontend/.env` - Updated environment variables
3. `frontend/.env.example` - Updated template with correct values

### Testing the Fix

1. **Start Backend:**
   ```bash
   ./start-backend.sh
   # Or manually:
   cd backend
   source venv/bin/activate
   uvicorn server:app --host 0.0.0.0 --port 8001 --reload
   ```

2. **Start Frontend:**
   ```bash
   ./start-frontend.sh
   # Or manually:
   cd frontend
   npm run dev
   ```

3. **Verify Connection:**
   - Open http://localhost:3000
   - Check browser console for errors
   - WebSocket should connect successfully
   - No continuous polling/restart messages

### Production Deployment

For production, update environment variables to use actual URLs:

**Frontend `.env.production`:**
```bash
VITE_BACKEND_URL=https://your-backend-domain.com
VITE_WS_URL=wss://your-backend-domain.com/ws
```

**Backend `.env`:**
```bash
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

---

## Backend Auto-Restart Issue

See `DEPLOYMENT_STATUS.md` for details on the `ALLOWED_ORIGINS` configuration fix.

---

## Quick Checklist

- [ ] Backend running on port 8001
- [ ] Backend health check returns `{"status":"healthy"}`
- [ ] Frontend `.env` uses empty string for `VITE_BACKEND_URL`
- [ ] Frontend `.env` uses `/ws` for `VITE_WS_URL`
- [ ] Vite HMR uses localhost, not remote host
- [ ] No CORS errors in browser console
- [ ] WebSocket connects successfully

---

## Need More Help?

1. Check backend logs for errors
2. Check browser DevTools console
3. Check browser DevTools Network tab for failed requests
4. Verify both servers are running on correct ports
5. Try clearing browser cache and localStorage
