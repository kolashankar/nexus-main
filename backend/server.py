"""Main FastAPI server entry point."""
import sys
import os
from pathlib import Path

# Add parent directory to path for backend imports
# This is necessary for modules inside 'backend' to be found by the imports below
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings

# Explicitly import all routers from their respective router files.
# This approach helps prevent common import errors, including circular dependencies,
# that might occur when relying on implicit package imports via __init__.py files.
from backend.api.v1.auth.router import router as auth_router
from backend.api.v1.player.router import router as player_router
from backend.api.v1.actions.router import router as actions_router
from backend.api.v1.combat.router import router as combat_router
from backend.api.v1.robots.router import router as robots_router
from backend.api.v1.guilds.router import router as guilds_router
from backend.api.v1.quests.router import router as quests_router
from backend.api.v1.market.router import router as market_router
from backend.api.v1.social.router import router as social_router
from backend.api.v1.karma.router import router as karma_router
from backend.api.v1.leaderboards.router import router as leaderboards_router
from backend.api.v1.tournaments.router import router as tournaments_router
from backend.api.v1.achievements.router import router as achievements_router
from backend.api.v1.ai.companion.router import router as ai_companion_router
from backend.api.v1.world.router import router as world_router
from backend.api.v1.seasonal.router import router as seasonal_router
from backend.api.v1.tasks.router import router as tasks_router
from backend.api.v1.marketplace.router import router as marketplace_router
from backend.api.v1.upgrades.router import router as upgrades_router
from backend.api.v1.traits.actions import router as trait_actions_router
from backend.api.websocket.handlers import websocket_endpoint


# Create FastAPI app
app = FastAPI(
    title="Karma Nexus API",
    description="Next-generation AI-driven multiplayer game",
    version="2.0.0"
)

# Configure CORS - Use settings from config
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers using the explicitly imported and renamed variables
app.include_router(auth_router, prefix="/api")
app.include_router(player_router, prefix="/api")
app.include_router(actions_router, prefix="/api")
app.include_router(combat_router, prefix="/api")
app.include_router(robots_router, prefix="/api")
app.include_router(guilds_router, prefix="/api")
app.include_router(quests_router, prefix="/api")
app.include_router(market_router, prefix="/api")
app.include_router(social_router, prefix="/api")
app.include_router(karma_router, prefix="/api")
app.include_router(leaderboards_router, prefix="/api")
app.include_router(tournaments_router, prefix="/api")
app.include_router(achievements_router, prefix="/api")
app.include_router(ai_companion_router, prefix="/api")
app.include_router(world_router, prefix="/api")
app.include_router(seasonal_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")
app.include_router(marketplace_router, prefix="/api")
app.include_router(upgrades_router, prefix="/api")
app.include_router(trait_actions_router, prefix="/api/traits")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Karma Nexus API",
        "version": "2.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Register WebSocket endpoint
app.websocket("/ws")(websocket_endpoint)


# Import spawner task
from backend.tasks.world_item_spawner import start_spawner, stop_spawner


@app.on_event("startup")
async def startup_event():
    """Start background tasks and services on application startup."""
    print("\n" + "="*60)
    print("\ud83c\udf89 KARMA NEXUS 2.0 - BACKEND STARTING")
    print("="*60)
    
    # Database connection
    print("\ud83d\udcbe Connecting to MongoDB...")
    from backend.core.database import get_database
    try:
        db = await get_database().__anext__()
        # Test database connection
        await db.command('ping')
        print("\u2705 MongoDB connected successfully!")
    except Exception as e:
        print(f"\u274c MongoDB connection failed: {e}")
    
    # Gemini AI initialization
    print("\ud83e\udd16 Initializing Gemini AI Task Generator...")
    try:
        from backend.services.ai.task_generator import TaskGenerator
        task_gen = TaskGenerator()
        print("\u2705 Gemini AI initialized successfully!")
    except Exception as e:
        print(f"\u26a0\ufe0f Gemini AI initialization warning: {e}")
    
    # World item spawner
    print("\ud83c\udf0e Starting world item spawner...")
    try:
        await start_spawner()
        print("\u2705 World item spawner started successfully!")
    except Exception as e:
        print(f"\u26a0\ufe0f World spawner warning: {e}")
    
    print("\n\u2728 BACKEND READY!")
    print(f"\ud83d\ude80 API available at: http://0.0.0.0:8001")
    print(f"\ud83d\udcda API Docs: http://0.0.0.0:8001/docs")
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop background tasks on application shutdown."""
    print("[Server] Stopping world item spawner...")
    await stop_spawner()
    print("[Server] World item spawner stopped")


if __name__ == "__main__":
    import uvicorn
    # Make sure your environment variables (like GEMINI_API_KEY) are set before running this.
    uvicorn.run(app, host="0.0.0.0", port=8001)
