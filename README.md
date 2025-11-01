# CareerGuide - Complete Job Portal Platform

<div align="center">

![CareerGuide](https://img.shields.io/badge/CareerGuide-Job%20Portal-blue)
![React Native](https://img.shields.io/badge/React%20Native-Expo-blue)
![Next.js](https://img.shields.io/badge/Next.js-15.5-black)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-green)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-green)

**A comprehensive job portal platform with Android mobile app, web application, and admin dashboard**

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Applications](#running-the-applications)
- [Build Commands](#build-commands)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)

---

## 🎯 Overview

CareerGuide is a complete job portal ecosystem consisting of:

1. **Mobile App (Expo React Native)** - Android app for end users
2. **Web Application (Next.js)** - Web platform for users  
3. **Admin Dashboard (Next.js)** - Web-based admin panel
4. **Backend API (FastAPI)** - Centralized REST API
5. **Database (MongoDB)** - NoSQL database

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CareerGuide Platform                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Mobile App  │  │   Web App    │  │Admin Dashboard│      │
│  │  (Expo RN)   │  │  (Next.js)   │  │  (Next.js)    │      │
│  │  Port: 3000  │  │  Port: 3002  │  │  Port: 3001   │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬────────┘      │
│         │                 │                  │                │
│         └─────────────────┼──────────────────┘                │
│                           │                                   │
│                  ┌────────▼────────┐                         │
│                  │   Backend API   │                         │
│                  │   (FastAPI)     │                         │
│                  │   Port: 8001    │                         │
│                  └────────┬────────┘                         │
│                           │                                   │
│                  ┌────────▼────────┐                         │
│                  │    MongoDB      │                         │
│                  │   Database      │                         │
│                  └─────────────────┘                         │
│                                                               │
│                  ┌─────────────────┐                         │
│                  │   Gemini API    │                         │
│                  │  (AI Services)  │                         │
│                  └─────────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend
- **Mobile:** Expo (React Native 0.79.5), TypeScript, NativeWind, Zustand, React Query
- **Web App:** Next.js 15.5.5, TypeScript, Tailwind CSS 4.0, Framer Motion
- **Admin:** Next.js 15.5.4, TypeScript, Chart.js, Monaco Editor, ReactFlow

### Backend
- **API:** FastAPI (Python)
- **Database:** MongoDB
- **Auth:** JWT
- **AI:** Google Gemini API

---

## ✨ Features

### All Apps
✅ Jobs, Internships, Scholarships (with filters, search, sort)
✅ Learning (Articles with categories, tags, reading progress)
✅ DSA Corner (Questions, Topics, Sheets, Companies, Progress tracking)
✅ Roadmaps (Interactive visual flowcharts)
✅ Career Tools (Resume Review, Cover Letter, ATS Hack, Cold Email - AI powered)
✅ Authentication & Profile Management

### Mobile App Only
✅ Offline support with auto-sync
✅ Push notifications
✅ Onboarding flow
✅ WhatsApp community integration

### Admin Dashboard Only
✅ AI content generation for all modules
✅ Analytics dashboard
✅ Bulk import/export (CSV/Excel)
✅ Content approval workflow
✅ Sub-admin management
✅ Push notifications management

---

## 🚀 Installation & Running

### Backend
```bash
cd backend
pip install -r requirements.txt
python seed_admin.py
python server.py  # Runs on http://localhost:8001
```

### Mobile App
```bash
cd user_app/frontend
yarn install
yarn start  # Runs on http://localhost:3000
```

### Admin Dashboard  
```bash
cd admin_dashboard/frontend
npm install
npm run dev  # Runs on http://localhost:3001
```

### Web App
```bash
cd web_app
npm install
npm run dev  # Runs on http://localhost:3002
```

---

## 🔨 Build Commands

### Mobile App
```bash
cd user_app/frontend
yarn lint
```

### Admin Dashboard
```bash
cd admin_dashboard/frontend
npm run build
```

### Web App
```bash
cd web_app
npm run build
```

---

## 🔐 Environment Variables

### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017/careerguide
JWT_SECRET=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

### Mobile App (.env)
```env
EXPO_PUBLIC_API_URL=http://localhost:8001
EXPO_BACKEND_URL=http://localhost:8001
```

---

## 📚 API Documentation

Full API documentation available at: **http://localhost:8001/docs** (when backend is running)

### Key Endpoints

**Authentication**
- POST /api/auth/user/register
- POST /api/auth/user/login  
- POST /api/auth/admin/login

**Jobs/Internships/Scholarships**
- GET/POST /api/admin/{module}
- POST /api/admin/{module}/generate-ai

**Learning**
- GET/POST /api/admin/articles
- GET /api/user/articles

**DSA**
- GET/POST /api/admin/dsa/questions
- GET/POST /api/admin/dsa/sheets
- POST /api/admin/dsa/questions/generate-ai

**Roadmaps**
- POST /api/admin/roadmaps/generate-ai
- POST /api/admin/roadmaps/{id}/nodes

**Career Tools** (Auth required)
- POST /api/career-tools/resume-review
- POST /api/career-tools/cover-letter
- POST /api/career-tools/ats-hack
- POST /api/career-tools/cold-email

---

## 🔑 Default Admin Credentials

**Email:** kolashankar113@gmail.com
**Password:** Shankar@113
**Role:** super_admin

⚠️ **Change these credentials after first login!**

---

## 📊 Implementation Status

| Component | Status | Features |
|-----------|--------|----------|
| Backend API | ✅ 100% | All modules complete |
| Mobile App | ✅ 100% | 8 phases complete |
| Web App | ✅ 100% | 8 phases complete |
| Admin Dashboard | ✅ 100% | Full admin functionality |

---

**CareerGuide** - Empowering careers through technology 🚀
