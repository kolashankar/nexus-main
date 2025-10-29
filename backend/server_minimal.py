"""Minimal FastAPI server for testing frontend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="Karma Nexus API",
    description="Next-generation AI-driven multiplayer game",
    version="2.0.0"
)

# CORS
origins = [
    "http://localhost:3000",
    "https://cityscape-adapt.preview.emergentagent.com"
]
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Karma Nexus 2.0 API", "status": "running"}

@app.get("/api/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/status")
async def status():
    return {"status": "ok", "version": "2.0.0"}
