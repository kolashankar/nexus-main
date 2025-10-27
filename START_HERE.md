# 🚀 Quick Start Guide - Karma Nexus

## Prerequisites

- Python 3.12+ with venv
- Node.js 16+ and npm
- MongoDB (local or remote)
- Redis (optional, for caching)

## First Time Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and update:
# - MONGO_URL (your MongoDB connection string)
# - SECRET_KEY (generate a secure key)
# - GEMINI_API_KEY (optional, for AI features)
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# The .env file should have:
# VITE_BACKEND_URL= (empty, uses proxy)
# VITE_WS_URL=/ws (relative path, uses proxy)
```

## Running the Application

### Option 1: Using Helper Scripts (Recommended)

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Verify Everything Works

1. **Backend Health Check:**
   ```bash
   curl http://localhost:8001/health
   # Should return: {"status":"healthy"}
   ```

2. **Backend API Docs:**
   Open http://localhost:8001/docs in your browser

3. **Frontend:**
   Open http://localhost:3000 in your browser

4. **Check for Errors:**
   - Backend: Look at terminal output
   - Frontend: Open browser DevTools (F12) and check Console

## Common Issues

### Backend won't start
- ✅ Check MongoDB is running and accessible
- ✅ Verify `.env` file exists with correct values
- ✅ Ensure virtual environment is activated
- ✅ Check `ALLOWED_ORIGINS` in `.env` includes `http://localhost:3000`

### Frontend shows "Connection Lost"
- ✅ Ensure backend is running on port 8001
- ✅ Check `.env` has `VITE_BACKEND_URL=` (empty)
- ✅ Check `.env` has `VITE_WS_URL=/ws`
- ✅ Clear browser cache and restart dev server
- ✅ See `TROUBLESHOOTING.md` for detailed fixes

### CORS Errors
- ✅ Update `backend/.env` ALLOWED_ORIGINS to include your frontend URL
- ✅ Default: `ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8001`

## Project Structure

```
nexus-main/
├── backend/              # FastAPI backend
│   ├── api/             # API routes
│   ├── models/          # Data models
│   ├── services/        # Business logic
│   ├── core/            # Core configuration
│   └── server.py        # Main entry point
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API clients
│   │   ├── hooks/       # Custom hooks
│   │   └── pages/       # Page components
│   └── vite.config.js   # Vite configuration
├── start-backend.sh     # Backend start script
├── start-frontend.sh    # Frontend start script
└── TROUBLESHOOTING.md   # Detailed troubleshooting
```

## Access URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8001
- **API Documentation:** http://localhost:8001/docs
- **Health Check:** http://localhost:8001/health

## Development Workflow

1. Make changes to code
2. Backend auto-reloads (with `--reload` flag)
3. Frontend hot-reloads automatically
4. Check browser console for errors
5. Check terminal for backend errors

## Testing

**Backend Tests:**
```bash
cd backend
source venv/bin/activate
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

## Production Deployment

See `docs/technical/deployment.md` for production deployment instructions.

## Need Help?

1. Check `TROUBLESHOOTING.md` for common issues
2. Check `DEPLOYMENT_STATUS.md` for recent fixes
3. Review backend logs in terminal
4. Check browser DevTools console

## Recent Fixes Applied

✅ Fixed backend auto-restart issue (ALLOWED_ORIGINS parsing)  
✅ Fixed frontend connection loss (HMR configuration)  
✅ Fixed import errors in backend  
✅ Created missing `src/lib/utils.js` for shadcn/ui  
✅ Updated environment variable configuration  

All systems operational! 🎮
