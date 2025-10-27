"""AI API Endpoints"""
from fastapi import APIRouter

# Import sub-routers
try:
    from .companion.router import router as companion_router
except ImportError:
    companion_router = None

try:
    from .karma_arbiter.router import router as karma_arbiter_router
except ImportError:
    karma_arbiter_router = None

try:
    from .oracle.router import router as oracle_router
except ImportError:
    oracle_router = None

# Create combined router
router = APIRouter(prefix="/ai", tags=["AI"])

# Include sub-routers
if companion_router:
    router.include_router(companion_router)
if karma_arbiter_router:
    router.include_router(karma_arbiter_router)
if oracle_router:
    router.include_router(oracle_router)

__all__ = ["router"]
